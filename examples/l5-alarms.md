# Worked example: L5 alarm list + detail (`l5-alarms.html`)

L5 "alarm list + detail": first-out alarm list on the left, the selected alarm's detail on the right. It is the screen behind ALARM LOG and the ALARMS tab. Question: *"Which alarm came first, and what do I do about it?"* Same 09:54 scenario. **No alarm band:** the list is the alarm view (`references/layouts.md`, L5), so the band's content would only repeat it; top line, footer and tab badge stay. Contract and chrome as in [`l1-alarm.md`](l1-alarm.md); markup follows [`references/recipes.md`](../references/recipes.md).

## Zones
| Zone | Spec |
|---|---|
| List | CELL C3 · 2 ACTIVE · FIRST OUT FIRST; P1 KR-03 protective stop 09:54:12 · UNACK; P2 KR-01 magazine low 09:51:40 · ACKED (rows `list-row` × scale, the selected row has a `stroke-accent` Ultramarine left border); then CLEARED · LAST 2 H in Muted |
| Detail pane | `aside.pane`, column width: the alarm detail (cause, values vs limit, PROCEDURE, acknowledge) of the selected row |
| Footer / tabs | ALARM LOG › and the ALARMS tab are active in every state |

## States
| `?state=` | Selected | Pane |
|---|---|---|
| `alarm` (default) | P1 | P1 detail with acknowledge |
| `normal` | — | no active alarms; cleared list only, pane hidden |
| `inspect` | P2 | P2 detail: magazine 14 %, LIMIT 10 %, PROCEDURE SP-031, 09:51:40 · ACKED / 09:52 · M. KELLER. The badge stays (the P1 is still active) |
| `detail` | P1 | as alarm (the phone shows the detail screen) |
| `flood` | P1 | a flood block (ALARM FLOOD · 23 IN 10 MIN · LIMIT 10 / 10 MIN, ISA-18.2) above the list; SUPPRESSED BY DESIGN · 6; SHELVED · 15 with time left and who shelved; cleared items hidden |

## Phone 390 × 844
alarm/normal: the list (pane hidden). inspect/detail: the detail screen replaces the list, ‹ ALL ALARMS returns. Acknowledge is the 1500 ms hold.

## Decisions
- No band on L5, as specified in `layouts.md`; the phone band's "+1 ›" on every other layout opens this screen. `persist_check.py` still guards the top line and footer.
- Ack state is text (UNACK / ACKED + who and when), not colour.
