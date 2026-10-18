# Fresh-agent eval

Does a fresh agent, given only this repository, produce a screen that follows ANDURA? This eval needs an agent, so CI does not run it; CI runs `scripts/andura_check.py` on the shipped examples instead.

| File | What it is |
|---|---|
| [`prompt.md`](prompt.md) | the fixed task (SAW-1 cutting station, a screen that is not one of the examples). Do not edit it between runs, or results stop being comparable |
| [`criteria.md`](criteria.md) | pass criteria: A1–A6 automatic, three manual |
| [`score.py`](score.py) | scores a produced page against A1–A6; exit 0 = pass |
| `out/` | where the agent writes `saw1.html` (not committed) |
| [`runs.md`](runs.md) | one line per run: date, skill version, agent, result, notes |

## Run it
1. Start a fresh agent session (no memory of earlier runs) with this repository checked out as its working directory.
2. Paste the part of `prompt.md` between the two rules as the first message. Do not help it.
3. When it is done, from the repo root: `python3 evals/score.py evals/out/saw1.html` (needs Chrome and Pillow, like the checks).
4. Look at the page in a browser in each state (`?state=alarm|normal|detail`) on the three canvases and record the manual criteria.
5. Append a line to `runs.md`. A failing criterion is a defect in the skill (unclear rule, missing recipe), not only in the agent: fix the skill and run again.
