# ANDURA — Charts

Four chart types, and only these: **sparkline**, **trend with limit band**, **histogram**, **Gantt / fabrication progress**. Principle 8 still holds: on the live monitor a trend is a sparkline. Full charts live on analytics (L4) and design-to-fabrication (L6) screens. Recipes: `recipes.md` §13 (`trend`, `hist`, `gantt`) and the `spark` part; CSS in `examples/andura-ui.css`.

## 1. Shared rules
| Rule | Value | Why |
|---|---|---|
| Data colour | Text trace for a single series; **cividis** (`color.data.cividis-0…6`) for categories and ordered stages | cividis is CVD-safe and monotonic in lightness (Nuñez et al. 2018) |
| Alarm hues | Caution / Emergency **only** on the part that violates a limit: the over-limit segment, the over-limit bins, a held stage's edge | alarm colour keeps one meaning (ISA-101; hard rule 2) |
| Ultramarine | never in a chart, except the selected item's outline | selection only |
| Axes | HTML labels in `type.label`, Muted; **min and max only** on each axis, plus the limit value | Tufte data-ink; labels stay text so they scale and pass touch_check |
| Gridlines | none, except a 1 px Line baseline and the limit | data-ink |
| Limit | dashed, `size.stroke-accent`, Muted, labelled with its value ("LIMIT 4:30") | limit reads the same everywhere |
| Height | `size.chart-h` (120) × scale; sparkline `size.spark-h` (32) | |
| Text inside | none; values and the violation note sit beside the plot in a label with a glyph (shape + word, never colour alone) | hard rule 4 |
| Stale | the whole chart takes `data-stale-in` and an age chip; traces go Muted | never fake live (§ states) |
| Motion | none; data replaces in place | |

## 2. Sparkline
Word-sized: width = its column, height `size.spark-h`. Trace 1.5 px Text, end dot r 2.5 Text, dashed limit Muted. No axes, frame or tick. Scale = value-to-limit (0 … limit × 1.25), so headroom reads the same for every parameter on screen. A crossing does not recolour the trace; the readout beside it shows the P2 glyph and "OVER".

## 3. Trend with limit band
`figure.trend` > `figcaption.label` + `.plot` (`.yax` + `svg.tr`) + `.xax`.
- Band: the allowed range as a `Surface` rect (`.band`); baseline 1 px Line (`.base`).
- Trace: 1.5 px Text (`.trace`). Only the segment outside the band is redrawn in Caution at `size.stroke-rim` (`.over`); a P1 limit uses Emergency.
- Y axis: min, limit, max. X axis: start, end (and NOW if live).
- Beside the plot: `P2 glyph + OVER LIMIT 09:12–09:41`.

## 4. Histogram
`figure.hist` > `.hbars` of `.hb` bins (Line fill, gap `space.4`) on a 1 px Line baseline, plus `.limit-mark` (dashed Muted) at the limit. Bins beyond the limit are `.hb.over` (Caution). Labels: bin range min/max, count max, "N PARTS · K OVER LIMIT". No per-bin numbers.

## 5. Gantt / fabrication progress
`figure.gantt` > rows `.grow` (label, `.gtrack` of `size.gantt-bar` (12) height) + `.xax` + `.gkey`.
- Stages in cividis order: CUT `cividis-1`, FRAME `cividis-3`, NAIL `cividis-4`, CHECK `cividis-5` (`.gbar.s1…s4`).
- NOW: 1 px Text line through all rows (`.now`).
- A held stage gets a `size.stroke-accent` bottom edge: Emergency (`.held`, P1 cause) or Caution (`.held2`), plus the glyph and word in the row label. The bar fill stays cividis.
- Legend `.gkey` always present: swatch + word.

## 6. Sunlit
All chart colours come from tokens, so `data-andura-mode="sunlit"` (`colour.md` §9) needs no chart changes; cividis stays.

## 7. Check
`scripts/check.py` validates the recipes (root and required parts); `touch_check.py` checks label size and the stale age chip at every scale. Alarm-hue placement is a review item (not yet automated).
