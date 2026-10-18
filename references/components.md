# ANDURA — Components v1.1 (2026-10-18)

> Provenance: paths under `layouts/` name the original design workspace and are not shipped. The renders are in `assets/`; runnable equivalents are `examples/`, `render/` and `scripts/`.
*Built on the LOCKED layouts L1–L6 (`layouts.md`). Sheet: `layouts/components.png` (renderer `layouts/src/components.py`, which uses the shared code in `L1min_parts.py`, `Lmin.py` and `resp.py`). Tokens: colour.md v2.2 (+ focus amendment), typography.md (desktop / tablet / phone scales). [DC] = design choice.*

## Global state rules
| State | Rule |
|---|---|
| Default | Normal = Muted/Text, no colour, no glyph (principle 2) |
| Hover | Text colour or Surface lift `#141518`; never the only signifier (touch has no hover) |
| Focus | 2 px Text `#DADADD` ring, 2 px gap outside, above content (WCAG 2.4.11 / 2.4.13, 15:1) |
| Active | Pressed: darker fill. Current: Text + 2 px underline or top bar. Selected: Ultramarine `#3A3CFF` outline |
| Disabled | 38 % opacity, no hover or focus, reason given in a tooltip or row text |
| Stale | Hatch + Muted value + stale glyph + "STALE · age"; never shows a live-looking value |
| Alarm | Colour + glyph + word (P1 Emergency octagon, P2 Caution triangle, P3 circle-i). Never hidden by selection: Ultramarine outside, status rim inside |

## Components
Sizes are given as desktop · tablet · phone. Touch targets are always ≥ 56 px on tablet and phone (asserted by `touch_check.py`).

| # | Component | Anatomy | States drawn | Sizes D · T · P | Source |
|---|---|---|---|---|---|
| 1 | **Top line** | mark (`size.logo`) · client logo slot · h1 (or breadcrumb) · CONTROL · DATA age · clock | default, focus (crumb), stale (DATA age glyph) | 72 · 72 · 64 (phone: mark, h1, clock) | `header`, `resp.top` |
| 2 | **Footer / tab bar** | 4 links in fixed slots + E-STOP note / 4 tabs | default, hover, focus, active (underline / top bar), disabled, alarm badge | slot 176×72 · 168×72 · tab 97×64 (+16 home zone) | `footer`, `resp.foot` |
| 3 | **Alarm band row** | priority bar · glyph · PRIORITY word · message · time/state · actions | default (acked), hover, focus, active, alarm (P1 unacked, 1 Hz pulse) | 48 · 56 · 64 (phone: 1 row + "+n") | `alarmband`, `resp.band` |
| 4 | **Value / limit readout** | value (value-m/l) · unit Muted · `LIMIT n unit` label | default, disabled (—), stale, alarm (over limit + glyph + word) | 22 · 24 · 22 px value | `vlim` |
| 5 | **Sparkline** | dashed limit · trace 1.5 px · end dot; value-to-limit scale | default, disabled, stale (hatch), alarm (crosses limit) | 32 · 32 · 24 h | `spark` |
| 6 | **Status tag** | glyph 16 + label-caps word (abnormal) / Muted word (normal) | default, stale, alarm (P1, P2) | label token per class | `Lmin.status` |
| 7 | **Robot list row** | glyph column 16 · ID mono · task/status · › (touch) | default, hover, focus, active (selected), disabled (offline), stale, alarm | 32 · 56 · 64 | `L1min` fleet, `resp.rows` |
| 8 | **Card** | label + drill link › · one answer · whole card is the target, no border | default, hover, focus, active, disabled, stale, alarm | grid cell · grid cell · full-width stack | `Lmin.L3`, `resp.L3` |
| 9 | **Button · primary** | Ultramarine fill, label caps | default, hover, focus, pressed, disabled | 32 (40 in band) · 56 · 56 | `.btn.pri` |
| 10 | **Button · secondary** | Line outline | default, hover, focus, pressed, disabled | 32 · 56 · 56 | `.btn` |
| 11 | **Button · danger** | Emergency outline; active = confirm step in Emergency fill | default, hover, focus, confirm, disabled | 32 · 56 · 56; always 2-step | components.py |
| 12 | **Hold-to-confirm** | Ultramarine fill, opacity 0 → 1 over `motion.duration.hold` (1500 ms, linear), no width growth (hard rule 9) · release cancels (reset over `duration.fast-out`) | default, focus, active (40 % held), disabled | phone only, 64 h full width; lives on the alarm detail screen (`references/layouts.md` L5 phone), never in the band | `resp.hold` |
| 13 | **Tooltip (peek)** | Black, 1 px Text outline, pointer notch, label · value/limit · time/age; 8 px above anchor | default, stale (age), alarm (over limit) | 192–320 w · same · long-press only | `tip` |
| 14 | **Back control** | ‹ + destination name + ESC keycap (desktop) | default, hover (underline), focus, pressed | 56 hit all classes | `back` |
| 15 | **3D selection + status overlay** | Ultramarine 2.5 px outline (selected) · status rim (P1/P2) inside · hover thin Text outline · stale dashed | all 7, incl. selected + alarm | k-scaled; outline constant 2.5 px | `common.robot` |
| 16 | **Matrix cell** | box = artefact · status tag inside · connector line in status colour | default, hover, focus, active (selected), disabled, stale (dashed), alarm (Caution outline) | 168×64 · 136×56 · becomes a 64 px row | `Lmin.L6`, `resp.L6` |

