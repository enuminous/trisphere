import numpy as np,json
from pathlib import Path
N=48; B=12; T=3000; WASH=200; SPLIT=2000; DT=.05; SUB=20

def tri(u,seed,beta=1,shelf=True):
 r=np.random.default_rng(seed); x=r.uniform(.1,11.9,N);v=r.uniform(-3,3,N);out=[]
 for inp in u:
  for _ in range(SUB):
   j=np.minimum((x*4).astype(int),47);cnt=np.bincount(j,minlength=48);s=np.bincount(j,weights=v,minlength=48);mean=s[j]/cnt[j];v=mean+(v-mean)*np.exp(-beta*DT)
   def force(x):return np.where((x>=11)|((x>=3.5)&(x<=4.5)&shelf),0,-.04*x)
   v+=force(x)*DT/2;v*=np.exp(-.08*DT);x+=v*DT
   hit=x>12;x[hit]=24-x[hit];v[hit]=-abs(v[hit]);hit=x<0;x[hit]=-x[hit];v[hit]=np.sqrt(v[hit]**2+2*(3+2*inp));v+=force(x)*DT/2
  j=np.minimum((x/12*B).astype(int),B-1);out.append(np.r_[np.bincount(j,minlength=B)/N,np.bincount(j,weights=v,minlength=B)/N])
 return np.array(out)
def esn(u,seed):
 r=np.random.default_rng(seed);W=r.normal(size=(24,24));W*=.9/max(abs(np.linalg.eigvals(W)));w=r.normal(size=24);h=np.zeros(24);out=[]
 for z in u:h=.5*h+.5*np.tanh(W@h+w*z);out.append(h.copy())
 return np.array(out)
def score(X,y,binary=False):
 tr=X[WASH:SPLIT];te=X[SPLIT:];mu=tr.mean(0);sd=tr.std(0);sd[sd<1e-9]=1;tr=(tr-mu)/sd;te=(te-mu)/sd;tr=np.c_[np.ones(len(tr)),tr];te=np.c_[np.ones(len(te)),te];reg=np.eye(tr.shape[1])*.01;reg[0,0]=0;w=np.linalg.solve(tr.T@tr+reg,tr.T@y[WASH:SPLIT]);p=te@w;actual=y[SPLIT:];return float(np.mean((p>=.5)==actual)) if binary else float(1-np.mean((p-actual)**2)/np.var(actual))
def main():
 results=[]
 for seed in [42,43,44]:
  u=np.random.default_rng(seed+100).choice([-1.,1.],T);b=(u>0).astype(int);targets={'delay1':(np.roll(u,1),False),'delay3':(np.roll(u,3),False),'delay5':(np.roll(u,5),False),'xor':(b^np.roll(b,1),True),'parity3':(b^np.roll(b,1)^np.roll(b,2),True),'temporal_and':(b&np.roll(b,2),True)}
  features={'TriSphere':tri(u,seed),'No coupling':tri(u,seed,0),'No inner shelf':tri(u,seed,1,False),'ESN':esn(u,seed),'Linear taps':np.column_stack([np.roll(u,k) for k in range(24)])}
  for name,X in features.items():results.append({'seed':seed,'model':name,**{k:score(X,y,bi) for k,(y,bi) in targets.items()}})
  print('seed',seed,flush=True)
 p=Path(__file__).parent/'results.json';p.write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
if __name__=='__main__':main()
