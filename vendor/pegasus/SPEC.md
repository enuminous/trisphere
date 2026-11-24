# PEGASUS animal contract v0.1.0

**Provenance-Enforced Geometric–Algebraic Synthesis Under Scrutiny**

Introduced November 11, 2026 for Monolithic LLC / Matthew Chenoweth Wright.
Implementation and documentation prepared with AI assistance at Matthew's request.
No independent review has yet been recorded.

## 1. Fixed operation

**Purpose:** audit whether a proposed mathematical hybrid has defined components,
explicit interfaces, checked invariants, and evidence adequate for its conclusions.

**Inputs:** frozen source bytes; a versioned claim manifest; required root claims;
typed mathematical data; declared dependencies; definitions and bridge obligations.

**Transformation:** validate the manifest; reject circular dependencies; run the
closed registry of exact checks; propagate failed and unresolved premises; emit
per-claim evidence and a root verdict without averaging.

**Outputs:** a reproducible JSON ledger with exact witnesses or counterexamples,
PASS/FAIL/UNRESOLVED verdicts, evidence status, input and checker hashes, and scope.

**PASS:** the specified checker establishes its bounded proposition and every
declared prerequisite passes. **FAIL:** a checked proposition is contradicted,
a required premise fails, or a circular support structure is found.
**UNRESOLVED:** a required definition, checker, witness, or computation is missing.
Malformed inputs are rejected as input errors, not mathematical refutations.

For a claim c with local result L(c) and declared dependencies D(c):

\[
V(c)=\begin{cases}
\mathrm{FAIL},&c\text{ is circular, or }\mathrm{FAIL}\in\{L(c),V(d):d\in D(c)\},\\
\mathrm{UNRESOLVED},&\mathrm{UNRESOLVED}\in\{L(c),V(d):d\in D(c)\},\\
\mathrm{PASS},&\text{otherwise}.
\end{cases}
\]

This is an evidence decision rule, not a probability or a physical law.
An empty required-claim set is invalid. Diagnostic claims remain visible without
silently becoming premises of a different target.

## 2. Seven audit stations

These station names are a mnemonic for the operational scope, not seven separate animals.

| Station | Input / operation | Output / criterion | v0.1 implementation |
|---|---|---|---|
| Provenance | Record exact source and input bytes | Hash match; source limitations retained | Freeze manifest and report hashes |
| Evidence | Distinguish checked result from assertion | No caller-provided PASS accepted | Closed check registry; obligation notes cannot certify themselves |
| Geometry | Check polynomial and count interpretations | Exact identity or counterexample | Rational polynomial arithmetic and finite integrality checks |
| Algebra | Specify and test concrete algebraic objects | Closure/inverses or missing construction | Bounded permutation-group enumeration; necessary order divisibility |
| Symmetry | Separate a symmetry from a picture or label | Explicit transformations preserve specified structure | Cube and Fano incidence enumerations |
| Uncertainty | Preserve budgets, missing maps, and scope | Unknown stays UNRESOLVED | Explicit unresolved operation and dependency propagation |
| Synthesis | Follow the declared bridge graph to roots | Every required premise supported | DAG evaluation and cycle rejection; general bridge verification remains manual |

## 3. Mathematical reading of the supplied image

The source uses speculative labels such as “L39 Plenum,” “Logos blocks,” “cubic
anyons,” and “mixed Monster numbers.” These are preserved as source terminology;
they are not silently substituted for established mathematical definitions.

### 3.1 Volume: exact identity, interpretation still open

The source specifies

\[
C_{3\mathrm{LDT}}(n)=\frac{40}{39}(8n^3+12n^2+6n)
=\frac{40}{39}\big((2n+1)^3-1\big).
\]

The equality follows by the binomial theorem: `(2n+1)^3` has coefficients
`1, 6, 12, 8` in ascending powers of n; subtracting one removes the constant.
The checker independently expands the affine cube and compares rational coefficients.
This identity is demonstrated; it does not derive the prefactor.

On the explicitly stated trial domain `n ∈ {1,...,39}`, the literal count
interpretation fails already at `n=1`:

\[
C_{3\mathrm{LDT}}(1)=\frac{40}{39}\,26=\frac{80}{3}.
\]

A finite union of whole, non-overlapping unit cubes has integer volume. A rational
effective measure, weighting, overlap correction, or a restricted n-domain could
still be defined, but would be a new explicit contract. This diagnostic does not
refute those unspecified alternatives. If side length is restored to `a`, ordinary
volume units would require an `a³` factor; counting and measure must be distinguished.

`40/39 = 1 + 1/39` is an upward scaling relative to the undressed expression.
The phrase “topological tax” does not establish its sign, geometric origin, or
physical value. Those remain postulates until a derivation or independent fit test exists.

### 3.2 Rotation, orientability, and statistics are separate obligations

For the ordinary cube centered at zero, proper rotational symmetries are signed
permutation matrices with determinant +1. Enumerating them gives 24. In particular,
`(x,y,z) -> (-y,x,z)` and `(x,y,z) -> (-x,-y,z)` preserve the vertex set and
have determinant +1. An asymmetric decoration may change appearance under a
rotation without making the underlying object non-orientable.