## Added from the locked layouts (minimal specs, drawn on components.png)
| # | Component | Implied by | Anatomy / rules | Sizes D · T · P |
|---|---|---|---|---|
| 17 | **Confirm dialog** | "ACKNOWLEDGE…" (desktop/tablet 2-step), danger buttons, shelve | Black, 1 px Text outline (Emergency outline for destructive actions) · title states the action as a question · one line of consequence · CANCEL (secondary) + CONFIRM (primary, or danger fill). Focus starts on CANCEL; Esc cancels; Enter does not auto-confirm destructive actions | 480 w · 480 w · bottom sheet, 56 px buttons |
| 18 | **Text input** | L5: "Shelving needs a reason" | label caps above · underline field (no box) · hover Text underline · focus 2 px Text underline + focus ring · disabled dashed · error = Caution underline + glyph + REQUIRED | 40 · 56 · 56 h |
| 19 | **Toast** | "ack 0.1 s visual confirmation" (layouts §L5), feedback rule in the heuristics audit | Surface lift `#1a1b1e`, 2 px left bar (Text = done, Emergency = failed + glyph), one line, timestamp; 4 s, never covers the alarm band; no undo for acknowledge | 40 · 56 · 56, above the tab bar on phone |

## Deferred (no locked layout needs them)
- **Toggle / switch, segmented control (LIVE/REPLAY, 3D/TOP):** used only in the pre-minimal L1–L6 drafts, not in the locked set. Spec them when replay mode is designed.
- **MORE-sheet list item:** reuses robot list row #7 (64 px, label + value + ›), so no new component (see `phone-more.png`).
- Wall-class sizes follow the typography.md wall column but are not drawn.
- Hover on the 3D overlay is drawn as a thin Text outline. Validate it on the real renderer, because the scene's grid may compete with it.

## 3D viewport aids (added 2026-10-18; see `viewport.md` §8, drawn in `layouts/viewport.png`)
| # | Component | Anatomy | States | Sizes D · T · P |
|---|---|---|---|---|
| 20 | **View cube** | iso cube, named faces TOP/FRONT/L, current face in Text | default (Muted), hover face Text, focus ring, active (current view) | 96 · 96 · 56 |
| 21 | **Viewport tool rail** | label + keycap rows: HOME, FIT, ZOOM TO ALARM, ISOLATE, SECTION, MEASURE, FOLLOW, LAYERS | default Muted, hover Text, focus ring, active fill #1a1b1e, disabled 38 %, alarm = Emergency edge on ZOOM TO ALARM | 40 · 56 · folds into "⋯ TOOLS" sheet (64 rows) |
| 22 | **Context action bar** | selection glyph + ID (or "n SELECTED") · DETAIL › · ISOLATE · HIDE · PATH | default, hover, focus, active, disabled per action | 40 · 56 · selection bar 64 |
| 23 | **View-mode indicator** | projection · camera mode · layers n/4 · section | default; stale/reduced states ("3D REDUCED", "3D PAUSED") | label token, all classes |
| 24 | **Edge chip (off-screen alarm)** | 3 px status edge · glyph · ID · › | alarm only; hover, focus | 56 h all classes |
| 25 | **Layers popover** | checkbox rows | on/off, focus, disabled | 32 rows D · 56 T/P |
| 26 | **Scale bar + axis tripod**, **minimap**, **gesture legend** | see viewport.md §8 | static; legend dismissable | — |
