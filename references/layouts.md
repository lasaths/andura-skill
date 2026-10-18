# ANDURA — Layout guidelines (locked)

> Provenance: paths under `layouts/` name the original design workspace and are not shipped. The renders are in `assets/`; runnable equivalents are `examples/`, `render/` and `scripts/`.

Six generic layouts (L1–L6) for dark-UI 3D digital-twin dashboards in robotic construction, each in desktop (`L*-min`), tablet (`L*-tab`) and phone (`L*-phone`) form. Built on `research.md` (R §x), `colour.md` (C) and `typography.md` (T). Worked examples: `examples/l1-alarm` … `l6-design-fab` (html + md); check with `scripts/andura_check.py`.

**Citation key.** *(R §n)* = research.md section. *(C)* = colour.md. *(T)* = typography.md. **[DC]** = my own design choice, not taken from a source.

---
## 0. Shared foundations

### 0.0 Header
Header height `size.header.*`: desktop 72, tablet 72, phone 64 (≥ `size.touch-min`, 8 px grid). Left: ANDURA mark (`size.logo` 32, Text, `assets/andura-mark.svg`), then an optional client/app logo slot (same height, max 4 × wide), then the h1. Right: CONTROL owner, DATA age, clock. Content starts at `size.content-top` (192). Markup: `recipes.md` §0.

### 0.1 Tokens used everywhere
| Role | Value |
|---|---|
| Canvas | Void `#000000`, only behind panels. Anything that scrolls, pans or animates sits on Surface (C §OLED smearing) |
| Panel | Surface `#090A0C` + 1px Line `#3C3D41` hairline (C v2.2: darker Surface, Line 1.94:1 on Void / 1.83:1 on Surface). **No shadows** (shadows do nothing on black; C) |
| Text / Muted | `#DADADD` / `#8A8C91` |
| Accent | Ultramarine `#3A3CFF` for fills, outlines, selection, commanded paths and primary buttons. Ultramarine Text `#5A74F1` for accent text and links only. Focus = 2 px Text ring, 2 px gap (C §6) |
| Status | Emergency `#F45536` (octagon + "P1 EMERG"), Caution `#FBB636` (triangle + "P2 CAUT"), Advisory = Text + (i) circle + "P3 ADV", Nominal `#44B782` check, **only** for completed or verified. Stale = Muted + diagonal Line hatch + dashed glyph + age. Status is always **colour + glyph + word** (R §3.1, C) |
| Type | h1 22 Sans 500 Muted (once per screen) · h2/title 18 Sans 500 · body 15 · label/h3 12 Mono 500 caps +0.08em · value-m 22 · value-l 36 · display 64 (max 1 per screen) (T) |

### 0.2 Locked chrome and spacing
- Spacing steps 8 / 16 / 24 / 32 / 48 (4 only inside components). All layout dimensions are multiples of 8. Margins 32 desktop / 24 tablet / 16 phone. Breakpoints and chrome per class: see *Breakpoints* below.
- Desktop chrome: header 72 · alarm band 48 per row, max 2 rows · footer 72 with 176 px slots. Content starts at y = 192.
- Touch targets 56 × 56 px minimum, ≥ 8 px apart, on every touch screen. Mouse buttons 32 px (40 in the alarm band). Rows 32 desktop / 56 tablet / 64 phone.
- Panels: Surface + 1 px Line hairline, no shadows, blur or gradients. Whitespace before lines.
- E-stop is physical. The UI mirrors its state and never draws an E-STOP button.