The source invokes a special “discrete junction sense”; no cell complex or gluing
maps accompany the image. Its orientability claim therefore remains UNRESOLVED.
A glued complex may be non-orientable even though its constituent cells are
orientable; PEGASUS does not rule out such a separately defined construction.

Likewise, orientation-dependent appearance does not establish anyonic exchange.
A mathematical anyon proposal needs an exchange/configuration model, state space,
and compatible braid operators. A physical claim additionally needs dynamics and
observables. Checking a braid relation alone would still not establish a physical
realization. The current version does not implement an anyon witness checker.

### 3.3 Algebraic names need explicit objects and maps

The Fano plane can be represented by the seven nonzero vectors of `F₂³`, with
lines `{a,b,a XOR b}`. Exhaustive permutation enumeration gives 168 incidence
automorphisms. ATLAS gives `|M11|=7920`; these full groups are not interchangeable.
The slash in the image is ambiguous and is **not** automatically interpreted as
a claim that they are equal. A selected common action still needs specification.

The reference Leech lattice has rank 24. A 24-component vector, a projection, or
a wing-shaped picture is not by itself a Leech lattice certificate or a coupling.
An actual construction needs lattice data and structure-preserving maps.

The complete reference Monster order is

\[
2^{46}3^{20}5^9 7^6 11^2 13^3\cdot17\cdot19\cdot23\cdot29\cdot31\cdot41\cdot47\cdot59\cdot71.
\]

The image's order expression is clipped after the visible factors. The full
reference factorization is a separately sourced reference, not a repaired quote.
Order divisibility is a necessary arithmetic filter for a finite subquotient;
it supplies no subgroup, normal subgroup, quotient, embedding, or action.
“Mixing numbers” must be replaced by a stated operation before group claims can pass.

## 4. Positive control: PEGASUS-T0

Let B be the eight vertices `(±1,±1,±1)`, used as labels; rescaling by 1/2 gives
a unit-side cube without changing the permutations. Add labels `L,R` for wings.
Let r rotate B by `(x,y,z)->(-y,x,z)` and fix L,R. Let w fix B and exchange L,R.

They satisfy `r⁴=e`, `w²=e`, and `rw=wr`. The action is faithful and has precisely
eight elements `r^i w^j`, `0≤i<4`, `0≤j<2`; distinct exponents give distinct
actions on the disjoint supports. It realizes `C4 × C2`.

The executable control supplies the two actual permutations and enumerates closure,
inverse witnesses, order, and commutativity. This is a standard direct-product
construction, not a new group, a connected body-wing mechanism, an emergent
coupling, an anyon, or a Monster/Leech specimen. It validates the finite-action
path of the auditor without being used as evidence for the source's root H1.

## 5. Anti-circularity and independence

- Freeze source, definitions, checks, required roots, and budgets before reporting.
- Keep source claims, diagnostic interpretations, and synthetic controls labeled.
- Never treat common prime factors or a fitted constant as proof of a structural map.
- Reject declared dependency cycles; disclose that undeclared dependencies need review.
- Do not replace unresolved evidence with prose assertions, supplied PASS labels, or averages.
- A source hash verifies bytes, not authorship, truth, prior publication, or independence.
- Development-case success and synthetic controls are not external validation.
- Changing the source domain or meaning requires a new version; preserve the prior result.

The included freeze is a local development freeze made before generating the first
saved reports. It is not a prospectively sealed experiment. No empirical test,
external custody, Lean kernel check, or independent replication has occurred.

## 6. Novelty and relation to the Zoo

| Element | Classification |
|---|---|
| Binomial expansion and rational arithmetic | Identical to standard mathematics |
| Cube rotations and Fano incidence automorphisms | Standard finite symmetry computations |
| Permutation group closure and `C4 × C2` | Standard algebraic constructions |
| Order divisibility filter | Standard necessary condition |
| Dependency propagation and cycle rejection | Adjacent to established proof-obligation and provenance workflows |
| PEGASUS name and this audit packaging | New project contribution here; global priority not established |
| Source's mixed lattice/anyon/sporadic construction | Hypothesis with unresolved definitions; novelty unassessable |

PEGASUS focuses on **interfaces between proposed mathematical structures**.
It complements existing Zoo work on provenance, circularity, robustness, and
prospective evaluation without claiming to replace those operations. This repo
registers a standalone extension and does not alter another repository's roster.

## 7. Minimal next test, fixed before a new run

Submit one concrete coupling: object sets or spaces; generators or maps;
preserved structure; all domains; and a finite witness or replayable proof.
State whether the claimed result is only an action, a lattice construction,
a subquotient, or a physical prediction. Select the root and checker before scoring.

**PASS:** the chosen witness checker verifies the stated maps and every required
premise within its declared scope. **FAIL:** a preserved relation or required
premise has a checked counterexample. **UNRESOLVED:** witness, checker, or resource
budget is insufficient. For a new coupled model, include a disconnected or
uncoupled control; passing T0 alone is not success on the coupling claim.

Any claim of empirical benefit additionally requires a frozen comparator,
observable, thresholds, custody, and independent replication protocol. Those
are open obligations, not claimed features of this release.
