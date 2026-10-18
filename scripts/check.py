"""ANDURA verification. Run from anywhere: python3 scripts/check.py
Source of truth: tokens/andura.tokens.json. Checks SKILL.md, references/*.md, assets/pal-v2.2.json and
tokens/build/* against it, scans for banned values, then runs a self-test that injects one violation per
check and confirms it fails. `--example path.html` checks only that page (token-only colour, andura.css loaded).
Exit code 0 = all pass; 1 = failures (each printed)."""
import subprocess, glob, json, os, re, sys
from html.parser import HTMLParser
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/scripts")
import export_tokens as ex

TOK = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))
COLOR = {k: v["$value"].upper() for k, v in TOK["color"].items() if "$value" in v}
SEQ = [TOK["color"]["data"]["cividis"][str(i)]["$value"].upper() for i in range(7)]
THREE = {k: v["$value"].upper() for k, v in TOK["color"]["3d"].items()}
MODES = TOK["$extensions"]["andura"].get("modes", {})
SUN = {k: v.upper() for k, v in MODES.get("sunlit", {}).get("color", {}).items()}
ALLHEX = set(COLOR.values()) | set(SEQ) | set(THREE.values()) | set(SUN.values())
VERSION = TOK["$extensions"]["andura"]["version"]
px = lambda node: node["$value"]["value"]

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return f"{(la + 0.05) / (lb + 0.05):.2f}"

key = lambda name: name.lower().replace(" ", "-")
def section(text, head):
    return text.split(head, 1)[1].split("\n## ", 1)[0] if head in text else ""
def rows(text):
    return [[c.strip() for c in l.strip().strip("|").split("|")] for l in text.splitlines() if l.startswith("| ")]

def check_skill(S):
    e = []
    for h in set(x.upper() for x in re.findall(r"#[0-9A-Fa-f]{6}\b", S)):
        if h not in ALLHEX: e.append(f"SKILL hex {h} is not a token")
    seen = set()
    for r in rows(section(S, "## 3. Colour")):
        k = key(r[0])
        if k in COLOR:
            seen.add(k)
            if r[1].strip("`") != COLOR[k]: e.append(f"SKILL colour {r[0]} {r[1]} != token {COLOR[k]}")
            m = re.match(r"([\d.]+) / ([\d.]+|—)", r[3])
            if m:
                if m.group(1) != ratio(COLOR[k], COLOR["void"]): e.append(f"SKILL contrast {r[0]} vs Void {m.group(1)} != {ratio(COLOR[k], COLOR['void'])}")
                if m.group(2) != "—" and m.group(2) != ratio(COLOR[k], COLOR["surface"]): e.append(f"SKILL contrast {r[0]} vs Surface {m.group(2)} != {ratio(COLOR[k], COLOR['surface'])}")
        elif r[0].startswith("Data scale") and r[1].strip("`").split() != SEQ: e.append("SKILL cividis stops != tokens")
    if seen != set(COLOR): e.append(f"SKILL colour table misses {sorted(set(COLOR) - seen)}")
    classes = ["desktop", "tablet", "phone", "wall"]
    for r in rows(section(S, "## 4. Type")):
        if r[0] not in TOK["type"]: continue
        for cls, cell in zip(classes, r[3:7]):
            t = TOK["type"][r[0]][cls]
            want = f"{t['$value']['fontSize']['value']}/{t['$extensions']['andura']['lineHeightPx']}"
            if cell != want: e.append(f"SKILL type {r[0]} {cls} {cell} != token {want}")
        t = TOK["type"][r[0]]["desktop"]
        fam = "Mono" if "mono" in t["$value"]["fontFamily"] else "Sans"
        w = ex.resolve(t["$value"]["fontWeight"])
        if not r[1].startswith(f"{fam} {w}"): e.append(f"SKILL type {r[0]} font {r[1]} != {fam} {w}")
        if not r[2].lower().startswith(t["$extensions"]["andura"]["color"]): e.append(f"SKILL type {r[0]} colour {r[2]}")
    if len([r for r in rows(section(S, "## 4. Type")) if r[0] in TOK["type"]]) != len(TOK["type"]): e.append("SKILL type table misses tokens")
    sz, bp = TOK["size"], TOK["breakpoint"]
    for r in rows(section(S, "## 5. Layout")):
        cls = r[0].lower()
        if cls not in bp: continue
        b = bp[cls]
        if not r[1].startswith(str(px(b))): e.append(f"SKILL breakpoint {cls} {r[1]} != {px(b)}")
        cw, ch = b["$extensions"]["andura"]["canvas"]
        if r[2] != f"{cw} × {ch}": e.append(f"SKILL canvas {cls} {r[2]}")
        if r[3] != str(px(sz["margin"][cls])): e.append(f"SKILL margin {cls} {r[3]}")
        if cls != "wall":
            if not r[4].startswith(str(px(sz["header"][cls]))): e.append(f"SKILL top line {cls} {r[4]}")
            band = f"{sz['alarm-rows-max'][cls]['$value']} row{'s' if sz['alarm-rows-max'][cls]['$value'] > 1 else ''} × {px(sz['alarm-row'][cls])}"
            if not r[5].startswith(band): e.append(f"SKILL alarm band {cls} {r[5]} != {band}")
            if str(px(sz["footer"][cls])) not in r[6]: e.append(f"SKILL footer {cls} {r[6]}")
            if cls in sz["footer-slot"] and f"{px(sz['footer-slot'][cls])} px slots" not in r[6]: e.append(f"SKILL footer slots {cls}")
    if not re.search(rf"at least {px(sz['touch-min'])} × {px(sz['touch-min'])} px", S): e.append("SKILL touch minimum != token")
    m = re.search(r"^version: (\S+)", S, re.M)
    if not m or m.group(1) != VERSION: e.append(f"SKILL version {m and m.group(1)} != tokens {VERSION}")
    return e

