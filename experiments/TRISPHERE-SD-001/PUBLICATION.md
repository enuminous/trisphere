# Publication record — 2026-11-27

SD-001 is published as a bounded computational research result, with its original report, protocol, source, dependency pins, logs, replay verification and manifests. Beth's Filter is an interpretive name for the constructed state selector. No consciousness, intentional agency, microscopic pinch derivation, generic quantum scaling or physical validation is established.

All thirteen original SHA-256 entries passed verification in the local evidence directory before publication. The complete original archive is TRISPHERE-SD-001.zip (SHA-256: 859dac60793a418dbb1884b8f126f3bafd4499da5c18ddcc3ec5073b32083c5a). The original raw results.json and supplement.json remain in that archive and are not included in this commit. All other original files are preserved. MANIFEST.sha256 describes the entire original package; until regenerating the two outputs, use sha256sum -c --ignore-missing MANIFEST.sha256 to verify the deposited files. Run sha256sum -c pre_execution.sha256 to verify primary inputs, then replay in a separate working directory:

    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python supplement.py
    sha256sum -c MANIFEST.sha256

The same-environment primary replay reported byte-identical numerical results. Floating-point/platform differences can affect replay hashes. No new execution or independent replication is claimed by this publication. The historical README statement "GitHub unchanged" refers to the time of the original experiment. The main lab and claims ledger remain unchanged. The original DRV-001/EXC-001 reference source is included here as a dependency; their standalone archive is a separate publication obligation.
