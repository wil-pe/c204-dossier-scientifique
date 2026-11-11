# -*- coding: utf-8 -*-
"""S08 — Reconstitution quantitative de C204-DOC-009 (« SECTION I — C204 TIPLER SINUSOID FIELD »).

On numérise approximativement les ellipses, anneaux et courbes du schéma, puis on regarde si une
famille de surfaces physiques (horizons et ergosurfaces de Kerr, équipotentielles de deux masses,
profils de gorge de trou de ver, sinusoïde) lui ressemble mieux qu'une construction graphique
générique (ellipses). C'est une DESCRIPTION géométrique du dessin, sans valeur de preuve physique.

Trois copies sont analysées avec le même code, dans le repère de la copie de référence :
  • « reference » : C204-DOC-009, copie marinertalk de 318×369 px (01_archive/originaux/) ;
  • « pt3 »       : C204-DOC-009, meilleure copie connue, PT3.jpg, 578×799 px ;
  • « doc014 »    : C204-DOC-014, variante du même tracé portant quatre distances EN MÈTRES
                    (première trace : août 2003, site tiers ; attribution à l'auteur non établie).
DOC-009 ne porte aucune cote ; DOC-014 en porte quatre (6, 5, 8 et 11 m). Les deux états portent
la mention « This area is not to scale » au-dessus du sphéroïde central.

ANALYSE D'IMAGE ILLUSTRATIVE : copies secondaires, incertitude de numérisation de 0,5 à 2,5 px.
Une ressemblance de forme ne prouverait de toute façon rien sur la physique ; ce n'est pas une
preuve expérimentale. Les fichiers de 01_archive/ sont ouverts en LECTURE SEULE.

Exécution :  .venv/bin/python 05_simulations/S08_reconstitution_doc009/s08_reconstitution_doc009.py
(l'exécution sans argument traite la copie de référence, puis relance le script sur les deux
autres copies avec l'option --copie et compare les résultats).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.optimize import minimize, least_squares, brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore")
FIG, RES = cc.dossiers(__file__)
col = cc.COULEURS
RNG = np.random.default_rng(204)
RACINE = Path(__file__).resolve().parents[2]
ALT = RACINE / "01_archive" / "copies_alternatives"
COPIES = {
    "reference": {"fichier": RACINE / "01_archive" / "originaux" / "MT7018__singularities1.jpg",
                  "designation": "C204-DOC-009, copie de référence (marinertalk, 318×369 px)", "initial": None},
    "pt3": {"fichier": ALT / "anomalies.net" / "20030830123900__PT3.jpg",
            "designation": "C204-DOC-009, meilleure copie (PT3.jpg, 578×799 px)",
            "initial": [1.616, 1.616, 0.0, 49.8, 113.9]},            # (sx, sy, rotation [rad], tx, ty) : estimation de départ du recalage
    "doc014": {"fichier": ALT / "bibliotecapleyades.net" / "LIVE__timetravel16_07.jpg",
               "designation": "C204-DOC-014, variante cotée en mètres (timetravel16_07.jpg, 550×594 px)",
               "initial": [1.610, 1.610, 0.017, 6.1, -72.6]},
}
_args = argparse.ArgumentParser(description="S08 — reconstitution de DOC-009")
_args.add_argument("--copie", choices=list(COPIES), default="reference")
COPIE = _args.parse_args().copie
SUFFIXE = "" if COPIE == "reference" else f"_{COPIE}"
DESIGNATION = COPIES[COPIE]["designation"]
val = cc.Validation("S08_reconstitution_doc009" + SUFFIXE)

# ---------------------------------------------------------------------------
# 1. Images, recalage et carte de « noirceur »
# ---------------------------------------------------------------------------
# REPÈRE DE TRAVAIL : pixels de la copie de référence (x = colonne, y = ligne), pour TOUTES les copies.
# Les autres copies sont recalées sur la référence (similitude à deux échelles : sx, sy, rotation,
# translation) par maximisation de la corrélation des noirceurs dans la zone du schéma ; la noirceur
# est ensuite lue dans la copie à sa résolution native (≈ 1,6 fois plus fine que la référence).
img_ref = np.asarray(Image.open(COPIES["reference"]["fichier"]).convert("L"), dtype=float)   # (369 lignes, 318 colonnes)
H_IMG, W_IMG = img_ref.shape
TRANSFO = None                                   # None = identité (copie de référence)
RECALAGE = {"copie": COPIE, "fichier": str(COPIES[COPIE]["fichier"].relative_to(RACINE))}


def vers_copie(xs, ys, T=None):
    """Repère de référence → pixels natifs de la copie analysée."""
    T = TRANSFO if T is None else T
    sx, sy, th, tx, ty = T
    c_, s_ = np.cos(th), np.sin(th)
    return sx * (c_ * xs - s_ * ys) + tx, sy * (s_ * xs + c_ * ys) + ty


if COPIE == "reference":
    img = img_ref
    NOIR = gaussian_filter(1.0 - img_ref / 255.0, 0.7)             # 0 = blanc, 1 = noir ; léger lissage
else:
    natif = np.asarray(Image.open(COPIES[COPIE]["fichier"]).convert("L"), dtype=float)
    _ref_l = gaussian_filter(1.0 - img_ref / 255.0, 1.0)
    _nat_l = gaussian_filter(1.0 - natif / 255.0, 1.6)             # même flou apparent que la référence, pour le recalage seulement
    _gy, _gx = np.mgrid[58:246:1.0, 14:316:1.0]                    # zone du schéma (hors cadre, hors légende)
    _R = _ref_l[58:246, 14:316]

    def _correlation(T):
        X, Y = vers_copie(_gx, _gy, T)
        V = map_coordinates(_nat_l, [Y, X], order=1, mode="constant", cval=0.0)
        a_, b_ = _R - _R.mean(), V - V.mean()
        return float((a_ * b_).sum() / np.sqrt((a_ * a_).sum() * (b_ * b_).sum() + 1e-30))

    _p0 = list(COPIES[COPIE]["initial"])
    _best = max(((_correlation(_p0[:3] + [_p0[3] + dx, _p0[4] + dy]), dx, dy) for dx in np.arange(-12, 12.1, 3) for dy in np.arange(-12, 12.1, 3)))
    _p1 = _p0[:3] + [_p0[3] + _best[1], _p0[4] + _best[2]]
    _r = minimize(lambda T: -_correlation(T), _p1, method="Nelder-Mead",
                  options={"xatol": 1e-5, "fatol": 1e-9, "maxiter": 6000,
                           "initial_simplex": np.array([_p1] + [np.array(_p1) + d_ for d_ in np.diag([0.02, 0.02, 0.005, 2.0, 2.0])])})
    TRANSFO = tuple(float(v) for v in _r.x)
    RECALAGE.update({"echelle_x": TRANSFO[0], "echelle_y": TRANSFO[1], "rotation_deg": float(np.degrees(TRANSFO[2])),
                     "translation_px": [TRANSFO[3], TRANSFO[4]], "correlation": float(-_r.fun), "pixels_natifs": [int(natif.shape[1]), int(natif.shape[0])]})
    print(f"S08 [{COPIE}] — recalage sur la référence : échelles {TRANSFO[0]:.4f} × {TRANSFO[1]:.4f}, rotation {np.degrees(TRANSFO[2]):+.2f}°, corrélation {-_r.fun:.4f}")
    NOIR = gaussian_filter(1.0 - natif / 255.0, 0.7)               # lissage de 0,7 px NATIF
    _ay, _ax = np.mgrid[0:H_IMG:1 / 3, 0:W_IMG:1 / 3]               # image d'affichage : copie ramenée dans le repère de référence (×3)
    img = map_coordinates(natif, list(vers_copie(_ax, _ay))[::-1], order=1, mode="constant", cval=255.0)


def noirceur(xs, ys):
    """Noirceur interpolée (bilinéaire) aux points (x, y) du repère de référence.

    Le cadre épais du schéma (bord haut y < 55, bord gauche x < 12) attire tout ajustement fondé sur
    la noirceur : il est neutralisé (constaté lors d'une première exécution, voir README)."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    X, Y = (xs, ys) if TRANSFO is None else vers_copie(xs, ys)
    v = map_coordinates(NOIR, [Y, X], order=1, mode="constant", cval=0.0)
    return np.where((ys < 55.0) | (xs < 12.0), 0.0, v)


def score_courbe(xs, ys, fraction_min=0.55):
    """Noirceur moyenne le long d'une courbe (points hors image ignorés)."""
    dedans = (xs >= 1) & (xs <= W_IMG - 2) & (ys >= 1) & (ys <= H_IMG - 2)
    if dedans.mean() < fraction_min:
        return 0.0
    return float(np.mean(noirceur(xs[dedans], ys[dedans])))


# ---------------------------------------------------------------------------
# 2. Axe horizontal en tirets : position et inclinaison de la numérisation
# ---------------------------------------------------------------------------
xs_axe, ys_axe = [], []
yy = np.arange(144.0, 155.01, 0.25)
for x in np.arange(24, 316, 1.0):
    prof = noirceur(np.full_like(yy, x), yy)
    if prof.max() > 0.35:                       # on ne garde que les colonnes où un tiret est présent
        w = np.clip(prof - 0.5 * prof.max(), 0, None)
        xs_axe.append(x)
        ys_axe.append(np.sum(w * yy) / np.sum(w))
xs_axe, ys_axe = np.array(xs_axe), np.array(ys_axe)
for _ in range(3):                              # ajustement linéaire robuste (rejet à 2,5 σ)
    pa = np.polyfit(xs_axe, ys_axe, 1)
    res = ys_axe - np.polyval(pa, xs_axe)
    garde = np.abs(res) < 2.5 * np.std(res)
    xs_axe, ys_axe = xs_axe[garde], ys_axe[garde]
PENTE_AXE, ORD_AXE = pa
INCLINAISON = float(np.arctan(PENTE_AXE))       # rad (≈ −0,7° : numérisation légèrement de travers)


def y_axe(x):
    return PENTE_AXE * np.asarray(x, float) + ORD_AXE


# ---------------------------------------------------------------------------
# 3. Ajustement d'ellipses par maximisation de la noirceur le long du contour
# ---------------------------------------------------------------------------
T_PARAM = np.linspace(0, 2 * np.pi, 361)[:-1]


def ellipse_xy(p, t=T_PARAM, incl=None):
    cx, cy, a, b = p
    incl = INCLINAISON if incl is None else incl
    ct, st = np.cos(incl), np.sin(incl)
    u, v = a * np.cos(t), b * np.sin(t)
    return cx + u * ct - v * st, cy + u * st + v * ct


def ajuster(courbe, p0, sigma_depart=1.0, n_departs=24, rayon_confiance=4.0, echelle=None, rng=None):
    """Maximise le score de noirceur d'une famille de courbes paramétrées, départs multiples.

    Un terme de rappel quadratique empêche de s'éloigner de plus de `rayon_confiance` (pixels ou
    unités d'`echelle`) de l'estimation initiale lue à l'œil : on affine une lecture, on ne cherche
    pas un autre trait. Retourne (paramètres médians des meilleurs départs, écart-type, score)."""
    p0 = np.asarray(p0, float)
    echelle = np.ones_like(p0) if echelle is None else np.asarray(echelle, float)

    def cout(p):
        ecart = np.abs(p - p0) / echelle
        return -score_courbe(*courbe(p)) + 0.02 * np.sum(np.clip(ecart - rayon_confiance, 0, None)**2)

    sols, scores = [], []
    for k in range(n_departs):
        depart = p0 + (0 if k == 0 else 1) * (RNG if rng is None else rng).normal(0, sigma_depart, p0.size) * echelle
        r = minimize(cout, depart, method="Nelder-Mead", options={"xatol": 0.02, "fatol": 1e-5, "maxiter": 800})
        sols.append(r.x)
        scores.append(-r.fun)
    sols, scores = np.array(sols), np.array(scores)
    bons = scores >= np.quantile(scores, 0.5)
    meilleur = sols[np.argmax(scores)]
    return meilleur, sols[bons].std(axis=0), float(scores.max())


# Estimations initiales lues sur l'image agrandie (pixels de l'original ; cx, cy, demi-axe horizontal, demi-axe vertical)
INITIAL = {
    "anneau G2 (« negative », gauche)": (71.5, 152.0, 8.0, 68.0),
    "anneau G3 (« null », gauche)": (48.0, 152.0, 7.0, 52.0),
    "anneau G4 (« positive », gauche)": (33.5, 151.5, 6.0, 34.5),
    "anneau D2 (« negative », droite)": (268.0, 149.0, 7.0, 71.0),
    "anneau D3 (« null », droite)": (296.0, 148.5, 6.0, 48.5),
    "anneau D4 (« positive », droite)": (310.0, 146.5, 5.0, 25.5),
    "sphéroïde central (enveloppe)": (144.5, 145.3, 50.0, 30.8),
    # Les meilleures copies (PT3.jpg, DOC-014) montrent que le « grand contour pâle » est fait de DEUX ellipses de même hauteur :
    # E1, enveloppe des six anneaux, et E2, décalée vers la droite. Sur la copie de 318 px elles se confondaient ; la première
    # version de S08 les ajustait comme une seule (171,5 ; 150,5 ; 148,5 ; 93,0), ce qui était une erreur de lecture (phase 7).
    "grande ellipse extérieure": (169.5, 150.2, 146.0, 93.5),                      # = E1, enveloppe des anneaux
    "second grand contour E2 (décalé vers la droite)": (192.0, 150.3, 137.0, 93.0),
}
RAYON_CONFIANCE = {"grande ellipse extérieure": 2.5, "second grand contour E2 (décalé vers la droite)": 2.5}   # traits pâles : on reste près de la lecture
print(f"S08 — numérisation des ellipses — {DESIGNATION}")
ellipses = {}
for nom, p0 in INITIAL.items():
    p, sig, sc = ajuster(ellipse_xy, p0, rayon_confiance=RAYON_CONFIANCE.get(nom, 4.0))
    ellipses[nom] = {"cx": p[0], "cy": p[1], "a": p[2], "b": p[3], "incertitude_px": sig.tolist(), "score": sc,
                     "initial": list(p0), "ecart_a_la_lecture_px": float(np.max(np.abs(p - np.array(p0))))}
    print(f"  {nom:36s} cx={p[0]:6.1f} cy={p[1]:6.1f} a={p[2]:6.1f} b={p[3]:6.1f}  score={sc:.3f}  (±{sig.max():.2f} px)")
_fy, _fx = np.mgrid[60:245:1.0, 20:316:1.0]
FOND = float(np.mean(noirceur(_fx, _fy)))          # noirceur moyenne de la zone du schéma (niveau de référence)

# Les deux « singularités » : losanges noirs sur l'axe
xx = np.arange(120.0, 156.0, 0.1)
prof = np.array([np.mean(noirceur(np.full(13, x), y_axe(x) + np.linspace(-3, 3, 13))) for x in xx])
pics = [i for i in range(1, len(xx) - 1) if prof[i] > prof[i - 1] and prof[i] >= prof[i + 1] and prof[i] > 0.75 * prof.max()]
pics = sorted(pics, key=lambda i: -prof[i])
x_sing = []
for i in pics:                                   # deux maxima distants d'au moins 5 px
    if all(abs(xx[i] - x) > 5 for x in x_sing):
        x_sing.append(float(xx[i]))
    if len(x_sing) == 2:
        break
x_sing = sorted(x_sing)
SEP_SING = x_sing[1] - x_sing[0]
X_MASSES = 0.5 * (x_sing[0] + x_sing[1])

# ---------------------------------------------------------------------------
# 4. Test de validation de la méthode (image de synthèse à vérité connue) et contrôles
# ---------------------------------------------------------------------------
# Correction n° 39 (Red Team, phase 7). Seuls entrent dans le décompte de validation les tests qui
# confrontent le code à une réponse connue indépendamment (image ou points de synthèse, limites
# analytiques). Les contrôles de l'ajustement sur lui-même (contraste du trait, écart à la lecture à
# l'œil — que le terme de rappel de `ajuster` borne par construction —, comparaison à une lecture
# manuelle) et les énoncés de résultat sont CONSIGNÉS HORS DÉCOMPTE (`val.consigner`).
print("S08 — test de validation de la méthode et contrôles")
Ys, Xs = np.mgrid[0:H_IMG, 0:W_IMG]
verite = (160.0, 150.0, 60.0, 35.0)
dist = np.abs(np.hypot((Xs - verite[0]) / verite[2], (Ys - verite[1]) / verite[3]) - 1) * min(verite[2:])
synth = np.exp(-0.5 * (dist / 1.0)**2) + 0.05 * RNG.random((H_IMG, W_IMG))
NOIR_REEL, TRANSFO_REELLE = NOIR, TRANSFO
NOIR, TRANSFO = gaussian_filter(synth, 0.7), None
p_syn, _, _ = ajuster(lambda p: ellipse_xy(p, incl=0.0), np.array(verite) + np.array([2.5, -2.0, 3.0, -2.5]))
NOIR, TRANSFO = NOIR_REEL, TRANSFO_REELLE
val.verifier("Méthode : ellipse de synthèse retrouvée (erreur max. sur cx, cy, a, b) [px]", np.max(np.abs(p_syn - np.array(verite))), 0.0, tol_abs=0.3)
val.verifier("Inclinaison de l'axe en tirets (numérisation) ≈ −0,7° (lecture à l'œil : −0,6° à −0,8°)", np.degrees(INCLINAISON), -0.7, tol_abs=0.25)
val.verifier_vrai("Deux singularités détectées sur l'axe (« deux points noirs rapprochés », transcription de l'Équipe A)", len(x_sing) == 2, f"x = {[round(v, 1) for v in x_sing]}")
for nom, e in ellipses.items():
    e["contraste_sur_fond"] = e["score"] / FOND
    if "grand" not in nom:               # les deux grands contours sont des traits pâles : contraste simplement rapporté
        val.consigner("contrôle", f"Contraste du trait ajusté / fond ({nom})", e["score"] / FOND, commentaire="attendu > 2", constat=e["score"] / FOND > 2.0)
    val.consigner("contrôle", f"Écart de l'ajustement à la lecture à l'œil [px] ({nom})", e["ecart_a_la_lecture_px"],
                  commentaire="borné par le terme de rappel de l'optimiseur : ne peut guère dépasser 4 px", constat=e["ecart_a_la_lecture_px"] < 4.0)

# ---------------------------------------------------------------------------
# 5. Familles physiques candidates pour les deux courbes fermées
# ---------------------------------------------------------------------------
# MÉTHODE. Une première version comparait les familles par leur « score de noirceur » maximal ;
# elle a ÉCHOUÉ comme discriminant (une courbe souple va se loger sur d'autres traits sombres :
# méridiens internes, cadre) et a été abandonnée. On compare désormais des RÉSIDUS GÉOMÉTRIQUES :
#   1) on extrait des points du contour dessiné (indépendamment de toute famille) ;
#   2) on ajuste chaque famille à ces points par moindres carrés robustes (distance au plus proche
#      point de la courbe) ; 3) on compare les résidus à l'incertitude de numérisation (~1 px).
T_FIN = np.linspace(0, 2 * np.pi, 3601)[:-1]


def _placer(u, v, cx, cy):
    ct, st = np.cos(INCLINAISON), np.sin(INCLINAISON)
    return cx + u * ct - v * st, cy + u * st + v * ct


def fam_ellipse(p, t=T_FIN):
    return _placer(p[2] * np.cos(t), p[3] * np.sin(t), p[0], p[1])


def fam_superellipse(p, t=T_FIN):
    """|x/a|^n + |y/b|^n = 1 : témoin de « carrure » (n = 2 : ellipse)."""
    n = max(p[4], 1.0)
    c, s_ = np.cos(t), np.sin(t)
    return _placer(p[2] * np.sign(c) * np.abs(c)**(2 / n), p[3] * np.sign(s_) * np.abs(s_)**(2 / n), p[0], p[1])


def fam_ergosurface(p, t=T_FIN, axe_vertical=True):
    """Coupe méridienne de l'ergosurface externe de Kerr (coordonnées de Kerr-Schild) :
    ρ = sqrt(r_E² + a²) sinθ, z = r_E cosθ, r_E = 1 + sqrt(1 − a² cos²θ). p = (cx, cy, échelle, a/M)."""
    a = np.clip(p[3], 0.0, 1.0)
    rE = 1 + np.sqrt(1 - a**2 * np.cos(t)**2)
    rho, z = np.sqrt(rE**2 + a**2) * np.sin(t), rE * np.cos(t)
    u, v = (rho, -z) if axe_vertical else (z, rho)
    return _placer(p[2] * u, p[2] * v, p[0], p[1])


def fam_ergosurface_h(p, t=T_FIN):
    return fam_ergosurface(p, t, axe_vertical=False)


def fam_horizon(p, t=T_FIN):
    """Horizon externe de Kerr (Kerr-Schild) : ellipse aplatie de rapport sqrt(2/r+) ≤ √2, axe vertical."""
    a = np.clip(p[3], 0.0, 1.0)
    rp = 1 + np.sqrt(1 - a**2)
    return _placer(p[2] * np.sqrt(rp**2 + a**2) * np.sin(t), -p[2] * rp * np.cos(t), p[0], p[1])


def fam_equipotentielle(p, t=T_FIN):
    """Équipotentielle newtonienne de deux masses égales en (cx ± h, cy) : 1/r1 + 1/r2 = C.
    p = (cx, cy, h, b), b = demi-axe transverse (C = 2/sqrt(b² + h²))."""
    h, b = abs(p[2]) + 1e-9, abs(p[3])
    Cc = 2 / np.hypot(b, h)
    a_ = (1 + np.sqrt(1 + Cc**2 * h**2)) / Cc                  # demi-grand axe : 2a/(a² − h²) = C
    lo, hi = np.full_like(t, b * 0.999), np.full_like(t, a_ * 1.001)
    cph = np.cos(t)
    for _ in range(45):                                        # bissection vectorisée sur chaque rayon
        mid = 0.5 * (lo + hi)
        V = 1 / np.sqrt(mid**2 + h**2 - 2 * mid * h * cph) + 1 / np.sqrt(mid**2 + h**2 + 2 * mid * h * cph)
        dedans = V > Cc
        lo, hi = np.where(dedans, mid, lo), np.where(dedans, hi, mid)
    r = 0.5 * (lo + hi)
    return _placer(r * np.cos(t), r * np.sin(t), p[0], p[1])


def residus(famille, p, px, py):
    """Distance signée (px) de chaque point au plus proche point de la courbe (+ : point à l'extérieur)."""
    X, Y = famille(p)
    d2 = (px[:, None] - X[None, :])**2 + (py[:, None] - Y[None, :])**2
    j = np.argmin(d2, axis=1)
    signe = np.sign(np.hypot(px - p[0], py - p[1]) - np.hypot(X[j] - p[0], Y[j] - p[1]))
    return signe * np.sqrt(d2[np.arange(len(px)), j])


def ajuster_points(famille, p0, px, py, bornes=None):
    kw = {} if bornes is None else {"bounds": bornes}
    r = least_squares(lambda p: residus(famille, p, px, py), p0, loss="soft_l1", f_scale=1.5, x_scale=np.maximum(np.abs(p0), 0.05), **kw)
    res = residus(famille, r.x, px, py)
    return r.x, float(np.sqrt(np.mean(res**2))), float(1.4826 * np.median(np.abs(res - np.median(res)))), res


def rapport_ergo(a):
    return np.sqrt(4 + a**2) / (1 + np.sqrt(1 - a**2))


def ecart_forme_ergo_ellipse(a):
    """Écart quadratique moyen (fraction du demi-grand axe) entre l'ergosurface de Kerr et l'ellipse de
    mêmes demi-axes — propriété des courbes, indépendante de l'image."""
    th = np.linspace(0, np.pi / 2, 2001)
    rE = 1 + np.sqrt(1 - a**2 * np.cos(th)**2)
    rho, z = np.sqrt(rE**2 + a**2) * np.sin(th), rE * np.cos(th)
    A, B = np.sqrt(4 + a**2), 1 + np.sqrt(1 - a**2)
    k = 1 / np.hypot(rho / A, z / B)
    return float(np.sqrt(np.mean((np.hypot(rho, z) * (1 - k))**2)) / A)


# --- 5a. Points du contour du sphéroïde central : trait le plus EXTÉRIEUR le long de rayons ----------
cen0 = ellipses["sphéroïde central (enveloppe)"]
SECTEURS = [(-36, 1), (11, 36), (144, 169), (179, 216)]     # degrés ; on évite les pôles (traits confondus) et l'axe en tirets
phis = np.radians(np.concatenate([np.arange(lo, hi + 0.01, 1.5) for lo, hi in SECTEURS]))
FEN = 6.0
pts_cen = []
for ph in phis:
    r_ell = 1 / np.hypot(np.cos(ph) / cen0["a"], np.sin(ph) / cen0["b"])
    rr = np.arange(r_ell + FEN, r_ell - FEN, -0.1)
    d = noirceur(cen0["cx"] + rr * np.cos(ph), cen0["cy"] + rr * np.sin(ph))
    seuil = max(0.5 * d.max(), 2.0 * FOND)
    for i in range(1, len(rr) - 1):                          # de l'extérieur vers l'intérieur : premier maximum local significatif
        if d[i] > seuil and d[i] >= d[i - 1] and d[i] >= d[i + 1]:
            pts_cen.append((cen0["cx"] + rr[i] * np.cos(ph), cen0["cy"] + rr[i] * np.sin(ph)))
            break
pts_cen = np.array(pts_cen)

# --- 5b. Points du grand contour E1 (enveloppe des anneaux) ----------------------------------------------
# E1 est d'abord défini par les 12 sommets des anneaux (ajustement géométrique d'une ellipse) ; on y ajoute des points du trait
# pâle relevés sur ses arcs GAUCHES (haut et bas), là où E1 et E2 sont séparés de plus de 6 px, dans une fenêtre de ±3,5 px autour
# de la prédiction. (Première version : arcs haut et bas complets — elle mélangeait des points de E1 et de E2 ; corrigé en phase 7.)
anneaux_ = {k: v for k, v in ellipses.items() if k.startswith("anneau")}
sommets = np.array([(e["cx"], e["cy"] - e["b"]) for e in anneaux_.values()] + [(e["cx"], e["cy"] + e["b"]) for e in anneaux_.values()])
p_E1, rms_E1_sommets, _, res_E1_sommets = ajuster_points(fam_ellipse, [169.5, 150.2, 146.0, 93.5], sommets[:, 0], sommets[:, 1])
E1 = {"cx": float(p_E1[0]), "cy": float(p_E1[1]), "a": float(p_E1[2]), "b": float(p_E1[3]), "rms_sommets_px": rms_E1_sommets,
      "definition": "ellipse ajustée aux 12 sommets des six anneaux (indépendante du trait pâle)"}
pts_ext = [tuple(v) for v in sommets]
n_sommets = len(pts_ext)
for x, signe in [(x_, -1) for x_ in np.arange(84, 132.1, 8.0)] + [(x_, +1) for x_ in np.arange(92, 122.1, 6.0)]:
    y_pred = E1["cy"] + signe * E1["b"] * np.sqrt(max(1 - ((x - E1["cx"]) / E1["a"])**2, 0.0))
    yv = np.arange(y_pred - 3.5, y_pred + 3.51, 0.1)
    d = np.mean([noirceur(np.full_like(yv, x + dx), yv) for dx in (-1, 0, 1)], axis=0)
    if d.max() > 1.5 * FOND:
        pts_ext.append((float(x), float(yv[np.argmax(d)])))
pts_ext = np.array(pts_ext)

SIGMA_NUM = 1.0             # incertitude de numérisation adoptée pour les points de contour [px]
comparaisons = {}
for cible, pts, e in (("sphéroïde central (enveloppe)", pts_cen, ellipses["sphéroïde central (enveloppe)"]),
                      ("grande ellipse extérieure", pts_ext, ellipses["grande ellipse extérieure"])):
    px, py = pts[:, 0], pts[:, 1]
    fam = {}
    p_ell, rms, mad, res_e = ajuster_points(fam_ellipse, [e["cx"], e["cy"], e["a"], e["b"]], px, py)
    fam["ellipse générique"] = {"n_parametres": 4, "parametres": p_ell.tolist(), "rms_px": rms, "sigma_robuste_px": mad}
    q = p_ell[2] / p_ell[3]
    p, rms, mad, _ = ajuster_points(fam_superellipse, list(p_ell) + [2.0], px, py, bornes=([-np.inf] * 4 + [1.2], [np.inf] * 4 + [6.0]))
    fam["super-ellipse (témoin de forme, exposant n libre)"] = {"n_parametres": 5, "parametres": p.tolist(), "rms_px": rms, "sigma_robuste_px": mad, "exposant_n": float(p[4])}
    a_ergo = brentq(lambda a: rapport_ergo(a) - min(q, rapport_ergo(1.0) - 1e-9), 0.0, 1.0)
    p, rms, mad, _ = ajuster_points(fam_ergosurface, [p_ell[0], p_ell[1], p_ell[2] / np.sqrt(4 + a_ergo**2), a_ergo], px, py,
                                    bornes=([-np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, 1]))
    fam["ergosurface de Kerr, axe de rotation vertical"] = {"n_parametres": 4, "parametres": p.tolist(), "rms_px": rms, "sigma_robuste_px": mad, "a_sur_M": float(p[3])}
    p, rms, mad, _ = ajuster_points(fam_ergosurface_h, [p_ell[0], p_ell[1], p_ell[3] / 2.0, 0.3], px, py, bornes=([-np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, 1]))
    fam["ergosurface de Kerr, axe de rotation horizontal"] = {"n_parametres": 4, "parametres": p.tolist(), "rms_px": rms, "sigma_robuste_px": mad, "a_sur_M": float(p[3])}
    p, rms, mad, _ = ajuster_points(fam_horizon, [p_ell[0], p_ell[1], p_ell[2] / np.sqrt(2), 0.99], px, py, bornes=([-np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, 1]))
    fam["horizon de Kerr, axe vertical (rapport d'axes ≤ √2)"] = {"n_parametres": 4, "parametres": p.tolist(), "rms_px": rms, "sigma_robuste_px": mad, "a_sur_M": float(p[3])}
    p, rms, mad, _ = ajuster_points(fam_equipotentielle, [p_ell[0], p_ell[1], 0.75 * p_ell[2], p_ell[3]], px, py)
    fam["équipotentielle de deux masses (écartement libre)"] = {"n_parametres": 4, "parametres": p.tolist(), "rms_px": rms, "sigma_robuste_px": mad, "demi_separation_h_px": abs(float(p[2]))}
    fam["équipotentielle de deux masses (écartement libre)"]["rapport_h_sur_demi_separation_dessinee"] = abs(float(p[2])) / (SEP_SING / 2)
    # équipotentielle des deux masses TELLES QUE DESSINÉES (positions et écartement imposés) : un seul paramètre libre
    r1 = least_squares(lambda pb: residus(fam_equipotentielle, [X_MASSES, float(y_axe(X_MASSES)), SEP_SING / 2, pb[0]], px, py),
                       [p_ell[3]], loss="soft_l1", f_scale=1.5)
    res1 = residus(fam_equipotentielle, [X_MASSES, float(y_axe(X_MASSES)), SEP_SING / 2, r1.x[0]], px, py)
    fam["équipotentielle des deux masses telles que dessinées"] = {
        "n_parametres": 1, "parametres": [X_MASSES, float(y_axe(X_MASSES)), SEP_SING / 2, float(r1.x[0])], "rms_px": float(np.sqrt(np.mean(res1**2))),
        "sigma_robuste_px": float(1.4826 * np.median(np.abs(res1 - np.median(res1))))}
    for k_ in fam:
        fam[k_]["rms_sur_demi_grand_axe"] = fam[k_]["rms_px"] / float(p_ell[2])
        fam[k_]["rms_sur_rms_ellipse"] = fam[k_]["rms_px"] / fam["ellipse générique"]["rms_px"]
    comparaisons[cible] = {
        "n_points": int(len(px)), "points_px": pts.tolist(),
        "rapport_d_axes_mesure": float(q),
        "rapport_max_horizon_kerr": float(np.sqrt(2)),
        "a_sur_M_donnant_ce_rapport_pour_l_ergosurface": float(a_ergo),
        "ecart_de_forme_ergosurface_vs_ellipse_fraction_du_demi_grand_axe": ecart_forme_ergo_ellipse(a_ergo),
        "ecart_de_forme_ergosurface_vs_ellipse_px": ecart_forme_ergo_ellipse(a_ergo) * float(p_ell[2]),
        "familles": fam,
    }

# --- 5c. Test des pôles (sphéroïde central) --------------------------------------------------------
# Les familles sont ajustées sur les seuls arcs équatoriaux (les pôles sont noyés dans les méridiens) :
# sur ces arcs, ellipse et ergosurface se distinguent mal (constaté sur données de synthèse). Ce qui les
# distingue, c'est la position des PÔLES qu'elles prédisent : une ergosurface y est déprimée (elle y
# rejoint l'horizon), une ellipse non. On mesure donc les pôles indépendamment et on compare.


def detecter_pole(y_dehors, y_dedans):
    """Bord extérieur de la tache sombre où convergent les méridiens, de part et d'autre de la ligne des pôles."""
    cols = np.concatenate([np.arange(X_MASSES - 8, X_MASSES - 2.9, 1.0), np.arange(X_MASSES + 3, X_MASSES + 8.1, 1.0)])   # on évite le trait de rappel du repère 1
    yv = np.arange(y_dehors, y_dedans, 0.1 * np.sign(y_dedans - y_dehors))
    d = np.mean([noirceur(np.full_like(yv, c_), yv) for c_ in cols], axis=0)
    for i in range(1, len(yv) - 1):
        if d[i] > 0.5 * d.max() and d[i] >= d[i - 1] and d[i] >= d[i + 1]:
            return float(yv[i])
    return float(yv[np.argmax(d)])


Y_POLE_HAUT, Y_POLE_BAS = detecter_pole(106.0, 122.0), detecter_pole(184.0, 170.0)
poles_x = np.array([X_MASSES, X_MASSES])
poles_y = np.array([Y_POLE_HAUT, Y_POLE_BAS])
GENERATEURS = {"ellipse générique": fam_ellipse, "super-ellipse (témoin de forme, exposant n libre)": fam_superellipse,
               "ergosurface de Kerr, axe de rotation vertical": fam_ergosurface, "ergosurface de Kerr, axe de rotation horizontal": fam_ergosurface_h,
               "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)": fam_horizon, "équipotentielle de deux masses (écartement libre)": fam_equipotentielle,
               "équipotentielle des deux masses telles que dessinées": fam_equipotentielle}
test_poles = {"y_pole_haut_px": Y_POLE_HAUT, "y_pole_bas_px": Y_POLE_BAS, "demi_hauteur_polaire_px": 0.5 * (Y_POLE_BAS - Y_POLE_HAUT), "erreur_de_prediction_px": {}}
for nom_f, f_ in comparaisons["sphéroïde central (enveloppe)"]["familles"].items():
    err = float(np.mean(np.abs(residus(GENERATEURS[nom_f], np.array(f_["parametres"]), poles_x, poles_y))))
    f_["erreur_aux_poles_px"] = err
    test_poles["erreur_de_prediction_px"][nom_f] = err

# Puissance du test, sur données de synthèse (mêmes secteurs, bruit de 0,7 px) : vraie ellipse, puis vraie ergosurface.
# Moyenne sur 20 réalisations du bruit (une seule réalisation donnait un résultat trop dépendant du tirage : 1,4 à 1,9 px).
th_syn = np.radians(np.concatenate([np.arange(lo, hi + 0.01, 1.5) for lo, hi in SECTEURS]))
N_REAL = 20
puissance = {}
for vrai, gen_v, p_v, t_v in (("ellipse de rapport 1,6", fam_ellipse, [150.0, 150.0, 49.5, 30.9], th_syn),
                              ("ergosurface de Kerr a/M = 0,93", fam_ergosurface, [150.0, 150.0, 22.4, 0.93], th_syn + np.pi / 2)):
    x0_, y0_ = gen_v(p_v, t_v)
    xp_, yp_ = gen_v(p_v, np.array([np.pi / 2, 3 * np.pi / 2]) if gen_v is fam_ellipse else np.array([0.0, np.pi]))     # vrais pôles
    err_e, err_g = [], []
    for _ in range(N_REAL):
        xs_, ys_ = x0_ + RNG.normal(0, 0.7, x0_.size), y0_ + RNG.normal(0, 0.7, y0_.size)
        pe_, _, _, _ = ajuster_points(fam_ellipse, [150, 150, 49, 31], xs_, ys_)
        pg_, _, _, _ = ajuster_points(fam_ergosurface, [150, 150, 22, 0.9], xs_, ys_, bornes=([-np.inf, -np.inf, 0, 0], [np.inf, np.inf, np.inf, 1]))
        err_e.append(float(np.mean(np.abs(residus(fam_ellipse, pe_, xp_, yp_)))))
        err_g.append(float(np.mean(np.abs(residus(fam_ergosurface, pg_, xp_, yp_)))))
    puissance[vrai] = {"n_realisations": N_REAL,
                       "erreur_poles_si_on_ajuste_une_ellipse_px": float(np.mean(err_e)), "ecart_type_ellipse_px": float(np.std(err_e)),
                       "erreur_poles_si_on_ajuste_une_ergosurface_px": float(np.mean(err_g)), "ecart_type_ergosurface_px": float(np.std(err_g))}
test_poles["puissance_sur_donnees_de_synthese"] = puissance

# ---------------------------------------------------------------------------
# 6. Les six anneaux sont-ils des sections parallèles de la grande ellipse ?
# ---------------------------------------------------------------------------
ext = E1                                             # E1 : ellipse des 12 sommets (et non plus le trait pâle ajusté à la noirceur)
anneaux = {k: v for k, v in ellipses.items() if k.startswith("anneau")}
table_anneaux = {}
for nom, e in anneaux.items():
    u = (e["cx"] - ext["cx"]) / ext["a"]
    b_pred = ext["b"] * np.sqrt(max(1 - u**2, 0))
    table_anneaux[nom] = {"position_relative": u, "demi_hauteur_mesuree_px": e["b"], "demi_hauteur_predite_px": b_pred,
                          "residu_fraction_de_B": (e["b"] - b_pred) / ext["b"],
                          "decentrement_vertical_vs_axe_px": e["cy"] - float(y_axe(e["cx"]))}
# Validation croisée : l'ellipse ajustée aux sommets de DEUX paires d'anneaux prédit-elle le rayon de la troisième paire ?
croisee = {}
for i_, n_ in ((2, "negative"), (3, "null"), (4, "positive")):
    exclus = [f"anneau G{i_} (« {n_} », gauche)", f"anneau D{i_} (« {n_} », droite)"]
    garde_ = [k for k in anneaux if k not in exclus]
    xs_ = np.array([anneaux[k]["cx"] for k in garde_] * 2)
    ys_ = np.array([anneaux[k]["cy"] - anneaux[k]["b"] for k in garde_] + [anneaux[k]["cy"] + anneaux[k]["b"] for k in garde_])
    pc_, _, _, _ = ajuster_points(fam_ellipse, list(p_E1), xs_, ys_)
    for k in exclus:
        bp_ = pc_[3] * np.sqrt(max(1 - ((anneaux[k]["cx"] - pc_[0]) / pc_[2])**2, 0.0))
        croisee[k] = {"rayon_mesure_px": anneaux[k]["b"], "rayon_predit_px": float(bp_), "erreur_px": float(anneaux[k]["b"] - bp_)}
erreur_croisee_max = float(max(abs(v["erreur_px"]) for v in croisee.values()))
erreur_croisee_rms = float(np.sqrt(np.mean([v["erreur_px"]**2 for v in croisee.values()])))
res_anneaux = np.array([v["residu_fraction_de_B"] for v in table_anneaux.values()])
# ajustement direct d'une ellipse aux 12 sommets des anneaux (indépendant de la grande ellipse tracée)
pts_x = np.array([e["cx"] for e in anneaux.values()] * 2)
pts_y = np.array([e["cy"] - e["b"] for e in anneaux.values()] + [e["cy"] + e["b"] for e in anneaux.values()])
fit12 = least_squares(lambda p: ((pts_x - p[0]) / p[2])**2 + ((pts_y - p[1]) / p[3])**2 - 1, [171, 150, 150, 92])
rms12 = float(np.sqrt(np.mean(fit12.fun**2)) / 2)          # ≈ résidu radial relatif
centre_anneaux = float(np.mean([0.5 * (anneaux[f"anneau G{i} (« {n} », gauche)"]["cx"] + anneaux[f"anneau D{i} (« {n} », droite)"]["cx"])
                                for i, n in ((2, "negative"), (3, "null"), (4, "positive"))]))
envergures = {n: anneaux[f"anneau D{i} (« {n} », droite)"]["cx"] - anneaux[f"anneau G{i} (« {n} », gauche)"]["cx"]
              for i, n in ((2, "negative"), (3, "null"), (4, "positive"))}
rapports_env = [envergures["null"] / envergures["negative"], envergures["positive"] / envergures["negative"]]


# Comparaison (déclarée a priori) aux trois rayons caractéristiques de Kerr {r-, r+, 2M} : existe-t-il a/M ?
def ecart_rapports_kerr(a):
    s = np.sqrt(1 - a**2)
    return np.hypot((1 + s) / (1 - s) - rapports_env[0], 2 / (1 - s) - rapports_env[1])


aa = np.linspace(0.05, 0.9999, 4000)
ec = np.array([ecart_rapports_kerr(a) for a in aa])
kerr_rayons = {"rapports_mesures_null_et_positive_sur_negative": rapports_env, "meilleur_a_sur_M": float(aa[np.argmin(ec)]),
               "rapports_kerr_au_meilleur_a": [float((1 + np.sqrt(1 - aa[np.argmin(ec)]**2)) / (1 - np.sqrt(1 - aa[np.argmin(ec)]**2))),
                                               float(2 / (1 - np.sqrt(1 - aa[np.argmin(ec)]**2)))],
               "ecart_minimal": float(ec.min())}

# ---------------------------------------------------------------------------
# 7. Méridiens du sphéroïde central (balayage de la demi-largeur)
# ---------------------------------------------------------------------------
cen = ellipses["sphéroïde central (enveloppe)"]
t_mer = np.radians(np.linspace(-70, 70, 141))
x_poles = X_MASSES                                   # les méridiens convergent vers des pôles situés au-dessus des masses
largeurs = np.arange(-52.0, 62.01, 0.25)
prof_mer = np.array([np.mean(noirceur(x_poles + s * np.cos(t_mer) + 0 * t_mer, cen["cy"] + cen["b"] * np.sin(t_mer))) for s in largeurs])
lis = gaussian_filter(prof_mer, 2)
pics_mer = [float(largeurs[i]) for i in range(2, len(largeurs) - 2) if lis[i] > lis[i - 1] and lis[i] >= lis[i + 1] and lis[i] > FOND * 1.6 and abs(largeurs[i]) > 3]

# ---------------------------------------------------------------------------
# 8. Courbes « en entonnoir » reliant le sphéroïde aux grands anneaux : profil R(x)
# ---------------------------------------------------------------------------
ANCRES_HAUT = np.array([(84, 97), (90, 101.5), (100, 106.5), (110, 110.5), (120, 112.5), (130, 114), (138, 114.5), (150, 113.5), (160, 112.5),
                        (170, 111.5), (185, 110), (200, 107), (215, 103.5), (230, 99), (245, 93.5), (255, 88.5), (262, 84)], float)
ANCRES_BAS = np.array([(84, 201), (90, 197), (100, 192), (115, 184.5), (130, 178.5), (140, 176), (155, 177.5), (170, 180), (190, 184.5),
                       (210, 190), (230, 197.5), (245, 204.5), (255, 210.5), (262, 215.5)], float)


def affiner(ancres, demi_fenetre=2.0):
    """Affine chaque ancre lue à l'œil : barycentre de noirceur sur ±2 px dans la direction verticale."""
    out = []
    for x, y in ancres:
        yv = np.arange(y - demi_fenetre, y + demi_fenetre + 1e-9, 0.1)
        pr = np.mean([noirceur(np.full_like(yv, x + dx), yv) for dx in (-1, 0, 1)], axis=0)
        w = np.clip(pr - 0.6 * pr.max(), 0, None)
        out.append((x, np.sum(w * yv) / np.sum(w)))
    return np.array(out)


haut, bas = affiner(ANCRES_HAUT), affiner(ANCRES_BAS)
deplacement_ancres = float(max(np.max(np.abs(haut[:, 1] - ANCRES_HAUT[:, 1])), np.max(np.abs(bas[:, 1] - ANCRES_BAS[:, 1]))))
# on ajoute les sommets des deux grands anneaux (extrémités de l'entonnoir)
g2, d2 = ellipses["anneau G2 (« negative », gauche)"], ellipses["anneau D2 (« negative », droite)"]
x_prof = np.concatenate([[g2["cx"]], haut[:, 0], [d2["cx"]]])
R_haut = np.concatenate([[g2["b"]], y_axe(haut[:, 0]) - haut[:, 1], [d2["b"]]])
x_prof_b = np.concatenate([[g2["cx"]], bas[:, 0], [d2["cx"]]])
R_bas = np.concatenate([[g2["b"]], bas[:, 1] - y_axe(bas[:, 0]), [d2["b"]]])
x_com = np.linspace(g2["cx"], d2["cx"], 41)
R_moy = 0.5 * (np.interp(x_com, x_prof, R_haut) + np.interp(x_com, x_prof_b, R_bas))
SIGMA_R = 1.5                                  # incertitude de numérisation adoptée [px]
i_gorge = int(np.argmin(R_moy))
X_GORGE, R_GORGE = float(x_com[i_gorge]), float(R_moy[i_gorge])

FAMILLES_ENTONNOIR = {
    "parabole de Flamm (Schwarzschild) : R0 + (x−x0)²/(4R0)": (lambda p, x: p[1] + (x - p[0])**2 / (4 * p[1]), [X_GORGE, R_GORGE]),
    "caténoïde d'Ellis/Morris-Thorne : R0 cosh((x−x0)/R0)": (lambda p, x: p[1] * np.cosh((x - p[0]) / p[1]), [X_GORGE, R_GORGE]),
    "parabole libre : R0 + κ(x−x0)²": (lambda p, x: p[1] + p[2] * (x - p[0])**2, [X_GORGE, R_GORGE, 3e-3]),
    "chaînette libre : R0 cosh((x−x0)/L)": (lambda p, x: p[1] * np.cosh((x - p[0]) / p[2]), [X_GORGE, R_GORGE, 80.0]),
    "hyperboloïde à une nappe : R0 sqrt(1 + ((x−x0)/L)²)": (lambda p, x: p[1] * np.sqrt(1 + ((x - p[0]) / p[2])**2), [X_GORGE, R_GORGE, 60.0]),
    "sinusoïde : A − B cos(2π(x−x0)/λ)": (lambda p, x: p[1] - p[2] * np.cos(2 * np.pi * (x - p[0]) / p[3]), [X_GORGE, R_GORGE + 20, 20.0, 300.0]),
    "témoin non physique : parabole à deux courbures (gauche ≠ droite)": (lambda p, x: p[1] + np.where(x < p[0], p[2], p[3]) * (x - p[0])**2, [X_GORGE, R_GORGE, 6e-3, 2e-3]),
}
entonnoir = {}
for nom, (f, p0) in FAMILLES_ENTONNOIR.items():
    r = least_squares(lambda p: f(p, x_com) - R_moy, p0, x_scale=np.maximum(np.abs(p0), 1e-3))
    rms = float(np.sqrt(np.mean(r.fun**2)))
    n_p = len(p0)
    chi2 = float(np.sum((r.fun / SIGMA_R)**2))
    entonnoir[nom] = {"parametres": r.x.tolist(), "n_parametres": n_p, "rms_px": rms, "rms_sur_R_gorge": rms / R_GORGE,
                      "chi2_reduit": chi2 / (len(x_com) - n_p), "courbe": f(r.x, x_com).tolist()}
# asymétrie de l'entonnoir : demi-largeurs à gauche et à droite de la gorge
asym = {"x_gorge_px": X_GORGE, "R_gorge_px": R_GORGE, "distance_gorge_anneau_gauche_px": X_GORGE - g2["cx"],
        "distance_gorge_anneau_droit_px": d2["cx"] - X_GORGE, "rapport_droite_sur_gauche": (d2["cx"] - X_GORGE) / (X_GORGE - g2["cx"]),
        "R_anneau_gauche_px": g2["b"], "R_anneau_droit_px": d2["b"]}

# ---------------------------------------------------------------------------
# 9. Tableau des proportions relatives (unité : demi-grand axe A de la grande ellipse)
# ---------------------------------------------------------------------------
A_REF = ext["a"]                                    # demi-grand axe de E1 (ellipse des 12 sommets d'anneaux)
E2 = ellipses["second grand contour E2 (décalé vers la droite)"]
LECTURES_MANUELLES = {      # extrémités des traits de cote 6 à 9, relues sur la copie nette recalée (±1,5 px ; voir §9 bis)
    "7_mass_offset": (140.4, 178.8), "8_rear_mass_dist": (82.6, 140.4), "9_forward_mass_dist": (140.4, 233.6),
    "6_vertical_safe_distance_hauteur_du_crochet": (125.5, 167.0), "barre_epaisse_horizontale": (82.0, 234.0),
}
proportions = {
    "unite": "demi-grand axe A du grand contour E1, ellipse passant par les 12 sommets des anneaux (DOC-009 ne porte aucune cote ; voir cotes_doc014 pour la variante cotée)",
    "A_px": A_REF, "B_sur_A": ext["b"] / A_REF,
    "spheroide_central_demi_axes_sur_A": [cen["a"] / A_REF, cen["b"] / A_REF],
    "spheroide_central_rapport_d_axes": cen["a"] / cen["b"],
    "grande_ellipse_rapport_d_axes": ext["a"] / ext["b"],
    "rapport_d_echelle_grande_ellipse_sur_spheroide": [ext["a"] / cen["a"], ext["b"] / cen["b"]],
    "second_grand_contour_E2": {"demi_axes_sur_A": [E2["a"] / A_REF, E2["b"] / A_REF], "rapport_d_axes": E2["a"] / E2["b"],
                                "decalage_du_centre_vs_E1_sur_A": (E2["cx"] - ext["cx"]) / A_REF, "contraste_sur_fond": E2["score"] / FOND,
                                "extremites_gauche_droite_px": [E2["cx"] - E2["a"], E2["cx"] + E2["a"]]},
    "separation_des_singularites_sur_A": SEP_SING / A_REF,
    "separation_des_singularites_sur_demi_largeur_du_spheroide": SEP_SING / cen["a"],
    "decalage_masses_vs_centre_des_anneaux_sur_A": (centre_anneaux - X_MASSES) / A_REF,
    "decalage_spheroide_vs_centre_des_anneaux_sur_A": (centre_anneaux - cen["cx"]) / A_REF,
    "decalage_vertical_spheroide_vs_axe_px": cen["cy"] - float(y_axe(cen["cx"])),
    "envergures_des_paires_d_anneaux_sur_A": {k: v / A_REF for k, v in envergures.items()},
    "rayons_des_anneaux_sur_A": {k: v["b"] / A_REF for k, v in anneaux.items()},
    "cotes_lues_a_l_oeil_sur_A": {k: (v[1] - v[0]) / A_REF for k, v in LECTURES_MANUELLES.items()},
}

# ---------------------------------------------------------------------------
# 9 bis. Les quatre distances en mètres de la variante C204-DOC-014 (correction n° 37)
# ---------------------------------------------------------------------------
# DOC-009 ne porte aucune cote. Sa variante DOC-014 (même tracé ; première trace en août 2003 sur un site
# tiers ; attribution à l'auteur de 2000-2001 NON ÉTABLIE) inscrit dans la légende : repère 6 « VERTICAL SAFE
# DISTANCE (6 METERS) », 7 « MASS OFFSET (5 METERS) », 8 « REAR MASS DIST. (8 METERS) », 9 « FORWARD MASS DIST.
# (11 METERS) » (transcription de l'Équipe A). Extrémités des traits de cote lues par nous sur la copie
# timetravel16_07.jpg recalée, en pixels du repère de référence (lecture manuelle, ±1,5 px).
COTES_DOC014 = {
    "6 — VERTICAL SAFE DISTANCE": {"metres": 6.0, "extremites_px": (125.5, 167.0), "direction": "verticale (hauteur du crochet)"},
    "7 — MASS OFFSET": {"metres": 5.0, "extremites_px": (140.4, 178.8), "direction": "horizontale"},
    "8 — REAR MASS DIST.": {"metres": 8.0, "extremites_px": (82.6, 140.4), "direction": "horizontale"},
    "9 — FORWARD MASS DIST.": {"metres": 11.0, "extremites_px": (140.4, 233.6), "direction": "horizontale"},
}
for _c in COTES_DOC014.values():
    _c["longueur_px"] = _c["extremites_px"][1] - _c["extremites_px"][0]
    _c["echelle_px_par_m"] = _c["longueur_px"] / _c["metres"]
_ech = np.array([_c["echelle_px_par_m"] for _c in COTES_DOC014.values()])
ECHELLE_MOY, ECHELLE_DISP = float(_ech.mean()), float(_ech.std(ddof=1) / _ech.mean())
cotes_doc014 = {
    "statut": "valeurs portées par DOC-014 seulement ; attribution à l'auteur non établie ; [DOC] pour la lecture, [DÉD] pour les conversions",
    "cotes": COTES_DOC014,
    "echelle_moyenne_px_ref_par_m": ECHELLE_MOY, "dispersion_relative_des_echelles": ECHELLE_DISP,
    "incertitude_relative_de_pointe": 1.5 / float(np.mean([_c["longueur_px"] for _c in COTES_DOC014.values()])),
    "rapport_cote8_sur_cote9_dessine": COTES_DOC014["8 — REAR MASS DIST."]["longueur_px"] / COTES_DOC014["9 — FORWARD MASS DIST."]["longueur_px"],
    "rapport_cote8_sur_cote9_inscrit": 8.0 / 11.0,
    "conversions_en_metres_DED": {
        "demi_grand_axe_A_du_contour_exterieur": A_REF / ECHELLE_MOY,
        "envergures_des_paires_d_anneaux": {k: v / ECHELLE_MOY for k, v in envergures.items()},
        "demi_largeur_du_spheroide_central_(zone_declaree_hors_echelle)": cen["a"] / ECHELLE_MOY,
        "separation_des_deux_singularites_(zone_declaree_hors_echelle)": SEP_SING / ECHELLE_MOY,
    },
    "comparaison_au_texte": {
        "champ_efficace_revendique_m": list(cc.REVENDICATIONS["zone_effet_m"]),
        "demi_envergures_dessinees_m": {k: 0.5 * v / ECHELLE_MOY for k, v in envergures.items()},
        "rapport_min_dessin_sur_texte": float(0.5 * min(envergures.values()) / ECHELLE_MOY / cc.REVENDICATIONS["zone_effet_m"][1]),
        "rapport_max_dessin_sur_texte": float(0.5 * max(envergures.values()) / ECHELLE_MOY / cc.REVENDICATIONS["zone_effet_m"][0]),
    },
    "lecture": "les quatre valeurs sont à peu près proportionnelles au dessin (une seule échelle à ~9 % près, pour ~2,5 % d'incertitude de pointé), "
               "mais pas exactement (rapport cote 8 / cote 9 dessiné 0,62 contre 8/11 = 0,73) ; à cette échelle les « horizons » dessinés "
               "s'étendent sur 26 à 36 m, sans rapport avec les 3,0 à 3,7 m (« 10 à 12 pieds ») du texte",
}

# ---------------------------------------------------------------------------
# 10. Tests de validation, contrôles, résultats et verdicts
# ---------------------------------------------------------------------------
val.consigner("résultat", "Les sommets des 6 anneaux sont sur une même ellipse E1 : erreur max. de validation croisée par paires [px]", erreur_croisee_max,
              commentaire=f"l'ellipse ajustée à deux paires prédit le rayon de la troisième ; RMS {erreur_croisee_rms:.2f} px ; RMS des 12 sommets {rms_E1_sommets:.2f} px",
              constat=erreur_croisee_max < 3.0)
val.consigner("contrôle", "Ancres de l'entonnoir : déplacement max. lors de l'affinage automatique [px]", deplacement_ancres,
              commentaire="borné à ±2 px par la fenêtre de recherche : ne peut pas échouer", constat=deplacement_ancres <= 2.01)
val.verifier("Équipotentielle : limite h → 0 = cercle (rapport d'axes)", (lambda xy: np.ptp(xy[0]) / np.ptp(xy[1]))(fam_equipotentielle([150, 150, 1e-6, 30])), 1.0, tol_rel=2e-2)
val.verifier("Ergosurface de Kerr : rapport d'axes (a = M) = √5", rapport_ergo(1.0), np.sqrt(5), tol_rel=1e-12)
# Puissance de la méthode. Un premier test (« le RMS sur les arcs préfère l'ergosurface quand les points en proviennent »)
# a ÉCHOUÉ : RMS 0,41 px (ergosurface) contre 0,40 px (ellipse) — sur les seuls arcs équatoriaux le RMS ne discrimine pas.
# Le test retenu porte sur la prédiction des pôles (§5c) : il doit discriminer dans les deux sens.
pu_e, pu_g = puissance["ellipse de rapport 1,6"], puissance["ergosurface de Kerr a/M = 0,93"]
val.verifier("Test des pôles, synthèse « vraie ellipse » (moyenne de 20 tirages) : l'ellipse ajustée prédit les pôles [px]", pu_e["erreur_poles_si_on_ajuste_une_ellipse_px"], 0.0, tol_abs=2.0)
val.verifier_vrai("Test des pôles, synthèse « vraie ellipse » : l'ergosurface ajustée manque les pôles de plus de 4 px",
                  pu_e["erreur_poles_si_on_ajuste_une_ergosurface_px"] > 4.0, f"{pu_e['erreur_poles_si_on_ajuste_une_ergosurface_px']:.1f} px")
val.verifier("Test des pôles, synthèse « vraie ergosurface » (moyenne de 20 tirages) : l'ergosurface ajustée prédit les pôles [px]", pu_g["erreur_poles_si_on_ajuste_une_ergosurface_px"], 0.0, tol_abs=2.0)
val.verifier_vrai("Test des pôles, synthèse « vraie ergosurface » : l'ellipse ajustée manque les pôles de plus de 4 px",
                  pu_g["erreur_poles_si_on_ajuste_une_ellipse_px"] > 4.0, f"{pu_g['erreur_poles_si_on_ajuste_une_ellipse_px']:.1f} px")

c_cen, c_ext = comparaisons["sphéroïde central (enveloppe)"], comparaisons["grande ellipse extérieure"]
PHYSIQUES = ("ergosurface de Kerr, axe de rotation vertical", "ergosurface de Kerr, axe de rotation horizontal", "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)",
             "équipotentielle de deux masses (écartement libre)", "équipotentielle des deux masses telles que dessinées")
meilleure_physique = {k: min(((n, v["familles"][n]["rms_sur_rms_ellipse"], v["familles"][n]["rms_px"]) for n in PHYSIQUES), key=lambda t: t[1]) for k, v in comparaisons.items()}
symetriques = [v["rms_px"] for k, v in entonnoir.items() if "témoin" not in k]
n_cen = c_cen["familles"]["super-ellipse (témoin de forme, exposant n libre)"]["exposant_n"]
n_ext = c_ext["familles"]["super-ellipse (témoin de forme, exposant n libre)"]["exposant_n"]
verdict = {
    "courbes_fermees": f"Sphéroïde central : ellipse à {c_cen['familles']['ellipse générique']['rms_px']:.2f} px près (RMS, {c_cen['n_points']} points de contour ; exposant de super-ellipse n = {n_cen:.2f}). "
                       f"Contour extérieur : ellipse à {c_ext['familles']['ellipse générique']['rms_px']:.2f} px près ({c_ext['n_points']} points ; n = {n_ext:.2f}).",
    "meilleure_famille_physique_par_courbe": {k: {"famille": v[0], "rms_rapporte_a_celui_de_l_ellipse": v[1], "rms_px": v[2]} for k, v in meilleure_physique.items()},
    "avertissement_zone_hors_echelle": "Les tests de forme « horizon » et « ergosurface » portent sur le sphéroïde central, que le document déclare lui-même "
                                       "hors d'échelle (« This area is not to scale ») ; la forme d'un horizon dépend en outre des coordonnées (sphère en "
                                       "Boyer-Lindquist, sphéroïde aplati en Kerr-Schild). Ces résultats sont DESCRIPTIFS, sans valeur de preuve.",
    "horizon_kerr": f"rapport d'axes mesuré {c_cen['rapport_d_axes_mesure']:.2f} (central) et {c_ext['rapport_d_axes_mesure']:.2f} (extérieur) > √2 = 1,414, "
                    "maximum pour un horizon de Kerr tracé en coordonnées de Kerr-Schild (1 en Boyer-Lindquist) : le dessin n'a pas la forme d'un horizon "
                    "dans ces coordonnées — constat descriptif, voir l'avertissement",
    "ergosurface_kerr": f"sur les arcs équatoriaux seuls, l'ergosurface (a/M ajusté) n'est pas discernable de l'ellipse au RMS "
                        f"({c_cen['familles']['ergosurface de Kerr, axe de rotation vertical']['rms_px']:.2f} px contre {c_cen['familles']['ellipse générique']['rms_px']:.2f} px) ; "
                        f"mais elle prédit des pôles déprimés, à {test_poles['erreur_de_prediction_px']['ergosurface de Kerr, axe de rotation vertical']:.1f} px des pôles dessinés "
                        f"(ellipse : {test_poles['erreur_de_prediction_px']['ellipse générique']:.1f} px ; horizon : {test_poles['erreur_de_prediction_px']['horizon de Kerr, axe vertical (rapport d\'axes ≤ √2)']:.1f} px). "
                        f"Grand contour E1 : ellipse {c_ext['familles']['ellipse générique']['rms_px']:.1f} px, ergosurface {c_ext['familles']['ergosurface de Kerr, axe de rotation vertical']['rms_px']:.1f} px, "
                        f"équipotentielle à écartement libre {c_ext['familles']['équipotentielle de deux masses (écartement libre)']['rms_px']:.1f} px ({c_ext['n_points']} points).",
    "homothetie": f"les deux contours fermés ont le même rapport d'axes ({c_cen['rapport_d_axes_mesure']:.2f} et {c_ext['rapport_d_axes_mesure']:.2f}) à une échelle ×{proportions['rapport_d_echelle_grande_ellipse_sur_spheroide'][0]:.1f} : "
                  "or les équipotentielles d'une paire de masses s'arrondissent en s'éloignant, et les surfaces caractéristiques d'un trou noir de Kerr (horizon, ergosurface) "
                  "n'ont pas la même forme entre elles : deux copies homothétiques ne correspondent à aucune des deux familles",
    "equipotentielle": "les deux masses dessinées ne sont séparées que de "
                       f"{proportions['separation_des_singularites_sur_demi_largeur_du_spheroide']:.2f} demi-largeur du sphéroïde : leurs équipotentielles seraient quasi sphériques "
                       f"(RMS {c_cen['familles']['équipotentielle des deux masses telles que dessinées']['rms_px']:.1f} px sur le sphéroïde) ; une équipotentielle de rapport d'axes 1,6 exigerait des masses "
                       f"{c_cen['familles']['équipotentielle de deux masses (écartement libre)']['rapport_h_sur_demi_separation_dessinee']:.0f} fois plus écartées que dessiné",
    "anneaux": f"les 12 sommets des six anneaux s'alignent sur une ellipse E1 à {rms_E1_sommets:.1f} px près (RMS, 4 paramètres ajustés) : compatible avec des sections parallèles "
               f"(« cercles de latitude ») d'une même ellipse. Réserve : en validation croisée par paires, le rayon de la paire écartée est prédit à {erreur_croisee_rms:.1f} px près (RMS), "
               f"avec une erreur de {erreur_croisee_max:.1f} px sur le plus petit anneau (extrapolation en bout d'ellipse) : le critère de 3 px que nous nous étions fixé n'est PAS satisfait",
    "deux_grands_contours": f"le grand contour pâle est fait de DEUX ellipses de même hauteur : E1 (enveloppe des anneaux, demi-axes {ext['a']:.0f} × {ext['b']:.0f} px) et E2 "
                            f"(demi-axes {E2['a']:.0f} × {E2['b']:.0f} px, centre décalé de {(E2['cx'] - ext['cx']) / A_REF:.2f} A vers la droite, contraste {E2['score'] / FOND:.1f}) ; "
                            "sur la copie de 318 px elles se confondaient et la première version de S08 les traitait comme une seule",
    "centrage": f"le système d'anneaux est centré {proportions['decalage_masses_vs_centre_des_anneaux_sur_A']:.2f} A à droite des masses (« mass offset ») : "
                "aucun champ du vide (newtonien ou relativiste) n'a de surfaces caractéristiques centrées ailleurs que sur ses sources",
    "entonnoir": f"profil asymétrique (anneau droit {asym['rapport_droite_sur_gauche']:.1f} fois plus loin de la gorge que l'anneau gauche) : aucune famille symétrique "
                 f"(Flamm, caténoïde, hyperboloïde, sinusoïde) ne l'ajuste (RMS ≥ {min(symetriques):.1f} px pour une incertitude de {SIGMA_R} px) ; "
                 "seul le témoin non physique à deux courbures passe",
    "sinusoide": "aucune sinusoïde n'apparaît dans le schéma : la sinusoïde ajustée au profil de l'entonnoir n'est pas meilleure que les autres courbes symétriques",
    "cotes": f"DOC-009 ne porte aucune cote ; sa variante DOC-014 (attribution non établie) porte quatre distances en mètres (6, 5, 8, 11 m), à peu près "
             f"proportionnelles au dessin (dispersion {100 * ECHELLE_DISP:.0f} %) et incompatibles avec les distances du texte : à cette échelle les demi-envergures "
             f"des anneaux valent {0.5 * min(envergures.values()) / ECHELLE_MOY:.0f} à {0.5 * max(envergures.values()) / ECHELLE_MOY:.0f} m, contre 3,0 à 3,7 m revendiqués",
    "conclusion": "DOC-009 est une figure géométriquement régulière (ellipses de même rapport d'axes, sections parallèles, sphéroïde « fil de fer ») ; elle ne correspond "
                  "à aucune famille de surfaces physiques testée mieux qu'à des ellipses génériques. DOC-009 ne porte aucune cote ; sa variante DOC-014 (attribution non "
                  "établie) porte quatre distances en mètres, à peu près proportionnelles au dessin et incompatibles avec les distances du texte. Description du schéma, "
                  "sans valeur de test physique ; cela ne prouve rien sur l'intention de l'auteur.",
}
pires_poles = {n: test_poles["erreur_de_prediction_px"][n] for n in PHYSIQUES}
# Les deux énoncés suivants SONT les conclusions de S08 : ce ne sont pas des validations (correction n° 39).
val.consigner("résultat", "Sphéroïde central : erreur de prédiction des pôles, ellipse [px] (référence : meilleure famille physique)",
              test_poles["erreur_de_prediction_px"]["ellipse générique"], min(pires_poles.values()),
              commentaire="zone déclarée « not to scale » par le document : résultat descriptif",
              constat=test_poles["erreur_de_prediction_px"]["ellipse générique"] < min(pires_poles.values()))
val.consigner("résultat", "RMS de la meilleure famille physique rapporté à celui de l'ellipse (minimum sur les deux contours)",
              min(v[1] for v in meilleure_physique.values()), 1.0,
              commentaire=f"{ {k: (v[0], round(v[1], 2)) for k, v in meilleure_physique.items()} } — un rapport de 1,03 à 1,08 signifie « aussi bien que l'ellipse », "
                          "non « moins bien » : le RMS ne départage pas les familles à 4 paramètres",
              constat=all(v[1] >= 1.0 for v in meilleure_physique.values()))

# ---------------------------------------------------------------------------
# 10 bis. Méthode ABANDONNÉE (score de noirceur), conservée pour reproductibilité (correction n° 40)
# ---------------------------------------------------------------------------
# La première version de S08 comparait les familles par le maximum de la noirceur moyenne le long de la courbe.
# Sur la copie de 318 px elle plaçait une famille physique DEVANT l'ellipse (équipotentielle : 1,13 fois le score de
# l'ellipse sur le sphéroïde ; ergosurface : 1,12 fois sur le grand contour — valeurs de la première exécution, dont
# ni le code ni la figure n'avaient été conservés : la Red Team a jugé à juste titre la justification non
# reproductible). On la rejoue ici avec les mêmes familles, les mêmes points de départ et les mêmes rayons de
# confiance, un générateur aléatoire dédié (graine 2040, 60 départs) ; pour chaque courbe obtenue on mesure sa
# distance aux points du contour relevés indépendamment de toute famille (§5a, §5b).
RNG_AB = np.random.default_rng(2040)


def _rejouer_score(e_ref, pts, candidats):
    pe = [e_ref["cx"], e_ref["cy"], e_ref["a"], e_ref["b"]]
    fam = {"ellipse générique": {"parametres": pe, "score_de_noirceur": e_ref["score"], "score_rapporte_a_l_ellipse": 1.0,
                                 "rms_distance_aux_points_du_contour_px": float(np.sqrt(np.mean(residus(fam_ellipse, np.array(pe), pts[:, 0], pts[:, 1])**2)))}}
    for nom_, (gen_, p0_, ech_, rc_) in candidats.items():
        p_, _, sc_ = ajuster(lambda q_, g_=gen_: g_(q_, T_PARAM), p0_, echelle=ech_, rayon_confiance=rc_, n_departs=60, rng=RNG_AB)
        res_ = residus(gen_, p_, pts[:, 0], pts[:, 1])
        fam[nom_] = {"parametres": p_.tolist(), "score_de_noirceur": sc_, "score_rapporte_a_l_ellipse": sc_ / e_ref["score"],
                     "rms_distance_aux_points_du_contour_px": float(np.sqrt(np.mean(res_**2))),
                     "fraction_des_points_du_contour_a_plus_de_3_px": float(np.mean(np.abs(res_) > 3.0))}
    phys = {k: v for k, v in fam.items() if "ellipse" not in k}
    meilleur = max(phys.items(), key=lambda kv: kv[1]["score_de_noirceur"])
    return {"familles": fam, "meilleure_famille_physique_au_score": meilleur[0], "son_score_rapporte_a_l_ellipse": meilleur[1]["score_rapporte_a_l_ellipse"],
            "sa_distance_rms_au_contour_px": meilleur[1]["rms_distance_aux_points_du_contour_px"],
            "distance_rms_de_l_ellipse_au_contour_px": fam["ellipse générique"]["rms_distance_aux_points_du_contour_px"],
            "une_famille_physique_devance_l_ellipse_au_score": bool(meilleur[1]["score_rapporte_a_l_ellipse"] > 1.0)}


_e, _g = ellipses["sphéroïde central (enveloppe)"], ellipses["grande ellipse extérieure"]
_ae = comparaisons["sphéroïde central (enveloppe)"]["a_sur_M_donnant_ce_rapport_pour_l_ergosurface"]
_ag = comparaisons["grande ellipse extérieure"]["a_sur_M_donnant_ce_rapport_pour_l_ergosurface"]
methode_abandonnee = {"cibles": {
    "sphéroïde central (enveloppe)": _rejouer_score(_e, pts_cen, {
        "ergosurface de Kerr, axe de rotation vertical": (fam_ergosurface, [_e["cx"], _e["cy"], _e["a"] / np.sqrt(4 + _ae**2), _ae], [1, 1, 0.5, 0.02], 4.0),
        "ergosurface de Kerr, axe de rotation horizontal": (fam_ergosurface_h, [_e["cx"], _e["cy"], _e["b"] / 2.0, 0.3], [1, 1, 0.5, 0.05], 20.0),
        "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)": (fam_horizon, [_e["cx"], _e["cy"], _e["a"] / np.sqrt(2), 0.99], [1, 1, 0.5, 0.02], 10.0),
        "équipotentielle de deux masses (écartement libre)": (fam_equipotentielle, [_e["cx"], _e["cy"], 0.75 * _e["a"], _e["b"]], [1, 1, 3, 1], 8.0)}),
    "grande ellipse extérieure": _rejouer_score(_g, pts_ext, {
        "ergosurface de Kerr, axe de rotation vertical": (fam_ergosurface, [_g["cx"], _g["cy"], _g["a"] / np.sqrt(4 + _ag**2), _ag], [1, 1, 0.5, 0.02], 4.0),
        "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)": (fam_horizon, [_g["cx"], _g["cy"], _g["a"] / np.sqrt(2), 0.99], [1, 1, 0.5, 0.02], 10.0),
        "équipotentielle de deux masses (écartement libre)": (fam_equipotentielle, [_g["cx"], _g["cy"], 0.75 * _g["a"], _g["b"]], [1, 1, 3, 1], 8.0)}),
}}
_phr = []
for _cib, _m in methode_abandonnee["cibles"].items():
    _phr.append(f"{_cib.split(' (')[0]} : « {_m['meilleure_famille_physique_au_score'].split(' (')[0]} » obtient {_m['son_score_rapporte_a_l_ellipse']:.2f} fois le score de l'ellipse "
                f"et passe à {_m['sa_distance_rms_au_contour_px']:.1f} px (RMS) des points du contour, contre {_m['distance_rms_de_l_ellipse_au_contour_px']:.1f} px pour l'ellipse")
methode_abandonnee["constat"] = " ; ".join(_phr) + (
    ". Un score supérieur ou voisin de celui de l'ellipse s'obtient donc avec une courbe qui ne suit pas le contour (elle longe d'autres traits) : "
    "le score de noirceur n'est pas un critère de ressemblance.")
methode_abandonnee["premiere_execution_non_archivee"] = ("sur la copie de 318 px : équipotentielle 1,13 fois le score de l'ellipse (sphéroïde), ergosurface 1,12 fois (grand contour) ; "
                                                         "valeurs relevées dans la sortie de la première exécution, non reproductibles à l'identique (départs aléatoires)")
val.consigner("contrôle", "Méthode abandonnée (score de noirceur) : meilleur score d'une famille physique rapporté à l'ellipse, max. sur les deux cibles",
              max(_m["son_score_rapporte_a_l_ellipse"] for _m in methode_abandonnee["cibles"].values()), 1.0, commentaire=methode_abandonnee["constat"], constat=None)

# ---------------------------------------------------------------------------
# 11. Figures
# ---------------------------------------------------------------------------
# --- Figure 1 : numérisation -----------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(17, 8.2))
for ax in axes:
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, extent=(0, W_IMG, H_IMG, 0), interpolation="bicubic")
    ax.set_xlim(0, W_IMG)
    ax.set_ylim(262, 42)
    ax.set_xlabel("x [pixels de l'original]")
    ax.set_ylabel("y [pixels]")
    ax.grid(False)
