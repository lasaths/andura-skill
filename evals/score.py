"""Score one eval page against evals/criteria.md. Usage: python3 evals/score.py evals/out/saw1.html
Exit 0 only if every automatic criterion (A1-A6) passes. Needs Chrome and Pillow (same as the checks)."""
import os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, f"{ROOT}/scripts")
from check import _Tree, _walk, _match  # the recipe matcher used by the drift check
from _chrome import screenshot
from PIL import ImageChops, Image

def has(tree, sel): return any(_match(n, sel) for n in _walk(tree))

def main(page):
    page = os.path.abspath(page); src = open(page).read(); res = []
    r = subprocess.run([sys.executable, f"{ROOT}/scripts/andura_check.py", page], capture_output=True, text=True)
    res.append(("A1 all ANDURA checks pass", r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]))
    m = re.search(r"<!--[^>]*\bL([1-6])\b", src[:2048]); res.append(("A2 layout declared", bool(m), f"L{m.group(1)}" if m else "no L1-L6 comment"))
    text = re.sub(r"<(script|style)\b.*?</\1>|<[^>]+>", " ", src, flags=re.S)
    miss = lambda ws: [w for w in ws if w not in text]
    m3 = miss(["KR-03", "09:54:12", "KR-01", "09:51:40", "P1", "P2"]); res.append(("A3 scenario shown", not m3, f"missing {m3}" if m3 else "ok"))
    m4 = miss(["SAW-1", "11:40", "14:00", "46", "20", "71", "85", "1:38", "LIMIT", "TARGET"]); res.append(("A4 values and limits", not m4, f"missing {m4}" if m4 else "ok"))
    t = _Tree(src); need = {"alarm-row P1": "div.r.p1", "alarm-row P2": "div.r.p2", "tabs": "nav.tabs", "hold": "button.hold", "dialog": "dialog"}
    m5 = [k for k, s in need.items() if not has(t.root, s)]; res.append(("A5 recipes used", not m5, f"missing {m5}" if m5 else "ok"))
    shots = {s: Image.open(screenshot(page, s, 1600, 1000, f"/tmp/andura_eval_{os.getpid()}_{s}.png")).convert("RGB") for s in ("alarm", "normal", "detail")}
    d1 = ImageChops.difference(shots["alarm"], shots["normal"]).getbbox(); d2 = ImageChops.difference(shots["alarm"], shots["detail"]).getbbox()
    for s in shots: os.remove(f"/tmp/andura_eval_{os.getpid()}_{s}.png")
    res.append(("A6 states differ", bool(d1 and d2), f"alarm≠normal: {bool(d1)}, alarm≠detail: {bool(d2)}"))
    for n, ok, why in res: print(f"{'PASS' if ok else 'FAIL'}  {n}: {why}")
    if r.returncode: print("A1 failures:\n" + "\n".join(l for l in r.stdout.splitlines() if not l.startswith("PASS"))[:3000])
    ok = all(x[1] for x in res); print(f"EVAL: {'PASS' if ok else 'FAIL'} ({sum(x[1] for x in res)}/{len(res)})"); return ok

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit(__doc__)
    sys.exit(0 if main(sys.argv[1]) else 1)
