# Worked example: L2 split (`l2-split.html`)

L2 "split": 3D on the left, a wider answer column on the right (`size.column.desktop` + `space.48`). Use it when the 3D view and the numbers matter equally. The question it answers: *"Which robot is working on what, and is any of them near a limit?"* Same 09:54 scenario as L1: P1 KR-03 protective stop at 09:54:12, unacked; P2 KR-01 magazine low at 09:51:40, acked. Page contract, chrome, band, footer, tab bar and 3D overlay are as in [`l1-alarm.md`](l1-alarm.md); shared markup is in `andura-ui.css` / `andura-ui.js` and follows [`references/recipes.md`](../references/recipes.md).

## Zones (desktop 1600 × 1000; tablet in brackets)
| Zone | Spec |
|---|---|
| 3D viewport | from x 0 to the column gap; the band (when present) is taken from its top |
| Answer column | `size.column.desktop` + `space.48` wide [`size.column.tablet`], Void, right margin `size.margin.*` |
| Column blocks | CELL summary (`cellsum` recipe) → KR-01 / W-11 progress 78 % → MAGAZINE 14 %, LIMIT 10 % (P2 glyph) → CYCLE 4:12, TARGET 4:00 · DEV +0:12 → PATH DEV 0.18 mm, LIMIT 0.50 → ROBOTS list (bottom-aligned) |

## States
| `?state=` | What changes |
|---|---|
| `alarm` (default) | band with 2 rows; Emergency rim on KR-03, Caution rim on KR-01; status tags; progress blocks dimmed (`.dim`) |
| `normal` | no band, no rims, no status tags; ALARMS tab without badge |
| `inspect` | KR-01 selected (`sel3d`, Ultramarine 2.5 px, drawn outside its Caution rim); the column shows KR-01. **The alarms stay active:** band, both rims, tags and badge are unchanged, because selecting a robot does not clear an alarm |
| `detail` | P1 KR-03 detail in the column; acknowledge = confirm dialog (desktop, tablet) or 1500 ms hold (phone) |
| `offline` | alarms stay; KR-02 drawn dashed (`off3d`) with an OFFLINE tag; its column block greys and shows "Offline since 09:41" with AGE; band gains no extra row (offline is a system row on L1) |

## Phone 390 × 844
3D thumbnail (176 tall, no tags, also in inspect), single scrolling column, one band row with "+1 ›", tab bar with badge. In inspect the KR-01 blocks replace the cell blocks.

## Decisions
- Inspect keeps the alarm chrome (band, rims, badge): the alarm state of the cell is independent of what the operator has selected. `persist_check.py` therefore sees identical fixed chrome in alarm and inspect.
- Values with several groups (`09:51:40 · ACKED`) are `.vals` rows: they wrap between groups at 200 % rather than overflow.
