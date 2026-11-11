#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — mesure des PROPORTIONS sur les documents sources.

Ce script ne modifie aucun original. Il relit les images de 01_archive/originaux/ (lecture seule),
combine des relevés automatiques (seuillage, profils) et des pointés manuels (coordonnées en pixels
de l'image d'origine, relevés sur des agrandissements quadrillés), puis écrit :

  mesures/mesures_proportions.json   toutes les proportions, avec incertitude de pointé
  mesures/DOC-007_reperes.png        contrôle visuel des pointés sur la vue de dessus
  mesures/DOC-004_coins.png          contrôle visuel des coins + reprojection de la caméra ajustée
  mesures/DOC-005_enveloppe.png      contrôle visuel des arêtes relevées sur l'écorché

Rappel : aucune cote chiffrée ne figure dans les documents ; seules des PROPORTIONS sont mesurables.
L'échelle absolue est la cote L de parametres.json (estimation de l'Équipe A, confiance faible).

Usage : python mesurer_proportions.py
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import least_squares

ICI = Path(__file__).resolve().parent
ARCHIVE = ICI.parents[1] / "01_archive" / "originaux"

DOC = {
    "DOC-003": ARCHIVE / "MT7012__JT3.jpg",
    "DOC-004": ARCHIVE / "MT7013__c204unit_johntitor.jpg",
    "DOC-005": ARCHIVE / "MT7014__johntitor_schematic.jpg",
    "DOC-007": ARCHIVE / "MT7016__timetravel_0_1.jpg",
    "DOC-008": ARCHIVE / "MT7017__c204_unit_instructions.jpeg",
}


def suites(masque, decalage=0, longueur_min=1):
    """Renvoie les intervalles [début, fin] (inclus) où le masque 1D est vrai."""
    res, debut = [], None
    for i, v in enumerate(masque):
        if v and debut is None:
            debut = i
        if not v and debut is not None:
            if i - debut >= longueur_min:
                res.append((debut + decalage, i - 1 + decalage))
            debut = None
    if debut is not None and len(masque) - debut >= longueur_min:
        res.append((debut + decalage, len(masque) - 1 + decalage))
    return res


