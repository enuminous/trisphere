"""Exchange-only spiral benchmark; all parameters dimensionless, no EuSi fit."""
import json
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], complex)
SY = np.array([[0, -1j], [1j, 0]], complex)
SZ = np.diag([1, -1]).astype(complex)
P = np.linspace(-np.pi, np.pi, 241)
E = np.linspace(-3.5, 3.5, 351)
T = 1.0

def lor(x, eta):
    return eta / (np.pi * (x*x + eta*eta))

def spectrum(L, winding, J, b=0., eta=.08, phase=0.):
    Q = 2*np.pi*winding/L
    theta = Q*np.arange(L) + phase
    moments = np.stack((np.sqrt(1-b*b)*np.sin(theta), np.full(L,b),
                        np.sqrt(1-b*b)*np.cos(theta)), axis=1)
    direct = np.empty((len(P), len(E), 4))
    analytic = np.empty((len(P), len(E), 2))
    max_sumrule = 0.
    for ip, p in enumerate(P):
        H = np.zeros((2*L, 2*L), complex)
        for n, (x,y,z) in enumerate(moments):
            H[2*n:2*n+2,2*n:2*n+2] += J*(x*SX+y*SY+z*SZ)
            m = (n+1)%L
            hop = -T * (np.exp(1j*p*L) if n == L-1 else 1.)*I
            H[2*n:2*n+2,2*m:2*m+2] += hop
            H[2*m:2*m+2,2*n:2*n+2] += hop.conj().T
        w, v = np.linalg.eigh(H)
        W = np.vstack([np.exp(1j*p*n)*I/np.sqrt(L) for n in range(L)])
        a = W.conj().T @ v
        weights = np.stack([np.einsum('in,ij,jn->n', a.conj(), op, a).real
                            for op in (I,SX,SY,SZ)])
        direct[ip] = lor(E[:,None]-w[None,:],eta) @ weights.T
        for col,s in enumerate((1,-1)):
            k = p+s*Q/2
            H2 = -2*T*np.cos(k)*np.cos(Q/2)*I + (J*b-2*T*np.sin(k)*np.sin(Q/2))*SY
            H2 += J*np.sqrt(1-b*b)*(np.cos(phase)*SZ+np.sin(phase)*SX)
            w2,v2 = np.linalg.eigh(H2)
            ws = np.einsum('in,ij,jn->n',v2.conj(),(I+s*SY)/2,v2).real
            max_sumrule = max(max_sumrule, abs(float(ws.sum())-1))
            analytic[ip,:,col] = lor(E[:,None]-w2[None,:],eta) @ ws
    A = direct[:,:,0]
    Y = direct[:,:,2]
    spin = Y/A
    mask = A > .10*A.max()
    even = .5*(Y+Y[::-1])
    odd = .5*(Y-Y[::-1])
    scale = A.max()
    mnet = np.linalg.norm(moments.mean(axis=0))
    chirality = np.cross(moments,np.roll(moments,-1,axis=0)).mean(axis=0)[1]
    info = dict(L=L,winding=winding,J=J,b=b,eta=eta,phase=phase,
        mean_moment=float(mnet), chirality_y=float(chirality),
        peak_polarization=float(np.max(abs(spin[mask]))),
        odd_spectral_max=float(np.max(abs(odd))/scale),
        even_spectral_max=float(np.max(abs(even))/scale),
        odd_weighted_rms=float(np.sqrt(np.sum(odd**2)/np.sum(A**2))),
        transverse_spectral_residual=float(np.max(abs(direct[:,:,[1,3]]))/scale),
        independent_unfolding_residual=float(np.max(abs(direct[:,:,[0,2]]-np.stack((analytic.sum(axis=2),analytic[:,:,0]-analytic[:,:,1]),axis=2)))/scale),
        spin_sumrule_residual=float(max_sumrule),
        node_residual=float(np.max(abs(Y[[0,len(P)//2,-1]]))/scale))
    return info, direct

specs = [
 ('spiral',3,1,1.,0.,.08,0.),('reversed',3,-1,1.,0.,.08,0.),
 ('zero_exchange',3,1,0.,0.,.08,0.),('collinear_AF',2,1,1.,0.,.08,0.),
 ('six_step',6,1,1.,0.,.08,0.),('conical',3,1,1.,.35,.08,0.),
 ('ferro_y',1,0,1.,1.,.08,0.),('weak_exchange',3,1,.25,0.,.08,0.),
 ('strong_exchange',3,1,2.,0.,.08,0.),('narrow',3,1,1.,0.,.04,0.),
 ('broad',3,1,1.,0.,.16,0.),('phase_shift',3,1,1.,0.,.08,1.234),
]
infos, arrays = {}, {}
for name,*args in specs:
    infos[name],arrays[name] = spectrum(*args)
base = arrays['spiral']; rev = arrays['reversed']
scale = base[:,:,0].max()
mixture = (base+rev)/2
extra = dict(chirality_flip_residual=float(np.max(abs(base[:,:,2]+rev[:,:,2]))/scale),
             domain_mixture_spin_residual=float(np.max(abs(mixture[:,:,2]))/scale),
             phase_shift_spin_residual=float(np.max(abs(base[:,:,2]-arrays['phase_shift'][:,:,2]))/scale),
             phase_shift_intensity_residual=float(np.max(abs(base[:,:,0]-arrays['phase_shift'][:,:,0]))/scale))
# The fixed window is a visualization cut, not selected as an experimental Fermi level.
ie = int(np.argmin(abs(E+.8)))
cut = {name: [[float(p),float(a[i,ie,0]),float(a[i,ie,2]/a[i,ie,0])] for i,p in enumerate(P)]
       for name,a in arrays.items() if name in ('spiral','reversed','zero_exchange','collinear_AF','conical')}
checks = {
 'net_zero': infos['spiral']['mean_moment'] < 1e-12,
 'odd_nonzero': infos['spiral']['odd_spectral_max'] > .01,
 'odd_parity': infos['spiral']['even_spectral_max'] < 1e-12,
 'node': infos['spiral']['node_residual'] < 1e-12,
 'spin_axis': infos['spiral']['transverse_spectral_residual'] < 1e-12,
 'chirality_flip': extra['chirality_flip_residual'] < 1e-12,
 'equal_domain_cancellation': extra['domain_mixture_spin_residual'] < 1e-12,
 'zero_exchange': infos['zero_exchange']['peak_polarization'] < 1e-12,
 'collinear_net_zero': infos['collinear_AF']['mean_moment'] < 1e-12 and infos['collinear_AF']['peak_polarization'] < 1e-12,
 'six_step': infos['six_step']['odd_spectral_max'] > .01 and infos['six_step']['even_spectral_max'] < 1e-12,
 'conical_even': infos['conical']['even_spectral_max'] > .01,
 'ferro_even': infos['ferro_y']['odd_spectral_max'] < 1e-12 and infos['ferro_y']['even_spectral_max'] > .01,
 'common_phase_invariance': max(extra['phase_shift_spin_residual'],extra['phase_shift_intensity_residual']) < 1e-12,
 'independent_unfolding': max(v['independent_unfolding_residual'] for v in infos.values()) < 1e-11,
 'sumrule': max(v['spin_sumrule_residual'] for v in infos.values()) < 1e-12,
 'broadening_and_exchange': all(infos[n]['odd_spectral_max'] > .01 and infos[n]['even_spectral_max'] < 1e-12 for n in ('weak_exchange','strong_exchange','narrow','broad')),
}
result = dict(environment=dict(python=sys.version.split()[0],numpy=np.__version__),
              momentum_points=len(P),energy_points=len(E),cut_energy=float(E[ie]),
              cases=infos,comparisons=extra,checks=checks,cut=cut)
(ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
np.savez_compressed(ROOT/'spectra.npz',momentum=P,energy=E,components=np.array(['I','Sx','Sy','Sz']),**arrays)
print(json.dumps({k:v for k,v in result.items() if k!='cut'},indent=2))
assert all(checks.values()), checks
print(f'{sum(checks.values())}/{len(checks)} checks passed')