### 0.6 Drill-down levels D1–D4 (R §3.2, ISA-101 Level 1–4)
**Naming:** `L1`–`L6` always mean the six layout patterns; the display hierarchy levels are `D1`–`D4`.
| Level | Content | Typical layout |
|---|---|---|
| D1 Overview | site / hall: all cells, counts, throughput | L3 grid, large-display version of L1/L3 |
| D2 Cell | one cell twin, current element, 3–4 key parameters | L1, L2 |
| D3 Robot / element | joints, toolpath deviation, element record | L2 right pane, L1 inspector, L6 record |
| D4 Diagnostics | logs, raw signals, procedures, rationale | L5 detail → "OPEN D4 LOG" |
- The breadcrumb in the h1 always shows the path. One click/key (`Esc` or `Home`) goes up one level. The overview is always one action away (R §3.2).
- Each panel labels its level in the header meta ("D3 · ROBOT") [DC], so operators know how deep they are.

### 0.7 Motion
See `motion.md` (locked tokens: 0 / 120 / 200 / 400 ms, P1 pulse 1 Hz until ack, ≤ 3 flashes/s, reduced motion = instant).

### 0.8 Alarm acknowledgement by device [user decision]
- **Desktop and tablet:** ACKNOWLEDGE button (56 px on touch), click or tap, then a confirm step (hard rule 8).
- **Phone:** P1 and P2 can be acknowledged, but **P1 needs press-and-hold** for 1.5 s on a 56 px-high full-width button ("HOLD TO ACKNOWLEDGE P1"). A fill bar grows across the button while held (feedback without motion elsewhere); releasing early cancels with no action; on success a 200 ms fade to "ACKED · name · time". Prevents pocket/accidental acks. P2/P3 ack is a normal tap.
- Every ack logs user, device and time and is shown in the alarm detail (L5). Acknowledge never clears or resets the cause; reset stays at the cell (R §2.4 ISA-18.2).

### 0.9 Control handover (mechanism undefined, rules work for key, token or pendant) [user decision]
1. **Always show the owner.** The top-line CONTROL field shows owner name + device ("M. KELLER · TABLET T2", "PENDANT C3", or "NONE · MONITOR ONLY") on every screen and screen class, including phone and large display. Controls that need ownership are disabled (Muted, with "NOT IN CONTROL") for everyone else.
2. **Request + confirm.** A non-owner taps REQUEST CONTROL → the current owner gets a alarm-band row prompt "T. ROSS · DESKTOP D1 requests control · GRANT / DENY" (56 px buttons on touch). Ownership moves only after GRANT. If the owner does not answer within a configurable timeout (default 30 s) the request expires; it is **never** auto-granted while robots move. When nobody holds control, taking it still needs a confirm step ("TAKE CONTROL OF CELL C3?").
3. **Physical pendant overrides software.** Enabling a teach pendant / local key switch takes control immediately, with no software request, and all software clients drop to monitor-only. The top line shows "PENDANT C3 · LOCAL" and REQUEST CONTROL is disabled until the pendant is released. Releasing the pendant returns to NONE (not to the previous software owner).
4. Every handover (request, grant, deny, expiry, pendant override) is logged and appears in the L5 event list. Handover is per cell; one owner per cell at a time.

---
## Interaction: progressive disclosure (L1-min) · LOCKED 2026-10-18
*Files: `layouts/L1-min-peek.png`, `L1-min-inspect.png`, `L1-min-drill.png`, `L1-min-flow.png`. Source: `layouts/src/L1min.py` (states `normal|alarm|peek|inspect|drill`), `L1min_parts.py`, `L1min_drill.py`, `L1min_flow.py`. All [DC] unless noted; principles numbers refer to `principles.md` §2.*

