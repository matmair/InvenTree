import{o as a,r as t,j as e,T as r}from"./vendor-44a51bcb.js";import{u,i,L as c,C as x}from"./index-519700e6.js";function f(s){u(()=>{typeof s=="string"&&s.trim().length>0&&(document.title=s.trim())},[s])}function j(){const s=a(),[n,o]=t.useState(i._({id:"SlfejT"}));return f(n),t.useEffect(()=>{s&&s.statusText&&o(i._({id:"TpqeIh",values:{0:s.statusText}}))},[s]),e.jsx(c,{children:e.jsxs(x,{children:[e.jsx("h1",{children:e.jsx(r,{id:"SlfejT"})}),e.jsx("p",{children:e.jsx(r,{id:"b3ilvM"})}),e.jsx("p",{children:e.jsx("i",{children:s.statusText||s.message})})]})})}export{j as default};