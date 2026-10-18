# Worked example: L3 card grid (`l3-cards.html`)

L3 "card grid": up to 3 × 2 borderless cards, each answering one question with one drill link. Use it for an overview screen (shift lead, line overview) where no single view dominates. Question: *"Is the cell on track today, and what needs me?"* Same 09:54 scenario as L1 (P1 KR-03 09:54:12 unacked; P2 KR-01 09:51:40 acked). Contract and chrome as in [`l1-alarm.md`](l1-alarm.md); markup follows [`references/recipes.md`](../references/recipes.md).

## Cards (reading order)
| Card | Content | Recipe |
|---|---|---|
| 3D · CELL C3 | the whole viewport is one `.hit`, opening the L1 3D screen; rims and status tags as in L1 | tag |
| THROUGHPUT · TODAY | 286 m², TARGET 296 m² · DEV −10, TRENDS › | kpi |
| ALARMS | P1 and P2 rows (alarm only), each opening the detail; "No active alarms" in normal | alarm row (list form) |
| CELL | cell summary + ROBOTS list | cellsum |
| STUD STOCK · RACK B | 380 pcs, LIMIT 120 · ~2 h, MATERIALS › | kpi |
| DESIGN | W-12 · rev C released, IFC 2026-10-17 14:02 · M. Keller, OPEN DESIGN › | — |

Gaps: `--gap` between cards (desktop `space.48`, tablet `space.32`); no card borders or fills (the Void/Surface rule holds; only the 3D card is Surface).

## Grid
`repeat(auto-fill, minmax(min(100%, column × scale), 1fr))` with rows `minmax(min-content, 1fr)`: three columns at 100 % on desktop, fewer when the text scale or the open detail pane narrows the content. The main area scrolls; the 3D card's height is capped to what fits between the chrome, so its target can always be seen whole. On desktop (≥ 1280, 100 %, no pane) a 12-column grid places the 3D card across 8 columns with ALARMS beside it (4), and the other cards 3 each, which removes the empty areas a 3-column auto grid left.

## States
| `?state=` | What changes |
|---|---|
| `alarm` (default) | band; alarm rows in the ALARMS card; KPI and design cards dimmed; rims and tags in the 3D card |
| `normal` | no band, no rims, "No active alarms" |
| `inspect` | not defined for a card grid (selection lives on the screen the card opens): renders as normal, `persist_check.py` reports SKIP |
| `detail` | P1 KR-03 detail opens as a right column (`aside.pane`) beside the grid |
| `empty` | startup before first data: KPIs show `—` + WAITING FOR DATA, the ALARMS card "No data yet · alarm state unknown", cell summary "Connecting · no data yet"; no tags, no lists, no sparklines, no digits (`touch_check` fails on any) |

## Phone 390 × 844
Single stack in card order, no 3D card (the thumbnail would not answer a question here); in detail the pane replaces the stack.

## Decisions
- Large empty areas on a 1600 px desktop are accepted: equal rows keep every card's drill link at a predictable place.
- No inspect state: a grid has nothing to select.
