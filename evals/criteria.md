# Pass criteria (scored by `evals/score.py`)

An eval run **passes** only if every automatic criterion passes. The manual criteria are recorded with the run but do not gate it.

## Automatic (score.py)
| # | Criterion | How it is checked |
|---|---|---|
| A1 | All ANDURA checks pass | `scripts/andura_check.py <page>`: check.py --example (tokens only, recipes without drift, canonical glyphs), touch_check (every class × state × scale), persist_check |
| A2 | Layout declared | a comment naming one of L1–L6 in the first 2 KB of the file |
| A3 | Scenario shown | the text contains KR-03, 09:54:12, KR-01, 09:51:40, P1, P2 |
| A4 | The question is answered with values and limits | the text contains SAW-1, 11:40, 14:00, 46, 20, 71, 85, 1:38 and LIMIT and TARGET |
| A5 | Recipes used | the alarm band uses the alarm-row recipe (≥ 2 rows: `.r.p1`, `.r.p2`); the tab bar uses the tabs recipe; the P1 detail has the hold recipe (phone acknowledge) and the dialog recipe (desktop/tablet) |
| A6 | States differ | the alarm and normal renders of the desktop canvas are not identical, and detail differs from alarm |

## Manual (record in the run report)
- **5-second test:** a viewer states the station status ("queue runs out at 11:40, before shift end") after 5 s.
- **Exception only:** the queue shortfall reads as the exception; nominal items (stock, blade) stay quiet.
- **Values:** unit and limit on each; DEV for the cycle time.
