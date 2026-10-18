# Changelog

ANDURA uses semantic versioning. The version lives in `tokens/andura.tokens.json` (`$extensions.andura.version`), in the `SKILL.md` frontmatter and in the top entry here; `scripts/check.py` fails if they differ.

**Breaking change** (bump the major version; while in `0.x`, bump the minor): a changed or removed token value or name, a renamed or renumbered rule (hard rules 1–10, rules 1–13), a changed breakpoint or chrome size, or a removed reference file. Adding tokens, references, checks or examples is not breaking.

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
