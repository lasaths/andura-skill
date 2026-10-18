---
name: andura
description: Use when designing, building or reviewing dark-mode operator UI for mission-critical 3D digital twins - HMI and SCADA screens, operator consoles, alarm screens, robot cell monitoring, BIM/digital-twin viewers, design-to-fabrication tracking and production analytics - on desktop, tablet, phone or control-room wall, on any platform (web, desktop, mobile, Unity, Three.js). Not for consumer apps, light themes or marketing pages.
version: 0.3.4-draft
license: MIT
allowed-tools: [Read, Write, Edit, Glob, Grep, Shell]
---
# ANDURA: mission-critical digital-twin UI

ANDURA is a human-factors system for supervising construction robots. Dark only. Every screen answers one question fast and never hides an abnormal state. (Credit: its monochrome, type-led, subtract-first style follows the nothing-design skill; nothing needs loading.)

**Before you design:** take every value from `tokens/andura.tokens.json` (or its exports in `tokens/build/`). Never type a hex, size or duration by hand. Start from the worked example `examples/l1-alarm.html` and its spec `examples/l1-alarm.md`. Read a `references/` file only when you need its depth. Run the checks in §7 before you hand over.

Units: **px** means device-independent pixels (CSS px, Android dp, iOS pt, WPF DIP). Durations are in **ms**.

---

## 1. Hard rules
Break none of these. If a request conflicts with one, refuse that part and say which rule blocks it.
1. **Use colour only for abnormal states.** Draw normal states in Muted and Text. Show Emergency and Caution only while their condition is active. Never show green "OK" on an overview.
2. **Give every status a colour, a glyph and a word.** P1 = octagon `!` EMERGENCY. P2 = triangle `!` CAUTION. P3 = circle `i` ADVISORY. Stale = dashed circle STALE. This includes glyph badges and cell summaries (e.g. `P1 · Partly stopped`).
3. **Never hide a status.** Selection, occlusion, LOD, tooltips and staleness must not cover it. For a selected object in alarm, draw the Ultramarine outline outside and the status rim inside. Phone "+n" is allowed; the ALARMS tab badge shows the highest priority plus the count (`P1 · 2`).
4. **Pair every live value with its unit and its limit.** Show data age once per stream in the top line, and next to a value only when it is stale. Write deviation as `DEV` in labels too (`PATH DEV`), never spelled out. Never use the Greek delta (Plex Mono has no glyph for it).
5. **Use locked tokens only:** palette v2.2, IBM Plex Sans and Mono, weights 400 and 500, at most 6 distinct type tokens per screen class.
6. **Keep the persistent zones fixed.** The top line, the alarm band and the footer or tab bar are pixel-identical across states and layouts.
7. **Make every touch target at least 56 × 56 px, 8 px apart,** on every touch screen. Keep all text at 12 px or larger. Desktop is pointer-first; treat any touch-capable display as tablet.
8. **Never send a robot command from a navigation gesture.** Commands (pause, resume, acknowledge, reset) live only in labelled buttons. On desktop and tablet, every command needs a confirm step. On phone, every command needs a 1500 ms press-and-hold.
9. **Animate opacity only, and only to carry meaning.** The only loop is the P1 pulse (1 Hz), and it stops on acknowledge. Never exceed 3 flashes per second.
10. **Treat the E-stop as physical only.** Show its state. Never draw a software E-STOP button.

---

