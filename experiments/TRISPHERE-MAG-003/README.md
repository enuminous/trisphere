# TRISPHERE-MAG-003 — Formation of Coherence
26 November 2026 (Pacific) | Monolithic LLC | Exploratory numerical experiment; not peer reviewed.

Predecessor: [TRISPHERE-MAG-002](../TRISPHERE-MAG-002/README.md), parent commit 8b27d640c7b298c2208ad75f554201e97f43b5e1. The prior random-start L-BFGS test at r=.5 had 0/72 ground hits. The present annealing protocol differs in compute budget and initial seeds, so this is not a matched comparison with MAG-002.

## Model and findings
The periodic XY chain has H=sum_j[cos(theta_(j+1)-theta_j)+r cos(theta_(j+2)-theta_j)]. At r=.5, all tested lengths are divisible by three, and the exact minimum is -0.75 per site. The reconstructed radial cycle has period 9.638611257581818. A common positive mobility f=1+.6*rho/12 defines the matched effective clock; over 12 cycles the clock is 152.57603223052882. The differential exchange ratio is centered at .5 using effective-time weights and varies approximately .159486 to .755636, crossing the collinear/spiral threshold .25. This differential law was chosen for exploration, not derived from the Blueprint. There is no spin backreaction.

Use 32 matched initial angle vectors and Gaussian noise paths for each N=24,48,96; Euler-Maruyama in effective time with 240 steps/cycle, a common decreasing temperature, and final deterministic quench at r=.5. The common breathing arm is identical to the static arm in the numerical effective-clock formulation; it is a constructed negative control, not an independent numerical test of the time-change theorem. The fourth arm ramps r=.2 to .5; this is only one conventional schedule, not an optimized baseline.

| Arm | N=24 hits | N=48 hits | N=96 hits | Total |
|---|---:|---:|---:|---:|
| Static | 7 | 1 | 0 | 8/96 |
| Scalar | 7 | 1 | 0 | 8/96 |
| Differential | 10 | 1 | 0 | 11/96 |
| Ramp | 0 | 0 | 0 | 0/96 |

Ground criterion: gap per site <1e-6. Differential versus static: 10 paired wins, 7 losses, two-sided exact binomial p=.629058837890625. Differential versus this ramp: 11 wins, 0 losses, nominal p=.0009765625; exploratory, unadjusted, and not a general comparison with conventional schedules.

At N=48, differential wall density at 25/50/75/100% annealing time was .4375/.3216/.0924/.0625; static .3698/.2839/.0924/.0664. After quench, differential near-120 bond fraction .9375, mean peak Fourier weight .40505, mean absolute global chirality .26083 and mean net moment .00038. Static corresponding values .93620/.42752/.31535/.00081. Local order does not imply global coherence. Bond-sign flips are a proxy for domain boundaries, not calibrated physical domain lengths.

Reflection of initial conditions AND noise (4 pairs per size/arm) had zero measured unit-vector discrepancy; no preferred handedness is introduced. Reflection pairs are not independent estimates of spontaneous preference. Halving step size for eight Brownian-coupled seeds per size changes individual outcomes (N=24 coarse/fine hits: static 3/2, differential 0/3, ramp 0/0). Larger-size ground recovery remains poor. No robust differential advantage over static annealing is established.

## Disposition
PASS: observed local ordering and reduced domain-wall proxy; some exact ground-state recovery; ground energy bound on tested coarse quenched states; reflected dynamical symmetry. FAIL: universal ground-state recovery in tested runs. UNRESOLVED: robust differential advantage, continuum/time-step convergence of hit rates, physically derived coupling, and EuSi-specific prediction. The scalar control is an identity by construction. None of these results validates the TriSphere Blueprint, predicts EuSi's phase transition or domain size, or demonstrates an actual new material mechanism.

## Replay
Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0. `OPENBLAS_NUM_THREADS=1 python run.py > log.txt` writes full angle endpoints, per-seed observables, checkpoints, reflection errors, and paired comparisons to results.json. The local evidence package includes full raw output. The protocol is recorded before execution but not independently preregistered. MAG-004 should predeclare a discriminator against ordinary time-dependent frustrated exchange; test matched waveform amplitude/frequency, shuffled or phase-scrambled drive and longer anneals, with larger independent seeds and refinement. Derive the coupling separately before making a TriSphere-specific claim.
