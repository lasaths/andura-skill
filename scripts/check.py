"""ANDURA verification. Run from anywhere: python3 scripts/check.py
Source of truth: tokens/andura.tokens.json. Checks SKILL.md, references/*.md, assets/pal-v2.2.json and
tokens/build/* against it, scans for banned values, then runs a self-test that injects one violation per
check and confirms it fails. Exit code 0 = all pass; 1 = failures (each printed)."""
import glob, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{ROOT}/scripts")
import export_tokens as ex

TOK = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))
COLOR = {k: v["$value"].upper() for k, v in TOK["color"].items() if "$value" in v}
SEQ = [TOK["color"]["data"]["cividis"][str(i)]["$value"].upper() for i in range(7)]
THREE = {k: v["$value"].upper() for k, v in TOK["color"]["3d"].items()}
ALLHEX = set(COLOR.values()) | set(SEQ) | set(THREE.values())
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
            if not r[4].startswith(str(px(sz["topline"][cls]))): e.append(f"SKILL top line {cls} {r[4]}")
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
        for m in re.finditer(r"\bSurface\b(?!(?i: lift| hover))[^#\n]{0,12}(#[0-9A-Fa-f]{6})", line):
            if m.group(1).upper() != COLOR["surface"]: e.append(f"{name}:{i} Surface {m.group(1)} != {COLOR['surface']}")
        if re.search(r"(?i)5A74F1", line) and re.search(r"(?i)focus\s*ring|focus ring", line) and not re.search(r"(?i)\bnever\b|\bnot\b|links only", line):
            e.append(f"{name}:{i} Ultramarine Text used as focus ring")
    return e

CSS = open(f"{ROOT}/tokens/build/andura.css").read()
def check_example(name, t):
    """An example may use colours only through var(--andura-*) tokens that exist, and must load andura.css."""
    e = []
    for bad in re.findall(r"#[0-9A-Fa-f]{3,8}\b(?![^<]*\")|rgba?\(|hsla?\(", re.sub(r'href="[^"]*"', "", t)):
        e.append(f"{name}: literal colour {bad}; use var(--andura-color-*)")
    for v in set(re.findall(r"var\((--andura-[a-zA-Z0-9-]+)\)", t)):
        if v + ":" not in CSS: e.append(f"{name}: unknown token {v}")
    if "andura.css" not in t: e.append(f"{name} does not load tokens/build/andura.css")
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
        e += check_example(os.path.basename(p), open(p).read())
    ch = open(f"{ROOT}/CHANGELOG.md").read() if os.path.exists(f"{ROOT}/CHANGELOG.md") else ""
    m = re.search(r"^## \[?([0-9][^\]\s]*)", ch, re.M)
    if not m or m.group(1) != VERSION: e.append(f"CHANGELOG top entry {m and m.group(1)} != tokens {VERSION}")
    return e

def run(S, R):
    e = check_skill(S) + check_refs(R) + check_bans("SKILL.md", S)
    for n, t in R.items(): e += check_bans(f"references/{n}", t)
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
    }
    ex_html = open(f"{ROOT}/examples/l1-alarm.html").read()
    for n, bad in {"example hex": ex_html.replace("</style>", ".x{color:#3A3CFF}</style>", 1),
                   "example rgb": ex_html.replace("</style>", ".x{color:rgb(0,0,0)}</style>", 1),
                   "example unknown token": ex_html.replace("</style>", ".x{color:var(--andura-color-pink)}</style>", 1)}.items():
        # run() does not read examples; map "check_example flagged it" onto a case run() flags.
        cases[n] = (S + "\nΔ", R) if check_example("l1-alarm.html", bad) else (S, R)
    allowed = [S + "\nhover 300 ms, peek 300 / 500 ms, Lighting soft.\n", R]
    e = [f"self-test: '{n}' was not detected" for n, (s, r) in cases.items() if not run(s, r)]
    if run(*allowed): e.append(f"self-test: allowed text flagged: {run(*allowed)}")
    return e, len(cases) + 1

if __name__ == "__main__":
    S = open(f"{ROOT}/SKILL.md").read()
    R = {os.path.basename(p): open(p).read() for p in sorted(glob.glob(f"{ROOT}/references/*.md"))}
    groups = [("SKILL.md vs tokens", check_skill(S)), ("references vs tokens", check_refs(R)),
              ("banned values", check_bans("SKILL.md", S) + sum((check_bans(f"references/{n}", t) for n, t in R.items()), [])),
              ("pal json + exports", check_data())]
    st, n = selftest(S, R)
    groups.append((f"self-test ({n} cases)", st))
    fail = 0
    for name, errs in groups:
        print(f"{'PASS' if not errs else 'FAIL'}  {name}")
        for x in errs: print("   ", x)
        fail += len(errs)
    print(f"{'OK' if not fail else f'{fail} failure(s)'}")
    sys.exit(1 if fail else 0)