**Four steps, one direction.** Each step answers one narrower question (principle 1) and adds detail only on request (principle 9).
| Step | Question | What changes | Mouse | Touch | Motion |
|---|---|---|---|---|---|
| 1 Normal | Is the cell OK? | — (L1-min as shipped) | — | — | — |
| 2 Peek | What exactly is this value? | A tooltip on Black with a Line border, placed above the existing KR-02 callout: parameter, exact value, limit, timestamp, data age. **Nothing else moves or changes.** | hover 300 ms | long-press 500 ms (release closes it) | fade in 120 ms |
| 3 Inspect | What is this robot doing, and how close to its limits? | KR-02 gets a 2.5 px Ultramarine **outline** (not a fill). The answer column becomes the robot: ‹ Back · Esc, h2 name, current task + ETA delta, 3 parameters as value / limit with sparklines on a shared value-to-limit scale (dashed = limit, so headroom reads the same way for each), "TCP speed in range", and max 3 recent events. 3D, top line and footer stay as they are; the active footer link turns Text and drops its ›. | click robot or a ROBOTS row | tap | column cross-fade 200 ms |
| 4 Drill | How has this task gone, and what comes next? | New level. The h1 becomes a breadcrumb `Cell C3 › KR-02 › Timeline`. The 3D shrinks to a 560 × 360 context card (grid 20 %, selection kept). Task timeline: completed = filled grey, current = Text outline + progress fill, upcoming = dashed; planned-end tick; NOW line. Path-deviation sparkline across the shift with ▼ markers only where the limit was exceeded. | TIMELINE › or double-click | tap TIMELINE › | level cross-fade 200 ms |

**Number budget.** Normal ≤ 5. Inspect relaxes this to 3 parameter values (each paired with its limit) + ETA delta; no display-size value, so the h2 is the anchor. Drill: ETA delta, 2 exceedance values, current value.

**Back with the alarm band.** When the band is present, the back control sits directly below it (hit area y = 160–216) and the inspector content starts at y = 232, so neither overlaps the band.

**Back / Esc.** Esc (or ‹ Back, or a tap on the previous breadcrumb segment) goes up one step: drill → inspect → normal. Moving the pointer away or lifting the finger closes a peek. Esc never cancels or acknowledges an alarm. Back is always top-left of the answer column at 88 px, so it sits in the same place on every level.

**Selection sync rule.** One selection per screen, always Ultramarine, held in one store: the 3D outline, the ROBOTS row, the inspector column, the breadcrumb and the timeline all show the same robot. Selecting in any of them selects in all. Peek does not select. An alarm does not steal selection; it shows in the band and on the 3D rim (Emergency/Caution) on top of the Ultramarine outline. If the selected robot raises P1, the inspector stays and the band names it.

**Navigation never sends commands.** Hover, tap, long-press, click, double-click, Esc and breadcrumbs only change what is shown. No gesture in steps 1–4 can move a robot, pause it or acknowledge anything. Commands (PAUSE, RESUME, ACKNOWLEDGE) are separate labelled buttons inside the inspector or the alarm band, with a 2-step confirm on desktop/tablet.

**Phones: press-and-hold for commands.** On phones every command (P1 ack, pause, resume) is press-and-hold 1.5 s with a progress ring that fills; releasing early cancels (see §0.8). Long-press 500 ms on the 3D is only for peek, so the two gestures differ in target (canvas vs. labelled button) and duration, and peek can never escalate into a command. Targets are 56 px.

**Motion.** Soft fades only (§0.7): tooltip 120 ms; inspector column and level change 200 ms cross-fade. No slide, zoom or camera fly-to. The 3D camera does not move on selection. With reduced motion, changes are instant.