# ----------------------------------------------------------------------------------------------
# 1. DOC-007 — vue de dessus (seule vue orthographique du corpus) : référence des proportions en plan
# ----------------------------------------------------------------------------------------------
def mesurer_doc007():
    im = np.asarray(Image.open(DOC["DOC-007"]).convert("L")).astype(float)
    sombre = im < 110

    # --- relevés automatiques --------------------------------------------------------------
    lignes = suites(sombre[:, 150:155].mean(axis=1) > 0.6)          # traits horizontaux
    colonnes = suites(sombre[200:260, :].mean(axis=0) > 0.8)        # traits verticaux (corps)
    # contour extérieur : traits épais (>= 2 px)
    x_g = [c for c in colonnes if 40 < c[0] < 60][0]
    x_d = [c for c in colonnes if 400 < c[0] < 410 and c[1] - c[0] >= 1][0]
    xg, xd = float(x_g[0]), float(x_d[1])                           # bords extérieurs
    L_px = xd - xg + 0.5
    # profondeur : bord haut du couvercle, ligne de charnière, bord bas du corps
    y_couv_haut = float([l for l in lignes if 60 < l[0] < 70][0][0])
    y_charniere = float([l for l in lignes if 168 < l[0] < 178][0][0])
    y_corps_bas = float([l for l in lignes if 280 < l[0] < 288][0][1])
    P_corps_px = y_corps_bas - y_charniere
    P_couv_px = (y_charniere - 1.5) - y_couv_haut

    def fx(x):
        return (x - xg) / L_px

    def fy(y):       # fraction de P depuis l'AVANT du corps (bas de l'image)
        return (y_corps_bas - y) / P_corps_px

    def fv(y):       # couvercle : fraction de P depuis la CHARNIÈRE
        return ((y_charniere - 1.5) - y) / P_couv_px

    # logements circulaires : plus longue suite très sombre par ligne
    def cercle(y0, y1):
        larg = []
        for y in range(y0, y1):
            s = suites(im[y, 160:212] < 60, 160, 6)
            if s:
                a, b = max(s, key=lambda t: t[1] - t[0])
                if b - a < 40:
                    larg.append((y, a, b))
        ys = [t[0] for t in larg]
        ymax = max(larg, key=lambda t: t[2] - t[1])
        diam = ymax[2] - ymax[1] + 1
        cx = np.mean([(t[1] + t[2]) / 2 for t in larg if t[2] - t[1] > diam - 4])
        cy = (min(ys) + max(ys)) / 2
        return float(cx), float(cy), float(diam) / 2

    c1 = cercle(183, 218)   # singularité principale (côté charnière)
    c2 = cercle(223, 258)   # singularité de direction (côté avant)

    # bandes obliques : suites sombres le long de deux colonnes -> pente, période, épaisseur
    def bande(x_a, x_b, y0, y1):
        ra = suites(im[y0:y1, x_a - 1:x_a + 2].mean(axis=1) < 100, y0, 4)
        rb = suites(im[y0:y1, x_b - 1:x_b + 2].mean(axis=1) < 100, y0, 4)
        # même raie noire suivie de a à b : la plus proche vers le haut
        decal = np.mean([min((a[0] - b[0] for b in rb if a[0] - b[0] > 0), default=np.nan) for a in ra[1:]])
        pente = decal / (x_b - x_a)
        periode = np.mean(np.diff([a[0] for a in ra]))
        epais = np.mean([a[1] - a[0] + 1 for a in ra[:-1]])
        return float(pente), float(periode), float(epais), ra

    pente1, per1, ep1, raies1 = bande(100, 129, 176, 282)
    pente2, per2, ep2, raies2 = bande(243, 270, 176, 282)
    pente_c, per_c, ep_c, raies_c = bande(100, 129, 66, 172)

    charn = suites(im[168:172, :].mean(axis=0) < 90, 0, 10)
    charn = [c for c in charn if 60 < c[0] < 400]

    # --- pointés manuels (px image d'origine ; incertitude ±1 px soit ±0,3 % de L) -----------
    px = {
        "panneau_interieur_gauche": 56.5, "division_zone_gauche": 77.0,
        "bande1_debut": 97.0, "bande1_fin": 132.0,
        "cadre_logements_debut": 156.5, "cadre_logements_fin": 214.0,
        "bande2_debut": 239.5, "bande2_fin": 274.0,
        "fente_ecran_secours": 286.3, "zone4_fin": 299.0,
        "panneau5_fin": 330.0, "panneau8_debut": 332.0, "panneau8_fin": 363.0,
        "rangement_debut": 364.0, "rangement_fin": 402.0,
        "afficheur5_x0": 303.3, "afficheur5_x1": 326.2,
        "interrupteur5_cx": 314.9, "interrupteur5_r": 6.7,
        "clavier_x0": 334.4, "clavier_x1": 360.0,
        "touches_col_isolee": 337.5, "touches_col1": 344.5, "touches_col2": 350.5,
        "marche_arret_x0": 337.8, "marche_arret_x1": 358.2,
        "plaque7_x0": 303.5, "plaque7_x1": 360.0,
        "telecommande_x0": 65.5, "telecommande_x1": 100.0,
        "connecteur_x0": 72.0, "connecteur_x1": 96.0, "cable_x": 391.5,
    }
    py = {
        "cadre_haut": 182.0, "cadre_bas": 257.5, "cadre_separation": 219.5,
        "afficheur5_y0": 182.2, "afficheur5_y1": 192.2,
        "hachures5a_y0": 235.6, "hachures5a_y1": 248.9, "hachures5b_y0": 264.9, "hachures5b_y1": 275.6,
        "interrupteur5_cy": 257.1,
        "clavier_y0": 178.9, "clavier_y1": 247.1,
        "marche_arret_y0": 255.1, "marche_arret_y1": 273.8,
        "telecommande_y0": 296.0, "telecommande_y1": 332.0, "connecteur_y1": 346.0, "cable_y": 340.0,
    }
    py_couv = {"plaque7_y0": 77.0, "plaque7_y1": 161.0}
    touches_y = {"col1": [181.5, 186.5, 191.5, 196.5, 201.5, 206.5, 211.5, 217.0, 226.0, 231.0, 236.0],
                 "col2": [181.5, 186.5, 191.5, 196.5, 201.5], "col_isolee": [182.0, 196.0]}

    res = {
        "image": DOC["DOC-007"].name, "taille_px": [463, 499],
        "contour": {"x_gauche_px": xg, "x_droit_px": xd, "L_px": L_px,
                    "y_couvercle_haut_px": y_couv_haut, "y_charniere_px": y_charniere,
                    "y_corps_bas_px": y_corps_bas, "P_corps_px": P_corps_px, "P_couvercle_px": P_couv_px},
        "rapport_L_sur_P": {"corps": L_px / P_corps_px, "couvercle": L_px / P_couv_px,
                            "retenu": 2 * L_px / (P_corps_px + P_couv_px),
                            "incertitude": abs(L_px / P_corps_px - L_px / P_couv_px) / 2 + 0.03},
        "fractions_x_de_L": {k: round(fx(v), 4) for k, v in px.items() if not k.endswith("_r")},
        "fractions_y_de_P_depuis_avant": {k: round(fy(v), 4) for k, v in py.items()},
        "couvercle_fraction_de_P_depuis_charniere": {k: round(fv(v), 4) for k, v in py_couv.items()},
        "logements": {
            "principal_centre_fx": round(fx(c1[0]), 4), "principal_centre_fy": round(fy(c1[1]), 4),
            "direction_centre_fx": round(fx(c2[0]), 4), "direction_centre_fy": round(fy(c2[1]), 4),
            "rayon_sur_L": round((c1[2] + c2[2]) / 2 / L_px, 4),
            "entraxe_sur_P": round((c2[1] - c1[1]) / P_corps_px, 4),
            "entraxe_sur_diametre": round((c2[1] - c1[1]) / (c1[2] + c2[2]), 3),
            "detail_px": {"principal": c1, "direction": c2},
        },
        "bandes_obliques": {
            "pente_tan": round(float(np.mean([pente1, pente2, pente_c])), 3),
            "angle_deg": round(float(np.degrees(np.arctan(np.mean([pente1, pente2, pente_c])))), 1),
            "periode_sur_P": round(float(np.mean([per1, per2])) / P_corps_px, 4),
            "epaisseur_noire_sur_P": round(float(np.mean([ep1, ep2])) / P_corps_px, 4),
            "phase_sur_P": round(fy(raies1[-1][1] + pente1 * (100 - px["bande1_debut"])), 4),
            "raies_par_bande": 4,
            "detail": {"corps_bande1_x100": raies1, "corps_bande2_x243": raies2, "couvercle_bande1_x100": raies_c,
                       "pentes": [pente1, pente2, pente_c]},
        },
        "charnieres_fx": [[round(fx(a), 4), round(fx(b + 1), 4)] for a, b in charn],
        "interrupteur5_rayon_sur_L": round(px["interrupteur5_r"] / L_px, 4),
        "touches": {"fy": {k: [round(fy(v), 4) for v in vals] for k, vals in touches_y.items()},
                    "nombre_total": sum(len(v) for v in touches_y.values()),
                    "pas_sur_P": round(5.0 / P_corps_px, 4)},
        "telecommande": {"largeur_sur_L": round((px["telecommande_x1"] - px["telecommande_x0"]) / L_px, 4),
                         "longueur_sur_L": round((py["telecommande_y1"] - py["telecommande_y0"]) / L_px, 4),
                         "connecteur_largeur_sur_L": round((px["connecteur_x1"] - px["connecteur_x0"]) / L_px, 4),
                         "connecteur_longueur_sur_L": round((py["connecteur_y1"] - py["telecommande_y1"]) / L_px, 4)},
        "incertitude_pointe_px": 1.0,
        "incertitude_fraction_x": round(1.0 / L_px, 4),
        "incertitude_fraction_y": round(1.0 / P_corps_px, 4),
    }

    # --- image de contrôle -------------------------------------------------------------------
    ctl = Image.open(DOC["DOC-007"]).convert("RGB").resize((463 * 3, 499 * 3), Image.LANCZOS)
    d = ImageDraw.Draw(ctl)
    for k, v in px.items():
        if k.endswith("_r") or k.endswith("_cx"):
            continue
        d.line([(v * 3, y_charniere * 3), (v * 3, y_corps_bas * 3)], fill=(230, 40, 40), width=1)
    for k, v in py.items():
        if "telecommande" in k or "connecteur" in k or "cable" in k or k.endswith("_cy"):
            continue
        d.line([(xg * 3, v * 3), (xd * 3, v * 3)], fill=(40, 110, 230), width=1)
    for c in (c1, c2):
        d.ellipse([(c[0] - c[2]) * 3, (c[1] - c[2]) * 3, (c[0] + c[2]) * 3, (c[1] + c[2]) * 3], outline=(20, 200, 60), width=2)
    d.rectangle([xg * 3, y_couv_haut * 3, xd * 3, y_corps_bas * 3], outline=(250, 160, 0), width=2)
    ctl.save(ICI / "DOC-007_reperes.png")
    return res


