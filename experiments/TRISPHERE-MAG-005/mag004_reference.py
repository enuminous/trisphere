import json, sys, time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.stats import binomtest
from scipy.integrate import cumulative_trapezoid
from numba import njit, prange, set_num_threads
import numba
from mag003_reference import PERIOD, radius, objective, metrics
ROOT=Path(__file__).resolve().parent
SIZES=(24,48,96); COHORTS=(0,1); SEEDS=12; REFINE=6; STEPS=3072; CYCLES=12
FREQ=(.5,1,2,4); WAVES=('native','sine','phase','shuffle')
set_num_threads(4)
t=np.linspace(0,PERIOD,8193); u=np.array([radius(float(v))/12 for v in t]); f=1+.6*u
clock=cumulative_trapezoid(f,t,initial=0); P=float(clock[-1]); horizon=CYCLES*P
M=4096; phase=np.arange(M)/M
native=.6*np.interp(phase*P,clock,u); native-=native.mean(); rms=float(np.sqrt(np.mean(native**2)))
fft=np.fft.rfft(native); sine_fft=np.zeros_like(fft); sine_fft[1]=fft[1]
sine=np.fft.irfft(sine_fft,n=M)
rng=np.random.default_rng(412607); scr=fft.copy(); scr[2:-1]=abs(scr[2:-1])*np.exp(1j*rng.uniform(-np.pi,np.pi,len(scr)-3)); scr[-1]=abs(scr[-1])*rng.choice([-1,1]); phase_scr=np.fft.irfft(scr,n=M)
perm=rng.permutation(16); shuffle=native.reshape(16,-1)[perm].ravel()
templates=dict(native=native,sine=sine,phase=phase_scr,shuffle=shuffle)
assert np.allclose(abs(np.fft.rfft(phase_scr)),abs(fft),atol=1e-10)
assert np.array_equal(np.sort(shuffle),np.sort(native))
ARMS=['static']+[f'{w}_{v:g}' for w in WAVES for v in FREQ]
def schedules(n):
    p=(np.arange(n)+.5)/n; tau=p*horizon; temp=1.2*(1-p)**2+.015
    rs=[np.full(n,.5)]
    for w in WAVES:
        for v in FREQ:
            a=np.interp((tau/P*v)%1,phase,templates[w],period=1); a-=a.mean(); a*=rms/np.sqrt(np.mean(a*a)); rs.append(.5+a)
    rs=np.array(rs)
    assert np.max(abs(rs.mean(axis=1)-.5))<1e-12
    assert np.max(abs(rs[1:].std(axis=1)-rms))<1e-12
    assert rs.min()>=0
    return rs,np.sqrt(2*temp)
@njit(parallel=True)
def evolve(init,noise,rs,sigma,dt):
    na,nt=rs.shape; ns,N=init.shape
    out=np.empty((na,ns,N))
    for j in prange(na*ns):
        a=j//ns; s=j%ns; x=init[s].copy(); d1=np.empty(N); d2=np.empty(N)
        for k in range(nt):
            for i in range(N):
                d1[i]=np.sin(x[(i+1)%N]-x[i]); d2[i]=np.sin(x[(i+2)%N]-x[i])
            r=rs[a,k]; b=sigma[k]
            for i in range(N):
                x[i]+=-dt*(d1[i]-d1[(i-1)%N]+r*(d2[i]-d2[(i-2)%N]))+b*noise[k,s,i]
        out[a,s]=x
    return out

def quench(end):
    na,ns,N=end.shape; q=np.empty_like(end); success=np.empty((na,ns),bool); grad=np.empty((na,ns))
    for a in range(na):
        for s in range(ns):
            opt=minimize(objective,end[a,s],jac=True,method='L-BFGS-B',options={'maxiter':2000,'ftol':1e-13,'gtol':1e-9})
            q[a,s]=opt.x; success[a,s]=opt.success; grad[a,s]=abs(opt.jac).max()
    m=metrics(q); m['success']=success; m['grad_inf']=grad
    assert np.min(m['gap'])>-1e-10
    return dict(metrics=m,angles=q,prequench=metrics(end))

def native_json(o):
    if isinstance(o,np.ndarray):return o.tolist()
    if isinstance(o,np.generic):return o.item()
    raise TypeError(type(o))
def run(N,c):
    rng=np.random.default_rng(2026112700+N*10+c)
    x=rng.uniform(-np.pi,np.pi,(SEEDS,N)); dt=horizon/STEPS
    fine=rng.standard_normal((STEPS*2,SEEDS,N))*np.sqrt(dt/2)
    coarse=fine.reshape(STEPS,2,SEEDS,N).sum(1)
    rs,sigma=schedules(STEPS); rf,sf=schedules(STEPS*2)
    end=evolve(x,coarse,rs,sigma,dt)
    reflected=evolve(-x[:1],-coarse[:,:1],rs,sigma,dt)
    reflection=float(abs(np.exp(1j*reflected)-np.exp(-1j*end[:,:1])).max()); assert reflection<1e-9
    end_f=evolve(x[:REFINE],fine[:,:REFINE],rf,sf,dt/2)
    d=dict(N=N,cohort=c,reflection=reflection,coarse=quench(end),fine=quench(end_f))
    print('finished',N,c,'hits',np.sum(d['coarse']['metrics']['gap']<1e-6,axis=1).tolist(),flush=True)
    return d

