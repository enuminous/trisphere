"""Exercise both the extracted local HTML and project-subpath HTTP deployment."""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def run(screenshot=None):
    request=functools.partial(Quiet,directory=str(ROOT.parent))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),request)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        with sync_playwright() as pw:
            for url,width in [((ROOT/'index.html').as_uri(),390),(f'http://127.0.0.1:{server.server_port}/{ROOT.name}/index.html',1280)]:
                browser=pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_EXECUTABLE") or shutil.which('chromium') or None,args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu","--no-zygote","--single-process"])
                print('Chromium',browser.version)
                page=browser.new_page(viewport={'width':width,'height':880},accept_downloads=True)
                errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('request',lambda req:requests.append(req.url))
                page.goto(url)
                assert int(page.locator('#proofCount').inner_text())>=25
                assert page.locator('#layerName').inner_text()=='Filter'
                if screenshot and width==1280:page.screenshot(path=screenshot)
                def pick(id,value):
                    page.locator('#'+id).fill(str(value));page.locator('#'+id).dispatch_event('input')
                def tab(id):page.locator('#tab-'+id).click()
                page.locator('#zero').click();assert page.locator('#hopfVal').inner_text()=='0'
                page.locator('#mirror').click();assert page.locator('#rVal').inner_text()=='12'
                pick('camera',140);assert '140' in page.locator('#cameraVal').inner_text()
                page.locator('#atlas details summary').click();pick('keep',100)
                assert 'Layer 11 = 0.00' in page.locator('#routing').inner_text()
                tab('dynamics');pick('drag',0.5)
                for mode in ['fixed','kick','removed','coast']:
                    page.select_option('#mode',mode)
                    for quantity in ['r','v','e']:page.select_option('#quantity',quantity)
                    assert page.locator('#rangeinfo').inner_text()
                page.locator('#dynamics details summary').click()
                page.select_option('#sweepFilter',label='positive fixed point')
                assert page.locator('#sweepRows tr').count()==36
                with page.expect_download() as event:page.locator('#exportSweep').click()
                assert len(json.loads(Path(event.value.path()).read_text()))==36
                pick('initial',1);assert 'Exit' in page.locator('#runStatus').inner_text()
                with page.expect_download() as event:page.locator('#exportTrace').click()
                csv=Path(event.value.path()).read_text().splitlines()
                assert csv[0].endswith('velocity,energy') and csv[1].startswith('coast,0.5,')
                page.locator('#resetDyn').click();assert page.locator('#mode').input_value()=='fixed'
                tab('compression');page.locator('#witness').click();assert page.locator('#fine').inner_text()=='5 / 12'
                page.locator('#tick').click();assert page.locator('#coarseNum').inner_text()=='2 / 4'
                page.locator('#reverse').click();page.locator('#tick').click();assert page.locator('#fine').inner_text()=='5 / 12'
                tab('ledger');page.locator('#fullReport summary').click()
                page.select_option('#reportSection',label='Energy accounting')
                assert 'E′' in page.locator('#reportBody pre').first.inner_text()
                with page.expect_download() as event:page.locator('#exportReport').click()
                assert Path(event.value.path()).read_text()==(ROOT/'AUDIT.md').read_text()
                page.locator('#fullReport summary').click()
                page.select_option('#verdict','FAIL');page.fill('#search','periodic')
                assert page.locator('#rows details').count()>0
                page.locator('#rows summary').first.click();page.locator('#rows button').first.click()
                assert page.locator('#sourceDialog').is_visible();page.locator('#sourceDialog button').click()
                page.locator('[data-ledger="roster"]').click();page.fill('#search','PEGASUS')
                with page.expect_download() as event:page.locator('#exportLedger').click()
                records=json.loads(Path(event.value.path()).read_text())
                assert len(records)==1 and records[0]['name']=='PEGASUS'
                tab('proofs');page.locator('#proofRows summary').first.click()
                assert 'TriSphere.mirror_involution' in page.locator('#proofRows pre').first.inner_text()
                with page.expect_download() as event:page.locator('#downloadLean').click()
                assert Path(event.value.path()).read_bytes()==(ROOT/'TriSphere.lean').read_bytes()
                for panel in ['atlas','dynamics','compression','ledger','proofs']:
                    tab(panel)
                    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),(width,panel)
                assert not errors,errors
                assert all(u==url or u.startswith('blob:') for u in requests),requests
                print(('file://' if width==390 else 'HTTP project subpath'),width,'PASS: all workspaces, inputs, local downloads, source, no external network or overflow.')
                page.close()
                browser.close()
    finally:server.shutdown();thread.join();server.server_close()
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--screenshot')
    run(parser.parse_args().screenshot)