axes[0].set_title(f"(a) {DESIGNATION}" + ("" if COPIE == "reference" else "\nramenée dans le repère de la copie de référence"), fontsize=9.5)
ax = axes[1]
ax.imshow(np.full_like(img, 255), cmap="gray", vmin=0, vmax=255, extent=(0, W_IMG, H_IMG, 0), alpha=0.45)
couleurs_e = {"anneau G2": col["rouge"], "anneau D2": col["rouge"], "anneau G3": col["vert"], "anneau D3": col["vert"], "anneau G4": col["bleu"], "anneau D4": col["bleu"],
              "sphéroïde": col["violet"], "grande": col["orange"], "second": col["jaune"]}
for nom, e in ellipses.items():
    c = next(v for k, v in couleurs_e.items() if nom.startswith(k))
    pe_ = [E1["cx"], E1["cy"], E1["a"], E1["b"]] if nom.startswith("grande") else [e["cx"], e["cy"], e["a"], e["b"]]   # E1 tracé d'après les sommets des anneaux
    x, y = ellipse_xy(pe_, np.linspace(0, 2 * np.pi, 400))
    ax.plot(x, y, color=c, lw=1.8, ls="--" if nom.startswith("second") else "-")
xa = np.array([20, 317])
ax.plot(xa, y_axe(xa), color="k", lw=1, ls="--")
ax.plot(x_sing, y_axe(np.array(x_sing)), "D", color="k", ms=5)
ax.plot(haut[:, 0], haut[:, 1], ".", color=col["ciel"], ms=7)
ax.plot(bas[:, 0], bas[:, 1], ".", color=col["ciel"], ms=7)
ax.plot(centre_anneaux, y_axe(centre_anneaux), "+", color=col["orange"], ms=14, mew=2)
ax.annotate("centre du système\nd'anneaux", (centre_anneaux, y_axe(centre_anneaux)), textcoords="offset points", xytext=(8, 14), fontsize=8, color=col["orange"])
ax.annotate("2 singularités", (X_MASSES, y_axe(X_MASSES)), textcoords="offset points", xytext=(-40, 22), fontsize=8)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([], [], color=col["rouge"], lw=2, label="anneaux « negative time »"), Line2D([], [], color=col["vert"], lw=2, label="anneaux « null time »"),
                   Line2D([], [], color=col["bleu"], lw=2, label="anneaux « positive time »"), Line2D([], [], color=col["violet"], lw=2, label="enveloppe du sphéroïde central"),
                   Line2D([], [], color=col["orange"], lw=2, label="grand contour E1 (par les 12 sommets d'anneaux)"),
                   Line2D([], [], color=col["jaune"], lw=2, ls="--", label="second grand contour E2 (ajusté au trait)"),
                   Line2D([], [], color=col["ciel"], marker=".", ls="", label="ancres de l'entonnoir"),
                   Line2D([], [], color="k", ls="--", label=f"axe (incliné de {np.degrees(INCLINAISON):.2f}°)".replace(".", ","))],
          loc="lower center", ncol=4, fontsize=7.5, framealpha=0.95)
