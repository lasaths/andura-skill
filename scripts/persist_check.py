"""Persistence check for examples/l1-alarm.html: the top line and the footer are pixel-identical between the normal and
alarm states and between normal and inspect, on desktop, tablet and phone (hard rule 6). The alarm band itself is excluded
because the P1 edge pulses. Only the exact rects of state-indicating elements are masked, in both images: the active slot
([aria-current]) and alarm badges (.badge), read from the DOM of each state. A state that renders identically to normal is reported SKIP (the page lacks it), not PASS.
Usage: python3 scripts/persist_check.py [page.html] [--classes desktop tablet phone] [--states alarm inspect]
Includes a self-test. Exit 0 = pass. Needs Pillow."""
import argparse, json, os, sys
from PIL import Image, ImageChops, ImageDraw
from _chrome import ROOT, EXAMPLE, CLASSES, STATES, screenshot, dump, prepare
S = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))["size"]
px = lambda n: n["$value"]["value"]

MARK = """<script>addEventListener('load',()=>setTimeout(()=>{const r=[...document.querySelectorAll('[aria-current],.badge')].filter(e=>e.offsetParent)
.map(e=>{const b=e.getBoundingClientRect();return [Math.floor(b.left),Math.floor(b.top),Math.ceil(b.right),Math.ceil(b.bottom)]});
const p=document.createElement('pre');p.id='R';p.style.display='none';p.textContent=JSON.stringify(r);document.body.appendChild(p)},100))</script>"""

def marks(page, state, w, h):
    """Exact rects of the state-indicating elements: the active slot ([aria-current]) and alarm badges (.badge)."""
    tmp = prepare(page, MARK, "pcm")
    try:
        return [tuple(r) for r in dump(tmp, w, h, f"?state={state}&scale=1")]
    finally:
        os.remove(tmp)

def diff(a, b, box, mask=()):
    if mask:
        a, b = a.copy(), b.copy()
        for im in (a, b):
            for m in mask: ImageDraw.Draw(im).rectangle(m, fill=(0, 0, 0))
    bb = ImageChops.difference(a.crop(box).convert("RGB"), b.crop(box).convert("RGB")).getbbox()
    return bb

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=EXAMPLE)
    ap.add_argument("--classes", nargs="+", default=list(CLASSES), choices=list(CLASSES))
    ap.add_argument("--states", nargs="+", default=[x for x in STATES if x != "normal"], help="states compared against normal")
    a = ap.parse_args()
    page = os.path.abspath(a.page)
    fail = 0
    for cls in a.classes:
        w, h = CLASSES[cls]
        shots = {s: Image.open(screenshot(page, s, w, h, f"/tmp/andura_pc_{cls}_{s}.png")) for s in ["normal"] + a.states}
        foot = px(S["footer"][cls]) + (px(S["home-zone"]) if cls == "phone" else 0)
        zones = {"top line": (0, 0, w, px(S["topline"][cls])), "footer": (0, h - foot, w, h)}
        mk = {st: marks(page, st, w, h) for st in shots}
        for other in a.states:
            if diff(shots["normal"], shots[other], (0, 0, w, h)) is None:
                print(f"SKIP  {cls}: '{other}' renders the same as normal (state not in this page)"); continue
            for name, box in zones.items():
                mask = mk["normal"] + mk[other]
                bb = diff(shots["normal"], shots[other], box, mask)
                print(f"{'PASS' if not bb else 'FAIL'}  {cls} {name}: normal vs {other}" + (f" differ in {bb}" if bb else ", 0 px"))
                fail += bool(bb)
        if cls == "desktop" and "alarm" in shots:  # self-test: a 1 px change in the footer must be caught
            t = shots["alarm"].copy(); ImageDraw.Draw(t).point((w // 2, h - 10), fill=(255, 255, 255))
            ok = diff(shots["alarm"], t, zones["footer"]) is not None
            print(f"{'PASS' if ok else 'FAIL'}  self-test: 1 px footer change detected"); fail += not ok
        if cls == "phone" and "alarm" in shots:  # self-test: masking is exact, a change next to the badge is still caught
            t = shots["alarm"].copy(); bx = [m for m in mk["alarm"] if m[1] > h - foot]
            x = max(m[2] for m in bx) + 4; ImageDraw.Draw(t).point((min(x, w - 1), h - foot // 2), fill=(255, 255, 255))
            ok = diff(shots["alarm"], t, zones["footer"], mk["alarm"]) is not None
            print(f"{'PASS' if ok else 'FAIL'}  self-test: 1 px change 4 px beside the masked badge detected"); fail += not ok
        for s in shots: os.remove(f"/tmp/andura_pc_{cls}_{s}.png")
    sys.exit(1 if fail else 0)
