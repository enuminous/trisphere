import json, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize
from scipy.integrate import solve_ivp, quad

root=Path(__file__).resolve().parent
sizes=[24,48,96]
ratios=[0,.2,.25,.3,.4,.5,.6,.8,1]
def energy_grad(x,r):
    d1=np.roll(x,-1)-x; d2=np.roll(x,-2)-x
    s1=np.sin(d1); s2=np.sin(d2)
    return float(np.sum(np.cos(d1)+r*np.cos(d2))), s1-np.roll(s1,1)+r*(s2-np.roll(s2,2))
def observables(x,r):
    e,g=energy_grad(x,r); z=np.exp(1j*x); f=abs(np.fft.fft(z)/len(x))**2
    return dict(e=e/len(x),moment=float(abs(z.mean())),chi=float(np.sin(np.roll(x,-1)-x).mean()),dominant_q_deg=float(np.fft.fftfreq(len(x))[np.argmax(f)]*360),peak_weight=float(f.max()),gradient_inf=float(abs(g).max()))
exact=[]
for N in sizes:
    for r in ratios:
        q=2*np.pi*np.arange(N)/N; es=np.cos(q)+r*np.cos(2*q); j=int(np.argmin(es)); qj=min(q[j],2*np.pi-q[j]); x=qj*np.arange(N)
        o=observables(x,r); o.update(N=N,r=r,q_deg=float(np.degrees(qj)),continuum_deg=float(np.degrees(np.arccos(-1/(4*r)))) if r>.25 else 180.,bound=float(es.min()),gap=o['e']-float(es.min()))
        exact.append(o)
relax=[]; rng=np.random.default_rng(20261126)
for N in sizes:
    for r in [.2,.5,.8]:
        bound=min(x['bound'] for x in exact if x['N']==N and x['r']==r)
        for seed in range(12):
            x=rng.uniform(-np.pi,np.pi,N); pair=[]
            for sign in [1,-1]:
                opt=minimize(energy_grad,sign*x,args=(r,),jac=True,method='L-BFGS-B',options={'maxiter':1500,'ftol':1e-13,'gtol':1e-9})
                o=observables(opt.x,r); o.update(sign=sign,converged=bool(opt.success),iterations=int(opt.nit),gap=o['e']-bound,angles=opt.x.tolist()); pair.append(o)
            relax.append(dict(N=N,r=r,seed=seed,pair=pair,energy_reflection_error=abs(pair[0]['e']-pair[1]['e']),chirality_reflection_error=abs(pair[0]['chi']+pair[1]['chi'])))
# Unfolded physical-momentum spin spectrum; standard exchange model, not a fit.
p=np.linspace(-np.pi,np.pi,241); en=np.linspace(-3.5,3.5,151); eta=.08
def spectral(Q,J):
    vals=[]
    for s in [1,-1]:
        k=p+s*Q/2; a=-2*np.cos(k)*np.cos(Q/2); b=-2*np.sin(k)*np.sin(Q/2); d=np.sqrt(J*J+b*b)
        z=np.divide(b,d,out=np.zeros_like(b),where=d>1e-14)
        v=np.zeros((len(p),len(en)))
        for branch in [1,-1]:
            w=(1+s*branch*z)/2; delta=en[None,:]-(a+branch*d)[:,None]; v+=w[:,None]*eta/(np.pi*(delta**2+eta**2))
        vals.append(v)
    return vals[0]+vals[1],vals[0]-vals[1]
spec=[]; cuts={}; idx=int(np.argmin(abs(en+.8)))
for r in ratios:
    Q=np.arccos(-1/(4*r)) if r>.25 else np.pi
    A,Y=spectral(Q,1); Ar,Yr=spectral(-Q,1); A0,Y0=spectral(Q,0); scale=A.max(); mask=A>.1*scale
    spec.append(dict(r=r,q_deg=float(np.degrees(Q)),odd=float(abs((Y-Y[::-1])/2).max()/scale),even=float(abs((Y+Y[::-1])/2).max()/scale),flip=float(abs(Y+Yr).max()/scale),zero_exchange=float(abs(Y0).max()/A0.max()),peak=float(abs(Y[mask]/A[mask]).max())))
    if r in [.2,.5,.8]: cuts[str(r)]=(Y[:,idx]/A[:,idx]).tolist()