# ----------------------------------------------------------------------------------------------
# 2. DOC-004 — vue 3/4 : hauteur du corps, angle d'ouverture du couvercle (caméra en perspective)
# ----------------------------------------------------------------------------------------------
COINS_004 = {   # pointés manuels, px de l'image d'origine (477x440), incertitude ±3 px (trame grossière)
    "A": (47, 241), "B": (99, 313), "C": (469, 168), "D": (404, 119),      # dessus : arr-g, av-g, av-d, arr-d
    "A1": (57, 316), "B1": (109, 391), "C1": (447, 243),                   # dessous : arr-g, av-g, av-d
    "TL": (7, 103), "TR": (397, 5),                                        # bord libre du couvercle ouvert
}


def _rot(lacet, tangage, roulis):
    cz, sz = np.cos(lacet), np.sin(lacet)
    cx, sx = np.cos(tangage), np.sin(tangage)
    cr, sr = np.cos(roulis), np.sin(roulis)
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Rr = np.array([[cr, -sr, 0], [sr, cr, 0], [0, 0, 1]])
    return Rr @ Rx @ Rz


def _projeter_004(p, centre=(238.5, 220.0)):
    f, lacet, tangage, roulis, tx, ty, tz, rP, rH, phi = p
    L, P, H = 1.0, rP, rH
    monde = {"A": (0, P, H), "B": (0, 0, H), "C": (L, 0, H), "D": (L, P, H),
             "A1": (0, P, 0), "B1": (0, 0, 0), "C1": (L, 0, 0)}
    d = np.array([0, -np.cos(phi), np.sin(phi)]) * P        # couvercle ouvert d'un angle phi autour de la charnière
    monde["TL"] = tuple(np.array([0, P, H]) + d)
    monde["TR"] = tuple(np.array([L, P, H]) + d)
    R = _rot(lacet, tangage, roulis)
    out = {}
    for k, w in monde.items():
        c = R @ np.array(w, float) + np.array([tx, ty, tz])
        out[k] = (centre[0] + f * c[0] / c[2], centre[1] + f * c[1] / c[2])
    return out


