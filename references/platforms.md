# ANDURA — Implementing on any platform
`tokens/andura.tokens.json` (W3C Design Tokens format) is the single source of truth. `python3 scripts/export_tokens.py` writes `tokens/build/andura.css`, `andura.ts`, `andura.py` and `Andura.cs`. Regenerate after every token change; never edit the build files.
| Platform | Consume the tokens as |
|---|---|
| Web (CSS) | custom properties `--andura-color-text`, `--andura-type-body-desktop-fontSize` |
| JS / TS | `import { andura } from "./andura"`; keys mirror the token path |
| Python (Qt, Dash, matplotlib) | `from andura import ANDURA`; convert px to the toolkit unit |
| C# / WPF | static class `Andura`; or load the values into a `ResourceDictionary` (1 px = 1 DIP) |
| Unity | read the JSON at build time into a ScriptableObject; draw UI in screen space, never world space, so sizes stay in px |
| Three.js / WebGL | use the CSS or TS export for the HUD; set outline widths in screen px (not world units) so 2.5 px stays 2.5 px at any zoom |

These must hold on every platform:
- **Units:** px = device-independent pixels. Scale the wall by visual angle (`typography.md` §8), never by a guessed factor.
- **Fonts:** embed IBM Plex Sans and Mono. Enable tabular figures and slashed zero. Never fall back silently; if a fallback renders, fail the build or log it.
- **Colour space:** sRGB hex as given. No HDR boost, no tone mapping on UI.
- **Selection and status in 3D** are screen-space overlays drawn above the scene, so lighting and depth never dim them.
- **Reduced motion and hover capability** come from the OS or platform setting.
- **Hit targets** are measured in px after scaling, not in world units.
