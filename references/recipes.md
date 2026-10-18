# ANDURA — Component recipes (exact markup)

Every example in `examples/` uses these recipes verbatim; only text, numbers, `href` and positions change. The styles live in `examples/andura-ui.css` and the behaviour in `examples/andura-ui.js` (tokens only). On other platforms keep the same structure and states. `scripts/check.py` reads the `recipe` comments below and fails an example whose instance of a recipe misses a required part (drift check).

**State classes** (on `body[data-state]`, set from `?state=`): `alarm` (default), `normal`, `inspect`, `detail`, and the data-quality and system states `stale`, `comms`, `offline`, `empty`, `flood` (§9–§12). A page lists the states it implements in `<meta name="andura-states" content="…">`; the checks run exactly those. While the 09:54 alarms are active (`alarm`, `detail`, `stale`, `comms`, `offline`, `flood`) `andura-ui.js` sets `body[data-alarms]`, which drives the band, rims, badge and `.dim`. `?mode=sunlit` sets the sunlit colour mode (`colour.md` §9). Helpers: `.only` + `.<state>-only` show content per state (`alarm-only` shows whenever `body[data-alarms]`); `.not-empty` / `.not-comms` / `.not-offline` / `.not-flood` hide live content in that state; `.dim` drops to `opacity.dim` while an alarm is active; `.phone-hide` / `.tab-hide` remove secondary content on smaller classes; `aria-current` marks the active slot (set from `data-for`); `.hit` marks every target; `.trunc` truncates with a peek title; `.value` never truncates.

## Status glyphs
16 px (`size.glyph`), always with the word next to them. Only these four shapes (checked):
```html
<svg class="glyph" viewBox="0 0 16 16" aria-hidden="true"><path d="M5 0h6l5 5v6l-5 5H5l-5-5V5z" style="fill:var(--andura-color-emergency)"/><path d="M7 3h2v6H7zM7 11h2v2H7z" style="fill:var(--andura-color-void)"/></svg>  <!-- P1 octagon -->
<svg class="glyph" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0l8 15H0z" style="fill:var(--andura-color-caution)"/><path d="M7 5h2v5H7zM7 11h2v2H7z" style="fill:var(--andura-color-void)"/></svg>  <!-- P2 triangle -->
<svg class="glyph" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="8" style="fill:var(--andura-color-text)"/><path d="M7 7h2v6H7zM7 3h2v2H7z" style="fill:var(--andura-color-void)"/></svg>  <!-- P3 circle i -->
<svg class="glyph" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="7" style="fill:none;stroke:var(--andura-color-muted);stroke-dasharray:3 2"/></svg>  <!-- stale dashed circle -->
```

## 0. Header (top line)
Height `size.header.*` (72 · 72 · 64), mark `size.logo` (32). Left to right: ANDURA mark, optional client/app logo (same height, max width 4 × `size.logo`, monochrome or its own approved colours, never an alarm hue), the h1 (cell name, truncates), then on the right CONTROL owner · DATA age (`.live`) · clock. Phone: mark, h1, clock. The mark is decorative branding: not a link, not a target. Sunlit mode needs no change (`currentColor` = Text).
<!-- recipe: header | root: header.top | requires: span.brand; svg.mark; span.h1.trunc; span.facts -->
```html
<header class="top">
 <span class="brand"><svg class="mark" viewBox="0 0 32 32" role="img" aria-label="ANDURA"><title>ANDURA</title><path d="M3 29 16 3l13 26h-7.5L16 17.5 10.5 29Z M13.5 29 16 24l2.5 5Z" style="fill:currentColor"/></svg>
  <img class="client-logo" src="client.svg" alt="Client name"><!-- optional --></span>
 <span class="h1 trunc" title="Cell C3 · Wall panel line">Cell C3 · Wall panel line</span>
 <span class="facts"><span class="label phone-hide">CONTROL <span class="text">M. KELLER</span></span><span class="label phone-hide live">…</span><span class="label"><time>09:56</time> CEST</span></span>
</header>
```
The mark source is `assets/andura-mark.svg`.

