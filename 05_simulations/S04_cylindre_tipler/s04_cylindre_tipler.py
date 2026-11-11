# -*- coding: utf-8 -*-
"""S04 — Cylindre de van Stockum / Tipler : fonctions métriques, rayon d'apparition des courbes de
genre temps fermées (CTC), basculement des cônes de lumière, ordres de grandeur d'un cylindre réel.

SIMULATION ILLUSTRATIVE : solution exacte d'un cylindre de poussière INFINI en rotation rigide
(van Stockum 1937 ; Tipler 1974). Elle n'est pas asymptotiquement plate et rien ne montre qu'un
cylindre fini produise des CTC. Ce n'est pas une preuve expérimentale.

Métrique (G = c = 1) :  ds² = H (dr² + dz²) + L dφ² + 2 M dφ dt − F dt²
  intérieur (r < R) : H = exp(−a²r²), L = r²(1 − a²r²), M = a r², F = 1 ; 8πρ = 4a² exp(a²r²)
  extérieur (r > R) : trois branches selon aR < 1/2, = 1/2, > 1/2 (Tipler 1974, éq. 3 à 5).
Paramètres : a [1/longueur] (vitesse angulaire de la poussière, ω = a·c), R (rayon du cylindre).

Exécution :  .venv/bin/python 05_simulations/S04_cylindre_tipler/s04_cylindre_tipler.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402
from matplotlib.patches import Polygon, Patch  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore")
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S04_cylindre_tipler")
col = cc.COULEURS


# ---------------------------------------------------------------------------
# 1. Fonctions métriques
# ---------------------------------------------------------------------------
def fonctions_metriques(r, a, R=1.0, tol=1e-9):
    """Retourne (H, L, M, F) en r (tableau), pour un cylindre de rayon R et de paramètre a."""
    r = np.atleast_1d(np.asarray(r, dtype=float))
    H = np.empty_like(r)
    L = np.empty_like(r)
    Mm = np.empty_like(r)
    F = np.empty_like(r)
    i = r <= R
    H[i] = np.exp(-a**2 * r[i]**2)
    L[i] = r[i]**2 * (1 - a**2 * r[i]**2)
    Mm[i] = a * r[i]**2
    F[i] = 1.0
    e = ~i
    x = r[e]
    aR = a * R
    lg = np.log(x / R)
    H[e] = np.exp(-aR**2) * (x / R)**(-2 * aR**2)
    if abs(aR - 0.5) < tol:                     # cas critique (limite des deux autres branches)
        L[e] = R * x / 4 * (3 + lg)
        Mm[e] = x / 2 * (1 + lg)
        F[e] = x / R * (1 - lg)
    elif aR < 0.5:
        s = np.sqrt(1 - 4 * aR**2)
        eps = np.arctanh(s)
        th = s * lg
        L[e] = R * x * np.sinh(3 * eps + th) / (2 * np.sinh(2 * eps) * np.cosh(eps))
        Mm[e] = x * np.sinh(eps + th) / np.sinh(2 * eps)
        F[e] = x * np.sinh(eps - th) / (R * np.sinh(eps))
    else:
        s = np.sqrt(4 * aR**2 - 1)
        beta = np.arctan(s)
        gam = s * lg
        L[e] = R * x * np.sin(3 * beta + gam) / (2 * np.sin(2 * beta) * np.cos(beta))
        Mm[e] = x * np.sin(beta + gam) / np.sin(2 * beta)
        F[e] = x * np.sin(beta - gam) / (R * np.sin(beta))
    return H, L, Mm, F


def rayon_ctc(aR):
    """Plus petit rayon (en unités de R) où g_φφ = L s'annule puis devient négatif.

    aR ≤ 1/2 : pas de CTC (inf) ; 1/2 < aR < 1 : à l'extérieur, r = R·exp[(π − 3β)/sqrt(4a²R² − 1)] ;
    aR ≥ 1 : à l'intérieur, r = 1/a."""
    if aR <= 0.5:
        return np.inf
    if aR >= 1.0:
        return 1.0 / aR
    s = np.sqrt(4 * aR**2 - 1)
    return float(np.exp((np.pi - 3 * np.arctan(s)) / s))


def vitesses_angulaires_nulles(r, a, R=1.0):
    """dφ/dt des photons azimutaux : L Ω² + 2 M Ω − F = 0 → Ω± = (−M ± r)/L (car M² + F L = r²)."""
    H, L, Mm, F = fonctions_metriques(r, a, R)
    return (-Mm - r) / L, (-Mm + r) / L


