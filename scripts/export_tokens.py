"""Export tokens/andura.tokens.json to CSS, TypeScript, Python and C#. Usage: python3 scripts/export_tokens.py"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOK = json.load(open(f"{ROOT}/tokens/andura.tokens.json"))

def flat(node, path=()):
    """Yield (path, value) for every leaf. Composite typography is split into its fields; references are resolved."""
    if isinstance(node, dict) and "$value" in node:
        v = node["$value"]
        if node.get("$type") == "typography":
            for f, x in v.items():
                yield path + (f,), resolve(x)
        else:
            yield path, resolve(v)
        return
    for k, x in node.items():
        if not k.startswith("$"):
            yield from flat(x, path + (k,))

def resolve(v):
    if isinstance(v, str) and v.startswith("{"):
        n = TOK
        for p in v.strip("{}").split("."):
            n = n[p]
        return resolve(n["$value"])
    return v

def scalar(v):
    """Return (number or string, unit). Dimensions and durations become numbers with unit px or ms."""
    if isinstance(v, dict):
        return v["value"], v["unit"]
    if isinstance(v, list) and all(isinstance(x, (int, float)) for x in v):
        return v, "bezier"
    if isinstance(v, list):
        return ", ".join(f'"{x}"' if " " in x else x for x in v), "family"
    return v, ""

TOKENS = list(flat(TOK))

def name(path, sep):
    return sep.join(re.sub(r"[^a-zA-Z0-9]", sep, p) for p in path)

def camel(path):
    s = re.sub(r"[^a-zA-Z0-9]+", " ", " ".join(path)).split()
    return "".join(w[:1].upper() + w[1:] for w in s)

def css():
    out = [":root {"]
    for p, v in TOKENS:
        x, u = scalar(v)
        val = (f"cubic-bezier({', '.join(map(str, x))})" if u == "bezier" else
               f"{x}{u}" if u in ("px", "ms", "em") else str(x))
        out.append(f"  --andura-{name(p, '-')}: {val};")
    return "\n".join(out + ["}"]) + "\n"

def literal(x, lang):
    if isinstance(x, str):
        return '"' + x.replace('"', '\\"') + '"'
    if isinstance(x, list):
        if lang == "cs":
            return "new[] { " + ", ".join(f"{float(i)}f" for i in x) + " }"
        return "[" + ", ".join(map(str, x)) + "]"
    if lang == "cs" and isinstance(x, float):
        return f"{x}f"
    return str(x)

def ts():
    out = ["// Generated from tokens/andura.tokens.json. Units: px for sizes, ms for durations.", "export const andura = {"]
    out += [f'  "{name(p, "-")}": {literal(scalar(v)[0], "ts")},' for p, v in TOKENS]
    return "\n".join(out + ["} as const;"]) + "\n"

def py():
    out = ["# Generated from tokens/andura.tokens.json. Units: px for sizes, ms for durations.", "ANDURA = {"]
    out += [f'    "{name(p, "-")}": {literal(scalar(v)[0], "py")},' for p, v in TOKENS]
    return "\n".join(out + ["}"]) + "\n"

def cs():
    out = ["// Generated from tokens/andura.tokens.json. Units: px (= WPF DIP) for sizes, ms for durations.",
           "public static class Andura", "{"]
    for p, v in TOKENS:
        x, _ = scalar(v)
        typ = "string" if isinstance(x, str) else "float[]" if isinstance(x, list) else "float" if isinstance(x, float) else "int"
        out.append(f"    public static readonly {typ} {camel(p)} = {literal(x, 'cs')};")
    return "\n".join(out + ["}"]) + "\n"

FONT_DIR = "../../render/fonts"  # relative to tokens/build/; scripts/render_hero.py downloads IBM Plex (OFL) there
FONT_FILES = [("font-family-mono", "IBMPlexMono-Regular.ttf", "400", ""), ("font-family-mono", "IBMPlexMono-Medium.ttf", "500", " Medium"),
              ("font-family-sans", "IBMPlexSans[wdth,wght].ttf", "400 500", "")]

def fonts():
    """@font-face rules: an installed local() face first, then the TTFs in render/fonts/. Override FONT_DIR for your app."""
    fam = {name(p, "-"): scalar(v)[0].split(",")[0].strip('"') for p, v in TOKENS if p[:2] == ("font", "family")}
    out = ["/* Generated from tokens/andura.tokens.json. IBM Plex is SIL OFL 1.1 and not bundled: run scripts/render_hero.py or put the",
           "   TTFs in render/fonts/ (or edit FONT_DIR in scripts/export_tokens.py). */"]
    for key, f, w, sfx in FONT_FILES:
        out.append(f"@font-face {{ font-family: \"{fam[key]}\"; font-weight: {w}; font-display: swap; "
                   f"src: local(\"{fam[key]}{sfx}\"), url(\"{FONT_DIR}/{f.replace('[', '%5B').replace(']', '%5D')}\") format(\"truetype\"); }}")
    return "\n".join(out) + "\n"

EXPORTS = {"andura.css": css, "andura-fonts.css": fonts, "andura.ts": ts, "andura.py": py, "Andura.cs": cs}

if __name__ == "__main__":
    os.makedirs(f"{ROOT}/tokens/build", exist_ok=True)
    for f, fn in EXPORTS.items():
        open(f"{ROOT}/tokens/build/{f}", "w").write(fn())
    print(f"{len(TOKENS)} tokens -> tokens/build/{', '.join(EXPORTS)}")
