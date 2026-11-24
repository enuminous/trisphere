"""Build standalone index.html from audited data, sources and offline assets."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build():
    lean=(ROOT/'TriSphere.lean').read_text()
    log=(ROOT/'evidence/lean-axioms.log').read_text()
    proofs=[]
    for n in re.findall(r'^theorem (\w+)',lean,re.M):
        name='TriSphere.'+n
        match=re.search(r'^'+re.escape(name)+r'\b.*?^\x27'+re.escape(name)+r'\x27[^\n]*',log,re.M|re.S)
        if not match: raise ValueError('Missing compiled proof record: '+n)
        proofs.append(dict(name=n,log=match.group()))
    data={k:json.loads((ROOT/(k+'.json')).read_text()) for k in ('claims','roster')}
    data.update(report=(ROOT/"AUDIT.md").read_text(),sweep=json.loads((ROOT/"evidence/sweep.json").read_text()),lean=lean,proofs=proofs,source=(ROOT/'source/blueprint.md').read_text().splitlines())
    data['correctedSource'] = (ROOT / 'source/blueprint-corrected.txt').read_text()
    template=(ROOT/'lab/page.html').read_text()
    for token,value in [('__APP__',(ROOT/'lab/app.js').read_text()),('__ENGINE__',(ROOT/'lab/engine.js').read_text()),('__DATA__',json.dumps(data,ensure_ascii=False).replace('<','\\u003c'))]:
        template=template.replace(token,value)
    return template
if __name__=='__main__':
    (ROOT/'index.html').write_text(build())