# ---------------------------------------------------------------------------
# 2. Validation
# ---------------------------------------------------------------------------
print("S04 — tests de validation")
# 2.1 Raccord C0 et C1 en r = R pour les trois branches
h = 1e-6
for aR in (0.3, 0.5, 0.8, 1.2):
    fi = fonctions_metriques(np.array([1 - 2 * h, 1 - h, 1.0]), aR)
    fe = fonctions_metriques(np.array([1 + 1e-12, 1 + h, 1 + 2 * h]), aR)
    saut = max(abs(fe[k][0] - fi[k][2]) for k in range(4))
    d_int = [(3 * fi[k][2] - 4 * fi[k][1] + fi[k][0]) / (2 * h) for k in range(4)]          # dérivée à gauche (ordre 2)
    d_ext = [(-3 * fe[k][0] + 4 * fe[k][1] - fe[k][2]) / (2 * h) for k in range(4)]         # dérivée à droite
    val.verifier(f"Raccord C0 en r = R (aR = {aR})", saut, 0.0, tol_abs=1e-9)
    val.verifier(f"Raccord C1 en r = R (aR = {aR})", max(abs(de - di) for de, di in zip(d_ext, d_int)), 0.0, tol_abs=1e-4)
# 2.2 Identité M² + F L = r² (déterminant du bloc t-φ)
for aR in (0.3, 0.5, 0.8, 1.2):
    rr = np.linspace(0.05, 30, 4000)
    H, L, Mm, F = fonctions_metriques(rr, aR)
    val.verifier(f"Identité M² + F·L = r² (aR = {aR})", np.max(np.abs(Mm**2 + F * L - rr**2) / rr**2), 0.0, tol_abs=1e-10)
# 2.3 Continuité des trois branches extérieures quand aR → 1/2 (formes 0/0 : sinh ε → 0, sin β → 0).
#     Critère RELATIF (les fonctions valent jusqu'à ~30 en r = 20 R) et test de convergence linéaire
#     en δ = aR − 1/2. (Première version du test : critère absolu de 2e-3, mal posé, en échec à
#     5,6e-3 pour δ = 1e-5 — écart physique d'ordre δ et non instabilité numérique.)
rr = np.array([1.5, 4.0, 20.0])
ref = fonctions_metriques(rr, 0.5)


def ecart_relatif_branche(d):
    f_ = fonctions_metriques(rr, 0.5 + d)
    return max(np.max(np.abs(f_[k] - ref[k]) / np.abs(ref[k])) for k in range(4))


for signe, nom_s in ((-1, "−"), (+1, "+")):
    e4, e6 = ecart_relatif_branche(signe * 1e-4), ecart_relatif_branche(signe * 1e-6)
    val.verifier(f"Branche aR = 1/2 {nom_s} 1e-6 → cas critique (écart relatif)", e6, 0.0, tol_abs=1e-4)
    val.verifier(f"Convergence linéaire en δ (aR = 1/2 {nom_s} δ) : écart(1e-4)/écart(1e-6)", e4 / e6, 100.0, tol_rel=0.2)
# 2.4 Rayon CTC : valeurs limites
val.verifier("r_CTC(aR = 1) = R (raccord intérieur/extérieur)", rayon_ctc(1.0 - 1e-12), 1.0, tol_abs=1e-6)
val.verifier("r_CTC(aR = 2) = R/2 (intérieur : r = 1/a)", rayon_ctc(2.0), 0.5, tol_abs=1e-14)
rr = np.linspace(1.0, 20.0, 400001)
L_num = fonctions_metriques(rr, 0.6)[1]
val.verifier("r_CTC(aR = 0,6) : formule ↔ premier zéro numérique de L(r)", rr[np.argmax(L_num < 0)], rayon_ctc(0.6), tol_rel=1e-4)


# 2.5 Calcul formel : équations d'Einstein
def tenseurs(g, coords):
    """Ricci et scalaire de Ricci (sympy), sans simplification lourde."""
    n = len(coords)
    ginv = g.inv()
    Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                 for l in range(n)) / 2 for k in range(n)] for j in range(n)] for i in range(n)]
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(j, n):
            e = sum(sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k]) for i in range(n))
            e += sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for i in range(n) for l in range(n))
            Ric[j, k] = Ric[k, j] = e
    Rs = sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n))
    return Ric, Rs, ginv


