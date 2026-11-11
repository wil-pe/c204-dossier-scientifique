#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparaison des copies alternatives avec les 12 pièces marinertalk (01_archive/originaux/).

Pour chaque couple (original, copie) :
  - identité binaire (SHA-256) ;
  - distance de Hamming entre hachages perceptuels pHash 64 bits (image entière, sensible au recadrage) ;
  - appariement de points d'intérêt SIFT + similitude RANSAC (robuste au recadrage et à l'échelle) :
    nombre de points concordants (« inliers ») et facteur d'échelle linéaire copie/original ;
  - netteté (variance du laplacien) et estimation de la qualité JPEG (tables de quantification).

Sortie : 01_archive/analyses/comparaison_copies.csv  (lecture seule des images ; à lancer avec python -I)
"""
import csv
import hashlib
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(RACINE, "originaux")
ALT = os.path.join(RACINE, "copies_alternatives")
SORTIE = os.path.join(RACINE, "analyses", "comparaison_copies.csv")


def charger(chemin):
    im = Image.open(chemin)
    try:
        im.seek(0)
    except Exception:
        pass
    g = np.array(im.convert("L"))
    q = None
    if im.format == "JPEG" and getattr(im, "quantization", None):
        t = np.array(list(im.quantization[0]), dtype=float)
        q = float(t.mean())  # moyenne de la table de luminance : petit = haute qualité
    return g, im.size, im.format, q


def phash(g):
    p = cv2.resize(g, (32, 32), interpolation=cv2.INTER_AREA).astype(np.float32)
    d = cv2.dct(p)[:8, :8]
    med = np.median(d.flatten()[1:])
    return (d > med).flatten()


def nettete(g):
    return float(cv2.Laplacian(g, cv2.CV_64F).var())


SIFT = cv2.SIFT_create(nfeatures=3000)


def sift(g):
    # petites images : agrandir pour obtenir assez de points
    f = 1.0
    if max(g.shape) < 500:
        f = 2.0
        g = cv2.resize(g, None, fx=f, fy=f, interpolation=cv2.INTER_CUBIC)
    kp, des = SIFT.detectAndCompute(g, None)
    pts = np.array([k.pt for k in kp], dtype=np.float32) / f if kp else np.zeros((0, 2), np.float32)
    return pts, des


def apparier(a, b):
    """Renvoie (inliers, échelle de b par rapport à a) ; a = original, b = copie."""
    pa, da = a
    pb, db = b
    if da is None or db is None or len(pa) < 8 or len(pb) < 8:
        return 0, None
    m = cv2.BFMatcher(cv2.NORM_L2).knnMatch(da, db, k=2)
    bons = [x for x, y in (p for p in m if len(p) == 2) if x.distance < 0.75 * y.distance]
    if len(bons) < 8:
        return len(bons), None
    src = np.float32([pa[x.queryIdx] for x in bons]).reshape(-1, 1, 2)
    dst = np.float32([pb[x.trainIdx] for x in bons]).reshape(-1, 1, 2)
    # Similitude (échelle + rotation + translation) : plus stricte qu'une homographie, elle évite les
    # faux appariements dégénérés sur les images tramées ou bruitées.
    M, masque = cv2.estimateAffinePartial2D(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    if M is None:
        return 0, None
    inl = int(masque.sum())
    ech = float(np.hypot(M[0, 0], M[1, 0]))
    rot = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
    if not (0.3 <= ech <= 3.5) or abs(rot) > 8:
        return 0, None
    return inl, ech


def main():
    originaux = sorted(os.listdir(ORIG))
    copies = []
    for d, _, fs in os.walk(ALT):
        for f in sorted(fs):
            if f.lower().endswith(".pdf"):
                continue
            copies.append(os.path.join(d, f))
    info = {}
    for c in [os.path.join(ORIG, o) for o in originaux] + copies:
        try:
            g, taille, fmt, q = charger(c)
        except Exception as e:
            print("illisible", c, e, file=sys.stderr)
            continue
        info[c] = dict(g=g, taille=taille, fmt=fmt, q=q, ph=phash(g), net=nettete(g), sift=sift(g),
                       sha=hashlib.sha256(open(c, "rb").read()).hexdigest())
    with open(SORTIE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["original", "orig_px", "copie", "copie_px", "format", "sha256_identique", "phash_hamming",
                    "sift_inliers", "echelle_copie_sur_original", "nettete_laplacien_copie",
                    "nettete_laplacien_original", "qtable_moy_copie", "sha256_copie"])
        vus = set()
        for o in originaux:
            co = os.path.join(ORIG, o)
            if co not in info:
                continue
            io = info[co]
            for c in copies:
                if c not in info:
                    continue
                ic = info[c]
                ham = int((io["ph"] != ic["ph"]).sum())
                ident = io["sha"] == ic["sha"]
                inl, ech = apparier(io["sift"], ic["sift"])
                if not ident and ham > 10 and inl < 30:
                    continue
                cle = (o, ic["sha"])
                if cle in vus:
                    continue
                vus.add(cle)
                w.writerow([o, "%dx%d" % io["taille"], os.path.relpath(c, RACINE), "%dx%d" % ic["taille"],
                            ic["fmt"], "oui" if ident else "non", ham, inl,
                            "" if ech is None else f"{ech:.3f}", f"{ic['net']:.0f}", f"{io['net']:.0f}",
                            "" if ic["q"] is None else f"{ic['q']:.1f}", ic["sha"]])
    print("écrit :", SORTIE)


if __name__ == "__main__":
    main()
