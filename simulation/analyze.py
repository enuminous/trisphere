"""Compare the archived engine to continuous integration and resolve layer passages."""
from pathlib import Path
import csv,json,math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
OUT=R/'results'
g,J,E0=.35,1.2,2.
omega=math.sqrt(1-g*g/4)
T=math.pi/omega
q=math.exp(-g*T)
peak_t=math.atan2(omega,g/2)/omega
per_speed=math.exp(-g*peak_t/2)*math.sin(omega*peak_t)/omega
def peak(E):return math.sqrt(2*E)*per_speed
def kick_to_touch(target):return (1-q)*target**2/(2*per_speed**2)
def integrate(E):
    sol=solve_ivp(lambda t,s:[s[1],-s[0]-g*s[1]],(0,T+.1),[0,math.sqrt(2*E)],method='DOP853',rtol=3e-13,atol=1e-14,dense_output=True,max_step=.12)
    assert sol.success
    local_peak=brentq(lambda t:sol.sol(t)[1],1,2)
    ret=brentq(lambda t:sol.sol(t)[0],3,3.3)
    return sol,local_peak,ret
profiles=[]
for target in [None,6.,11.9,12.,12.1]:
    j=J if target is None else kick_to_touch(target)
    energy=j/(1-q)
    sol,tp,treturn=integrate(energy)
    peakr,v=sol.sol(tp)
    assert abs(peakr-peak(energy))<1e-9 and abs(treturn-T)<1e-9
    assert abs(sol.sol(treturn)[1]**2/2+j-energy)<1e-9
    profiles.append(dict(label='default' if target is None else f'touch-{target:g}',J=j,E_star=energy,peak=float(peakr),peak_t=tp,free_return=treturn,wall_outbound=brentq(lambda t:sol.sol(t)[0]-12,0,tp) if peakr>12+1e-9 else None))
# Grazing control is evaluated at its steady post-kick energy. Resolve every labeled crossing.
sol,tp,ret=integrate(kick_to_touch(12)/(1-q))
with (OUT/'layer_passages.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['layer','outward_time','inward_time','event'])
    for n in range(13):
        if n==0:a,b,what=0,ret,'launch / return'
        elif n==12:a,b,what=tp,tp,'smooth grazing turn'
        else:a,b,what=brentq(lambda t:sol.sol(t)[0]-n,0,tp),brentq(lambda t:sol.sol(t)[0]-n,tp,ret),'two crossings'
        w.writerow([n,a,b,what])
rows=list(csv.DictReader((OUT/'trajectories.csv').open()))
data={m:np.array([[float(r[k]) for k in ['t','r','v','energy']] for r in rows if r['model']==m]) for m in ['fixed','kick','removed']}
events=list(csv.DictReader((OUT/'returns.csv').open()))
# Independently integrate all 20 excursions, including the discontinuous energy updates.
worst=0
for mode,j in [('kick',J),('removed',0)]:
    energy=E0
    for row in [r for r in events if r['model']==mode]:
        sol_i,_,tt=integrate(energy)
        energy=sol_i.sol(tt)[1]**2/2+j
        worst=max(worst,abs(energy-float(row['energy_after'])))
assert worst<1e-9
def slope(r):return (r*(1-r/11.25)**2 if r<11.25 else 0)-(J*(1-r/3)**2 if r<3 else 0)
eq=brentq(slope,0,3)
fixed_ref=solve_ivp(lambda t,s:[s[1],-slope(s[0])-g*s[1]],(0,64),[2,0],method='DOP853',rtol=3e-12,atol=1e-13,dense_output=True)
assert fixed_ref.success
max_diff=float(np.max(np.abs(fixed_ref.sol(data['fixed'][:,0]).T-data['fixed'][:,1:3])))
assert max_diff<1e-8 and max(np.diff(data['fixed'][:,3]))<1e-12
stats=dict(gamma=g,J=J,E0=E0,period=T,q=q,E_star=J/(1-q),default_steady_peak=peak(J/(1-q)),fixed_equilibrium=eq,return_max_absolute_discrepancy=worst,fixed_max_abs_state_discrepancy=max_diff,profiles=profiles)
(OUT/'checks.json').write_text(json.dumps(stats,indent=2)+'\n')
with (OUT/'kick_thresholds.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=profiles[0]);w.writeheader();w.writerows(profiles)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#203e43','axes.edgecolor':'#9aa8a6','text.color':'#17373e','xtick.color':'#365257','ytick.color':'#365257','axes.axisbelow':True})
fig=plt.figure(figsize=(11,7.1),layout='constrained')
grid=fig.add_gridspec(2,2,height_ratios=[1.1,1]);a=fig.add_subplot(grid[0,:]);b=fig.add_subplot(grid[1,0]);c=fig.add_subplot(grid[1,1])
teal='#00796f';amber='#ae5c18';purple='#7660a2'
for m,color,l in [('fixed',purple,'Fixed position drive'),('removed',amber,'Kick removed'),('kick',teal,'Center kick')]:
    d=data[m];mask=d[:,0]<=24;a.plot(d[mask,0],d[mask,1],label=l,color=color,lw=1.8,ls='--' if m=='removed' else '-')
a.set(title='Radial motion over the first 24 time units',xlabel='Model time',ylabel='Radius ρ',xlim=(0,24),ylim=(-.03,2.15));a.legend(loc='upper right',ncol=3,frameon=False,fontsize=9)
for mode,color,label in [('kick',teal,'Kick on'),('removed',amber,'Kick off')]:
    es=[E0]+[float(r['energy_after']) for r in events if r['model']==mode]
    b.plot(np.arange(len(es)),es,color=color,lw=2,marker='.',ms=5,label=label)
b.axhline(J/(1-q),color=teal,alpha=.55,ls=':',lw=1);b.set(title='Energy after each center return',xlabel='Return number (0 is launch)',ylabel='Energy',ylim=(-.05,2.15),xticks=[0,5,10,15,20]);b.legend(loc='center right',frameon=False)
jvals=np.linspace(0,90,400);c.plot(jvals[jvals<=kick_to_touch(12)],np.sqrt(2*jvals[jvals<=kick_to_touch(12)]/(1-q))*per_speed,color=teal,lw=2)
c.plot(jvals[jvals>=kick_to_touch(12)],np.sqrt(2*jvals[jvals>=kick_to_touch(12)]/(1-q))*per_speed,color=amber,lw=1.5,ls=':')
for n,col,loc in [(6,purple,'Filter'),(12,amber,'Outer shell')]:
    j=kick_to_touch(n);c.axhline(n,color=col,lw=1,ls='--');c.scatter([j],[n],color=col,s=27,zorder=3);c.annotate(f'{loc}  J = {j:.2f}',(j,n),xytext=(3,-14 if n==12 else 6),textcoords='offset points',ha='right' if n==12 else 'left',fontsize=8,color=col)
c.scatter([J],[peak(J/(1-q))],color=teal,s=28);c.set(title='Steady excursion by kick strength',xlabel='Energy added per return J',ylabel='Peak radius ρ',xlim=(-2,90),ylim=(0,13.5))
for ax in (a,b,c):ax.grid(axis='y',color='#e0e7e5',lw=.7);ax.title.set_fontsize(12)
fig.suptitle('Tri-Sphere simulation   |   γ = 0.35',fontsize=19,fontweight='bold',x=.04,ha='left')
fig.savefig(R/'files'/'TriSphere_Simulation.png',dpi=155,facecolor='white')
print(json.dumps(stats,indent=2))
