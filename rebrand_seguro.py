#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rebrand visible TENISI->StepUp. NUNCA toca URLs, slugs, archivos ni CDN."""
import pathlib, re
ROOT = pathlib.Path("/home/kali/proj/site")
URL_GUARD = re.compile(r'(https?:)?//[^\s"\'<>]*', re.I)
def safe_sub(pat, rep, text):
    out = []
    last = 0
    for m in URL_GUARD.finditer(text):
        seg = text[last:m.start()]
        seg = re.sub(pat, rep, seg)
        out.append(seg); out.append(m.group(0))
        last = m.end()
    seg = text[last:]
    out.append(re.sub(pat, rep, seg))
    return "".join(out)
REPS = [
    (r'TENISI\.CO', 'STEPUP'),
    (r'TENISÍ', 'StepUp'),
    (r'Tenisí', 'StepUp'),
    (r'(?<![A-Za-z])TENISI(?![A-Za-z/])', 'STEPUP'),
    (r'(?<![A-Za-z/])Tenisi(?![A-Za-z/])', 'StepUp'),
    (r'atencion@tenisi\.co', 'atencion@stepup.co'),
    (r' X Tenisi ', ' X StepUp '),
    (r'"title"\s*:\s*"([^"]*?)x Tenisi"', r'"title":"\1x StepUp"'),
]
n = 0
for fp in sorted(ROOT.rglob("*")):
    if not fp.is_file() or fp.suffix not in {".html", ".js"}: continue
    h = fp.read_bytes().decode("utf-8", errors="ignore")
    h2 = h
    for pat, rep in REPS:
        h2 = safe_sub(pat, rep, h2)
    if h2 != h:
        fp.write_bytes(h2.encode("utf-8")); n += 1
print("ARCHIVOS:", n)