def check_refs(R):
    e = []
    C = R["colour.md"]
    for r in rows(section(C, "## 2. Contrast")):
        k = key(r[0].replace(" (graphic)", ""))
        if k not in COLOR or k == "void": continue
        if r[1].strip("`") != COLOR[k]: e.append(f"colour.md {r[0]} hex {r[1]}")
        if r[3] != ratio(COLOR[k], COLOR["void"]): e.append(f"colour.md {r[0]} vs Void {r[3]} != {ratio(COLOR[k], COLOR['void'])}")
        if re.sub(r"[^\d.].*", "", r[4].strip("*")) != ratio(COLOR[k], COLOR["surface"]): e.append(f"colour.md {r[0]} vs Surface {r[4]}")
    for r in rows(section(C, "## 1. Palette")):
        k = key(r[0])
        if k in COLOR and r[1].strip("`") != COLOR[k]: e.append(f"colour.md palette {r[0]} {r[1]}")
    T = R["typography.md"]
    for r in rows(section(T, "## 2. Scale")):
        k = r[0].strip("`").split()[0].strip("`")
        if k not in TOK["type"]: continue
        for cls, cell in zip(["desktop", "tablet", "wall"], r[3:6]):
            t = TOK["type"][k][cls]
            want = f"{t['$value']['fontSize']['value']}/{t['$extensions']['andura']['lineHeightPx']}"
            if cell.split()[0] != want: e.append(f"typography.md {k} {cls} {cell} != {want}")
    for r in rows(section(T, "## 3. Phone scale")):
        for k in r[0].split(" / "):
            if k in TOK["type"]:
                t = TOK["type"][k]["phone"]
                want = f"{t['$value']['fontSize']['value']}/{t['$extensions']['andura']['lineHeightPx']}"
                if r[1].split()[0] != want: e.append(f"typography.md phone {k} {r[1]} != {want}")
    D = TOK["motion"]["duration"]
    for r in rows(section(R["motion.md"], "## Tokens")):
        for k in re.findall(r"`duration\.([a-z-]+)`", r[0]):
            if k in D and not r[1].startswith(f"{px(D[k])}"): e.append(f"motion.md duration.{k} {r[1]} != {px(D[k])} ms")
        for k in re.findall(r"`easing\.([a-z]+)`", r[0]):
            want = "(" + ", ".join(f"{x:g}" for x in TOK["motion"]["easing"][k]["$value"]) + ")"
            if r[1] != want: e.append(f"motion.md easing.{k} {r[1]} != {want}")
    for name, t in R.items():
        if name == "research.md": continue  # cites external palettes on purpose
        for h in set(x.upper() for x in re.findall(r"#[0-9A-Fa-f]{6}\b", t)):
            if h not in ALLHEX: e.append(f"{name}: hex {h} is not a token")
    L = R["layouts.md"]
    for r in rows(section(L, "### Breakpoints").split("\n### ")[0]):
        cls = r[0].lower()
        if cls in TOK["breakpoint"]:
            cw, ch = TOK["breakpoint"][cls]["$extensions"]["andura"]["canvas"]
            if not r[2].startswith(f"{cw} × {ch}"): e.append(f"layouts.md canvas {cls} {r[2]}")
            if r[4] != str(px(TOK["size"]["margin"][cls])): e.append(f"layouts.md margin {cls} {r[4]}")
    return e