## 1. Alarm row (band)
<!-- recipe: alarm-row | root: div.r.p1, div.r.p2 | requires: span.edge; svg.glyph; span.label.text.value; span.trunc; span.label.value -->
```html
<section class="band" aria-label="Active alarms">
 <div class="r p1"><span class="edge"></span>
  <svg class="glyph" …P1…></svg>
  <span class="label text value">P1 EMERGENCY</span><span class="trunc" title="Cell C3 · KR-03 protective stop · J5 force 412 N, limit 380 N">Cell C3 · KR-03 protective stop · J5 force 412 N, limit 380 N</span><span class="label value phone-hide ack-state">09:54:12 · UNACK</span>
  <span class="acts"><button class="btn hit">PROCEDURE SP-114</button><button class="btn pri hit" onclick="confirmAck()">ACKNOWLEDGE</button></span>
  <a class="more hit label text" href="?state=detail">+1 ›</a>
 </div>
 <div class="r p2"><span class="edge"></span>
  <svg class="glyph" …P2…></svg>
  <span class="label text value">P2 CAUTION</span><span class="muted trunc" title="…">…</span><span class="label value">09:51:40 · ACKED</span>
 </div>
</section>
```
States: shown in `alarm` and `detail`; P1 edge pulses until `body.acked`; phone shows the top row only, buttons hidden, "+n" opens `detail`. Never put a hold button in the band.

## 2. KPI tile
<!-- recipe: kpi | root: div.kpi | requires: span.label; div.kpi-v; span.value; span.vals; span.label.value -->
```html
<div class="kpi">
 <span class="label">THROUGHPUT · TODAY</span>
 <div class="kpi-v"><span class="value vl">286</span><span class="muted value">m²</span></div>
 <span class="vals"><span class="label value">TARGET 296 <span class="unit">m²</span></span><span class="label value">· DEV −10</span></span>
 <a class="hit label kpi-link" href="#trends">TRENDS ›</a>
</div>
```
One value per tile, unit Muted, then LIMIT (alarm setpoint) or TARGET (plan, Muted, with DEV). The drill link is optional. Inside `.dim` while an alarm is active. A line of several values is a `.vals` row of one `.value` per group: at 200 % or in a narrow column it wraps between groups, never inside one (values never truncate or wrap). Keep each group short (about 16 characters): on a 390 px phone at 200 % one group must fit the column. A screen's hero number is this recipe with `display` in `.kpi-v`; never put a bare `display` row directly above other text (its line box overlaps the next line).

## 3. 3D tag
<!-- recipe: tag | root: span.tag.em, span.tag.ca | requires: svg.glyph; span.label.text -->
```html
<span class="tag em row only alarm-only" style="left:66%;top:47%"><svg class="glyph" …P1…></svg><span class="label text">KR-03 · STOP</span></span>
<span class="tag label text" style="left:52%;top:40%">KR-02 · NAILING</span>  <!-- neutral tag -->
```
Status tags (`em`, `ca`) carry glyph + word and show only while the alarm is active; the matching 3D object gets `class="rim rim-em o3d"` (or `rim-ca`) with `vector-effect="non-scaling-stroke"`. Selection: `class="sel3d o3d" data-inner="<body width>"`. Phone hides tags (the thumbnail is too small).

## 4. Confirm dialog
<!-- recipe: dialog | root: dialog | requires: span.title; p.muted; div.acts; button.btn.hit[autofocus]; button.btn.pri.hit -->
```html
<dialog id="ack" aria-labelledby="ack-t">
 <span class="title" id="ack-t">Acknowledge P1 · KR-03 protective stop?</span>
 <p class="muted">Acknowledging silences the alarm. It does not reset the robot.</p>
 <div class="acts"><button class="btn hit" autofocus onclick="ack.close()">CANCEL</button><button class="btn pri hit" onclick="ack.close();acked()">ACKNOWLEDGE P1</button></div>
</dialog>
```
Surface + 1 px Line, Void scrim at `opacity.scrim`, focus on CANCEL, the command named. Opened by `confirmAck()` on desktop and tablet.

## 5. Hold button
<!-- recipe: hold | root: button.hold | requires: span.fill; span -->
```html
<button class="btn hit hold" aria-label="Press and hold 1.5 seconds to acknowledge P1 KR-03"><span class="fill"></span><span>HOLD TO ACKNOWLEDGE</span></button>
```
Phone only (hidden on desktop and tablet, where `.confirm-ack` shows instead). Fill opacity 0 → 1 over `motion.duration.hold`, linear; release cancels.

## 6. Tab bar (phone)
<!-- recipe: tabs | root: nav.tabs | requires: a.hit.label[data-for]; span.badge; svg.glyph; span.text -->
```html
<nav class="tabs" aria-label="Sections">
 <a class="hit label" data-for="alarm normal" href="?state=alarm" title="Cell"><span>CELL</span></a><a class="hit label" data-for="inspect" href="?state=inspect" title="Robots"><span>ROBOTS</span></a>
 <a class="hit label" data-for="detail" href="?state=detail" title="Alarms"><span class="badge"><svg class="glyph" …P1…></svg><span class="text">P1 · 2</span></span><span>ALARMS</span></a>
 <a class="hit label" href="#more" title="More"><span>MORE</span></a>
</nav>
```
Same four tabs on every layout; only `data-for` changes. The badge slot is always reserved (visible in `alarm` and `detail`). The desktop/tablet `footer` uses the same `data-for` mechanism.