def mesurer_doc004():
    cles = list(COINS_004)

    def residus(p):
        m = _projeter_004(p)
        return np.array([m[k][i] - COINS_004[k][i] for k in cles for i in (0, 1)])

    bas = [150, -np.pi, 0, -np.pi, -10, -10, 0.3, 0.1, 0.05, 0.5]
    haut = [20000, np.pi, np.pi, np.pi, 10, 10, 60, 1.0, 1.0, 3.1]
    rng = np.random.default_rng(204)

    def ajuster(n, fixe=None):
        meilleur = None
        b, h = list(bas), list(haut)
        if fixe:
            for i, v in fixe.items():
                b[i], h[i] = v - 1e-4, v + 1e-4
        for _ in range(n):
            p0 = [rng.uniform(300, 3000), rng.uniform(-1.5, 1.5), rng.uniform(0.6, 2.4), rng.uniform(-0.4, 0.4),
                  rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(1, 8), 0.3, 0.25, 1.8]
            if fixe:
                for i, v in fixe.items():
                    p0[i] = v
            try:
                r = least_squares(residus, p0, bounds=(b, h))
            except Exception:
                continue
            if meilleur is None or r.cost < meilleur.cost:
                meilleur = r
        return meilleur

    libre = ajuster(300)
    p = libre.x
    rms = float(np.sqrt(2 * libre.cost / len(libre.fun)))
    impose = ajuster(150, {7: 0.304})               # P/L imposé à la valeur de DOC-007
    q = impose.x
    balayage = []
    for f in (500, 800, 1200, 2000, 5000):          # sensibilité à la focale (inconnue)
        r = ajuster(40, {0: float(f)})
        balayage.append({"focale_px": f, "rms_px": round(float(np.sqrt(2 * r.cost / len(r.fun))), 2),
                         "L_sur_P": round(1 / r.x[7], 2), "H_corps_sur_L": round(r.x[8], 3),
                         "H_corps_sur_P": round(r.x[8] / r.x[7], 3), "angle_couvercle_deg": round(float(np.degrees(r.x[9])), 1)})

    # méthode indépendante : axonométrie (perspective faible), arêtes moyennes
    c = {k: np.array(v, float) for k, v in COINS_004.items()}
    ex = np.mean([c["C"] - c["B"], c["C1"] - c["B1"], c["D"] - c["A"]], axis=0)
    ey = np.mean([c["B"] - c["A"], c["B1"] - c["A1"], c["C"] - c["D"]], axis=0)
    ez = np.mean([c["A1"] - c["A"], c["B1"] - c["B"], c["C1"] - c["C"]], axis=0)
    M = np.array([[ex[0] ** 2, ey[0] ** 2, ez[0] ** 2],
                  [ex[1] ** 2, ey[1] ** 2, ez[1] ** 2],
                  [ex[0] * ex[1], ey[0] * ey[1], ez[0] * ez[1]]])
    a, b, cc = np.linalg.solve(M, np.array([1.0, 1.0, 0.0]))
    Lp, Pp, Hp = 1 / np.sqrt(a), 1 / np.sqrt(b), 1 / np.sqrt(cc)

    h_vals = [x["H_corps_sur_L"] for x in balayage] + [float(p[8]), float(q[8]), float(Hp / Lp)]
    res = {
        "image": DOC["DOC-004"].name, "taille_px": [477, 440], "coins_px": COINS_004,
        "incertitude_pointe_px": 3.0,
        "camera_perspective_libre": {
            "rms_px": round(rms, 2), "focale_px": round(float(p[0])),
            "lacet_deg": round(float(np.degrees(p[1])), 1), "tangage_deg": round(float(np.degrees(p[2])), 1),
            "roulis_deg": round(float(np.degrees(p[3])), 1), "translation": [round(float(v), 3) for v in p[4:7]],
            "L_sur_P": round(float(1 / p[7]), 2), "H_corps_sur_L": round(float(p[8]), 3),
            "H_corps_sur_P": round(float(p[8] / p[7]), 3), "angle_couvercle_deg": round(float(np.degrees(p[9])), 1)},
        "camera_perspective_P_sur_L_impose_0.304": {
            "rms_px": round(float(np.sqrt(2 * impose.cost / len(impose.fun))), 2), "focale_px": round(float(q[0])),
            "H_corps_sur_L": round(float(q[8]), 3), "H_corps_sur_P": round(float(q[8] / q[7]), 3),
            "angle_couvercle_deg": round(float(np.degrees(q[9])), 1)},
        "sensibilite_focale": balayage,
        "axonometrie_perspective_faible": {"L_sur_P": round(float(Lp / Pp), 2), "H_corps_sur_L": round(float(Hp / Lp), 3),
                                           "H_corps_sur_P": round(float(Hp / Pp), 3)},
        "synthese": {
            "H_corps_sur_L": round(float(np.mean(h_vals)), 3),
            "H_corps_sur_L_incertitude": round(float((max(h_vals) - min(h_vals)) / 2 + 0.01), 3),
            "L_sur_P_plage": [3.3, 3.75],
            "angle_couvercle_deg": round(float(np.mean([x["angle_couvercle_deg"] for x in balayage] + [np.degrees(q[9])])), 0),
            "angle_couvercle_plage_deg": [101, 112],
            "epaisseur_couvercle_sur_P": 0.125, "epaisseur_couvercle_sur_P_incertitude": 0.05,
            "note_epaisseur": "rebord intérieur du couvercle visible sur 10 à 15 px en bout droit (P ≈ 80 px à cet endroit) : pointé grossier",
        },
    }

    ctl = Image.open(DOC["DOC-004"]).convert("RGB").resize((477 * 3, 440 * 3), Image.LANCZOS)
    d = ImageDraw.Draw(ctl)
    m = _projeter_004(p)
    for a_, b_ in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("A", "A1"), ("B", "B1"), ("C", "C1"),
                   ("A1", "B1"), ("B1", "C1"), ("A", "TL"), ("D", "TR"), ("TL", "TR")]:
        d.line([m[a_][0] * 3, m[a_][1] * 3, m[b_][0] * 3, m[b_][1] * 3], fill=(40, 200, 80), width=2)
    for k, (x, y) in COINS_004.items():
        d.ellipse([x * 3 - 5, y * 3 - 5, x * 3 + 5, y * 3 + 5], outline=(240, 40, 40), width=2)
        d.text((x * 3 + 7, y * 3 - 7), k, fill=(240, 40, 40))
    ctl.save(ICI / "DOC-004_coins.png")
    return res


