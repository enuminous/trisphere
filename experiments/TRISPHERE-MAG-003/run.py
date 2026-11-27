import json, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent
SIZES = (24, 48, 96)
ARMS = ('static', 'scalar', 'differential', 'ramp')
SEEDS = 32
CYCLES = 12
STEPS = 240

def orbit():
    state = [0., np.sqrt(2*7.268050808342798)]
    t = 0.; segments = []
    for target, sign, inner in [(11,1,True),(12,1,False),(11,-1,False),(0,-1,True)]:
        def event(t,z): return z[0]-target
        event.terminal=True; event.direction=sign
        sol=solve_ivp(lambda t,z:[z[1],-.08*z[1]-(.04*z[0] if inner else 0.)],(t,t+50),state,events=event,rtol=1e-11,atol=1e-12,dense_output=True)
        assert len(sol.t_events[0])==1
        segments.append(sol); t=float(sol.t[-1]); state=sol.y[:,-1].copy()
        if target==12: state[1]*=-1
    assert abs(7.268050808342798-state[1]**2/2-5)<1e-8
    def radius(t):
        return next(float(s.sol(t)[0]) for s in segments if t<=s.t[-1]+1e-12)
    return t, radius

PERIOD, radius = orbit()

def gradient(x,r):
    a=np.sin(np.roll(x,-1,axis=-1)-x); b=np.sin(np.roll(x,-2,axis=-1)-x)
    return a-np.roll(a,1,axis=-1)+r*(b-np.roll(b,2,axis=-1))

def objective(x):
    return float(np.sum(np.cos(np.roll(x,-1)-x)+.5*np.cos(np.roll(x,-2)-x))), gradient(x,.5)

def metrics(x):
    d=np.roll(x,-1,axis=-1)-x; z=np.exp(1j*x); chi=np.sin(d)
    return dict(gap=np.mean(np.cos(d)+.5*np.cos(np.roll(x,-2,axis=-1)-x),axis=-1)+.75,
                peak=np.max(abs(np.fft.fft(z,axis=-1)/x.shape[-1])**2,axis=-1),
                chi=np.mean(chi,axis=-1),wall=np.mean((chi>0)!= (np.roll(chi,-1,axis=-1)>0),axis=-1),
                near=np.mean(abs(np.arccos(np.cos(d))-2*np.pi/3)<np.pi/12,axis=-1),moment=abs(z.mean(axis=-1)))

def schedule(steps):
    u=np.array([radius((j+.5)*PERIOD/steps)/12 for j in range(steps)])
    dt=(1+.6*u)*PERIOD/steps
    center=np.average(u,weights=dt)
    return np.tile(dt,CYCLES),np.tile(.5+.6*(u-center),CYCLES)

def integrate(x, noise, dt, ratios):
    x=x.copy(); traces=[]
    elapsed=np.cumsum(dt)-dt/2; s=elapsed/dt.sum(); T=1.2*(1-s)**2+.015
    for j,(h,temp,r) in enumerate(zip(dt,T,ratios)):
        x-=h*gradient(x,r); x+=np.sqrt(2*temp)*noise[j]
        if j+1 in (len(dt)//4,len(dt)//2,3*len(dt)//4,len(dt)):
            traces.append(metrics(x))
    return x,traces

def run(N):
    rng=np.random.default_rng(20261126+N)
    x=rng.uniform(-np.pi,np.pi,(SEEDS,N)); dt,rd=schedule(STEPS); hf,rf=schedule(2*STEPS)
    # Brownian increments on fine grid; coarse increments are the sum of paired increments.
    # Rescale fine increments in each coarse interval to match its midpoint clock length.
    fine=rng.normal(size=(len(hf),SEEDS,N))*np.sqrt(hf)[:,None,None]
    fine*=np.repeat(np.sqrt(dt/hf.reshape(-1,2).sum(1)),2)[:,None,None]
    coarse=fine.reshape(-1,2,SEEDS,N).sum(1)
    # Use the same adjusted fine clock in the refinement, exactly preserving coarse sums.
    hf=hf*np.repeat(dt/hf.reshape(-1,2).sum(1),2)
    def ratio_map(h,r):
        s=(np.cumsum(h)-h/2)/h.sum()
        return dict(static=np.full(len(h),.5),scalar=np.full(len(h),.5),differential=r,ramp=.2+.3*s)
    results={}; fine_results={}; checkpoints={}; reflection={}; endpoints={}; refined_endpoints={}
    for arm,rs in ratio_map(dt,rd).items():
        end,tr=integrate(x,coarse,dt,rs)
        reflected,_=integrate(-x[:4],-coarse[:,:4],dt,rs)
        reflection[arm]=float(abs(np.exp(1j*reflected)-np.exp(-1j*end[:4])).max())
        f_end,_=integrate(x[:8],fine[:,:8],hf,ratio_map(hf,rf)[arm])
        def quench(y):
            return np.array([minimize(objective,row,jac=True,method='L-BFGS-B',options={'maxiter':2000,'ftol':1e-13,'gtol':1e-9}).x for row in y])
        q=quench(end); fq=quench(f_end)
        results[arm]=metrics(q); fine_results[arm]=metrics(fq); checkpoints[arm]=tr
        endpoints[arm]=q; refined_endpoints[arm]=fq
    assert np.array_equal(endpoints['static'],endpoints['scalar'])
    assert max(reflection.values())<1e-10
    assert min(v['gap'].min() for v in results.values())>-1e-10
    return dict(N=N,results=results,fine=fine_results,checkpoints=checkpoints,reflection=reflection,angles=endpoints,refined_angles=refined_endpoints)

def native(o):
    if isinstance(o,np.ndarray):return o.tolist()
    if isinstance(o,np.generic):return o.item()
    raise TypeError(type(o))

def summarize(m):
    return dict(n=len(m['gap']),hits=int(sum(m['gap']<1e-6)),**{k:float(np.mean(abs(v) if k=='chi' else v)) for k,v in m.items()})

if __name__=='__main__':
    data=[run(N) for N in SIZES]
    summary=[]
    for row in data:
        summary.append(dict(N=row['N'],arms={a:summarize(v) for a,v in row['results'].items()},fine={a:summarize(v) for a,v in row['fine'].items()},coarse_subset={a:summarize({k:v[:8] for k,v in m.items()}) for a,m in row['results'].items()},checkpoints={a:[summarize(m) for m in tr] for a,tr in row['checkpoints'].items()},reflection=row['reflection']))
    def paired(a,b):
        aa=np.concatenate([r['results'][a]['gap']<1e-6 for r in data]); bb=np.concatenate([r['results'][b]['gap']<1e-6 for r in data]); win=int(sum(aa&~bb)); loss=int(sum(bb&~aa))
        return dict(win=win,loss=loss,p=float(binomtest(win,win+loss).pvalue) if win+loss else 1.)
    dt,r=schedule(STEPS)
    out=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),period=PERIOD,clock=float(dt.sum()),ratio_range=[float(r.min()),float(r.max())],summary=summary,paired={a:paired('differential',a) for a in ('static','ramp')},raw=data)
    (ROOT/'results.json').write_text(json.dumps(out,default=native,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='raw'},default=native,indent=2))