BANS = [
    (r"\bLight\b", "thin weight 'Light'"),
    (r"\b300\b(?!\s*(ms|/\s*500 ms))", "weight 300"),
    (r"\bSans 600\b|\bsemibold\b", "Sans 600 / semibold"),
    (r"(?i)#121315|#0D0E10|#37383C", "superseded Surface or Line hex"),
    (r"(?i)status bar 40|banner 40|alarm banner \(40", "pre-minimal 40 px chrome"),
    (r"Δ", "Greek delta"),
]
def check_bans(name, text):
    e = []
    for i, line in enumerate(text.splitlines(), 1):
        for pat, why in BANS:
            if re.search(pat, line): e.append(f"{name}:{i} banned {why}: {line.strip()[:90]}")
        for m in re.finditer(r"(?<!Sunlit )\bSurface\b(?!(?i: lift| hover))[^#\n]{0,12}(#[0-9A-Fa-f]{6})", line):
            if m.group(1).upper() != COLOR["surface"]: e.append(f"{name}:{i} Surface {m.group(1)} != {COLOR['surface']}")
        if re.search(r"(?i)5A74F1", line) and re.search(r"(?i)focus\s*ring|focus ring", line) and not re.search(r"(?i)\bnever\b|\bnot\b|links only", line):
            e.append(f"{name}:{i} Ultramarine Text used as focus ring")
    return e

CSS = open(f"{ROOT}/tokens/build/andura.css").read()
LINK = re.compile(r"""<link\b(?=[^>]*\brel=["']?stylesheet)[^>]*\bhref=["'][^"']*andura\.css["'][^>]*>|@import\s+(?:url\()?["'][^"']*andura\.css["']""")

BP = {px(v) + d for v in TOK["breakpoint"].values() if isinstance(v, dict) and "$value" in v for d in (0, -1)}
TOKVAL = {}
for _p, _v in ex.TOKENS:
    _x, _u = ex.scalar(_v)
    if _u in ("px", "ms"): TOKVAL.setdefault(f"{_x:g}{_u}" if isinstance(_x, (int, float)) else "", f"--andura-{ex.name(_p, '-')}")

def inlined(code):
    """<style> blocks that are an inlined copy of andura.css (marker comment 'andura.css' or 10+ --andura-* definitions)."""
    return [b for b in re.findall(r"<style\b[^>]*>.*?</style>", code, re.S)
            if re.search(r"/\*[^*]*andura\.css", b) or len(re.findall(r"--andura-[\w-]+\s*:", b)) >= 10]

