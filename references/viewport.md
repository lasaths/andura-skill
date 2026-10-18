# ANDURA — 3D Viewport rules v1 (2026-10-18)
*Render: `layouts/viewport.png` (renderer `layouts/src/viewport.py`, reuses `common.cell_scene`). Top: desktop viewport with every navigation aid (FIT hovered, LAYERS open). Below: 12 rule panels. Sources: `research.md` §2.9, §3.5, §3.6, §3.7 (R) and `principles.md` §1 (S). [DC] = ANDURA design choice.*

**Why 3D at all:** ISA HP-HMI prefers 2D, low-contrast graphics for process screens. 3D is justified only for spatial robot state, and is then rendered desaturated (R §2.9, [ISA HP-HMI overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf)). Show only measured state, synoptic rather than photoreal ([SFTE ch. 21](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)).

Engine mapping (three.js, Babylon.js, Unity): `3d-engines.md`.

## 1. Camera and projection
| Rule | Spec | Basis |
|---|---|---|
| Projection | **Orthographic by default**: lengths are comparable, nothing is distorted, and it matches the 2D layouts. Perspective is an option in full-screen only (`V` toggles); the mode label shows it | R §3.6 (top-down/ortho toggle, NVIDIA placement check) [DC] |
| Home view | Ortho iso, 30° yaw, 30° elevation, whole cell plus 1 m margin, north/X to the right. Fixed per cell, the same on every device | consistency (Nielsen 4) |
| Standard views | View cube: TOP (7), FRONT (1), ISO (5), plus faces L/R/BACK by click; numpad keys as in CAD | recognition over recall |
| Reset | `H` / HOME button → home view, 300 ms ease-in-out (cut under reduced motion) | user control |
| Roll | **Never.** The up axis is locked; elevation is clamped to 5°–89° | disorientation prevention [DC] |

## 2. Navigation
| Input | Orbit | Pan | Zoom | Other |
|---|---|---|---|---|
| Mouse | left-drag | right-drag or Shift+left | wheel, zooms to the cursor | double-click = fit to object |
| Touch | 1 finger | 2 fingers | pinch | double-tap = fit · long-press 500 ms = peek |
| Keyboard | arrows | Shift+arrows | + / − | H home · F fit · A zoom to alarm · Tab cycles objects |
| Limits | elevation 5–89°, no roll | target clamped to cell + 2 m | 0.5–60 m distance, ortho scale 1:5–1:200 | |

Navigation never sends a robot command (layouts §Interaction).

