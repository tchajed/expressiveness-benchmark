_N_E=(window.webpackJsonp_N_E=window.webpackJsonp_N_E||[]).push([[10],{"/EDR":function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/",function(){return n("23aj")}])},"20a2":function(e,t,n){e.exports=n("nOHt")},"23aj":function(e,t,n){"use strict";n.r(t),n.d(t,"default",(function(){return b}));var s=n("ODXe"),a=n("nKUr"),c=n("q1tI"),r=n("LvDl"),i=n.n(r),o=n("/4Ii"),l=n("YFqc"),d=n.n(l),j=n("20a2"),h=n("I7Fo"),u=function(e){var t=e.program,n=e.task;return Object(a.jsx)(h.a,{program:t,task:n,width:"160px",height:"100px",show_plan:!1,editor_props:{showGutter:!1,fontSize:4}})};function b(){var e=Object(j.useRouter)(),t=Object(c.useState)(null),n=t[0],r=t[1],l=i.a.groupBy(o.e,"category"),h=o.f.map((function(e){return[e,l[e]]}));return Object(a.jsxs)("div",{children:[Object(a.jsxs)("p",{children:["This benchmark is a work-in-progress dataset of programs implementing tabular data analytics tasks, similar to ",Object(a.jsx)("a",{href:"https://rosettacode.org/",children:"Rosetta Code"})," or ",Object(a.jsx)("a",{href:"https://eugenkiss.github.io/7guis/",children:"7GUIs"}),". This benchmark has two goals:"]}),Object(a.jsxs)("ol",{children:[Object(a.jsxs)("li",{children:[Object(a.jsx)("strong",{children:"Assist in cross-language learning."})," This benchmark provides an interface for easily comparing programs that do the same task in many languages."]}),Object(a.jsxs)("li",{children:[Object(a.jsx)("strong",{children:"Quantify the relationship between programs and tasks."})," A preliminary analysis of program size compares the relative conciseness of each language."]})]}),Object(a.jsx)("div",{class:"desktop",children:Object(a.jsxs)("center",{children:[Object(a.jsx)("strong",{children:"Click on a task name"}),Object(a.jsx)("span",{children:"or"}),Object(a.jsx)("strong",{children:"Click on a language"}),Object(a.jsx)("span",{children:"or"}),Object(a.jsxs)("strong",{children:["Read the ",Object(a.jsx)(d.a,{href:"/analysis",children:"analysis"})]})]})}),Object(a.jsxs)("div",{class:"mobile",children:[Object(a.jsx)("strong",{children:"Note:"})," this site is optimized for large screens. Try it when you get the chance."]}),Object(a.jsx)("div",{class:"desktop",children:Object(a.jsxs)("table",{className:"matrix code-table",children:[Object(a.jsx)("thead",{children:Object(a.jsxs)("tr",{children:[Object(a.jsx)("th",{className:"task-kind",children:"Category"}),Object(a.jsx)("th",{className:"task-kind",children:"Task name"}),o.a.map((function(t){var n={type:"lang",id:t.id};return Object(a.jsx)("th",{className:"hoverable",onMouseEnter:function(){return r(n)},onMouseLeave:function(){return r(null)},onClick:function(){e.push("/lang/".concat(t.id))},children:t.name},t.id)}))]})}),Object(a.jsx)("tbody",{children:h.map((function(t){var c=Object(s.a)(t,2),l=c[0],d=c[1];return d.map((function(t,s){var c={type:"task",id:t.id};return Object(a.jsxs)("tr",{children:[0==s?Object(a.jsx)("td",{className:"task-type",rowSpan:d.length,children:l}):null,Object(a.jsx)("td",{className:"task-description hoverable",onMouseEnter:function(){return r(c)},onMouseLeave:function(){return r(null)},onClick:function(){e.push("/task/".concat(t.id))},children:t.name}),o.a.map((function(e){var s=i.a.find(o.c,{task:t.id,language:e.id}),c=!!n&&("lang"==n.type&&n.id==e.id||"task"==n.type&&n.id==t.id);return Object(a.jsx)("td",{className:"task-code ".concat(c?"hover":""),children:s?Object(a.jsx)(u,{program:s,task:t}):""},e.id)}))]},t.id)}))}))})]})}),Object(a.jsx)("div",{class:"mobile",children:o.f.map((function(e){return Object(a.jsxs)("div",{className:"tasks-mobile",children:[Object(a.jsx)("h2",{children:e}),Object(a.jsx)("ul",{children:l[e].map((function(e){return Object(a.jsx)("li",{children:Object(a.jsx)(d.a,{href:"/task/".concat(e.id),children:e.name})})}))})]})}))})]})}}},[["/EDR",0,2,4,3,1,5]]]);