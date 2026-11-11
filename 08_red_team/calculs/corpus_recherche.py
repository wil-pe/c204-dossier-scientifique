#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G (red team) — outil de recherche dans le corpus textuel attribué à « John Titor ».

Usage :
    python corpus_recherche.py "regex1" ["regex2" ...] [--ctx N] [--max M]

Pour chaque occurrence, affiche la date d'en-tête la plus proche qui précède (les messages de la
compilation marinertalk sont introduits par des lignes de date du type « November 04, 2000 » ou
« 01-27-2001 12:45 PM ») ainsi qu'un contexte de N caractères autour de l'occurrence.
Lecture seule ; le fichier source n'est jamais modifié.
"""
import re, sys, argparse

SRC = _RACINE + "/01_archive/sources_web/marinertalk_t7778_texte_integral.txt"

DATE_RE = re.compile(
    r"^(?:\s*)((?:January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2},?\s+\d{4}(?:\s+\d{1,2}:\d{2}(?:\s*[AP]M)?)?|\d{1,2}-\d{1,2}-\d{4}(?:\s+\d{1,2}:\d{2}\s*[AP]M)?)\s*$",
    re.M)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patterns", nargs="+")
    ap.add_argument("--ctx", type=int, default=220)
    ap.add_argument("--max", type=int, default=40)
    a = ap.parse_args()
    txt = open(SRC, encoding="utf-8", errors="replace").read()
    dates = [(m.start(), m.group(1).strip()) for m in DATE_RE.finditer(txt)]
    def date_at(pos):
        d = "?"
        for p, s in dates:
            if p <= pos: d = s
            else: break
        return d
    for pat in a.patterns:
        rx = re.compile(pat, re.I)
        ms = list(rx.finditer(txt))
        print(f"\n===== /{pat}/ : {len(ms)} occurrence(s) =====")
        last_end = -1
        n = 0
        for m in ms:
            if m.start() < last_end:      # évite les doublons de contexte
                continue
            s = max(0, m.start() - a.ctx); e = min(len(txt), m.end() + a.ctx)
            last_end = e
            snippet = re.sub(r"\s+", " ", txt[s:e])
            print(f"[{date_at(m.start())} | car. {m.start()}] …{snippet}…")
            n += 1
            if n >= a.max:
                print("  (troncature --max)")
                break

if __name__ == "__main__":
    main()
