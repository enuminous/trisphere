# Tri-Sphere simulation · 24 November 2026

The default timed kick produces a stable center-to-center excursion. In dimensionless units, its limiting energy immediately after a return is 1.7839314709 and its peak radius is 1.4741058111. With the kick removed, the same harmonic oscillator has post-return energy 3.99×10⁻¹⁰ at return 20. The separate smooth position-driven model is near its equilibrium radius 0.766145868 at t=64.

## Inputs and trajectories

The unchanged JavaScript engine and Python grid runner were extracted from the previously delivered TriSphere_Zoo_Laboratory.zip, SHA-256 b27eb90ea40a6641d268a7d89f405e71990dafa7cadb02c8a28f4a7f596ee602. No data fitting or sampling seeds were used.

All three traces have γ=0.35, span 64 and output spacing 0.005. The fixed-drive law uses k=1.2 and starts at r=2 with v=0. Its smooth potential differs from the harmonic control, so its energy zero and initial state have a different meaning. The harmonic kick-on and kick-off runs both launch from the center at E₀=2, v=2. They differ only in the energy added at incoming center returns, J=1.2 or 0. Returns are 3.190832193 model time units apart. The first plot shows 24 of the 64 time units. CSV energy rows are instantaneous samples; exact before/after event energies are in a separate file.

## Reaching the layers

For a unit-mass, unit-spring half-oscillator the section update is Eₙ₊₁ = qEₙ + J with q=exp(−γπ/ω) and ω=√(1−γ²/4). The steady energy is J/(1−q). A flight from that energy has radius r(t)=√(2E) exp(−γt/2) sin(ωt)/ω until the next center event or a wall crossing. Peak time is atan2(ω,γ/2)/ω. Hence the required steady kick scales with the square of the desired peak radius. Numerically integrated excursions independently checked the calculated thresholds and both sides of the wall threshold.

The layer-6 and layer-12 scenarios use J≈19.88046 and J≈79.52184, respectively. These are an explicit extrapolation beyond the browser's drive slider (0–5). The new cases begin at their respective steady post-kick energy. A layer-12 grazing turn arises from the harmonic restoring force. The test targeting a free peak of 12.1 at J≈80.85273 first crosses the wall at t≈1.28906; subsequent unconstrained values in the thresholds table describe the formal free oscillator only. The dotted curve above 12 likewise denotes extrapolated free motion. No wall-impact or filter-transfer mechanics are imposed. An exact threshold approached from a lower initial energy need not be reached in finite cycles.

## Output files

- results/trajectories.csv contains all three engine traces, with t, r, v and energy.
- results/returns.csv records exact center-return times and incoming/outgoing energies.
- results/kick_thresholds.csv records five continuous-solver scenarios.
- results/layer_passages.csv records launch, grazing turn, return and both passage times at intermediate layers for the layer-12 orbit.
- results/checks.json contains the formula, integrator comparison metrics and derived constants as numeric summaries. results/runs.json records the original engine outputs and extrema.
- results/original-grid.json contains the fresh 80-case sweep of the lab's previously defined grid, plus its nine first-return integrator checks.
- files/TriSphere_Simulation.png is the summary figure.

## Replay

From the extracted directory, run the following commands with Node 18+ and Python with NumPy, SciPy and Matplotlib installed.

```sh
node run.js
python3 model/return_sweep.py results/original-grid.json
python3 analyze.py
```

The SciPy DOP853 solver integrated the fixed-drive trajectory separately and located the harmonic return and apogee as roots. For the matched 20-return comparisons its energies agreed with the engine within 1.60×10⁻¹⁴. Its maximum position/velocity discrepancy on the fixed-drive trace was 3.52×10⁻¹¹. These checks share the declared equations and parameter choices. Physical interpretation remains open.
