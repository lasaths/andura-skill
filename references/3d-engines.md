# ANDURA — 3D engines: three.js, Babylon.js, Unity

How to implement the engine-neutral viewport rules (`viewport.md`) in three engines. The rules decide; this file only maps them. Every colour, width and duration comes from the token exports (`tokens/build/andura.ts`, `Andura.cs`), never typed by hand. APIs checked against the official docs on 2026-10-18: three.js r17x (OrbitControls, Raycaster, LineMaterial, CSS2DRenderer, ViewHelper), Babylon.js 8 (ArcRotateCamera, `scene.pick`, SelectionOutlineLayer, GUI `linkWithMesh`), Unity 6 (Cinemachine 3 `CinemachineOrbitalFollow`, `Physics.Raycast`, UI Toolkit `RuntimePanelUtils.CameraTransformWorldToPanel`, URP).

## 1. Rule → engine map
| Rule (`viewport.md`) | three.js | Babylon.js | Unity |
|---|---|---|---|
| Ortho by default, home = iso 30° / 30° | `OrthographicCamera`; `controls.saveState()` at home, `controls.reset()` for HOME | `camera.mode = Camera.ORTHOGRAPHIC_CAMERA`, `orthoLeft/Right/Top/Bottom`; `storeState()` / `restoreState()` | `Camera.orthographic = true`, `orthographicSize`; Cinemachine camera with a home preset |
| No roll; elevation 5–89° | `minPolarAngle = 1°`, `maxPolarAngle = 85°` (polar = 90° − elevation) | `lowerBetaLimit` / `upperBetaLimit` (beta from +Y, same conversion); `allowUpsideDown = false` | `CinemachineOrbitalFollow.VerticalAxis.Range = (5, 89)`; never rotate the camera's Z |
| Target clamped to cell + 2 m | `controls.cursor = cellCentre`, `maxTargetRadius = cellRadius + 2` | `panningDistanceLimit = cellRadius + 2`, `panningOriginTarget = cellCentre` | clamp the follow target's position in `LateUpdate` |
| Distance 0.5–60 m | `minDistance` / `maxDistance` (perspective) or `minZoom` / `maxZoom` (ortho) | `lowerRadiusLimit` / `upperRadiusLimit` | `RadialAxis.Range`, or clamp `orthographicSize` |
| Zoom to cursor | `zoomToCursor = true` | `zoomToMouseLocation = true` | move the target toward the ray hit before zooming |
| HOME 300 ms ease-in-out, cut under reduced motion | tween camera + target over `motion.duration.camera`; 0 if `prefers-reduced-motion` | `camera.interpolateTo(…)`, or set directly when reduced | tween over `Andura.MotionDurationCamera`, or set directly |
| Picking (click/tap selects, never commands) | `Raycaster.setFromCamera(ndc, camera)` → `intersectObjects` | `scene.pick(scene.pointerX, scene.pointerY)` | `Physics.Raycast(cam.ScreenPointToRay(pointer), out hit)` |
| Selection outline 2.5 px Ultramarine, screen-constant | `LineMaterial({ linewidth: 2.5, worldUnits: false })` on the body's edges (`Line2` / `LineSegments2`), or `OutlinePass` with `edgeThickness` | `SelectionOutlineLayer`: `outlineThickness = 2.5`, `outlineColor` = ultramarine, `addSelection(mesh)` | URP renderer feature (rendering layer mask + full-screen outline pass) with a pixel width = `Andura.SizeOutlineSelect3d` |
| Status rim inside the outline (rule 3) | second `LineMaterial`, `linewidth = size.stroke-rim`, status colour, drawn after the outline | `mesh.enableEdgesRendering()`, `edgesColor` = status colour; keep the outline layer for selection | second pass / material on the same rendering layer, status colour |
| Hover: 1 px Text outline | `linewidth: 1`, Text colour | second `SelectionOutlineLayer` with `outlineThickness = 1` | same feature, 1 px |
| Tags in screen space, ≥ 12 px, max 5 | `CSS2DRenderer` + `CSS2DObject(div)` (HTML tags use the CSS recipes) | GUI `AdvancedDynamicTexture.CreateFullscreenUI`, `control.linkWithMesh(mesh)`, `linkOffsetY` | UI Toolkit label positioned with `RuntimePanelUtils.CameraTransformWorldToPanel(panel, worldPos, cam)` |
| View cube TOP / FRONT / ISO | `ViewHelper` (axes; add TOP/FRONT/ISO buttons as HTML) | a small second viewport or HTML buttons calling `interpolateTo` | UI Toolkit buttons that set the orbit axes |
| X-ray outline of an occluded alarm | `LineMaterial` with `depthTest = false`, `dashed = true`, status colour | `SelectionOutlineLayer` option `useDepthOcclusion = false` on a second layer | outline pass with depth test off, dashed |
| Frame budget (`viewport.md` §9) | `renderer.info`, render on demand (`controls` `change` event) | `scene.freezeActiveMeshes()` for static parts, `engine.getFps()` | URP SRP Batcher, render on demand where possible |