## 3. Model, grid, light
- **Grey model:** geometry in neutral greys, no textures or PBR; materials only lift a face a little (`color.3d.face-1/2/3`: #141517 / #18191C / #1A1B1E; robots `color.3d.link`, `joint`, `base`). Colour appears only on abnormal parts (ISA, R §3.6).
- **Floor grid** 1 m, Line at 22 % opacity; safety fence dashed `color.3d.edge` (#55575C). **Lighting:** one soft key light plus ambient, no shadows, no bloom, no reflections [DC].

## 4. Selection, hover, status
- **Hover:** thin Text outline (1 px each side) plus a name tag. No fill change.
- **Select:** Ultramarine outline, 2.5 px each side. **Multi-select:** Shift-click or drag lasso; the context bar shows "2 SELECTED".
- **Status:** colour + glyph + word tag; Emergency/Caution rim on the object. **Rule 11: status is never hidden by selection.** Selected + status draws Ultramarine outside and the status rim inside (panel 03).
- **Commanded vs actual:** commanded = dashed Ultramarine 3 px; actual = solid Text 1.6 px on top. Deviation over the limit adds a Caution segment and tag (SFTE command/actual, R §3.6).
- **Stale:** pose older than 2 s → geometry Muted, hatch veil, stale glyph + age + last time. It is never extrapolated (NASA App F / SFTE, R §3.5).

## 5. Labels
Leader line plus box tag. Tags are placed in screen space, so they stay 12 px minimum at any zoom. At most **5 tags**; P1/P2 objects are always tagged, then the selection, then hover. The rest collapse to "+n LABELS ›". Tags never cover a selected or alarmed object: they move along their leader (8 px steps), then collapse [DC].

## 6. Data overlay
Layer off by default. **Cividis is the only data scale** ([Nuñez 2018](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199239), S11), for magnitudes like |deviation|. A legend with units is always shown. Alarm hues are never used for data.

## 7. Occlusion
- An alarmed object hidden behind geometry is drawn as an **x-ray outline** (dashed status colour) through occluders.
- **Ghost/isolate (`I`):** non-selected objects drop to 15 % opacity.
- An alarmed object outside the view gets an **edge chip** on the side where it lies (glyph + ID + ›). Click or `A` = zoom to alarm.

## 8. Navigation and interaction aids (main render)
Quiet by default: Muted, no fill. They show in Text on hover or need. 40 px on desktop, **56 px on touch**. On phone they fold into one "⋯ TOOLS" sheet, except the view cube and CLOSE.
| Aid | Where | Key | Principle |
|---|---|---|---|
| View-mode indicator ("ISO · ORTHO · FREE CAMERA · LAYERS 3/4 · SECTION OFF") | top-left, always visible | — | visibility of system status |
| View cube with TOP / FRONT / ISO | top-right | 7 / 1 / 5 | recognition over recall |
| HOME | rail | H | user control (undo for navigation) |
| FIT to selection | rail | F | Fitts (brings the target to you) |
| ZOOM TO ALARM (Emergency edge when an alarm is off-view) | rail + edge chip | A | visibility, error prevention |
| ISOLATE / ghost toggle | rail + context bar | I | focus, user control |
| SECTION plane (one plane, drag handle, readout) | rail | S | user control; Esc removes |
| MEASURE (snap, 1 mm readout) | rail | M | feedback; Esc clears |
| FOLLOW robot (target only; any manual move ends it) | rail | Shift+F | user control; mode label shown |
| LAYERS: robots, paths, elements, data overlay | rail → popover | L | recognition, minimalism |
| Context action bar: DETAIL › · ISOLATE · HIDE · PATH | bottom centre, fixed place | ↵ I Shift+H P | Fitts + consistency |
| Scale bar (1 m) + axis tripod (X, Y, Z·N) | bottom-left | — | orientation |
| Overview minimap with view frame and alarm dots (useful once the view is zoomed) | bottom-right | — | SA level 1 (Endsley) |
| Gesture legend on first use; `?` reopens | centre overlay | ? | help and documentation |
| Hover tooltip naming the tool and its key | next to the tool | — | recognition over recall |
Undo: navigation is undoable with `Backspace` (camera history, 20 steps) [DC]. Hide/isolate show a "SHOW ALL" chip until undone.

## 9. LOD and performance budget
| Item | Budget |
|---|---|
| Frame rate floor | **30 fps** for the 3D view (pose at frame rate, R §3.5); numbers beside it stay at 2–4 Hz |
| Frame time | ≤ 33 ms at p95 on the reference tablet |
| Degrade order (first → last) | 1 floor grid density → 2 path history length → 3 robot mesh LOD (3 levels by screen size) → 4 element detail (studs to boxes) → 5 data overlay resolution. **Never degraded:** selection, status rims, alarm tags, edge chips |
| If below the floor for 2 s | show "3D REDUCED" in the mode label; below 15 fps → freeze 3D, show "3D PAUSED · DATA LIVE" (values stay live) |

## 10. Per screen class
| Class | 3D |
|---|---|
| Desktop / tablet | full-bleed panel, all aids, view cube 96 px |
| Phone | L1 thumbnail 358 × 176, no gestures on the thumbnail (scrolling wins); "3D ›" → full-screen with CLOSE, RESET, selection bar, "⋯ TOOLS" sheet, view cube 56 px; band and tab bar stay |
| Wall | home view or follow only, no aids except the mode label and edge chips; alarm tags at wall type size |

## Risks / open
- 30 fps on tablets is unverified; it needs a profile on the real twin scene (mesh counts unknown).
- The x-ray outline through dense geometry may be noisy; validate it with real BIM elements.
- Perspective toggle and camera history are specified but not rendered.
