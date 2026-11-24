# Claim register

32 findings on the pinned blueprint. Source lines refer to source/blueprint.md.

## E1 · Thirteen indexed positions

**PASS** · Definition · lines 116–128

Fin 13 gives precisely 0 through 12. The integer labels sample a continuous radius. The count is stipulated.

Evidence — TriSphere.lean · Layer; evidence/experiments.json · atlas

Scope or next test — A derivation of the count needs an independent selection rule.

## E2 · Positive-radius shells and their center

**PASS** · Geometry · lines 130–136

For positive radius the level set is a scaled unit 3-sphere in four real coordinates. At zero all four coordinates vanish.

Evidence — TriSphere.shell_zero; Lyons, An Elementary Introduction to the Hopf Fibration

Scope or next test — Distinguish the degenerate level set in every universal statement.

## E3a · Hopf map on positive shells

**PASS** · Geometry · lines 138–143

The output has length ρ². Divide by ρ² for a unit-sphere target. Common complex phase preserves the output. Linking magnitude one for distinct fibers with consistent orientations is an established topological result.

Evidence — TriSphere.hopf_norm, hopf_phase, radius_two_control; Lyons pp. 8–14

Scope or next test — The Lean results cover the polynomial and symmetry identities; linking uses the cited topology.

## E3b · Every layer has linked circular fibers

**FAIL** · Counterexample · lines 138–143; 2325–2331

At ρ=0 the domain is a singleton. Two distinct circular fibers cannot exist there.

Evidence — TriSphere.shell_zero; evidence/experiments.json · hopf-scaling

Scope or next test — Restrict the fibration to ρ>0; supply radial transport independent of the fiber chart.

## E4 · A zero radial speed implies a reflecting wall

**FAIL** · Counterexample · lines 145–149; 246–255

ρ(t)=12+t³ crosses 12 with zero velocity there. This tests a pointwise condition. A reflecting impact with incoming speed generally jumps velocity; a smooth turn has different conditions.

Evidence — TriSphere.stationary_crossing

Scope or next test — Specify a phase-space boundary law, uniqueness assumptions, and energy exchange.

## E5a · The stated return map has the given endpoint

**PASS** · Definition · lines 151–155

There is exactly one function into a singleton, so the endpoint requirement carries no trajectory information.

Evidence — Source lines 151–155; AUDIT.md · endpoint versus path

Scope or next test — Specify a time-parametrized family of paths or a transition law.

## E5b · The return map specifies a definite path

**FAIL** · Counterexample · lines 151–155

12(1−t) and 12(1−t)² share start and end at t=0,1, but at t=1/2 they give 6 and 3. The endpoint map cannot select between them.

Evidence — TriSphere.a_destination_does_not_fix_a_path

Scope or next test — Supply dynamics that select a return path and duration.

## E6 · The mirror is an involution with one fixed layer

**PASS** · Formal theorem · lines 157–161

All 13 indices map back after two reflections. Only layer 6 maps to itself.

Evidence — TriSphere.mirror_involution, midpoint_unique

Scope or next test — Complete on the declared finite domain.

## E7 · A human-controlled Product/Compost filter

**UNRESOLVED** · Candidate mechanism · lines 163–184; 219–225

A typed choice and a conservative split are possible. A position-dependent or observer-dependent valve and its physical coupling are unspecified. The lab exposes the two routing choices as assumptions.

Evidence — TriSphere.filter_conservation; lab/engine.js; lines 163–177

Scope or next test — Provide valve inputs, timing, destination weights, units and a measured output.

## E8 · Periodic motion as a stated condition

**PASS** · Definition · lines 186–191

The displayed equality is a definition of T-periodicity for positive T. Constant trajectories satisfy it. A nontrivial cycle needs a nonconstant state and a return law.

Evidence — TriSphere.periodic_level; lines 186–191

Scope or next test — Require nonzero velocity somewhere and simultaneous position/velocity closure.

## E9 · Twelve ordered face choices each way

**PASS** · Arithmetic · lines 193–197

Allowing all 12 inward and all 12 outward face labels yields 144 ordered pairs. No geometry fixes a physical pairing or reflection probability.

Evidence — TriSphere.face_pairs; Wolfram MathWorld, Regular Dodecahedron

Scope or next test — Supply a transition relation to count actual reachable pairs.

## E10a · Steady position drive automatically sustains a nonconstant loop

**FAIL** · Formal obstruction · lines 199–250; 426–446; 1576–1582

For a fixed valve, a single-valued drive with a primitive and positive damping, effective energy falls at rate −γv². A periodic smooth state must have v=0 at every time. The later timed-drive correction survives.

Evidence — TriSphere.drive_primitive, energy_rate, fixed_drive_periodic_velocity_zero

Scope or next test — State an external phase, hysteresis, or an event law, then derive its return map.