def check_example(name, t, sheet=False):
    """An example may use colours, sizes and durations only through var(--andura-*) tokens that exist, and must load
    andura.css with a real <link rel=stylesheet>, an @import, or an inlined copy (self-contained page). Allowed literals:
    0/1 px, 0 ms, breakpoint values in @media and @container, and anything inside <svg> (3D/scene geometry)."""
    e = []
    blocks = inlined(t)
    own = set(re.findall(r"(--andura-[\w-]+)\s*:", "".join(blocks)))
    for b in blocks: t = t.replace(b, "")
    code = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    for bad in re.findall(r"(?<![&\w])#[0-9A-Fa-f]{3,8}\b|rgba?\(|hsla?\(", re.sub(r"""\bhref=["'][^"']*["']""", "", code)):
        e.append(f"{name}: literal colour {bad}; use var(--andura-color-*)")
    for v in set(re.findall(r"var\((--andura-[a-zA-Z0-9-]+)\)", code)):
        if v + ":" not in CSS and v not in own: e.append(f"{name}: unknown token {v}")
    if sheet: code = f"<style>{code}</style>"
    if not sheet and not LINK.search(code) and not blocks: e.append(f"{name} does not load tokens/build/andura.css")
    nosvg = re.sub(r"<svg\b.*?</svg>", "", code, flags=re.S)
    css = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", nosvg, re.S) + re.findall(r'style="([^"]*)"', nosvg))
    for q in re.findall(r"@(?:media|container)[^{]*", css):
        e += [f"{name}: @media/@container {n}px is not a breakpoint token" for n in re.findall(r"(\d+)px", q) if int(n) not in BP]
    css = re.sub(r"@(?:media|container)[^{]*", "", re.sub(r"/\*.*?\*/", "", css, flags=re.S))
    for n, u in re.findall(r"(?<![\w.#-])(\d+(?:\.\d+)?)(px|ms)\b", css):
        lit = f"{float(n):g}{u}"
        if lit in ("0px", "1px", "0ms"): continue
        tok = TOKVAL.get(lit)
        e.append(f"{name}: hand-typed {lit}" + (f"; use var({tok})" if tok else "; not a token value"))
    return e

class _Tree(HTMLParser):
    """Minimal DOM: each node = [tag, classes, attrs, children]."""
    VOID = {"meta", "link", "br", "img", "input", "hr", "source", "path", "line", "circle", "polyline", "rect"}
    def __init__(self, t):
        super().__init__(); self.root = ["#root", set(), {}, []]; self.stack = [self.root]; self.feed(t)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); n = [tag, set((a.get("class") or "").split()), a, []]
        self.stack[-1][3].append(n)
        if tag not in self.VOID: self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        a = dict(attrs); self.stack[-1][3].append([tag, set((a.get("class") or "").split()), a, []])
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i][0] == tag: del self.stack[i:]; break

def _match(n, sel):
    m = re.match(r"([a-z0-9#]*)((?:\.[\w-]+)*)((?:\[[\w-]+\])*)$", sel)
    tag, cls, att = m.group(1), m.group(2).split(".")[1:], re.findall(r"\[([\w-]+)\]", m.group(3))
    return (not tag or n[0] == tag) and set(cls) <= n[1] and all(x in n[2] for x in att)

def _walk(n):
    yield n
    for c in n[3]: yield from _walk(c)

RECIPES = [(m.group(1), [x.strip() for x in m.group(2).split(",")], [x.strip() for x in m.group(3).split(";")])
           for m in re.finditer(r"<!-- recipe: ([\w-]+) \| root: ([^|]+)\| requires: ([^>]+?) -->", open(f"{ROOT}/references/recipes.md").read())]
GLYPHS = {x for x in (tuple(re.findall(r'(?:d|r)="([^"]+)"', g)) for g in re.findall(r"<svg class=\"glyph\".*?</svg>", open(f"{ROOT}/references/recipes.md").read())) if x}