## Minimal set: L1-min gap fixes + L2-min … L6-min (2026-10-18)
*Files: `layouts/L1-min-focus.png`, `L1-min-stale.png`, `L1-min-touch.png`, `L2-min.png` … `L6-min.png`, `sheet-min.png`. Source: `src/L1min.py` (new states `focus|stale|touch`), `src/Lmin.py` (L2–L6), `src/sheet_min.py`, `src/persist_check.py`; `bash render.sh` renders everything and runs the check.*
- **L1 states:** focus ring (2 px Text, 2 px gap) and link hover (Text, no underline) in `L1-min-focus`; stale value (Muted, hatch, stale glyph + STALE + AGE 12 s, last good time) in `L1-min-stale`; tablet ROBOTS rows 56 px with › in `L1-min-touch`.
- **Shared chrome:** `topline()`, `footer(active,hover,focus)`, `back(x,dest,y)`, `vlim()`, `spark()` from `L1min_parts.py` on every layout; footer keys `inspect|drill|alarm|diag`. `p1band()` (48 px) is the same unacked alarm on L2/L3/L4/L6; L5 omits it because the list is the alarm view.
- **L2-min:** 3D left 800 px, answer column right: W-11 78 % hero, magazine / cycle / path deviation as value-limit rows.
- **L3-min:** 3 × 2 borderless cards (3D, throughput, alarms, robots, materials, design link), each one answer + one drill link.
- **L4-min:** hero 412 m² vs plan, m²/day bars with plan line, top-3 downtime.
- **L5-min:** first-out list in 56 px rows, selected alarm detail with 56 px PROCEDURE / ACKNOWLEDGE.
- **L6-min:** elements × stages matrix; only exceptions in colour; selected W-12 detail.
- **Check:** all L1 state checks pass; top line (excl. h1) and footer (excl. active slot) of L2–L6 match L1-min at 0 px.
- **Locked details:**
  - **One alarm band** (`L1min_parts.alarmband`): 48 px per active P1/P2 row, P1 on top, maximum 2 rows (more go to "+n" in row 2), total 96 px. It is on every layout including L5, always with the same scenario (P1 KR-03 09:54:12 UNACK, P2 KR-01 09:51:40 ACKED). Content starts at y = 176 below it. The sheet's L1 tile is now `L1-min-alarm`.
  - **Focus ≠ selection:** focus = 2 px Text ring with a 2 px gap; selection = Ultramarine on the element. See colour.md for the amendment.
  - **L2:** selected + caution draws both (Ultramarine outline + Caution rim + tagged glyph). New rule 11 in principles.md.
  - **L4:** below-plan bars labelled "−18 vs plan"; week data now sums to the hero (96 + 72 + 101 + 143 = 412).
  - **L3 / L5:** focus rings drawn (card, row). L5 groups by cell, with group header, first-out, alarm rate and ACK GROUP (n).
  - **Interaction states:** `L2/L3/L4/L6-min-peek` (shared `tip()` tooltip, 8 px above its anchor, pointer, cursor) and `L5-min-inspect` (selection moved to the P2 row, detail column follows).
  - **Tablet:** `L2…L6-min-touch` (dashed 56 px hit areas, band buttons 56 px). Compact sheet `states-min.png`.
  - **Check:** `persist_check.py` now also compares the band L1-min-alarm vs every L2–L6 render (tablet: button hit overlay masked), and top line + band + footer for each layout's state vs base. All pass; the only listed difference is the expected KR-02 outline in L1 inspect.

## Responsive layouts: tablet + phone (2026-10-18) · LOCKED
> **Status: LOCKED 2026-10-18.** L1–L6 (desktop `L*-min`, tablet `L*-tab`, phone `L*-phone`) are frozen as the reference for components. Changes now go through `components.md` first; layout edits need a new version note here.

*Files: `layouts/L1-tab.png … L6-tab.png` (1180 × 820), `L1-phone.png … L6-phone.png` (390 × 844), `responsive-sheet.png`. Source `src/resp.py` (reuses `common`, `L1min_parts`, `Lmin.status`), shot via `src/shot_r.sh`. Check `src/touch_check.py` (headless Chrome measures every `.hit` element: asserts ≥ 56 × 56 px, inside the canvas, and no text below 12 px). All 12 pass. Scenario everywhere: 09:54 P1 KR-03 unacked + P2 KR-01 acked.*

