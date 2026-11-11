#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Téléchargement d'images/PDF depuis la Wayback Machine (octets bruts, modificateur « id_ »)
et tenue du journal de provenance.

Usage :
    python -I telecharger_wayback.py <liste.tsv> <dossier_sortie> <journal.csv>

<liste.tsv> : une ligne par pièce, colonnes séparées par des tabulations :
    horodatage_wayback (14 chiffres) <TAB> url_originale <TAB> étiquette_source
Pour une URL « vivante » (non Wayback), mettre « LIVE » comme horodatage.

Règles de sécurité : seuls les fichiers dont la signature binaire est celle d'une image
(JPEG, PNG, GIF, BMP, TIFF, WEBP) ou d'un PDF sont conservés ; tout autre contenu est rejeté.
Rien de ce qui est téléchargé n'est exécuté.
"""
import csv
import datetime
import hashlib
import io
import os
import re
import subprocess
import sys
import time

from PIL import Image

AGENT = "Mozilla/5.0 (compatible; archivage-documentaire; curl)"

SIGNATURES = [
    (b"\xff\xd8\xff", "JPEG"),
    (b"\x89PNG\r\n\x1a\n", "PNG"),
    (b"GIF87a", "GIF"),
    (b"GIF89a", "GIF"),
    (b"BM", "BMP"),
    (b"II*\x00", "TIFF"),
    (b"MM\x00*", "TIFF"),
    (b"%PDF", "PDF"),
]

CHAMPS = [
    "fichier_local", "source", "url_originale", "url_telechargement", "date_capture_wayback",
    "date_telechargement_utc", "sha256", "format", "largeur_px", "hauteur_px", "taille_octets",
    "statut", "remarque",
]


def signature(octets):
    for sig, nom in SIGNATURES:
        if octets.startswith(sig):
            return nom
    if octets[:4] == b"RIFF" and octets[8:12] == b"WEBP":
        return "WEBP"
    return None


def nom_sur(url):
    base = url.split("?")[0].rstrip("/").split("/")[-1] or "index"
    if "?" in url:
        base += "_" + re.sub(r"[^A-Za-z0-9]+", "-", url.split("?", 1)[1])[:60]
    return re.sub(r"[^A-Za-z0-9._-]+", "_", base)[:120]


def telecharger(url, tentatives=4):
    for i in range(tentatives):
        res = subprocess.run(
            ["curl", "-s", "-L", "-m", "90", "-A", AGENT, "-w", "%{http_code}", "-o", "-", url],
            capture_output=True,
        )
        donnees = res.stdout
        code = donnees[-3:].decode("ascii", "replace") if len(donnees) >= 3 else "000"
        corps = donnees[:-3]
        if code == "200" and corps:
            return code, corps
        if code in ("404", "403"):
            return code, corps
        time.sleep(6 * (i + 1))
    return code, corps


def main():
    liste, sortie, journal = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(sortie, exist_ok=True)
    nouveau = not os.path.exists(journal)
    deja = set()
    if not nouveau:
        with open(journal, newline="", encoding="utf-8") as f:
            for ligne in csv.DictReader(f):
                deja.add(ligne["url_telechargement"])
    with open(journal, "a", newline="", encoding="utf-8") as fj:
        ecr = csv.DictWriter(fj, fieldnames=CHAMPS)
        if nouveau:
            ecr.writeheader()
        for brut in open(liste, encoding="utf-8"):
            brut = brut.rstrip("\n")
            if not brut or brut.startswith("#"):
                continue
            horo, url, source = brut.split("\t")[:3]
            if horo == "LIVE":
                cible = url
                prefixe = "LIVE"
            else:
                cible = f"https://web.archive.org/web/{horo}id_/{url}"
                prefixe = horo
            if cible in deja:
                continue
            code, corps = telecharger(cible)
            maintenant = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            ligne = dict.fromkeys(CHAMPS, "")
            ligne.update(source=source, url_originale=url, url_telechargement=cible,
                         date_capture_wayback=("" if horo == "LIVE" else horo),
                         date_telechargement_utc=maintenant)
            fmt = signature(corps) if corps else None
            if code != "200" or not fmt:
                ligne.update(statut="ECHEC", remarque=f"HTTP {code} ; signature={fmt} ; {len(corps)} octets (non conservé)")
                ecr.writerow(ligne)
                fj.flush()
                print("ECHEC", code, fmt, url)
                time.sleep(1.5)
                continue
            nom = f"{prefixe}__{nom_sur(url)}"
            chemin = os.path.join(sortie, nom)
            with open(chemin, "wb") as f:
                f.write(corps)
            os.chmod(chemin, 0o444)
            larg = haut = ""
            rem = ""
            if fmt != "PDF":
                try:
                    im = Image.open(io.BytesIO(corps))
                    larg, haut = im.size
                    rem = f"mode={im.mode}"
                    if getattr(im, "n_frames", 1) > 1:
                        rem += f" ; {im.n_frames} images (animation)"
                except Exception as e:  # image tronquée ou illisible
                    rem = f"illisible par PIL : {e}"
            ligne.update(fichier_local=os.path.relpath(chemin, os.path.dirname(journal)),
                         sha256=hashlib.sha256(corps).hexdigest(), format=fmt,
                         largeur_px=larg, hauteur_px=haut, taille_octets=len(corps),
                         statut="OK", remarque=rem)
            ecr.writerow(ligne)
            fj.flush()
            print("OK", fmt, larg, haut, len(corps), url)
            time.sleep(1.2)


if __name__ == "__main__":
    main()
