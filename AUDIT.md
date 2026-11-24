# Tri-Sphere Zoo audit

**24 November 2026 · A. Beth Jones’s TGS:ATE / ORION blueprint · Monolithic Zoo**

The mirror works on all thirteen layers. The original dynamical claim fails for a more interesting reason than a poorly chosen parameter. If the valve setting is fixed, a force depending only on position gives back on the inward trip exactly the work it supplied on the outward trip. Positive damping still takes energy away. A moving orbit therefore cannot repeat indefinitely under that smooth law. The blueprint itself recognizes this in its later five-position section, where it calls for a drive timed to the breath.

Adding a timed center kick produces a constructive example. Its working parts are identifiable, the kick can be removed, and its loss of motion can be measured. This result establishes a mechanism for the example. The drive, valve and field coupling of a physical Tri-Sphere remain **UNRESOLVED**.

## What was examined

The target is the attached plain-text manuscript, including both parts, dated corrections and final caveats. The original bytes are in [source/blueprint.md](source/blueprint.md), SHA-256 `a93e2539d89c5cd5a1558fda2bc19557fcc4433cf99620621aa3b79550e1cff4`. Line references count the opening code fence as line 1. The source names Beth as the framework’s author; the November 19 technical companion identifies her as A. Beth Jones. The two linked living documents, social posts, referenced books and private conversations are external context. The audit does not attribute their contents or measurements to this upload.

[Claim-by-claim findings](CLAIMS.md) cover all ten numbered equations, later corrections and major cross-domain extensions. [The complete operation roster](ROSTER.md) records each input requirement, decision rule, actual execution or applicability review, and source. [The protocol](protocol/criteria.md) fixes the acceptance criteria for this retrospective audit. [The diagnostic extension](protocol/extension.md) records the subsequent numerical comparisons. The auditor wrote and ran the proof, adapters and controls in one environment. Independent reproduction remains open.

| Inventory | PASS | FAIL | UNRESOLVED | NOT_APPLICABLE |
|---|---:|---:|---:|---:|
| 32 scoped source findings | 11 | 9 | 11 | 1 |
| 53 named Zoo entries | 1 | 3 | 38 | 11 |

The first row counts propositions. The second counts outcomes against the declared **target** question for each operation. Neither row estimates the probability that the physical framework is true. The target-specific runs were CAT, TURTLE, WEASEL, CHIMERA, CIRCUS, MONSTER and PEGASUS. Several tools consume human-supplied fields. For example, TURTLE enforces a veto whose mathematical basis is the energy theorem; counting its result again would double-count the same evidence.

## Equation 10 correction, 24 November 2026

Beth’s revised text calls the thirteen layers the atlas and the five positions the observer’s GPS view of a single oscillator. The observer sits at Layer 6. The inner and outer membranes represent inhale and exhale. Beth describes the emergence of additional layers from Filter imbalance as an interpretation. The revised text also restricts Hopf circles to positive radii and states that damping slows motion on the flat shelf.

The Monolithic edition corrects the remaining automatic-cycle claim. The laboratory’s incoming-center event needs a positive launch energy for a first return. In the confined harmonic model with positive damping and positive energy per kick, successive return energies approach a positive fixed point. At the fixed point the orbit repeats exactly. Starting at rest produces zero returns and zero kicks. Periodicity of a whole density field and the proposed valve bifurcation each require additional dynamics.