def check_recipes(name, t):
    """Drift check: every instance of a recipe root contains the recipe's required parts; glyphs use the 4 canonical shapes."""
    e = []
    tree = _Tree(t).root
    for rname, roots, req in RECIPES:
        for n in _walk(tree):
            if any(_match(n, r) for r in roots):
                miss = [q for q in req if not any(_match(d, q) for d in _walk(n) if d is not n or q == req[0] and False)]
                if miss: e.append(f"{name}: recipe '{rname}' ({n[0]}.{'.'.join(sorted(n[1]))}) misses {', '.join(miss)} (references/recipes.md)")
    for g in re.findall(r"<svg class=\"glyph[^\"]*\"[^>]*>.*?</svg>", t, re.S):
        if tuple(re.findall(r'(?:d|r)="([^"]+)"', g)) not in GLYPHS: e.append(f"{name}: non-canonical status glyph {g[:60]}…")
    return e

def check_modes(colour_md):
    """Every colour mode overrides only existing colour tokens and meets its contrast targets; colour.md §9 matches."""
    e = []
    base = {**COLOR, **{f"3d.{k}": v for k, v in THREE.items()}}
    for m, d in MODES.items():
        c = {k: v.upper() for k, v in d["color"].items()}
        e += [f"mode {m}: {k} is not a colour token" for k in c if k not in base]
        full = {**base, **c}
        for a, b, tgt in d.get("contrast-targets", []):
            r = float(ratio(full[a], full[b]))
            if r < tgt: e.append(f"mode {m}: {a} on {b} is {r:.2f}:1 < target {tgt}:1")
    sec = section(colour_md, "## 9.")
    for r in rows(sec):
        k = key(r[0].replace("Sunlit ", "")) if r and r[0].startswith("Sunlit") else None
        if not k: continue
        if k not in SUN: e.append(f"colour.md §9 {r[0]} is not a sunlit token"); continue
        if r[1].strip("`").upper() != SUN[k]: e.append(f"colour.md §9 {r[0]} {r[1]} != token {SUN[k]}")
        full = {**COLOR, **SUN}
        if r[2] != ratio(SUN[k], full["void"]) or r[3] != ratio(SUN[k], full["surface"]): e.append(f"colour.md §9 {r[0]} contrast {r[2]} / {r[3]} != {ratio(SUN[k], full['void'])} / {ratio(SUN[k], full['surface'])}")
    if MODES and not sec: e.append("colour.md has no §9 for the colour modes")
    return e

def check_data():
    e = []
    pal = json.load(open(f"{ROOT}/assets/pal-v2.2.json"))
    for r in pal["rows"]:
        if COLOR.get(key(r["name"])) != r["hex"].upper(): e.append(f"pal-v2.2.json {r['name']} {r['hex']} != token")
    if [h.upper() for h in pal["seq"]] != SEQ: e.append("pal-v2.2.json seq != tokens")
    for f, fn in ex.EXPORTS.items():
        p = f"{ROOT}/tokens/build/{f}"
        if not os.path.exists(p) or open(p).read() != fn(): e.append(f"tokens/build/{f} is stale: run scripts/export_tokens.py")
    ns = {}; exec(open(f"{ROOT}/tokens/build/andura.py").read(), ns)
    for p, v in ex.TOKENS:
        if ns["ANDURA"].get(ex.name(p, "-")) != ex.scalar(v)[0]: e.append(f"andura.py {ex.name(p, '-')} differs"); break
    for p in glob.glob(f"{ROOT}/examples/*.html"):
        e += check_example(os.path.basename(p), open(p).read()) + check_recipes(os.path.basename(p), open(p).read())
    for p in glob.glob(f"{ROOT}/examples/*.css"):  # shared example stylesheet: same token-only rules
        e += check_example(os.path.basename(p), open(p).read(), sheet=True)
    ch = open(f"{ROOT}/CHANGELOG.md").read() if os.path.exists(f"{ROOT}/CHANGELOG.md") else ""
    m = re.search(r"^## \[?([0-9][^\]\s]*)", ch, re.M)
    if not m or m.group(1) != VERSION: e.append(f"CHANGELOG top entry {m and m.group(1)} != tokens {VERSION}")
    return e