# ----------------------------------------------------------------------------------------------
# 3. DOC-008 — tailles RELATIVES des 12 composants (schéma de principe, échelle non garantie)
# ----------------------------------------------------------------------------------------------
def mesurer_doc008():
    D = 65.0   # diamètre extérieur de l'anneau noir (enveloppe de refroidissement) en px — référence
    boites_px = {   # (x0, y0, x1, y1) px image d'origine 415x580, pointé ±1,5 px
        "carter_gauche_anneau": (98.5, 207.5, 163.5, 272.5), "carter_droit_anneau": (203.5, 207.5, 268.5, 272.5),
        "bobines_gauche_etendue": (97, 222, 170, 258), "regulateur_electrons_5": (178, 262, 205, 296),
        "regulateur_champ_3_gauche": (131, 314, 174, 338), "regulateur_champ_3_droit": (210, 314, 252, 338),
        "generateur_electrons_6": (330, 271, 393, 385), "bande_noire_generateur": (330, 318, 393, 338),
        "pompe_9": (166, 163, 217, 183), "reservoir_10_gauche": (300, 96, 342, 225), "reservoir_10_droit": (343, 96, 387, 225),
        "capteurs_gravite_11_ensemble": (138, 73, 258, 137), "capteurs_gravite_11_capsule": (142, 82, 155, 122),
        "capteurs_gravite_11_module_tambours": (170, 75, 241, 120), "batterie_12": (224, 416, 312, 445),
        "amplificateur_capteur_7": (157, 204, 169, 216), "raccord_superieur": (128, 206, 138, 214),
    }
    rel = {k: {"largeur_sur_D": round((b[2] - b[0]) / D, 3), "hauteur_sur_D": round((b[3] - b[1]) / D, 3),
               "centre_px": [round((b[0] + b[2]) / 2, 1), round((b[1] + b[3]) / 2, 1)]} for k, b in boites_px.items()}
    return {
        "image": DOC["DOC-008"].name, "taille_px": [415, 580], "reference_D_px": D,
        "boites_px": boites_px, "tailles_relatives": rel,
        "entraxe_carters_sur_D": round((236.0 - 131.0) / D, 3),
        "rayon_carter_interieur_sur_R": 0.68,
        "bobines_positions_axiales_sur_R": [0.28, 0.52, 0.77],
        "calottes_position_axiale_sur_R": 1.12,
        "positions_sous_le_centre_sur_D": {"regulateur_electrons_5": round((279 - 240) / D, 3),
                                           "collecteur_4": round((285 - 240) / D, 3),
                                           "regulateurs_champ_3": round((326 - 240) / D, 3)},
        "etendue_noyau_px": {"horizontal": 197, "vertical": 140},
        "etendue_schema_px": {"horizontal": 340, "vertical": 372},
        "incertitude_pointe_px": 1.5,
        "avertissement": "DOC-008 est un schéma de principe : les tailles relatives ne sont pas garanties à l'échelle.",
    }


