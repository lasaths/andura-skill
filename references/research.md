# ANDURA — Research Brief
*Dark-mode design guideline for 3D digital-twin dashboards in robotic construction (live robot monitoring, design→fabrication data lineage, analytics)*
Compiled 2026-10-17. Base skill: `/home/box/agent-data/workflows/nothing-design/` (SKILL.md + references/tokens.md, components.md, platform-mapping.md).

> **How to read the citations.** Every external claim has a URL. Where a source was only seen as a search excerpt or summary and not read in full, it is marked **[excerpt]**. Treat those as leads to check before you rely on them for anything normative. Paywalled standards (ISA-101, ISA-18.2, EEMUA 191, ISO 10218, MIL-STD-1472) are cited through the publisher's preview or overview, or through practitioner summaries, and not from the full text. Sections 3–5 are ANDURA design rules **derived** from those sources. Each rule names the source it comes from. Where a rule is a design choice and not a sourced fact, it says so (*design choice*).

---

## 1. The nothing-design base skill

### 1.1 Core rules (as written in the skill files)
| Area | Rule |
|---|---|
| Philosophy | "Subtract, don't add." "Monochrome is the canvas. Color is an event." Type does the hierarchy, not color, icons or borders. Equal dark (OLED black) and light modes. |
| Hierarchy | Exactly 3 layers (primary / secondary / tertiary). Run the squint test. |
| Type | Doto (dot-matrix display, 36px+ only), Space Grotesk (UI), Space Mono (data/labels, ALL CAPS, 0.06–0.1em tracking). Per screen: at most 2 families, 3 sizes, 2 weights. Scale runs 72/48/36/24/18/16/14/12/11 px. |
| Color | Dark: `#000` bg, `#111`/`#1A1A1A` surfaces, `#222`/`#333` borders, text `#666/#999/#E8E8E8/#FFF`. One accent red `#D71921` as an "interrupt". Status colors: success `#4A9E5C`, warning `#D4A843`. Color goes on the **value**, not the label or row background. Interactive blue `#5B9BF6`. |
| Spacing | 4/8/16/24/32/48/64/96 px. Spacing carries meaning. "If a divider is needed, spacing is probably wrong." Containers in order of preference: spacing, then divider, then border, then card. |
| Components | Pill or technical buttons (min 44 px). Underline inputs. Stat rows (label left, value right). Tables (numbers right-aligned, no zebra rows). Segmented progress bars as the signature visual. Gauges with numeric readouts. "Always show numeric value alongside any visual". |
| Restraint | No gradients, shadows, blur, toasts, skeletons, filled icons, bounce easing or parallax. Exactly ONE "pattern break" per screen. Asymmetric layouts. Motion 150–400 ms ease-out, opacity over position. Charts separate series by opacity, then pattern, then color. |

