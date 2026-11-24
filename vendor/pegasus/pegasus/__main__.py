import argparse
import json
import sys
from pathlib import Path

from .audit import FAIL, audit_file, verify_freeze


def main():
    parser = argparse.ArgumentParser(description="PEGASUS bounded hybrid-construction auditor")
    parser.add_argument("input", nargs="?", type=Path, help="Claims JSON")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify-freeze", action="store_true")
    args = parser.parse_args()
    if args.verify_freeze:
        report = verify_freeze()
    elif args.input:
        try:
            report = audit_file(args.input)
        except (ValueError, OSError) as exc:
            print(f"Invalid input: {exc}", file=sys.stderr)
            return 2
    else:
        parser.error("Provide input JSON or --verify-freeze")
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    # UNRESOLVED must never produce a successful certification exit code.
    return {"PASS": 0, "FAIL": 1, "UNRESOLVED": 3}[report["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())