LEAK = re.compile("/" + "home/box|/" + "workspace\\b|/" + "Users/")  # split so this file does not match itself

def check_leaks(name, t):
    """No internal machine paths in shipped files."""
    return [f"{name}:{t.count(chr(10), 0, m.start()) + 1}: internal path {m.group(0)!r}" for m in LEAK.finditer(t)]

def shipped():
    """Every text file git would ship (tracked + untracked, not ignored)."""
    r = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True)
    names = r.stdout.split() if r.returncode == 0 else [os.path.relpath(p, ROOT) for p in glob.glob(f"{ROOT}/**/*", recursive=True) if os.path.isfile(p)]
    out = {}
    for n in names:
        try: out[n] = open(f"{ROOT}/{n}", encoding="utf-8").read()
        except (UnicodeDecodeError, OSError): pass
    return out

def run(S, R):
    e = check_skill(S) + check_refs(R) + check_bans("SKILL.md", S) + check_leaks("SKILL.md", S)
    for n, t in R.items(): e += check_bans(f"references/{n}", t) + check_leaks(f"references/{n}", t)
    return e

def selftest(S, R):
    """Inject one violation per check family; each must produce at least one failure."""
    cases = {
        "SKILL hex": (S.replace("`#3C3D41`", "`#3C3D42`", 1), R),
        "SKILL contrast": (S.replace("15.05 / 14.20", "15.05 / 13.33", 1), R),
        "SKILL type": (S.replace("| 36/40 |", "| 36/44 |", 1), R),
        "SKILL breakpoint": (S.replace("| Tablet | 600 |", "| Tablet | 640 |", 1), R),
        "motion.md duration": (S, {**R, "motion.md": R["motion.md"].replace("| `duration.base` | 200 ms", "| `duration.base` | 250 ms", 1)}),
        "ref non-token hex": (S, {**R, "viewport.md": R["viewport.md"] + "\nfill #123456\n"}),
        "SKILL version": (S.replace("version: ", "version: 9", 1), R),
        "ref contrast": (S, {**R, "colour.md": R["colour.md"].replace("| 6.24 |", "| 6.20 |", 1)}),
        "ref phone type": (S, {**R, "typography.md": R["typography.md"].replace("| 28/32 Mono", "| 28/36 Mono", 1)}),
        "ban Light": (S, {**R, "research.md": R["research.md"] + "\nDisplay in Plex Light.\n"}),
        "ban 300": (S, {**R, "research.md": R["research.md"] + "\nweight 300 for hero\n"}),
        "ban Sans 600": (S, {**R, "research.md": R["research.md"] + "\nheadings Sans 600\n"}),
        "ban Surface": (S, {**R, "research.md": R["research.md"] + "\nSurface `#121314`\n"}),
        "ban focus": (S, {**R, "research.md": R["research.md"] + "\nfocus ring #5A74F1 2 px\n"}),
        "ban status bar": (S, {**R, "research.md": R["research.md"] + "\nstatus bar 40 px\n"}),
        "ban delta": (S + "\nΔ 0.4\n", R),
        "internal path": (S, {**R, "research.md": R["research.md"] + "\nsee /" + "home/box/x\n"}),
    }
    ex_html = open(f"{ROOT}/examples/l1-alarm.html").read()
    for n, bad in {"example hex": ex_html.replace("</head>", "<style>.x{color:#3A3CFF}</style></head>", 1),
                   "example rgb": ex_html.replace("</head>", "<style>.x{color:rgb(0,0,0)}</style></head>", 1),
                   "example unknown token": ex_html.replace("</head>", "<style>.x{color:var(--andura-color-pink)}</style></head>", 1),
                   "example hex in style attr": ex_html.replace("<body", '<body style="color:#3A3CFF"', 1),
                   "example hex before quote": ex_html.replace("<body", '<body data-x="a" title="#3A3CFF"', 1),
                   "example no stylesheet link": re.sub(r'<link rel="stylesheet" href="[^"]*andura\.css">', "<!-- andura.css -->", ex_html),
                   "example hand-typed px": ex_html.replace("</head>", "<style>.x{width:57px}</style></head>", 1),
                   "example px equal to a token": ex_html.replace("</head>", "<style>.x{height:56px}</style></head>", 1),
                   "example hand-typed ms": ex_html.replace("</head>", "<style>.x{transition:opacity 200ms}</style></head>", 1),
                   "recipe drift (alarm row without edge)": ex_html.replace('<div class="r p1"><span class="edge"></span>', '<div class="r p1">', 1),
                   "recipe drift (dialog focus not on cancel)": ex_html.replace('<button class="btn hit" autofocus', '<button class="btn hit"', 1),
                   "non-canonical glyph": ex_html.replace('M8 0l8 15H0z', 'M8 0l7 15H1z', 1),
                   "example raw hex outside the inlined block": re.sub(r'<link rel="stylesheet" href="[^"]*andura\.css">', lambda m: "<style>" + CSS + "</style>", ex_html).replace("</body>", '<i style="color:#3A3CFF"></i></body>')}.items():
        # run() does not read examples; map "check_example flagged it" onto a case run() flags.
        cases[n] = (S + "\nΔ", R) if check_example("l1-alarm.html", bad) + check_recipes("l1-alarm.html", bad) else (S, R)
    if MODES.get("sunlit"):  # a sunlit colour below its contrast target must fail
        c = MODES["sunlit"]["color"]; keep = c["muted"]; c["muted"] = COLOR["muted"]
        cases["sunlit Muted below 7:1"] = (S + "\nΔ", R) if check_modes(R.get("colour.md", "")) else (S, R); c["muted"] = keep
    allowed = [S + "\nhover 300 ms, peek 300 / 500 ms, Lighting soft.\n", R]
    # a self-contained page with andura.css inlined (raw hexes and px inside that block) must pass
    selfcontained = re.sub(r'<link rel="stylesheet" href="[^"]*andura\.css">', lambda m: "<style>/* andura.css */\n" + CSS + "</style>", ex_html)
    if check_example("inline", selfcontained): allowed[0] += "\nΔ"
    e = [f"self-test: '{n}' was not detected" for n, (s, r) in cases.items() if not run(s, r)]
    if run(*allowed): e.append(f"self-test: allowed text flagged: {run(*allowed)}")
    return e, len(cases) + 1

