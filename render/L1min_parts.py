# Interaction-state parts for L1-min (peek tooltip, inspect column, shared sparkline).
from common import *
FOOT=[('ROBOT DETAIL','inspect'),('TIMELINE','drill'),('ALARM LOG','alarm'),('DIAGNOSTICS','diag')]
def topline(h1):
    """Shared top line: identical pixels on every L1-min state; only the h1 text changes per level."""
    return f'''<div class="a row" style="left:32px;right:32px;top:0;height:56px;gap:32px">
<span class="mono" style="font-weight:500;font-size:12px;letter-spacing:.2em;color:{MUT}">ANDURA</span>
<span class="h1">{h1}</span><span style="flex:1"></span>
<span class="lbl">CONTROL <span style="color:{TXT}">M. KELLER</span></span>
<span class="lbl">DATA <span style="color:{TXT}">0.3 s</span></span>
<span class="lbl" style="color:{TXT}">09:56 <span class="mut">CEST</span></span></div>'''
def footer(active=None,hover=None,focus=None):
    """Fixed 176 px slots so links never shift; active = Text + 2 px underline (not colour alone)."""
    o=f'<div class="a row lbl" style="left:32px;right:32px;bottom:0;height:72px">'
    for t,k in FOOT:
        on=k is not None and k==active;hv=t==hover;fc=t==focus
        ring=f'outline:2px solid {TXT};outline-offset:2px;' if fc else ''
        o+=(f'<span class="hit" style="width:176px;height:72px;display:flex;align-items:center">'
            f'<span style="{ring}color:{TXT if on or hv else MUT};box-shadow:{"0 6px 0 -4px "+TXT if on else "none"};padding-bottom:4px;margin-top:4px">{t} ›</span></span>')
    o+='<span style="flex:1"></span><span>E-STOP: PHYSICAL ONLY</span></div>'
    return o
def back(x,dest,y=60):
    """Back: names its destination, Esc keycap as quiet signifier, 56 px tall hit area centred on y=88."""
    return (f'<div class="a row hit" style="left:{x}px;top:{y}px;height:56px;gap:12px">'
            f'<span class="lbl" style="color:{TXT}">‹ {dest}</span>'
            f'<span class="lbl" style="border:1px solid {LINE};padding:0 4px;line-height:14px;font-size:11px;letter-spacing:.04em">ESC</span></div>')
def vlim(v,u,lim,cls='vm'):
    """One value/limit format everywhere: value (Text) + unit (Muted) … LIMIT n unit (label)."""
    return (f'<div class="row" style="align-items:baseline;gap:8px"><span class="{cls}">{v}</span><span class="mut">{u}</span>'
            f'<span style="flex:1"></span><span class="lbl">LIMIT {lim} <span style="text-transform:none">{u}</span></span></div>')

def spark(vals,lim,w,h=32,lo=0.4):
    """Frameless sparkline on a value/limit scale: the dashed line is the limit, so every
    parameter shows headroom the same way (deviation, not raw units)."""
    top=1.15
    f=lambda v:h-((v/lim)-lo)/(top-lo)*h
    P=' '.join(f'{i/(len(vals)-1)*(w-4):.1f},{f(v):.1f}' for i,v in enumerate(vals))
    ex,ey=w-4,f(vals[-1])
    return (f'<svg width="{w}" height="{h}" style="display:block;overflow:visible">'
            f'<line x1="0" y1="{f(lim):.1f}" x2="{w}" y2="{f(lim):.1f}" stroke="{MUT}" stroke-dasharray="2 4"/>'
            f'<polyline points="{P}" fill="none" stroke="{TXT}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="2.5" fill="{TXT}"/></svg>')

def inspect_col(VW,band=False):
    # With the alarm band (56-152) present, back moves below it (hit 160-216) and content starts at 232, so nothing overlaps.
    X=VW+48;Wc=1600-X-32;o=back(X,'CELL C3',160 if band else 60)
    r=f'<div class="a" style="left:{X}px;top:{232 if band else 176}px;width:{Wc}px">'
    r+=f'<div class="row" style="gap:8px">{glyph("sel",14)}<span class="h2">KR-02 · Nailing</span></div>'
    r+=f'<div class="row" style="justify-content:space-between;margin-top:8px"><span class="mut">W-12 · stud 6 of 9</span><span class="mono">ETA 10:21 <span class="mut">· +2 min</span></span></div>'
    par=[('PATH DEVIATION','0.42','mm','0.50',[0.30,0.32,0.35,0.31,0.36,0.38,0.37,0.40,0.39,0.41,0.42,0.42],0.50),
         ('NAIL DEPTH ERROR','0.30','mm','1.00',[0.2,0.3,0.25,0.35,0.3,0.28,0.32,0.3,0.27,0.3,0.31,0.3],1.0),
         ('J3 TORQUE','62','%','85',[55,58,60,57,61,63,60,62,64,61,62,62],85)]
    r+='<div style="margin-top:48px">'
    for lab,v,u,lim,sp,l in par:
        r+=f'<div style="margin-bottom:24px"><div class="lbl">{lab}</div><div style="margin-top:8px">{vlim(v,u,lim)}</div><div style="margin-top:8px">{spark(sp,l,Wc)}</div></div>'
    r+=f'<div class="mut" style="margin-top:-8px">Last 10 min · dashed = limit · TCP speed in range</div></div>'
    r+=f'<div class="lbl" style="margin-top:48px">EVENTS</div><div style="margin-top:8px">'
    for t,e in [('09:52','Stud 5 set'),('09:41','Magazine refilled'),('09:30','W-12 started')]:
        r+=f'<div class="row" style="height:32px;gap:16px"><span class="mono mut">{t}</span><span>{e}</span></div>'
    r+='</div></div>';o+=r
    return o


BAND_H=96
def alarmband():
    """ONE band spec for every layout: 48 px row per active P1/P2, P1 on top, max 2 rows (more -> '+n' in row 2).
    Same 09:54 scenario everywhere: P1 KR-03 unacked, P2 KR-01 acked but still active."""
    return (f'<div class="a" style="left:0;right:0;top:56px;height:{BAND_H}px;background:{SURF}">'
        f'<div class="a row" style="left:0;right:32px;top:0;height:48px;gap:16px"><span class="pulse" style="width:6px;height:48px;background:{EM}"></span>'
        f'<span style="margin-left:26px" class="row">{glyph("p1",16)}</span><span class="h3">P1 EMERGENCY</span>'
        f'<span>Cell C3 · KR-03 protective stop · J5 force 412 N, limit 380 N</span><span class="lbl">09:54:12 · UNACK</span><span style="flex:1"></span>'
        f'<span class="btn hit" style="height:40px">PROCEDURE SP-114</span><span class="btn pri hit" style="height:40px">ACKNOWLEDGE</span></div>'
        f'<div class="a row" style="left:0;right:32px;top:48px;height:48px;gap:16px;border-top:1px solid #000"><span style="width:6px;height:47px;background:{CA}"></span>'
        f'<span style="margin-left:26px" class="row">{glyph("p2",16)}</span><span class="h3">P2 CAUTION</span>'
        f'<span class="mut">Cell C3 · KR-01 nailer magazine 14 % · ~6 min left</span><span class="lbl">09:51:40 · ACKED</span></div></div>')
TOUCH_CSS=f'.hit{{outline:1px dashed {MUT};outline-offset:-1px;min-height:56px}}'
