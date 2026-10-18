# ANDURA — Interaction, accessibility, do and don't

## 1. Interaction
| Step | Question | Mouse | Touch | Shows |
|---|---|---|---|---|
| Normal | Is the cell OK? | — | — | overview |
| Peek | What exactly is this value? | hover 300 ms | long-press 500 ms | tooltip with value, limit, time, age; nothing else moves |
| Inspect | What is this robot doing? | click | tap | Ultramarine outline; the answer column becomes the robot |
| Drill | How has it gone, what's next? | TIMELINE › or double-click | tap link | new level, breadcrumb, 3D shrinks to context |
- **Back:** `‹ destination` in a fixed spot. Esc, back or a breadcrumb goes up one step. Esc never acknowledges or cancels an alarm.
- **Selection:** one per screen, synced across 3D, lists, column, breadcrumb and timeline. Peek never selects. An alarm never steals selection.
- **Commands:** see SKILL.md hard rule 8. A confirm dialog opens with focus on CANCEL. Enter never confirms a destructive action.
- **Haptics:** where the device supports it, give one haptic tick when a hold completes. Nothing else vibrates.

## 2. Accessibility
- Text contrast 4.5:1 minimum (Text 15.05, Muted 6.24 on Void). Graphics 3:1 minimum (Ultramarine 3.27 on Void).
- Show a visible focus ring on every focusable element (WCAG 2.4.11 and 2.4.13). Keyboard order: top line, band, content, footer. Give every 3D action a key.
- Never use colour alone (SKILL.md hard rule 2). Selection = outline + square glyph. Current link = underline.
- Respect the platform reduced-motion setting (`motion.md`).
- Touch 56 px minimum, text 12 px minimum. The palette is CVD-checked (minimum dE 14 in all simulations); glyphs carry the rest.

## 3. Do and don't
| Do | Don't |
|---|---|
| Lead with the value and its limit | Show raw readings without a limit |
| Grey normal, colour the exception | Green RUNNING chips, zero-alarm badges |
| Group with whitespace | Box every panel |
| Sparkline with a dashed limit | Axis-heavy charts on overviews |
| `DEV`, `LIMIT 0.50 mm`, unit in SI case | Greek delta, "MM", mixed decimals |
| Fixed zones, fixed slots | Links that shift when one becomes active |
| Fade 120–200 ms, opacity only | Slide, bounce, spinner, pulse on P2 |
| Name the back destination | Bare "Back" or icon-only back |
| Ultramarine for selection only | Ultramarine for focus, status or decoration |
| Reflow layouts for tablet and phone | Squeeze the desktop canvas onto a phone |

**Press feedback:** show the pressed state on press-down, with no delay. Commit on release, and cancel when the pointer or finger leaves the target.

## Peek on truncated labels (text scaling)
When OS text size truncates a label (ellipsis), peek shows the full text: hover 300 ms on desktop, long-press 500 ms on touch. Peek never carries the only copy of a value; values do not truncate. Rules: `references/layouts.md` (Text scaling).
