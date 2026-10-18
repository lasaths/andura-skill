# ANDURA — Typography (locked, IBM Plex)
*Dark UI for 3D digital-twin dashboards. **Sans for text, Mono for numbers, IDs and labels.** Palette v2.2. Specimen `assets/type-scale-v2.png`. [DC] = design choice; [ASSUMPTION] = verify on the real installation.*

## 1. Fonts
**IBM Plex Sans (text) + IBM Plex Mono (numbers, labels, IDs). Regular width only (`wdth` 100). Weights: 400 and 500.**
```css
--font-sans: "IBM Plex Sans", system-ui, sans-serif;
--font-mono: "IBM Plex Mono", ui-monospace, monospace;
body { font-family: var(--font-sans); font-stretch: 100%; font-variant-numeric: tabular-nums; }
.num, .label, code { font-family: var(--font-mono); font-variant-numeric: tabular-nums slashed-zero; }
```
- **Plex Mono has no Greek delta (U+0394):** write deviation as `DEV`. Glyph-check any other Greek before use.
- Licence: SIL OFL 1.1 ([github.com/IBM/plex](https://github.com/IBM/plex)).
- Weight evidence: at 64 px under combined blur, glare and distance, Regular 400 keeps 24 % more stroke contrast than thinner weights (2.29 vs 1.85), so every value is 400. Label 12 px Mono 500 beats 400 (1.81 vs 1.68), so labels are 500. Body stays 400 so it is clearly lighter than title 500. These are proxy metrics; validate on real screens.

## 2. Scale: desktop, tablet, wall (7 tokens, 6 distinct sizes)
| Token | Font / weight | Colour | Desktop | Tablet | Wall 4K (cap arcmin @5 m) | Tracking | Use |
|---|---|---|---|---|---|---|---|
| `display` | Mono 400 | Text | 64/64 | 72/72 | 320/320 (97′) | −0.02em | Hero value, max 1 per screen |
| `value-l` | Mono 400 | Text | 36/40 | 40/48 | 176/192 (53′) | −0.01em | KPI readouts |
| `value-m` | Mono 400 | Text | 22/28 | 24/32 | 112/136 (34′) | 0 | Table/stat values. Safety floor for values |
| `h1` | Sans 500 | Muted | 22/28 | 24/32 | 112/136 (34′) | 0 | Page/view title, once per screen |
| `title` (h2) | Sans 500 | Text | 18/24 | 20/28 | 88/112 (27′) | 0 | Panel title, one per panel |
| `body` | Sans 400 | Text; Muted for secondary/caption | 15/20 | 16/24 | 72/92 (22′) | 0 | Text, row names, notes, KPI units |
| `label` (h3 in Text) | Mono 500 CAPS | Muted (Text for section heads, chips) | 12/16 | 13/16 | 56/64 (17′) | +0.08em | Field labels, column headers, section heads, chips, footer meta |

## 3. Phone scale
| Token | Phone | Step |
|---|---|---|
| label | 12/16 Mono 500 caps | floor |
| body | 15/20 Sans 400 | ×1.25 |
| title / h1 | 18/24 Sans 500 (h1 Muted) | ×1.20 |
| value-m | 22/28 Mono 400 | ×1.22 |
| value-l | 28/32 Mono 400 | ×1.27 |
| display | 40/44 Mono 400 | ×1.43 |
Six sizes, every step ≥ 1.2, nothing below 12 px (checked by `layouts/src/touch_check.py`). h1 shares 18 with title on phone; it stays distinct by colour (Muted) and position (top line).

## 4. Heading hierarchy
| Level | Token | Spec | Colour | Role | Count |
|---|---|---|---|---|---|
| h1 | `h1` (new) | Plex Sans 500, 22/28 D · 24/32 T · 112/136 W (34′ @5 m) | Muted #8A8C91 (6.24:1 Void, 5.89:1 Surface) | Page/view title | Once per screen |
| h2 | `title` | Plex Sans 500, 18/24 · 20/28 · 88/112 | Text | Panel title | One per panel |
| h3 | `label` | Plex Mono 500 CAPS +0.08em, 12/16 · 13/16 · 56/64 | Text (Muted for plain field labels) | Section inside a panel | As needed |

- **Sizing (visual-angle method):** h1 sits on the existing 22 → 24 → 112 step (wall 112 px = 34′ cap height at 5 m, the same as `value-m`). This adds no new size, so the unique-size ramp is unchanged and every adjacent step stays ≥ 1.20: desktop 1.25 · 1.20 · 1.22 · 1.64 · 1.78; tablet 1.23 · 1.25 · 1.20 · 1.67 · 1.80; wall 1.29 · 1.22 · 1.27 · 1.57 · 1.82. Giving h1 its own size between title 18 and value-m 22 would make a step below 1.2. Putting it between 22 and 36 would need about 27 (1.23 / 1.33), which makes h1 bigger than table values and works against the blur rule.
- **Shared 22 px with value-m is acceptable** *(design choice)*: they never compete, because they differ on three axes: family (Sans vs Mono), colour (Muted vs Text) and position (h1 only at top-left of the view, above a rule; value-m only in tables and stats). The `legibility_v2.py` ratio check now runs on unique sizes and lists `h1 = value-m` as the only intentional shared size.

## 5. Ratio: a mixed scale
- **Text ramp ×1.2–1.25** (label 12 → body 15 → title 18 → value-m 22: 1.25 · 1.20 · 1.22). Dense dashboards need small steps at the bottom; 1.2 is the smallest step that still reads as a separate level.
- **Value ramp ×1.6–1.8** (22 → 36 → 64: 1.64 · 1.78). Values must be found at a glance and outrank all text; a single 1.25 ramp either puts KPIs too close to headings (v1: 44 vs 22 only because steps were skipped) or runs out of room.
- Every adjacent pair ≥ 1.20 on all three targets (desktop 1.25/1.20/1.22/1.64/1.78, tablet 1.23/1.25/1.20/1.67/1.80, wall 1.29/1.22/1.27/1.57/1.82), checked in `legibility_v2.py`.


## 6. Squint test (blur 6 px, peak luminance, `legibility_v2.json`)
hero 110 · KPI 75 · table value 62 · title 58 · h1 44 (Muted) · body 41. Strictly values > headings > text.

## 7. Contrast (WCAG, on Void #000 / Surface #090A0C)
Text #DADADD 15.05 / 14.20 · Muted #8A8C91 6.24 / 5.89 · Ultramarine Text #5A74F1 5.20 / 4.91 (links only). All ≥ 4.5:1. #3A3CFF is never text.

## 8. Wall sizes (visual angle)
θ = 2·atan(h / 2d). Character height ≥ 16 arcmin minimum, 20–22′ preferred (MIL-STD-1472, NASA HIDH §10, ANSI/HFES 100) [ASSUMPTION: verify clause numbers]. Installation [ASSUMPTION]: 110″ 4K wall, pixel pitch 0.634 mm, farthest viewer 5 m, cap height 0.698 em.
- 16′ at 5 m → 56 px floor (label); 22′ → body 72 px; values ≥ 34′ (value-m 112 px); display 320 px = 97′.
- Formula for another wall: `font_px = d·tan(θ) / (0.698·p)`. A 65″ 4K wall (p = 0.375 mm) needs every wall size ×1.69.
- The wall shows only the L1 overview.

## 9. Rules
1. Tabular figures wherever numbers update or align; right-align numeric columns, fixed field widths.
2. `slashed-zero` on in Mono; IDs, part codes and coordinates always in Mono.
3. Floors: text ≥ 12 px on every class; safety-relevant values ≥ value-m; wall ≥ 56 px.
4. Weights: 400 (values, body), 500 (h1, title, label). Nothing else.
5. Colour: Text for values and primary text, Muted for labels and units. Status colours go on glyphs and edge bars, with the words in Text colour. Colour is never the only cue.
6. CAPS only in Mono labels/status, tracked +0.08em. Sentence case for Sans. Units keep SI case even in caps headers (`CMD Nm`, `LIMIT 0.50 mm`).
7. Units: Muted, after a space, on the baseline (hero → value-m, KPI → body). Fewest significant digits; mm with 2 decimals. Numbers refresh at 2–4 Hz.
8. Line length 45–75 characters; tooltips ≤ 2 lines. Per screen: 2 families, ≤ 6 sizes, 400 + 500.
9. **OS text size (WCAG 1.4.4).** Support `text-scale.*` steps 1, 1.25, 1.5 and 2. Multiply font size and line height by the step on every class except the wall (wall sizes come from visual angle). Values and units never truncate or wrap; labels truncate with an ellipsis and show the full text on peek. The 12 px floor applies at 100 %.
