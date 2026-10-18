"""Persistence check for examples/l1-alarm.html: the top line and the footer are pixel-identical between the normal and
alarm states and between normal and inspect, on desktop, tablet and phone (hard rule 6). The alarm band itself is excluded
because the P1 edge pulses. For inspect the active navigation slot (footer ROBOT DETAIL; phone CELL/ROBOTS tabs) is masked,
since showing where you are is its job.
Includes a self-test. Usage: python3 scripts/persist_check.py   (exit 0 = pass). Needs Pillow."""
import json, os, sys
from PIL import Image, ImageChops, ImageDraw
from _chrome import ROOT, EXAMPLE, CLASSES, STATES, screenshot
S = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))["size"]
px = lambda n: n["$value"]["value"]

def diff(a, b, box, mask=None):
    if mask:
        a, b = a.copy(), b.copy()
        for im in (a, b): ImageDraw.Draw(im).rectangle(mask, fill=(0, 0, 0))
    bb = ImageChops.difference(a.crop(box).convert("RGB"), b.crop(box).convert("RGB")).getbbox()
    return bb

if __name__ == "__main__":
    fail = 0
    for cls, (w, h) in CLASSES.items():
        shots = {s: Image.open(screenshot(EXAMPLE, s, w, h, f"/tmp/andura_pc_{cls}_{s}.png")) for s in STATES}
        foot = px(S["footer"][cls]) + (px(S["home-zone"]) if cls == "phone" else 0)
        zones = {"top line": (0, 0, w, px(S["topline"][cls])), "footer": (0, h - foot, w, h)}
        m = px(S["margin"][cls])
        active = (0, h - foot, w // 2, h) if cls == "phone" else (0, h - foot, m + px(S["footer-slot"][cls]) + 16, h)
        for other in ("alarm", "inspect"):
            for name, box in zones.items():
                bb = diff(shots["normal"], shots[other], box, active if other == "inspect" and name == "footer" else None)
                print(f"{'PASS' if not bb else 'FAIL'}  {cls} {name}: normal vs {other}" + (f" differ in {bb}" if bb else ", 0 px"))
                fail += bool(bb)
        if cls == "desktop":  # self-test: a 1 px change in the footer must be caught
            t = shots["alarm"].copy(); ImageDraw.Draw(t).point((w // 2, h - 10), fill=(255, 255, 255))
            ok = diff(shots["alarm"], t, zones["footer"]) is not None
            print(f"{'PASS' if ok else 'FAIL'}  self-test: 1 px footer change detected"); fail += not ok
        for s in shots: os.remove(f"/tmp/andura_pc_{cls}_{s}.png")
    sys.exit(1 if fail else 0)