ax.set_title("(b) Numérisation : ellipses ajustées par maximisation de la noirceur le long du contour", fontsize=10)
cc.titre(fig, "S08 — Numérisation approximative du schéma « Tipler sinusoid field » (DOC-009 ne porte aucune cote ; sa variante DOC-014 en porte quatre, en mètres)")
cc.sauver_figure(fig, FIG / f"S08_fig1_numerisation{SUFFIXE}.png", rect=(0, 0.03, 1, 0.93))

# --- Figure 2 : familles physiques vs courbes fermées ------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(16.5, 11.5), gridspec_kw={"width_ratios": [1.5, 1]})
styles = {"ellipse générique": (col["orange"], "-", fam_ellipse), "ergosurface de Kerr, axe de rotation vertical": (col["rouge"], "--", fam_ergosurface),
          "ergosurface de Kerr, axe de rotation horizontal": (col["gris"], "--", fam_ergosurface_h),
          "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)": (col["bleu"], "-.", fam_horizon),
          "équipotentielle de deux masses (écartement libre)": (col["vert"], ":", fam_equipotentielle),
          "équipotentielle des deux masses telles que dessinées": (col["violet"], "-", fam_equipotentielle),
          "super-ellipse (témoin de forme, exposant n libre)": (col["ciel"], "-", fam_superellipse)}
