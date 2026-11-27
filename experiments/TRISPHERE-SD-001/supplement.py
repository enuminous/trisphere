"""Post-main exploratory checks; not part of primary gate."""
import json, math
from pathlib import Path
from scipy.optimize import brentq
from run import limits, shell, inner, R0,b0,g0,o0,lam,a,Jmid,Emid, effective, reduced, lim0

def margins(x):
    l=limits(R0,b0,g0,effective('feedback',x))
    return dict(inner_launch=l['Eg']-Emid,inner_kick=l['Jg']-Jmid,shell_launch=Emid-l['Ec'],shell_kick=Jmid-l['Jc'])
roots={key:brentq(lambda x:margins(x)[key],-1,1) for key in margins(0)}
# Both launch and constant-kick conditions are necessary for the guaranteed pure branch.
# Here all margins are monotone on the tested range; thresholds are numerical roots.
checks=[]
for p in (1.,.5):
    for s in (1e-6,1e-4,1e-2,1.,1e2,1e4,1e6):
        tau=s**p; e=(s/tau)**2; R=R0*s;b=b0*s;g=g0/tau;o=o0/tau;ll=lam*e
        for x in (-1.,1.):
            oo=math.sqrt(o**2-2*ll*x/(R-b)**2); l=limits(R,b,g,oo); J=Jmid*e; E=Emid*e
            if x==1:
                launch_margin=(E-l['Ec'])/e;kick_margin=(J-l['Jc'])/e;q=shell(R,b,g,oo,J);peak=1.
            else:
                launch_margin=(l['Eg']-E)/e;kick_margin=(l['Jg']-J)/e;q=inner(g,oo,J);peak=q['peak']/R
            assert launch_margin>0 and kick_margin>0
            checks.append(dict(s=s,tau=tau,x=x,launch_margin=launch_margin,kick_margin=kick_margin,period=q['T']/tau,multiplier=q['m'],peak_ratio=peak,energy=q['E']/e))
# Identical state-independent force (+/- lambda W potential) can remove the stall,
# but because it has no internal-state dependence it gives the same fate for everyone.
force_controls=[dict(state_independent_force_sign=x, fates=[reduced('feedback',x,Jmid,Emid)['fate'] for _ in (1,-1,0)]) for x in (-1.,1.)]
ref={x:next(z for z in checks if z['x']==x and z['s']==1) for x in (-1.,1.)}
errors={k:max(abs(z[k]/ref[z['x']][k]-1) for z in checks) for k in ('launch_margin','kick_margin','period','multiplier','peak_ratio','energy')}
out=dict(note='Exploratory analytic reduced-sector similarity only; generic full quantum evolution not scale invariant for fixed hbar under these transformations.',roots=roots,inner_guaranteed_below=min(roots['inner_launch'],roots['inner_kick']),shell_guaranteed_above=max(roots['shell_launch'],roots['shell_kick']),scaled_state_checks=checks,max_relative_errors=errors,state_independent_controls=force_controls)
Path('supplement.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='scaled_state_checks'},indent=2))
