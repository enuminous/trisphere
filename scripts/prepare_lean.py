"""Install the bundled pinned Lean dependencies into the local project, offline."""
import argparse
import json
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MATH = ROOT / "formal-deps" / "mathlib"

def prepare(source_only=False):
    bundles = sorted((ROOT / "vendor").glob("lean-sources*.zip"))
    if not bundles:
        raise FileNotFoundError("Missing bundled Lean sources")
    for bundle in bundles:
        with zipfile.ZipFile(bundle) as source:
            source.extractall(MATH.parent)
    if source_only:
        return
    osname = platform.system()
    arch = {"AMD64":"x86_64","arm64":"aarch64"}.get(platform.machine(),platform.machine())
    suffix = {"Linux":"unknown-linux-musl","Darwin":"apple-darwin","Windows":"pc-windows-msvc"}.get(osname)
    ext = ".zip" if osname=="Windows" else ".tar.gz"
    archive = ROOT / "vendor/leantar" / f"leantar-v0.1.15-{arch}-{suffix}{ext}"
    if not archive.exists():
        print("Source snapshot installed. Build locally with lake build.")
        return
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp)
        exe = path / ("leantar.exe" if osname=="Windows" else "leantar")
        if ext==".zip":
            with zipfile.ZipFile(archive) as z:
                exe.write_bytes(z.read(next(n for n in z.namelist() if n.endswith("leantar.exe"))))
        else:
            with tarfile.open(archive) as z:
                member=next(m for m in z if m.isfile() and Path(m.name).name=="leantar")
                with z.extractfile(member) as src, exe.open("wb") as dst: shutil.copyfileobj(src,dst)
        exe.chmod(0o755)
        for pack in sorted((ROOT/"vendor/cache").glob("part-*.zip")):
            with zipfile.ZipFile(pack) as z:
                z.extractall(path)
                names=[str(path/n) for n in z.namelist()]
            subprocess.run([str(exe),"-x","-j","-"],input=json.dumps(names),text=True,cwd=MATH,check=True)
            for n in names: Path(n).unlink()

if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-only",action="store_true",help="Omit precompiled dependencies")
    prepare(p.parse_args().source_only)