if __name__ == "__main__":
    if "--example" in sys.argv:  # check one screen of your own: python3 scripts/check.py --example path.html
        f = sys.argv[sys.argv.index("--example") + 1]
        errs = check_example(os.path.basename(f), open(f).read()) + check_recipes(os.path.basename(f), open(f).read())
        print(f"{'PASS' if not errs else 'FAIL'}  example {f}"); [print("   ", x) for x in errs]
        sys.exit(1 if errs else 0)
    S = open(f"{ROOT}/SKILL.md").read()
    R = {os.path.basename(p): open(p).read() for p in sorted(glob.glob(f"{ROOT}/references/*.md"))}
    groups = [("SKILL.md vs tokens", check_skill(S)), ("references vs tokens", check_refs(R)),
              ("banned values", check_bans("SKILL.md", S) + sum((check_bans(f"references/{n}", t) for n, t in R.items()), [])),
              ("pal json + exports", check_data()),
              ("colour modes (sunlit contrast targets)", check_modes(R.get("colour.md", ""))),
              ("no internal paths in shipped files", sum((check_leaks(n, t) for n, t in shipped().items()), []))]
    st, n = selftest(S, R)
    groups.append((f"self-test ({n} cases)", st))
    fail = 0
    for name, errs in groups:
        print(f"{'PASS' if not errs else 'FAIL'}  {name}")
        for x in errs: print("   ", x)
        fail += len(errs)
    print(f"{'OK' if not fail else f'{fail} failure(s)'}")
    sys.exit(1 if fail else 0)
