# Worked example: L6 design-to-fab (`l6-design-fab.html`)

L6 "design-to-fab": the elements (W-10 … W-14) against the production stages (DESIGN, CUT, FRAME, NAIL). Use it where design data meets the shop floor. Question: *"Which element is held up, at which stage, and why?"* Same 09:54 scenario: W-13 is held at NAIL by the P1 (KR-03 stopped), W-11 by the P2 (magazine low). Contract and chrome as in [`l1-alarm.md`](l1-alarm.md); markup follows [`references/recipes.md`](../references/recipes.md).

## Matrix
Grid rows: ELEMENT (min-content) + 4 stages (`1.5fr`, min-content). Each cell is one `a.hit.cellm` (`list-row` × scale tall). Done stages read DONE and waiting ones —, both `label` Muted; only exceptions carry colour or a glyph:
| Cell | Content |
|---|---|
| W-11 NAIL | alarm: P2 glyph + P2 · MAG LOW; normal: KR-01 · 88 % |
| W-12 NAIL | KR-02 · 63 % (in work, Text) |
| W-13 NAIL | alarm: P1 glyph + P1 · STOPPED; normal: KR-03 · 40 % |
| W-14 FRAME | IN PROGRESS; NAIL waits (—) |

## States
| `?state=` | What changes |
|---|---|
| `alarm` (default) | band, badge, P1/P2 cells with glyphs |
| `normal` | no band; the held cells show their robot and progress instead |
| `inspect` | W-12 selected (Ultramarine left border on its row); pane shows its 4-stage record (DESIGN REV C · 10-17 14:02 … NAIL KR-02 · 63 % · ETA 10:21); ROBOT DETAIL › active. Like L1 inspect, no band |
| `detail` | P1 detail in the pane |
| `comms` | MES link lost: the matrix and Gantt grey (`.stale`) with "LAST DATA 09:55:18 · AGE 0:42"; nothing is shown as live |

Below the note: a fabrication Gantt for W-11–W-14 (06:00–14:00, NOW 09:56; stages in cividis, held edges in the alarm hue only; `references/charts.md`).

## Narrow content and phone
A container query on the matrix (`@container (max-width: 599px)`, the tablet breakpoint − 1) switches to the phone form whenever the content is narrow, also when the pane is open on tablet or the text is at 150–200 %: one row per element still in work, showing only its active stage; done rows hidden. On phone inspect the record replaces the list.

## Decisions
- `check.py` accepts breakpoint tokens in `@container` as in `@media`; a container query is the honest tool for "the pane took the width".
- Stage records split into `.vals` groups so they wrap at 200 % instead of overflowing.
