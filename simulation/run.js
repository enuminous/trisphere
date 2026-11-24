"use strict";
const L=require("./model/engine.js");
const fs=require("node:fs");
const path=require("node:path");
const out=path.join(__dirname,"results");
fs.mkdirSync(out,{recursive:true});
const time=["model,t,r,v,energy"],returns=["model,return,t,energy_before,energy_after"];
const summary={};
for(const mode of ["fixed","kick","removed"]){
  const run=L.simulate(mode,0.35,1.2,2,0.005,64);
  for(const p of run.points)time.push([mode,p.t,p.r,p.v,p.e].join(","));
  for(const [i,e] of run.events.entries())returns.push([mode,i+1,e.t,e.before,e.after].join(","));
  summary[mode]={status:run.status,samples:run.points.length,end:run.points.at(-1),events:run.events.length,lastReturn:run.events.at(-1)??null,minRadius:Math.min(...run.points.map(p=>p.r)),maxRadius:Math.max(...run.points.map(p=>p.r))};
}
fs.writeFileSync(path.join(out,"trajectories.csv"),time.join("\n")+"\n");
fs.writeFileSync(path.join(out,"returns.csv"),returns.join("\n")+"\n");
fs.writeFileSync(path.join(out,"runs.json"),JSON.stringify(summary,null,2)+"\n");
