#!/usr/bin/env python3
"""Affiche les résumés (abstracts) arXiv présents dans le cache pour une liste d'identifiants.
Usage : python -I resumes.py <dossier 09> <longueur_max> id1 id2 ...   (lecture seule du cache)"""
import pathlib, re, sys
import xml.etree.ElementTree as ET
ATOM = "{http://www.w3.org/2005/Atom}"
base = pathlib.Path(sys.argv[1]); n = int(sys.argv[2]); ids = sys.argv[3:]
found = {}
for f in (base / "donnees_brutes" / "cache").glob("*.txt"):
    t = f.read_text(encoding="utf-8")
    if "<feed" not in t[:400]:
        continue
    try:
        root = ET.fromstring(t)
    except ET.ParseError:
        continue
    for e in root.findall(ATOM + "entry"):
        m = re.search(r"abs/(.+?)(v\d+)?$", (e.findtext(ATOM + "id") or "").strip())
        if m:
            found[m.group(1)] = (re.sub(r"\s+", " ", e.findtext(ATOM + "title") or ""),
                                 re.sub(r"\s+", " ", e.findtext(ATOM + "summary") or "").strip())
for i in ids:
    if i in found:
        print(f"## {i} — {found[i][0][:90]}\n{found[i][1][:n]}\n")
    else:
        print(f"## {i} — ABSENT DU CACHE\n")
