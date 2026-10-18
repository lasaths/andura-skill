"""Touch and text-scale check for examples/l1-alarm.html, every class x state x text scale (tokens text-scale.*).
Fails when: a .hit target is < size.touch-min (56 px) on tablet/phone (any class at 200 %) or leaves the canvas; two targets
overlap; two text runs overlap; text is below size.text-min (12 px); text is clipped (overflows its box without ellipsis +
title for peek, or is cut by an overflow:hidden ancestor); a .value is truncated at all; a clickable-looking element
(button, link, ›, ‹, ✕) sits outside a .hit. Includes a self-test. Usage: python3 scripts/touch_check.py   (exit 0 = pass)"""
import json, os, sys
from _chrome import ROOT, EXAMPLE, CLASSES, STATES, dump
TOK = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))
TOUCH, TEXT = TOK["size"]["touch-min"]["$value"]["value"], TOK["size"]["text-min"]["$value"]["value"]
SCALES = [v["$value"] for k, v in TOK["text-scale"].items() if not k.startswith("$")]
JS = """<script>addEventListener('load',()=>{const vis=e=>e.offsetParent||getComputedStyle(e).position=='fixed';
const sc=e=>{for(let a=e.parentElement;a;a=a.parentElement){const o=getComputedStyle(a).overflowY;if((o=='auto'||o=='scroll')&&a.scrollHeight>a.clientHeight)return a}return null};
const inview=e=>{const s=sc(e);if(!s)return true;const b=e.getBoundingClientRect(),p=s.getBoundingClientRect();return b.top>=p.top-1&&b.bottom<=p.bottom+1};
const hits=[...document.querySelectorAll('.hit')].filter(e=>vis(e)&&inview(e)).map(e=>{const b=e.getBoundingClientRect();
return [Math.round(b.width),Math.round(b.height),Math.round(b.right),Math.round(b.bottom),(e.textContent||'').trim().slice(0,24),Math.round(b.left),Math.round(b.top)]});
let mn=99;const clip=[],runs=[];const ok3d=e=>e.closest('.viewport');
document.querySelectorAll('body *:not(script):not(style):not(pre)').forEach(e=>{if(!vis(e))return;const own=[...e.childNodes].filter(n=>n.nodeType==3&&n.textContent.trim());
const cs=getComputedStyle(e);if(own.length)mn=Math.min(mn,parseFloat(cs.fontSize));
if(!ok3d(e)&&e.scrollWidth>e.clientWidth+1&&cs.overflowX!='visible'){const ell=cs.textOverflow=='ellipsis'&&e.closest('[title]');
 if(e.closest('.value')||!ell)clip.push((e.className.baseVal===undefined?e.className:'')+' '+e.textContent.trim().slice(0,24))}
const tr=[...document.querySelectorAll('*')].find(a=>a.contains(e)&&getComputedStyle(a).textOverflow=='ellipsis'&&a.closest('[title]'));
own.forEach((n,k)=>{if(ok3d(e))return;const r=document.createRange();r.selectNodeContents(n);[...r.getClientRects()].forEach(b0=>{if(b0.width<1)return;let b=b0;
 if(tr&&!e.closest('.value')){const t=tr.getBoundingClientRect();b={left:Math.max(b0.left,t.left),right:Math.min(b0.right,t.right),top:b0.top,bottom:b0.bottom}}
 for(let a=e;a;a=a.parentElement){const ac=getComputedStyle(a);if(['auto','scroll'].includes(ac.overflowY))break;
  if(ac.overflow!='visible'){const p=a.getBoundingClientRect();
  if(b.left<p.left-1||b.right>p.right+1||b.top<p.top-1||b.bottom>p.bottom+1){clip.push('cut '+n.textContent.trim().slice(0,24));break}}}
 if(inview(e))runs.push([b.left,b.top,b.right,b.bottom,n.textContent.trim().slice(0,16),n])})})});
const ov=[];for(let i=0;i<runs.length;i++)for(let j=i+1;j<runs.length;j++){const a=runs[i],b=runs[j];
 if(a[5]!==b[5]&&a[0]<b[2]-1&&b[0]<a[2]-1&&a[1]<b[3]-2&&b[1]<a[3]-2)ov.push(a[4]+' / '+b[4])}
const un=[];document.querySelectorAll('body *:not(script):not(style)').forEach(e=>{if(!vis(e))return;const own=[...e.childNodes].filter(n=>n.nodeType==3).map(n=>n.textContent).join('');
if((e.matches('button,a,.btn')||/[›‹✕]/.test(own))&&!e.closest('.hit'))un.push(own.trim().slice(0,24)||e.tagName)});
const p=document.createElement('pre');p.id='R';p.style.display='none';p.textContent=JSON.stringify({hits,minfont:mn,unmarked:un,clip,overlap:ov});document.body.appendChild(p)})</script>"""