t_, r_, z_, p_ = sp.symbols("t r z phi", real=True)
coords = (t_, r_, z_, p_)


def metrique_sympy(Hs, Ls, Ms, Fs):
    g = sp.zeros(4, 4)
    g[0, 0] = -Fs
    g[0, 3] = g[3, 0] = Ms
    g[3, 3] = Ls
    g[1, 1] = g[2, 2] = Hs
    return g


symb = {}
# Intérieur : G_μν = 8πρ u_μ u_ν avec u = ∂_t, 8πρ = 4a² exp(a²r²)
a_s = sp.Rational(3, 4)
g_int = metrique_sympy(sp.exp(-a_s**2 * r_**2), r_**2 * (1 - a_s**2 * r_**2), a_s * r_**2, sp.Integer(1))
Ric, Rs, _ = tenseurs(g_int, coords)
Ein = (Ric - g_int * Rs / 2).applyfunc(sp.simplify)
rho8pi = 4 * a_s**2 * sp.exp(a_s**2 * r_**2)
u_bas = sp.Matrix([-1, 0, 0, a_s * r_**2])
residu = (Ein - rho8pi * u_bas * u_bas.T).applyfunc(sp.simplify)
symb["interieur_poussiere"] = all(residu[i, j] == 0 for i in range(4) for j in range(4))
val.verifier_vrai("Intérieur : G_μν ≡ 8πρ u_μ u_ν, 8πρ = 4a²exp(a²r²) (calcul formel exact, a = 3/4)", symb["interieur_poussiere"])
# Extérieur : R_μν = 0 (évaluation numérique à 40 chiffres en plusieurs rayons)
Rr = sp.Integer(1)
for nom, aRv in (("aR = 3/10 (< 1/2)", sp.Rational(3, 10)), ("aR = 1/2", sp.Rational(1, 2)), ("aR = 4/5 (> 1/2)", sp.Rational(4, 5))):
    lg = sp.log(r_ / Rr)
    Hs = sp.exp(-aRv**2) * (r_ / Rr)**(-2 * aRv**2)
    if aRv == sp.Rational(1, 2):
        Ls, Ms, Fs = Rr * r_ / 4 * (3 + lg), r_ / 2 * (1 + lg), r_ / Rr * (1 - lg)
    elif aRv < sp.Rational(1, 2):
        s = sp.sqrt(1 - 4 * aRv**2)
        eps = sp.atanh(s)
        th = s * lg
        Ls = Rr * r_ * sp.sinh(3 * eps + th) / (2 * sp.sinh(2 * eps) * sp.cosh(eps))
        Ms = r_ * sp.sinh(eps + th) / sp.sinh(2 * eps)
        Fs = r_ * sp.sinh(eps - th) / (Rr * sp.sinh(eps))
    else:
        s = sp.sqrt(4 * aRv**2 - 1)
        beta = sp.atan(s)
        gam = s * lg
        Ls = Rr * r_ * sp.sin(3 * beta + gam) / (2 * sp.sin(2 * beta) * sp.cos(beta))
        Ms = r_ * sp.sin(beta + gam) / sp.sin(2 * beta)
        Fs = r_ * sp.sin(beta - gam) / (Rr * sp.sin(beta))
    Ric, Rs, _ = tenseurs(metrique_sympy(Hs, Ls, Ms, Fs), coords)
    res_max = 0.0
    for rv in (sp.Rational(3, 2), sp.Integer(5), sp.Integer(40)):
        for i in range(4):
            for j in range(i, 4):
                res_max = max(res_max, abs(float(sp.N(Ric[i, j].subs(r_, rv), 40))))
    symb[f"exterieur_vide_{nom}"] = res_max
    val.verifier(f"Extérieur : R_μν = 0 ({nom}), résidu max. à 40 chiffres", res_max, 0.0, tol_abs=1e-25)

# ---------------------------------------------------------------------------
# 3. Figures
# ---------------------------------------------------------------------------
cas = [(0.3, col["bleu"]), (0.5, col["vert"]), (0.6, col["orange"]), (0.8, col["rouge"]), (1.2, col["violet"])]
r = np.logspace(-1.3, 2, 4000)