### Breakpoints (by viewport width, CSS px)
| Class | Range | Reference canvas | Type tokens | Margin | Chrome |
|---|---|---|---|---|---|
| Phone | < 600 | 390 × 844 portrait | phone scale (below) | 16 | top line 48 · alarm band 1 row 64 · bottom tab bar 64 + 16 home zone |
| Tablet | 600 – 1279 | 1180 × 820 landscape | tablet column of typography.md | 24 | header 72 · alarm band 2 × 56 · footer 72 (168 px slots) |
| Desktop | ≥ 1280 | 1600 × 1000 | desktop column | 32 | top line 56 · band 2 × 48 · footer 72 (176 px slots) |
| Wall | ≥ 2560 at ≥ 3 m | 3840 × 2160 | wall column | 64 | desktop layout, wall sizes; no touch |

**Phone type scale (6 sizes, ≥ 1.2 per step, floor 12):** label 12/16 · body 15/20 (×1.25) · title = h1 18/24 (×1.20) · value-m 22/28 (×1.22) · value-l 28/32 (×1.27) · display 40/44 (×1.43). Same families and weights as desktop. h1 drops to 18 (shares with title, still Muted) so a long cell name fits on 358 px.

### Reflow rules
| Element | Desktop | Tablet | Phone |
|---|---|---|---|
| Top line | ANDURA · h1 · CONTROL · DATA · clock | same | h1 + clock only; CONTROL and DATA move to MORE; DATA age comes back in the top line only when stale |
| Alarm band | 2 rows × 48 (P1 then P2), ACK in row | 2 rows × 56; buttons fill the row height (56) | **1 row × 64**: highest unacked alarm + "+n"; the whole row is the target and opens the L5 detail |
| Acknowledge | click → confirm | tap → confirm (2 steps) | **press-and-hold 1.5 s** with ring + fill; release early cancels; never in the band itself |
| Footer | 4 text links + E-STOP note | same, 168 px slots | **bottom tab bar**: CELL · ROBOTS · ALARMS (P1 glyph badge) · MORE (timeline, analytics, graph, diagnostics, control); active = Text + 2 px top bar |
| 3D | full-bleed left (L1, L2) or card (L3) | same, auto-fit scene | L1: 358 × 176 **thumbnail**, tap → full-screen 3D. L2/L3/L5/L6: no 3D (behind "TRENDS · 3D ›" or the CELL tab) |
| Answer column | right column | right column, narrower | single column under the thumbnail, exceptions first |
| L3 card grid | 3 × 2 | 3 × 2 | single stack: alarms, throughput, robots, then Materials / Design link as 64 px rows |
| L4 chart | vertical bars | vertical bars, "−18" deltas | one 56 px row per day: bar, plan tick, value, delta |
| L5 list + detail | list left, detail right | same; groups + 56 px rows | detail screen first (from band, "+n" or ALARMS tab): "‹ ALL ALARMS · n" back row, glyph + word + time, message `title`, value + LIMIT, cause/next step, PROCEDURE, then **HOLD TO ACKNOWLEDGE** (64 px full width, fill opacity 0 → 1 over 1500 ms, release cancels). No 3D thumbnail |
| L6 matrix | elements × 4 stages | same, 136 × 56 cells | one 64 px row per element with only the stage that needs action; tap → 4-stage detail |
| Lists / rows | 32 | 56 | 64 |
| Hover peeks | hover 300 ms | long-press 500 ms | long-press 500 ms on the thumbnail only; values are already in rows |

### Text scaling (WCAG 1.4.4, 0.3.1)
At OS text size 125 / 150 / 200 % (`text-scale.*`):
| Element | Rule |
|---|---|
| Type | every size and line height × step |
| Top line, alarm rows, band buttons, footer, tab bar, list rows | height × step (`size.*` token × step) |
| Margins, grid, gaps, strokes, 3D view, phone thumbnail | unchanged |
| Answer column | width × step, at most 50 % of the canvas; wraps and scrolls vertically; same value budget |
| Labels, band messages, h1, tab labels | one line, ellipsis, full text on peek (hover 300 ms / long-press 500 ms) |
| Values and units | never truncate, wrap or clip; the value row wraps its LIMIT to the next line instead |
| Targets | ≥ 56 × 56 px on touch classes, and on every class at 200 % |
The persistent zones stay pixel-identical across states at any one step. `scripts/touch_check.py` checks all four steps on the worked example.

