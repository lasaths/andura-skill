import json, math, os
_T = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tokens', 'andura.tokens.json')))['color']
_c = lambda k: _T[k]['$value']
BG,SURF,LINE,MUT,TXT=_c('void'),_c('surface'),_c('line'),_c('muted'),_c('text')
UM,UMT,EM,CA,NO=_c('ultramarine'),_c('ultramarine-text'),_c('emergency'),_c('caution'),_c('nominal')
D3={k:v['$value'] for k,v in _T['3d'].items()}  # 3D greys (color.3d.*)
W,H=1600,1000
CSS=f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;background:{BG};color:{TXT};font-family:'IBM Plex Sans';font-size:15px;line-height:20px;overflow:hidden;position:relative;font-variant-numeric:tabular-nums}}
.a{{position:absolute}}
.mono{{font-family:'IBM Plex Mono'}}
.lbl{{font-family:'IBM Plex Mono';font-weight:500;font-size:12px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;color:{MUT}}}
.h3{{font-family:'IBM Plex Mono';font-weight:500;font-size:12px;line-height:16px;letter-spacing:.08em;text-transform:uppercase;color:{TXT}}}
.h1{{font-weight:500;font-size:22px;line-height:28px;color:{MUT}}}
.h2{{font-weight:500;font-size:18px;line-height:24px;color:{TXT}}}
.vm{{font-family:'IBM Plex Mono';font-size:22px;line-height:28px}}
.vl{{font-family:'IBM Plex Mono';font-size:36px;line-height:40px;letter-spacing:-.01em}}
.disp{{font-family:'IBM Plex Mono';font-size:64px;line-height:64px;letter-spacing:-.02em}}
.mut{{color:{MUT}}} .acc{{color:{UMT}}}
.panel{{position:absolute;background:{SURF};border:1px solid {LINE}}}
.ph{{position:absolute;left:16px;right:16px;top:12px;height:24px;display:flex;align-items:center;justify-content:space-between}}
.hr{{height:1px;background:{LINE}}}
.chip{{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 8px;border:1px solid {LINE};font-family:'IBM Plex Mono';font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;white-space:nowrap}}
.btn{{display:inline-flex;align-items:center;justify-content:center;height:32px;padding:0 12px;border:1px solid {LINE};font-family:'IBM Plex Mono';font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:{TXT};white-space:nowrap}}
.btn.pri{{background:{UM};border-color:{UM}}}
.row{{display:flex;align-items:center}}
table{{border-collapse:collapse;width:100%}}
td,th{{text-align:left;padding:0 8px;height:36px;border-bottom:1px solid {LINE};white-space:nowrap}}
th{{height:32px;font-family:'IBM Plex Mono';font-weight:500;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:{MUT}}}
td.n,th.n{{text-align:right;font-family:'IBM Plex Mono'}}
.seg{{display:inline-flex;border:1px solid {LINE};height:32px}}
.seg span{{padding:0 12px;display:flex;align-items:center;font-family:'IBM Plex Mono';font-weight:500;font-size:12px;letter-spacing:.08em;color:{MUT}}}
.seg span.on{{color:{TXT};box-shadow:inset 0 -2px 0 {UM}}}
@keyframes p1pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
.pulse{{animation:p1pulse 1s ease-in-out infinite;animation-play-state:paused}} /* paused for static screenshots; live UI runs it until ack */
.hatch{{background:repeating-linear-gradient(135deg,transparent 0 5px,{LINE} 5px 6px)}}
"""
def glyph(kind,s=16):
    if kind=='p1':
        r=s/2;pts=' '.join(f"{r+r*math.cos(math.radians(22.5+45*i)):.1f},{r+r*math.sin(math.radians(22.5+45*i)):.1f}" for i in range(8))
        return f'<svg width="{s}" height="{s}" style="flex:none"><polygon points="{pts}" fill="{EM}"/><rect x="{s/2-1.2}" y="{s*.22}" width="2.4" height="{s*.36}" fill="#000"/><rect x="{s/2-1.2}" y="{s*.66}" width="2.4" height="2.4" fill="#000"/></svg>'
    if kind=='p2':
        return f'<svg width="{s}" height="{s}" style="flex:none"><polygon points="{s/2},1 {s-0.5},{s-1} 0.5,{s-1}" fill="{CA}"/><rect x="{s/2-1.1}" y="{s*.36}" width="2.2" height="{s*.3}" fill="#000"/><rect x="{s/2-1.1}" y="{s*.72}" width="2.2" height="2.2" fill="#000"/></svg>'
    if kind=='p3':
        return f'<svg width="{s}" height="{s}" style="flex:none"><circle cx="{s/2}" cy="{s/2}" r="{s/2-1}" fill="none" stroke="{TXT}" stroke-width="1.5"/><rect x="{s/2-1}" y="{s*.42}" width="2" height="{s*.34}" fill="{TXT}"/><rect x="{s/2-1}" y="{s*.22}" width="2" height="2" fill="{TXT}"/></svg>'
    if kind=='ok':
        return f'<svg width="{s}" height="{s}" style="flex:none"><polyline points="{s*.15},{s*.52} {s*.4},{s*.78} {s*.88},{s*.24}" fill="none" stroke="{NO}" stroke-width="2.2"/></svg>'
    if kind=='stale':
        return f'<svg width="{s}" height="{s}" style="flex:none"><circle cx="{s/2}" cy="{s/2}" r="{s/2-1}" fill="none" stroke="{MUT}" stroke-width="1.5" stroke-dasharray="2 2"/></svg>'
    if kind=='sel':
        return f'<svg width="{s}" height="{s}" style="flex:none"><rect x="1" y="1" width="{s-2}" height="{s-2}" fill="none" stroke="{UM}" stroke-width="2"/></svg>'

def page(body,title):
    return f'<!doctype html><html><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'
# ---------- isometric 3D ----------
class Iso:
    def __init__(s,ox,oy,k,yaw=30):
        s.ox,s.oy,s.k=ox,oy,k;s.c=math.cos(math.radians(yaw));s.s=math.sin(math.radians(yaw))
    def p(s,x,y,z=0):
        return (s.ox+(x-y)*s.c*s.k, s.oy+(x+y)*s.s*s.k*0.5*2*0.5*2 - z*s.k) if False else (s.ox+(x-y)*0.866*s.k, s.oy+(x+y)*0.5*s.k - z*s.k)
    def line(s,a,b,col,w=1,dash=None,op=1):
        (x1,y1),(x2,y2)=s.p(*a),s.p(*b);d=f' stroke-dasharray="{dash}"' if dash else ''
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"{d}/>'
    def poly(s,pts,fill='none',col=LINE,w=1,dash=None,op=1):
        P=' '.join(f'{x:.1f},{y:.1f}' for x,y in (s.p(*q) for q in pts));d=f' stroke-dasharray="{dash}"' if dash else ''
        return f'<polygon points="{P}" fill="{fill}" stroke="{col}" stroke-width="{w}" opacity="{op}"{d} stroke-linejoin="round"/>'
    def pl(s,pts,col,w=1,dash=None,op=1):
        P=' '.join(f'{x:.1f},{y:.1f}' for x,y in (s.p(*q) for q in pts));d=f' stroke-dasharray="{dash}"' if dash else ''
        return f'<polyline points="{P}" fill="none" stroke="{col}" stroke-width="{w}" opacity="{op}"{d} stroke-linejoin="round" stroke-linecap="round"/>'
    def box(s,x,y,z,dx,dy,dz,fill=D3['face-3'],col=D3['edge'],w=1):
        o=''
        o+=s.poly([(x,y+dy,z),(x+dx,y+dy,z),(x+dx,y+dy,z+dz),(x,y+dy,z+dz)],D3['face-1'],col,w)
        o+=s.poly([(x+dx,y,z),(x+dx,y+dy,z),(x+dx,y+dy,z+dz),(x+dx,y,z+dz)],D3['face-2'],col,w)
        o+=s.poly([(x,y,z+dz),(x+dx,y,z+dz),(x+dx,y+dy,z+dz),(x,y+dy,z+dz)],fill,col,w)
        return o
def robot(I,bx,by,pose,state='norm',label=None):
    # pose: list of world pts relative chain
    pts=[(bx+a,by+b,c) for a,b,c in pose]
    o=''
    base=I.p(bx,by,0);o+=f'<ellipse cx="{base[0]:.1f}" cy="{base[1]:.1f}" rx="{0.45*I.k:.1f}" ry="{0.26*I.k:.1f}" fill="{D3["base"]}" stroke="{D3["detail"]}"/>'
    if state=='hover':   # hover: thin Text outline, no fill change
        o+=I.pl(pts,TXT,max(10,0.30*I.k)+2)
    if state in('selp1','selp2'):   # status is never hidden by selection: Ultramarine outer outline + status rim inside
        o+=I.pl(pts,UM,max(10,0.30*I.k)+10);o+=I.pl(pts,EM if state=='selp1' else CA,max(10,0.30*I.k)+5)
    if state in('sel','p1','p2'):
        c={'sel':UM,'p1':EM,'p2':CA}[state]
        o+=I.pl(pts,c,max(10,0.30*I.k)+5)
    o+=I.pl(pts,D3['link'],max(10,0.30*I.k))
    o+=I.pl(pts,D3['link-line'],1.2)
    for q in pts[1:-1]:
        x,y=I.p(*q);o+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(4,0.12*I.k):.1f}" fill="{D3["joint"]}" stroke="{D3["joint-line"]}" stroke-width="1"/>'
    tx,ty=I.p(*pts[-1]);o+=f'<rect x="{tx-4:.1f}" y="{ty-2:.1f}" width="8" height="10" fill="{D3["detail"]}"/>'
    return o,pts
def callout(x,y,dx,dy,html,col=LINE,w=None):
    lx,ly=x+dx,y+dy
    o=f'<svg class="a" style="left:0;top:0;overflow:visible" width="1" height="1"><line x1="{x}" y1="{y}" x2="{lx}" y2="{ly}" stroke="{col}" stroke-width="1"/><circle cx="{x}" cy="{y}" r="2.5" fill="{col}"/></svg>'
    o+=f'<div class="a" style="left:{lx}px;top:{ly-14}px;background:{SURF};border:1px solid {col};padding:4px 8px;white-space:nowrap{";width:%dpx"%w if w else ""}">{html}</div>'
    return o
def cell_scene(w,h,k=None,ox=None,oy=None,pad=24,sel='KR-02',alarm='KR-03',progress=0.63,showlabels=True,element='W-12',caut=None,hover=None):
    if k is None:
        k=min((w-2*pad)/(20*0.866),(h-2*pad-40)/(10+2.6))
        ox=pad+8*0.866*k+((w-2*pad)-20*0.866*k)/2; oy=pad+40+2.6*k
    I=Iso(ox,oy,k);o=''
    # floor grid on Surface-ish
    for i in range(0,13):
        o+=I.line((i,0,0),(i,8,0),LINE,1,op=.55)
    for j in range(0,9):
        o+=I.line((0,j,0),(12,j,0),LINE,1,op=.55)
    # safety zone fence
    o+=I.pl([(0.3,0.3,0),(11.7,0.3,0),(11.7,7.7,0),(0.3,7.7,0),(0.3,0.3,0)],D3['edge'],1,'6 4')
    # rail track
    o+=I.line((1,1.2,0),(11,1.2,0),D3['edge'],2);o+=I.line((1,1.6,0),(11,1.6,0),D3['edge'],2)
    # assembly table
    o+=I.box(3,3.2,0,6,2.8,0.75)
    z=0.76
    # wall panel element W-12: 5.4 x 2.5 frame
    x0,y0=3.3,3.35;L,Wd=5.4,2.5
    o+=I.poly([(x0,y0,z),(x0+L,y0,z),(x0+L,y0+Wd,z),(x0,y0+Wd,z)],D3['element'],TXT,1.4)
    # window opening
    o+=I.poly([(x0+2.0,y0+0.7,z),(x0+3.4,y0+0.7,z),(x0+3.4,y0+1.9,z),(x0+2.0,y0+1.9,z)],D3['face-1'],MUT,1)
    n=10
    for i in range(n):
        sx=x0+0.3+i*(L-0.6)/(n-1)
        if 2.0<sx-x0<3.4: continue
        done=i/(n-1)<=progress
        o+=I.line((sx,y0,z),(sx,y0+Wd,z),TXT if done else MUT,2 if done else 1,None if done else '4 4',1 if done else .8)
    # toolpath commanded (dashed ultramarine) and actual
    tp=[(x0+0.3+i*(L-0.6)/(n-1),y0+0.15,z+0.02) for i in range(n)]
    o+=I.pl(tp,UM,3,'8 6')
    cur=int(progress*(n-1))
    o+=I.pl(tp[:cur+1],TXT,1.6)
    # robots on track
    poses={'KR-01':[(0,0,0),(0,0,0.9),(0.6,0.8,1.7),(1.2,1.8,1.3),(1.4,2.2,0.95)],
           'KR-02':[(0,0,0),(0,0,0.9),(-0.2,0.9,1.9),(0.0,1.9,1.6),(0.05,2.2,0.95)],
           'KR-03':[(0,0,0),(0,0,0.9),(0.5,0.6,1.8),(1.3,1.0,2.0),(1.7,1.0,1.6)]}
    bases={'KR-01':(2.2,1.4),'KR-02':(x0+0.3+cur*(L-0.6)/(n-1),1.4),'KR-03':(10.3,1.4)}
    pts={}
    for r in ['KR-01','KR-02','KR-03']:
        st=('selp1' if r==alarm else 'selp2' if r==caut else 'sel') if (r==sel or (isinstance(sel,tuple) and r in sel)) else ('p1' if r==alarm else ('p2' if r==caut else ('hover' if r==hover else 'norm')))
        s_,p_=robot(I,*bases[r],poses[r],st);o+=s_;pts[r]=p_
    # commanded ghost pose for selected (hollow)
    return f'<svg class="a" style="left:0;top:0" width="{w}" height="{h}">{o}</svg>',I,pts
