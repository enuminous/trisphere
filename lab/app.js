"use strict";
const D=JSON.parse(document.getElementById("lab-data").textContent);
const $=id=>document.getElementById(id), txt=(id,value)=>{$(id).textContent=value;};
const f=(x,n=3)=>Number(x).toFixed(n);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const workspaces=[["atlas","Layer atlas"],["dynamics","Oscillator"],["compression","Five vs. thirteen"],["ledger","Audit ledger"],["proofs","Lean proofs"]];
let active="atlas", ledger="claims",phase=0,trace,visible=[];
function tab(id,focus=false){
  active=id;
  for(const [key] of workspaces){
    $(key).hidden=key!==id;
    const b=$("tab-"+key);b.setAttribute("aria-selected",String(key===id));b.tabIndex=key===id?0:-1;
  }
  if(focus)$("tab-"+id).focus();
  if(id==="atlas")drawAtlas();
  if(id==="dynamics")dynamics();
  if(id==="compression")compress();
  if(id==="ledger")showRows();
}
const nav=document.querySelector("nav");
workspaces.forEach(([id,name],i)=>{
  const b=document.createElement("button");
  b.textContent=name;b.id="tab-"+id;b.setAttribute("role","tab");b.setAttribute("aria-controls",id);
  $(id).setAttribute("role","tabpanel");$(id).setAttribute("aria-labelledby",b.id);
  b.onclick=()=>tab(id);b.onkeydown=e=>{
    const delta=e.key==="ArrowRight"?1:e.key==="ArrowLeft"?-1:0;
    if(delta){e.preventDefault();tab(workspaces[(i+delta+workspaces.length)%workspaces.length][0],true);}
    if(e.key==="Home"||e.key==="End"){e.preventDefault();tab(workspaces[e.key==="Home"?0:workspaces.length-1][0],true);}
  };nav.append(b);
});
function frame(id){
  const c=$(id),w=c.clientWidth,h=c.clientHeight,scale=Math.min(window.devicePixelRatio||1,2);
  c.width=Math.round(w*scale);c.height=Math.round(h*scale);
  const ctx=c.getContext("2d");ctx.scale(scale,scale);ctx.lineJoin="round";ctx.lineCap="round";
  ctx.fillStyle="#102c31";ctx.fillRect(0,0,w,h);
  ctx.fillStyle="#335054";
  for(let x=10;x<w;x+=20)for(let y=10;y<h;y+=20)ctx.fillRect(x,y,1,1);
  return {ctx,w,h};
}
function drawAtlas(){
  const n=Number($("radius").value),angle=Number($("camera").value), group=TriLab.branch(n);
  txt("rVal",n);txt("cameraVal",angle+"°");txt("layerGroup",TriLab.groups[group]);txt("layerName",TriLab.NAMES[n]);
  txt("layerCaption",n===0?"The shell equation forces z₁ = z₂ = 0. Its fiber is a point.":n===6?"Layer 6 is the only fixed point of the mirror. The blueprint places the human choice here.":"This layer and its mirror are equally far from the Filter in the indexed atlas.");
  txt("mirrorVal",12-n);txt("hopfVal",n*n);txt("binVal",group+" / 4");txt("atlasCoord","ρ = "+n+"  •  M(ρ) = "+(12-n));txt("fiberFoot",n?"24 PHASE ORBITS":"DEGENERATE SHELL");
  $("mirror").textContent=n===6?"Mirror fixes layer 6":"Show mirror · "+(12-n);
  const {ctx,w,h}=frame("fibers"),cx=w/2,cy=h/2,α=angle*Math.PI/180;
  ctx.strokeStyle="#345256";ctx.setLineDash([3,6]);ctx.beginPath();ctx.moveTo(w*.09,cy);ctx.lineTo(w*.91,cy);ctx.moveTo(cx,h*.08);ctx.lineTo(cx,h*.92);ctx.stroke();ctx.setLineDash([]);
  if(n===0){ctx.fillStyle="#ffb075";ctx.beginPath();ctx.arc(cx,cy,5,0,7);ctx.fill();return;}
  const paths=[],eta=.71,co=Math.cos(eta),si=Math.sin(eta);
  for(let k=0;k<24;k++){
    const δ=k*2*Math.PI/24;let prev;
    for(let j=0;j<=128;j++){
      const u=j*2*Math.PI/128,den=1-si*Math.sin(u+δ);
      const x=co*Math.cos(u)/den,y=co*Math.sin(u)/den,z=si*Math.cos(u+δ)/den;
      const a=x*Math.cos(α)-z*Math.sin(α), b=z*Math.cos(α)+x*Math.sin(α);
      const vertical=.68*y-.733*b,depth=.733*y+.68*b;
      const scale=Math.min(w*.195,h*.235),pt=[cx+scale*a*1.22,cy+scale*vertical,depth];
      if(prev)paths.push([prev,pt,k]);prev=pt;
    }
  }
  paths.sort((a,b)=>a[1][2]-b[1][2]);
  for(const [p,q,k] of paths){
    const alpha=.32+.52*Math.min(1,Math.max(0,(q[2]+2)/4));
    ctx.strokeStyle=k%6===0?"rgba(255,177,113,.96)":k%3===0?"rgba(217,232,178,"+alpha+")":"rgba(134,234,209,"+alpha+")";
    ctx.lineWidth=k%6===0?2:1.15;
    ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(q[0],q[1]);ctx.stroke();
  }
}
function route(){
  const kept=Number($("keep").value),b=Number($("bias").value);
  const ws=[0,1,2,3].map(i=>Math.exp(b*(i-1.5))),total=ws.reduce((a,v)=>a+v,0);
  txt("keepVal",kept+" / 100");txt("biasVal",f(b,1));txt("routing","Product "+kept+" units • "+ws.map((v,i)=>"Layer "+(i+8)+" = "+f((100-kept)*v/total,2)).join(" • ")+" units (rounded).");
}
$("radius").oninput=$("camera").oninput=drawAtlas;
$("mirror").onclick=()=>{$("radius").value=12-Number($("radius").value);drawAtlas();};
$("zero").onclick=()=>{$("radius").value=0;drawAtlas();};
$("keep").oninput=$("bias").oninput=route;
function drawTrace(run,key) {
  const {ctx,w,h}=frame("trace"),P=run.points,left=48,bottom=h-30,top=20,right=w-14;
  let min=Math.min(...P.map(p=>p[key])),max=Math.max(...P.map(p=>p[key]));
  if(min===max){min-=.5;max+=.5;}else{let gap=(max-min)*.07;min-=gap;max+=gap;}
  const tmax=P.at(-1).t||1,toX=t=>left+t/tmax*(right-left),toY=v=>bottom-(v-min)/(max-min)*(bottom-top);
  ctx.font="11px monospace";ctx.fillStyle="#d5e8df";
  for(let i=0;i<=4;i++){
    const y=top+(bottom-top)*i/4;ctx.strokeStyle="#365357";ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(right,y);ctx.stroke();ctx.fillText(f(max-(max-min)*i/4,2),2,y+3);
    const t=tmax*i/4;ctx.fillText(f(t,1),Math.min(w-25,toX(t)-4),bottom+18);
  }
  ctx.setLineDash([3,4]);ctx.strokeStyle="#976f55";for(const e of run.events){ctx.beginPath();ctx.moveTo(toX(e.t),top);ctx.lineTo(toX(e.t),bottom);ctx.stroke();}ctx.setLineDash([]);
  ctx.strokeStyle="#99eaca";ctx.lineWidth=2;ctx.beginPath();P.forEach((p,i)=>{const x=toX(p.t),y=toY(p[key]);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y);});ctx.stroke();
  if(key==="r"&&min<=12&&max>=12){ctx.strokeStyle="#ffb075";const y=toY(12);ctx.beginPath();ctx.moveTo(left,y);ctx.lineTo(right,y);ctx.stroke();}
  txt("rangeinfo",P.length+" SAMPLES • Δt "+f(run.dt,4));
}
const descriptions={
 fixed:"Illustrative position law: V′ = ρ(1−ρ/11.25)² below 11.25 and zero above. D = k(1−ρ/3)² below 3 and zero above. Initial velocity is zero. The integrator stops at the first sampled exit.",
 kick:"Harmonic half-oscillator with elastic redirection at the center and J added to kinetic energy on each return. Dashed lines mark exact events. This model supplies the extra rule suggested in the blueprint.",
 removed:"The same half-oscillator and center redirection with J = 0. Each return loses energy when damping is positive.",
 coast:"Start at ρ = 11.25 with outward speed v₀. For γ > 0, ρ(t) = 11.25 + v₀(1−e⁻ᵞᵗ)/γ. A finite wall crossing needs v₀ > 0.75γ. The orange reference line marks ρ = 12 when in range."
};
function dynamics(){
 const m=$("mode").value,g=+$("drag").value,k=+$("drive").value,ini=+$("initial").value,key=$("quantity").value;
 $("drive").disabled=["removed","coast"].includes(m);
 txt("dragVal",f(g,2));txt("driveVal",$("drive").disabled?"inactive":f(k,1));txt("driveLabel",m==="kick"?"Energy per return J":"Drive strength k");
 txt("initialLabel",m==="fixed"?"Initial radius":m==="coast"?"Entry speed v₀":"Initial energy E₀");txt("initVal",f(ini,2));
 trace=TriLab.simulate(m,g,k,ini);const end=trace.points.at(-1);
 txt("modelNote",descriptions[m]);txt("solver",m==="fixed"?"RK4":"CLOSED FORM");
 txt("chartName",({r:"RADIAL POSITION",e:"ENERGY",v:"VELOCITY"})[key]);
 txt("runStatus",trace.status);txt("runSummary","Last sample at t = "+f(end.t)+" • ρ = "+f(end.r)+" • v = "+f(end.v)+" • E = "+f(end.e)+".");
 const en=m==="fixed"?"E = v²/2 + V − ∫D dρ. For the smooth fixed drive, dE/dt = −γv². With positive damping, a nonconstant periodic state is impossible.":m==="coast"?"With zero drive and flat V, v(t) = v₀ exp(−γt). At the threshold the wall is approached asymptotically.":g===0?"With γ = 0, q = 1. Removing the kick conserves energy; adding J gives linear growth per event.":"At a center return Eₙ₊₁ = qEₙ + J. Here q = "+f(trace.q,5)+" and E* = "+f((m==="kick"?k:0)/(1-trace.q),5)+". Returns observed: "+trace.events.length+".";
 txt("energyNote",en);drawTrace(trace,key);
}
for(const id of ["mode","drag","drive","initial","quantity"])$(id).oninput=dynamics;
$("resetDyn").onclick=()=>{for(const [id,v] of [["mode","fixed"],["drag",".35"],["drive","1.2"],["initial","2"],["quantity","r"]])$(id).value=v;dynamics();};
function download(name,type,content){const url=URL.createObjectURL(new Blob([content],{type}));const a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$("exportTrace").onclick=()=>{
 const r=trace;
 download("trisphere-"+r.mode+".csv","text/csv","mode,gamma,k_input,initial,dt,t,rho,velocity,energy\n"+r.points.map(p=>[r.mode,r.g,r.k,r.initial,r.dt,p.t,p.r,p.v,p.e].join(",")).join("\n")+"\n");
};
const strip=$("strip");for(let n=0;n<=12;n++){const b=document.createElement("button");b.textContent=n;b.setAttribute("aria-label","Select fine layer "+n);b.onclick=()=>{phase=n;compress();};strip.append(b);}
function rad(p){return Math.min(p,24-p);}
function compress(){const n=rad(phase),next=rad((phase+1)%24),c=TriLab.branch(n);
 txt("fine",n+" / 12");txt("coarseNum",c+" / 4");txt("stepText",TriLab.groups[c]+" • directed phase "+phase+" / 24 • next fine layer "+next+" → "+TriLab.groups[TriLab.branch(next)]);
 [...strip.children].forEach((b,i)=>b.setAttribute("aria-pressed",i===n));
}
$("tick").onclick=()=>{phase=(phase+1)%24;compress();};
$("reverse").onclick=()=>{phase=(24-phase)%24;compress();txt("witnessText",phase===0||phase===12?"At an endpoint, both phase labels coincide.":"The radius stays fixed while the next step reverses.");};
$("witness").onclick=()=>{phase=5;compress();txt("witnessText","Layer 1 → 2 stays in Time. Layer 5 → 6 reaches Space. The same starting bin therefore has two different successors.");};
function sourceAt(range){
 const sections=(range||"1").split(";").map(part=>{
   const nums=part.match(/\d+/g)||["1"],start=Number(nums[0]),end=Math.min(Number(nums[1]||start),D.source.length);
   return D.source.slice(start-1,end).map((line,i)=>(start+i)+"  "+line).join("\n");
 });
 txt("sourceText",sections.join("\n\n⋯\n\n"));
 $("sourceDialog").showModal();
}
$("viewSource").onclick=()=>{txt("sourceText",D.source.map((s,i)=>(i+1)+"  "+s).join("\n"));$("sourceDialog").showModal();};
function showRows(){
 const st=$("verdict").value,q=$("search").value.trim().toLowerCase();visible=D[ledger].filter(r=>(!st||r.status===st)&&Object.values(r).join(" ").toLowerCase().includes(q));
 txt("shown",visible.length+" of "+D[ledger].length+(ledger==="claims"?" claim findings":" named operations"));
 $("rows").replaceChildren();
 for(const r of visible){
   const row=document.createElement("details");row.className="record";
   const fields=ledger==="claims"?[["Finding",r.result],["Evidence",r.evidence],["Scope or next test",r.next]]:[["Operation",r.scope],["Criterion",r.criterion],["Finding",r.result],["Execution",r.mode],["Software replay",r.baseline],["Evidence",r.evidence],["Source revision",r.pin||"Unresolved"]];
   row.innerHTML='<summary><span class="pill '+esc(r.status)+'">'+esc(r.status)+'</span> '+esc(ledger==="claims"?r.id+" · "+r.title:r.name+" · "+r.family)+'</summary>'+fields.map(([k,v])=>'<p><b>'+esc(k)+'</b> '+esc(v)+'</p>').join("");
   if(r.lines){const b=document.createElement("button");b.className="btn";b.textContent="Source lines "+r.lines;b.onclick=()=>sourceAt(r.lines);row.append(b);}
   $("rows").append(row);
 }
 if(!visible.length)$("rows").textContent="No matching entries.";
}
for(const b of document.querySelectorAll("[data-ledger]"))b.onclick=()=>{ledger=b.dataset.ledger;$("search").value="";$("verdict").value="";for(const x of document.querySelectorAll("[data-ledger]"))x.setAttribute("aria-pressed",x===b);showRows();};
$("verdict").onchange=$("search").oninput=showRows;
$("exportLedger").onclick=()=>download(ledger+"-filtered.json","application/json",JSON.stringify(visible,null,2)+"\n");
for(const proof of D.proofs){
 const row=document.createElement("details");row.className="record";const title=document.createElement("summary");title.textContent=proof.name.replaceAll("_"," ");const pre=document.createElement("pre");pre.textContent=proof.log;row.append(title,pre);$("proofRows").append(row);
}
$("downloadLean").onclick=()=>download("TriSphere.lean","text/plain",D.lean);
txt("proofCount",D.proofs.length);txt("rosterCount",D.roster.length);
route();tab("atlas");
window.addEventListener("resize",()=>{if(active==="atlas")drawAtlas();if(active==="dynamics")drawTrace(trace,$("quantity").value);});

const sweepFilter=$("sweepFilter");
for(const outcome of ["All outcomes",...Object.keys(D.sweep.counts)]){
  const opt=document.createElement("option"); opt.textContent=outcome; sweepFilter.append(opt);
}
function sweepRows(){
  const subset=D.sweep.sweep.filter(r=>sweepFilter.selectedIndex===0||r.outcome===sweepFilter.value);
  $("sweepRows").innerHTML=subset.map(r=>"<tr>"+[r.gamma,r.J,r.E0,r.returns,r.outcome].map(v=>"<td>"+esc(v)+"</td>").join("")+"</tr>").join("");
  $("exportSweep").onclick=()=>download("return-map-sweep.json","application/json",JSON.stringify(subset,null,2)+"\n");
}
sweepFilter.onchange=sweepRows;sweepRows();
const reportSections=[];
for(const line of D.report.split("\n")){
  if(line.startsWith("# ")||line.startsWith("## ")){
    reportSections.push({title:line.replace(/^#+ /,""),lines:[]});
  }else if(reportSections.length)reportSections.at(-1).lines.push(line);
}
function inline(text){
  return esc(text).replace(/\[([^\]]+)\]\(([^)]+)\)/g,(_,name,url)=>
    /^https:\/\//.test(url)?'<a href="'+url+'" target="_blank" rel="noopener">'+name+'</a>':name)
    .replace(/\*\*([^*]+)\*\*/g,"<b>$1</b>").replace(/`([^`]+)`/g,"<code>$1</code>").replace(/\*([^*]+)\*/g,"<i>$1</i>");
}
function showReport(){
  const lines=reportSections[$("reportSection").selectedIndex].lines,html=[];
  for(let i=0;i<lines.length;i++){
    const l=lines[i];if(!l.trim())continue;
    if(l.startsWith("```")){const code=[];while(++i<lines.length&&!lines[i].startsWith("```"))code.push(lines[i]);html.push("<pre>"+esc(code.join("\n"))+"</pre>");}
    else if(l.startsWith("|")){
      const t=[];while(i<lines.length&&lines[i].startsWith("|")){const cells=lines[i].slice(1,-1).split("|");if(!cells.every(v=>/^[:\-\s]+$/.test(v)))t.push(cells);i++;}i--;
      html.push('<div class="tablewrap"><table>'+t.map((r,k)=>"<tr>"+r.map(c=>k?"<td>"+inline(c)+"</td>":"<th>"+inline(c)+"</th>").join("")+"</tr>").join("")+"</table></div>");
    }else if(l.startsWith("* ")){const items=[];while(i<lines.length&&lines[i].startsWith("* ")){items.push("<li>"+inline(lines[i].slice(2))+"</li>");i++;}i--;html.push("<ul>"+items.join("")+"</ul>");}
    else if(l.startsWith("### "))html.push("<h4>"+inline(l.slice(4))+"</h4>");
    else html.push("<p>"+inline(l)+"</p>");
  }
  $("reportBody").innerHTML=html.join("");
}
for(const s of reportSections){const opt=document.createElement("option");opt.textContent=s.title;$("reportSection").append(opt);}
$("reportSection").onchange=showReport;showReport();
$("exportReport").onclick=()=>download("AUDIT.md","text/markdown",D.report);