for ligne, (cible, fenetre) in enumerate((("sphéroïde central (enveloppe)", (85, 205, 185, 105)), ("grande ellipse extérieure", (0, 318, 262, 42)))):
    ax = axes[ligne, 0]
    ax.imshow(img, cmap="gray", vmin=0, vmax=255, extent=(0, W_IMG, H_IMG, 0), interpolation="bicubic", alpha=0.6)
    fam = comparaisons[cible]["familles"]
    for nom, (c, ls, gen) in styles.items():
        if "super" in nom:
            continue
        x, y = gen(fam[nom]["parametres"])
        ax.plot(np.append(x, x[0]), np.append(y, y[0]), color=c, ls=ls, lw=1.8, label=f"{nom.split(' (')[0]} : RMS {fam[nom]['rms_px']:.2f} px".replace(".", ","))
    pts = np.array(comparaisons[cible]["points_px"])
    ax.plot(pts[:, 0], pts[:, 1], "o", color="k", ms=3.5, mfc="yellow", label=f"points de contour numérisés ({len(pts)})")
    if ligne == 0:
        ax.plot(poles_x, poles_y, "*", color="k", ms=13, mfc="cyan", label="pôles dessinés (mesurés à part, non utilisés dans l'ajustement)")
    ax.set_xlim(fenetre[0], fenetre[1])
    ax.set_ylim(fenetre[2], fenetre[3])
    ax.set_title(f"({'a' if ligne == 0 else 'c'}) {'grand contour E1 (enveloppe des anneaux)' if ligne else cible} — rapport d'axes mesuré : {comparaisons[cible]['rapport_d_axes_mesure']:.2f}".replace(".", ","), fontsize=10)
    ax.legend(fontsize=7.6, loc="lower right" if ligne == 0 else "lower center", ncol=1 if ligne == 0 else 2, framealpha=0.95)
    ax.grid(False)
    ax.set_xlabel("x [px]")
    ax.set_ylabel("y [px]")
    ax = axes[ligne, 1]
    noms = list(fam.keys())
    vals = [fam[n]["rms_px"] for n in noms]
    ax.barh(range(len(noms)), vals, color=[styles[n][0] for n in noms])
    ax.axvline(SIGMA_NUM, color="k", lw=1, ls="--")
    ax.text(SIGMA_NUM * 1.05, len(noms) - 0.55, f"incertitude de numérisation ≈ {SIGMA_NUM:g} px", fontsize=8)
    ax.set_yticks(range(len(noms)))
    ax.set_yticklabels([n.split(" (")[0].replace(", axe", ",\naxe").replace(" de deux", "\nde deux").replace(" des deux", "\ndes deux") + f"\n[{fam[n]['n_parametres']} par.]" for n in noms], fontsize=7.8)
    for i, (n_, v) in enumerate(zip(noms, vals)):
        suffixe = f" ; pôles : {fam[n_]['erreur_aux_poles_px']:.1f} px" if ligne == 0 else ""
        ax.text(v * 1.05, i, (f"{v:.2f} px" + suffixe).replace(".", ","), va="center", fontsize=8.3)
    ax.set_xscale("log")
    ax.set_xlim(0.2, max(vals) * (12 if ligne == 0 else 3))
    ax.set_xlabel("résidu RMS entre les points de contour et la courbe ajustée [px]")
    ax.set_title(("(b) RMS sur les arcs (peu discriminant) et erreur aux pôles (discriminante)" if ligne == 0
                  else "(d) Qualité d'ajustement géométrique (plus petit = meilleur)"), fontsize=9.5)
    ax.grid(axis="y", visible=False)
