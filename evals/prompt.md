# Eval prompt: SAW-1 cutting station (fixed; do not edit between runs)

Give this text, unchanged, to a fresh agent that has this repository and has not seen the run before. The agent may read anything in the repo.

---

You are designing an operator screen with the ANDURA skill (`SKILL.md` in this repository). Follow the skill exactly.

**Screen:** the cutting station SAW-1 in Cell C3 (wall panel line). **Question it must answer:** "Will SAW-1 run out of work or of material before the shift ends at 14:00?"

**Data at 09:56:**
- Cut queue: 7 parts left for elements W-13 and W-14; queue covers until 11:40 at the current pace (TARGET: covers to 14:00).
- Timber stock at the infeed: 46 pcs, LIMIT 20 pcs; about 2 h 10 min left.
- Blade wear 71 %, LIMIT 85 %.
- Cycle time per part 1:38, TARGET 1:30 (DEV +0:08).
- The same cell alarms as the worked examples are active: P1 KR-03 protective stop at 09:54:12, not acknowledged; P2 KR-01 nailer magazine low at 09:51:40, acknowledged.

**Deliver** one HTML file at `evals/out/saw1.html` that:
- picks one of the layout patterns L1–L6 and says which in a comment at the top of the file;
- links `../../tokens/build/andura.css`, `../../tokens/build/andura-fonts.css` and, if you use them, `../../examples/andura-ui.css` and `../../examples/andura-ui.js`;
- supports `?state=alarm` (default), `normal` and `detail` (the P1 alarm detail with its acknowledge), and `?scale=`;
- works on desktop, tablet and phone;
- passes `python3 scripts/andura_check.py evals/out/saw1.html`.

Report the layout you chose, why, and the check output.
