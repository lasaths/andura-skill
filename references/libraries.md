# ANDURA — Using a component library

Suggest a library, then adapt it to ANDURA. The tokens (`tokens/andura.tokens.json` and its exports) stay the source of truth; the library supplies behaviour and accessibility, never the look.

## 1. Workflow
1. **Detect the stack** from the project: `package.json` (React, Vue, Svelte, plain web), `*.csproj` (WPF, Avalonia, MAUI), `pyproject.toml` / `requirements.txt` (PySide6, Dash), Unity `Packages/manifest.json`. Ask only if nothing is found.
2. **Suggest 1–2 options** from §2 with a one-line reason each (headless vs themed, licence, what the project already uses). Prefer a library already in the project.
3. **Map tokens:** load the matching export (`andura.css`, `andura.ts`, `andura.py`, `Andura.cs`) and bind the library's theme variables to it. Never type a colour, size or duration literal. See `references/platforms.md`.
4. **Override defaults** with the checklist in §4.
5. **Run the checks** in §6 before you ship.

## 2. Pick list (licences checked October 2026)
| Platform | Library | Licence | Notes |
|---|---|---|---|
| React | Radix Primitives | MIT | headless; style with `andura.css` |
| React | React Aria (Adobe) | Apache-2.0 | headless hooks/components; strongest a11y and touch handling |
| React | shadcn/ui | MIT | copy-in code on Radix or Base UI + Tailwind; you own the source, so replace its theme variables with tokens |
| React | Base UI (`@base-ui/react`, v1) | MIT | headless, from the Radix / MUI teams; Combobox, nested dialogs |
| Vue | Reka UI (formerly Radix Vue) | MIT | headless |
| Svelte | Bits UI | MIT | headless |
| Any web | Web Awesome (Shoelace successor) | MIT (Core) | web components, themed by CSS custom properties; Pro tier is paid, do not depend on it |
| .NET desktop | WPF, Avalonia (MIT), .NET MAUI (MIT) | open | merge a `ResourceDictionary` built from `Andura.cs`; restyle control templates |
| Python desktop | PySide6 (Qt) + QSS | LGPLv3 / commercial | generate the QSS from `andura.py`; mind LGPL linking terms |
| Python web | Dash (Plotly) | MIT | style with `andura.css`; set Plotly templates from tokens |
| Charts | uPlot (MIT), Apache ECharts (Apache-2.0) | open | sequential data uses cividis (`color.cividis.*`); disable chart animation |
| 3D | Three.js (MIT), React Three Fiber (MIT) | open | greys from `color.3d.*`; rules in `references/viewport.md` |
| Unity | UI Toolkit + USS for the 2D overlay | Unity licence | generate USS variables from the tokens; 3D rules as above |

## 3. Selection criteria
- Headless, or fully themeable through variables (no hard-coded palette).
- Accessible: keyboard, focus management, screen-reader roles, WCAG 2.2 AA.
- Motion can be turned off globally and honours reduced motion.
- No forced radius, shadow, ripple or elevation.
- Open licence (MIT, Apache-2.0, BSD; LGPL only with care) and actively maintained (release in the last 12 months).
- Supports tabular figures and a custom font stack (IBM Plex).

## 4. Override checklist
- [ ] Radius 0 everywhere (buttons, inputs, cards, menus, dialogs).
- [ ] No shadows or elevation; separate with Surface / Line only.
- [ ] No ripple, scale or bounce on press; opacity changes only (`motion.*`).
- [ ] Focus ring = 2 px Text outline, 2 px offset (`size.focus-ring`, `size.focus-gap`); never the library's blue glow, never Ultramarine.
- [ ] Touch targets ≥ 56 × 56 px, 8 px apart, on every touch class (`size.touch-min`).
- [ ] IBM Plex Sans and Mono, weights 400 and 500, tabular and slashed-zero figures in Mono.
- [ ] Colour only from tokens; delete the library's palette and status colours.
- [ ] Toasts never carry an undo for a robot command and never auto-dismiss a P1/P2 (alarms go to the band).
- [ ] Confirm dialogs open with focus on **Cancel**; the command button is labelled with the action, not "OK".

## 5. Component mapping
| ANDURA (`references/components.md`) | Radix | React Aria | shadcn/ui | WPF |
|---|---|---|---|---|
| Button (primary, secondary) | — (native `button`) | `Button` | `Button` | `Button` + style |
| Confirm dialog | `AlertDialog` | `Dialog` (`role="alertdialog"`) | `AlertDialog` | `Window` (modal) / `ContentDialog` |
| Peek / tooltip | `Tooltip`, `HoverCard` | `Tooltip` | `Tooltip`, `HoverCard` | `ToolTip` / `Popup` |
| Menu / MORE | `DropdownMenu` | `Menu` | `DropdownMenu` | `ContextMenu` / `Menu` |
| Tabs / tab bar | `Tabs` | `Tabs` | `Tabs` | `TabControl` |
| Toggle / mode switch | `Switch`, `ToggleGroup` | `Switch`, `ToggleButtonGroup` | `Switch`, `ToggleGroup` | `ToggleButton` |
| Robot list rows | — (list of buttons) | `ListBox`, `GridList` | — | `ListBox` |
| Alarm list | — | `Table` | `Table` | `DataGrid` |
| Progress | `Progress` | `ProgressBar` | `Progress` | `ProgressBar` |
| Toast / notice | `Toast` | `Toast` (beta) | `Sonner` | custom `Popup` |
| Scroll area (answer column) | `ScrollArea` | — | `ScrollArea` | `ScrollViewer` |

The alarm band, top line, footer, status glyphs and sparklines are ANDURA's own; build them from tokens, not from a library component.

## 6. Gate
A screen built on a library ships only if it passes `python3 scripts/check.py`, `scripts/touch_check.py` and `scripts/persist_check.py` (point the render checks at it with the `.hit` convention in `examples/l1-alarm.md`). Where the checks can't run (WPF, Qt, Unity), do the same checks by hand: no literal colours, 56 px targets, no clipped text at 200 % text size, top line and footer identical across states, plus the manual list in `SKILL.md` §7.
