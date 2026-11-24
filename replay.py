"""Verify the flat release and rerun its pinned science and proof checks."""
from pathlib import Path
import argparse
from collections import Counter
import hashlib
import json
import os
import re
import subprocess
import sys
from scripts.build_lab import build
from scripts.tables import render

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'replay-output'
def check_package():
    targets=[]
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        p=ROOT/name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise SystemExit('Archive identity mismatch: '+name)
        targets.append(name)
    if len(set(targets))!=len(targets):raise SystemExit('Duplicate manifest entry')
    if hashlib.sha256((ROOT/'source/blueprint.md').read_bytes()).hexdigest()!='a93e2539d89c5cd5a1558fda2bc19557fcc4433cf99620621aa3b79550e1cff4':raise SystemExit('Unexpected target manuscript')
    for target,expected in [('index.html',build()),*render().items()]:
        if (ROOT/target).read_text()!=expected:raise SystemExit('Generated artifact is stale: '+target)
    roster=json.loads((ROOT/'roster.json').read_text())
    canonical=json.loads((ROOT/'vendor/zoo/coverage.json').read_text())
    if [r['name'] for r in roster[:46]]!=[r['name'] for r in canonical] or len({r['name'] for r in roster})!=53:raise SystemExit('Roster mismatch')
    print(f'Integrity PASS: {len(targets)} named release files. Standalone lab and ledgers reproduce.',flush=True)

def run(label,args,cwd=ROOT):
    log=OUT/(label+'.log')
    with log.open('w') as f:
        print('cwd:',Path(cwd).relative_to(ROOT),'\n$',*args,file=f,flush=True)
        r=subprocess.run(args,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
        print('EXIT',r.returncode,file=f)
    if r.returncode:
        print(log.read_text()[-3000:],file=sys.stderr)
        raise SystemExit(f'{label} failed; see {log}')
    print(label,'PASS',flush=True)
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only',action='store_true')
    parser.add_argument('--browser',action='store_true',help='Include optional Playwright/Chromium checks')
    args=parser.parse_args()
    check_package()
    if args.integrity_only:return
    OUT.mkdir(exist_ok=True)
    lean=subprocess.check_output(['lean','--version'],cwd=ROOT,text=True).strip()
    if not re.search(r'version 4\.19\.0[, ]',lean) or '6caaee8' not in lean:raise SystemExit('This release requires official Lean 4.19.0')
    print(lean)
    run('prepare',['python3','scripts/prepare_lean.py'])
    run('lean-build',['lake','build','TriSphere'])
    run('lean-axioms',['lake','env','lean','-DwarningAsError=true','Audit.lean'])
    run('negative-controls',['python3','scripts/proof_controls.py'])
    run('zoo-suite',['python3','replay_zoo.py','--output',str(OUT/'zoo.log')])
    run('zoo-target',['lake','env','lean','-DwarningAsError=true','../../ZooTarget.lean'],ROOT/'vendor/zoo')
    run('target-gates',['python3','scripts/target_gates.py',str(OUT)])
    run('experiments',['node','scripts/experiments.js',str(OUT/'experiments.json')])
    run('sweep',['python3','scripts/return_sweep.py',str(OUT/'sweep.json')])
    for name in ['target-gates','pegasus']:
        expected=json.loads((ROOT/f'evidence/{name}.json').read_text())
        actual=json.loads((OUT/f'{name}.json').read_text())
        if actual!=expected:raise SystemExit(name+' gate evidence changed')
    a=json.loads((OUT/'experiments.json').read_text())['checks']
    b=json.loads((ROOT/'evidence/experiments.json').read_text())['checks']
    if [(x['id'],x['pass']) for x in a]!=[(x['id'],x['pass']) for x in b]:raise SystemExit('Control inventory changed')
    a=json.loads((OUT/'sweep.json').read_text())
    b=json.loads((ROOT/'evidence/sweep.json').read_text())
    if [r['outcome'] for r in a['sweep']]!=[r['outcome'] for r in b['sweep']]:raise SystemExit('Sweep verdict changed')
    if args.browser:run('browser',['python3','scripts/check_lab.py'])
    print('Replay complete. Logs and regenerated evidence are in replay-output/.')
if __name__=='__main__':main()