# --- Figure 1 : fonctions métriques -------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(13.5, 9.5))
noms = [("H", "$H = g_{rr} = g_{zz}$"), ("L", r"$L/r^2 = g_{\varphi\varphi}/r^2$"), ("M", r"$M/r = g_{t\varphi}/r$"), ("F", "$F = -g_{tt}$")]
for k, (ax, (cle, lab)) in enumerate(zip(axes.ravel(), noms)):
    for aR, c in cas:
        f = fonctions_metriques(r, aR)[k]
        if cle == "L":
            f = f / r**2
        if cle == "M":
            f = f / r
        ax.semilogx(r, f, color=c, lw=1.8, label=f"aR = {aR}".replace(".", ","))
    ax.axvline(1.0, color="k", lw=1, ls=":")
    ax.axhline(0.0, color="k", lw=0.8)
    ax.set_xlabel("r / R")
    ax.set_ylabel(lab)
    ax.set_title(lab)
    if cle in ("L", "F"):
        ax.set_ylim(-3, 3)
        ax.axhspan(-3, 0, color=col["rouge"], alpha=0.07)
        ax.text(0.055, -2.6, "L < 0 : ∂φ de genre temps → CTC" if cle == "L" else "F < 0 : ∂t de genre espace (pas de CTC à lui seul)", fontsize=8.5, color=col["rouge"])
    if cle == "M":
        ax.set_ylim(-6, 6)
    if cle == "H":
        ax.set_yscale("log")
    ax.text(1.05, ax.get_ylim()[1] * (0.5 if cle == "H" else 0.86), "surface du cylindre", fontsize=8, rotation=90, va="top")
axes[0, 0].legend(fontsize=8.5, loc="lower left")
cc.titre(fig, "S04 — Cylindre de van Stockum-Tipler : fonctions métriques intérieures et extérieures pour plusieurs valeurs de aR")
cc.sauver_figure(fig, FIG / "S04_fig1_fonctions_metriques.png", rect=(0, 0.03, 1, 0.94))

# --- Figure 2 : domaine des CTC ---------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 6))
aR_g = np.linspace(0.05, 2.0, 500)
r_g = np.logspace(-1, 4, 900)
Z = np.zeros((len(aR_g), len(r_g)))
for i, aR in enumerate(aR_g):
    H, L, Mm, F = fonctions_metriques(r_g, aR)
    Z[i] = np.where(L < 0, 2, np.where(F < 0, 1, 0))
cmap = plt.matplotlib.colors.ListedColormap(["#f7f7f7", "#a6cee3", "#e31a1c"])
ax1.pcolormesh(r_g, aR_g, Z, cmap=cmap, vmin=-0.5, vmax=2.5, shading="auto")
ax1.set_xscale("log")
aR_c = np.linspace(0.5001, 2.0, 600)
ax1.plot([rayon_ctc(x) for x in aR_c], aR_c, color="k", lw=2, label="rayon d'apparition des CTC (formule analytique)")
ax1.axvline(1.0, color="k", lw=1, ls=":")
ax1.axhline(0.5, color=col["vert"], lw=1.5, ls="--")
ax1.axhline(1.0, color=col["violet"], lw=1.5, ls="--")
ax1.text(0.11, 0.52, "aR = 1/2 : seuil d'existence des CTC (extérieur)", color=col["vert"], fontsize=8.5)
ax1.text(0.11, 1.02, "aR = 1 : CTC dès la surface, puis à l'intérieur (r > 1/a)", color=col["violet"], fontsize=8.5)
ax1.set_xlabel("r / R")
ax1.set_ylabel("aR  (« vitesse de surface » en unités de c)")
ax1.set_xlim(0.1, 1e4)
ax1.legend(handles=[Patch(fc="#e31a1c", label="$g_{\\varphi\\varphi}$ = L < 0 : CTC"), Patch(fc="#a6cee3", label="F < 0 seulement"),
                    plt.Line2D([], [], color="k", lw=2, label="rayon d'apparition des CTC (analytique)")], loc="upper right", fontsize=8.5)
ax1.set_title("(a) Domaine des CTC dans le plan (r/R, aR)")
ax1.grid(False)

ax2.semilogy(aR_c, [rayon_ctc(x) for x in aR_c], color=col["rouge"], lw=2)
ax2.axvline(0.5, color=col["vert"], lw=1.5, ls="--")
ax2.axvline(1.0, color=col["violet"], lw=1.5, ls="--")
for x in (0.51, 0.55, 0.6, 0.8, 1.0, 1.5):
    ax2.plot(x, rayon_ctc(x), "o", color="k", ms=4)
    ax2.annotate(f"{rayon_ctc(x):.3g}".replace(".", ","), (x, rayon_ctc(x)), textcoords="offset points", xytext=(6, 5), fontsize=8)