## 2. The 13 rules
1. **One question per view.** Write the question at the top of the spec. Move anything that does not answer it down a level.
2. **Grey when normal, colour when abnormal.** In normal state, use at most one accent: the commanded path.
3. **Hide normal, annunciate the exception.** No RUNNING chips, zero counts or empty alarm glyphs.
4. **Keep to the budget.** At most 5 numeric values and 1 display-size value per screen. At most 3 value callouts in 3D (1 in normal state). Limits, DEV, units, clock, data age and alarm-band text do not count.
5. **Show deviation against a limit, not raw readings.** `0.42 mm … LIMIT 0.50 mm`, `ETA 10:21 · +2 min`. Collapse in-range parameters into "others in range".
6. **Use whitespace before lines and lines before boxes.** No panel frames on overviews. Keep groups at least 32 px apart.
7. **Label a value only when it is ambiguous.** Units are Muted.
8. **Show trends as sparklines.** Frameless, one dashed limit line, value-to-limit scale, end dot. The end dot never uses an alarm hue; the value text carries the alarm.
9. **Disclose progressively, with obvious exits.** Peek, inspect and drill are each one action away, with a named back control.
10. **Keep one fixed zone for always-on facts.** The top line holds identity, control owner, data age and clock. Nothing else.
11. **Never hide a status** (hard rule 3), in 2D and 3D. Draw occluded alarmed objects as an x-ray outline and off-screen alarms as an edge chip.
12. **An alarm shifts the hierarchy, never the layout.** The alarm goes to the band and the 3D rim. Routine values dim to 55 % opacity. Nothing moves. The camera moves only on a user action.
13. **Motion means something.** Opacity fades only. `motion.duration.*`: instant 0 ms, fast 120 ms, fast-out 80 ms, base 200 ms, slow 400 ms, camera 300 ms, hold 1500 ms, toast 4000 ms, pulse 1000 ms, peek-delay 300 ms, long-press 500 ms. See `references/motion.md`.

When two rules conflict, the lower-numbered hard rule wins, then the lower-numbered rule. Sources and audits: `references/principles.md`, `references/research.md`.

---

## 3. Colour (palette v2.2, locked; `color.*` tokens; `assets/swatch-v2.2.png`)
| Token | Hex | Role | vs Void / vs Surface |
|---|---|---|---|
| Void | `#000000` | canvas | — |
| Surface | `#090A0C` | the only raised layer (3D viewport, band, popovers) | 1.06 / — |
| Surface Hover | `#141518` | hover lift on rows and cards (never the only signifier) | 1.15 / — |
| Surface Lift | `#1A1B1E` | active tool, toast background | 1.22 / — |
| Line | `#3C3D41` | hairlines, grid, separators (never text) | 1.94 / 1.83 |
| Muted | `#8A8C91` | labels, units, secondary text, stale | 6.24 / 5.89 |
| Text | `#DADADD` | values, primary text, focus ring | 15.05 / 14.20 |
| Ultramarine | `#3A3CFF` | selection, commanded path, primary button fill | 3.27 / 3.08 |
| Ultramarine Text | `#5A74F1` | accent text and links only | 5.20 / 4.91 |
| Emergency | `#F45536` | P1 only | 6.20 / 5.85 |
| Caution | `#FBB636` | P2 only | 11.85 / 11.17 |
| Nominal | `#44B782` | explicit confirmation on detail levels only | 8.34 / 7.87 |
| Data scale (cividis) | `#163770 #47516C #696B71 #8B8778 #AFA471 #D7C45C #FEE838` | magnitudes only (heatmaps, abs DEV) | — |

- **Dialog:** Surface fill + 1 px Line border; scrim Void at `opacity.scrim` (0.6). Dimmed routine values: `opacity.dim` (0.55).
- **Focus ring:** 2 px Text, 2 px gap outside the target. Never use Ultramarine for focus.
- **Strokes:** accent strokes 2 px minimum. 3D selection outline 2.5 px. Commanded path dashed 3 px. 3D outlines, rims and paths keep a constant on-screen width at any zoom or thumbnail scale (SVG `vector-effect: non-scaling-stroke`, screen-space lines in engines), never under 2 px.
- Put colour on the value or the glyph, never on a row background. Never use alarm hues for data, decoration or brand.
- 3D model greys: `color.3d.*` tokens. Depth: `references/colour.md`.

---

