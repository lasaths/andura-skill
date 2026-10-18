# Changelog

ANDURA uses semantic versioning. The version lives in `tokens/andura.tokens.json` (`$extensions.andura.version`), in the `SKILL.md` frontmatter and in the top entry here; `scripts/check.py` fails if they differ.

**Breaking change** (bump the major version; while in `0.x`, bump the minor): a changed or removed token value or name, a renamed or renumbered rule (hard rules 1–10, rules 1–13), a changed breakpoint or chrome size, or a removed reference file. Adding tokens, references, checks or examples is not breaking.

## [0.6.0-draft] - 2026-10-18

### Breaking
- `size.topline.*` renamed to `size.header.*`.
- Header heights changed from 56 · 56 · 48 to 72 · 72 · 64 (desktop · tablet · phone). Every touch class is now ≥ 56, on the 8 px grid.
- `size.content-top` changed from 176 to 192, and the alarm band now starts at y 72 (phone: y 64).

### Added
- The ANDURA mark: a bold geometric A, a solid chevron with a small foot triangle, monochrome Text (`currentColor`). Saved as `assets/andura-mark.svg`, used at the left of the header in all six examples, and in the README title.
- `size.logo` (32): the height of both the mark and the optional client/app logo slot (max width 4 × that). Header recipe in `recipes.md` §0 (checked for drift); header documented in `layouts.md` §0.0.

## [0.5.0-draft] - 2026-10-18

