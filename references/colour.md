# ANDURA — Colour (palette v2.2, locked)

> Provenance: paths under `layouts/` name the original design workspace and are not shipped. The renders are in `assets/`; runnable equivalents are `examples/`, `render/` and `scripts/`.
*Source of truth: `assets/pal-v2.2.json` (scripts `v2.2/pal.py`, `v2.2/render.py`). Swatch `assets/swatch-v2.2.png`. History: v1 had 14 colours; v2 cut it to 9; v2.1 deepened Ultramarine; v2.2 darkened Surface and lifted Line.*

## 1. Palette
| Token | Hex | OKLCH | Role |
|---|---|---|---|
| Void | `#000000` | 0 0 0 | Outer canvas |
| Surface | `#090A0C` | .145 .004 272 | The only raised layer: 3D viewport, alarm band, popovers |
| Surface Hover | `#141518` | — | Hover lift (never the only signifier) |
| Surface Lift | `#1A1B1E` | — | Active tool, toast background |
| Line | `#3C3D41` | .360 .007 272 | Hairlines, grid, separators, panel edges (non-text) |
| Muted | `#8A8C91` | .640 .008 272 | Labels, units, secondary text, stale values |
| Text | `#DADADD` | .890 .004 272 | Values, primary text, actual traces, focus ring |
| Ultramarine | `#3A3CFF` | .510 .274 271 | Selection, commanded path, primary button fill. Never text |
| Ultramarine Text | `#5A74F1` | .605 .190 271 | Accent text and links only |
| Emergency | `#F45536` | .660 .200 33 | P1 emergency, protective stop |
| Caution | `#FBB636` | .820 .155 78 | P2 caution, limit approach |
| Nominal | `#44B782` | .700 .130 160 | Explicit confirmation on detail levels only; never on overviews |

## 2. Contrast (WCAG ratio)
| Token | Hex | OKLCH | vs Void | vs Surface |
|---|---|---|---|---|
| Surface | `#090A0C` | .145 .004 272 | 1.06 | 1.00 |
| Line | `#3C3D41` | .360 .007 272 | 1.94 | 1.83 |
| Text | `#DADADD` | .890 .004 272 | 15.05 | **14.20** AAA |
| Muted | `#8A8C91` | .640 .008 272 | 6.24 | **5.89** AA |
| Ultramarine Text | `#5A74F1` | .605 .190 271 | 5.20 | **4.91** AA |
| Emergency | `#F45536` | .660 .200 33 | 6.20 | **5.85** AA |
| Caution | `#FBB636` | .820 .155 78 | 11.85 | **11.17** AAA |
| Nominal | `#44B782` | .700 .130 160 | 8.34 | **7.87** AAA |
| Ultramarine (graphic) | `#3A3CFF` | .510 .274 271 | 3.27 | **3.08** passes 3:1 (WCAG 1.4.11) |

All text tokens pass AA on both layers. Ultramarine is a graphic colour (≥ 3:1, WCAG 1.4.11); strokes ≥ 2 px; 3D selection outline 2.5 px; commanded path dashed 3 px.

