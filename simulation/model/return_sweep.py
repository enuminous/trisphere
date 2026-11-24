"""Independent continuous integration and bounded iteration of the declared return map."""
import argparse
import json
import math
from collections import Counter
from pathlib import Path

def rk4(x,v,h,g):
    def rhs(y,w): return w,-y-g*w
    a,b=rhs(x,v)
    c,d=rhs(x+h*a/2,v+h*b/2)
    e,f=rhs(x+h*c/2,v+h*d/2)
    i,j=rhs(x+h*e,v+h*f)
    return x+h*(a+2*c+2*e+i)/6,v+h*(b+2*d+2*f+j)/6

def event(E,g):
    x,v,t,h=0.,math.sqrt(2*E),0.,1/160
    for _ in range(1600):
        y,w=rk4(x,v,h,g)
        if x>0 and y<=0:
            lo,hi=0.,h
            for _ in range(44):
                mid=(lo+hi)/2
                if rk4(x,v,mid,g)[0]>0: lo=mid
                else: hi=mid
            _,end_v=rk4(x,v,hi,g)
            return t+hi,end_v**2/2
        x,v,t=y,w,t+h
    raise ValueError("Center event missing")

def classify(g,J,E):
    start=E
    omega=math.sqrt(1-g*g/4)
    period=math.pi/omega
    peak_time=math.atan2(omega,g/2)/omega
    peak_per_speed=math.exp(-g*peak_time/2)*math.sin(omega*peak_time)/omega
    cap_energy=(12/peak_per_speed)**2/2
    q=math.exp(-g*period)
    fixed=J/(1-q) if g else None
    wall=None
    if start==0: reason='rest without a trigger';n=0
    elif q==1 and J==0: reason='neutral continuum';n=0
    elif q==1:
        n=math.floor((cap_energy-E)/J)+1
        E+=n*J;wall=n;reason='growth to wall exit'
    else:
        for n in range(257):
            if E>cap_energy: reason='wall exit';wall=n;break
            if abs(E-fixed)<=1e-8: reason='decay to zero' if J==0 else 'positive fixed point';break
            if n==256: reason='iteration budget';break
            E=q*E+J
    return dict(gamma=g,J=J,E0=start,q=q,E_star=fixed,last_energy=E,returns=n,outcome=reason,first_exit_orbit_index=wall)

def main(outfile):
    checks=[]
    for g in [0,.35,1.2]:
        for E in [.5,2,8]:
            t,e=event(E,g);T=math.pi/math.sqrt(1-g*g/4)
            err_t=abs(t-T);err_e=abs(e-E*math.exp(-g*T))
            assert max(err_t,err_e)<1e-7,(g,E,t,e)
            checks.append(dict(gamma=g,E0=E,return_time=t,incoming_energy=e,time_error=err_t,energy_error=err_e))
    grid=[classify(g,j,e) for g in [0,.05,.35,1.2,1.5] for j in [0,.25,1.2,5] for e in [0,.5,2,8]]
    assert len(grid)==80
    result=dict(protocol='protocol/extension.md',integrations=checks,sweep=grid,counts=dict(Counter(r['outcome'] for r in grid)))
    outfile.parent.mkdir(parents=True,exist_ok=True)
    outfile.write_text(json.dumps(result,indent=2)+'\n')
    print('9/9 independent-implementation comparisons met 1e-7; 80/80 cases terminated.',result['counts'])
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path)
    main(parser.parse_args().output)
