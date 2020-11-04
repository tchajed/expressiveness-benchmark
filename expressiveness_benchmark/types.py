import json
import os
import sqlite3
import subprocess as sp
import tempfile
from dataclasses import dataclass, field, replace
from glob import glob
from pathlib import Path
from typing import Any, Dict, List

import ipywidgets as widgets
import pandas as pd
from dataclasses_json import dataclass_json
from IPython.display import display

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


class Base:
    def validate(self):
        pass

    def save(self):
        self.validate()

        p = Path(self.fname())
        p.parent.mkdir(parents=True, exist_ok=True)

        with p.open("w") as f:
            f.write(self.to_json())

    def load(self):
        return self.from_json(open(self.fname(), "r").read())


@dataclass_json
@dataclass
class Plan:
    id: str
    description: str


@dataclass_json
@dataclass
class Task(Base):
    id: str
    category: str = ""
    description: str = ""
    plan: List[Plan] = field(default_factory=list)
    sample_input: Dict[str, List[Dict[str, Any]]] = field(default_factory=dict)
    sample_output: Any = None

    def fname(self):
        return os.path.join(DATA_DIR, "tasks", f"{self.id}.json")

    def validate(self):
        assert self.sample_input is not None
        assert self.sample_output is not None


@dataclass_json
@dataclass
class Language(Base):
    id: str
    name: str

    def fname(self):
        return os.path.join(DATA_DIR, "languages", f"{self.id}.json")


@dataclass_json
@dataclass
class SourceRange:
    line: int
    start: int
    end: int


@dataclass_json
@dataclass
class Program(Base):
    task: str
    language: str
    plan: Dict[str, List[SourceRange]] = field(default_factory=dict)
    source: str = ""
    author: str = ""
    implementation: str = ""

    def fname(self):
        return os.path.join(
            DATA_DIR,
            "programs",
            self.task,
            f"{self.language}_{self.implementation}_{self.author}.json",
        )

    def validate(self):
        try:
            Task(id=self.task).load()
        except FileNotFoundError:
            assert False, f"{self.task} is not a valid task"
        assert self.author != "", "Author must not be empty"
        assert self.source != "", "Source must not be empty"
        assert self.language in LANGUAGES, f"{self.language} is not a valid language"

    def load_plan(self):
        try:
            saved_self = self.load()
            return replace(self, plan=saved_self.plan)
        except FileNotFoundError:
            return self

    def widget(self, task):
        from code_widget.example import CodeWidget

        widget = CodeWidget(program=self.to_json(), task=task.to_json())
        output = widgets.Output()
        display(output)

        def save_plan_changes(changes):
            with output:
                if changes["name"] == "plan":
                    plan = json.loads(changes["new"])
                    replace(self, plan=plan).save()
                elif changes["name"] == "source":
                    replace(self, source=changes["new"]).save()

        widget.observe(save_plan_changes, names=["plan", "source"])

        return widget

    def to_dataframe(self, value):
        if isinstance(value, pd.DataFrame):
            return value

        if isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                return pd.DataFrame(value)
            else:
                return pd.DataFrame([[el] for el in value])
        else:
            return pd.DataFrame([value])

    def check_equals(self, target, actual):
        target = self.to_dataframe(target)
        actual = self.to_dataframe(actual)

        try:
            target = target.sort_values(by=target.columns[0], ignore_index=True)
            actual = actual.sort_values(by=target.columns[0], ignore_index=True)

            if not target.equals(actual):
                assert False
        except Exception:
            print("Mismatch between target and actual output.")
            print("Target: ", target)
            print("Actual: ", actual)
            raise

    def execute(self, task):
        dataframes = {}
        for table_name, table in task.sample_input.items():
            df = pd.DataFrame(table)
            dataframes[table_name] = df.reindex(sorted(df.columns), axis=1)

        if "python" in self.language:
            globls = {}
            imports = [
                "import pandas as pd",
                "import numpy as np",
                "from collections import defaultdict",
            ]

            exec(
                "\n".join(imports) + "\n" + self.source,
                globls,
                globls,
            )

            args = [
                f"{k}=pd.DataFrame({v})" if "pandas" in self.language else f"{k}={v}"
                for k, v in task.sample_input.items()
            ]

            call = f"{task.id}({', '.join(args)})"
            ret = eval(call, globls, globls)

        elif self.language == "sql":
            conn = sqlite3.connect(":memory:")

            # https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
            def dict_factory(cursor, row):
                d = {}
                for idx, col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d

            conn.row_factory = dict_factory

            try:
                for table_name, df in dataframes.items():
                    df.to_sql(table_name, con=conn)
                conn.commit()
                c = conn.cursor()

                commands = self.source.split(";")
                for cmd in commands:
                    c.execute(cmd)

                ret = c.fetchall()
                if len(ret) > 0 and len(ret[0]) == 1:
                    ret = [r[list(r.keys())[0]] for r in ret]

            finally:
                conn.close()

        elif self.language == "datalog":

            def columns_to_relation(df):
                type_map = {"int64": "number", "object": "symbol", "float64": "float"}

                def convert_name(c):
                    try:
                        int(c)
                        return f"x{c}"
                    except ValueError:
                        return c

                return [
                    f"{convert_name(c)}:{type_map[str(df[c].dtype)]}"
                    for c in df.columns
                ]

            prelude = []
            for table_name, df in dataframes.items():
                columns = columns_to_relation(df)
                prelude.append(f'.decl {table_name}({", ".join(columns)})')
                prelude.append(f".input {table_name}")

            output_df = self.to_dataframe(task.sample_output)
            columns = columns_to_relation(output_df)
            prelude.append(f'.decl {task.id}({", ".join(columns)})')
            prelude.append(f".output {task.id}")
            prelude = "\n".join(prelude)

            program = prelude + "\n" + self.source

            with tempfile.TemporaryDirectory() as path:
                with open(f"{path}/program.dl", "w") as f:
                    f.write(program)

                for table_name, df in dataframes.items():
                    df.to_csv(
                        f"{path}/{table_name}.facts",
                        sep="\t",
                        index=False,
                        header=False,
                    )

                try:
                    sp.check_output(
                        "souffle -F. -D. program.dl",
                        cwd=path,
                        shell=True,
                        stderr=sp.PIPE,
                    )
                except sp.CalledProcessError as e:
                    print(e.stderr.decode("utf-8"))
                    raise

                try:
                    ret = pd.read_csv(
                        f"{path}/{task.id}.csv",
                        sep="\t",
                        header=None,
                        names=output_df.columns.tolist(),
                    )
                except pd.errors.EmptyDataError:
                    ret = pd.DataFrame()

        self.check_equals(task.sample_output, ret)


def load_all_programs():
    programs = glob(os.path.join(DATA_DIR, "programs", "*.json"))
    return [Program.from_json(open(p).read()) for p in programs]


LANGUAGES = {
    l.id: l
    for l in [
        Language(id="python-imperative", name="Python (Imperative)"),
        Language(id="python-functional", name="Python (Functional)"),
        Language(id="python-pandas", name="Python (Pandas)"),
        Language(id="sql", name="SQL"),
        Language(id="datalog", name="Datalog"),
    ]
}


def save_languages():
    for l in LANGUAGES.values():
        l.save()