def paired_test(d,rng):
    obs=float(d.mean()); count=0
    for _ in range(50):
        signs=rng.choice([-1.,1.],size=(1000,len(d))); count+=int(np.sum((signs@d/len(d))>=obs-1e-15))
    boot=d[rng.integers(len(d),size=(10000,len(d)))].mean(1)
    return obs,(1+count)/50001,np.quantile(boot,[.025,.975]).tolist()
def summary(data):
    def combine(key,res='coarse',cohort=None,subset=False):
        return np.concatenate([d[res]['metrics'][key][:,:REFINE] if subset else d[res]['metrics'][key] for d in data if cohort is None or d['cohort']==cohort],axis=1)
    def summarize(ds,res='coarse',subset=False):
        g=np.concatenate([d[res]['metrics']['gap'][:,:REFINE] if subset else d[res]['metrics']['gap'] for d in ds],axis=1)
        stats={k:np.concatenate([d[res]['metrics'][k][:,:REFINE] if subset else d[res]['metrics'][k] for d in ds],axis=1) for k in ('wall','peak','chi','near','moment','success','grad_inf')}
        return {a:dict(n=g.shape[1],hits=int(np.sum(g[i]<1e-6)),gap=float(g[i].mean()),**{k:float(np.mean(abs(v[i]))) for k,v in stats.items()}) for i,a in enumerate(ARMS)}
    g=combine('gap'); f=combine('gap','fine'); sub=combine('gap',subset=True); idx=ARMS.index('native_1'); test_rng=np.random.default_rng(84117); tests={}
    for a in ('static','sine_1','phase_1','shuffle_1'):
        j=ARMS.index(a); d=g[j]-g[idx]; effect,p,ci=paired_test(d,test_rng); win=int(sum((g[idx]<1e-6)&(g[j]>=1e-6))); loss=int(sum((g[idx]>=1e-6)&(g[j]<1e-6)))
        tests[a]=dict(gap_improvement=effect,p=p,bootstrap_ci95_unadjusted=ci,cohort_effects=[float((combine('gap',cohort=c)[j]-combine('gap',cohort=c)[idx]).mean()) for c in COHORTS],coarse_subset=float((sub[j]-sub[idx]).mean()),fine_subset=float((f[j]-f[idx]).mean()),hit_wins=win,hit_losses=loss,hit_p_two_sided=float(binomtest(win,win+loss).pvalue) if win+loss else 1.)
    running=0
    for i,a in enumerate(sorted(tests,key=lambda a:tests[a]['p'])):
        running=max(running,min(1.,(len(tests)-i)*tests[a]['p']));tests[a]['holm']=running
    rs,_=schedules(STEPS); rf,_=schedules(STEPS*2)
    def diagnostics(rs):return {a:dict(mean=float(x.mean()),rms=float(x.std()),min=float(x.min()),max=float(x.max()),below_quarter=float((x<.25).mean())) for a,x in zip(ARMS,rs)}
    return dict(pooled=summarize(data),by_size={str(N):summarize([d for d in data if d['N']==N]) for N in SIZES},by_cohort={str(c):summarize([d for d in data if d['cohort']==c]) for c in COHORTS},coarse_subset=summarize(data,subset=True),fine_subset=summarize(data,'fine'),primary=tests,primary_gate=all(v['holm']<.05 and v['gap_improvement']>0 and min(v['cohort_effects'])>0 and v['fine_subset']>0 for v in tests.values()),drive=diagnostics(rs),fine_drive=diagnostics(rf),reflection_max=max(d['reflection'] for d in data),quench_failures=sum(int((~d[k]['metrics']['success']).sum()) for d in data for k in ('coarse','fine')))
if __name__=='__main__':
    start=time.monotonic(); data=[run(N,c) for N in SIZES for c in COHORTS]; s=summary(data)
    out=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,numba=numba.__version__),arms=ARMS,physical_period=PERIOD,effective_period=P,horizon=horizon,ratio_rms=rms,shuffle_permutation=perm,steps=STEPS,summary=s,raw=data)
    (ROOT/'results.json').write_text(json.dumps(out,default=native_json,separators=(',',':'))+'\n')
    (ROOT/'summary.json').write_text(json.dumps({k:v for k,v in out.items() if k!='raw'},default=native_json,indent=2)+'\n')
    print('elapsed_seconds',time.monotonic()-start,flush=True)
    print(json.dumps(dict(primary=s['primary'],primary_gate=s['primary_gate'],pooled=s['pooled'],reflection=s['reflection_max'],quench_failures=s['quench_failures']),indent=2),flush=True)
