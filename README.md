<p align="center"><img src="assets/hero.png" alt="ANDURA: close-up of a digital-twin dashboard with the alarm band on top, a selected robot outlined in Ultramarine, robots tagged in Caution and Emergency, and live values with sparklines" width="100%"></p>

# ANDURA

**A dark-mode design system and agent skill for mission-critical 3D digital-twin dashboards: grey when everything is normal, colour only for what needs attention.**

`version 0.3.4-draft` · tokens in W3C Design Tokens format · works on any platform · [MIT License](LICENSE)

## What you get
- **An agent skill** ([`SKILL.md`](SKILL.md)): hard rules, the 13 rules, colour, type, layout, workflow and checks for HMI, SCADA, robot-cell and BIM/digital-twin screens.
- **Design tokens** ([`tokens/andura.tokens.json`](tokens/andura.tokens.json)) exported to CSS, TypeScript, Python and C#.
- **A worked example** ([`examples/l1-alarm.html`](examples/l1-alarm.html)) on desktop, tablet and phone, in alarm, normal, inspect and alarm-detail states, up to 200 % text size.
- **Checks** that prove tokens, contrast, 56 px targets, clipping and fixed chrome.

![Desktop layouts L1 to L6](assets/sheet-min.png)

## Install as an agent skill

One command, for Cursor, Claude Code, Codex, Copilot and [many more agents](https://github.com/vercel-labs/skills#supported-agents):

```bash
npx skills add lasaths/andura-skill        # this project
npx skills add lasaths/andura-skill -g     # all projects
```

Or copy this folder into your agent's skills directory (e.g. `~/.cursor/skills/andura` or `~/.claude/skills/andura`).

## Example prompt
```text
Use the andura skill to design an L1 screen for robot cell C3 in the alarm state, desktop and phone.
Review this dashboard against andura and list rule violations.
```
The agent loads `SKILL.md` (about 150 lines) and opens the example and `references/` only when it needs more depth.

## Tokens
`python3 scripts/export_tokens.py` writes [`tokens/build/`](tokens/build/) (`andura.css`, `andura-fonts.css`, `andura.ts`, `andura.py`, `Andura.cs`). Per-platform use: [`references/platforms.md`](references/platforms.md); component libraries: [`references/libraries.md`](references/libraries.md).

## Checks
```bash
python3 scripts/check.py && python3 scripts/touch_check.py && python3 scripts/persist_check.py
```
The render checks need Chrome; CI ([`.github/workflows/check.yml`](.github/workflows/check.yml)) also compiles the TS and C# exports.

## Repository
```text
SKILL.md        the skill (agents read this first)
references/     depth, read on demand
tokens/         source of truth + generated exports
examples/       worked L1 screen and its spec
scripts/        export, checks, hero render
render/ assets/ hero renderer and rendered specimens
```

## References
[Layouts](references/layouts.md) · [Components](references/components.md) · [Interaction](references/interaction.md) · [3D viewport](references/viewport.md) · [Motion](references/motion.md) · [Colour](references/colour.md) · [Typography](references/typography.md) · [Platforms](references/platforms.md) · [Libraries](references/libraries.md) · [Principles](references/principles.md) · [Research](references/research.md) · [Changelog](CHANGELOG.md)

## Status
**0.3.4-draft.** Rules, palette, type, layouts and components are locked; the skill as a whole is under review. Only L1 is built as an example (L2–L6 are specified). Wall screens don't follow OS text size, and 3D labels aren't checked at large text sizes. Changes are breaking if they touch a token or the rule numbering; see [`CHANGELOG.md`](CHANGELOG.md).

## License
[MIT](LICENSE) © 2026 Lassie (lasaths). IBM Plex is not bundled and stays under the SIL Open Font License 1.1.