ax2.set_xlabel("aR")
ax2.set_ylabel("$r_{CTC}$ / R")
ax2.set_ylim(0.3, 1e7)
ax2.set_title("(b) Rayon d'apparition des CTC : diverge quand aR → 1/2⁺\n$r_{CTC} = R\\,\\exp[(\\pi - 3\\beta)/\\sqrt{4a^2R^2-1}]$, tan β = $\\sqrt{4a^2R^2-1}$", fontsize=10)
cc.titre(fig, "S04 — Cylindre de van Stockum-Tipler : où apparaissent les courbes de genre temps fermées ?")
cc.sauver_figure(fig, FIG / "S04_fig2_domaine_ctc.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : cônes de lumière --------------------------------------------------------------


def dessiner_cone(ax, x0, y0, g_tt, g_tp, g_pp, taille=0.4):
    R_ = np.sqrt(abs(g_pp)) if g_pp != 0 else 1.0
    alpha = np.linspace(0, 2 * np.pi, 1441)
    dphi = np.cos(alpha) / R_
    dt = np.sin(alpha)
    q = g_tt * dt**2 + 2 * g_tp * dt * dphi + g_pp * dphi**2
    temps = q < 0
    idx = np.where(np.diff(temps.astype(int)) != 0)[0]
    bornes = np.concatenate([[0], idx + 1, [len(alpha) - 1]])
    for i0, i1 in zip(bornes[:-1], bornes[1:]):
        if temps[i0:i1].all() and i1 - i0 > 1:
            al = alpha[i0:i1 + 1]
            pts = np.column_stack([np.concatenate([[x0], x0 + taille * np.cos(al)]), np.concatenate([[y0], y0 + taille * np.sin(al)])])
            futur = np.mean(np.sin(al)) > 0
            ax.add_patch(Polygon(pts, closed=True, fc=col["orange"] if futur else col["ciel"], ec="k", lw=0.6, alpha=0.9))


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.8), gridspec_kw={"width_ratios": [1.25, 1]})
aR_cone = 1.2
rayons = [0.15, 0.4, 0.6, 0.75, 0.8333, 0.9, 1.0, 1.3, 2.0]
for x0, rv in enumerate(rayons):
    H, L, Mm, F = [f[0] for f in fonctions_metriques(rv, aR_cone)]
    dessiner_cone(ax1, x0, 0.0, -F, Mm, L)
    ax1.text(x0, -0.6, f"r = {rv:.2f} R".replace(".", ","), ha="center", fontsize=8, rotation=45, va="top")
    if L < 0:
        ax1.text(x0, 0.55, "CTC", ha="center", color=col["rouge"], weight="bold", fontsize=9)
ax1.axhline(0, color=col["gris"], lw=0.6)
ax1.axvline(4.0, color=col["rouge"], lw=1, ls="--")
ax1.text(4.05, 0.78, "r = 1/a : $g_{\\varphi\\varphi}$ = 0, la direction φ devient lumière", fontsize=8.5, color=col["rouge"])
ax1.axvline(6.0, color="k", lw=1, ls=":")
ax1.text(6.05, -0.95, "surface r = R", fontsize=8.5)
ax1.set_xlim(-0.7, len(rayons) - 0.3)
ax1.set_ylim(-1.0, 0.95)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_xlabel("abscisse locale de chaque cône : déplacement azimutal propre →   (orange : futur ; bleu : passé)")
ax1.set_ylabel("ordonnée locale : dt ↑")
ax1.set_title(f"(a) Basculement des cônes de lumière dans le plan (φ, t), aR = {aR_cone}".replace(".", ","))
ax1.grid(False)

for aR, c in ((0.3, col["bleu"]), (0.8, col["rouge"]), (1.2, col["violet"])):
    rr = np.linspace(0.02, 3.0, 3000)
    Om_m, Om_p = vitesses_angulaires_nulles(rr, aR)
    for Om, ls in ((Om_p, "-"), (Om_m, "--")):
        Om = np.where(np.abs(Om) > 40, np.nan, Om)
        ax2.plot(rr, Om, color=c, ls=ls, lw=1.6, label=(f"aR = {aR}".replace(".", ",") + (" : $\\Omega_+$" if ls == "-" else " : $\\Omega_-$")))
