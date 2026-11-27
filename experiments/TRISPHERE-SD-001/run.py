import math,sys,json
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.linalg import null_space
from drv_exc_reference import exchange_basis,exchange_matrices
root=Path(__file__).resolve().parent
R0,b0,g0,o0=12.,1.,.08,.2

def branch(R,b,g,o,u):
 a=R-b; al=g/2; be=math.sqrt(o*o-al*al); w=u-2*g*b
 to=math.atan2(be*a,u+al*a)/be; vo=a*be*math.exp(al*to)/math.sin(be*to)
 ti=math.atan2(be*a,w-al*a)/be; vr=math.exp(-al*ti)*math.hypot(be*a,al*a-w)
 E=vo*vo/2; F=vr*vr/2
 return dict(u=u,w=w,E=E,F=F,loss=E-F,T=to+ti+math.log(u/w)/g if w>0 else None)
def limits(R,b,g,o):
 a=R-b; al=g/2; be=math.sqrt(o*o-al*al); t=math.atan2(be,al)/be
 Eg=.5*(a*be*math.exp(al*t)/math.sin(be*t))**2; c=branch(R,b,g,o,2*g*b)
 return dict(Eg=Eg,Ec=c['E'],Jg=Eg*(-math.expm1(-g*math.pi/be)),Jc=c['loss'])
def inner(g,o,J):
 al=g/2;be=math.sqrt(o*o-al*al);t=math.pi/be;p=math.atan2(be,al)/be;m=math.exp(-g*t);E=J/(1-m)
 return dict(E=E,T=t,m=m,peak=math.sqrt(2*E)*math.exp(-al*p)*math.sin(be*p)/be)
def shell(R,b,g,o,J):
 lo=2*g*b; hi=lo+o*R
 while branch(R,b,g,o,hi)['loss']<=J:hi=lo+2*(hi-lo)
 u=brentq(lambda u:branch(R,b,g,o,u)['loss']-J,lo,hi,xtol=1e-13*o*R)
 q=branch(R,b,g,o,u);q['m']=math.exp(-g*q['T']);return q
def scale(s,tau):
 R,b,g,o=R0*s,b0*s,g0/tau,o0/tau; e=(s/tau)**2;J=5*e;floor=3*e
 lim=limits(R,b,g,o);q=shell(R,b,g,o,J);i=inner(g,o,floor);y=np.array([0.,math.sqrt(2*q['E'])]);time=0.
 for target,direction,flat in [(R-b,1,False),(R,1,True),(R-b,-1,True),(0,-1,False)]:
  def f(t,y):return [y[1],-g*y[1]-(0 if flat else o*o*y[0])]
  def ev(t,y):return y[0]-target
  ev.terminal=True;ev.direction=direction
  sol=solve_ivp(f,(0,100*tau),y,events=ev,rtol=2e-11,atol=np.array([s,s/tau])*2e-12,max_step=.15*tau)
  assert len(sol.t_events[0])==1
  y=sol.y_events[0][0].copy();time+=sol.t_events[0][0]
  if target==R:y[1]*=-1
 return dict(s=s,tau=tau,energy_scale=e,Jcrit=lim['Jc'],Jgraze=lim['Jg'],floor=floor,ratio=lim['Jc']/floor,gap_ratio=(lim['Jc']-lim['Jg'])/floor,multiplier=q['m'],normalized_period=q['T']/tau,normalized_energy=q['E']/e,peak_ratio=i['peak']/R,ode_period_error=abs(time-q['T'])/tau,ode_loss_error=abs(q['E']-.5*y[1]**2-J)/e)
def run_scale():
 rows=[scale(s,s**p) for p in (1.,.5) for s in (1e-6,1e-4,1e-2,1.,1e2,1e4,1e6)];base=rows[3]
 keys=['ratio','gap_ratio','multiplier','normalized_period','normalized_energy','peak_ratio'];dev={k:max(abs(r[k]/base[k]-1) for r in rows) for k in keys}
 neg=[]
 for s in (.01,.1,1.,10.,100.):
  for name,tau in [('size_only',1.),('half_time_fixed_floor',math.sqrt(s))]:
   lim=limits(R0*s,b0*s,g0/tau,o0/tau);neg.append(dict(s=s,arm=name,ratio=lim['Jc']/3,gap_ratio=(lim['Jc']-lim['Jg'])/3))
 pe=max(r['ode_period_error'] for r in rows);le=max(r['ode_loss_error'] for r in rows)
 return dict(rows=rows,reference=base,max_relative_deviation=dev,max_ode_period_error=pe,max_ode_loss_error=le,negative=neg,passed=max(dev.values())<1e-7 and max(pe,le)<1e-8)