cc.titre(fig, f"S08 — Contours fermés ajustés par des familles de surfaces physiques et par une ellipse générique — {DESIGNATION.split(' (')[0]}\n"
              "résultat descriptif : le sphéroïde central est déclaré « not to scale » par le document")
cc.sauver_figure(fig, FIG / f"S08_fig2_familles_physiques{SUFFIXE}.png", rect=(0, 0.03, 1, 0.93))

# --- Figure 3 : entonnoir, anneaux, méridiens --------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(16, 10.5))
ax = axes[0, 0]
ax.errorbar(x_com, R_moy, yerr=SIGMA_R, fmt="o", color="k", ms=3.5, lw=0.8, capsize=2, label=f"profil numérisé (moyenne haut/bas, ±{SIGMA_R} px)".replace(".", ","))
cols_f = [col["bleu"], col["rouge"], col["ciel"], col["orange"], col["vert"], col["violet"], col["gris"]]
for (nom, d), c in zip(entonnoir.items(), cols_f):
    ax.plot(x_com, d["courbe"], color=c, lw=1.6, ls="--" if "témoin" in nom else "-", label=f"{nom.split(' : ')[0]} ({d['n_parametres']} par.) : RMS {d['rms_px']:.1f} px".replace(".", ","))
ax.axvline(X_GORGE, color="k", ls=":", lw=1)
ax.set_xlabel("x [px] le long de l'axe")
ax.set_ylabel("rayon R(x) de la courbe en entonnoir [px]")
ax.set_ylim(20, 110)
ax.set_title("(a) Profil de l'« entonnoir » entre les grands anneaux, et familles ajustées", fontsize=10)
ax.legend(fontsize=7.3, loc="upper center", ncol=2)
ax = axes[0, 1]
noms_f = [n.split(" : ")[0] for n in entonnoir]
ax.barh(range(len(noms_f)), [d["chi2_reduit"] for d in entonnoir.values()], color=cols_f)
ax.axvline(1.0, color="k", lw=1)
ax.text(1.05, len(noms_f) - 0.55, "χ² réduit = 1 (compatible)", fontsize=8)
ax.set_xscale("log")
ax.set_yticks(range(len(noms_f)))
ax.set_yticklabels([n.replace(" (", "\n(") for n in noms_f], fontsize=8)
ax.set_xlabel(f"χ² réduit (incertitude de numérisation σ = {SIGMA_R} px)".replace(".", ","))
ax.set_title("(b) Aucune famille symétrique n'ajuste le profil ; le témoin asymétrique, si", fontsize=10)
ax.grid(axis="y", visible=False)
ax = axes[1, 0]
uu = np.linspace(-1, 1, 400)
ax.plot(uu, np.sqrt(1 - uu**2), color=col["orange"], lw=2, label="ellipse E1 ajustée aux 12 sommets : R/B = sqrt(1 − u²)")
for (nom, v), c in zip(table_anneaux.items(), (col["rouge"], col["vert"], col["bleu"], col["rouge"], col["vert"], col["bleu"])):
    ax.errorbar(v["position_relative"], v["demi_hauteur_mesuree_px"] / ext["b"], yerr=1.5 / ext["b"], fmt="o", color=c, ms=7, capsize=3)
    ax.annotate(nom.split(" (")[0].replace("anneau ", ""), (v["position_relative"], v["demi_hauteur_mesuree_px"] / ext["b"]), textcoords="offset points", xytext=(6, 6), fontsize=8.5)
