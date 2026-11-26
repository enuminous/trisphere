# RETURN-MAP-002 — Upper energy boundedness for bounded central kicks
2026-11-25 · Monolithic LLC · Beth's conjecture, analytical derivation with AI assistance.

## Assumptions
A regular one-dimensional hybrid trajectory on [0,R], R>0; bounded nonnegative continuous piecewise differentiable potential V with maximum M; constant gamma>0; between impacts x''=-V'(x)-gamma*x'; non-energy-producing outer reflection; central kicks only at completed excursions, adding energy J_n in [0,Jmax]. No other drive, and no repeated kicks at rest without excursions. Energy E=v²/2+V. Normalize V(0)=0. Claims apply to well-defined trajectories on their domain; global existence across singular events is not asserted.

## Proof
Between kicks E'=-gamma*v², and outer impacts cannot increase E. Define total loss L over an excursion (including any impact loss). Suppose launch E exceeds Ec=M+Jmax+Jmax²/(8 gamma² R²) and a completed excursion loses at most Jmax. Throughout, energy >=E-Jmax, hence speed >=sqrt(2(E-Jmax-M))>0 between impacts. No interior turning point is possible, so the excursion goes to R and back, traversing 2R. Continuous dissipative loss alone is gamma*integral |v| ds >=2 gamma R sqrt(2(E-Jmax-M))>Jmax, contradiction. Thus any completed excursion launched above Ec loses more than Jmax and its next launch energy decreases. Otherwise its next launch is at most Ec+Jmax. Induction and monotonicity between kicks give E(t)<=max(E0,M+2Jmax+Jmax²/(8 gamma² R²)). An incomplete excursion receives no additional kicks and cannot grow in energy. Nonnegative energy is automatic; positive lower energy and return accessibility are not implied.

## Candidate constants
R=12, gamma=.08, V=.02 min(x,11)², M=2.42, Jmax=5. Ec=10.810842013888889, ceiling=15.810842013888889. Exact expression: 2.42+10+25/(8*.08²*12²). The ceiling is conservative, not sharp. Bounded valve position must control energy, not merely velocity increments. Persistent breathing requires separate proof. No physical units or cosmological validation inferred.

## Status
Analytical derivation; not independently reviewed or Lean checked. Prior candidate: https://github.com/enuminous/trisphere/blob/58c756870b601e7b83b6dcccec071daa2ca6d366/protocol/RETURN-MAP-001.md
