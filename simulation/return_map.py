"""Piecewise exact TriSphere return map; standard library only."""
import math,json
w,g,J,b,wall=.2,.08,5.,11.,12.
a=g/2; wd=math.sqrt(w*w-a*a)
def harmonic(x,v,t):
    B=(v+a*x)/wd;c=math.cos(wd*t);s=math.sin(wd*t);e=math.exp(-a*t)
    return e*(x*c+B*s),e*(-a*(x*c+B*s)+wd*(-x*s+B*c))
def bisect(f,l,r):
    fl=f(l)
    if fl*f(r)>0: raise ValueError("not bracketed")
    for _ in range(65):
        m=(l+r)/2
        if f(m)==0:return m
        if (f(m)>0)==(fl>0):l=m
        else:r=m
    return (l+r)/2
def return_map(E):
    if E<=0: raise ValueError("positive launch required")
    v=math.sqrt(2*E);peak=math.atan(wd/a)/wd
    if harmonic(0,v,peak)[0]<=b:
        T=math.pi/wd
        return dict(next=J+E*math.exp(-g*T),T=T,wall=False)
    t1=bisect(lambda t:harmonic(0,v,t)[0]-b,0,peak)
    v1=harmonic(0,v,t1)[1];delta=g*(wall-b)
    if v1<=2*delta:raise ValueError("flat band traversal or return not supported")
    t2=-math.log1p(-delta/v1)/g;vw=v1-delta
    t3=-math.log1p(-delta/vw)/g;vi=-(vw-delta)
    t4=bisect(lambda t:harmonic(b,vi,t)[0],0,math.pi/wd)
    vr=harmonic(b,vi,t4)[1]
    return dict(next=J+vr*vr/2,T=t1+t2+t3+t4,wall=True,vr=vr,vw=vw)
def run():
    E=bisect(lambda e:return_map(e)["next"]-e,7,8);r=return_map(E)
    trajectories={}
    for initial in (5,10,20):
        e=initial;vals=[e]
        for _ in range(15):e=return_map(e)["next"];vals.append(e)
        trajectories[str(initial)]=vals
    derivative=math.exp(-g*r["T"])
    fd=(return_map(E+1e-5)["next"]-return_map(E-1e-5)["next"])/2e-5
    assert r["wall"] and abs(r["next"]-E)<1e-10 and abs(fd-derivative)<1e-7
    return dict(E=E,orbit=r,loss=J,multiplier=derivative,finite_difference=fd,trajectories=trajectories)
if __name__=="__main__": print(json.dumps(run(),indent=2))