## 3. Rules
1. **Pure black canvas, never pure white text.** The user chose `#000000`. To limit halation (bright text blooming on black, worse with astigmatism), text is capped at OKLCH L 0.89 (Text `#DADADD`, 15.05:1). No pure white anywhere ([LookUp, OLED dark theme](https://medium.com/lookup-design/designing-a-dark-theme-for-oled-iphones-e13cdfea7ffe) [excerpt]; [vocab.design true-black](https://vocab.design/true-black-theme) [excerpt]; SFTE avoids stark white because of ghosting, [SFTE ch.21](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)).
2. **Desaturated, lighter accents on dark.** Saturated colours vibrate on dark backgrounds. Use lighter, less saturated tones ([Material dark theme](https://m2.material.io/develop/android/theming/dark), [Material codelab](https://codelabs.developers.google.com/codelabs/design-material-darktheme) [excerpt]). Status hues sit at L 0.66–0.82, chroma ≤ 0.20, and clear 4.5:1 on Void and Surface.
3. **Normally dark: grey means normal.** Colour appears only for abnormal states, and green never means "running" ([ISA HP-HMI overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf); [ISA InTech 2023](https://www.isa.org/intech-home/2023/april-2023/features/how-dcs-migration-improves-operator-experience); [ASM grey backgrounds](https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/white-papers/February%2028%202011%20-%20Why%20Gray%20Backgrounds%20for%20DCS%20Operating%20Displays.pdf)).
4. **Fixed alert colours.** Red is warning/emergency, yellow/amber is caution, blue is advisory (NASA). FAA uses red for warnings and amber for cautions, and requires consistent red/amber use under §25.1322 ([NASA-STD-3001 V2 App. F](https://www.nasa.gov/reference/appendix-f-vol-2/) [excerpt]; [FAA AC 25-11B §5.8, Table 5-1](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_25-11b.pdf)). These hues are reserved for alerts and are never used for decoration, series or brand.
5. **Never colour alone.** Every status carries a shape and a word ([NASA-STD-3001 V2 10045](https://www.nasa.gov/reference/10-0-crew-interfaces-vol-2/); [AC 25-11B §5.8.1](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_25-11b.pdf); SFTE §21.2). Status uses a glyph and edge bar, not only coloured numerals on black (SFTE §21.2.1).
6. **MIL-STD-1472 hue shifts.** Red shifts toward orange (255,65,30) and green toward blue (17,192,130) for CVD (via [SFTE §21.2](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html); the primary standard is paywalled). Emergency H33 and Nominal H160 follow this.
7. **Build in OKLCH.** Lightness and chroma are perceptually uniform, so steps are predictable across hues ([Ottosson, Oklab](https://bottosson.github.io/posts/oklab/); [Evil Martians, OKLCH in CSS](https://evilmartians.com/chronicles/OKLCH-in-css-why-quit-rgb-hsl); [Harmonizer](https://github.com/evilmartians/harmonizer/blob/main/README.md)). Neutrals carry a faint cool tint (H272, C ≤ 0.008). All values are inside the sRGB gamut (asserted in code).
8. **Data scales** must be perceptually uniform and CVD-safe. No rainbow or jet ([Crameri et al. 2020, Nat. Commun.](https://www.nature.com/articles/s41467-020-19160-7); [Crameri colour maps](https://www.fabiocrameri.ch/colourpalettes/); [viridis, BIDS](https://bids.github.io/colormap/); [cividis, Nuñez et al. 2018](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199239); [Moreland diverging maps](https://www.kennethmoreland.com/color-maps/)).
9. **Selection is an outline, never a fill;** status is drawn as an outline or rim plus glyph and word, never by tinting a whole mesh or row.

## 4. Situational use
| Situation | Treatment |
|---|---|
| Normal running | Greys only. Values in Text, labels in Muted. No Nominal green |
| Selected object | Ultramarine 2 px outline (3D: 2.5 px) + label |
| Keyboard focus | 2 px Text ring, 2 px gap (§6) |
| Commanded vs actual | Commanded = dashed Ultramarine; actual = solid Text on top. Gap > tolerance → Caution segment + tag |
| Stale (no update > n s) | Muted value + diagonal Line hatch + stale glyph + age stamp. Never a fresh colour on old data |
| Invalid / comms lost | Value replaced by "---" + ⊘ glyph; Emergency if safety-relevant, else Muted |
| P3 advisory | Text + circle-i glyph + ADVISORY |
| P2 caution | Caution triangle glyph + CAUTION + edge bar; 3D Caution rim |
| P1 emergency | Emergency octagon glyph + EMERGENCY + edge bar pulsing 1 Hz until ack; 3D Emergency rim |
| Selected + status | Ultramarine outside, status rim inside (status is never hidden) |
| Completed / verified | Small Nominal check glyph, detail levels only |
| Alarm flood | Ladder unchanged; P3 colour suppressed so P1/P2 stay salient |

## 5. 3D and data
- **3D twin:** greys only (context darkest, robot Muted, as-built Text, as-designed Line wireframe) plus the Ultramarine selection outline. Status overlays use the status colours as rims and tags.
- **Data scale (only one): cividis**, for magnitudes such as heatmaps and abs DEV. The sign of a deviation is shown with a +/− glyph and labels.: density, load, cycle time, progress):** cividis, trimmed to 0.12–1.0 so the low end lifts off black. Stops: `#163770 #47516C #696B71 #8B8778 #AFA471 #D7C45C #FEE838`. Cividis is optimised so deuteranomalous and normal viewers read it almost identically, and it rises in brightness linearly ([Nuñez 2018](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199239)). Viridis is the fallback ([BIDS](https://bids.github.io/colormap/)). Note: the lowest stop is only about 1.8:1 on Void. On flat 2D charts put it on Surface or a Line outline.
- Never use alarm hues for data, decoration, series or brand.

## 6. Focus ring vs selection
**Keyboard focus = 2 px solid Text `#DADADD` ring with a 2 px gap outside the target.**
- **Why:** selection is Ultramarine `#3A3CFF` (outline, glyph). Focus differs from it in hue, luminance and position (outside ring vs the element's own outline), so the two are never confused.
- **WCAG 2.4.11 Focus Not Obscured (AA):** the ring is drawn outside the element on a z-layer above content, and tooltips never cover a focused element. **2.4.13 Focus Appearance (AAA):** the area is a 2 px perimeter, ≥ the 2 CSS px perimeter minimum. The focused-vs-unfocused change is #000 → #DADADD = **15.05:1 on Void, 14.20:1 on Surface (v2.2)** (needs ≥ 3:1). Against the Ultramarine selection outline it is ≈4.6:1 (needed when focus and selection sit on the same element).
- Implemented in `layouts/src/L1min_parts.py` (`focus_ring`, footer `focus=`); drawn in `L1-min-focus.png`, `L3-min.png` (card) and `L5-min.png` (row).

## 7. Colour-blind check (Machado 2009 severity 100, CAM02-UCS, from `pal-v2.2.json`)
| Vision | Weakest pairs (dE) |
|---|---|
| Normal | Ultramarine/Ultramarine Text 15.0 · Nominal/Muted 26.2 · Emergency/Caution 31.0 |
| Protan | Caution/Nominal 18.7 · Nominal/Muted 19.9 · Emergency/Nominal 21.6 |
| Deutan | Nominal/Muted 14.1 · Emergency/Nominal 17.2 · Emergency/Caution 18.0 |
| Tritan | Ultramarine Text/Nominal 16.3 · Ultramarine/Nominal 26.4 · Emergency/Caution 27.4 |
Ultramarine vs Emergency and Caution stays ≥ 51 in every simulation. Ultramarine and Ultramarine Text are one hue by design (never both meaning different things). Weak status pairs are covered by glyph + word.

## 8. Sources
- NASA-STD-3001 Vol 2 App. F (alert classes/colours): https://www.nasa.gov/reference/appendix-f-vol-2/ [excerpt] · Vol 2 §10 (V2 10045 colour redundancy): https://www.nasa.gov/reference/10-0-crew-interfaces-vol-2/ · HIDH Rev 1 (Ch. 10 displays, C&W): https://www.nasa.gov/wp-content/uploads/2015/03/human_integration_design_handbook_revision_1.pdf · NASA Ames Color Usage: https://colorusage.arc.nasa.gov/ [excerpt]
- FAA AC 25-11B §5.8, Tables 5-1/5-2: https://www.faa.gov/documentlibrary/media/advisory_circular/ac_25-11b.pdf · FAA HF flight-deck guide §3.7 Color: https://hfcc.dot.gov/publications/docs/GeneralGuidance/zz_FAA_GeneralGuidanceDoc_Chapter_03_Section_07.pdf
- MIL-STD-1472 colour shifts, via SFTE handbook ch.21: https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html
- ISA-101 / HP-HMI: https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf · https://www.isa.org/intech-home/2023/april-2023/features/how-dcs-migration-improves-operator-experience · ASM grey backgrounds: https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/white-papers/February%2028%202011%20-%20Why%20Gray%20Backgrounds%20for%20DCS%20Operating%20Displays.pdf
- IBM Carbon colour: https://www.carbondesignsystem.com/building-blocks/foundations/color/overview · data-viz palettes: https://www.carbondesignsystem.com/building-blocks/data-visualization/color-palettes · chart themes: https://charts.carbondesignsystem.com/themes
- Material dark theme: https://m2.material.io/develop/android/theming/dark · codelab: https://codelabs.developers.google.com/codelabs/design-material-darktheme [excerpt]
- Apple HIG Dark Mode: https://developer.apple.com/design/human-interface-guidelines/dark-mode [excerpt; read via mirror] · WWDC19 Implementing Dark Mode: https://developer.apple.com/videos/play/wwdc2019/214/
- Okabe-Ito / Color Universal Design: https://jfly.uni-koeln.de/color/index.html · https://matplotlib.org/devdocs/release/next_whats_new/okabe_ito_colormap.html
- OKLCH/Oklab: https://bottosson.github.io/posts/oklab/ · https://evilmartians.com/chronicles/OKLCH-in-css-why-quit-rgb-hsl · https://github.com/evilmartians/harmonizer/blob/main/README.md
- Halation and OLED smearing: https://medium.com/lookup-design/designing-a-dark-theme-for-oled-iphones-e13cdfea7ffe · https://vocab.design/true-black-theme [both practitioner sources, not standards]
- Scales: cividis https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199239 · viridis https://bids.github.io/colormap/ · Crameri 2020 https://www.nature.com/articles/s41467-020-19160-7 · https://www.fabiocrameri.ch/colourpalettes/ · Moreland https://www.kennethmoreland.com/color-maps/
- WCAG 2.2: https://www.w3.org/TR/WCAG22/ · 1.4.11: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html · 2.3.1: https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold
- CVD model: colorspacious (Machado 2009), as used by Nuñez 2018.
