#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, colorsys, pathlib, re, shutil, sys
from collections import Counter, defaultdict
CSS_VARS = {
    "--bg": "#FAF9F6", "--bg-2": "#F0EBE1", "--rose": "#2C2A29",
    "--rose-btn": "#1A1A1A", "--rose-deep": "#000000",
    "--rose-soft": "#EFECE6", "--rose-line": "#DCD5CB", "--green": "#3A4F3C",
}
WINE = "#5E2628"
RULES = {
    ".p-off": {"background": WINE},
    ".disc": {"background": WINE},
    ".cod": {"background": "#E6E8E3", "color": "#2F3E2B", "border": "1px solid #D3D8CE"},
    ".hb-announce": {"background": "#EFECE6", "color": "#111111"},
    ".hb-ann-price": {"color": "#111111", "text-shadow": "none"},
    ".hb-ann-long": {"color": "#555555"},
    ".hb-ann-end": {"color": "#555555"},
}
GRADIENTS = {
    ("#0B0B0F", "#E04A7B"): ("#2B2623", "#4A3F38"),
    ("#1B181A", "#3d3538"): ("#2A2A2A", "#111111"),
    ("#B82E5E", "#7A2245"): ("#4A2527", "#2A1416"),
    ("#E04A7B", "#B82E5E"): ("#4A4A4A", "#2B2B2B"),
}
LITERALS = {"#E04A7B": "#2C2A29", "#B82E5E": "#1A1A1A", "#7A2245": WINE}
OLD_HACK_IDS = ("luxury-theme", "lujo-silencioso")
EXTS = {".html", ".htm", ".css", ".js"}
BACKUP_DIR = pathlib.Path("_backup_antes_lujo")
SKIP_DIRS = {"node_modules", ".git", BACKUP_DIR.name}
COMMENT = re.compile(r"/\*.*?\*/", re.S)
BLOCK = re.compile(r"\{([^{}]*)\}")
VALUE = r"(?:[^;(){}]|\((?:[^()]|\([^()]*\))*))*"
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def set_var(text, name, value, stats):
    pat = re.compile(r"(?<![\w-])(" + re.escape(name) + r")(\s*:\s*)([^;}\"'\n]+)", re.I)
    def repl(m):
        imp = " !important" if "!important" in m.group(3).lower() else ""
        return m.group(1) + m.group(2) + value + imp
    text, n = pat.subn(repl, text)
    stats["variable " + name] += n
    return text
def set_decls(body, decls):
    for prop, val in decls.items():
        pat = re.compile(r"(?<![\w-])" + re.escape(prop) + r"(\s*:\s*)(" + VALUE + r")", re.I)
        if pat.search(body):
            def repl(m, prop=prop, val=val):
                imp = " !important" if "!important" in m.group(2).lower() else ""
                return prop + m.group(1) + val + imp
            body = pat.sub(repl, body)
        else:
            stripped = body.rstrip()
            ws = body[len(stripped):]
            sep = "" if (not stripped or stripped.endswith(";")) else ";"
            body = stripped + sep + prop + ":" + val + ";" + ws
    return body
def apply_rules(text, stats):
    out, last = [], 0
    for m in BLOCK.finditer(text):
        s = m.start()
        b = max(text.rfind("}", 0, s), text.rfind("{", 0, s), text.rfind(";", 0, s)) + 1
        selector = COMMENT.sub("", text[max(b, s-400):s])
        sels = [x.strip() for x in selector.split(",")]
        body = m.group(1)
        new_body = body
        for target, decls in RULES.items():
            if any(x.endswith(target) for x in sels):
                stats["regla " + target] += 1
                new_body = set_decls(new_body, decls)
        if new_body != body:
            out.append(text[last:m.start(1)])
            out.append(new_body)
            last = m.end(1)
    out.append(text[last:])
    return "".join(out)
def apply_gradients(text, stats):
    for (o1, o2), (n1, n2) in GRADIENTS.items():
        pat = re.compile(r"linear-gradient\(\s*([^,()]+?)\s*,\s*" + re.escape(o1) + r"(?![0-9a-fA-F])\s*,\s*" + re.escape(o2) + r"(?![0-9a-fA-F])\s*\)", re.I)
        text, n = pat.subn(lambda m, n1=n1, n2=n2: "linear-gradient(" + m.group(1) + ", " + n1 + ", " + n2 + ")", text)
        stats["degradado " + o1 + "->" + o2] += n
    return text
def apply_literals(text, stats):
    for old, new in LITERALS.items():
        pat = re.compile(re.escape(old) + r"(?![0-9a-fA-F])", re.I)
        text, n = pat.subn(new, text)
        r, g, b = hex_to_rgb(old)
        nr, ng, nb = hex_to_rgb(new)
        pat2 = re.compile(r"(rgba?\(\s*)" + str(r) + r"(\s*,\s*)" + str(g) + r"(\s*,\s*)" + str(b) + r"(?!\d)", re.I)
        text, n2 = pat2.subn(lambda m: m.group(1) + str(nr) + m.group(2) + str(ng) + m.group(3) + str(nb), text)
        stats["color suelto " + old] += n + n2
    return text
def remove_old_hacks(text, stats):
    ids = "|".join(re.escape(i) for i in OLD_HACK_IDS)
    pat = re.compile(r"\s*<style\b[^>]*\bid\s*=\s*[\"']?(?:" + ids + r")[\"']?[^>]*>.*?</style>", re.S | re.I)
    text, n = pat.subn("", text)
    stats["hack anterior eliminado"] += n
    return text
def transform(text, suffix, stats):
    if suffix in (".html", ".htm"):
        text = remove_old_hacks(text, stats)
    for name, value in CSS_VARS.items():
        text = set_var(text, name, value, stats)
    text = apply_rules(text, stats)
    text = apply_gradients(text, stats)
    text = apply_literals(text, stats)
    return text
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default="site")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--no-backup", action="store_true")
    args = ap.parse_args()
    site = pathlib.Path(args.site)
    if not site.is_dir():
        print("ERROR: no existe " + str(site)); return 1
    originals = {}
    for p in sorted(site.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXTS or (set(p.parts) & SKIP_DIRS):
            continue
        try:
            originals[p] = p.read_bytes().decode("utf-8")
        except UnicodeDecodeError:
            print("AVISO: " + str(p) + " no UTF-8, se omite.")
    print("Archivos:", len(originals), flush=True)
    stats = Counter()
    results, changed = {}, []
    for p, original in originals.items():
        new = transform(original, p.suffix.lower(), stats)
        if new.count("{") - new.count("}") != original.count("{") - original.count("}"):
            print("ERROR llaves: " + str(p)); results[p] = original; continue
        results[p] = new
        if new != original: changed.append(p)
    if not args.dry_run:
        for p in changed:
            if not args.no_backup:
                dest = BACKUP_DIR / p
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(p, dest)
            p.write_bytes(results[p].encode("utf-8"))
    print("STATS:")
    for k, v in stats.most_common():
        print("  " + k + ": " + str(v))
    print(("SIMULACION: " if args.dry_run else "APLICADO: ") + str(len(changed)))
    return 0
if __name__ == "__main__":
    sys.exit(main())