# QG/TRISPHERE return-map candidate: solve four segments on a single known orbit.
# Central launch energy from RETURN-MAP-001, no backreaction from the added spins.
state=[0.,np.sqrt(2*7.268050808342798)]; t=0.; segments=[]
for target,sgn,inner in [(11,1,True),(12,1,False),(11,-1,False),(0,-1,True)]:
    def event(t,z):return z[0]-target
    event.terminal=True;event.direction=sgn
    s=solve_ivp(lambda t,z:[z[1],-.08*z[1]-(.04*z[0] if inner else 0.)],(t,t+50),state,events=event,rtol=1e-11,atol=1e-12,dense_output=True)
    assert len(s.t_events[0])==1
    segments.append(s); t=float(s.t[-1]); state=s.y[:,-1].copy()
    if target==12:state[1]*=-1
period=t; loss=7.268050808342798-state[1]**2/2
breaks=[s.t[-1] for s in segments[:-1]]
def radius(t):
    t=min(max(t,0),period)
    for s in segments:
        if t<=s.t[-1]+1e-12:return float(s.sol(t)[0])
    raise ValueError(t)
def factor(t):return 1+.6*radius(t)/12
clock=quad(factor,0,period,points=breaks,epsabs=1e-10)[0]
clock_tests=[]
for j in range(8):
    x=rng.uniform(-np.pi,np.pi,24)
    f=lambda t,x:-energy_grad(x,.5)[1]
    a=solve_ivp(f,(0,clock),x,rtol=1e-10,atol=1e-11).y[:,-1]
    b=solve_ivp(lambda t,x:factor(t)*f(t,x),(0,period),x,rtol=1e-10,atol=1e-11,max_step=.03).y[:,-1]
    c=solve_ivp(lambda t,x:factor(t)*f(t,x),(0,period),-x,rtol=1e-10,atol=1e-11,max_step=.03).y[:,-1]
    clock_tests.append(dict(seed=j,clock_error=float(abs(np.exp(1j*a)-np.exp(1j*b)).max()),reflection_error=float(abs(np.exp(1j*c)-np.exp(-1j*b)).max())))
summary=[]
for N in sizes:
    for r in [.2,.5,.8]:
        cases=[p for row in relax if row['N']==N and row['r']==r for p in row['pair']]; summary.append(dict(N=N,r=r,n=len(cases),ground_hits=sum(p['gap']<1e-6 for p in cases),positive=sum(p['chi']>1e-5 for p in cases),negative=sum(p['chi']<-1e-5 for p in cases),max_gap=max(p['gap'] for p in cases),converged=sum(p['converged'] for p in cases)))
checks=dict(exact_bound=max(abs(x['gap']) for x in exact)<1e-12,three_step_at_half=all(abs(x['q_deg']-120)<1e-10 for x in exact if x['r']==.5),pitch_not_universal=any(abs(x['q_deg']-120)>10 for x in exact),reflection_energy=max(x['energy_reflection_error'] for x in relax)<1e-8,reflection_chirality=max(x['chirality_reflection_error'] for x in relax)<1e-8,ground_bound_respected=min(p['gap'] for x in relax for p in x['pair'])>-1e-10,odd_parity=max(x['even'] for x in spec)<1e-10,chirality_flip=max(x['flip'] for x in spec)<1e-10,zero_exchange=max(x['zero_exchange'] for x in spec)<1e-10,collinear_null=max(x['odd'] for x in spec if x['r']<=.25)<1e-10,spiral_signal=min(x['odd'] for x in spec if x['r']>.25)>.01,return_orbit=abs(loss-5)<1e-8,clock_equivalence=max(x['clock_error'] for x in clock_tests)<1e-6,clock_reflection=max(x['reflection_error'] for x in clock_tests)<1e-8)
result=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),exact=exact,relax=relax,summary=summary,spectral=spec,cut=dict(momentum=p.tolist(),energy=float(en[idx]),spin=cuts),oscillator=dict(period=period,loss=loss,effective_time=clock,tests=clock_tests),checks=checks)
(root/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['environment','summary','spectral','oscillator','checks']},indent=2)); assert all(checks.values()),checks
