"use strict";
const fs=require("node:fs");
const L=require("../lab/engine.js");
const checks=[];
function check(id,condition,observed) {
  checks.push({id,pass:Boolean(condition),observed});
}
const close=(a,b)=>Math.abs(a-b)<=1e-9*(1+Math.max(Math.abs(a),Math.abs(b)));
const mirrors=Array.from({length:13},(_,n)=>({n,m:12-n,c:L.branch(n)}));
check("atlas",mirrors.every(x=>12-x.m===x.n && L.branch(x.m)===4-x.c) &&
  mirrors.filter(x=>x.n===x.m).length===1,mirrors);
check("coarse-counterexample",L.branch(1)===L.branch(5)&&L.branch(2)!==L.branch(6),[1,5,2,6]);
const base=L.hopf(1,2,3,4), rotated=L.hopf(-2,1,-4,3);
check("hopf-common-phase",base.every((v,i)=>v===rotated[i]),{base,rotated});
check("hopf-scaling",L.hopf(2,0,0,0)[0]===4 && L.hopf(0,0,0,0).every(x=>x===0),[4,0]);
for(const E of [0.5,2,8]) {
 const run=L.simulate("kick",0.35,1.2,E,1/80,40);
 const fixed=1.2/(1-run.q);
 const errors=run.events.map((e,i)=>Math.abs(e.after-(fixed+run.q**(i+1)*(E-fixed))));
 check("return-map-"+E,errors.length>=10 && Math.max(...errors)<1e-9,{events:errors.length,maxError:Math.max(...errors),fixed,last:run.events.at(-1)});
}
for(const [mode,g,k] of [["removed",0.35,3],["removed",0,3],["kick",0,1]]) {
 const run=L.simulate(mode,g,k,2);
 const n=run.events.length, expected=g===0 ? 2+(mode==="kick"?n:0) : 2*run.q**n;
 check([mode,g,k].join("-"),n>0&&close(run.events.at(-1).after,expected),{n,expected,observed:run.events.at(-1).after});
}
const steps=[1/40,1/80,1/160];
const refine=steps.map(dt=>L.simulate("fixed",0.4,2,1,dt,12));
const ends=refine.map(x=>x.points.at(-1));
const diff=ends.slice(1).map((p,i)=>Math.hypot(ends[i].r-p.r,ends[i].v-p.v));
check("rk4-refinement",ends.every(p=>close(p.t,12))&&Math.max(...diff)<1e-5,{steps,ends,diff});
const energies=refine[2].points.map(p=>p.e);
const inc=Math.max(...energies.slice(1).map((v,i)=>v-energies[i]));
check("dissipation",inc<1e-8 && energies.at(-1)<energies[0],{maxIncrease:inc,first:energies[0],last:energies.at(-1)});
const eq=L.simulate("fixed",0.4,3,11.75);
check("plateau-equilibrium",eq.points.every(p=>p.r===11.75 && p.v===0),eq.points.at(-1));
const hit=L.simulate("coast",0.5,0,1);
const miss=L.simulate("coast",0.5,0,0.25);
const graze=L.simulate("coast",0.5,0,0.375);
check("wall-threshold",hit.status.includes("Exit") && !miss.status.includes("Exit") && !graze.status.includes("Exit"),[hit,miss,graze].map(r=>r.points.at(-1)));
const free=L.simulate("coast",0,0,1);
check("zero-drag-control",free.points.every(p=>p.v===1)&&hit.points[1].v<1,[hit.points[1],free.points[1]]);
// State conjugacy for a pure rescaling x=rho/3, with explicitly transformed coefficients.
let r=1,v=0,x=r/3,w=v/3,maxError=0;
for(let i=0;i<960;i++){
 [r,v]=L.rk4(r,v,1/80,(s,z)=>-L.gradient(s,2)-0.4*z);
 [x,w]=L.rk4(x,w,1/80,(s,z)=>-L.gradient(3*s,2)/3-0.4*z);
 maxError=Math.max(maxError,Math.abs(r/3-x),Math.abs(v/3-w));
}
check("coordinate-rescaling",maxError<1e-9,{maxError,steps:960});
const out={protocol:"protocol/criteria.md",runner:"Node / deterministic, no seed",checks};
const file=process.argv[2];
if(file) fs.writeFileSync(file,JSON.stringify(out,null,2)+"\n");
for(const c of checks) console.log(c.pass?"PASS":"FAIL",c.id);
if(checks.some(c=>!c.pass)) process.exitCode=1;
