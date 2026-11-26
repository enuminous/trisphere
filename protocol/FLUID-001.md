# TRISPHERE-FLUID-001 — interacting packets and shelf entrainment
Monolithic LLC · exploratory computation · 2026-11-26 publication.

## Specification
240 equal-mass particles, 60 initially stationary at x in [3.65,4.15), others seeded uniformly in [.1,11.8) with signed speed in [1,3). Seeds 42,43,44, deterministic 32-bit LCG. Radius 12; shelves [3.5,4.5] and [11,12]. Continuous potential V=.02 times x² up to 3.5, 12.25 through 4.5, x²-8 through 11, then 113. Damping .08, external central energy increment 5, elastic outer reflection. Equal-width .25 spatial cells; local velocity relaxation v_i <- mean + (v_i-mean) exp(-beta dt), conserves cell momentum and dissipates relative kinetic energy. Split force/damping/drift update with approximate reflected crossing, not exact event localization. Duration 160; dt=.02,.01; beta=0,.2,1. No prescribed carrier velocity. No pressure, interface, or diffusion model.

## Results
18 runs, 51,840,000 particle updates. Recovery means a tagged stationary particle is observed outside [3.5,4.5] at least once, not permanent recirculation. Shelf occupancy counts particles, not volumetric density.
| beta | Mean escapes /60 | Range | Peak occupancy /240 |
|---|---:|---:|---:|
| 0 | 0.000 | 0–0 | 92 |
| 0.2 | 37.167 | 9–60 | 121 |
| 1 | 60.000 | 60–60 | 189 |
Maximum momentum residual during mixing 6.821210263296962e-13; maximum absolute energy budget residual 8.91991024600577. Particle count fixed by construction. Fine-step moderate coupling remains sensitive; no convergence claim. The earlier chat rounded moderate recovery to 61.9%; exact mean is 61.9444%. Strong coupling yielded 60/60 across all six runs. Pooling can be transient. No physical bubbles, persistent foam, or validated cosmology established. Initial stalled packets were planted. No no-shelf or uncoupled-pressure comparator run; full fluid and continuum limit remain unresolved. Momentum conservation applies to the relaxation substep, not external forces or boundaries.

## Reproduce
Run node simulation/fluid001.js > fluid001-replay.json from repository root. Published results regenerated with the same JavaScript algorithm; no independent runtime replay or reviewer claimed. See evidence/FLUID-001.json for full per-run summaries and 20-time-unit samples. No changes to historical audit verdicts.

Next: FLUID-002 should test no-shelf controls, spatial and temporal refinement, pressure and interface closure, and unseeded structure formation.