basis=exchange_basis(8,2,2,0,0);Tmat,Xmat,index=exchange_matrices(basis);N=len(basis);ps={}
for s in (1,-1):
 Z=null_space(np.vstack([Tmat,Xmat-s*np.eye(N)]));assert Z.shape==(N,1);ps[s]=Z[:,0]
lam=.1;a=R0-b0;lim0=limits(R0,b0,g0,o0);Jmid=(lim0['Jg']+lim0['Jc'])/2;Emid=(lim0['Eg']+lim0['Ec'])/2
arms=['feedback','lambda_zero','scalar_clock','one_way']
def effective(arm,x):return math.sqrt(o0**2-(2*lam*x/a**2 if arm=='feedback' else 0.))
def state(x):return (math.sqrt((1+x)/2)*ps[1]+math.sqrt((1-x)/2)*ps[-1]).astype(complex)
def excursion(E,o):
 lim=limits(R0,b0,g0,o);al=g0/2;be=math.sqrt(o*o-al*al)
 if E<lim['Eg']:
  t=math.pi/be;tp=math.atan2(be,al)/be;return dict(fate='interior',F=E*math.exp(-g0*t),period=t,peak=math.sqrt(2*E)*math.exp(-al*tp)*math.sin(be*tp)/be)
 def E_of_u(u):
  to=math.atan2(be*a,u+al*a)/be;v=a*be*math.exp(al*to)/math.sin(be*to);return .5*v*v
 hi=o*R0
 while E_of_u(hi)<E:hi*=2
 u=brentq(lambda u:E_of_u(u)-E,0,hi,xtol=1e-13)
 if u<=g0*b0:return dict(fate='stall_outbound',u=u,stall_radius=a+u/g0)
 if u<=2*g0*b0:return dict(fate='stall_inbound',u=u,stall_radius=R0-(u-g0*b0)/g0)
 q=branch(R0,b0,g0,o,u);return dict(fate='shell',F=q['F'],period=q['T'],peak=R0,u=u)
def reduced(arm,x,J,E,n=24):
 o=effective(arm,x);rows=[]
 for k in range(n):
  r=excursion(E,o);r.update(k=k,E=E);rows.append(r)
  if 'stall' in r['fate']:break
  E=r['F']+J
 fate=rows[-1]['fate'];lim=limits(R0,b0,g0,o);target=None
 if fate=='shell' and J>lim['Jc']:target=shell(R0,b0,g0,o,J)
 if fate=='interior' and J<lim['Jg']:target=inner(g0,o,J)
 return dict(arm=arm,x=x,J=J,E0=rows[0]['E'],omega_eff=o,limits=lim,fate=fate,cycles=sum('F' in r for r in rows),target=target,final_fixed_error=abs(E-target['E']) if target else None,history=rows)
def full(arm,x,J,E,n=12):
 y=np.concatenate(([0.,math.sqrt(2*E),0.],state(x))).astype(complex);rows=[];norm=0.;xe=0.;balance=0.
 def H(r):
  W=min(max(r,0.)/a,1.)**2
  if arm=='lambda_zero':return -Tmat
  if arm=='scalar_clock':return -(1+lam*W)*Tmat
  return -Tmat-lam*W*Xmat
 def total(y):
  r,v=y[:2].real;p=y[3:];return .5*v*v+.5*o0**2*min(max(r,0.),a)**2+float(np.vdot(p,H(r)@p).real)
 def deriv(flat):
  def f(t,y):
   r,v=y[:2].real;p=y[3:];force=0.
   if not flat:
    if arm=='feedback':force=2*lam*r/a**2*np.vdot(p,Xmat@p).real
    elif arm=='scalar_clock':force=2*lam*r/a**2*np.vdot(p,Tmat@p).real
   return np.concatenate(([v,-g0*v-(0 if flat else o0**2*r)+force,g0*v*v],-1j*(H(r)@p)))
  return f
 def ev(pos,direction):
  def f(t,y):return y[0].real-pos
  f.direction=direction;f.terminal=True;return f
 def turn(t,y):return y[1].real
 turn.terminal=True;turn.direction=-1
 def integrate(y,flat,events):
  nonlocal norm,xe
  sol=solve_ivp(deriv(flat),(0,250),y,events=events,method='DOP853',rtol=2e-10,atol=2e-12,max_step=.2)
  assert sol.success;pp=sol.y[3:];norm=max(norm,float(np.max(abs(np.sum(abs(pp)**2,axis=0)-1))));xe=max(xe,float(np.max(abs(np.sum(pp.conj()*(Xmat@pp),axis=0).real-x))))
  found=[i for i,z in enumerate(sol.t_events) if len(z)];assert len(found)==1,(arm,x,sol.y[:2,-1]);i=found[0]
  return sol.y_events[i][0].copy(),float(sol.t_events[i][0]),i
 for k in range(n):
  start=total(y);d0=y[2].real;t=0.;y,dt,i=integrate(y,False,[ev(a,1),turn]);t+=dt
  if i==1:
   fate='interior';peak=y[0].real;y,dt,_=integrate(y,False,[ev(0,-1)]);t+=dt
  else:
   u=y[1].real
   if u<=2*g0*b0:
    fate='stall_outbound' if u<=g0*b0 else 'stall_inbound';radius=a+u/g0 if u<=g0*b0 else R0-(u-g0*b0)/g0
    rows.append(dict(k=k,fate=fate,u=u,stall_radius=radius));break
   y,dt,_=integrate(y,True,[ev(R0,1)]);t+=dt;y[1]*=-1
   y,dt,_=integrate(y,True,[ev(a,-1)]);t+=dt;y,dt,_=integrate(y,False,[ev(0,-1)]);t+=dt;fate='shell';peak=R0
  err=abs(total(y)-start+y[2].real-d0);balance=max(balance,err)
  rows.append(dict(k=k,fate=fate,period=t,peak=peak,return_energy=.5*y[1].real**2,balance=err));y[0]=0;y[1]=math.sqrt(y[1].real**2+2*J)
 return dict(arm=arm,x=x,fate=rows[-1]['fate'],cycles=sum('period' in r for r in rows),max_norm_error=norm,max_x_error=xe,max_energy_balance_error=balance,history=rows)
