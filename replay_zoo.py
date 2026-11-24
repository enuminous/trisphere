"""Run the original pinned Zoo checks. Logs go to a selectable directory."""
import argparse
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMMANDS = [
    "python3 verify.py",
    "lake build",
    "lake env lean -DwarningAsError=true Audit.lean",
    "python3 scripts/test_axiom_audit.py",
    "python3 scripts/extension_fixtures.py",
    "python3 scripts/report_fixtures.py",
    "lake env lean -DwarningAsError=true .lake/SourceReportFixtures.lean",
    "python3 scripts/threshold_fixtures.py",
    "lake env lean -DwarningAsError=true .lake/ThresholdFixtures.lean",
    "python3 scripts/test_alternative_report.py",
    "lake exe regression",
    "lake exe zoo46",
]
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "replay-output" / "zoo.log")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as log:
        for command in COMMANDS:
            print("$", command, file=log, flush=True)
            result = subprocess.run(command.split(), cwd=ROOT / "vendor/zoo", stdout=log, stderr=subprocess.STDOUT)
            print("EXIT", result.returncode, file=log, flush=True)
            if result.returncode:
                raise SystemExit(result.returncode)