Navigation never sends a robot command in any engine: picking only selects; commands go through the HMI's command path (hard rule 8).

## 2. Colours and widths from tokens
Read the exported tokens once and convert; never paste hexes.

**three.js** (TypeScript):
```ts
import { andura } from "../tokens/build/andura";
import { Color } from "three";
import { LineMaterial } from "three/addons/lines/LineMaterial.js";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
const deg = Math.PI / 180;
export const selectMat = new LineMaterial({ color: new Color(andura["color-ultramarine"]), linewidth: andura["size-outline-select-3d"], worldUnits: false });
export const rimMat = (p1: boolean) => new LineMaterial({ color: new Color(andura[p1 ? "color-emergency" : "color-caution"]), linewidth: andura["size-stroke-rim"], worldUnits: false });
export function limits(c: OrbitControls, cellRadius: number) {
  c.minPolarAngle = 1 * deg; c.maxPolarAngle = 85 * deg;      // elevation 5–89°
  c.maxTargetRadius = cellRadius + 2; c.zoomToCursor = true;   // target within cell + 2 m
}
```
(`LineMaterial.resolution` must track the canvas size, as the docs require.)

**Babylon.js** (TypeScript):
```ts
import { andura } from "../tokens/build/andura";
import { ArcRotateCamera, Color3, SelectionOutlineLayer, Scene } from "@babylonjs/core";
export function setup(scene: Scene, cam: ArcRotateCamera, cellRadius: number) {
  cam.lowerBetaLimit = 1 * Math.PI / 180; cam.upperBetaLimit = 85 * Math.PI / 180; cam.allowUpsideDown = false;
  cam.panningDistanceLimit = cellRadius + 2; cam.lowerRadiusLimit = 0.5; cam.upperRadiusLimit = 60; cam.zoomToMouseLocation = true;
  const sel = new SelectionOutlineLayer("select", scene);
  sel.outlineColor = Color3.FromHexString(andura["color-ultramarine"]); sel.outlineThickness = andura["size-outline-select-3d"];
  scene.onPointerDown = () => { const hit = scene.pick(scene.pointerX, scene.pointerY); sel.clearSelection(); if (hit?.pickedMesh) sel.addSelection(hit.pickedMesh); };
}
```

**Unity** (C#):
```csharp
using UnityEngine;
public static class AnduraUnity
{
    public static Color C(string hex) { ColorUtility.TryParseHtmlString(hex, out var c); return c; }
    public static readonly Color Selection = C(Andura.ColorUltramarine);
    public static readonly Color P1 = C(Andura.ColorEmergency), P2 = C(Andura.ColorCaution);
    public static float OutlinePx => Andura.SizeOutlineSelect3d;   // feed the URP outline feature in pixels
    public static Transform Pick(Camera cam, Vector2 pointer) =>
        Physics.Raycast(cam.ScreenPointToRay(pointer), out var hit) ? hit.transform : null;  // selects; never commands
}
```
Sunlit mode (`colour.md` §9): swap in `anduraSunlit` / `AnduraSunlit` values for the same keys, including `3d.*`.

## 3. What stays out of the engine
Band, top line, footer, tags' text style and every value readout stay in the HMI layer (HTML, WPF, UI Toolkit) so the persistent-zone and touch rules hold and `scripts/andura_check.py` can test them. The engine draws geometry, rims, outlines, the commanded path and the x-ray outline only.

Sources: three.js docs (threejs.org/docs: OrbitControls, LineMaterial, ViewHelper, Raycaster, CSS2DRenderer); Babylon.js docs (doc.babylonjs.com: ArcRotateCamera, Selection Outline Layer, GUI Control `linkWithMesh`); Unity 6 manual and Cinemachine 3.1 API (`CinemachineOrbitalFollow`), `RuntimePanelUtils`.
