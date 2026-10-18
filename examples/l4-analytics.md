# Worked example: L4 analytics (`l4-analytics.html`)

L4 "analytics": one hero number against plan, one chart, one ranked list. Use it for the review question after or during a shift. Question: *"How did this week go against plan, and what cost the most time?"* Same 09:54 scenario (the band stays: live alarms outrank analysis). Contract and chrome as in [`l1-alarm.md`](l1-alarm.md); markup follows [`references/recipes.md`](../references/recipes.md).

## Zones
| Zone | Spec |
|---|---|
| Left column | hero KPI: THROUGHPUT · THIS WEEK 412 m², TARGET 440 m² · DEV −28 (`kpi` recipe, `display`); below it TOP DOWNTIME · THIS WEEK: KR-03 protective stops 0:14 h, KR-01 magazine refills 0:09 h, W-12 fixture changes 0:06 h (glyphs on the alarm-related rows while the alarm is active) |
| Chart | M² PER DAY · PLAN 110 m² (DASHED). One HTML bar per day (MON 96, TUE 72, WED 101, THU 143), scale 0–160. Bars Line, plan = dashed Muted line drawn in the same track as each bar, so it lines up with the bar heights. Days below plan carry "−N vs plan" above the bar; exact values on peek (`title`). Every bar is one `.hit` |
| Footer | TIMELINE › is the active slot (`aria-current`); phone: MORE tab |

## Layout
Flex-wrap, not breakpoints: the left column (`flex: 1 1 column × scale`) and the chart (`flex: 2 1 column × scale`, so tablet keeps it beside the list at full height) sit side by side and the chart drops below as soon as the content gets narrow (tablet, open pane, 150–200 %). Chart height = viewport minus 5 × `size.touch-min` × scale, so a bar target always fits on screen. Below it: a cycle-time trend with limit band and a cycle-time histogram (`references/charts.md`).

## States
| `?state=` | What changes |
|---|---|
| `alarm` (default) | band, badge, glyphs in the downtime list; hero and chart dimmed |
| `normal` | no band, no glyphs |
| `inspect` | not defined (renders as normal, SKIP) |
| `detail` | P1 detail as a right pane; the content reflows (flex-wrap) beside it |
| `stale` | MES feed late: hero, chart, trend and histogram take `.stale` (Muted) with age chips "MES · AGE 12:40"; alarms stay |

## Phone 390 × 844
Hero, then horizontal bars (day label right, "−N vs plan" left, plan = a vertical Muted tick in the track), then the downtime list. Each bar row is ≥ 56 px × scale.

## Decisions
- No chart library: four HTML bars meet every rule (tokens only, touch targets, peek). Phase B will add chart rules for real libraries.
- Only below-plan deltas are labelled; on-plan or above-plan days carry no text (exception-only, rule 2).