## E10b · A timed kick can maintain a repeating excursion

**PASS** · Constructive control · lines 239–245; 1576–1582

For the auditor’s harmonic half-oscillator, positive post-impact E obeys E_next=qE+J. For 0≤q<1 deviations shrink as qⁿ. Positive J gives a positive fixed point. The theorem concerns the declared return map.

Evidence — TriSphere.kick_fixed, kick_iterate, kick_converges; evidence/experiments.json · return-map

Scope or next test — For the blueprint, identify a measured kick law and its work per return.

## E10c · Frictional flat-band flight keeps constant speed

**FAIL** · Formal obstruction · lines 250–255; 285–295

Where both potential slope and drive vanish, v′=−γv. Nonzero speed decays when γ>0. There is a sharp entry-speed threshold even in a perfectly flat band.

Evidence — TriSphere.coast_accel_ne_zero; evidence/experiments.json · wall-threshold

Scope or next test — Specify entry speed, plateau width, damping and wall law.

## E10d · Layer-11 turn and wall turn describe one event

**UNRESOLVED** · Source revisions · lines 74–86; 250–255; 285–308; 691–708

An interior reversal, a finite-time wall impact, and an asymptotic approach have different traces. The text uses all three descriptions.

Evidence — Source lines 74–86, 246–255, 285–308, 691–708

Scope or next test — Choose a boundary rule and a measurable event definition.

## E10e · One oscillator derives the other geometric structures

**FAIL** · Countermodel · lines 487–501

The same scalar trajectory can be attached to any number of sampling layers. Its ODE has no fiber variables, face labels or intent classifier. Changing the number of sample positions leaves the smooth law intact.

Evidence — AUDIT.md · independence of the atlas; evidence/experiments.json · coordinate-rescaling

Scope or next test — Add a noncircular rule deriving the discrete atlas and its coupling.

## E10f · Capture, storage and bifurcation at a valve threshold

**UNRESOLVED** · Hypothesis · lines 309–344; 426–446

A flat shelf alone supplies no restoring force toward a unique storage point. With a fixed localized drive, an initially resting plateau point can remain there at nonzero k. No bifurcation parameter or return-memory dynamics is specified uniquely.

Evidence — evidence/experiments.json · plateau-equilibrium

Scope or next test — Freeze force, valve policy, impact and storage rules; test perturbed initial states.

## S1 · Newtonian shell theorem yields a flat exterior

**FAIL** · Superseded claim · lines 552–576

For nonzero enclosed mass in ordinary 3D inverse-square gravity, exterior V=−GM/r and V′=GM/r². The later correction retracts flatness; its description of the gradient as 1/r still confuses potential with gradient. A shell S³ in four coordinates needs its own force law.

Evidence — MathWorld, Newton’s Shell Theorem; AUDIT.md · shell theorem

Scope or next test — Choose ambient dimension, density and field equation before deriving V.

## A1 · Dated Time / Space / Phase assignment

**PASS** · Interpretive specification · lines 450–466; 1632–1640; 2292–2303

The November 24 range assigns boundaries 0 and 12, Time 1–5, Space 6, Phase 7–11. Opposite bins pair under the mirror. The older open orientation entry remains visible.

Evidence — TriSphere.coarse_mirror, coarse_surjective; source lines 450–466

Scope or next test — Use as an atlas convention unless an independent experiment establishes a physical mapping.

## A2 · The coarse atlas inherits an exact one-step dynamics

**FAIL** · Counterexample to unconditional inheritance · lines 1495–1511; 1564–1608

Fine layers 1 and 5 both lie in Time. One outward index step sends them to 2 and 6, in different bins. A memoryless step on the five bins cannot reproduce this particular map. Other evolutions might descend.

Evidence — TriSphere.no_coarse_step; evidence/experiments.json · coarse-counterexample

Scope or next test — Prove coarse∘fineStep = coarseStep∘coarse for the actual dynamics or retain hidden state.

## A3 · Five physical positions are fixed by the five Platonic solids

**UNRESOLVED** · Unproved bridge · lines 1592–1608; 1641–1651

Counting the regular convex Platonic solids gives five; the text alternates between choosing and finding a position count. No map establishing necessity is supplied.

Evidence — MathWorld, Platonic Solid; source lines 1592–1608, 1641–1651

Scope or next test — Specify a bijection and prove why the dynamical states exhaust precisely its five members.

## A4 · Dodecahedron / icosahedron duality and mirror pairing

**PASS** · Known geometry · lines 1663–1688

The dodecahedron and icosahedron exchange vertices and faces under duality and both have 30 edges. The layer labels 5 and 7 pair arithmetically. These are two independently defined relations.

Evidence — MathWorld, Platonic Solid; TriSphere.mirror_involution