## 7. Cell summary
<!-- recipe: cellsum | root: div.cellsum | requires: span.label; div.normal-only; span.title; div.alarm-only; svg.glyph; span.title.trunc -->
```html
<div class="cellsum">
 <span class="label">CELL</span>
 <div class="row only normal-only"><span class="title">Running</span></div>
 <div class="row only alarm-only"><svg class="glyph" …P1…></svg><span class="title trunc">P1 · Partly stopped</span></div>
 <span class="muted only alarm-only">KR-03 stopped · KR-01 caution</span>
</div>
```
Pattern `<highest priority> · <state>` (Running, Partly stopped, Stopped, Waiting); the Muted line is hidden on tablet and phone.

## 8. Sparkline
<!-- recipe: spark | root: svg.spark | requires: line.limit-line; polyline.trace; path.end -->
```html
<svg class="spark" viewBox="0 0 400 32" preserveAspectRatio="none" aria-label="Path deviation, last 10 minutes">
 <line class="limit-line" x1="0" y1="4" x2="400" y2="4" vector-effect="non-scaling-stroke"/>
 <polyline points="0,22 … 398,13" class="trace" vector-effect="non-scaling-stroke"/><path class="end" d="M398 13h0" vector-effect="non-scaling-stroke"/>
</svg>
```
Frameless, 32 px (`size.spark-h`), limit at the top (value-to-limit scale), 1.5 px Text trace, end dot r 2.5 in Text, never an alarm hue.

## 9. Stale value (data age)
<!-- recipe: stale | root: div[data-stale-in], a[data-stale-in] | requires: span.age -->
```html
<div data-stale-in="stale comms offline">
 <span class="label">PATH DEV</span>
 <div class="row"><span class="value vm">0.42</span><span class="muted value">mm</span><span class="label value">LIMIT 0.50 <span class="unit">mm</span></span></div>
 <span class="age label"><svg class="glyph" …stale…></svg>TRACKER · AGE 0:42</span>
</div>
```
`data-stale-in` lists the states in which the block's source is stale; `andura-ui.js` adds `.stale`. A stale block keeps the **last** value, turns values Muted, traces Muted, and shows its data age (`AGE m:ss`, the source name if more than one feeds the screen). Never extrapolate, animate or blank a stale value, and never show it in Text. `touch_check.py` fails a visible `.stale` block without a visible age (`m:ss` or `n s`) and any of its values not in Muted. Stale = older than 3 × the source's update period (top-line `DATA` shows the period).

