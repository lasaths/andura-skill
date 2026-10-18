# Worked example: L1 alarm (`l1-alarm.html`)

A complete L1 "3D dominant" screen built only from `tokens/build/andura.css`. It has no hex values and no other stylesheet (`scripts/check.py` enforces both). Open it in a browser. `?state=alarm` (default) shows the 09:54 scenario: P1 KR-03 protective stop unacked, P2 KR-01 magazine low acked. `?state=normal` shows the same cell with nothing active. `?state=inspect` shows KR-02 selected with its detail in the column. `?scale=1.25|1.5|2` follows OS text size (`text-scale.*`). The 3D view is a flat SVG stand-in; in production an engine renders it, and the overlay rules stay the same.

Coordinates are CSS px, measured in headless Chrome at the reference canvases. They are y from the top, x from the left.

## Zones
| Zone | Desktop 1600 × 1000 | Tablet 1180 × 820 | Token |
|---|---|---|---|
| Margin | 32 | 24 | `size.margin.*` |
| Top line | y 0–56 | y 0–56 | `size.topline.*` |
| Alarm band (alarm only) | y 56–152, 2 rows × 48 | y 56–168, 2 rows × 56 | `size.alarm-row.*` |
| 3D viewport (Surface) | x 0–1120, from the band (or y 56) to y 928 | x 0–680, to y 748 | — |
| Gap viewport → column | 48 | 32 | `space.48`, `space.32` |
| Answer column (Void) | x 1168–1568, width 400 | x 712–1156, width 444 | — |
| Column content starts | y 176 in both states | y 192 alarm, y 176 normal | — |
| Footer | y 928–1000; slots of 176 at x 32, 208, 384, 560 | y 748–820; slots of 168 from x 24 | `size.footer.*`, `size.footer-slot.*` |

The band appears only while a P1 or P2 is active. Its height comes out of the viewport and the column, so the top line and footer never move. `scripts/persist_check.py` proves this pixel for pixel.

## Alarm band row
- **Edge bar:** 4 px wide (`space.4`), full row height, at x 0. Emergency for P1, pulsing at 1 Hz (opacity 1 → 0.35, `motion.duration.pulse`) until it is acknowledged. Caution for P2, steady. With reduced motion, the pulse stops.
- **Glyph:** 16 × 16 px at x = margin, vertically centred (desktop y 72). P1 = Emergency octagon with a Void `!`. P2 = Caution triangle with a Void `!`.
- **Content, left to right, gap 16:** priority word (`label`, Text), message (`body`; Text for P1, Muted for P2), time and ack state (`label`, Muted).
- **Buttons:** right-aligned to the margin, gap 8. Desktop height 40 (`size.button-band`): PROCEDURE (secondary, Line outline), then ACKNOWLEDGE (primary, Ultramarine fill). On tablet the buttons fill the 56 px row.

## Answer column (desktop values; tablet in brackets)
| Block | Spec |
|---|---|
| CELL | `label` at y 176. Then, 8 below: status glyph 16 + `title` "Partly stopped". Then `body` Muted "KR-03 stopped · KR-01 caution" (hidden on tablet) |
| Progress (dimmed to 55 % in alarm) | 48 [24] below. `label` "KR-02 · W-12 PROGRESS". `display` 64 [`value-l` 40] "63" + `value-m` Muted "%". 4 px bar (Line track, Text fill), 16 below |
| Path deviation | 48 [24] below. `label`, then `value-l` "0.42" + Muted "mm" with "LIMIT 0.50 mm" right-aligned, `label` |
| Sparkline | 8 below the value. Full column width × 32 px. Limit = dashed Muted line (2/3 dash) at the top. Trace = 1.5 px Text. End dot r = 2.5. Desktop y 560–592 |
| Robots | Bottom-aligned, 24 above the footer. `label` "ROBOTS". Rows of 32 [56] px (`size.row.*`). The 16 px glyph column is always reserved. Abnormal rows are in Text, normal rows Muted. On tablet each row shows ›. Desktop first row y 808 |

## 3D overlay
- **Status tags:** 1 px border in the status colour, Void fill, padding 4 × 8, glyph 16 + `label` in Text ("KR-03 · STOP").
- **Neutral tag:** Line border ("KR-02 · NAILING").
- **Status rim:** 2.5 px on the robot in Emergency or Caution, drawn over its `color.3d.face-3` body.
- **Commanded path:** dashed Ultramarine 3 px (`size.stroke-commanded`).
- **Legend:** bottom-left at the margin, 24 above the viewport bottom.

## Interaction marking (used by the checks)
- Mark every interactive element with class `hit`: band buttons, robot rows, footer links. `scripts/touch_check.py` measures every `.hit`. On tablet each must be 56 × 56 px or larger, inside the canvas, and must not overlap another. Text must be 12 px or larger on every class.
- Anything that looks clickable (`button`, `a`, `.btn`, or text with ›, ‹ or ✕) must sit inside a `.hit`.
- Focus: 2 px Text outline with a 2 px offset (`size.focus-ring`, `size.focus-gap`).

## Phone 390 × 844 (< 600 px)
| Zone | Spec |
|---|---|
| Top line | y 0–48 (`size.topline.phone`): h1 (truncates) + clock only |
| Alarm band | y 48–112, 1 row × 64 (`size.alarm-row.phone`): edge bar, glyph, P1 word, message (ellipsis), "+1 ›" target (≥ 56 wide, full row height) opening the alarm list. No buttons; acknowledge is hold-to-ack in the detail |
| 3D thumbnail | x 16–374, 16 below the band, 176 tall (`size.thumb-3d-phone`); one `.hit`, opens full-screen 3D; no tags or legend |
| Column | single column under the thumbnail, scrolls; progress block hidden; robot rows 64 (`size.row.phone`) |
| Tab bar | y 764–844: 64 (`size.footer.phone`) + 16 home zone (`size.home-zone`). CELL · ROBOTS · ALARMS (Emergency glyph badge) · MORE, 4 equal slots; active = Text + 2 px top bar |

## Inspect state (`?state=inspect`)
- No alarm active (band absent). KR-02 gets a 2.5 px Ultramarine outline drawn outside the robot in 3D.
- Column from y 176 (phone: 24 below the thumbnail): back target "‹ CELL C3" with ESC keycap (keycap hidden on phone), then 16 below the selection square (2 px Ultramarine) + `title` "KR-02 · Nailing", then W-12 / ETA.
- Three parameters, 24 apart: `label`, `value-m` value + Muted unit, LIMIT right-aligned, 32 px sparkline with dashed limit: PATH DEVIATION 0.42 / 0.50 mm, NAIL DEPTH ERROR 0.30 / 1.00 mm, J3 TORQUE 62 / 85 %.
- Footer: ROBOT DETAIL is active (Text + 2 px underline). Phone: ROBOTS tab active. `persist_check.py` masks only this slot.

## Text scaling (`?scale=`)
`--s` multiplies every font size, line height and text-bearing chrome height. The column is `min(400 × s, 50 %)` wide and scrolls. `.trunc` labels get an ellipsis and a `title` (peek); `.value` never shrinks or wraps. 3D tags are engine labels and are not scaled-checked (see risks in `CHANGELOG.md`).
