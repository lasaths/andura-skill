"""Shared headless-Chrome helpers for touch_check.py and persist_check.py. Set CHROME to override the binary."""
import json, os, re, shutil, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLE = f"{ROOT}/examples/l1-alarm.html"
CHROME = os.environ.get("CHROME") or next((b for b in ("google-chrome", "chromium", "chromium-browser") if shutil.which(b)), "google-chrome")
BASE = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1"]
CLASSES = {"desktop": (1600, 1000), "tablet": (1180, 820), "phone": (390, 844)}
STATES = ("alarm", "normal", "inspect")

def url(path, state, scale=1):
    return f"file://{path}?state={state}&scale={scale}"

def screenshot(path, state, w, h, out, scale=1):
    subprocess.run(BASE + [f"--window-size={w},{h}", "--virtual-time-budget=1000", f"--screenshot={out}", url(path, state, scale)], check=True, capture_output=True)
    return out

_PAD = None
def _chrome_pad():
    """Headless --dump-dom reserves window chrome (about 87 px), so the viewport is shorter than --window-size. Measure it once."""
    global _PAD
    if _PAD is None:
        tmp = "/tmp/andura_vh.html"
        open(tmp, "w").write('<html><body><script>document.write("<pre id=R>"+JSON.stringify([innerWidth,innerHeight])+"</pre>")</script></body></html>')
        out = subprocess.run(BASE + ["--window-size=800,800", "--dump-dom", f"file://{tmp}"], capture_output=True, text=True, check=True).stdout
        _PAD = 800 - int(re.search(r"\[\d+,(\d+)\]", out).group(1))
        os.remove(tmp)
    return _PAD

def dump(html_path, w, h, query=""):
    """Load the page in an iframe of exactly w x h CSS px (headless windows cannot go below 500 px wide) and return the JSON
    the page wrote into <pre id="R">."""
    wrap = f"/tmp/andura_wrap_{os.getpid()}.html"
    open(wrap, "w").write(f'<html><body style="margin:0"><iframe id=F src="file://{html_path}{query}" style="border:0;width:{w}px;height:{h}px"></iframe>'
        '<script>const t=setInterval(()=>{try{const r=F.contentDocument.getElementById("R");if(r){clearInterval(t);'
        'const p=document.createElement("pre");p.id="R";p.textContent=r.textContent;document.body.appendChild(p)}}catch(e){}},50)</script></body></html>')
    try:
        out = subprocess.run(BASE + ["--allow-file-access-from-files", f"--window-size={max(w, 500) + 20},{h + _chrome_pad() + 20}",
                                     "--virtual-time-budget=4000", "--dump-dom", f"file://{wrap}"], capture_output=True, text=True, check=True).stdout
    finally:
        os.remove(wrap)
    m = re.search(r'<pre id="R"[^>]*>(.*?)</pre>', out, re.S)
    return json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">"))