ax.set_xlabel("position de l'anneau le long de l'axe, u = (x − X₀)/A")
ax.set_ylabel("rayon de l'anneau / B")
ax.set_title(f"(c) Sommets des six anneaux et ellipse E1 ajustée (RMS {rms_E1_sommets:.1f} px ; validation croisée par paires : erreur maximale {erreur_croisee_max:.1f} px)".replace(".", ","), fontsize=9.5)
ax.legend(fontsize=8.5, loc="lower center")
ax = axes[1, 1]
ax.plot(largeurs, prof_mer, color=col["gris"], lw=0.8)
ax.plot(largeurs, lis, color="k", lw=1.5, label="noirceur moyenne le long du demi-méridien (lissée)")
for s in pics_mer:
    ax.axvline(s, color=col["violet"], lw=1, ls=":")
ax.axhline(FOND, color=col["gris"], ls="--", lw=1)
ax.text(largeurs[0], FOND * 1.05, "fond", color=col["gris"], fontsize=8)
ax.set_xlabel("demi-largeur signée du méridien par rapport à la ligne des pôles [px]")
ax.set_ylabel("noirceur moyenne")
ax.set_title(f"(d) Sphéroïde « fil de fer » : {len(pics_mer)} méridiens détectés (traits violets)", fontsize=10)
ax.legend(fontsize=8.5, loc="upper left")
cc.titre(fig, f"S08 — Profil de l'entonnoir, alignement des anneaux et méridiens du sphéroïde central — {DESIGNATION.split(' (')[0]}")
cc.sauver_figure(fig, FIG / f"S08_fig3_entonnoir_anneaux{SUFFIXE}.png", rect=(0, 0.03, 1, 0.94))

