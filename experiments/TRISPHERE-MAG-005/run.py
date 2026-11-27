import json,sys,time
from pathlib import Path
import numpy as np
import scipy,numba
from numba import njit,prange
import mag004_reference as ref
ROOT=Path(__file__).resolve().parent
SIZES=(24,48,96); COHORTS=(0,1); SEEDS=16; REFINE=8; STEPS=3072; CYCLES=12
LOWS=(.18,.24,.26,.32); REPEATS=(1,2)
ARMS=['static','native_1','sine_1']+[f'pulse_{L:.2f}_{k}x' for k in REPEATS for L in LOWS]
def idx(L,k):return ARMS.index(f'pulse_{L:.2f}_{k}x')
def levels(L):
    p=1/8; m=(.5-p*L)/(1-p); v=(ref.rms**2-p*(L-.5)**2)/(1-p)-(m-.5)**2
    return L,m-np.sqrt(v),m+np.sqrt(v)
def schedules(n):
    orig,sigma=ref.schedules(n); rs=[orig[ref.ARMS.index(a)] for a in ARMS[:3]]
    for k in REPEATS:
        per=n//(CYCLES*k); assert per%16==0
        for L in LOWS:rs.append(np.tile(np.repeat(levels(L),[per//8,7*per//16,7*per//16]),CYCLES*k))
    rs=np.array(rs)
    assert np.max(abs(rs.mean(axis=1)-.5))<1e-12 and np.max(abs(rs[1:].std(axis=1)-ref.rms))<1e-12 and np.all(rs>=0)
    for i,a in enumerate(ARMS[3:],3):assert np.isclose(np.mean(rs[i]<.25),.125 if float(a.split('_')[1])<.25 else 0)
    return rs,sigma
def checkpoints(n):
    t=set()
    for k in REPEATS:
        per=n//(CYCLES*k)
        for j in range((CYCLES-4)*k,CYCLES*k):t.update((j*per,j*per+per//8,(j+1)*per))
    return np.array(sorted(t),dtype=np.int64)
@njit(parallel=True)
def evolve(init,noise,rs,sigma,dt,times):
    na,nt=rs.shape; ns,N=init.shape
    out=np.empty((na,ns,N)); sn=np.empty((len(times),na,ns,N))
    for j in prange(na*ns):
        a=j//ns; s=j%ns; x=init[s].copy(); d1=np.empty(N); d2=np.empty(N); cp=0
        for k in range(nt):
            for i in range(N):
                d1[i]=np.sin(x[(i+1)%N]-x[i]); d2[i]=np.sin(x[(i+2)%N]-x[i])
            r=rs[a,k]; b=sigma[k]
            for i in range(N):x[i]+=-dt*(d1[i]-d1[(i-1)%N]+r*(d2[i]-d2[(i-2)%N]))+b*noise[k,s,i]
            if cp<len(times) and k+1==times[cp]:sn[cp,a,s]=x; cp+=1
        out[a,s]=x
    return out,sn
def run(N,c):
    rng=np.random.default_rng(2026112800+N*10+c)
    x=rng.uniform(-np.pi,np.pi,(SEEDS,N)); dt=ref.horizon/STEPS
    fine=rng.standard_normal((STEPS*2,SEEDS,N))*np.sqrt(dt/2); coarse=fine.reshape(STEPS,2,SEEDS,N).sum(1)
    rs,sigma=schedules(STEPS); rf,sf=schedules(STEPS*2)
    end,sn=evolve(x,coarse,rs,sigma,dt,checkpoints(STEPS))
    reflected,_=evolve(-x[:1],-coarse[:,:1],rs,sigma,dt,np.empty(0,dtype=np.int64))
    reflection=float(abs(np.exp(1j*reflected)-np.exp(-1j*end[:,:1])).max()); assert reflection<1e-9
    ef,snf=evolve(x[:REFINE],fine[:,:REFINE],rf,sf,dt/2,checkpoints(STEPS*2))
    d=dict(N=N,cohort=c,reflection=reflection,coarse=ref.quench(end),fine=ref.quench(ef),snapshots=ref.metrics(sn),fine_snapshots=ref.metrics(snf))
    print('finished',N,c,'hits',np.sum(d['coarse']['metrics']['gap']<1e-6,axis=1).tolist(),flush=True)
    return d
def paired_test(ds,rng):
    d=np.concatenate(ds); obs=float(d.mean()); count=0
    for _ in range(50):
        signs=rng.choice([-1.,1.],size=(1000,len(d))); count+=int(np.sum(signs@d/len(d)>=obs-1e-15))
    boot=np.concatenate([v[rng.integers(len(v),size=(10000,len(v)))] for v in ds],axis=1).mean(1)
    return obs,(1+count)/50001,np.quantile(boot,[.025,.975]).tolist()
def summarize(data):
    def get(ds,key,res='coarse',sub=False,pre=False):
        name='prequench' if pre else 'metrics'
        return np.concatenate([d[res][name][key][:,:REFINE] if sub else d[res][name][key] for d in ds],axis=1)
    def table(ds,res='coarse',sub=False,pre=False):
        g=get(ds,'gap',res,sub,pre); ks=('wall','peak','chi','near','moment')+(() if pre else ('success','grad_inf'))
        stats={k:get(ds,k,res,sub,pre) for k in ks}
        return {a:dict(n=g.shape[1],hits=int(sum(g[i]<1e-6)),gap=float(g[i].mean()),**{k:float(np.mean(abs(v[i]))) for k,v in stats.items()}) for i,a in enumerate(ARMS)}
    def contrast(g,l,h):return np.mean([g[idx(l,k)]-g[idx(h,k)] for k in REPEATS],axis=0)
    rng=np.random.default_rng(941108); tests={}
    for name,l,h in [('deep',.18,.32),('near',.24,.26)]:
        ds=[contrast(d['coarse']['metrics']['gap'],l,h) for d in data]; eff,p,ci=paired_test(ds,rng)
        g=get(data,'gap'); f=get(data,'gap','fine'); sub=get(data,'gap',sub=True)
        tests[name]=dict(effect=eff,p=p,ci95_unadjusted=ci,cohort_effects=[float(np.concatenate([v for v,d in zip(ds,data) if d['cohort']==c]).mean()) for c in COHORTS],size_effects={str(N):float(np.concatenate([v for v,d in zip(ds,data) if d['N']==N]).mean()) for N in SIZES},timing_effects={str(k):float((g[idx(l,k)]-g[idx(h,k)]).mean()) for k in REPEATS},coarse_subset=float(contrast(sub,l,h).mean()),fine_subset=float(contrast(f,l,h).mean()))
    running=0
    for i,a in enumerate(sorted(tests,key=lambda a:tests[a]['p'])):
        running=max(running,min(1.,(len(tests)-i)*tests[a]['p']));tests[a]['holm']=running
    def pulses(res='coarse'):
        n=STEPS if res=='coarse' else 2*STEPS; ts=checkpoints(n).tolist(); key='snapshots' if res=='coarse' else 'fine_snapshots'; result={}
        for k in REPEATS:
            per=n//(CYCLES*k); js=range((CYCLES-4)*k,CYCLES*k)
            a0=[ts.index(j*per) for j in js]; a1=[ts.index(j*per+per//8) for j in js]; a2=[ts.index((j+1)*per) for j in js]
            for L in LOWS:
                i=idx(L,k); result[ARMS[i]]={}
                for m in ('near','wall','chi','gap','peak'):
                    v=np.concatenate([d[key][m][:,i] for d in data],axis=1)
                    if m=='chi':v=abs(v)
                    result[ARMS[i]][m]=dict(before=float(v[a0].mean()),after_low=float(v[a1].mean()),end=float(v[a2].mean()),change_low=float((v[a1]-v[a0]).mean()),change_recovery=float((v[a2]-v[a1]).mean()))
        return result
    def diagnostics(n):return {a:dict(mean=float(x.mean()),rms=float(x.std()),min=float(x.min()),max=float(x.max()),below_quarter=float((x<.25).mean())) for a,x in zip(ARMS,schedules(n)[0])}
    gate=all(t['holm']<.05 and t['effect']>0 and min(t['cohort_effects'])>0 and min(t['timing_effects'].values())>0 and t['fine_subset']>0 for t in tests.values())
    return dict(pooled=table(data),by_size={str(N):table([d for d in data if d['N']==N]) for N in SIZES},by_cohort={str(c):table([d for d in data if d['cohort']==c]) for c in COHORTS},coarse_subset=table(data,sub=True),fine_subset=table(data,'fine'),prequench=table(data,pre=True),primary=tests,primary_gate=gate,pulse_dynamics=pulses(),fine_pulse_dynamics=pulses('fine'),drive=diagnostics(STEPS),fine_drive=diagnostics(STEPS*2),reflection_max=max(d['reflection'] for d in data),quench_failures=sum(int((~d[k]['metrics']['success']).sum()) for d in data for k in ('coarse','fine')))
if __name__=='__main__':
    start=time.monotonic(); data=[run(N,c) for N in SIZES for c in COHORTS]; s=summarize(data)
    out=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,numba=numba.__version__),arms=ARMS,physical_period=ref.PERIOD,effective_period=ref.P,horizon=ref.horizon,ratio_rms=ref.rms,steps=STEPS,checkpoint_steps=checkpoints(STEPS),fine_checkpoint_steps=checkpoints(STEPS*2),summary=s,raw=data)
    (ROOT/'results.json').write_text(json.dumps(out,default=ref.native_json,separators=(',',':'))+'\n')
    (ROOT/'summary.json').write_text(json.dumps({k:v for k,v in out.items() if k!='raw'},default=ref.native_json,indent=2)+'\n')
    print('elapsed_seconds',time.monotonic()-start,flush=True)
    print(json.dumps(dict(primary=s['primary'],primary_gate=s['primary_gate'],pooled=s['pooled'],reflection=s['reflection_max'],quench_failures=s['quench_failures']),indent=2),flush=True)
