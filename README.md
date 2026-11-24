# Tri-Sphere Laboratory

[Open the interactive laboratory](https://enuminous.github.io/trisphere/) · [Simulation report](simulation/README.md) · [Simulation plot](simulation/files/TriSphere_Simulation.png) · [Download simulation data and replay code](simulation/TriSphere_Simulation_Run.zip)

The timed-kick simulation at γ = 0.35 and J = 1.2 attained a steady peak radius of 1.474. A second run initialized on its steady orbit grazed layer 12 at J ≈ 79.522 in the same dimensionless harmonic model. [Layer passage times](simulation/results/layer_passages.csv)

Open **[index.html](index.html)** after extraction. The complete browser lab works from one file, offline, with no installation. It includes the 13-layer atlas and Hopf-fiber viewer, filter dials, four oscillator experiments, a five-versus-thirteen comparison, an 80-case parameter sweep, the claim and Zoo ledgers, the manuscript text and the checked Lean proof register. Use the controls to export the run trace, filtered ledger, sweep or Lean source.

**[Read the audit](AUDIT.md)** · [32 claim findings](CLAIMS.md) · [53 named Zoo operations](ROSTER.md) · [Target Lean source](TriSphere.lean) · [Raw evidence](evidence/)

The fixed-position drive in the smooth, positively damped equation cannot sustain a nonconstant periodic state. The later event-timed interpretation admits a diagnostic oscillator with a positive stable return energy. All quantities in that example are dimensionless. The mathematical example supplies no measured physical coupling for the broader architecture.

## Reproduce the audit

Use a fresh extraction for a clean build. The proof replay requires the official **Lean 4.19.0** toolchain (Lean and Lake on PATH), Python 3.10+ and Node 18+. Mathlib, its source dependencies, the Zoo package and the relevant Mathlib build cache are bundled. The repository stores the larger dependency archives in smaller ZIP files. Their extracted entries match the original audit distribution byte for byte. The Lean compiler itself is a prerequisite. The recorded run used Linux x86-64. Other platforms have not been replayed. Allow several GB of free space when unpacking the proof dependencies.

From the directory containing this file:

```sh
python3 replay.py --integrity-only
python3 replay.py
```

The integrity-only command needs just Python. Full replay verifies the release file hashes, builds the target, audits axiom dependencies, checks rejection controls, runs the original Zoo suite, runs the target adapters and regenerates the numerical experiments. Each command's status and output are written under `replay-output/`. A fresh extraction compiles the target and the Zoo from source and reuses the shipped Mathlib dependency cache. To repeat the browser interactions, install Python Playwright and Chromium and run `python3 replay.py --browser`. Set `CHROMIUM_EXECUTABLE` if using a separate Chromium or Chrome Headless Shell binary.

To work directly with the Lean target:

```sh
python3 scripts/prepare_lean.py
lake build TriSphere
lake env lean -DwarningAsError=true Audit.lean
```

Use `python3 scripts/prepare_lean.py --source-only` on a fresh extraction to omit the prebuilt Mathlib cache. A full dependency rebuild is a slower route. Dependency revisions are in [lean-pins.json](vendor/lean-pins.json). The distribution includes cache-extraction utilities for the platforms listed in `vendor/leantar/`; the verified platform is Linux x86-64. For work on the front end, edit `lab/page.html`, `lab/app.js` and `lab/engine.js`, then run `python3 scripts/build_lab.py`. The authoritative mathematical and audit outputs are inputs to the generated page.

## GitHub flat-stack deployment

The live site is served from the root of the `gh-pages` branch. That branch contains the standalone `index.html` and `.nojekyll`. The complete audit and simulation sources live on `main`. For branch publication, copy the verified HTML to `gh-pages` after changing the lab. [Open the deployed laboratory](https://enuminous.github.io/trisphere/)

The included workflow replays the Lean build and audit on pushes and pull requests. After the first successful push to `main`, it packages the tracked repository files into a flat downloadable ZIP and creates the versioned first release. Subsequent pushes preserve that edition. [GitHub releases](https://github.com/enuminous/trisphere/releases)

For continuous deployment from `main`, select **GitHub Actions** under **Settings → Pages → Build and deployment** and set the Actions repository variable `TRISPHERE_ACTIONS_PAGES` to `true`. The workflow then deploys the standalone page after successful verification. For offline use, extract the ZIP and open `index.html`. Preserve the dotfiles if copying the full project into another repository. [GitHub Pages publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Evidence and attribution

The attached manuscript remains attributed to Beth / TGS:ATE / ORION. The proof, diagnostic models and claim mappings are an audit of that manuscript. Upstream project notices accompany their respective sources. A content digest establishes the bytes used in this run. Independent physical data, independent reviewer approval and a hosted GitHub Actions run are outside the recorded evidence.

[Run record](evidence/RUN.md) · [Original protocol](protocol/criteria.md) · [Numerical follow-up protocol](protocol/extension.md) · [Source manuscript](source/blueprint.md)
