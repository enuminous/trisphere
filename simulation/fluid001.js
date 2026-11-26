function run(beta,dt,N=240,T=160,seed=42,shelf=true){
 let s=seed;const rand=()=>((s=(Math.imul(1664525,s)+1013904223)>>>0)/4294967296);
 let x=[],v=[],tag=[],cross=[],kicks=0,inj=0,damp=0,mix=0,err=0,peak=0,trace=[];
 const V=x=>.02*(shelf?(x<=3.5?x*x:x<=4.5?12.25:x<=11?x*x-8:113):Math.min(x,11)**2);
 const force=x=> (x>=11||(shelf&&x>=3.5&&x<=4.5))?0:-.04*x;
 for(let i=0;i<N;i++){let t=i<N/4;tag.push(t);x.push(t?3.65+.5*rand():.1+11.7*rand());v.push(t?0:(rand()<.5?-1:1)*(1+2*rand()));cross.push(false)}
 const energy=()=>x.reduce((z,a,i)=>z+.5*v[i]**2+V(a),0);const E0=energy();
 for(let step=0;step<Math.round(T/dt);step++){
  let n=Array(48).fill(0),u=Array(48).fill(0);for(let i=0;i<N;i++){let j=Math.min(47,Math.floor(x[i]*4));n[j]++;u[j]+=v[i]}
  for(let j=0;j<48;j++)if(n[j])u[j]/=n[j];
  let p0=v.reduce((a,b)=>a+b,0),ke0=v.reduce((a,b)=>a+b*b/2,0);
  for(let i=0;i<N;i++){let j=Math.min(47,Math.floor(x[i]*4));v[i]=u[j]+(v[i]-u[j])*Math.exp(-beta*dt)}
  err=Math.max(err,Math.abs(v.reduce((a,b)=>a+b,0)-p0));mix+=ke0-v.reduce((a,b)=>a+b*b/2,0);
  for(let i=0;i<N;i++){v[i]+=force(x[i])*dt/2;let old=v[i];v[i]*=Math.exp(-.08*dt);damp+=(old*old-v[i]*v[i])/2;x[i]+=v[i]*dt;
   if(x[i]>12){x[i]=24-x[i];v[i]=-Math.abs(v[i])}
   if(x[i]<0){x[i]=-x[i];v[i]=Math.sqrt(v[i]*v[i]+10);kicks++;inj+=5}
   v[i]+=force(x[i])*dt/2;if(tag[i]&&(x[i]<3.5||x[i]>4.5))cross[i]=true;
  }
  let count=x.filter(z=>z>=3.5&&z<=4.5).length;peak=Math.max(peak,count);
  if((step+1)%Math.round(20/dt)===0)trace.push({t:(step+1)*dt,pool:count,escaped:cross.filter(Boolean).length,energy:energy()});
 }
 return {beta,dt,N,seed,shelf,kicks,peak,escaped:cross.filter(Boolean).length,finalPool:x.filter(z=>z>=3.5&&z<=4.5).length,E0,E:energy(),inj,damp,mix,energyResidual:energy()-E0-inj+damp+mix,momentumError:err,trace};
}
const results=[];for(const seed of [42,43,44])for(const dt of [.02,.01])for(const beta of [0,.2,1])results.push(run(beta,dt,240,160,seed));
console.log(JSON.stringify(results,null,2));