# ----------------------------------------------------------------------------------------------
# 4. DOC-005 — écorché : proportions de l'enveloppe (projection oblique, échelle de profondeur inconnue)
# ----------------------------------------------------------------------------------------------
def mesurer_doc005():
    aretes = {   # px image d'origine 1023x782, pointé ±4 px
        "dessus_arriere": [(65, 293), (828, 263)], "dessous_avant": [(130, 635), (870, 573)],
        "extremite_droite_dessus": [(828, 263), (975, 392)], "cloison_gauche_dessus": [(150, 300), (250, 445)],
        "hauteur_avant_droite": [(735, 418), (735, 583)], "hauteur_cloison_gauche": [(250, 445), (215, 628)],
        "biseau_droit": [(975, 392), (905, 572)],
    }
    v = {k: np.array(b, float) - np.array(a, float) for k, (a, b) in aretes.items()}
    Lpx = float(np.mean([np.linalg.norm(v["dessus_arriere"]), np.linalg.norm(v["dessous_avant"])]))
    Ltop = float(np.linalg.norm(v["dessus_arriere"]))
    Ppx = float(np.mean([np.linalg.norm(v["extremite_droite_dessus"]), np.linalg.norm(v["cloison_gauche_dessus"])]))
    Hpx = float(np.mean([np.linalg.norm(v["hauteur_avant_droite"]), np.linalg.norm(v["hauteur_cloison_gauche"])]))
    res = {
        "image": DOC["DOC-005"].name, "taille_px": [1023, 782], "aretes_px": aretes,
        "L_px": round(Ltop, 1), "P_projete_px": round(Ppx, 1), "H_px": round(Hpx, 1),
        "H_sur_L": round(Hpx / Ltop, 3),
        "P_sur_L_si_cavaliere_k1": round(Ppx / Ltop, 3), "P_sur_L_si_cabinet_k0.5": round(Ppx / 0.5 / Ltop, 3),
        "P_sur_L_retenu": round(float(np.sqrt((Ppx / Ltop) * (Ppx / 0.5 / Ltop))), 3),
        "P_sur_L_incertitude": round(float((Ppx / 0.5 / Ltop - Ppx / Ltop) / 2), 3),
        "biseau_droit_recul_sur_L": round(abs(v["biseau_droit"][0]) / Ltop, 3),
        "biseau_droit_hauteur_sur_H": round(abs(v["biseau_droit"][1]) / Hpx, 3),
        "raccourcissement_dessous_sur_L": round((Ltop - float(np.linalg.norm(v["dessous_avant"]))) / Ltop, 3),
        "note": "Le dessin est une perspective à main levée proche d'une projection oblique (axe long quasi horizontal, "
                "verticales vraies, fuyantes à ≈ 45°) : le rapport de réduction des fuyantes est inconnu (0,5 à 1), "
                "d'où une large plage pour P/L.",
        "incertitude_pointe_px": 4.0,
    }
    ctl = Image.open(DOC["DOC-005"]).convert("RGB")
    d = ImageDraw.Draw(ctl)
    for k, (a, b) in aretes.items():
        d.line([a, b], fill=(230, 40, 40), width=3)
    ctl.save(ICI / "DOC-005_enveloppe.png")
    return res


