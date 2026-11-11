#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâches 3 et 6. Mesure, sur les deux copies de C204-DOC-014 (variante cotée en mètres), des
longueurs dessinées des cotes 6, 7, 8, 9 et des envergures 11-12-13, puis teste si les valeurs inscrites
(6 m, 5 m, 8 m, 11 m) sont proportionnelles au dessin. Lecture seule des images (python -I conseillé)."""
import json, os, sys
import numpy as np
from PIL import Image

BASE = _RACINE + "/01_archive/copies_alternatives/"
COPIES = {"timetravel16_07 (550x594)": BASE + "bibliotecapleyades.net/LIVE__timetravel16_07.jpg",
          "OP4 (460x600)": BASE + "johntitor.strategicbrains.com/20030805133122__OP4.jpg"}
SEUIL = 110

def runs(v, thr=SEUIL):
    d = v < thr
    out, s = [], None
    for i, b in enumerate(d):
        if b and s is None:
            s = i
        if not b and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, len(d) - 1))
    return out

def fusion(r, trou):
    out = []
    for t in r:
        if out and t[0] - out[-1][1] <= trou:
            out[-1] = (out[-1][0], t[1])
        else:
            out.append(t)
    return out

def plus_long(v):
    r = runs(v)
    return max(r, key=lambda t: t[1] - t[0]) if r else (0, -1)

res = {}
for nom, chemin in COPIES.items():
    a = np.asarray(Image.open(chemin).convert("L")).astype(float)
    H, W = a.shape
    # 1) barre horizontale épaisse (cotes 8 + 9) : segment sombre long, épais (>= 2 lignes), dans la moitié basse du dessin,
    #    strictement intérieur au cadre
    cand = []
    for y in range(int(0.25 * H), int(0.62 * H)):
        x0, x1 = plus_long(a[y])
        if 0.3 * W < x1 - x0 < 0.6 * W:
            cand.append((y, x0, x1))
    # regroupe les lignes consécutives de mêmes extrémités
    groupes, cur = [], [cand[0]]
    for c in cand[1:]:
        if c[0] == cur[-1][0] + 1 and abs(c[1] - cur[-1][1]) <= 3 and abs(c[2] - cur[-1][2]) <= 3:
            cur.append(c)
        else:
            groupes.append(cur); cur = [c]
    groupes.append(cur)
    barre = max(groupes, key=len)
    yb = int(np.mean([c[0] for c in barre])); xg = float(np.median([c[1] for c in barre])); xd = float(np.median([c[2] for c in barre]))
    # 2) cote 7 : court segment horizontal fléché juste sous la barre (entre la verticale des masses et la verticale du centre)
    c7 = None
    for y in range(yb + 3, yb + 16):
        for (s, e) in runs(a[y]):
            if 0.15 * (xd - xg) < e - s < 0.40 * (xd - xg) and xg + 10 < s and e < xd - 10:
                if c7 is None or e - s > c7[2] - c7[1]:
                    c7 = (y, s, e)
    # 3) ligne des cotes 8 et 9 (contrôle seulement : sur OP4 le trait est interrompu) : segments fusionnés (trous <= 8 px)
    c89 = None
    for y in range(yb + 10, yb + 40):
        r = fusion([t for t in runs(a[y], 140) if t[1] - t[0] >= 5], 8)
        r = [t for t in r if abs((t[1] - t[0]) - (xd - xg)) < 14]
        if r:
            c89 = (y, r[0][0], r[0][1]); break
    x_masses, x_centre = c7[1], c7[2]
    # 4) barre verticale épaisse (cote 6), à droite du sphéroïde : plus long segment vertical sombre au voisinage de xd
    c6 = None
    for x in range(int(xd) - 6, int(xd) + 7):
        col = a[:yb - 5, x]
        s, e = plus_long(col)
        if c6 is None or e - s > c6[2] - c6[1]:
            c6 = (x, s, e)
    # 5) envergures 11, 12, 13 : trois longues lignes fléchées sous la ligne 8-9 (interrompues par le numéro cerclé) ;
    #    segments fusionnés (trous <= 16 px), longueur > 1,2 fois la barre, strictement à l'intérieur du cadre
    env = []
    y_dep = (c89[0] if c89 else yb + 20) + 12
    for y in range(y_dep, min(H, y_dep + 130)):
        r = fusion([t for t in runs(a[y], 140) if t[1] - t[0] >= 5], 16)
        r = [t for t in r if 1.2 * (xd - xg) < t[1] - t[0] < 0.90 * W]
        if r:
            t = max(r, key=lambda u: u[1] - u[0])
            env.append((y, t[0], t[1]))
    env2 = []
    for e in env:
        if env2 and e[0] - env2[-1][0] <= 4:
            if e[2] - e[1] > env2[-1][2] - env2[-1][1]:
                env2[-1] = e
        else:
            env2.append(e)
    L = {"cote 8 (REAR, 8 m)": (x_masses - xg, 8.0), "cote 9 (FORWARD, 11 m)": (xd - x_masses, 11.0),
         "cote 7 (OFFSET, 5 m)": (x_centre - x_masses, 5.0), "cote 6 (VERTICAL, 6 m)": (c6[2] - c6[1], 6.0)}
    ech = {k: v[0] / v[1] for k, v in L.items()}
    e_moy = float(np.mean(list(ech.values()))); e_sd = float(np.std(list(ech.values()), ddof=1))
    res[nom] = {"barre_epaisse": [yb, xg, xd], "cote7": c7, "cote89": c89, "cote6": c6,
                "longueurs_px": {k: v[0] for k, v in L.items()}, "echelle_px_par_m": ech,
                "echelle_moyenne_px_par_m": e_moy, "ecart_type": e_sd, "dispersion_relative": e_sd / e_moy,
                "rapport_dessine_8_sur_9": L["cote 8 (REAR, 8 m)"][0] / L["cote 9 (FORWARD, 11 m)"][0], "rapport_inscrit_8_sur_9": 8 / 11,
                "envergures_px": [e[2] - e[1] for e in env2],
                "envergures_m_a_l_echelle_moyenne": [(e[2] - e[1]) / e_moy for e in env2]}
    print("==", nom)
    for k, v in L.items():
        print(f"   {k:<26} {v[0]:6.1f} px  -> {v[0]/v[1]:5.2f} px/m")
    print(f"   échelle moyenne {e_moy:.2f} ± {e_sd:.2f} px/m (dispersion {100*e_sd/e_moy:.0f} %) ; incertitude de pointé ±1,5 px")
    print(f"   rapport cote 8 / cote 9 : dessiné {res[nom]['rapport_dessine_8_sur_9']:.3f} ; inscrit 8/11 = {8/11:.3f}")
    print("   envergures (détection automatique FRAGILE, traits interrompus : valeurs indicatives) :", ", ".join(f"{(e[2]-e[1]):.0f} px = {(e[2]-e[1])/e_moy:.1f} m" for e in env2))
    if nom.startswith("timetravel"):
        print("   lecture retenue au rapport (copie de 550 px) : cote 11 ≈ 316 px, cote 12 ≈ 399 px (lue sur agrandissement), cote 13 ≈ 445 px"
              f" → {316/e_moy:.0f}, {399/e_moy:.0f} et {445/e_moy:.0f} m")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "journaux", "mesure_doc014.json")
json.dump(res, open(out, "w"), indent=1, default=float)
