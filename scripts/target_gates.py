"""Run pinned decision procedures on declared target inputs; preserve native output."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys, tempfile, types
B = Path(__file__).resolve().parents[1]

def run(out):
    sources=json.loads((B/'vendor/zoo/extension-sources.json').read_text())
    # Authored, reviewable adapters. Their field choices are part of the evidence boundary.
    specs={
      'Chimera':{'object':'fixed-position drive trajectory','interaction':'audit of the written law',
                 'has_classical_record': True,'operational_recovery':False,'evidence_sufficient':False},
      'Circus':{'pipeline':[{'stage':'definition','provenance_status':'documented'}],
                'dependencies':[],'risks':[{'materiality':'material','status':'present',
                  'description':'periodicity used to describe a drive that does not yield a periodic orbit'}],
                'independent_checks':[]},
      'Zoo-Monster':{'preregistration':{'registered_before_outcomes':False},
                     'baseline':{'matched':False},'conditions':[]}
    }
    results={}
    for repo,inp in specs.items():
        r=next(s for s in sources if s['repository']=='enuminous/'+repo)
        code=r['content'].encode()
        assert hashlib.sha1(b'blob '+str(len(code)).encode()+b'\0'+code).hexdigest()==r['git_blob_sha1']
        mod=types.ModuleType('target_'+repo.replace('-','_')); sys.modules[mod.__name__]=mod
        exec(compile(code,r['path'],'exec'),mod.__dict__)
        value=mod.classify(mod.Event(**inp)) if repo=='Chimera' else mod.decide(inp)
        results[repo]={'input':inp,'result':value,'commit':r['commit'],'git_blob':r['git_blob_sha1']}
    assert results['Chimera']['result']['tags']==['U','C']
    assert results['Circus']['result']=='FAIL' and results['Zoo-Monster']['result']=='N/A'
    out.mkdir(parents=True,exist_ok=True)
    (out/'target-gates.json').write_text(json.dumps(results,indent=2)+'\n')
    proc=subprocess.run([sys.executable,'-m','pegasus',str(B/'protocol/pegasus.json'),'--output',str(out/'pegasus.json')],cwd=B/'vendor/pegasus')
    assert proc.returncode==3,proc.returncode
    report=json.loads((out/'pegasus.json').read_text())
    assert report['verdict']=='UNRESOLVED' and report['counts']['PASS']==2
    print('CHIMERA',results['Chimera']['result']['tags'],'CIRCUS FAIL, MONSTER N/A, PEGASUS UNRESOLVED (expected native exit 3)')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path,nargs='?',default=B/'replay-output')
    run(p.parse_args().output.resolve())
