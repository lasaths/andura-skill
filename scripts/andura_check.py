"""ANDURA single entry point. Runs, for each page: check.py --example (token-only colour/size/duration, andura.css loaded,
recipes without drift, canonical glyphs), touch_check.py (targets, text, clipping, 3D outlines; every class x state x
scale) and persist_check.py (fixed chrome across states). With --all it also runs the repo check (check.py) and every
examples/*.html. Prints one PASS or FAIL summary; exit 0 only if everything passes.
Usage: python3 scripts/andura_check.py page.html [more.html ...] [--classes ...] [--states ...] [--scales ...]
       python3 scripts/andura_check.py --all"""
import argparse, glob, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)

def run(name, cmd):
    r = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=ROOT)
    out = (r.stdout + r.stderr).strip().splitlines()
    bad = [l for l in out if l.startswith(("FAIL", "    ", "Traceback")) or "Error" in l]
    skips = [l for l in out if l.startswith("SKIP")]
    print(f"{'PASS' if r.returncode == 0 else 'FAIL'}  {name}" + (f"  ({len(skips)} skipped)" if skips else ""))
    for l in (bad if r.returncode else []) + skips: print("   ", l)
    return r.returncode == 0

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="*")
    ap.add_argument("--all", action="store_true", help="repo check + every examples/*.html")
    ap.add_argument("--classes", nargs="+"); ap.add_argument("--states", nargs="+"); ap.add_argument("--scales", nargs="+")
    a = ap.parse_args()
    pages = [os.path.abspath(p) for p in a.pages] + (sorted(glob.glob(f"{ROOT}/examples/*.html")) if a.all else [])
    if not pages and not a.all: ap.error("give a page.html or --all")
    opt = lambda *k: sum(([f"--{x}"] + getattr(a, x) for x in k if getattr(a, x)), [])
    ok = run("repo: check.py", [f"{HERE}/check.py"]) if a.all else True
    for p in pages:
        n = os.path.relpath(p, ROOT) if p.startswith(ROOT) else p
        ok &= run(f"{n}: check.py --example", [f"{HERE}/check.py", "--example", p])
        ok &= run(f"{n}: touch_check", [f"{HERE}/touch_check.py", p] + opt("classes", "states", "scales"))
        ok &= run(f"{n}: persist_check", [f"{HERE}/persist_check.py", p] + opt("classes") + (["--states"] + [s for s in a.states if s != "normal"] if a.states else []))
    print(f"ANDURA CHECK: {'PASS' if ok else 'FAIL'} ({len(pages)} page{'s' * (len(pages) != 1)})")
    sys.exit(0 if ok else 1)