# ----------------------------------------------------------------------------------------------
# 5. Photographies — position des bandes et étiquettes à l'intérieur du couvercle (DOC-003, pointé x4)
# ----------------------------------------------------------------------------------------------
def mesurer_photos():
    x4 = {"couvercle_gauche": 735, "couvercle_droit": 1800, "bande1": (850, 925), "bande2": (1210, 1290),
          "etiquette_centrale": (1010, 1140), "plaque_instructions": (1455, 1620), "etiquette_jaune": (750, 830)}
    Lp = x4["couvercle_droit"] - x4["couvercle_gauche"]
    f = lambda x: round((x - x4["couvercle_gauche"]) / Lp, 3)
    y4 = {"couvercle_haut": 150, "couvercle_bas": 440, "etiquette_blanche": (250, 325), "etiquette_orange": (335, 375),
          "etiquette_jaune": (195, 245), "boitier_gris": (250, 320)}
    Hp = y4["couvercle_bas"] - y4["couvercle_haut"]
    g = lambda y: round((y4["couvercle_bas"] - y) / Hp, 3)
    return {
        "image": DOC["DOC-003"].name, "agrandissement": 4, "pointes_x4_px": x4, "pointes_y_x4_px": y4,
        "fractions_x_de_L": {"bande1": [f(x4["bande1"][0]), f(x4["bande1"][1])], "bande2": [f(x4["bande2"][0]), f(x4["bande2"][1])],
                             "etiquette_centrale": [f(x4["etiquette_centrale"][0]), f(x4["etiquette_centrale"][1])],
                             "plaque_instructions": [f(x4["plaque_instructions"][0]), f(x4["plaque_instructions"][1])],
                             "etiquette_jaune": [f(x4["etiquette_jaune"][0]), f(x4["etiquette_jaune"][1])]},
        "fractions_v_depuis_charniere": {k: [g(v[1]), g(v[0])] for k, v in y4.items() if isinstance(v, tuple)},
        "L_sur_hauteur_couvercle_apparente": round(Lp / Hp, 2),
        "raies_noires_par_bande": "2 à 3 (contre 4 sur DOC-007)",
        "incertitude": "±0,02 en fraction (photo floue, bord droit du couvercle incertain, légère perspective)",
    }


