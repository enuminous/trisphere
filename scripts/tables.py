"""Render human-readable ledgers from the machine-readable audit rows."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def render():
    claims=json.loads((R/'claims.json').read_text())
    roster=json.loads((R/'roster.json').read_text())
    c=['# Claim register','',f'{len(claims)} findings on the pinned blueprint. Source lines refer to source/blueprint.md.','']
    for r in claims:
        c.extend([f"## {r['id']} · {r['title']}",'',f"**{r['status']}** · {r['kind']} · lines {r['lines']}",'',r['result'],'',f"Evidence — {r['evidence']}",'',f"Scope or next test — {r['next']}",''])
    z=['# Zoo operation register','','53 names accounted for. The registered core has 46 entries. The five tracked extensions, standalone PEGASUS and unresolved HUMMINGBIRD lookup are listed by provenance. Each finding addresses the target criterion printed on its row.','']
    for r in roster:
        z.extend([f"## {r['name']} · {r['status']}",'',f"{r['family']} · {r['mode']}",'',f"**Operation** — {r['scope']}",'',f"**Target criterion** — {r['criterion']}",'',r['result'],'',f"**Software baseline** — {r['baseline']}",'',f"**Evidence** — {r['evidence']}",''])
        if r['pin']:z.extend([f"[Source at {r['pin']}]({r['repository']}/tree/{r['pin']})",''])
    return {'CLAIMS.md':'\n'.join(c),'ROSTER.md':'\n'.join(z)}
if __name__=='__main__':
    for n,s in render().items():(R/n).write_text(s)
