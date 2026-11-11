#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement de pages HTML/texte archivées (Wayback, modificateur « id_ ») avec reprises.

Usage : python -I telecharger_pages.py <liste.tsv> <dossier_sortie>
<liste.tsv> : horodatage <TAB> url <TAB> nom_de_fichier_de_sortie
Les pages sont enregistrées telles quelles (données non fiables, jamais exécutées).
Un index « _index_pages.tsv » (horodatage, url, fichier, taille, sha256, code HTTP) est tenu dans le dossier.
"""
import hashlib
import os
import subprocess
import sys
import time

AGENT = "Mozilla/5.0 (compatible; archivage-documentaire; curl)"


def recuperer(url, tentatives=5):
    code, corps = "000", b""
    for i in range(tentatives):
        res = subprocess.run(
            ["curl", "-s", "-L", "-m", "90", "-A", AGENT, "-w", "%{http_code}", "-o", "-", url],
            capture_output=True,
        )
        d = res.stdout
        code = d[-3:].decode("ascii", "replace") if len(d) >= 3 else "000"
        corps = d[:-3]
        if code == "200" and corps:
            break
        if code in ("404", "403"):
            break
        time.sleep(8 * (i + 1))
    return code, corps


def main():
    liste, sortie = sys.argv[1], sys.argv[2]
    os.makedirs(sortie, exist_ok=True)
    index = os.path.join(sortie, "_index_pages.tsv")
    with open(index, "a", encoding="utf-8") as fi:
        for ligne in open(liste, encoding="utf-8"):
            ligne = ligne.rstrip("\n")
            if not ligne or ligne.startswith("#"):
                continue
            horo, url, nom = ligne.split("\t")[:3]
            chemin = os.path.join(sortie, nom)
            if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
                continue
            cible = url if horo == "LIVE" else f"https://web.archive.org/web/{horo}id_/{url}"
            code, corps = recuperer(cible)
            if code == "200" and corps:
                with open(chemin, "wb") as f:
                    f.write(corps)
                fi.write(f"{horo}\t{url}\t{nom}\t{len(corps)}\t{hashlib.sha256(corps).hexdigest()}\t{code}\n")
                print("OK", nom, len(corps))
            else:
                fi.write(f"{horo}\t{url}\t{nom}\t0\t\t{code}\n")
                print("ECHEC", code, url)
            fi.flush()
            time.sleep(1.5)


if __name__ == "__main__":
    main()