def measure(src, w, h, state, scale=1):
    tmp = f"/tmp/andura_tc_{os.getpid()}.html"
    html = open(src).read().replace('href="../', f'href="file://{os.path.dirname(os.path.dirname(os.path.abspath(src)))}/')
    open(tmp, "w").write(html.replace("</body>", JS + "</body>"))
    try:
        return dump(tmp, w, h, f"?state={state}&scale={scale}")
    finally:
        os.remove(tmp)

def evaluate(R, w, h, touch):
    errs = []
    if touch:
        errs += [f"target {x[4]!r} {x[0]}x{x[1]} < {TOUCH}" for x in R["hits"] if x[0] < TOUCH or x[1] < TOUCH]
        errs += [f"target {x[4]!r} outside canvas" for x in R["hits"] if x[2] > w or x[3] > h]
    for i, a in enumerate(R["hits"]):
        for b in R["hits"][i + 1:]:
            if a[5] < b[2] and b[5] < a[2] and a[6] < b[3] and b[6] < a[3]: errs.append(f"targets {a[4]!r} and {b[4]!r} overlap")
    if R["minfont"] < TEXT: errs.append(f"text {R['minfont']} px < {TEXT}")
    errs += [f"unmarked interactive element {u!r}" for u in R["unmarked"]]
    errs += [f"clipped text {c!r}" for c in R["clip"]] + [f"text overlap {o!r}" for o in R["overlap"]]
    return errs

if __name__ == "__main__":
    fail = 0
    bad = "/tmp/andura_tc_selftest.html"
    open(bad, "w").write('<html><body><button>X</button><span>MORE ›</span><div class="hit" style="width:40px;height:40px">ok</div><div class="hit" style="position:absolute;left:0;top:0;width:60px;height:60px">a</div><div class="hit" style="position:absolute;left:30px;top:30px;width:60px;height:60px">b</div><span style="font-size:10px">tiny</span>'
                     '<div style="width:30px;overflow:hidden;white-space:nowrap">CLIPPED LABEL</div><div style="width:40px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis"><span class="value">123.456</span></div>'
                     '<div style="position:absolute;left:200px;top:200px">OVER</div><div style="position:absolute;left:205px;top:202px">LAP</div></body></html>')
    st = evaluate(measure(bad, 390, 844, "alarm"), 390, 844, True)
    os.remove(bad)
    ok = (len([e for e in st if "unmarked" in e]) == 2 and any("< 56" in e for e in st) and any(e.startswith("text ") for e in st)
          and any("targets" in e for e in st) and any("CLIPPED" in e for e in st) and any("123" in e for e in st) and any("text overlap" in e for e in st))
    print(f"{'PASS' if ok else 'FAIL'}  self-test: unmarked button and › link, 40 px target, overlapping targets, 10 px text, clipped label, truncated value, overlapping text detected")
    fail += not ok
    for cls, (w, h) in CLASSES.items():
        for state in STATES:
            for s in SCALES:
                R = measure(EXAMPLE, w, h, state, s)
                errs = evaluate(R, w, h, cls != "desktop" or s >= 2)
                print(f"{'PASS' if not errs else 'FAIL'}  {cls} {state} {int(s*100)} %: {len(R['hits'])} targets, min {min(min(x[0], x[1]) for x in R['hits'])} px, min text {R['minfont']} px")
                for e in errs: print("   ", e)
                fail += bool(errs)
    sys.exit(1 if fail else 0)