def main():
    mesures = {
        "avertissement": "Proportions mesurées sur des copies de basse résolution de documents NON authentifiés. "
                         "Aucune cote absolue n'est documentée.",
        "DOC-007": mesurer_doc007(),
        "DOC-004": mesurer_doc004(),
        "DOC-008": mesurer_doc008(),
        "DOC-005": mesurer_doc005(),
        "photos_DOC-003": mesurer_photos(),
    }
    (ICI / "mesures_proportions.json").write_text(json.dumps(mesures, ensure_ascii=False, indent=1), encoding="utf-8")
    d7, d4, d5 = mesures["DOC-007"], mesures["DOC-004"], mesures["DOC-005"]
    print("DOC-007 : L/P = %.2f (corps %.2f, couvercle %.2f)" % (d7["rapport_L_sur_P"]["retenu"], d7["rapport_L_sur_P"]["corps"], d7["rapport_L_sur_P"]["couvercle"]))
    print("DOC-007 : logements", d7["logements"])
    print("DOC-007 : bandes", {k: v for k, v in d7["bandes_obliques"].items() if k != "detail"})
    print("DOC-007 : charnières", d7["charnieres_fx"])
    print("DOC-004 :", json.dumps(d4["camera_perspective_libre"], ensure_ascii=False))
    print("DOC-004 : synthèse", json.dumps(d4["synthese"], ensure_ascii=False))
    print("DOC-005 : H/L = %.3f ; P/L ∈ [%.2f ; %.2f]" % (d5["H_sur_L"], d5["P_sur_L_si_cavaliere_k1"], d5["P_sur_L_si_cabinet_k0.5"]))
    print("photos  :", mesures["photos_DOC-003"]["fractions_x_de_L"])


if __name__ == "__main__":
    main()
