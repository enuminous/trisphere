"""Exploratory hybrid-oscillator and constrained-exchange checks. No fit or material prediction."""
import itertools, json, math, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parent
R=12.

def branch(gamma,omega,b,u):
    a=R-b; alpha=gamma/2; beta=math.sqrt(omega**2-alpha**2)
    assert u>=2*gamma*b
    to=math.atan2(beta*a,u+alpha*a)/beta
    v=a*beta*math.exp(alpha*to)/math.sin(beta*to)
    w=u-2*gamma*b
    ti=math.atan2(beta*a,w-alpha*a)/beta
    vr=math.exp(-alpha*ti)*math.hypot(beta*a,alpha*a-w)
    E=v*v/2; loss=E-vr*vr/2
    T=to+ti+math.log(u/w)/gamma if w>0 else math.inf
    return dict(u=u,w=w,launch_speed=v,return_speed=vr,E=E,loss=loss,T=T,t_out=to,t_in=ti)

def thresholds(g,o,b):
    a=R-b; al=g/2; beta=math.sqrt(o*o-al*al)
    t=math.atan2(beta,al)/beta
    E_graze=.5*(a*beta*math.exp(al*t)/math.sin(beta*t))**2
    J_graze=E_graze*(-math.expm1(-g*math.pi/beta))
    return branch(g,o,b,2*g*b)['loss'], J_graze

def fixed_shell(g,o,b,J):
    low=2*g*b
    assert J>thresholds(g,o,b)[0]
    hi=low+1
    while branch(g,o,b,hi)['loss']<=J: hi=low+2*(hi-low)
    u=brentq(lambda u:branch(g,o,b,u)['loss']-J,low,hi,xtol=1e-13)
    return branch(g,o,b,u)

def segment(g,o,y,goal,direction,flat=False):
    def f(t,y): return (y[1],-g*y[1]-(0 if flat else o*o*y[0]))
    def ev(t,y):return y[0]-goal
    ev.terminal=True; ev.direction=direction
    sol=solve_ivp(f,(0,10000),y,events=ev,rtol=2e-11,atol=2e-12,max_step=.15)
    assert len(sol.t_events[0])==1
    return sol.y_events[0][0],float(sol.t_events[0][0])

def verify_cycle(g,o,b,J):
    q=fixed_shell(g,o,b,J); a=R-b
    y=(0,q['launch_speed']); T=0
    for goal,direction,flat in [(a,1,False),(R,1,True),(a,-1,True),(0,-1,False)]:
        y,t=segment(g,o,y,goal,direction,flat); T+=t
        if goal==R: y[1]*=-1
    h=max(1e-7,1e-5*(q['u']-2*g*b)); lo=branch(g,o,b,q['u']-h); hi=branch(g,o,b,q['u']+h)
    map_slope=((hi['E']-hi['loss'])-(lo['E']-lo['loss']))/(hi['E']-lo['E'])
    expected=math.exp(-g*q['T'])
    return dict(J=J,E=q['E'],period=q['T'],multiplier=expected,ode_period=T,ode_loss=q['E']-.5*y[1]**2,ode_period_error=abs(T-q['T']),ode_loss_error=abs(q['E']-.5*y[1]**2-J),slope_fd=map_slope,slope_error=abs(map_slope-expected))

def inner_orbit(g,o,J):
    beta=math.sqrt(o*o-(g/2)**2); t=math.atan2(beta,g/2)/beta
    E=J/(-math.expm1(-g*math.pi/beta))
    return dict(launch_energy=E,peak_radius=math.sqrt(2*E)*math.exp(-g/2*t)*math.sin(beta*t)/beta,period=math.pi/beta,multiplier=math.exp(-g*math.pi/beta))

def exchange_basis(N,plus,minus,Q,P):
    return [s for s in itertools.product((-1,0,1),repeat=N) if s.count(1)==plus and s.count(-1)==minus and sum(s)==Q and sum(i*x for i,x in enumerate(s))==P]