ax2.axhline(0, color="k", lw=0.8)
ax2.axvline(1.0, color="k", lw=1, ls=":")
ax2.set_ylim(-12, 12)
ax2.set_xlabel("r / R")
ax2.set_ylabel(r"$\Omega_\pm = d\varphi/dt$ des photons azimutaux  [c/R]")
ax2.set_title("(b) $\\Omega_\\pm = (-M \\pm r)/L$ : $\\Omega_-$ diverge puis change de signe là où L = 0")
ax2.title.set_fontsize(9.5)
ax2.legend(fontsize=8, ncol=3, loc="lower center")
cc.titre(fig, "S04 — Cylindre de van Stockum-Tipler : basculement des cônes de lumière jusqu'à englober la direction azimutale")
cc.sauver_figure(fig, FIG / "S04_fig3_cones_lumiere.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 4. Ordres de grandeur d'un cylindre « réel » (SI)
# ---------------------------------------------------------------------------
# Relations (re-dérivées) :  ω = a c ;  densité sur l'axe ρ0 = a²c²/(2πG) = ω²/(2πG) ;
# densité à la surface ρ(R) = ρ0 exp(a²R²) ; masse propre par unité de longueur
# μ = ∫ρ dV_propre = a²R² c²/(2G)  (indépendante de R à aR fixé).
RHO_NUCLEAIRE = 2.3e17      # kg/m³ (ordre de grandeur de la densité de saturation nucléaire)
MU_SEUIL = cc.C**2 / (8 * cc.G)


def cylindre(R_m, aR, longueur_m):
    omega = aR * cc.C / R_m
    rho0 = omega**2 / (2 * np.pi * cc.G)
    mu = aR**2 * cc.C**2 / (2 * cc.G)
    return {"R_m": R_m, "aR": aR, "longueur_m": longueur_m, "omega_rad_s": omega, "frequence_Hz": omega / (2 * np.pi),
            "densite_axe_kg_m3": rho0, "densite_surface_kg_m3": rho0 * np.exp(aR**2),
            "densite_axe_sur_nucleaire": rho0 / RHO_NUCLEAIRE, "masse_lineique_kg_m": mu,
            "masse_totale_kg": mu * longueur_m, "masse_totale_masses_solaires": mu * longueur_m / cc.M_SOLEIL,
            "masse_totale_masses_terrestres": mu * longueur_m / cc.M_TERRE,
            "r_ctc_m": rayon_ctc(aR) * R_m}


exemples = {
    "Tipler 1974 (R = 10 km, L = 100 km, aR = 1/2 : seuil)": cylindre(1e4, 0.5, 1e5),
    "R = 10 km, L = 100 km, aR = 0,6 (CTC à ~8 R)": cylindre(1e4, 0.6, 1e5),
    "échelle C204 (R = 0,1 m, L = 1 m, aR = 0,6)": cylindre(0.1, 0.6, 1.0),
    "échelle C204 (R = 0,1 m, L = 1 m, aR = 1)": cylindre(0.1, 1.0, 1.0),
}
M_unite = cc.REVENDICATIONS["masse_unite_kg"]
aR_227 = np.sqrt(2 * cc.G * M_unite / 1.0 / cc.C**2)      # aR d'un cylindre de 227 kg par mètre
exemples_227 = {"masse_lineique_kg_m": M_unite, "aR_obtenu": aR_227, "aR_requis": 0.5, "rapport_aR": 0.5 / aR_227,
                "rapport_de_masse_requis": MU_SEUIL / M_unite}
val.verifier("Tipler 1974 : densité sur l'axe pour R = 10 km, aR = 1/2 ≈ 5e17 kg/m³ (~1e14 g/cm³ cité : ordre de grandeur)",
             np.log10(exemples["Tipler 1974 (R = 10 km, L = 100 km, aR = 1/2 : seuil)"]["densite_axe_kg_m3"]), 17.5, tol_abs=0.6)
# masse linéique : intégrale numérique de ρ dV_propre ↔ formule fermée
rr = np.linspace(0, 1, 200001)
a_num = 0.8
mu_num = np.trapezoid((a_num**2 / (2 * np.pi)) * np.exp(a_num**2 * rr**2) * np.exp(-a_num**2 * rr**2) * 2 * np.pi * rr, rr)
val.verifier("Masse propre par unité de longueur : intégrale numérique ↔ a²R²/2 (G = c = 1)", mu_num, a_num**2 / 2, tol_rel=1e-8)

# --- Figure 4 : ordres de grandeur -----------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.8))
Rm = np.logspace(-2, 5, 200)
for aR, c in ((0.5, col["vert"]), (1.0, col["violet"])):
    ax1.loglog(Rm, (aR * cc.C / Rm)**2 / (2 * np.pi * cc.G), color=c, lw=2, label=f"densité sur l'axe, aR = {aR}".replace(".", ","))
for y, nom, c in ((RHO_NUCLEAIRE, "matière nucléaire (2,3×10¹⁷ kg/m³)", col["rouge"]), (2.2e4, "osmium (2,2×10⁴ kg/m³)", col["gris"]),
                  (1e9, "naine blanche (~10⁹ kg/m³)", col["bleu"])):
    ax1.axhline(y, color=c, ls=":", lw=1.3)
    ax1.text(1.2e-2, y * 2, nom, color=c, fontsize=8.5)
ax1.axvline(0.1, color=col["orange"], ls="--", lw=1.2)
ax1.text(0.115, 3e12, "échelle d'un coffre\n(R = 0,1 m)", color=col["orange"], fontsize=8.5)
ax1.axvline(1e4, color="k", ls="--", lw=1.2)
ax1.text(9e3, 3e12, "exemple de Tipler\n(R = 10 km)", fontsize=8.5, ha="right")
ax1.set_xlabel("rayon du cylindre R [m]")
ax1.set_ylabel("densité requise ρ₀ = (aRc/R)² / (2πG)  [kg/m³]")
ax1.set_title("(a) Densité requise en fonction du rayon")
ax1.legend(fontsize=8.5, loc="upper right")

aRs = np.logspace(-13.5, 0.3, 300)
ax2.loglog(aRs, aRs**2 * cc.C**2 / (2 * cc.G), color="k", lw=2, label="μ = a²R²c²/(2G)")
ax2.axvline(0.5, color=col["vert"], lw=1.5, ls="--")
ax2.plot(0.5, MU_SEUIL, "o", color=col["vert"])
ax2.annotate(f"seuil des CTC : aR = 1/2\nμ = c²/(8G) = {cc.sci(MU_SEUIL)} kg/m\n(≈ {MU_SEUIL / cc.M_TERRE:.0f} masses terrestres par mètre)", (0.5, MU_SEUIL),
             textcoords="offset points", xytext=(-235, -42), fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
ax2.plot(aR_227, M_unite, "o", color=col["bleu"])
ax2.annotate(f"227 kg par mètre :\naR = {cc.sci(aR_227, 2)}", (aR_227, M_unite), textcoords="offset points", xytext=(14, -28), fontsize=8.5, color=col["bleu"])
ax2.annotate("", xy=(0.5, M_unite), xytext=(aR_227, M_unite), arrowprops=dict(arrowstyle="<->", color=col["rouge"], lw=1.5))
ax2.text(1e-6, M_unite * 12, f"écart : ×{cc.sci(0.5 / aR_227, 2)} en aR, ×{cc.sci(MU_SEUIL / M_unite, 2)} en masse", color=col["rouge"], fontsize=9, ha="center")
ax2.set_xlabel("aR  (« vitesse de surface » / c)")
ax2.set_ylabel("masse par unité de longueur μ [kg/m]")
ax2.set_title("(b) Masse linéique requise (indépendante de R)")
ax2.legend(fontsize=8.5, loc="upper left")
cc.titre(fig, "S04 — Ordres de grandeur d'un cylindre de Tipler « réel » : densité et masse linéique requises")
cc.sauver_figure(fig, FIG / "S04_fig4_ordres_de_grandeur.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 5. Résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S04_cylindre_tipler",
    "avertissement": cc.MENTION,
    "rayon_ctc_sur_R": {f"aR={x}": rayon_ctc(x) for x in (0.5, 0.51, 0.55, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0)},
    "seuil_ctc": {"aR_min_exterieur": 0.5, "aR_min_interieur": 1.0, "masse_lineique_seuil_kg_m": MU_SEUIL,
                  "masse_lineique_seuil_masses_terrestres_par_m": MU_SEUIL / cc.M_TERRE},
    "exemples_SI": exemples,
    "cylindre_227_kg_par_metre": exemples_227,
    "verification_symbolique": symb,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S04_resultats.json", resultats)
val.imprimer_bilan()
print("S04 terminé.")
