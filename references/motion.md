# ANDURA — Motion (locked)

> Provenance: paths under `layouts/` name the original design workspace and are not shipped. The renders are in `assets/`; runnable equivalents are `examples/`, `render/` and `scripts/`.
*Values: `motion.*` in `tokens/andura.tokens.json`. Storyboard `assets/motion.png` (renderer `layouts/src/motion.py`). Sources: research.md §3.5 (R), WCAG 2.3.1.*

**Rule 13: animate only where motion carries meaning** (alarm, state change, feedback). Never decorate (ISA HP-HMI, R §3.5). Animate opacity only; the camera transform is the one exception.

## Tokens
| Token | Value | Use |
|---|---|---|
| `duration.instant` | 0 ms | reduced motion, keyboard navigation, camera cut |
| `duration.fast` | 120 ms | peek in |
| `duration.fast-out` | 80 ms | peek out, hold-fill reset |
| `duration.base` | 200 ms | state change, column and level cross-fade, toast in and out |
| `duration.slow` | 400 ms | live to stale styling (noticeable, R §3.5) |
| `duration.camera` | 300 ms | home, fit, standard views, user-triggered only |
| `duration.hold` | 1500 ms | press-and-hold confirm |
| `duration.toast` | 4000 ms | toast dwell |
| `duration.pulse` | 1000 ms | P1 pulse period |
| `duration.peek-delay` / `long-press` | 300 / 500 ms | hover / touch before a peek |
| `easing.out` | (0.2, 0, 0, 1) | everything that appears or leaves |
| `easing.camera` | (0.4, 0, 0.2, 1) | camera |
| `easing.linear` | (0, 0, 1, 1) | hold fill opacity 0 → 1 (progress must be honest) |
The P1 pulse uses a sine curve between opacity 1.0 and `pulse-min-opacity` 0.35.

Every duration token is listed in `SKILL.md` rule 13; `toast`, `pulse`, `peek-delay` and `long-press` are component-only (toast, alarm band edge, peek).

## Behaviours
| Motion | Spec |
|---|---|
| **P1 pulse** | Opacity 100 → 35 → 100 %, 1 Hz sine, on the band glyph, edge bar and tab badge only. Stops on acknowledge (steady). Never for P2 or P3. The only loop in the product |
| **State-change fade** | New content fades in over 200 ms with ease-out while old content fades out. Values jump at 2–4 Hz and never tween |
| **Keyboard navigation** | Esc, Tab and shortcuts switch instantly (0 ms). Only mouse and touch get the cross-fade |
| **Peek** | Opens after 300 ms hover or 500 ms long-press, fades in over 120 ms, out over 80 ms. A second peek within 1000 ms of the last one opens with no delay and no fade |
| **Toast** | 200 ms in, 4000 ms dwell, 200 ms out. Never over the alarm band, one at a time, never for alarms. The timer pauses while the window is hidden |
| **Hold-to-confirm** | Ring and fill run linearly over 1500 ms. Release or drag-off before the end resets in 80 ms (slow deliberate phase, fast system response). Completion gives one haptic tick where supported, then the toast "P1 acked" |
| **Camera** | Home, fit and view cube: 300 ms, camera easing, target and zoom only, no roll, no fly-through. Zoom to alarm is a cut (0 ms). The camera never moves without a user action |
| **Live to stale** | 400 ms fade to Muted + hatch |
| **Interruption** | Every fade starts from the current opacity. Input is never blocked during a transition |
| **Hover** | Only on devices with a hover-capable pointer |

## Reduced motion (platform setting)
All fades become instant. The P1 pulse becomes a steady inverted chip (Emergency fill, Void text). The camera always cuts. The hold fill still goes from opacity 0 to 1, linearly, because it is the progress feedback.

## Forbidden
Bounce, slide, scale-in, springs with overshoot, parallax, spinners, looping decoration, camera fly-throughs, animated or counting numbers, shake and colour cycling. **Photosensitivity:** never more than 3 flashes in any 1 s ([WCAG 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold)). The 1 Hz pulse has soft edges and a small area, so it stays well under the limit.