### Alarm decisions (ISA-18.2 / ISA-101, 0.3.4)
- **P2-only on phone:** the band row has a steady Caution edge, triangle glyph, `P2 CAUTION`, the message and "+n". The ALARMS badge shows a triangle with `P2 · n`.
- **Badge:** the highest active priority (glyph + word) and the count of active P1 + P2 alarms, acknowledged or not. Its slot is reserved, so the tab label never moves.
- **Cell summary:** `<highest priority> · <cell state>`, with cell state one of Running, Partly stopped, Stopped or Waiting (`P1 · Partly stopped`). A Muted line under it names the abnormal robots. With nothing active: just the state (`Running`), no glyph, no colour.
- **LIMIT vs TARGET:** LIMIT is an alarm setpoint; crossing it raises a P1 or P2. TARGET is a plan value (for example cycle time); show it Muted as `TARGET 4:00 · DEV +0:12` and never in an alarm hue unless a LIMIT is also crossed.
- **Dimming** (`opacity.dim`): routine values dim while any P1 is active, or any P2 is unacknowledged. An acknowledged P2 alone does not dim.

### Polish v1.1 (2026-10-18)
- **Tablet 3D centred** (L1, L2): auto-fit uses the true floor extent (x−y centre at 2 units, x+y at 0–20 less robot height).
- **Phone full-screen 3D** `L1-phone-3d.png`: scene fills the body; ✕ CLOSE and RESET VIEW (56 px) at top; gesture hint; a 64 px selection bar at the bottom (KR-02 · DETAIL ›); band and tab bar stay.
- **Phone MORE** `phone-more.png`: VIEWS (Timeline, Analytics, Design to fab with status, Diagnostics) and CELL C3 (Control owner, Data age, Alarm history) as 64 px rows, plus the E-STOP note.
- **touch_check** now also fails on any clickable-looking element (`.btn`, or text containing ›, ‹ or ✕) that is not inside a `.hit` target. A self-test proves the detector catches an unmarked button and an unmarked › link. 14 screens pass.
### Risks
- The detector keys on ›/‹/✕ and `.btn`. A tappable element with none of these signifiers would still need the `.hit` mark by hand.
- On the phone 3D view the scene is width-bound (landscape cell in a portrait frame), so robots render small. Pinch zoom is assumed.

---
## Cross-layout rules (summary)
1. Top line, alarm band and footer are identical across all six layouts (pixel-checked). Only the content area changes.
2. One h1, one display value, one h2 per panel, per screen (T).
3. Selection is Ultramarine everywhere and is synced across 3D, lists, graph and charts.
4. Every live value: unit, range/limit, age. Stale = hatch + Muted + age (C).
5. Fades only (200 ms), plus the P1 ~1 Hz slow fade pulse while unacked, stopping on ack (§0.7).
8. Touch targets 56 px on every touch screen; P1 ack on phone is press-and-hold (§0.8).
9. CONTROL owner always visible; handover = request + confirm; physical pendant overrides software (§0.9).
10. L3 grid: per-user layout, admin default, reset to default, alarms pinned to the top row.
6. E-stop is physical. The UI mirrors it and never offers it as a button.
7. Layouts do not reflow because of data. Position is stable; only state changes.

## Open questions
1. **Advisory colour:** v2.2 has no advisory hue (Text + (i)). In L5 advisory rows look close to acked rows. Is that acceptable?
2. **Handover mechanism:** once the real mechanism is chosen (key switch, software token, pendant), confirm the 30 s request timeout and whether a supervisor may force-take control.
