# TRISPHERE-MAG-005 — Criticality and Defect Erasure
Exploratory computational study, following MAG-004; not independently preregistered or peer reviewed.

**Verdict: specified crossing-harm gate FAIL; a universal threshold-crossing penalty is not established.** A deep excursion transiently reduces local target-pitch order; this is a descriptive observation in an ad hoc driven spin model, not evidence of a material mechanism. The observed recovery is consistent with, but does not prove, an explanation of the weak final effect.

## Model and design
Use MAG-004's classical periodic XY chain H=sum[cos(theta_(j+1)-theta_j)+r cos(theta_(j+2)-theta_j)], r=J2/J1, and radial oscillator effective clock P=12.714661850535; horizon=12P=152.575942206422. At final r=.5 the exact ground energy is -.75/site for N=24,48,96. Infinite-chain minimizing twist is pi for r<=1/4 and arccos(-1/(4r)) above. The first finite-ring pitch transition occurs at r=1/[2(1+cos(2pi/N))], i.e. .254333, .251074, .250268 respectively. Thus .24 and .26 straddle the first discrete ground-state crossover in all tested rings. Neither ground-state crossover is assumed to be a finite-temperature dynamical singularity.

The eight pulse interventions use L=.18,.24,.26,.32 for 1/8 of the period, then two compensating levels each for 7/16. Let p=1/8, m=(.5-pL)/(1-p), v=(sigma^2-p(L-.5)^2)/(1-p)-(m-.5)^2 with sigma=.172941615226. The other levels are m +/- sqrt(v). Mean r=.5 and RMS sigma match across all driven arms; 1x and 2x pulse trains at each L share a histogram. Crossing arms spend 12.5% of effective time below .25; noncrossing arms spend none. Native and sine references have respective exposures 10.9375% and 0%. Static has no modulation. Compensation changes levels/range along with L, so the design does not isolate a binary causal effect of threshold crossing. Rectangular drives are chosen interventions, not derived from the oscillator.

Use 96 independent seed paths per arm (16 per size/cohort), paired across arms, Euler-Maruyama (3072 steps), common annealing temperature and final L-BFGS-B quench at r=.5. Fine Brownian increments aggregate to coarse; first eight seeds per size/cohort also tested at 6144 steps. One reflected initial state and noise path per arm/size/cohort. Total 1056 coarse and 528 refined quenches, 66 reflection controls. See pre-execution protocol and hashes.

## Primary outcomes
Ground hit: final gap/site <1e-6. Lower gap is better. Fine: nested 48 seeds per arm.

| Arm | Coarse hits /96 | Mean gap/site | Wall proxy | Fine hits /48 | Fine gap/site |
|---|---:|---:|---:|---:|---:|
| static | 1 | 0.04038807 | 0.080729 | 2 | 0.03992740 |
| native_1 | 4 | 0.03690546 | 0.073785 | 5 | 0.03540458 |
| sine_1 | 9 | 0.03409020 | 0.068142 | 3 | 0.03517583 |
| pulse_0.18_1x | 6 | 0.03562244 | 0.070312 | 2 | 0.03734845 |
| pulse_0.24_1x | 8 | 0.03355688 | 0.066189 | 5 | 0.03390459 |
| pulse_0.26_1x | 9 | 0.03257803 | 0.065104 | 8 | 0.03105006 |
| pulse_0.32_1x | 12 | 0.02986864 | 0.058811 | 6 | 0.03104551 |
| pulse_0.18_2x | 8 | 0.03735645 | 0.073785 | 6 | 0.03408106 |
| pulse_0.24_2x | 8 | 0.03323052 | 0.065538 | 3 | 0.03343449 |
| pulse_0.26_2x | 7 | 0.03885794 | 0.077691 | 2 | 0.03649418 |
| pulse_0.32_2x | 7 | 0.03744808 | 0.074870 | 3 | 0.03652753 |

All 352 primary runs at N=96 missed the exact ground state. The best descriptive arm (.32, 1x) reduces mean gap by 26.0% versus static; it was not a prespecified inferential comparison. Neither a general superiority claim nor a physical resonance is warranted.

## Paired primary tests
Positive effects mean crossing is worse. Each seed contributes the average paired gap difference over 1x and 2x; one-sided 50,000-draw sign-flip tests assume sign symmetry/exchangeability under null. Bootstrap intervals are unadjusted and resample within size/cohort. Holm correction across both contrasts. The support gate required both adjusted p<.05 and positive effects in both cohorts, both timing patterns and fine subset.

