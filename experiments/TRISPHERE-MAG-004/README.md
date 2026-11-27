# TRISPHERE-MAG-004 — Resonant Coherence
26 November 2026 (Pacific). Exploratory computational study; not peer reviewed.

**Verdict: native-waveform superiority gate FAIL; a unique TriSphere resonance is UNRESOLVED and not established.** Native frequency modestly reduces mean quenched energy gap compared with static annealing, but sine at native frequency and phase-scrambled drive at half frequency produce lower gaps. The native result does not survive the prespecified multiplicity gate.

## Model and design
Continuation of [MAG-003](https://github.com/enuminous/trisphere/tree/0b41771edeea08bfeb7900ad14d18164e577b545/experiments/TRISPHERE-MAG-003). We used its planar XY frustrated chain with exact minimum -0.75/site at r=.5, reconstructed radial orbit, and effective clock. See protocol.md for the pre-execution specification. Physical radial period 9.638611257582; effective period 12.714661850535; total effective time 152.575942206422; all nonstatic arms mean r=.5 and RMS 0.172941615226. This is a forced overdamped stochastic model, not a derivation of a material or a spin-wave resonance.

17 arms, three sizes, two cohorts, 12 independent seed pairs per size/cohort (72 seeds per arm), 1224 primary runs, 612 half-step runs on nested seeds, 102 reflected trajectories. Each run shares noise and initial conditions across treatments; all primary and refined quenches returned optimizer success, all respected the exact energy bound within 1e-10, and maximum reflected unit-vector discrepancy was zero. Optimizer success is not ground-state success. No independent replication or external preregistration.

## Results
Coarse and half-step columns use 72 and 36 seeds per arm respectively; matched coarse subset also uses 36 seeds. Wall is the chirality sign-change bond fraction after quench.

|Arm|Primary hits|Mean gap/site|Wall fraction|Matched coarse hits|Matched fine hits|Fine gap/site|r range|Fraction r<.25|
|---|---:|---:|---:|---:|---:|---:|---|---:|
|static|5|0.03691580|0.072627|3|1|0.03906151|0.500000–0.500000|0.000000|
|native_0.5|4|0.03324948|0.063657|1|2|0.03452900|0.158664–0.756875|0.111328|
|native_1|4|0.03256615|0.065104|2|2|0.03590861|0.159975–0.756115|0.109375|
|native_2|6|0.03676955|0.073495|3|4|0.03240728|0.162595–0.757051|0.109375|
|native_4|5|0.03677308|0.072338|2|5|0.03506035|0.167713–0.754073|0.109375|
|sine_0.5|4|0.03257211|0.063947|1|2|0.03183160|0.255425–0.744575|0.000000|
|sine_1|10|0.03041073|0.060764|5|2|0.03328795|0.255435–0.744565|0.000000|
|sine_2|4|0.03553137|0.068287|3|4|0.03594062|0.255425–0.744575|0.000000|
|sine_4|4|0.03864897|0.076968|1|3|0.03966844|0.255515–0.744485|0.000000|
|phase_0.5|10|0.03025593|0.060475|5|5|0.02904656|0.275194–0.787732|0.000000|
|phase_1|5|0.03706275|0.074074|1|1|0.03588749|0.275245–0.787654|0.000000|
|phase_2|6|0.03488344|0.069734|3|3|0.03386121|0.275701–0.787570|0.000000|
|phase_4|5|0.03982043|0.079282|3|2|0.03854964|0.275269–0.786558|0.000000|
|shuffle_0.5|6|0.03676857|0.073495|3|4|0.03211894|0.158664–0.756875|0.111328|
|shuffle_1|4|0.03735260|0.073495|2|2|0.03589624|0.159975–0.756115|0.109375|
|shuffle_2|0|0.04183161|0.083623|0|2|0.03938264|0.162595–0.757051|0.109375|
|shuffle_4|2|0.03966612|0.078125|1|4|0.03331716|0.167713–0.754073|0.109375|

All 408 coarse trials at N=96 missed the exact ground. Full per-size, per-cohort, per-seed and refinement results are provided in summary.json and results.json.

## Primary comparisons
Positive gap improvement favors native at 1×. One-sided sign-flip test uses paired exchangeability/symmetry under the null; Holm-adjusted across four comparisons. Bootstrap intervals in summary.json are unadjusted. The gate requires all adjusted p<.05 and positive effects in both cohorts and refined subset.

|Control at 1× (or static)|Gap improvement|Raw p|Holm p|Cohort 0 effect|Cohort 1 effect|Fine subset effect|
|---|---:|---:|---:|---:|---:|---:|
|static|+0.00434965|0.038819|0.085198|+0.00434451|+0.00435479|+0.00315290|
|sine_1|-0.00215542|0.783384|0.783384|+0.00090015|-0.00521099|-0.00262067|
|phase_1|+0.00449660|0.019660|0.078638|+0.00900470|-0.00001149|-0.00002112|
|shuffle_1|+0.00478646|0.028399|0.085198|+0.00346740|+0.00610551|-0.00001237|

The native waveform lowered gap relative to static by 11.8% descriptively and retained this direction in both cohorts and fine subset, but adjusted p=.0852 and unadjusted 95% bootstrap interval crosses zero. No primary comparison passed Holm; phase and shuffle advantages vanish on refinement. Native had 4/72 ground hits, static 5/72, sine at 1× and phase-scrambled at .5× both 10/72. Frequency sweep is exploratory; no significance test for post hoc winners. Native has the lowest native-waveform energy gap at 1×, but that is insufficient to infer resonance.

## Limitations and next test
RMS matching does not match instantaneous ranges, higher harmonics, or time below r=.25. The sine and phase-scramble controls never cross that threshold; native and shuffle do for about 11% of effective time. Each scrambled control is a single fixed realization. Half-step comparison is limited to half the seeds and does not establish asymptotic numerical convergence. Model has no physically derived differential coupling, backreaction, or spin inertia. Claims about EuSi or the physical validity of TriSphere remain unsupported. A follow-on should sample surrogate ensembles, separately match threshold exposure and range, confirm lower-frequency candidates on fresh seeds, and compare longer budgets against conventional annealing.

## Replay
Environment: python 3.13.5, numpy 2.3.5, scipy 1.17.0, numba 0.65.1. Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=4 python run.py > log.txt` after installing requirements.txt. `mag003_reference.py` is the MAG-003 source snapshot, imported for the original orbit and objective. `pre_execution.sha256` records the exact protocol and run.py before execution; `MANIFEST.sha256` covers the delivered evidence. The elapsed time in log.txt is not deterministic.
