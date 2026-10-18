# ANDURA — Reduction principles + L1 audit

> Provenance: paths under `layouts/` name the original design workspace and are not shipped. The renders are in `assets/`; runnable equivalents are `examples/`, `render/` and `scripts/`.

*2026-10-18. Answers the feedback "too verbose, too much information, weak hierarchy, want NASA-quality". Sources were read via web search excerpts on 2026-10-18 unless noted; paywalled standards (ISA-101, MPCV 72242) are cited via public summaries, not full text. **[DC]** = ANDURA design choice, not a sourced fact.*

## 1. Sources (what each actually says)
| # | Source | Claim used |
|---|---|---|
| S1 | Few, "Dashboard Confusion", *Intelligent Enterprise*, Mar 2004 — [PDF](https://www.perceptualedge.com/articles/ie/dashboard_confusion.pdf); repeated in [Common Pitfalls](https://www.perceptualedge.com/articles/Whitepapers/Common_Pitfalls.pdf) | Dashboard = "the most important information needed to achieve one or more objectives; consolidated and arranged on a single screen so the information can be monitored at a glance." It "need not be comprehensive", must show "when action is required" and give "an easy gateway" to detail. |
| S2 | Few, "Dashboard Design: Taking a Metaphor Too Far", 2005 — [PDF](https://www.perceptualedge.com/articles/dmreview/dashboard_design.pdf) | Gadget-like widgets are "a poor use of valuable screen space"; "the only goal is communication". |
| S3 | Few, Real-time SA dashboards — [PDF](https://www.perceptualedge.com/articles/Whitepapers/Dashboard_Design.pdf) (cited in research.md, [excerpt]) | Stable single screen, emphasis on exceptions, sparklines for projection. |
| S4 | Tufte, *The Visual Display of Quantitative Information* (data-ink, chartjunk), via [data.europa.eu guide](https://data.europa.eu/apps/data-visualisation-guide/chart-junk-and-data-ink-origins) and [Tufte's Razor](https://tuftesrazor.scienceux.org/) | Data-ink ratio = data ink / total ink; erase non-data and redundant ink "within reason" — but keep labels the reader needs. Chartjunk = decoration, heavy gridlines, "ducks". |
| S5 | Tufte, sparklines — [edwardtufte.com](https://www.edwardtufte.com/notebook/sparklines-history-by-tufte-1324-to-now/), [theory & practice](https://www.edwardtufte.com/notebook/sparkline-theory-and-practice-edward-tufte/) (*Beautiful Evidence* 46–63) | Sparklines: word-sized, "no frames, tic marks, and non-data paraphernalia"; clinical use: "detect quickly … deviations from normal limits". |
| S6 | Tufte, small multiples (VDQI p.168) via [masnick.org](https://masnick.org/projects/datatips/guidelines/small-multiples/) | Same graphic repeated, indexed by one variable, for comparison. |
| S7 | NASA, *Appendix F: Display Standard* (HIDH) — [nasa.gov](https://www.nasa.gov/reference/appendix-f-vol-2/) | F.4.1-1 "amount of information displayed should be limited to what is needed to perform required tasks or to provide situation awareness"; F.4.1-5 "directly usable form that does not require mental transposition or computation"; F.4.2-3 group elements used together; F.4.2-4 separate groupings from others "or from graphical or virtual borders"; F.4.2-6 a common dedicated area for key info always visible. |
| S8 | NASA CLDP HSI workshop, *Crew Interfaces* (2024) — [NTRS](https://ntrs.nasa.gov/api/citations/20240003566/downloads/CLD%20HSI%20Workshop%20Crew%20Interfaces.pdf) | Poor designs include "displays that contain an excessive amount of information, and appear cluttered"; Orion display format standard **MPCV 72242**; displays verified per checklist; "the cumulative effect of many small deviations raises workload". |
| S9 | NASA AES/MOSA briefing, Apr 2022 — [PDF](https://lsic.jhuapl.edu/uploadedDocs/focus-files/1657-MOSA%20Monthly%20Meeting%20-%202022%2004%20April_Presentation%20-%20NASA.pdf) | MPCV 72242 developed by Human Factors, Rapid Prototyping Lab and Cockpit Working Group. |
| S10 | NASA JSC Crew Interfaces / HF&P — [nasa.gov](https://www.nasa.gov/reference/jsc-crew-interfaces/) | JSC HE Displays & Controls: iterative user-centred design, HITL evaluation, workload assessment. |
| S11 | SpaceX Dragon UI — [InfoQ 2020](https://www.infoq.com/news/2020/06/javascript-spacex-dragon/) (research.md §2.2) | "Just a few buttons for very mission-critical operations"; minimal crew interaction as a success criterion. |
| S12 | Hollifield, "Proper HMI graphics should look BORING!" — [Control Global](https://www.controlglobal.com/visualize/hmi/article/11380785/human-machine-interface-proper-hmi-graphics-should-look-boring); [ISA HP-HMI overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf) | Normal operation looks calm/grey; colour reserved for abnormal; Level 1 = at-a-glance overview of whole span of control, not a control screen. ANSI/ISA-101.01-2015 display hierarchy L1–L4 (via [Yokogawa](https://www.yokogawa.com/us/library/resources/media-publications/isa-101-toward-a-more-effective-hmi-strategy/)). |
| S13 | ASM Consortium, "Why gray backgrounds…" — [Honeywell PDF](https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/white-papers/February%2028%202011%20-%20Why%20Gray%20Backgrounds%20for%20DCS%20Operating%20Displays.pdf) | Salience comes from contrast against a subdued background. |
| S14 | "Design Displays", *Avionics News* Oct 2003 — [AEA PDF](https://aea.net/AvionicsNews/ANArchives/DesignDisplayOct03.pdf); Airbus FAST #20 ([copy](https://idoc.tips/airbus-fbw-pdf-free.html)); [CIEHF maritime paper](https://publications.ergonomics.org.uk/uploads/Optimising-Operator-Attention-on-the-Maritime-Platform-Human-Computer-Interface-.pdf) | Quiet/dark: "information is not displayed until something goes wrong. A screen or annunciator stays black until a system condition warrants notifying the pilot." Airbus overhead: all lights out = normal. |
| S15 | Nielsen, *Progressive Disclosure*, NN/g 2006 — [nngroup.com](https://www.nngroup.com/articles/progressive-disclosure/) | Defer rare features to a secondary screen; primary level "can't contain too many options"; path to the next level must be obvious with clear labels. |
| S16 | NN/g, 5-second test — [video](https://www.nngroup.com/videos/5-second-usability-test/), [Testing Visual Design](https://www.nngroup.com/articles/testing-visual-design/); Gronier 2016, *J. Usability Studies* — [PDF](https://www.guillaumegronier.com/resources/2016_JUS_Gronier.pdf) | First-impression test: show the screen ~5 s, ask what it is about / what it says. Note: it measures impression and gist, not task performance; Gronier only partly validated it. We use it as a design check, not as a law. |
| S17 | ABB / Emerson alarm targets (research.md §2.3) | <10 alarms in 10 min after upset; standing alarms <10. |

## 2. The 13 rules (same numbering as SKILL.md)
1. **One question per view.** Write it at the top of the spec; anything that doesn't answer it moves down a level. L1 question: *"Is the cell OK, and what is the robot doing?"* (S1, S7 F.4.1-1, S12)
2. **Grey when normal. Colour = abnormal only.** Normal values in Muted/Text; Emergency/Caution appear only with an active condition; Nominal green is not used on overview screens. Max one accent use (the commanded path) in normal state. (S12, S13, S14)
3. **Hide what is normal; annunciate the exception.** No "RUNNING" chips, no empty-alarm glyphs, no zero counts. The alarm band is absent when no P1 or P2 is active; its space belongs to the content area, so nothing else moves. (S14, S3, S1 "when action is required")
4. **Budget: ≤ 5 numeric values and ≤ 1 display-size value per screen; ≤ 3 3D callouts (normal: 1).** [DC, derived from S7 F.4.1-1, S8 "excessive amount of information", S11 "just a few"]
5. **Show deviation against limit, not raw readings.** A value earns its place only with its limit or plan next to it (0.42 / LIMIT 0.50; ETA +2 min). Four in-range parameters collapse into one sentence: "other parameters in range". (S7 F.4.1-5 no mental computation, S5 deviation from normal limits)
6. **Whitespace before lines, lines before boxes.** No panel frames on the overview; groups separated by ≥ 32 px space. Hairlines only in tables. (S7 F.4.2-4 "virtual borders", S4 non-data ink)
7. **Labels only when the value is ambiguous.** No legends that repeat meaning already carried by position; units in Muted; no breadcrumbs/level meta on L1. (S4 redundant ink — but keep needed labels, Tufte's Razor caveat)
8. **Trends as sparklines, not charts.** Frameless, word-sized, one limit line, no axes. (S5)
9. **Progressive disclosure with obvious exits.** Every removed item lives one action away behind a named link (ROBOT DETAIL ›, TIMELINE ›, ALARM LOG ›, DIAGNOSTICS ›). (S15, S1 "easy gateway", S12 L1→L4)
10. **Fixed dedicated zone for always-on facts, and only those.** Top line: cell name, control owner, data age, clock. Everything else is earned. (S7 F.4.2-6, S7 F.4.2-2 consistent positions)
11. **Status is never hidden.** Not by selection (Ultramarine outside, status rim inside, plus glyph and word), not by occlusion (x-ray), not off-screen (edge chip), not by LOD or staleness. Interaction states layer on top and never replace a status.
12. **Alarm shifts hierarchy; layout stays; the camera never moves on its own.** In alarm, alarm text goes to the band and the 3D rim, routine values dim (≈55 % opacity), nothing moves. The camera moves only on a user action; explicit zoom-to-alarm is a cut. (S12, S8, S17)
13. **Motion = fades for meaning.** Tokens in `motion.md`; one loop only (P1 pulse 1 Hz, stops on ack); ≤ 3 flashes/s.

Pre-ship check (not a rule): show the screen 5 s; a naive viewer must state cell status and the active robot task. If not, cut again. (S16)

## 3. L1-min design (files `layouts/L1-min.png`, `L1-min-alarm.png`, `L1-compare.png`; source `layouts/src/L1min.py`, `compare.py`)
- **Grid:** top line 56 px · 3D full-bleed 1120 × 872 on Surface, no frame · answer column 432 px on Void, whitespace-separated · footer 72 px of drill-down links.
- **Reading order** (left-to-right, top-to-bottom, S7 F.4.2-1): cell name → CELL state word → robot progress (display 64) → ETA delta → one deviation vs limit + sparkline → robots list.
- **Normal:** no colour except the dashed Ultramarine commanded path. "Running · 3 robots · no alarms" is plain text, not a green chip (S14: normal is quiet).
- **Alarm:** a 96 px band appears over the empty top of the 3D (reserved space, no reflow): P1 line (6 px Emergency edge, octagon, message with value vs limit, PROCEDURE, ACKNOWLEDGE) and a quieter P2 line (triangle, Muted text, ACKED time). The cell word becomes "Partly stopped" with glyph; robots KR-03/KR-01 get rims + one callout each; the KR-02 values dim to 55 % so the eye goes to the alarm. Colour + glyph + word everywhere (C, R §3.1).
- **Typography:** only existing tokens (h1, label, body, value-l, display). Palette v2.2 only.


## UX heuristics audit (L1-min states, 2026-10-18)
| Principle | How it's met | Gap / follow-up |
|---|---|---|
| Nielsen 1 · Visibility of system status | DATA age + clock always in the top line; tooltip shows timestamp + age; alarm band; NOW line on the timeline; stale state drawn (`L1-min-stale.png`: Muted value, hatched trace, stale glyph + STALE + AGE 12 s + last good time) | — |
| Nielsen 4 · Consistency | One shared top line/footer, one value/limit format, one sparkline scale, Ultramarine = selection only; pixel-diff verified | — |
| Nielsen 5 · Error prevention | Navigation never commands; commands are labelled buttons with 2-step confirm; peek long-press ≠ command press-and-hold | — |
| Nielsen 6 · Recognition over recall | Back names its destination; breadcrumb; limits printed next to values; legend on the timeline | — |
| Nielsen 3 · User control / undo | Esc / ‹ Back / crumb go up one step; peek closes on leave/release; selection never steals by alarm | No undo for ACK (by design; ACK has confirm) |
| Fitts's law | Back 56 px tall hit area at a fixed spot; footer slots 176 × 72; alarm buttons 40 px desktop | Closed: tablet variant `L1-min-touch.png` has 56 px ROBOTS rows with a › signifier (desktop stays 32 px) |
| Hick's law | Max 4 footer links + 1 back per screen; inspect shows 3 parameters, 3 events | — |
| Gestalt proximity / similarity / alignment | Label→value 8 px, block gaps 48 px; one left edge per column; tooltip shares the tag's left edge; same type token = same role | — |
| Visual hierarchy, F/Z scan | h1 top-left (Muted), status then hero value down the right column; values (display/value-l/value-m) outrank labels | — |
| Affordance & signifiers | › on every link, ESC keycap, pointer notch on the tooltip, underline on the active link | Closed: hover drawn in `L1-min-focus.png` (TIMELINE › turns Text, no underline, so hover ≠ active) |
| Feedback for every action | Hover → tooltip 120 ms; click → outline + column 200 ms; active link underlined; ack 0.1 s confirm | — |
| WCAG contrast | Text 15:1, Muted 6.2:1 on Void, all text ≥ 4.5:1; Line #3c3d41 used only for non-text separators | — |
| WCAG focus | Spec: 2 px Text focus ring, 2 px offset, on back, links, ROBOTS rows, buttons (keyboard order: top line → column → footer) | Closed: 2 px Text #DADADD ring, 2 px gap, on the L1 robot row, an L3 card and an L5 row (colour.md amendment: 15:1, satisfies WCAG 2.4.13; clearly unlike the Ultramarine selection) |
| WCAG not colour alone | Alarms = glyph shape + word + colour; selection = outline + square glyph; active link = underline; exceedances = ▼ | — |

## UX heuristics audit · L2-min … L6-min (2026-10-18)
Shared by all five (verified by `layouts/src/persist_check.py`, 0 px diff vs L1-min / L1-min-alarm): top line (excl. h1), footer (excl. active slot), alarm band (one spec: 48 px per active P1/P2 row, max 2 rows, same 09:54 scenario on every layout), statuses = colour + glyph + word, normal = Muted word without glyph, locked tokens only, 8 px grid, primary targets ≥ 56 px.
| Layout | Question | Met | Gap |
|---|---|---|---|
| L2-min split | What is this robot doing, and how close to its limits? | One display value (78 %), 3 value/limit rows with the shared sparkline; caution = glyph + CAUTION + word; 3D left full-bleed | Closed: selected + caution draws Ultramarine outer outline with a Caution rim inside, plus the glyph tag (rule: status is never hidden by selection) |
| L3-min card grid | Is the hall on plan, and where is the exception? | 6 cards, no borders, label + one answer + one drill link (Hick ≤ 6); rows 56 px; 3D thumbnail matches the alarms | Closed: whole card is the target (focus ring drawn on THROUGHPUT); peek on a robot row in `L3-min-peek` |
| L4-min analytics | Is the week on plan, and what costs most? | Hero 412 m² vs plan, one bar chart with dashed plan line and printed values, top-3 downtime ranking | Closed: below-plan bars carry "−18 vs plan"; peek on a bar in `L4-min-peek` |
| L5-min alarm list | What needs me first? | First-out on top, 56 px rows, priority word + glyph + colour, UNACK in Text; detail with value/limit, 3 steps, 56 px buttons, confirm note | Closed: the band is now on L5 too (one rule everywhere); flood grouping by cell drawn with first-out, rate and ACK GROUP; focus ring on a row; `L5-min-inspect` moves the selection to the P2 row |
| L6-min graph | Which design changes have not reached the robot? | Elements × stages matrix; only exceptions coloured (glyph + word); stale = dashed box + stale glyph + NO FILE; back with ESC; selection Ultramarine | Nominal "Done/Pass" has no glyph by design (principle 2); edge semantics (data flow) only implied by lines |

**Tablet variants** (`L2…L6-min-touch.png`, `L1-min-touch.png`): every interactive element carries a `hit` class. The tablet render draws each one as a dashed 56 px minimum hit area. Remaining risk: hit areas are checked visually, not measured.

## 3D viewport + motion audit (2026-10-18, `viewport.md`, `motion.md`)
Covered by rules 11 and 12.
Covered by rule 13.
| Principle | How it's met (3D + motion) | Gap |
|---|---|---|
| Nielsen 1 · Visibility of system status | View-mode indicator always visible (projection, follow, layers, section); stale pose hatched with age; "3D REDUCED / PAUSED" label | — |
| Nielsen 3 · User control / undo | HOME (H) resets; camera history (Backspace, 20 steps); Esc ends section/measure/follow; HIDE shows a SHOW ALL chip | Camera history not rendered |
| Nielsen 4 · Consistency | Same home view on every device; selection/status/hover encodings identical in 2D and 3D; action bar in a fixed place | — |
| Nielsen 5 · Error prevention | No roll, clamped elevation and target; navigation never commands; follow ends on any manual move | — |
| Nielsen 6 · Recognition over recall | View cube with named faces; every tool labelled with its key; tooltips; first-use gesture legend (? reopens) | — |
| Fitts's law | FIT and ZOOM TO ALARM bring targets to the user; tools 40 px D, 56 px touch; action bar at a fixed bottom-centre spot | Rail at the far right edge of wide screens; keyboard keys compensate |
| Hick's law | 8 rail tools, 4 layers, 4 context actions; phone folds aids into one sheet | — |
| Feedback | Hover outline, selection outline, tool active fill, measure readout, toast after ack; all ≤ 0.1 s | — |
| Gestalt / hierarchy | Grey model, quiet grid, colour only for status; max 5 tags + "+n" | Label collision avoidance is spec only |
| WCAG not colour alone | Status = rim + glyph + word; selection = outline + square glyph; commanded = dashed vs solid | — |
| WCAG 2.3.1 / 2.3.3 (motion) | Only the 1 Hz P1 pulse loops; reduced motion turns fades instant and the pulse into a steady chip | — |
| Performance | 30 fps floor; fixed degrade order; status layers never degraded | Unprofiled on real hardware |