# --- Figure 4 : méthode abandonnée (score de noirceur) ---------------------------------------------
fig, (ax, axb) = plt.subplots(1, 2, figsize=(16.5, 7.6), gridspec_kw={"width_ratios": [1.3, 1]})
ax.imshow(img, cmap="gray", vmin=0, vmax=255, extent=(0, W_IMG, H_IMG, 0), interpolation="bicubic", alpha=0.75)
_styles4 = {"ellipse générique": (col["orange"], "-", fam_ellipse), "ergosurface de Kerr, axe de rotation vertical": (col["rouge"], "--", fam_ergosurface),
            "ergosurface de Kerr, axe de rotation horizontal": (col["gris"], "--", fam_ergosurface_h),
            "horizon de Kerr, axe vertical (rapport d'axes ≤ √2)": (col["bleu"], "-.", fam_horizon),
            "équipotentielle de deux masses (écartement libre)": (col["vert"], "-", fam_equipotentielle)}
_fc = methode_abandonnee["cibles"]["sphéroïde central (enveloppe)"]["familles"]
for _nom, _f in _fc.items():
    _c, _ls, _gen = _styles4[_nom]
    _x, _y = _gen(np.array(_f["parametres"]))
    ax.plot(np.append(_x, _x[0]), np.append(_y, _y[0]), color=_c, ls=_ls, lw=2.0,
            label=f"{_nom.split(' (')[0]} : score ×{_f['score_rapporte_a_l_ellipse']:.2f} ; à {_f['rms_distance_aux_points_du_contour_px']:.1f} px du contour".replace(".", ","))
ax.plot(pts_cen[:, 0], pts_cen[:, 1], "o", color="k", ms=3.5, mfc="yellow", label=f"points du contour extérieur du sphéroïde ({len(pts_cen)})")
ax.set_xlim(80, 210)
ax.set_ylim(196, 100)
ax.set_xlabel("x [px du repère de référence]")
ax.set_ylabel("y [px]")
ax.legend(fontsize=7.8, loc="upper center", bbox_to_anchor=(0.5, -0.13), framealpha=0.95, ncol=2)
ax.grid(False)
ax.set_title("(a) Sphéroïde central : courbes qui maximisent la noirceur moyenne le long de leur tracé", fontsize=10)
_barres = [(f"{'sph.' if 'sph' in _cib else 'E1'} : " + _n.split(",")[0].split(" (")[0].replace(" de deux masses", "").replace(" de Kerr", "").replace(" générique", "")
            + (" (axe horiz.)" if "horizontal" in _n else ""), _f["score_rapporte_a_l_ellipse"], _f["rms_distance_aux_points_du_contour_px"], _styles4[_n][0])
           for _cib, _m in methode_abandonnee["cibles"].items() for _n, _f in _m["familles"].items()]
_yb = np.arange(len(_barres))[::-1]
axb.barh(_yb + 0.2, [b_[1] for b_ in _barres], 0.38, color=col["bleu"], label="score de noirceur / score de l'ellipse (axe du bas)")
axb.axvline(1.0, color=col["bleu"], ls=":", lw=1.2)
axb2 = axb.twiny()
axb2.barh(_yb - 0.2, [b_[2] for b_ in _barres], 0.38, color=col["rouge"], label="distance RMS aux points du contour [px] (axe du haut)")
axb.set_yticks(_yb)
axb.set_yticklabels([b_[0] for b_ in _barres], fontsize=8.5)
axb.set_xlabel("score de noirceur rapporté à celui de l'ellipse", color=col["bleu"])
axb2.set_xlabel("distance RMS aux points du contour [px]", color=col["rouge"])
axb2.grid(False)
axb.grid(axis="y", visible=False)
_h1, _l1 = axb.get_legend_handles_labels()
_h2, _l2 = axb2.get_legend_handles_labels()
axb.legend(_h1 + _h2, _l1 + _l2, fontsize=7.8, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=1)
axb.set_title("(b) Les deux cibles : un bon score n'implique pas de suivre le contour", fontsize=10, pad=34)
cc.titre(fig, f"S08 — Méthode abandonnée (score de noirceur), conservée pour reproductibilité — {DESIGNATION.split(' (')[0]}")
cc.sauver_figure(fig, FIG / f"S08_fig4_methode_abandonnee{SUFFIXE}.png", rect=(0, 0.04, 1, 0.92))

# ---------------------------------------------------------------------------
# 12. Résultats
# ---------------------------------------------------------------------------
for d in entonnoir.values():
    d.pop("courbe")
resultats = {
    "simulation": "S08_reconstitution_doc009",
    "copie_analysee": {"cle": COPIE, "designation": DESIGNATION, **RECALAGE},
    "avertissement": cc.MENTION,
    "source": {"fichier": RECALAGE["fichier"], "repere_de_travail_px": [W_IMG, H_IMG],
               "nature": "copie secondaire ; DOC-009 ne porte aucune cote ; la variante DOC-014 (attribution non établie) porte quatre distances en mètres ; "
                         "les deux états portent « This area is not to scale » au-dessus du sphéroïde central"},
    "axe": {"pente": PENTE_AXE, "inclinaison_deg": float(np.degrees(INCLINAISON)), "ordonnee_a_l_origine_px": ORD_AXE},
    "noirceur_moyenne_du_fond": FOND,
    "ellipses_numerisees_px": ellipses,
    "singularites": {"x_px": x_sing, "separation_px": SEP_SING},
    "proportions_relatives": proportions,
    "cotes_doc014": cotes_doc014,
    "grand_contour_E1_par_les_sommets_des_anneaux": E1,
    "validation_croisee_des_anneaux_par_paires": {"table": croisee, "erreur_max_px": erreur_croisee_max, "erreur_rms_px": erreur_croisee_rms},
    "anneaux_sur_grande_ellipse": {"table": table_anneaux, "rms_fraction_de_B": float(np.sqrt(np.mean(res_anneaux**2))),
                                   "ellipse_par_les_12_sommets": {"cx": fit12.x[0], "cy": fit12.x[1], "A": fit12.x[2], "B": fit12.x[3], "rms_relatif": rms12},
                                   "centre_du_systeme_d_anneaux_px": centre_anneaux},
    "envergures_vs_rayons_de_kerr": kerr_rayons,
    "courbes_fermees_vs_familles_physiques": comparaisons,
    "test_des_poles_spheroide_central": test_poles,
    "methode_abandonnee_score_de_noirceur": methode_abandonnee,
    "meridiens_du_spheroide": {"x_ligne_des_poles_px": x_poles, "demi_largeurs_px": pics_mer, "nombre": len(pics_mer),
                               "ecarts_successifs_px": np.diff(pics_mer).tolist()},
    "entonnoir": {"asymetrie": asym, "sigma_numerisation_px": SIGMA_R, "familles": entonnoir},
    "verdict": verdict,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / f"S08_resultats{SUFFIXE}.json", resultats)
with open(RES / f"S08_ellipses_numerisees{SUFFIXE}.csv", "w", encoding="utf-8") as f:
    f.write("element,cx_px,cy_px,demi_axe_horizontal_px,demi_axe_vertical_px,score_noirceur,cx_sur_A,demi_axe_h_sur_A,demi_axe_v_sur_A\n")
    for nom, e in ellipses.items():
        f.write(f"\"{nom}\",{e['cx']:.2f},{e['cy']:.2f},{e['a']:.2f},{e['b']:.2f},{e['score']:.4f},{(e['cx'] - ext['cx']) / A_REF:.4f},{e['a'] / A_REF:.4f},{e['b'] / A_REF:.4f}\n")
print(f"  résultats : {RES / f'S08_ellipses_numerisees{SUFFIXE}.csv'}")

if COPIE != "reference":
    _b = val.bilan()
    print(f"  Bilan des contrôles S08 [{COPIE}] : {_b['n_passes']}/{_b['n_tests']} tests de méthode passés ; {_b['n_hors_decompte']} contrôles ou résultats hors décompte")
    print(f"S08 [{COPIE}] terminé.")
    sys.exit(0)

# ---------------------------------------------------------------------------
# 13. Mêmes mesures sur la meilleure copie de DOC-009 (PT3.jpg) et sur la variante cotée DOC-014
# ---------------------------------------------------------------------------
# Demande de la phase 7 : les conclusions de S08 changent-elles sur de meilleures copies ?
print("S08 — relance sur les autres copies")
jeux = {"reference": resultats}
relances = {}
for _cle in ("pt3", "doc014"):
    if not COPIES[_cle]["fichier"].exists():
        relances[_cle] = {"execute": False, "motif": "fichier absent de 01_archive/copies_alternatives"}
        print(f"  [{_cle}] copie absente : relance impossible (limite consignée)")
        continue
    _proc = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--copie", _cle], capture_output=True, text=True)
    for _ligne in _proc.stdout.splitlines():
        if any(m in _ligne for m in ("recalage", "ÉCHEC]", "Bilan des contrôles", "figure :")):
            print(f"    [{_cle}] {_ligne.strip()}")
    if _proc.returncode != 0:
        relances[_cle] = {"execute": False, "motif": f"échec d'exécution : {_proc.stderr.strip().splitlines()[-1] if _proc.stderr.strip() else 'inconnu'}"}
        print(f"  [{_cle}] ÉCHEC D'EXÉCUTION : {relances[_cle]['motif']}")
        continue
    jeux[_cle] = cc.lire_json(RES / f"S08_resultats_{_cle}.json")
    relances[_cle] = {"execute": True, **jeux[_cle]["copie_analysee"]}