### 1.2 Keep / Adapt / Drop for mission-critical dark dashboards
| Verdict | Item | Why (source) |
|---|---|---|
| **KEEP** | Monochrome base, color as event | Matches ISA-101 / high-performance HMI: grey graphics, color only for abnormal ([ISA HP-HMI overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf); [ISA InTech 2023](https://www.isa.org/intech-home/2023/april-2023/features/how-dcs-migration-improves-operator-experience)) |
| KEEP | Grey-scale contrast as hierarchy (critical = highest contrast) | SFTE real-time display guidelines §21.1.2.2 ([SFTE handbook ch.21](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)) |
| KEEP | Numeric value paired with every graphic | SFTE §21.1.2.5 ("Graphics should always include a numerical value") (same URL) |
| KEEP | Monospace data, ALL-CAPS labels | SFTE §21.1.2.4: acronyms, button labels and annunciators in ALL CAPS (same URL) |
| KEEP | No gratuitous animation | HP-HMI: "No animation except for specific alarm-related graphic behavior" ([ISA overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf)) |
| KEEP | No toasts; inline status | Transient popups can disappear before they are read. NASA requires alerts to persist in a queue with ack state ([NASA-STD-3001 Vol 2 App. F](https://www.nasa.gov/reference/appendix-f-vol-2/)) **[excerpt]** |
| **ADAPT** | Pure `#000` OLED background | Material recommends `#121212` over pure black for depth and less eye strain ([Material dark theme](https://m2.material.io/develop/android/theming/dark)) **[excerpt]**. The ASM Consortium recommends grey backgrounds in control rooms ([Honeywell/ASM white paper](https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/white-papers/February%2028%202011%20-%20Why%20Gray%20Backgrounds%20for%20DCS%20Operating%20Displays.pdf)). SFTE avoids stark white to reduce "ghosting" ([SFTE](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)). → Use a dark grey base and cap text below pure white. |
| ADAPT | Single accent red = everything urgent | Needs a formal priority ladder: NASA uses red for Emergency/Warning, yellow for Caution, blue for Advisory ([App. F §F.6.4](https://www.nasa.gov/reference/appendix-f-vol-2/)). |
| ADAPT | "Green = success" status color | HP-HMI: using green for normal "running" hides abnormal states ([Nasby HP-HMI slides](https://grahamnasby.com/files_publications/NasbyG_2017_HighPerformanceHMIs_IntelligentWastewaterSeminar_WEAO_sept14-2017_slides-public.pdf)). Red/green is the most common CVD confusion ([SFTE §21.2](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)). → Normal stays grey. |
| ADAPT | Color on the value only | SFTE: colored green/yellow/red numerals on black "should be avoided" for CVD users. Add a fill, box or icon ([SFTE §21.2.1](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)). |
| ADAPT | 3-size type budget and vast whitespace | Control rooms need density. SFTE still targets ≥40% empty space ([SFTE §21.1.2.1](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)). → Keep the budget per *panel*, not per wall. |
| ADAPT | Opacity-first series coding | Fine for analytics. Live status must use redundant coding (color + shape + text) ([NASA-STD-3001 V2 10045](https://www.nasa.gov/reference/10-0-crew-interfaces-vol-2/)). |
| ADAPT | 44 px touch targets | Gloves need larger targets (Dragon style guide covered "touch targets for astronaut gloves", [Fitzpatrick](https://www.andrewjfitzpatrick.com/portfolio-spacex.html)). Headsets need ≥60 pt spacing ([Apple visionOS HIG](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos)) **[excerpt]**. |
| **DROP** | Doto dot-matrix for values | Decorative display face, poorer digit discrimination (*design choice*). Use tabular sans or mono numerals instead ([MDN tabular-nums](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric)). |
| DROP | "One surprise per screen" and deliberate asymmetry as aesthetics | In ops UIs, salience is reserved for abnormal states (HP-HMI). Layout should follow the operator's mental model and stay stable ([Few, real-time SA](https://www.perceptualedge.com/articles/Whitepapers/Dashboard_Design.pdf)) **[excerpt]**. |
| DROP | "No expand/collapse, indentation is hierarchy" | Drill-down hierarchy is required ([ISA-101 levels](https://www.yokogawa.com/us/library/resources/media-publications/isa-101-toward-a-more-effective-hmi-strategy/)) **[excerpt]**. |
| DROP | Mandatory light mode parity | Out of scope (dark-mode skill). |

---

## 2. Research findings

### 2.1 NASA human factors (NASA-STD-3001, HIDH)
- **Alert classes and colors:** Emergency and Warning use red symbology/text, Caution uses yellow, Advisory uses blue. The alerts display shows counts per class, unacknowledged count and a queue. Each event shows priority, name, ID, timestamp, system, active state, annunciation state (inhibit/suppress), ack state and root cause. Events are sortable and link to malfunction procedures. Allowed actions are acknowledge, suppress, inhibit and enable. A yellow or red up/down arrow next to a telemetry value marks an exceeded threshold. — [NASA-STD-3001 Vol 2 Appendix F](https://www.nasa.gov/reference/appendix-f-vol-2/) **[excerpt]**
- **Distinct, dual-coded alerts:** [V2 10114] requires distinct visual *and* audio annunciation for emergency, warning and caution. **Color redundancy:** [V2 10045] requires "an additional cue when color is [used] to convey meaning for critical information". Indicator colors must be distinguishable, e.g. "yellow is not confusable with green". — [NASA-STD-3001 Vol 2 §10](https://www.nasa.gov/reference/10-0-crew-interfaces-vol-2/)
- The HIDH (NASA/SP-2010-3407) covers displays, C&W, information management, automated systems and mobile systems in Chapter 10. — [HIDH Rev 1 PDF](https://www.nasa.gov/wp-content/uploads/2015/03/human_integration_design_handbook_revision_1.pdf)
- **Lessons learned (NASA CLDP HSI workshop):** "Use color sparingly… drawing attention to fault conditions or alerts". "Avoid dense displays and overuse of color". "Make sure controls provide feedback". Display colors changed when viewed off-angle. "Confusing color use resulted in a near failed verification task". — [NASA NTRS 20240003566](https://ntrs.nasa.gov/api/citations/20240003566/downloads/CLD%20HSI%20Workshop%20Crew%20Interfaces.pdf)
- NASA Ames Color Usage site: guidance on color in display graphics; luminance contrast is the main driver of legibility. — [colorusage.arc.nasa.gov](https://colorusage.arc.nasa.gov/) **[excerpt]**

### 2.2 Real-time telemetry displays (control room / flight test), the closest analog to mission control
From the SFTE Flight Test Engineering Reference Handbook ch. 21, which covers aircraft and telemetry control-room displays and cites MIL-STD-1472, the NASA JSC HCI guide and NASA Ames — [SFTE ch.21](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html):
- ≤ ~60% of the screen occupied (≥40% empty).
- Contrast is the *primary* cue and color is *secondary*. Critical elements get the highest contrast.
- ≤ 4–5 distinct colors besides background and data colors.
- Don't assign limits arbitrarily. If there is no engineering limit, show the data as "no limits" (neutral).
- Update rate ≤ 8–10 Hz. Filter numerics to 2–4 Hz to avoid flicker, while keeping data visibly "alive".
- ≤ 4 actively monitored critical parameters per person. Automate the rest with alerting.
- Show the commanded value hollow and the actual value filled.
- Clearly show transition and invalid-signal states.
- Values increase clockwise, up or right. Numeric boxes stay stationary.
- Prefer synoptic over photo-real depiction.
- "Normally dark" philosophy: annunciate only off-nominal.
- Toggles for on/off. Labels are verbs (actions) or states.
- Version-control displays and validate them on recorded data.
- Advisory / Caution / Warning definitions (warning = immediate action required).

**SpaceX Crew Dragon:**
- Chromium/JS is used only as a rendering layer. Fault-tolerant flight software sits outside the display boundary. "Just a few buttons for very mission-critical operations." Minimum crew interaction was a success criterion. — [InfoQ](https://www.infoq.com/news/2020/06/javascript-spacex-dragon/), [Hackaday](https://hackaday.com/2020/06/08/displaying-html-interfaces-and-managing-network-nodes-in-space/), [RocketSTEM](https://www.rocketstem.org/2020/11/12/from-cell-phones-to-spacecraft-touchscreens-are-taking-over-ui/)
- A physical panel below the touchscreens handles abort and emergencies. — [Hackaday](https://hackaday.com/2020/06/08/displaying-html-interfaces-and-managing-network-nodes-in-space/)
- The style guide covered glove touch targets and legibility under vibration. — [Fitzpatrick portfolio](https://www.andrewjfitzpatrick.com/portfolio-spacex.html)

### 2.3 ISA-101 high-performance HMI
- HP graphics use limited, consistent color, grey backgrounds to minimise glare, no animation except alarm behavior, embedded trends, and analog indication of value relative to normal/abnormal/alarm ranges. They follow a display hierarchy with progressive exposure of detail, use **low-contrast 2-D, not 3-D**, keep navigation consistent and embed context such as alarm rationale and SOPs. Anti-patterns: spinning pumps, colorful 3-D vessels, highly detailed equipment, misuse of alarm colors, no hierarchy. "Color, by itself, is [not sufficient]". — [ISA HP-HMI Overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf)
- ISA-101 practice is a grey palette with sparse color that draws attention to abnormal situations. — [ISA InTech Apr 2023](https://www.isa.org/intech-home/2023/april-2023/features/how-dcs-migration-improves-operator-experience)
- "Happy plant = no alarms, no colour". Show alarms through color, shape and text ("redundant coding"). Color change is poorly detected in peripheral vision. — [Nasby 2017](https://grahamnasby.com/files_publications/NasbyG_2017_HighPerformanceHMIs_IntelligentWastewaterSeminar_WEAO_sept14-2017_slides-public.pdf); [IPD white paper](https://resources.ipd.com.au/documents/white-papers/Best-practices-for-high-performance-HMI-design_White%20Paper_ENUS_2023.pdf)
- "Data is not information": provide scale, desirable operating range and alarm range. — [IPD white paper](https://resources.ipd.com.au/documents/white-papers/Best-practices-for-high-performance-HMI-design_White%20Paper_ENUS_2023.pdf)
- **Display hierarchy:** L1 overview of the whole span of control, L2 primary operating display per area or task, L3 detail for troubleshooting, L4 diagnostics, procedures and point detail. — [Yokogawa on ISA-101](https://www.yokogawa.com/us/library/resources/media-publications/isa-101-toward-a-more-effective-hmi-strategy/), [ISA blog L1 overviews](https://blog.isa.org/modern-dcs-graphics-level-1-overview-displays) **[excerpt]**. Standard: [ANSI/ISA-101.01-2015](https://www.isa.org/products/isa-101-01-2015-human-machine-interfaces-for).
- **Why grey:** salience comes from contrast against a blended background. Background combined with ambient light affects eye strain. — [ASM Consortium white paper](https://process.honeywell.com/content/dam/process/en/documents/document-lists/doc_asm-consortium/white-papers/February%2028%202011%20-%20Why%20Gray%20Backgrounds%20for%20DCS%20Operating%20Displays.pdf)

### 2.4 Alarm management (ISA-18.2, EEMUA 191)
- EEMUA 191 benchmarks for steady-state alarm rate: under 1 per 10 min per operator is "very likely acceptable", 1 per 5 min "manageable", 1 per 2 min "over-demanding", more than 1 per min "very likely unacceptable". — [ProcessVue KPI paper](https://www.processvue.com/downloads/Alarm_system_performance_KPIs_V1_0.pdf)
- Under 10 alarms in the first 10 min after an upset. Priority split roughly 5% high, 15% medium, 80% low. Fewer than 10 standing alarms. — [ABB white paper](https://library.e.abb.com/public/72f20c70c7b44d889d463db81df5c38d/SCADA%20Alarm%20Management%20White%20Paper.pdf)
- Example targets: zero chattering or fleeting alarms; system in flood less than 1% of the time; fewer than 5 stale alarms (active >24 h). — [Emerson "by the numbers"](https://www.emerson.com/is/content/emerson/en/corporate/news-and-events/articles/documents/alarm-management-by-the-numbers.pdf)
- ISA-18.2 covers the alarm lifecycle, state transition diagram, deadband and delay times, recommended alarm state indications and priority distribution (table of contents). — [ANSI preview](https://webstore.ansi.org/preview-pages/ISA/preview_ANSI%2BISA%2B18.2-2009.pdf). Priority is set by severity of consequence and time available to respond ([Emerson](https://www.emerson.com/is/content/emerson/en/corporate/news-and-events/articles/documents/alarm-management-by-the-numbers.pdf)) **[excerpt]**.

### 2.5 Situation awareness (Endsley)
- SA is "the perception of the elements in the environment within a volume of time and space, the comprehension of their meaning, and the projection of their status in the near future". Accident data link most human-error accidents to SA problems. Automation especially degrades Level 2 SA. — [Endsley 1995](https://maritimesafetyinnovationlab.org/wp-content/uploads/2020/09/Towards-a-New-Paradigm-for-Automation-Designing-for-Situation-Awareness-Endsley-1995.pdf)
- SA-oriented design principles: organize around goals, present Level 2 directly (integrated information), support Level 3 projection, support global SA, avoid attentional narrowing, make critical cues salient. — [Endsley NDIA slides](https://ndia.dtic.mil/wp-content/uploads/2012/armaments/WednesdayEndsley.pdf)
- Keeping the user in control is fundamental to SA. Goal-directed task analysis drives the design. — [Designing for SA (book)](https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.1201%2F9780203485088&type=googlepdf)

### 2.6 Glanceability and preattentive design
- Real-time dashboards: a stable single-screen overview, emphasis on exceptions, flashing and sound reserved for urgent events and easy to silence, sparklines and history to support projection. — [Few, Dashboard Design for Real-Time SA](https://www.perceptualedge.com/articles/Whitepapers/Dashboard_Design.pdf) **[excerpt]**; [Few, Rich Data Poor Data](https://www.perceptualedge.com/articles/Whitepapers/Rich_Data_Poor_Data.pdf) **[excerpt]**
- Response-time limits: 0.1 s feels instantaneous, 1 s keeps flow, 10 s is the limit of attention (show progress). — [NN/g](https://www.nngroup.com/articles/response-times-3-important-limits/)

### 2.7 Dark-mode legibility and contrast
- WCAG 2.2: text 4.5:1 (large text 3:1). Non-text UI and state indicators 3:1. Target size min 24×24 CSS px. — [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum)
- Flashing: no more than 3 flashes per second. — [WCAG 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold)
- APCA (candidate for WCAG 3, still draft): body text about Lc 75 minimum, Lc 90 preferred. Polarity-aware, so light-on-dark gives a negative Lc and you use the absolute value. — [APCA calculator](https://www.myndex.com/APCA/), [ARC](https://www.readtech.org/ARC/), [WCAG 3 draft](https://www.w3.org/TR/wcag-3.0/) **[excerpt]**
- Dark theme: dark grey `#121212` base, desaturated accents (lighter tones), lighter surface means higher elevation. — [Material](https://m2.material.io/develop/android/theming/dark), [Material codelab](https://codelabs.developers.google.com/codelabs/design-material-darktheme) **[excerpt]**
- Saturated pure blue has very low luminance and is poor for text on dark backgrounds. — [ARC visual contrast guide](https://www.readtech.org/ARC/guides/designing-with-visual-contrast/) **[excerpt]**

### 2.8 Color-blind-safe status colors
- Okabe-Ito palette: `#E69F00` orange, `#56B4E9` sky blue, `#009E73` bluish green, `#F0E442` yellow, `#0072B2` blue, `#D55E00` vermilion, `#CC79A7` reddish purple. — [Matplotlib docs](https://matplotlib.org/devdocs/release/next_whats_new/okabe_ito_colormap.html), [Color Universal Design](https://jfly.uni-koeln.de/color/index.html)
- Red/green is the most common CVD confusion. Avoid colored-numeral-only status. Use fill, box, icon, or the "normally dark" approach. MIL-STD-1472 shifts red toward orange (255,65,30) and green toward blue (17,192,130). — [SFTE §21.2](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)

### 2.9 3D viewport and digital-twin practice
- ISA HP-HMI explicitly prefers 2-D, low-contrast depiction over colorful 3-D for *process* graphics ([ISA overview](https://www.isa.org/getmedia/06130a38-f7af-4b35-8c9c-2c34f25c1977/The-High-Performance-HMI-Overview-v2-01.pdf)). For ANDURA, 3-D is justified for spatial robot state but should be rendered desaturated (*design choice*).
- Prefer synoptic over photorealistic depiction, and don't imply state that isn't measured. — [SFTE](https://society-of-flight-test-engineers.github.io/quarto-handbook/21-display-guidelines.html)
- Omniverse factory twins: verify placement in both 3D and top-down views. Minimaps, waypoints and teleport for large-facility navigation. Centralised style definitions. — [NVIDIA precision placement](https://docs.nvidia.com/learning/physical-ai/assembling-digital-twins/latest/materials-assembly/precision-machine-placement.html), [VFI guide](https://docs.omniverse.nvidia.com/vfi/latest/guide/common-scenarios.html), [Kit UI style best practice](https://docs.omniverse.nvidia.com/kit/docs/kit-manual/latest/guide/ui_style_best_practice.html) **[excerpt]**
- Construction-robot twins: live robot pose and process-state sync, human supervision and approval of trajectories, BIM-driven closed loop. — [Springer, Construction Robotics 2022](https://link.springer.com/article/10.1007/s41693-022-00068-1), [NSF PAR BIM-driven HRC](https://par.nsf.gov/servlets/purl/10567681), [ASCE immersive process-level DT](https://doi.org/10.1061/(asce)cp.1943-5487.0000988), [PMC DT-VR robot control](https://pmc.ncbi.nlm.nih.gov/articles/PMC12251752/) **[excerpt]**
- Robot safety: the three-position enabling device permits motion only in the middle position. E-stop is independent. The pendant has single-point control when active. — [UR safety FAQ](https://www.universal-robots.com/articles/ur/safety/safety-faq/), [UR pendant config](https://www.universal-robots.com/manuals/EN/HTML/SW10_15/Content/prod-usr-man/complianceUR18/PolyX_SW/polyx-Safety-Hardware.htm), [ISO 10218-1:2025 preview](https://webstore.ansi.org/preview-pages/DS/preview_M324308CURES.pdf) **[excerpt]**

### 2.10 Headsets
- visionOS: keep content in the field of view, anchored in the world rather than head-locked. Use system glass and vibrancy. Interactive targets at least 60 pt apart. — [Apple HIG visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos), [WWDC23 spatial UI](https://developer.apple.com/videos/play/wwdc2023/10076/) **[excerpt]**
- Meta Quest: typography guidance at [Meta Horizon typography](https://developers.meta.com/horizon/design/styles_typography/). Text ≥1° visual angle, UI at about 1–2 m, never under 0.5 m. These numbers come from Meta's own agent-skill repo ([meta-quest/agentic-tools](https://github.com/meta-quest/agentic-tools/blob/main/skills/hz-immersive-designer/references/spatial-layout.md)), not the official HIG page **[excerpt — verify]**.

---

## 3. ANDURA design rules

### 3.1 Status color and alarm hierarchy
Normal is grey ("normally dark"). Color always comes with a shape and a text word (NASA V2 10045, ISA HP-HMI, SFTE §21.2).

| Level | Meaning (time to act) | Color (starting values, check them) | Shape + text | Behavior |
|---|---|---|---|---|
| P1 WARNING / E-STOP | Immediate action. Injury or damage possible. | Red-orange, MIL-1472-shifted, ~`#FF411E` (SFTE Table 21.4) | ◆ filled diamond + `WARN` | Flashes at ≤3 Hz until acked (WCAG 2.3.1), then steady. Audio tone. Pinned in the banner. |
| P2 CAUTION | Action needed soon | Yellow ~`#F0E442` (Okabe-Ito) | ▲ triangle + `CAUT` | Steady, audio optional |
| P3 ADVISORY | Awareness, degraded redundancy | Blue/cyan, light enough for dark bg, ~`#56B4E9` (Okabe-Ito, ARC) | ● circle + `ADV` | Steady, no audio |
| NOMINAL | In range | Neutral grey text | none | none |
| STALE / NO DATA / INVALID | Value can't be trusted | Magenta/purple ~`#CC79A7` or hatched grey (*design choice*) | `--` or `STALE 4.2s` | Required (SFTE 21.1.2.5 #13; NASA App F) |
| Command vs actual | | Hollow = command, filled = actual | | (SFTE Fig 21.4) |

**Rules**
- Red/yellow/blue mapping follows NASA App F §F.6.4. Shift red toward orange for CVD (MIL-1472 via SFTE).
- Never use green for "running/OK" (HP-HMI). If a positive confirmation is needed (e.g. "task complete"), use a text label plus a neutral glyph.
- Status colors go on a fill, chip or outline next to the value, never on bare numerals only (SFTE §21.2.1).
- Alarm list per NASA App F: counts by priority, unacked count, sortable queue, ack / shelve / suppress state, timestamp, robot or cell, root cause, link to procedure.
- Priority budget is about 80/15/5 low/med/high. Target under 1 alarm per 10 min per operator in steady state, flood under 10 in 10 min. Treat chattering alarms as defects (EEMUA/ISA via ABB, Emerson, ProcessVue).
- Flood mode: group by robot or cell and show first-out. *(design choice; motivated by flood KPIs)*
- Limit distinct status colors to ≤4–5 (SFTE).

### 3.2 Information layering (ISA-101 levels mapped to Endsley SA)
| ANDURA level | Content | SA level |
|---|---|---|
| L1 Fleet / site overview | All cells and robots as tiles or 3D mini-map. Alarm counts. Throughput vs plan. Everything grey unless abnormal. | Perception, global SA |
| L2 Cell / task | 3D twin of one cell. Robot pose. Current element being fabricated. Progress. Key 3–4 parameters with ranges. Embedded trends. | Comprehension |
| L3 Robot / element detail | Joint states, tool, path deviation, the design→fabrication record of the element. | Comprehension and projection |
| L4 Diagnostics | Logs, raw signals, procedures, alarm rationale. | Support |

- The overview is always one action away. Use a persistent breadcrumb (ISA "logical and consistent navigation").
- Show integrated meaning ("Panel W-12: 63%, ETA 14:20, +2 min vs plan"), not raw signals alone (Endsley principle 2). Show projection (ETA, trend toward limit) (principle 3, SFTE strip charts).
- An operator should never actively watch more than ~4 critical parameters. Automate alerting for the rest (SFTE 21.1.2.8).

### 3.3 Typography and numerics
- Sans-serif UI plus monospace or tabular-figure numerals: `font-variant-numeric: tabular-nums` so digits don't jitter ([MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric)). Keep Space Grotesk / Space Mono from the base. Drop Doto for live values.
- Contrast: body ≥4.5:1 (WCAG) and aim for APCA |Lc| ≥75. Status glyphs and UI ≥3:1. Primary text off-white (~`#E8E8E8`, not `#FFF`) (SFTE ghosting note).
- Labels ALL CAPS, mono, secondary grey. Running text in sentence case (SFTE 21.1.2.4).
- Show the fewest significant digits needed. Fixed field widths. Units in a smaller size next to the value. Numeric boxes stay put (SFTE).
- Every graphic carries its number, and the number shows range context (IPD, ISA "analog representation").

### 3.4 Data density
- Per panel, ≤60% filled (SFTE). The nothing-design 3-layer and 3-size rule applies **per panel**.
- Prefer tapes, bars and bullet-style range indicators with normal and alarm bands over dials. Use sparklines for trend (ISA embedded trends, SFTE, Few).
- Minimal gridlines and ticks (SFTE 21.1.2.5 #11). Keep dividers (nothing-design) for dense tables only.

### 3.5 Motion and update rates for live data
- Displayed numerics refresh at 2–4 Hz (filtered). Graphics up to 8–10 Hz max. Data must still visibly be "alive", e.g. a heartbeat or age stamp (SFTE 21.1.2.8).
- 3D robot pose may render at display frame rate, but numeric readouts beside it follow the 2–4 Hz rule. *(design choice, reconciling the twin with SFTE)*
- Animation only for alarm behavior. No spinning or decorative motion (ISA HP-HMI). Flash ≤3 Hz (WCAG 2.3.1). The FAA/MIL literature gives other flash rates ([FAA 2004 visual coding](https://hf.tc.faa.gov/publications/2004-visual-coding-of-status-for-technical-operations-systems/full_text.pdf)) **[excerpt]**. Pick one rate and keep it consistent.
- Control feedback: acknowledge input within 0.1 s, show the command state immediately, then actual state once reached. Show progress for anything over 1 s (NN/g, SFTE hollow/filled).
- Show data age and link status for every live stream. Stale data must look different (NASA App F, SFTE).
- Keep the base's 150–250 ms ease-out for UI transitions only.

### 3.6 Layout patterns for the three use cases
**(a) Live robot monitoring (prefab)**
- Top: persistent alarm banner (counts by priority, newest unacked). Left: fleet / cell list (L1). Center: 3D cell twin (L2). Right: selected robot's key parameters with ranges and trends. Bottom: task timeline (planned vs actual, ETA).
- 3D twin rendering: desaturated grey geometry. Color only on abnormal parts (ISA). Ghost the planned path or target pose against the solid actual pose (SFTE command vs actual). Provide a top-down or orthographic toggle (NVIDIA).
- Live control:
  - Physical or independent E-stop. The UI only mirrors it (Dragon physical panel, ISO 10218 / UR).
  - Few on-screen commands, as verb buttons.
  - Two-step confirm for motion commands (*design choice*, motivated by ISA "techniques to minimise data entry mistakes").
  - Single-point-of-control indicator showing who holds control (UR).
  - The display layer is separate from the safety controller (Dragon).
**(b) Design→fabrication lineage**
- A left-to-right lineage graph: design element (BIM/CAD) → fabrication plan / toolpath → robot task → as-built / QA. Link it to selection in the 3D model, so selecting either one highlights the other.
- Mark version mismatch and missing links with the advisory/caution scheme. Never use decorative color. *(design choices, grounded in BIM-driven closed-loop DT literature, e.g. [NSF PAR](https://par.nsf.gov/servlets/purl/10567681))*
**(c) Analytics**
- Slower cadence. Opacity / pattern series coding is acceptable here (nothing-design). Use Okabe-Ito for categorical series. Label lines directly. Show context: plan vs actual, normal range (Few, IPD).

### 3.7 Responsive rules across devices
| Device | Rules |
|---|---|
| Control-room wall | L1 overview only, read at distance: large numerals, high contrast. No fine interaction. Must work in peripheral vision, so use motion or flash for P1 because color change is poorly detected peripherally (Nasby). Test on the actual monitors and ambient light (SFTE 21.1.2.3 #9, NASA off-angle lesson). |
| Desktop | Full L1–L4, multi-panel, keyboard shortcuts, alarm list docked. |
| Tablet (shop floor) | L2/L3 for one cell. Targets ≥24 px (WCAG minimum). Use larger targets for gloves and vibration (Dragon). Keep the base's 44 px+. Alarm banner always visible. |
| Headset (AR/VR) | World-anchored panels (Apple). Text ≥1° visual angle (Meta, verify). Panels at 1–2 m. Minimal text. Spatial overlays on robots for state. No safety-critical control only in the headset (*design choice*, consistent with independent E-stop). |
- The same color, priority and shape semantics apply on every device. Only density and layout change (SFTE "common design philosophy").

### 3.8 Do / Don't
**Do**
- Keep the screen grey when everything is normal.
- Color + shape + word for every status.
- Show a range on every value.
- Show the age of every stream.
- Use hollow for command and filled for actual.
- Keep the overview one action away.
- Version and validate dashboards against recorded data (SFTE 21.1.4).

**Don't**
- Green for running.
- Status-colored numerals on black as the only cue.
- Spinning or animated equipment.
- Photoreal, saturated 3D.
- Toasts for alarms.
- Flash above 3 Hz.
- Refresh numbers faster than about 4 Hz.
- Pure `#FFF` on `#000` for large text areas.
- Saturated blue text.
- Arbitrary limits.
- Safety-critical control that exists only in software.

---

## 4. Gaps and caveats
- Not read in full: the ISA-101, ISA-18.2, EEMUA 191, ISO 10218 and MIL-STD-1472 texts (paywalled). NASA App F was seen via excerpt only (the page fetch timed out). Few's papers, the Omniverse docs, Apple/Meta and APCA were also seen via excerpts.
- No primary source was found for NASA MCC console color standards beyond NASA-STD-3001 App F and the 1990 NTRS paper ([NTRS 19900012897](https://ntrs.nasa.gov/api/citations/19900012897/downloads/19900012897.pdf), not reviewed).
- Hex values in §3.1 are starting points taken from the cited palettes. Check them for contrast (WCAG/APCA) on the chosen background, and with a CVD simulator.