### Added
- Data-quality states on the examples (`?state=`): `stale`, `comms`, `offline`, `empty`, `flood`. Pages declare their states in `<meta name="andura-states">`; the checks default to them. L1 has all four live-data states, plus L2 offline, L3 empty, L4 stale, L5 flood and L6 comms.
- Rules (SKILL.md, `recipes.md` §9–12): stale values stay in Muted with their data age and are never shown as live; comms loss and robot offline get a band row; startup shows `—` + `WAITING FOR DATA`, never zeros; an alarm flood (> 10 alarms in 10 min, ISA-18.2) collapses to one band row, and the alarm list shows shelved alarms (time left, by whom) and suppressed-by-design counts. Alarms stay active (`body[data-alarms]`) through all of these states.
- `touch_check.py` data-quality checks: a visible stale block must show a data age, a stale value must be Muted, and no digits may appear in the empty state. New self-test.
- `references/charts.md`: sparkline, trend with limit band, histogram, Gantt. Covers tokens, axes (min/max only), no gridlines, cividis for data and alarm hues only on violations. Recipes `trend`, `hist` and `gantt`; used on L4 (cycle-time trend and histogram) and L6 (fabrication Gantt).
- `references/3d-engines.md`: maps the viewport rules to three.js, Babylon.js 8 and Unity 6, with token-driven snippets. APIs were checked against the current docs.
- Sunlit-tablet mode: `$extensions.andura.modes.sunlit` (positive polarity, Text 15:1, Muted 7:1, Line 3:1, hues 4.5:1). Exported as `[data-andura-mode="sunlit"]` CSS, `anduraSunlit` (TS), `ANDURA_SUNLIT` (Py) and `AnduraSunlit` (C#). Documented in `colour.md` §9; `check.py` verifies every target and the table. Examples accept `?mode=sunlit`.
- Tokens: `size.chart-h` (120), `size.gantt-bar` (12), `color.on-ultramarine` (#DADADD, text on an Ultramarine fill).

### Changed
- L3 desktop uses a 12-column grid (3D 8, alarms 4, other cards 3 each), so it has no large empty areas. On tablet, L4's chart takes a full column instead of being squashed.
- Example chrome: alarm styling keys on `body[data-alarms]` instead of `data-state=alarm`. The top-line DATA fact is the only chrome text that changes by state; `persist_check` masks it.

## [0.4.0-draft] - 2026-10-18
Consistency and coverage (Phase A). Minor bump: a new required entry point and the L5 band decision; no token changed.
- **Reference screens L2–L6** (`examples/l2-split`, `l3-cards`, `l4-analytics`, `l5-alarms`, `l6-design-fab`, each html + md spec), same 09:54 scenario, `?state=` / `?scale=` contract, every class × state × scale passing. L3 and L4 define no inspect state (SKIP). L5 has no alarm band (the list is the alarm view, as `layouts.md` specifies). L2 inspect keeps the alarm chrome. L4 reflows with flex-wrap; L6 switches to the phone list by container query when the pane narrows it.
- **Shared chrome:** `examples/andura-ui.css` + `andura-ui.js` (state/scale, peek titles, `aria-current`, `--k`, hold, confirm). L1 refactored onto them. New `.vals` rows: multi-value lines wrap between groups, never inside a value.
- **`references/recipes.md`:** exact markup and state classes for alarm row, KPI, 3D tag, dialog, hold, tabs, cell summary, sparkline, plus the 4 canonical glyphs. `check.py --example` fails recipe drift (machine-readable `requires` selectors) and non-canonical glyphs.
- **Single entry point `scripts/andura_check.py page.html [--classes|--states|--scales]`** (`--all` = repo check + every example): runs check.py --example, touch_check and persist_check, one PASS/FAIL summary, non-zero exit. SKILL.md §7 and CI use only this.
- **`evals/`:** fixed fresh-agent prompt (SAW-1 cutting station), pass criteria A1–A6, `score.py`, run log. Needs an agent, so not in CI.
- `check.py`: breakpoint tokens accepted in `@container`; new rule failing internal machine paths in any shipped file (31 self-test cases). Render checks use per-process temp files (safe to run in parallel); persist self-test picks an unmasked pixel next to the badge.
- `research.md` no longer names an internal path for the base skill.

## [0.3.4-draft] - 2026-10-18
Fixes from a second fresh-agent test.
- Example `?state=detail`: alarm detail with acknowledge per hard rule 8 (confirm dialog with focus on CANCEL on desktop/tablet, also from the band ACKNOWLEDGE; 1500 ms hold with opacity fill on phone). Specified in `l1-alarm.md`, `layouts.md` (L5 phone) and `components.md` #12.
- 3D strokes keep a constant on-screen width (new rule in §3); the example uses non-scaling strokes and `--k` for the selection outline. `touch_check.py` fails any `.o3d` stroke under 2 px on screen.
- `touch_check.py` scrolls each target into view instead of skipping it and rewrites every relative href/src (shared `prepare()` in `_chrome.py`). `persist_check.py` masks only the exact `[aria-current]` and `.badge` rects from the DOM. `check.py --example` flags hand-typed px/ms (with the matching token, if any) and accepts an inlined andura.css. New self-tests for each (27 check.py cases; 2 new touch, 1 new persist).
- Naming: layout patterns stay `L1`–`L6`; display hierarchy levels are now `D1`–`D4`.
- Labels write `PATH DEV` (hard rule 4). New token `size.content-top` (176).
- Alarm decisions documented: P2-only phone band and badge, badge = highest priority + count with a reserved slot, cell summary pattern, LIMIT vs TARGET, dimming while a P1 is active or a P2 is unacknowledged.
- Example: ALARMS badge slot reserved (the label no longer shifts when an alarm appears; `persist_check.py` caught it).

## [0.3.3-draft] - 2026-10-18
Fixes from a cold fresh-agent test.
- Scripts take a target: `touch_check.py page.html [--classes] [--states] [--scales]`, `persist_check.py page.html [--classes] [--states]` (a state the page lacks is SKIP, not PASS), `check.py --example page.html`. Page contract (`?state=`, `?scale=`, `.hit`, `.trunc`, `.value`) documented in `examples/l1-alarm.md`.
- `check_example`: hex inside `style=""` or before any quote is now caught; andura.css must be loaded by a real `<link rel=stylesheet>` or `@import`. Three new self-tests (23 cases). `touch_check.py` also fails on more than 6 distinct font sizes.
- New tokens: `size.glyph`, `size.spark-h`, `size.column.desktop|tablet`, `size.stroke-rim`, `opacity.dim`, `opacity.scrim`, `type.label.tracking`. The example has no size/opacity literals left (bar geometry aside).
- New export `tokens/build/andura-fonts.css` (`@font-face` for IBM Plex, `local()` then `render/fonts/`); documented in `platforms.md` and the workflow.
- `SKILL.md`: hard rule 2 covers badges and cell summaries; hard rule 3 allows phone +n and defines the ALARMS badge; hard rule 7 treats touch displays as tablet; rule 4 lists what doesn't count; rule 8 end dot never in an alarm hue; rule 13 lists every duration token; §3 dialog and scrim; §4 at most 6 distinct type tokens and hero-unit rule; workflow loads fonts and renders named classes plus checked ones.
- `components.md` #12 hold-to-confirm: fill opacity 0 → 1 over `motion.duration.hold`, no width growth (hard rule 9). `libraries.md`: default to React Aria or Radix with no project.
- Example: cell summary "P1 · Partly stopped"; ALARMS badge `P1 · 2` only while an alarm is active; tab bar active state is a 2 px border-top; path deviation uses value-m (6 type tokens).

## [0.3.2-draft] - 2026-10-18
- New `references/libraries.md`: pick a component library per platform and adapt it to the tokens (workflow, pick list, criteria, override checklist, mapping, gate).
- README cut to a short human overview; depth lives in `SKILL.md` and `references/`.

## [0.3.1-draft] - 2026-10-18
- Worked example now covers phone (390 × 844: tab bar, 64 px one-row band, 3D thumbnail) and `?state=inspect` (KR-02 selected, detail column).
- OS text scaling (WCAG 1.4.4): tokens `text-scale.100|125|150|200`; rules in `SKILL.md` §5, `references/layouts.md`, `typography.md`, `interaction.md`; `?scale=` in the example.
- New tokens `size.home-zone` (16) and `size.thumb-3d-phone` (176).
- `touch_check.py` runs every class × state × scale and also fails on clipped text, truncated values and overlapping text; `persist_check.py` covers phone and normal vs inspect. Headless measurement now uses an exact-size iframe (Chrome windows can't go below 500 px).
- `check.py` self-test covers colour literals and unknown tokens in examples.
- Removed unused pre-minimal render helpers; hero renders byte-identical.
- MIT licence (`LICENSE`); IBM Plex stays under SIL OFL 1.1 and is not bundled.

## [0.3.0-draft] - 2026-10-18
- Self-contained repo: `scripts/touch_check.py` and `scripts/persist_check.py` run against `examples/l1-alarm.html`; `render/` vendors the renderer for `scripts/render_hero.py`, which downloads IBM Plex (OFL) on first run.
- Worked example `examples/l1-alarm.html` (tokens only, desktop and tablet) with the annotated spec `examples/l1-alarm.md`.
- `SKILL.md` cut to the essentials; components, 3D, motion and interaction depth now live in `references/` (new `interaction.md`, `platforms.md`). Hard rules are now §1, the 13 rules §2 (numbering inside unchanged).
- Description lists triggers (HMI, SCADA, operator console, alarm screen, robot cell, BIM/digital twin) and a not-for clause.
- Tokens: `color.3d.*` (11 greys for the 3D model), version in `$extensions`. The renderer reads its palette from the tokens.
- Back control moves below the alarm band when both are shown (hit y = 160–216, content from y = 232).
- CI: `.github/workflows/check.yml` runs the checks, the export diff, `tsc --noEmit` and a `dotnet build`. TS and C# exports now compile.
- New hero image with an alarm band slice.

## [0.2.0-draft] - 2026-10-18
- W3C Design Tokens file `tokens/andura.tokens.json` as single source of truth; exports to CSS, TS, Python and C#.
- `SKILL.md` rewritten platform-neutral (px, ms), directive wording; "Implementing on any platform" section.
- References cleaned to locked content only; principles renumbered to the 13 rules.
- `scripts/check.py`: token, contrast, reference and banned-value checks with a self-test.
- Motion: exits use ease-out, keyboard navigation is instant, fades are interruptible, peek chaining, hover gating. Camera never moves without a user action.
- Surface Hover and Surface Lift tokenised. README and hero image.

## [0.1.0-draft] - 2026-10-18
- First `SKILL.md` draft: hard rules, 13 rules, palette v2.2, IBM Plex type scale, L1–L6 layouts, components, 3D viewport, motion, checklist.