def _indicateurs(r):
    cf = r["courbes_fermees_vs_familles_physiques"]
    cen_, ext_ = cf["sphéroïde central (enveloppe)"], cf["grande ellipse extérieure"]
    tp = r["test_des_poles_spheroide_central"]["erreur_de_prediction_px"]
    ent = r["entonnoir"]["familles"]
    pr = r["proportions_relatives"]
    sym = [v["rms_px"] for k, v in ent.items() if "témoin" not in k and ("libre" in k or "hyperbolo" in k or "sinuso" in k)]
    return {
        "rapport_d_axes_spheroide_central": cen_["rapport_d_axes_mesure"],
        "rapport_d_axes_contour_exterieur": ext_["rapport_d_axes_mesure"],
        "rms_ellipse_spheroide_px": cen_["familles"]["ellipse générique"]["rms_px"],
        "rms_ellipse_contour_exterieur_px": ext_["familles"]["ellipse générique"]["rms_px"],
        "rms_ergosurface_sur_rms_ellipse_contour_exterieur": ext_["familles"]["ergosurface de Kerr, axe de rotation vertical"]["rms_sur_rms_ellipse"],
        "rms_horizon_sur_rms_ellipse_contour_exterieur": ext_["familles"]["horizon de Kerr, axe vertical (rapport d'axes ≤ √2)"]["rms_sur_rms_ellipse"],
        "rms_equipotentielle_libre_sur_rms_ellipse_contour_exterieur": ext_["familles"]["équipotentielle de deux masses (écartement libre)"]["rms_sur_rms_ellipse"],
        "nombre_de_points_du_grand_contour_E1": ext_["n_points"],
        "erreur_aux_poles_ellipse_px": tp["ellipse générique"],
        "erreur_aux_poles_horizon_px": tp["horizon de Kerr, axe vertical (rapport d'axes ≤ √2)"],
        "erreur_aux_poles_ergosurface_px": tp["ergosurface de Kerr, axe de rotation vertical"],
        "erreur_aux_poles_equipotentielle_libre_px": tp["équipotentielle de deux masses (écartement libre)"],
        "anneaux_validation_croisee_erreur_max_px": r["validation_croisee_des_anneaux_par_paires"]["erreur_max_px"],
        "anneaux_rms_des_12_sommets_sur_E1_px": r["grand_contour_E1_par_les_sommets_des_anneaux"]["rms_sommets_px"],
        "second_contour_E2_contraste": pr["second_grand_contour_E2"]["contraste_sur_fond"],
        "second_contour_E2_decalage_sur_A": pr["second_grand_contour_E2"]["decalage_du_centre_vs_E1_sur_A"],
        "second_contour_E2_rapport_d_axes": pr["second_grand_contour_E2"]["rapport_d_axes"],
        "decalage_masses_centre_des_anneaux_sur_A": pr["decalage_masses_vs_centre_des_anneaux_sur_A"],
        "separation_des_singularites_sur_A": pr["separation_des_singularites_sur_A"],
        "rayon_anneaux_negative_sur_A": 0.5 * (pr["rayons_des_anneaux_sur_A"]["anneau G2 (« negative », gauche)"] + pr["rayons_des_anneaux_sur_A"]["anneau D2 (« negative », droite)"]),
        "rayon_anneaux_null_sur_A": 0.5 * (pr["rayons_des_anneaux_sur_A"]["anneau G3 (« null », gauche)"] + pr["rayons_des_anneaux_sur_A"]["anneau D3 (« null », droite)"]),
        "rayon_anneaux_positive_sur_A": 0.5 * (pr["rayons_des_anneaux_sur_A"]["anneau G4 (« positive », gauche)"] + pr["rayons_des_anneaux_sur_A"]["anneau D4 (« positive », droite)"]),
        "entonnoir_rapport_droite_sur_gauche": r["entonnoir"]["asymetrie"]["rapport_droite_sur_gauche"],
        "entonnoir_rms_flamm_px": ent["parabole de Flamm (Schwarzschild) : R0 + (x−x0)²/(4R0)"]["rms_px"],
        "entonnoir_rms_catenoide_ellis_px": ent["caténoïde d'Ellis/Morris-Thorne : R0 cosh((x−x0)/R0)"]["rms_px"],
        "entonnoir_rms_meilleure_courbe_symetrique_libre_px": min(sym),
        "entonnoir_rms_temoin_asymetrique_px": ent["témoin non physique : parabole à deux courbures (gauche ≠ droite)"]["rms_px"],
        "entonnoir_longueur_d_onde_sinusoide_px": abs(ent["sinusoïde : A − B cos(2π(x−x0)/λ)"]["parametres"][3]),
        "nombre_de_meridiens_detectes": r["meridiens_du_spheroide"]["nombre"],
        "score_noirceur_meilleure_famille_physique_sur_ellipse_spheroide": r["methode_abandonnee_score_de_noirceur"]["cibles"]["sphéroïde central (enveloppe)"]["son_score_rapporte_a_l_ellipse"],
        "score_noirceur_meilleure_famille_physique_sur_ellipse_grand_contour": r["methode_abandonnee_score_de_noirceur"]["cibles"]["grande ellipse extérieure"]["son_score_rapporte_a_l_ellipse"],
    }


def _conclusions(i):
    return {
        "deux contours elliptiques de même rapport d'axes (1,45 à 1,75 ; écart < 0,1)": bool(1.45 < i["rapport_d_axes_spheroide_central"] < 1.75 and 1.45 < i["rapport_d_axes_contour_exterieur"] < 1.75
                                                                                             and abs(i["rapport_d_axes_spheroide_central"] - i["rapport_d_axes_contour_exterieur"]) < 0.1),
        "rapport d'axes > √2 (forme d'horizon de Kerr-Schild écartée, à titre descriptif)": bool(min(i["rapport_d_axes_spheroide_central"], i["rapport_d_axes_contour_exterieur"]) > np.sqrt(2)),
        "pôles du sphéroïde : ellipse à moins de 2 px, ergosurface à plus de 4 px": bool(i["erreur_aux_poles_ellipse_px"] < 2.0 and i["erreur_aux_poles_ergosurface_px"] > 4.0),
        "grand contour E1 : l'ergosurface de Kerr n'ajuste pas mieux que l'ellipse": bool(i["rms_ergosurface_sur_rms_ellipse_contour_exterieur"] >= 1.0),
        "grand contour E1 : l'équipotentielle à écartement libre ajuste nettement moins bien que l'ellipse (RMS > 1,5 fois)": bool(i["rms_equipotentielle_libre_sur_rms_ellipse_contour_exterieur"] > 1.5),
        "sommets des six anneaux sur une même ellipse E1 (validation croisée : erreur < 3 px)": bool(i["anneaux_validation_croisee_erreur_max_px"] < 3.0),
        "second grand contour E2 présent (contraste > 1,5), décalé de 0,10 à 0,22 A vers la droite": bool(i["second_contour_E2_contraste"] > 1.5 and 0.10 < i["second_contour_E2_decalage_sur_A"] < 0.22),
        "système d'anneaux décentré de 0,15 à 0,30 A par rapport aux masses": bool(0.15 < i["decalage_masses_centre_des_anneaux_sur_A"] < 0.30),
        "entonnoir asymétrique (rapport droite/gauche > 1,5)": bool(i["entonnoir_rapport_droite_sur_gauche"] > 1.5),
        "profils de Flamm et d'Ellis écartés (RMS > 10 px)": bool(min(i["entonnoir_rms_flamm_px"], i["entonnoir_rms_catenoide_ellis_px"]) > 10.0),
        "témoin asymétrique nettement meilleur que toute courbe symétrique libre (RMS < 60 %)": bool(i["entonnoir_rms_temoin_asymetrique_px"] < 0.6 * i["entonnoir_rms_meilleure_courbe_symetrique_libre_px"]),
        "sinusoïde dégénérée (longueur d'onde > 3 fois l'étendue du profil)": bool(i["entonnoir_longueur_d_onde_sinusoide_px"] > 3 * 198.0),
    }


indic = {k: _indicateurs(v) for k, v in jeux.items()}
concl = {k: _conclusions(v) for k, v in indic.items()}
differences = {c: {k: concl[k][c] for k in concl} for c in concl["reference"] if len({concl[k][c] for k in concl}) > 1}
comparaison_copies = {
    "copies": {k: jeux[k]["copie_analysee"] for k in jeux}, "relances": relances,
    "indicateurs": indic, "conclusions_par_copie": concl,
    "conclusions_qui_different_selon_la_copie": differences,
    "synthese": ((f"Les {len(concl['reference'])} énoncés descriptifs de S08 reçoivent la même réponse sur les {len(jeux)} copies analysées : "
                  f"{sum(concl['reference'].values())} vérifiés, {len(concl['reference']) - sum(concl['reference'].values())} non vérifié(s)"
                  + ("" if all(concl["reference"].values()) else " (" + " ; ".join(k for k, v in concl["reference"].items() if not v) + ")") + ".")
                 if not differences else f"{len(differences)} énoncé(s) sur {len(concl['reference'])} reçoivent une réponse différente selon la copie : " + " ; ".join(differences)),
    "limites": "ancres de l'entonnoir et estimations initiales lues sur la copie de référence, puis affinées automatiquement sur chaque copie (±2 px) ; "
               "recalage par similitude (pas de correction de déformation locale) ; DOC-014 analysé sur la copie timetravel16_07.jpg seulement (OP4.jpg, 460 px, non traitée)",
}
cc.ecrire_json(RES / "S08_comparaison_copies.json", comparaison_copies)
resultats["comparaison_des_copies"] = {"synthese": comparaison_copies["synthese"], "conclusions_qui_different": differences, "fichier": "S08_comparaison_copies.json"}
cc.ecrire_json(RES / "S08_resultats.json", resultats)
print("  " + comparaison_copies["synthese"])

# --- Figure 5 : comparaison des copies ------------------------------------------------------------
_lignes = [
    ("rapport d'axes du sphéroïde central", "rapport_d_axes_spheroide_central", "{:.2f}"), ("rapport d'axes du grand contour E1", "rapport_d_axes_contour_exterieur", "{:.2f}"),
    ("RMS de l'ellipse, sphéroïde [px]", "rms_ellipse_spheroide_px", "{:.2f}"), ("RMS de l'ellipse, grand contour E1 [px]", "rms_ellipse_contour_exterieur_px", "{:.2f}"),
    ("erreur aux pôles : ellipse [px]", "erreur_aux_poles_ellipse_px", "{:.1f}"), ("erreur aux pôles : horizon de Kerr [px]", "erreur_aux_poles_horizon_px", "{:.1f}"),
    ("erreur aux pôles : ergosurface de Kerr [px]", "erreur_aux_poles_ergosurface_px", "{:.1f}"), ("erreur aux pôles : équipotentielle libre [px]", "erreur_aux_poles_equipotentielle_libre_px", "{:.1f}"),
    ("grand contour E1 : nombre de points de contour", "nombre_de_points_du_grand_contour_E1", "{:.0f}"),
    ("grand contour E1 : RMS ergosurface / RMS ellipse", "rms_ergosurface_sur_rms_ellipse_contour_exterieur", "{:.2f}"),
    ("grand contour E1 : RMS équipotentielle libre / RMS ellipse", "rms_equipotentielle_libre_sur_rms_ellipse_contour_exterieur", "{:.2f}"),
    ("anneaux sur E1 : erreur max. de validation croisée [px]", "anneaux_validation_croisee_erreur_max_px", "{:.2f}"),
    ("second grand contour E2 : contraste / décalage [A]", None, None),
    ("rayons des anneaux negative / null / positive [A]", None, None),
    ("décalage masses ↔ centre des anneaux [A]", "decalage_masses_centre_des_anneaux_sur_A", "{:.3f}"), ("séparation des deux singularités [A]", "separation_des_singularites_sur_A", "{:.3f}"),
    ("entonnoir : rapport droite / gauche", "entonnoir_rapport_droite_sur_gauche", "{:.2f}"), ("entonnoir : RMS Flamm / Ellis [px]", None, None),
    ("entonnoir : RMS meilleure courbe symétrique libre [px]", "entonnoir_rms_meilleure_courbe_symetrique_libre_px", "{:.1f}"),
    ("entonnoir : RMS témoin asymétrique [px]", "entonnoir_rms_temoin_asymetrique_px", "{:.1f}"), ("méridiens détectés", "nombre_de_meridiens_detectes", "{:.0f}"),
    ("méthode abandonnée : meilleur score physique / ellipse (sph. ; E1)", None, None),
    ("énoncés descriptifs vérifiés", None, None),
]
_cles = list(jeux)
_cellules = []
for _lib, _k, _fmt in _lignes:
    _row = []
    for _c in _cles:
        _i = indic[_c]
        if _k is not None:
            _row.append(_fmt.format(_i[_k]).replace(".", ","))
        elif "rayons" in _lib:
            _row.append(" / ".join(f"{_i[k]:.2f}".replace(".", ",") for k in ("rayon_anneaux_negative_sur_A", "rayon_anneaux_null_sur_A", "rayon_anneaux_positive_sur_A")))
        elif "abandonnée" in _lib:
            _row.append(f"{_i['score_noirceur_meilleure_famille_physique_sur_ellipse_spheroide']:.2f} ; {_i['score_noirceur_meilleure_famille_physique_sur_ellipse_grand_contour']:.2f}".replace(".", ","))
        elif "E2" in _lib:
            _row.append(f"{_i['second_contour_E2_contraste']:.1f} / {_i['second_contour_E2_decalage_sur_A']:.2f}".replace(".", ","))
        elif "Flamm" in _lib:
            _row.append(f"{_i['entonnoir_rms_flamm_px']:.0f} / {_i['entonnoir_rms_catenoide_ellis_px']:.0f}")
        else:
            _row.append(f"{sum(concl[_c].values())} / {len(concl[_c])}")
    _cellules.append(_row)
fig, ax = plt.subplots(figsize=(14.5, 9.2))
ax.axis("off")
_entetes = {"reference": "DOC-009, référence\n(318×369 px)", "pt3": "DOC-009, PT3.jpg\n(578×799 px)", "doc014": "DOC-014, variante cotée\n(550×594 px)"}
_tab = ax.table(cellText=_cellules, rowLabels=[l[0] for l in _lignes], colLabels=[_entetes[c] for c in _cles], cellLoc="center", loc="center",
                bbox=[0.36, 0.02, 0.62, 0.9])
_tab.auto_set_font_size(False)
_tab.set_fontsize(9)
for (_r, _c_), _cell in _tab.get_celld().items():
    _cell.set_edgecolor("#999999")
    if _r == 0:
        _cell.set_facecolor("#dddddd")
        _cell.set_height(_cell.get_height() * 1.6)
_rec = (f"Recalage : PT3 échelle ×{relances.get('pt3', {}).get('echelle_x', float('nan')):.3f}, corrélation {relances.get('pt3', {}).get('correlation', float('nan')):.3f} ; "
        f"DOC-014 échelle ×{relances.get('doc014', {}).get('echelle_x', float('nan')):.3f}, rotation {relances.get('doc014', {}).get('rotation_deg', float('nan')):+.2f}°, "
        f"corrélation {relances.get('doc014', {}).get('correlation', float('nan')):.3f}").replace(".", ",") + "."
ax.text(0.0, 0.97, "Longueurs exprimées dans le repère de la copie de référence (px) ou en demi-grand axe A du grand contour E1 ; « sph. » = sphéroïde central.\n" + _rec,
        transform=ax.transAxes, fontsize=9, va="top")
cc.titre(fig, "S08 — Les mêmes mesures sur trois copies : DOC-009 (référence et meilleure copie PT3) et sa variante cotée DOC-014")
cc.sauver_figure(fig, FIG / "S08_fig5_comparaison_copies.png", rect=(0, 0.035, 1, 0.93))

val.imprimer_bilan()
print("S08 terminé.")