The original findings and numbered source links above refer to the manuscript frozen for the first audit. The editorial correction uses the later public text with SHA-256 `9db10f701efa9d485353f2ce192ade0e4c43d75b9af843781c5a2d9dc7a17a01`. [Beth’s public text](https://tri-sphere-text.abethjones.workers.dev/) · [Corrected edition](source/blueprint-corrected.txt) · [Exact text changes](source/equation-10.patch)

## Energy accounting

Write the smooth fixed-valve equation as

```text
r′ = v                    v′ = −V′(r) − γv + D(r,k)
W′(r) = D(r,k)            U(r) = V(r) − W(r)
E(t) = v(t)²/2 + U(r(t))  E′(t) = −γv(t)²
```

The assumptions matter. Take γ > 0, hold k fixed and require the indicated derivatives along a classical trajectory. A continuous position-only drive on an interval has a primitive. If r and v repeat after the same positive period, E repeats as well. E is nonincreasing; a periodic nonincreasing real-valued function is constant. Its derivative vanishes, so v is zero at every time. In Lean, `drive_primitive` constructs the effective-potential derivative; `energy_rate`, `periodic_level` and `fixed_drive_periodic_velocity_zero` complete the argument. The final theorem quantifies over real functions. It has no positivity assumption on the potential and no fitted drive coefficient.

Equation 8 writes periodicity for Φ(ρ,t). If Φ denotes a density or another Eulerian field, its periodicity is a different proposition from the return of an individual streamline. The attachment supplies no evolution law for Φ, flux, or source term. The theorem addresses the text’s stronger trajectory reading of equation 10.

This adjudicates the fixed-position reading of lines 233–250. Lines 219–232 already allow external intent; a valve schedule k(t), a direction-sensitive force or an incoming-center reset changes the mathematical problem. The text’s correction at lines 1576–1582 is consistent with the calculation. A time-dependent input alone gives no general guarantee of entrainment, uniqueness, global attraction, or a return from every initial state. These require a specified drive and basin.

### A working repair with a measurable cost

The laboratory’s diagnostic oscillator follows r″+γr′+r=0 on its outward-and-inward excursion. It starts at r=0 with strictly positive outward speed. At each incoming return, redirect the velocity outward and add J to the kinetic energy. The parameters are dimensionless, with unit mass and unit spring constant. For 0≤γ<2,

```text
ω = √(1−γ²/4)              Tᵣ = π/ω
r(t) = v₀ exp(−γt/2) sin(ωt)/ω
q = exp(−γTᵣ)              Eₙ₊₁ = qEₙ + J
E* = J/(1−q)               Eₙ−E* = qⁿ(E₀−E*)
```

Tᵣ is the time between center returns, with an instantaneous event. The formula applies while the excursion stays inside the outer radius; crossing the wall requires another law. Lean proves the fixed point, exact n-step deviation and convergence for the affine map under its stated hypotheses. The continuous flight-to-map derivation above is analytic, with a second implementation checking the first return. In the browser, set γ=0.35, J=1.2 and compare three positive initial energies. All converge toward **1.78393147**. Removing the pump makes energy decay to zero. At precisely zero initial energy there is no incoming event to trigger the pump.

| Sweep outcome | Cases out of 80 | Interpretation |
|---|---:|---|
| Positive fixed point | 36 | Positive damping, kick and initial energy |
| Decay to zero | 12 | Positive damping, kick removed |
| Rest without a trigger | 20 | E₀=0; no spontaneous launch rule |
| Neutral continuum | 3 | No damping or kick; initial energies persist |
| Growth to wall exit | 9 | No damping with positive kicks; each return raises energy |

The 80 cells are an auditor-designed grid. The nine independent-implementation comparisons locate center crossings by RK4 and bisection. Maximum absolute errors were below 6.24×10⁻¹¹ in return time and 1.39×10⁻¹⁰ in incoming energy, against 10⁻⁷ limits. For the separate smooth fixed-position model, halving the step changed the final (r,v) by 4.72×10⁻¹⁰, then 2.95×10⁻¹¹ or less. Solver agreement verifies arithmetic for the shared diagnostic law. All settings and outputs are in [experiments.json](evidence/experiments.json) and [sweep.json](evidence/sweep.json).

### The wall and the shelf

The path r(t)=12+t³ reaches 12 with zero speed at t=0 and passes straight through. This is a counterexample to the **isolated boundary inference** in lines 145–149; it is not offered as a solution of all ten equations. A hard impact can instead have different incoming and outgoing velocities, with no single classical derivative at impact. An invariant boundary under a well-posed first-order velocity field is yet another prescription. Each gives a different experiment.

On a flat shelf with the drive shut off, v(t)=v₀ exp(−γt). Write L for the remaining distance to the wall. With positive damping the maximum possible displacement is v₀/γ. The wall is reached in finite time exactly when v₀>γL. Equality gives asymptotic approach; less leaves the trajectory short. In the lab the shelf is 0.75 units wide. At γ=0.5, entry speeds 1, 0.375 and 0.25 give all three outcomes. A constant nonzero speed is possible in the zero-drag control. The browser records the first sampled exterior point; it does not assign a collision time to that sample.

### Geometry, mapping and counting

* **The Hopf map.** Write z₁=a+ib, z₂=c+id. The unnormalized map has squared norm (a²+b²+c²+d²)². Its image on radius ρ>0 lies on a 2-sphere of radius ρ². The common phase cancels; the fiber topology on a positive shell is the standard Hopf construction. At zero the four coordinates all vanish and there is no linked pair of circles. The visualization projects normalized fibers, and labels the original image radius separately. Linking magnitude one for oriented regular fibers is cited standard topology. A proof of the linking theorem is outside the target Lean module. [Lyons, *An Elementary Introduction to the Hopf Fibration*](https://nilesjohnson.net/hopf-articles/Lyons_Elem-intro-Hopf-fibration.pdf)
* **Endpoint versus path.** An outer-shell map into the singleton CRP sends everything to one point. Infinitely many temporally different inward paths can have that same endpoint. Two explicit profiles disagree at t=1/2 in the Lean theorem. Neither a map into the center nor fiber linking determines a radial flow.
* **Independence of the atlas.** The scalar ODE has no variable for face labels, dimension of a fiber, or the number of sampling sites. Sampling the same continuous function r(t) at five or thirteen levels leaves that ODE unchanged. An atlas must be declared or obtained from a separate law. The arithmetic 12×12 counts ordered pairs if every pairing is admitted.
* **Circle versus interval.** Source lines 927–933 call 0 and 12 opposite phases, while equation 1 treats them as the ends of an interval. One compatible construction takes a phase p modulo 24 and displays ρ=min(p,24−p). Phases 5 and 19 share a radius and have different next steps. Constructing periodicity explicitly cannot independently establish that a dissipative oscillator has a limit cycle.
* **Five versus thirteen.** Under the November 24 convention the bins are {0}, {1,…,5}, {6}, {7,…,11}, {12}. This quotient respects the mirror. It loses the information required for an outward unit step: 1 and 5 have the same bin; 2 and 6 do not. An exact change of units x=r/3 instead changes the force to F(3x,3x′)/3 and retains the continuous state. The numerical equality after rescaling and the discrete non-equivalence are both reproducible. The theorem concerns this selected fine update; other updates may admit a quotient.
* **Shell theorem.** For an ordinary three-dimensional spherically symmetric positive mass, outside the matter the potential is −GM/r and its radial derivative is +GM/r². The phrase “one-over-r gradient” in the correction at lines 570–574 is still imprecise. A Euclidean S³ is embedded in four real coordinates, so applying the ordinary shell theorem there requires a field equation and ambient space. No layer mass profile or force source is derived in the attachment. [Newton’s Shell Theorem](https://mathworld.wolfram.com/NewtonsShellTheorem.html)
* **Solids and views.** Dualization exchanges faces and vertices. Multidimensional labels such as “5D consciousness” in the manuscript are the author’s terms. They supply no additional Euclidean coordinate or observable. A change of camera cannot turn a 20-vertex solid into a 12-vertex solid. [Platonic Solid](https://mathworld.wolfram.com/PlatonicSolid.html)

## Source-wide coverage and interpretation

| Source lines | Content examined | Finding or handling |
|---|---|---|
| 1–108 | Attribution, visual approach, companion documents, outline of the flow | The upload is pinned. The opening interior turn and subsequent wall rule require reconciliation. |
| 109–455 | Ten equations, driven oscillator, storage, observer and fluid interpretation | E1–E10f and A6; analytic witnesses and limits above. |
| 456–588 | November range assignment, external drive, gravity and retraction | A1, S1; the revision history is part of the result. |
| 589–917 | Layer-by-layer roles, standing, two readings of geometry and flow | Descriptive atlas and author-assigned roles. Stable numbered layer and dynamic observer seat are distinct modeling choices. |
| 918–1244 | Phase circle, shape corrections, doubling and viewpoint | A4, A7–A10. Diagnostic phase lift preserves the intended picture while exposing the missing direction bit. |
| 1245–1493 | Light, LCL, social readings, IT-cubed and physics analogies, counts and foam | B1, A8, T1. Similar shapes or names do not supply dynamical maps. No independent novelty or empirical claim follows from the parallel. |
| 1494–1706 | Five-position alternative, biological mapping, duality and Genesis | E10b, A1–A5, A10, B1, T1. Later timed-drive correction and conflicting “found”/“chosen” labels retained. |
| 1707–1976 | Monad, scapegoat, language, cuneiform, Voynich, impedance | T1 and B2. Symbolic readings are attributed. Empirical historical or health propositions would need distinct sources and methods. |
| 1977–2313 | Expanded theology, biological analogies, open labels | T1 and B1. The audit makes no theological, clinical or manuscript-decoding determination. |
| 2314–2380 | CIV brief and final status | The author labels the assembly interpretive and expressly disclaims established physics. The universal regular-fiber wording still includes the singular center. |

This is a section-complete review of the attachment, with proposition-level testing of its mathematical architecture. Side remarks about individual scholars, sacred texts, anatomy and the contemporary state of particle physics are preserved as source material. They have not been independently fact-checked sentence by sentence.

## Zoo provenance, Lean scope and independence

The baseline is [Monolithic-Zoo-Lean4 at b1220036](https://github.com/enuminous/Monolithic-Zoo-Lean4/tree/b12200364f7d1424c4d9cdfbe20fff4d52de379d). Its `Registry.lean` gives 46 main-sequence names. Five extension procedures have separately pinned definitions. The standalone [PEGASUS at 41d57615](https://github.com/enuminous/Pegasus/tree/41d57615f16c43ea8858e35cd1250d44c3c7df97) adds a geometric bridge check. Earlier [BSA-R audit](https://github.com/enuminous/bsa-r/tree/9e463fafd2c22d040f4587889246b93bfef860b5/audits/2026-11-17-monolithic-zoo) names HUMMINGBIRD; its contract remains unlocated. The [previous Physlib roster accounting](https://github.com/enuminous/papers/blob/2f7e645fc157e9a0560ef42c0e94f70371b17d38/Physlib-Maxwell-Full-Zoo-Audit-2026-11-16.md) records the same limitation. Thus 53 names are accounted for without assigning a global roster number to PEGASUS.

The exact Zoo replay compiled its selected kernels, passed all 90 upstream fixture comparisons, tested four axiom-rejection controls, and reconstructed the 643 decision certificates, 1,432 structured-report certificates and 2,100 exact threshold certificates. These are checks of the shared software. The 17 rank-aggregation modules require upstream features and a comparison population. The manuscript has neither. Generating a score from arbitrary manuscript paragraphs would introduce an unvalidated adapter. [Zoo build log](evidence/zoo-build.log)

The target module contains **25 named theorems**. The audit enumerated all 56 safe declarations, including 43 theorem declarations when generated lemmas are counted. The transitive allowlist is `propext`, `Classical.choice` and `Quot.sound`. The report shows the actual axioms of every named theorem. A false mirror statement, fabricated axiom and placeholder were rejected; logs include the reason. Two auxiliary target-adapter theorems are in a separate file. The finite return map and the real energy obstruction have different hypotheses. No statement in this build formalizes human intent as a measured force, the full physical assembly, all topology, or theology. [Proof source](TriSphere.lean) · [Axiom report](evidence/lean-axioms.log) · [Negative controls](evidence/negative-controls.log)

The observed dependences agree with known damped-oscillator theory and standard Hopf geometry. The [November 19 TriSphere technical companion](https://github.com/enuminous/papers/blob/2f7e645fc157e9a0560ef42c0e94f70371b17d38/TriSphere-Tokamak-Model-Comparison-2026-11-19.md) already distinguished a harmonic center-kick model from the proposed physical extension. The present contribution is a source-specific formal obstruction, an explicit repair and its reproducible tests. No discovery-priority or cosmological validation claim was tested. For conventional damping and time-dependent forcing see [OpenStax, Damped Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-5-damped-oscillations) and [Forced Oscillations](https://openstax.org/books/university-physics-volume-1/pages/15-6-forced-oscillations).

## Smallest discriminating physical test

Define one accessible oscillator and record position, velocity and the externally supplied work. State which variable in that device represents the valve, how the boundary acts and which state triggers a return. Calibrate friction with the input disabled. Before seeing the test run, freeze the tolerances for energy closure and the window of initial energies. Compare a fixed-position actuator to an equal-budget event-timed actuator in randomly ordered runs. Have a second operator hold the settings and raw traces.

The predicted discriminator is the signed work per completed return. Under the fixed-position model its closed-path integral is zero. Under the timed-kick model it must balance dissipation at a positive steady return energy. A persistent positive cycle without accounted external work rejects the specified energy accounting or its measurement model. Convergence confined to the timed actuator supports that actuator mechanism in the tested device. Extrapolation to the cosmological or biological interpretation would still require a separate bridge. This physical experiment was not run.
