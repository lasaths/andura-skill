"""Render assets/hero.png (2400 x 1200) with the vendored renderer in render/.
Steps: download IBM Plex (SIL OFL 1.1) into render/fonts/ if missing, write render/hero.html (L1 desktop, alarm + inspect),
screenshot it at 3x in headless Chrome, crop a 1200 x 600 CSS-px window and downsample to 2400 x 1200, add the wordmark.
Usage: python3 scripts/render_hero.py   Needs Pillow and Chrome (set CHROME to override the binary)."""
import os, subprocess, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chrome import ROOT, BASE
R = f"{ROOT}/render"; FONTS = f"{R}/fonts"
PLEX = "https://raw.githubusercontent.com/google/fonts/main/ofl"
FILES = {"IBMPlexMono-Regular.ttf": "ibmplexmono", "IBMPlexMono-Medium.ttf": "ibmplexmono", "IBMPlexSans[wdth,wght].ttf": "ibmplexsans"}

os.makedirs(FONTS, exist_ok=True)
for f, d in FILES.items():
    if not os.path.exists(f"{FONTS}/{f}"):
        urllib.request.urlretrieve(f"{PLEX}/{d}/{f.replace('[', '%5B').replace(']', '%5D')}", f"{FONTS}/{f}")
subprocess.run([sys.executable, "hero.py"], cwd=R, env={**os.environ, "PYTHONPATH": R}, check=True)
shot = "/tmp/andura-hero-3x.png"
subprocess.run(BASE[:-1] + ["--force-device-scale-factor=3", "--window-size=1600,1000", "--virtual-time-budget=2000",
                f"--screenshot={shot}", f"file://{R}/hero.html"], check=True, capture_output=True)
x, y = 420, 56  # CSS px: alarm band slice on top, KR-01/02/03 with tags, selected KR-02, value column
hero = Image.open(shot).convert("RGB").crop((x * 3, y * 3, x * 3 + 3600, y * 3 + 1800)).resize((2400, 1200), Image.LANCZOS)
d = ImageDraw.Draw(hero)
mono = ImageFont.truetype(f"{FONTS}/IBMPlexMono-Medium.ttf", 40)
sans = ImageFont.truetype(f"{FONTS}/IBMPlexSans[wdth,wght].ttf", 30)
sans.set_variation_by_axes([400, 100])  # weight 400, width 100
cx = 80
for ch in "ANDURA":  # label tracking +0.08em
    d.text((cx, 236), ch, font=mono, fill="#DADADD"); cx += mono.getlength(ch) + 0.08 * 40
d.text((80, 296), "Dark-mode UI for mission-critical digital twins", font=sans, fill="#8A8C91")
hero.save(f"{ROOT}/assets/hero.png", optimize=True)
os.remove(f"{R}/hero.html"); os.remove(shot)
print("assets/hero.png", hero.size)