| Contrast | Mean difference | Raw p | Holm p | Unadjusted bootstrap 95% interval | Cohort 0 | Cohort 1 | 1x | 2x | Fine subset |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| deep | +0.00283108 | 0.030099 | 0.060199 | [-0.00005386, +0.00572302] | +0.00315436 | +0.00250780 | +0.00575380 | -0.00009164 | +0.00192824 |
| near | -0.00232429 | 0.928701 | 0.928701 | [-0.00526864, +0.00060512] | +0.00066512 | -0.00531369 | +0.00097885 | -0.00562742 | -0.00010258 |

Deep contrast favors avoiding crossings descriptively in both cohorts, all sizes and nested fine subset, but not at both timing patterns, and adjusted p=.060199. Near contrast has the opposite pooled direction, changes sign by cohort/timing and is nearly zero at half step. The specified gate fails. This is not proof of equivalence or proof that deep crossing is harmless.

## Intra-pulse dynamics
Average over last four native periods, all seeds and sizes. Near-target fraction means unsigned bond angle within 15 degrees of 120 degrees. Wall proxy counts flips in bond chirality sign; it is not calibrated physical wall density and is unreliable near collinear order. Differences in these descriptive observables are not inferential tests.

| Arm | Near before | After low | End cycle | Change low | Fine change low | Wall before | After low | End cycle |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| pulse_0.18_1x | 0.506239 | 0.487006 | 0.609755 | -0.019233 | -0.021756 | 0.098307 | 0.102919 | 0.083930 |
| pulse_0.24_1x | 0.521729 | 0.523058 | 0.626085 | +0.001329 | +0.002062 | 0.089247 | 0.091797 | 0.074327 |
| pulse_0.26_1x | 0.524387 | 0.529812 | 0.628961 | +0.005425 | +0.000760 | 0.086534 | 0.090115 | 0.072483 |
| pulse_0.32_1x | 0.521891 | 0.541070 | 0.628499 | +0.019179 | +0.004395 | 0.088976 | 0.087999 | 0.071289 |
| pulse_0.18_2x | 0.552368 | 0.542494 | 0.602932 | -0.009874 | -0.017578 | 0.093804 | 0.093913 | 0.086507 |
| pulse_0.24_2x | 0.562907 | 0.561469 | 0.616686 | -0.001438 | -0.002848 | 0.083957 | 0.083984 | 0.077284 |
| pulse_0.26_2x | 0.552070 | 0.554172 | 0.603421 | +0.002102 | -0.000977 | 0.096327 | 0.096110 | 0.089166 |
| pulse_0.32_2x | 0.552897 | 0.562717 | 0.604031 | +0.009820 | +0.005778 | 0.094564 | 0.093587 | 0.087945 |

Deep crossing reduces local 120-degree order during the low segment at both tested pulse frequencies and both discretizations. The .32 noncrossing arm increases it. Subsequent high-r portions restore local order; the full-cycle endpoint remains less than perfectly ordered. These observations do not track individual defects, prove their annihilation or establish a causal threshold effect. Local order, global winding and chirality-domain coarsening are distinct.

## Verification and limitations
All 1584 quenches reported optimizer success and respected the exact ground-energy bound; minimum recorded gap 0, maximum final gradient infinity norm 7.40e-6. Maximum reflected unit-vector discrepancy 0 in 66 controls; no handedness bias introduced. All pre-execution source/protocol hashes verified. Half-step results do not demonstrate asymptotic convergence, especially of individual ground hits. A single clock and rectangular waveform family are tested, not a general causal threshold intervention; finite-size effects, longer budgets, pulse depth/timing, and microscopic origin remain unresolved. No empirical EuSi prediction or TriSphere validation follows.

Next discriminator: prepare controlled pairs of opposite-chirality domains at known separation and a known winding sector; compare probability of annihilation versus new defect nucleation under matched driving and static schedules, with tracking across time rather than a local pitch proxy alone. Use winding and phase slips as additional observables; a new protocol should separate varying separation, duration, waveform and temperature. Do not infer topological protection merely from poor ground recovery.

## Replay
Python 3.13.5; NumPy 2.3.5; SciPy 1.17.0; Numba 0.65.1. Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python run.py > log.txt` after installing requirements. The reference scripts are exact copies of the prior package's run.py and mag003_reference.py (renamed MAG-004 script only). `results.json` contains per-seed angles after quench, observables at endpoints and intra-pulse snapshots (metrics, not snapshot angles), including half-step results. `summary.json` contains all aggregated contrasts. `pre_execution.sha256` seals inputs locally; `MANIFEST.sha256` covers this package. No external preregistration or independent replication. Runtime is not deterministic. GitHub unchanged.