## 4. Type (IBM Plex, locked; `type.*` tokens; `assets/type-scale-v2.png`)
| Token | Font / weight | Colour | Desktop | Tablet | Phone | Wall |
|---|---|---|---|---|---|---|
| display | Mono 400 | Text | 64/64 | 72/72 | 40/44 | 320/320 |
| value-l | Mono 400 | Text | 36/40 | 40/48 | 28/32 | 176/192 |
| value-m | Mono 400 | Text | 22/28 | 24/32 | 22/28 | 112/136 |
| h1 | Sans 500 | Muted | 22/28 | 24/32 | 18/24 | 112/136 |
| title | Sans 500 | Text | 18/24 | 20/28 | 18/24 | 88/112 |
| body | Sans 400 | Text / Muted | 15/20 | 16/24 | 15/20 | 72/92 |
| label | Mono 500 CAPS +0.08em | Muted | 12/16 | 13/16 | 12/16 | 56/64 |

- Set numbers, IDs and labels in Mono with tabular figures and slashed zero. Set text in Sans.
- Use one h1 (Muted) and one display value per screen, and one title per panel. A hero unit uses value-m; with no hero, units take the size of their value's row (body).
- At most 6 distinct type tokens per screen class (`touch_check.py` counts sizes).
- Values must outrank headings when the screen is blurred. If a heading outweighs a value, shrink the heading.
- Depth: `references/typography.md`.

---

## 5. Layout (`size.*`, `space.*`, `breakpoint.*` tokens)
**Grid:** 8 px. Use 4 px only inside components. Spacing steps: 8, 16, 24, 32, 48.

| Class | Min width | Canvas | Margin | Top line | Alarm band | Footer |
|---|---|---|---|---|---|---|
| Phone | 0 | 390 × 844 | 16 | 48 (h1 + clock) | 1 row × 64, top alarm + "+n" | tab bar 64 + 16 home zone |
| Tablet | 600 | 1180 × 820 | 24 | 56 | 2 rows × 56 | 72, 168 px slots |
| Desktop | 1280 | 1600 × 1000 | 32 | 56 | 2 rows × 48 | 72, 176 px slots |
| Wall | 2560, viewed from ≥ 3 m | 3840 × 2160 | 64 | 56 at wall scale | 2 rows, wall scale | none, read-only |

**Persistent zones** (`assets/sheet-min.png`):
- **Top line:** `ANDURA · h1 (or breadcrumb Cell C3 › KR-02 › Timeline) … CONTROL owner · DATA age · clock`.
- **Alarm band:** one row per active P1 or P2, acknowledged or not, P1 on top, at most 2 rows. Put extras into "+n". The band appears while any P1 or P2 is active and disappears when none is. Its space belongs to the content area, so nothing else moves. A P1 row has an Emergency edge bar (pulsing until acknowledged), glyph, word, message (`412 N, limit 380 N`), time, PROCEDURE and ACKNOWLEDGE.
- **Footer:** ROBOT DETAIL › · TIMELINE › · ALARM LOG › · DIAGNOSTICS › in fixed slots, then E-STOP: PHYSICAL ONLY. The active link is Text with a 2 px underline and keeps its ›. **Phone:** tab bar CELL · ROBOTS · ALARMS (P1 badge) · MORE.

**Six layout patterns** (`L1`–`L6`; hierarchy levels are `D1`–`D4`, ISA-101) (pick one by the question): L1 3D dominant · L2 split · L3 card grid · L4 analytics · L5 alarm list · L6 design-to-fab. Questions and shapes: `references/layouts.md`.

**Alarm decisions** (`references/layouts.md`): the ALARMS badge shows the highest priority + count (`P2 · 1` when only a P2 is active); cell summary `<priority> · <state>`; LIMIT is an alarm setpoint, TARGET a Muted plan value with DEV; dim routine values while a P1 is active or a P2 is unacknowledged. Phone acknowledge lives on the alarm detail screen as a 1500 ms hold.

**Reflow to phone:** `references/layouts.md` (Reflow rules), `assets/responsive-sheet.png`.

**OS text size** (WCAG 1.4.4; `text-scale.*` = 1, 1.25, 1.5, 2): follow the OS setting up to 200 %. Multiply every type size and line height by the step. Chrome that holds text grows by the same step (top line, alarm rows, band buttons, footer or tab bar, list rows); margins, grid, strokes and the 3D view do not. The answer column grows to at most half the width, wraps, and scrolls; it keeps its value budget (no extra values). Labels and messages stay on one line and truncate with an ellipsis; peek shows the full text. Values and units never truncate, wrap or clip. Targets stay at least 56 × 56 px.