def run_decision():
 main=[reduced(arm,x,Jmid,Emid) for arm in arms for x in (1.,-1.,0.)]
 numerical=[full(arm,x,Jmid,Emid) for arm in arms for x in (1.,-1.,0.)]
 grid=[reduced(arm,x,lim0['Jg']+j*(lim0['Jc']-lim0['Jg']),lim0['Eg']+e*(lim0['Ec']-lim0['Eg'])) for j in (.1,.5,.9) for e in (.1,.5,.9) for arm in arms for x in (1.,-1.,0.)]
 scan=[reduced('feedback',float(x),Jmid,Emid) for x in np.linspace(-1,1,9)]
 def expected(r):return r['fate']=='shell' if r['arm']=='feedback' and r['x']==1 else r['fate']=='interior' if r['arm']=='feedback' and r['x']==-1 else 'stall' in r['fate']
 err={k:max(r[k] for r in numerical) for k in ('max_norm_error','max_x_error','max_energy_balance_error')};m=[]
 for r,s in zip(main,numerical):
  for v,w in zip(r['history'],s['history']):
   if 'F' in v and 'period' in w:m.append(abs(v['F']-w['return_energy']))
 return dict(J=Jmid,E=Emid,base_limits=lim0,lambda_=lam,sector_dimension=N,commutator_norm=float(np.linalg.norm(Tmat@Xmat-Xmat@Tmat,2)),state_errors={str(s):dict(T=float(np.linalg.norm(Tmat@p)),X=float(np.linalg.norm(Xmat@p-s*p)),norm=float(abs(np.vdot(p,p)-1))) for s,p in ps.items()},state_overlap=float(abs(np.vdot(ps[1],ps[-1]))),main=main,numerical=numerical,grid=grid,scan=scan,max_errors=err,max_map_vs_ode_energy_error=max(m),grid_matches=sum(expected(r) for r in grid),passed=all(expected(r) for r in main+numerical+grid) and max(err.values())<1e-7 and max(m)<1e-7 and all(r['final_fixed_error']<1e-7 for r in main if r['target']))
def native(o):
 if isinstance(o,np.generic):return o.item()
 raise TypeError(type(o))
if __name__=='__main__':
 A=run_scale();print('Scale',A['passed'],A['max_relative_deviation'],A['max_ode_period_error'],A['max_ode_loss_error'],flush=True)
 B=run_decision();print('Decision',B['passed'],B['max_errors'],B['max_map_vs_ode_energy_error'],B['grid_matches'],flush=True)
 for r in B['main']:print(r['arm'],r['x'],r['fate'],r['cycles'],r['target'],r['final_fixed_error'],flush=True)
 for r in B['scan']:print('Scan',r['x'],r['fate'],r['cycles'],flush=True)
 out=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),scale=A,decision=B)
 (root/'results.json').write_text(json.dumps(out,default=native,indent=2)+'\n')