## 10. System rows in the band: comms loss, alarm flood
<!-- recipe: system-row | root: div.r.cm, div.r.fl | requires: span.edge; svg.glyph; span.label.text.value; span.trunc -->
```html
<div class="r cm only comms-only"><span class="edge"></span><svg class="glyph" …stale…></svg>
 <span class="label text value">COMMS LOST</span><span class="trunc">Cell C3 PLC · no data since 09:55:18 · values show their last state and age</span><span class="label value">AGE 0:42</span></div>
<div class="r fl only flood-only"><span class="edge"></span><svg class="glyph" …P3…></svg>
 <span class="label text value">ALARM FLOOD</span><span class="trunc">23 alarms in 10 min · 15 shelved · 6 suppressed by design</span>
 <span class="acts"><a class="btn hit" href="l5-alarms.html?state=flood">ALARM LIST</a></span><a class="more hit label text" href="l5-alarms.html?state=flood">LIST ›</a></div>
```
Comms loss goes on top (every other row's truth is now unknown); its edge is Muted, never a priority colour. The top line's `DATA` fact turns into `COMMS LOST · AGE 0:42` (class `.live`, the only chrome text that may change by state; `persist_check.py` masks it), the 3D view freezes under a `NO LIVE DATA · LAST 09:55:18` label, and every live block goes stale. Flood: the summary row sits under the P1 row (P2 folds into it); phone shows the system row instead of P1.

## 11. Flood list: shelved and suppressed (ISA-18.2)
<!-- recipe: flood | root: div.flood | requires: svg.glyph; span.label.text.value; span.label.value -->
<!-- recipe: shelved | root: a.shelved | requires: svg.glyph; span.trunc; span.label.value.shelf -->
```html
<div class="flood row vals"><svg class="glyph" …P3…></svg><span class="label text value">ALARM FLOOD</span><span class="label value">23 IN 10 MIN</span><span class="label value">· LIMIT 10 / 10 MIN</span></div>
<span class="label sub">SUPPRESSED BY DESIGN · 6</span>  <!-- one summary row, never the 6 alarms -->
<span class="label sub">SHELVED · 15</span>
<a class="hit shelved" href="#s1"><svg class="glyph" …P3…></svg><span class="label value">P3</span><span class="trunc muted">KR-01 infeed sensor chatter</span><span class="label value shelf">0:28 LEFT</span><span class="chev label">›</span></a>
```
Flood = more than 10 new alarms in 10 min for one operator (ISA-18.2 / EEMUA 191 benchmark). Active alarms stay first-out on top, never shelved automatically; consequential alarms of a known cause are **suppressed by design** (state-based, listed as one row); nuisance alarms may be **shelved** by the operator for a fixed time (`0:28 LEFT`, who), and return when the time runs out. Cleared history hides during a flood (`.not-flood`).

## 12. Empty / startup KPI
```html
<div class="kpi-v not-empty"><span class="value vl">286</span><span class="muted value">m²</span></div>
<div class="kpi-v only empty-only"><span class="value vl muted">—</span><span class="label">WAITING FOR DATA</span></div>
```
Before the first data arrives show `—` with `WAITING FOR DATA`, the cell as `Connecting · no data yet` with the stale glyph, alarm state "unknown" (never "No active alarms") and top-line `DATA CONNECTING`. Never show zeros, placeholders or a previous session's values as if live. `touch_check.py` fails any digit in a `display`/`vm`/`vl` value or a visible sparkline in `empty`.

## 13. Charts: trend, histogram, Gantt
Rules, tokens and axes: [`charts.md`](charts.md). Labels are HTML, never text inside a stretched SVG.
<!-- recipe: trend | root: figure.trend | requires: svg.tr; line.limit-line; polyline.trace; polyline.over; div.yax; div.xax -->
<!-- recipe: hist | root: figure.hist | requires: div.hbars; span.hb; span.limit-mark; div.xax -->
<!-- recipe: gantt | root: figure.gantt | requires: div.grow; div.gtrack; span.gbar; span.now; div.xax; div.gkey -->
```html
<figure class="trend" aria-label="Cycle time today, limit 4:30 min, over limit 09:12 to 09:41">
 <div class="row vals"><span class="label">CYCLE TIME · TODAY</span><span class="label value">LIMIT 4:30 min</span></div>
 <div class="plot"><div class="yax"><span class="label value">5:00</span><span class="label value">3:00</span></div>
  <svg class="tr" viewBox="0 0 400 120" preserveAspectRatio="none" aria-hidden="true"><rect class="band" x="0" y="0" width="400" height="30"/>
   <line class="limit-line" x1="0" y1="30" x2="400" y2="30" vector-effect="non-scaling-stroke"/><line class="base" x1="0" y1="120" x2="400" y2="120" vector-effect="non-scaling-stroke"/>
   <polyline class="trace" points="…" vector-effect="non-scaling-stroke"/><polyline class="over" points="…" vector-effect="non-scaling-stroke"/></svg></div>
 <div class="xax"><span class="label">06:00</span><span class="label">NOW</span></div>
 <div class="row vals"><svg class="glyph" …P2…></svg><span class="label text value">OVER LIMIT</span><span class="label value">09:12–09:41</span></div>
</figure>
<figure class="hist" aria-label="…"><div class="row vals">…</div>
 <div class="hbars"><span class="hb" style="height:18%" title="3:30 min: 3 parts"></span>… <span class="hb over" style="height:29%" title="4:30 min: 5 parts"></span><span class="limit-mark" style="left:66.67%"></span></div>
 <div class="xax"><span class="label">3:30</span><span class="label">4:30 LIMIT</span><span class="label">5:00</span></div></figure>
<figure class="gantt" aria-label="Fabrication progress today, 06:00 to 14:00">
 <div class="grow"><span class="row"><svg class="glyph" …P1…></svg><span class="label text value">W-13</span></span>
  <div class="gtrack"><span class="gbar s1" style="left:15%;width:8.33%" title="W-13 07:20–08:00"></span>… <span class="gbar s3 held" …></span><span class="now" style="left:49.17%"></span></div></div>
 <div class="xax">…</div><div class="gkey"><span class="label"><i style="background:var(--andura-color-data-cividis-1)"></i>CUT</span>…<span class="label">EDGE = HELD BY ALARM</span></div>
</figure>
```
