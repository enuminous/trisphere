"""Ensure incorrect statements and hidden assumptions fail for the intended reason."""
from pathlib import Path
import subprocess
import tempfile
import sys

ROOT=Path(__file__).resolve().parents[1]
base=(ROOT/'Audit.lean').read_text()
marker='open Lean in\nrun_cmd do'
probes=[
 ('false mirror center','import TriSphere\nexample : TriSphere.mirror 0 = 0 := by decide\n','is false'),
 ('invented axiom',base.replace(marker,'axiom AuditProbe.fabrication : False\n'+marker),'Unapproved axiom AuditProbe.fabrication'),
 ('placeholder proof',base.replace(marker,'theorem AuditProbe.hole : False := by sorry\n'+marker),'Unapproved axiom sorryAx')]
with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
    p=Path(tmp)/'Probe.lean'
    for name,src,expected in probes:
        p.write_text(src)
        r=subprocess.run(['lake','env','lean',str(p)],cwd=ROOT,capture_output=True,text=True)
        log=r.stdout+r.stderr
        if r.returncode==0 or expected not in log:
            raise SystemExit(f'{name}: unexpected acceptance or diagnostic\n{log[-2200:]}')
        print(f'{name}: rejected (exit {r.returncode})')
        print(next(line for line in log.splitlines() if expected in line))
