# Execution record

The auditor ran the commands below in an isolated Linux x86-64 workspace on 24 November 2026. The attachment is a manuscript, with no producer build entry point or raw physical data. The Lean target, finite controls, browser models and target adapters in this release were written by the auditor. The shared Zoo source is the pinned producer baseline. All numerical parameter choices in the lab are diagnostic assumptions.

| Working directory | Command or entry point | Evidence |
|---|---|---|
| root | `python3 scripts/prepare_lean.py` then `lake build TriSphere` | lean-build.log, anchored by lean-toolchain, lake-manifest.json and vendor/lean-pins.json |
| root | `lake env lean -DwarningAsError=true Audit.lean` | lean-axioms.log, 25 named source theorems and module-wide transitive axiom audit |
| root | `python3 scripts/proof_controls.py` | negative-controls.log, three rejected controls |
| vendor/zoo | Each command in `../../replay_zoo.py`, beginning with `python3 verify.py` | zoo-build.log, commands, exit codes, retained native warnings, fixtures and build output |
| vendor/zoo | `lake env lean -DwarningAsError=true ../../ZooTarget.lean` | zoo-target-lean.log, native CAT, TURTLE and WEASEL target outputs |
| root | `python3 scripts/target_gates.py evidence` | target-gates.json and pegasus.json, input fields, native results and pins |
| root | `node scripts/experiments.js evidence/experiments.json` | 16 named controls and observations |
| root | `python3 scripts/return_sweep.py evidence/sweep.json` | Separate RK4 event integrator, 9 comparisons, 80 deterministic return-map cells |
| root | `python3 scripts/build_lab.py`; `python3 scripts/check_lab.py` | browser.log, local file and HTTP subpath, narrow/desktop widths, interactive exports |
| root | `python3 replay.py --browser` | Reproduces the above and records each command, exit code, and regenerated evidence in replay-output/ |

**Environment.** Linux 6.18.57 x86_64; Python 3.12.14; Node 24.22.3; Lean 4.19.0, compiler commit 6caaee842e94; Lake 5.0.0-6caaee8; Chromium Headless Shell 151.0.7922.34. The downloaded official Lean Linux archive had SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. Standard-library Python runs the audit; Python Playwright is required only for browser testing. Neither random seeds nor a model-training stage enter these deterministic comparisons.

**Software provenance.** Zoo source archive at b12200364f7d1424c4d9cdfbe20fff4d52de379d. PEGASUS executable Python modules at 41d57615f16c43ea8858e35cd1250d44c3c7df97. Mathlib v4.19.0 at c44e0c8ee63ca166450922a373c7409c5d26b00b and eight locked dependencies. The upstream mathlib cache supplied compiled dependencies. Prebuilt ProofWidgets assets accompany the source snapshot for the corresponding release. Native cache extraction uses leantar v0.1.15; upstream revision c9266d97703277b680be72bc77226c2b62d1d38d. See vendor/leantar/LICENSE and SHA256SUMS. The browser lab has no network dependencies.

**Iteration history.** The first target build exposed tactic/elaboration and lint errors. A second pass isolated an unnecessary tactic; a later limit proof required a small tactic cleanup. The final target was rebuilt and checked with its actual declarations. The first system Chromium failed at startup under the local socket restrictions. Chrome Headless Shell passed the file scenario; separate processes per viewport then passed both launch modes. These are development failures and repairs to auditor-created code. None changes a source-claim FAIL to PASS. The upstream Zoo compiled with a retained warning for an unused Moth argument; its axiom audit and reference regressions completed successfully.

**Limits.** The lab plots sampled trajectories and explicitly signals a detected exit. The event-sampled curve is a visual aid; diagnostic return and threshold decisions use the documented rules. A source-only cold rebuild of all Mathlib dependencies, other operating systems, remote GitHub workflow execution, independent replication and physical validation are separate from the observed local replay. The downloadable release includes no live service, API key or external measurement.

A clean extraction of the pre-release ZIP completed every stage of `python3 replay.py --browser`. Its top-level results are retained in [pre-release-replay.log](pre-release-replay.log). The final editing pass expanded the source-range viewer and embedded the full audit analysis in the offline laboratory. The browser checks include reading and exporting that analysis.