Scope or next test — Show an actual transformation for a claim that changing viewpoint alone changes a solid into its dual.

## A5 · Thirteen layers plus five positions give seventeen distinct objects

**UNRESOLVED** · Cardinality assumption · lines 505–519; 1652–1662

13+5−1=17 assumes two sets with precisely one common element. If the five are bins of the same atlas, that intersection has not been defined.

Evidence — Source lines 505–519; AUDIT.md · atlas and quotient

Scope or next test — Give the two sets, their types and an embedding before counting a union.

## A6 · Fluid, seams and observer standing determine radial flux

**UNRESOLVED** · Model closure · lines 262–284; 341–429; 505–538

A streamline ODE alone does not specify a transported density, flux, storage or valve law. A fixed Filter index and a moving decision point need separate state variables.

Evidence — Source lines 262–284 and 505–519

Scope or next test — Give a continuity equation, flux, boundary and reservoir budgets, and observables.

## B1 · Biological, optics and tokamak parallels validate the assembly

**UNRESOLVED** · Empirical bridge · lines 1245–1399; 1610–1640; 2122–2148

The source itself distinguishes analogies and observations. No observation model, independent dataset, measurable intervention or competing model for this assembly accompanies the upload.

Evidence — Source sections; prior technical companion cited in AUDIT.md

Scope or next test — Choose one observable and test a frozen differential prediction on held-out data.

## B2 · Language and manuscript readings as testable physical mechanisms

**UNRESOLVED** · Historical/empirical hypothesis · lines 1816–1975

The source labels these mappings interpretive. Symbolic correspondences and assigned impedance numbers provide no calibrated sensor, independently decoded corpus or held-out prediction here.

Evidence — Source lines 1880–1920, 1960–1975

Scope or next test — For a historical decoding claim, freeze a codebook and blind-score unseen pages.

## T1 · Theological, social and personal readings

**NOT_APPLICABLE** · Author interpretation · lines 16–25; 1707–1815; 1977–2291

The Monad, Source, ego and theological readings express Beth’s interpretation. A physical proof criterion has no target in an explicitly symbolic reading. Adjacent empirical claims remain separately open.

Evidence — Source lines 11–25, 1707–1749, 2305–2310

Scope or next test — Preserve author attribution and source wording.

## B3 · The combined structure describes the physical universe

**UNRESOLVED** · Empirical scope · lines 2356–2377

The author expressly withholds this claim. The audit assesses empirical standing as an obligation for any future physical reading. Formal identities, cross-domain similarities and simulations use shared assumptions.

Evidence — Source lines 2356–2377; evidence/pegasus.json

Scope or next test — A distinct, falsifiable observable with a sealed comparison and independent measurements.

## A7 · Circular phase and interval radius

**PASS** · Constructive interpretation · lines 29–37; 927–933

A directed phase on 24 ticks can project onto 13 radii by taking the smaller distance from phase zero. Phases 5 and 19 share radius 5 but have different next radii. This reconciles the two coordinate pictures only after adding direction.

Evidence — TriSphere.phase_period, phase_orientation_loss; five-versus-thirteen lab

Scope or next test — Derive the phase and period from a physical dynamics before assigning them empirical meaning.

## A8 · Doubling, additive patterns and standing generate geometric states

**UNRESOLVED** · Interpretive construction · lines 1065–1190; 1401–1493

The text gives examples of doubling and sums such as 3+5=8 and 5+7=12, then assigns the results to faces, layers or perspectives. It supplies no single-valued generation rule for unseen shapes or a criterion for choosing which count to compare.

Evidence — Source lines 1116–1137 and 1401–1454

Scope or next test — Freeze the objects and a typed update rule; withhold at least one predicted count.

## A9 · A change in viewpoint makes geometric duals identical

**FAIL** · Literal geometric reading · lines 1177–1190; 1663–1688

A rotation or change of coordinates preserves vertex count. The dodecahedron has 20 vertices and its dual has 12. Dualization can construct the second object; viewpoint alone cannot give a rigid equivalence. The figurative standing interpretation remains attributed.

Evidence — MathWorld, Platonic Solid; source lines 1663–1688

Scope or next test — Use an explicit face-to-vertex dualization map wherever a geometric transformation is intended.

## A10 · Two atlas descriptions identify the same avatar seat

**UNRESOLVED** · Cross-section vocabulary · lines 179–184; 1555–1575; 1652–1662

One passage puts the human at the Filter. The alternate calls layer 4 the seat and layer 6 supporting structure, while its own coarse midpoint also acts as avatar/Filter. A static seat, routing interface and observer-dependent role need separate types.

Evidence — Source lines 1555–1575; the November 24 range assignment is recorded separately in A1.

Scope or next test — Specify maps from observer seat to fine layer, coarse membrane and decision locus.
