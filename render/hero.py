"""L1 desktop in the alarm + inspect state (KR-02 selected while KR-03 is in P1), written to hero.html.
Trimmed from the ANDURA layouts pipeline; palette comes from tokens/andura.tokens.json via common.py."""
from common import *
from L1min_parts import topline, footer, alarmband, inspect_col
T = 56; VW = 1120; VH = 1000 - T - 72
svg, I, pts = cell_scene(VW, VH, sel='KR-02', alarm='KR-03', caut='KR-01', pad=40, k=60, ox=500, oy=280)
svg = svg.replace('opacity="0.55"', 'opacity="0.28"')
vp = f'<div class="a" style="left:0;top:{T}px;width:{VW}px;height:{VH}px;background:{SURF};overflow:hidden">{svg}'
x, y = I.p(*pts['KR-02'][-2]); vp += callout(x, y, 40, -110, '<span class="h3">KR-02 · NAILING</span>', LINE)
x, y = I.p(*pts['KR-03'][-2]); vp += callout(x, y, -60, -130, f'<span class="row" style="gap:6px">{glyph("p1",14)}<span class="h3">KR-03 · STOP</span></span>', EM)
x, y = I.p(*pts['KR-01'][-2]); vp += callout(x, y, -40, -120, f'<span class="row" style="gap:6px">{glyph("p2",14)}<span class="h3">KR-01 · MAG LOW</span></span>', CA)
vp += '</div>'
b = vp + topline('Cell C3 · Wall panel line') + alarmband() + inspect_col(VW, band=True) + footer('inspect')
FACES = ''.join(f"@font-face{{font-family:'{fam}';src:url('fonts/{f}');font-weight:{w};}}" for fam, f, w in
                [('IBM Plex Sans', 'IBMPlexSans[wdth,wght].ttf', '100 700'), ('IBM Plex Mono', 'IBMPlexMono-Regular.ttf', '400'), ('IBM Plex Mono', 'IBMPlexMono-Medium.ttf', '500')])
open('hero.html', 'w').write(page(b, 'hero').replace('<style>', '<style>' + FACES, 1))