---

## 6. Workflow
1. State the one question for the view and pick the layout pattern (§5).
2. Copy the persistent zones (top line, band, footer) from `examples/l1-alarm.html` unchanged. Load `tokens/build/andura.css` and `andura-fonts.css` (IBM Plex, see `references/platforms.md`).
3. Place the answer: one display value, at most 5 values, each with a limit.
4. Add exceptions in colour, glyph and word. Check rule 11.
5. Define peek, inspect and drill, and the back path (`references/interaction.md`).
6. Render desktop, tablet and phone in the alarm scenario. If the user names classes, render those plus any the checks cover. Then run §7.

---

## 7. Verify before you ship
Run from the repo root. Each script exits 0 only if every check passes, and prints each failure.
- `python3 scripts/check.py`: this file, the references and the exports match `tokens/andura.tokens.json`; contrast figures match the WCAG ratio of the token hexes; no banned or superseded value (thin weights, Sans at weight 600, old surfaces, an Ultramarine Text focus ring, old 40 px chrome, the Greek delta, a hex that is not a token); versions agree. Includes a self-test.
- `python3 scripts/touch_check.py`: every class (desktop, tablet, phone) × state (alarm, normal, inspect, detail) × text scale (100–200 %). Targets 56 × 56 px or larger on touch classes and on every class at 200 %; no overlapping targets or text; no clipped text and no truncated value; no text below 12 px; no unmarked interactive element; targets in scroll areas are scrolled into view and measured.
- `python3 scripts/persist_check.py`: on every class the top line and footer (phone: tab bar) are pixel-identical between normal and alarm, and between normal and inspect or detail apart from the exact active-slot and badge elements.

To check your own screen: `check.py --example page.html`, `touch_check.py page.html [--classes …] [--states …]` (also: 3D `.o3d` outlines ≥ 2 px on screen), `persist_check.py page.html` (states the page lacks are reported SKIP; it masks only `[aria-current]` and `.badge`). A self-contained page may inline `andura.css` (marker comment `/* andura.css */`). The page must use the `.hit` convention and the `?state=` / `?scale=` contract in `examples/l1-alarm.md`. Then check by hand:
- [ ] **5-second test:** a naive viewer states the cell status and the active task after 5 s.
- [ ] **Colour, glyph and word** on every status. Nominal green absent from overviews.
- [ ] **No hidden status** under selection, tooltip, occlusion, off-screen position or LOD.
- [ ] **Values:** unit and limit on each, consistent decimals, deviation as DEV.
- [ ] **Reduced motion:** fades instant, pulse steady, camera cuts.
- [ ] **Commands:** none reachable by a navigation gesture.

---

## References (read on demand)
| File | Read it when you need |
|---|---|
| `examples/l1-alarm.html`, `l1-alarm.md` | a working screen built only from tokens, with coordinates |
| `references/layouts.md` | L1–L6 questions and shapes, reflow rules, interaction states |
| `references/components.md` | anatomy, states and sizes for components 1–26 |
| `references/interaction.md` | peek/inspect/drill, selection, commands, accessibility, do and don't |
| `references/viewport.md` | 3D camera, navigation, encodings, labels, aids, frame budget |
| `references/motion.md` | motion tokens, behaviours, reduced motion, forbidden motion |
| `references/colour.md` · `typography.md` | palette derivation, CVD, focus vs selection · scale tests, wall sizing |
| `references/platforms.md` | consuming tokens in CSS, TS, Python, C#/WPF, Unity, Three.js |
| `references/libraries.md` | picking a component library (Radix, React Aria, WPF, Qt, …) and adapting it to the tokens |
| `references/principles.md` · `research.md` | sources and audits for the 13 rules · research brief |
| `assets/` | rendered specimens (`swatch-v2.2.png`, `sheet-min.png`, `components.png`, …) |