def exchange_matrices(basis):
    N=len(basis[0]); index={s:i for i,s in enumerate(basis)}; n=len(basis)
    T=np.zeros((n,n)); X=np.zeros((n,n)); missing=0
    for j,s in enumerate(basis):
        for i in range(N-2):
            for sign in (-1,1):
                a,b=(sign,-sign,0),(0,sign,-sign)
                if s[i:i+3] not in (a,b):continue
                target=s[:i]+(b if s[i:i+3]==a else a)+s[i+3:]
                if target not in index: missing+=1;continue
                T[index[target],j]+=1
        for i in range(N-3):
            a,b=(1,-1,-1,1),(-1,1,1,-1)
            if s[i:i+4] not in (a,b):continue
            target=s[:i]+(b if s[i:i+4]==a else a)+s[i+4:]
            if target not in index: missing+=1;continue
            X[index[target],j]+=1
    assert not missing
    assert np.array_equal(T,T.T) and np.array_equal(X,X.T)
    return T,X,index

def exchange_checks():
    N=8
    one=exchange_basis(N,1,0,1,3); T1,X1,_=exchange_matrices(one)
    pair=exchange_basis(N,1,1,0,-1); T2,X2,_=exchange_matrices(pair)
    eig=np.linalg.eigvalsh(-T2); exact=np.sort(-2*np.cos(np.pi*np.arange(1,N)/N))
    both=exchange_basis(N,2,2,0,0); T,X,idx=exchange_matrices(both)
    s=(0,0,1,-1,-1,1,0,0); target=(0,0,-1,1,1,-1,0,0); i,j=idx[s],idx[target]
    k=.3; t=1.; H=-t*T-k*X
    U=expm(-1j*H*.2)
    U0=expm(-1j*(-t*T)*.2)
    comm=np.linalg.norm(T@X-X@T,ord=2)
    out=dict(N=N,isolated_charge_sector_dimension=len(one),isolated_charge_hopping_norm=float(np.linalg.norm(T1)),single_dipole_sector_dimension=len(pair),single_dipole_eigenvalues=eig.tolist(),single_dipole_band_error=float(max(abs(eig-exact))),opposite_dipole_sector_dimension=len(both),exchange_matrix_element=float(H[j,i]),exchange_removed_matrix_element=float((-t*T)[j,i]),example_exchange_probability=float(abs(U[j,i])**2),exchange_removed_probability=float(abs(U0[j,i])**2),commutator_norm=float(comm),unitarity_error=float(np.linalg.norm(U.conj().T@U-np.eye(len(both)),ord=2)))
    assert out['single_dipole_band_error']<1e-12 and out['isolated_charge_hopping_norm']==0 and out['exchange_matrix_element']==-.3 and out['exchange_removed_matrix_element']==0 and comm>0 and out['unitarity_error']<1e-12
    return out

if __name__=='__main__':
    rows=[]
    for o,g,b in itertools.product((.16,.20,.24),(.04,.08,.12),(.5,1.,2.)):
        Jc,Jg=thresholds(g,o,b); v=verify_cycle(g,o,b,Jc*1.1)
        rows.append(dict(gamma=g,omega=o,band_width=b,J_crit=Jc,J_graze=Jg,floor_shell_access=3>Jc,verification=v))
    gamma=.08; omega=.20; b=1.
    Jc,Jg=thresholds(gamma,omega,b)
    ref=dict(J_crit=Jc,J_graze=Jg,minimum_extra_drive_infimum=Jc-3,gamma_crit=brentq(lambda g:thresholds(g,omega,b)[0]-3,.04,.12),floor_orbit=inner_orbit(gamma,omega,3),J5_cycle=verify_cycle(gamma,omega,b,5),sufficient_grid_count=sum(r['floor_shell_access'] for r in rows))
    maxes={key:max(r['verification'][key] for r in rows) for key in ('ode_period_error','ode_loss_error','slope_error')}
    assert maxes['ode_period_error']<1e-6 and maxes['ode_loss_error']<1e-8 and maxes['slope_error']<1e-6
    assert ref['floor_orbit']['peak_radius']<11 and ref['sufficient_grid_count']==13
    out=dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),reference=ref,grid=rows,maximum_verification_errors=maxes,exchange=exchange_checks())
    (ROOT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='grid'},indent=2))
