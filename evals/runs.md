# Eval runs

| Date | Skill | Agent | Result | Notes |
|---|---|---|---|---|
| 2026-10-18 | 0.4.0-draft | Grok Bot executor (same session that wrote 0.4.0, so not fully cold) | attempt 1 FAIL (A1), attempt 3 PASS 6/6 | Chose L2 starting from `l2-split.html`. Attempt 1: hero written as a bare `display` row (text overlap with the TARGET line on every class) and "LIMIT 20 pcs · ~2:10 h" as one value (overflow on phone at 200 %). Attempt 2: KPI recipe + `.vals` fixed both, but the group "TARGET 14:00 (SHIFT END)" was still wider than the phone column at 200 %. Skill fix: recipes.md now says the hero is the KPI recipe and value groups stay short. Manual: 5-second test, "queue runs out 11:40" is the display value; stock and blade quiet; DEV on cycle. |
