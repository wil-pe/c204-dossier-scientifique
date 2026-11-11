# -*- coding: utf-8 -*-
"""S02 — Géométrie de Kerr et de Kerr-Newman : horizons, ergosphère, entraînement des référentiels,
basculement des cônes de lumière, région à courbes de genre temps fermées (CTC, g_φφ < 0).

SIMULATION ILLUSTRATIVE : on trace des propriétés de solutions exactes connues des équations
d'Einstein. Rien ici ne prouve qu'un dispositif puisse les réaliser, ni que la région r < 0 existe
physiquement (elle se trouve derrière un horizon de Cauchy réputé instable).

Unités géométriques dans les calculs (G = c = 1, longueurs en unités de M) ; conversion en mètres
dans le tableau d'échelles (r_g = GM/c²).

Exécution :  .venv/bin/python 05_simulations/S02_kerr_geometrie/s02_kerr_geometrie.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore")   # Δ = 0 (horizons) et Σ = 0 (anneau) sont attendus sur les grilles
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S02_kerr_geometrie")
col = cc.COULEURS

# ---------------------------------------------------------------------------
# 1. Fonctions métriques (coordonnées de Boyer-Lindquist, signature - + + +, M = 1 par défaut)
# ---------------------------------------------------------------------------
# Variables : r (peut être négatif : extension analytique à travers le disque r = 0), θ ∈ [0, π].
# Paramètres : M (masse), a = J/M (moment cinétique spécifique), Q (charge, unités géométriques).


def Delta(r, a, Q=0.0, M=1.0):
    return r**2 - 2 * M * r + a**2 + Q**2


def Sigma(r, th, a):
    return r**2 + a**2 * np.cos(th)**2


def metrique(r, th, a, Q=0.0, M=1.0):
    """Retourne (g_tt, g_tφ, g_φφ, g_rr, g_θθ) de Kerr-Newman."""
    S = Sigma(r, th, a)
    D = Delta(r, a, Q, M)
    s2 = np.sin(th)**2
    g_tt = -(D - a**2 * s2) / S
    g_tp = -a * s2 * (r**2 + a**2 - D) / S
    g_pp = s2 * ((r**2 + a**2)**2 - D * a**2 * s2) / S
    return g_tt, g_tp, g_pp, S / D, S


def omega_entrainement(r, th, a, Q=0.0, M=1.0):
    """Vitesse angulaire des observateurs à moment cinétique nul : ω = -g_tφ / g_φφ."""
    g_tt, g_tp, g_pp, _, _ = metrique(r, th, a, Q, M)
    return -g_tp / g_pp


def horizons(a, Q=0.0, M=1.0):
    disc = M**2 - a**2 - Q**2
    if disc < 0:
        return None, None   # singularité nue (pas d'horizon)
    return M + np.sqrt(disc), M - np.sqrt(disc)


def ergosurfaces(th, a, Q=0.0, M=1.0):
    """Racines de g_tt = 0 : r_E± = M ± sqrt(M² - Q² - a² cos²θ)."""
    disc = M**2 - Q**2 - a**2 * np.cos(th)**2
    disc = np.where(disc >= 0, disc, np.nan)
    return M + np.sqrt(disc), M - np.sqrt(disc)


def omega_horizon(a, Q=0.0, M=1.0):
    rp, _ = horizons(a, Q, M)
    return a / (rp**2 + a**2)


def vitesses_angulaires_nulles(r, th, a, Q=0.0, M=1.0):
    """Ω± des photons purement azimutaux : g_tt + 2Ω g_tφ + Ω² g_φφ = 0."""
    g_tt, g_tp, g_pp, _, _ = metrique(r, th, a, Q, M)
    disc = g_tp**2 - g_tt * g_pp
    rac = np.sqrt(np.where(disc >= 0, disc, np.nan))
    return (-g_tp - rac) / g_pp, (-g_tp + rac) / g_pp


def kerr_schild_rz(r, th, a):
    """Coordonnées quasi cartésiennes de Kerr-Schild (ρ, z) : ρ = sqrt(r²+a²) sinθ, z = r cosθ."""
    return np.sqrt(r**2 + a**2) * np.sin(th), r * np.cos(th)


def bl_depuis_rz(rho, z, a):
    """Inversion (ρ, z) → (r ≥ 0, θ) sur le feuillet r > 0."""
    R2 = rho**2 + z**2 - a**2
    r = np.sqrt(0.5 * (R2 + np.sqrt(R2**2 + 4 * a**2 * z**2)))
    r = np.maximum(r, 1e-12)
    cth = np.clip(z / r, -1, 1)
    return r, np.arccos(cth)


def rayon_ctc_equatorial(a, Q=0.0, M=1.0):
    """Bord équatorial de la région g_φφ < 0 : racine de r⁴ + a²r² + 2Ma²r - Q²a² = 0.

    Kerr (Q = 0) : unique racine négative de r³ + a²r + 2Ma² = 0. Kerr-Newman : une racine négative
    et une racine positive (la région CTC déborde sur r > 0)."""
    p = lambda r: r**4 + a**2 * r**2 + 2 * M * a**2 * r - Q**2 * a**2
    r_neg = brentq(p, -10 * M, -1e-12) if p(-1e-12) < 0 else 0.0
    r_pos = brentq(p, 1e-12, 10 * M) if Q != 0 else 0.0
    return r_neg, r_pos


# ---------------------------------------------------------------------------
# 2. Tests de validation
# ---------------------------------------------------------------------------
print("S02 — tests de validation")
rp, rm = horizons(0.0)
val.verifier("Limite de Schwarzschild : r+ = 2M", rp, 2.0, tol_abs=1e-14)
val.verifier("Limite de Schwarzschild : r- = 0", rm, 0.0, tol_abs=1e-14)
val.verifier("Limite de Reissner-Nordström extrémale (Q = M) : r+ = M", horizons(0.0, 1.0)[0], 1.0, tol_abs=1e-14)
val.verifier("Kerr extrémal (a = M) : r+ = r- = M", horizons(1.0)[0] - horizons(1.0)[1], 0.0, tol_abs=1e-14)
val.verifier("Ergosurface équatoriale de Kerr : r_E = 2M (tout a)", float(ergosurfaces(np.pi / 2, 0.9)[0]), 2.0, tol_abs=1e-14)
val.verifier("Ergosurface aux pôles = horizon externe (a = 0,9)", float(ergosurfaces(0.0, 0.9)[0]), horizons(0.9)[0], tol_abs=1e-14)
# Identité g_tφ² - g_tt g_φφ = Δ sin²θ (points aléatoires, graine fixée)
rng = np.random.default_rng(204)
rr = rng.uniform(-3, 5, 2000)
tt = rng.uniform(0.05, np.pi - 0.05, 2000)
aa, QQ = 0.7, 0.4
g_tt, g_tp, g_pp, _, _ = metrique(rr, tt, aa, QQ)
ident = g_tp**2 - g_tt * g_pp - Delta(rr, aa, QQ) * np.sin(tt)**2
val.verifier("Identité g_tφ² − g_tt·g_φφ = Δ sin²θ (2000 points, Kerr-Newman)", np.max(np.abs(ident)), 0.0, tol_abs=1e-9)
# ω(r+, θ) = Ω_H indépendamment de θ (rigidité de l'horizon)
for a_, Q_ in ((0.5, 0.0), (0.9, 0.0), (0.6, 0.6)):
    rp_, _ = horizons(a_, Q_)
    w = omega_entrainement(rp_, np.linspace(0.1, np.pi - 0.1, 9), a_, Q_)
    val.verifier(f"ω(r+, θ) = Ω_H pour tout θ (a = {a_}, Q = {Q_})", np.max(np.abs(w - omega_horizon(a_, Q_))), 0.0, tol_abs=1e-12)
# Les deux vitesses angulaires nulles convergent vers Ω_H à l'horizon
Om_m, Om_p = vitesses_angulaires_nulles(horizons(0.9)[0] + 1e-9, np.pi / 2, 0.9)
val.verifier("Ω+ − Ω− → 0 à l'horizon (a = 0,9)", Om_p - Om_m, 0.0, tol_abs=1e-4)
# Bord de la région CTC équatoriale pour a = M : r = -M exactement
val.verifier("Bord CTC équatorial, Kerr a = M : r = −M", rayon_ctc_equatorial(1.0)[0], -1.0, tol_abs=1e-10)
# Champ lointain : ω → 2J/r³ (Lense-Thirring)
val.verifier("ω(r = 1000 M, équateur)·r³/(2J) → 1 (limite de Lense-Thirring)",
             omega_entrainement(1000.0, np.pi / 2, 0.9) * 1000.0**3 / (2 * 0.9), 1.0, tol_rel=3e-3)
# Conversion SI : rayon gravitationnel du Soleil ≈ 1476,6 m
val.verifier("r_g(Soleil) = GM/c² ≈ 1476,6 m", cc.G * cc.M_SOLEIL / cc.C**2, 1476.6, tol_rel=1e-3)


def verification_symbolique():
    """Vérifie par calcul formel exact (sympy, nombres rationnels) que :
    (i) la métrique de Kerr est une solution du vide (R_μν = 0) ;
    (ii) Kerr-Newman vérifie Einstein-Maxwell : G_μν = 2(F_μα F_ν^α − ¼ g_μν F²), R = 0.
    Coordonnées (t, r, x = cos θ, φ) pour que toutes les composantes soient rationnelles."""
    t, r, x, ph = sp.symbols("t r x phi", real=True)
    coords = (t, r, x, ph)
    sortie = {}
    for nom, a_, Q_ in (("Kerr a=3/5", sp.Rational(3, 5), sp.Integer(0)),
                        ("Kerr-Newman a=3/5 Q=1/2", sp.Rational(3, 5), sp.Rational(1, 2))):
        Mv = sp.Integer(1)
        S = r**2 + a_**2 * x**2
        D = r**2 - 2 * Mv * r + a_**2 + Q_**2
        s2 = 1 - x**2
        g = sp.zeros(4, 4)
        g[0, 0] = -(D - a_**2 * s2) / S
        g[0, 3] = g[3, 0] = -a_ * s2 * (r**2 + a_**2 - D) / S
        g[3, 3] = s2 * ((r**2 + a_**2)**2 - D * a_**2 * s2) / S
        g[1, 1] = S / D
        g[2, 2] = S / s2
        ginv = g.inv().applyfunc(sp.cancel)
        # Symboles de Christoffel Γ^i_{jk}
        Gam = [[[sp.cancel(sum(ginv[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j])
                                              - sp.diff(g[j, k], coords[l])) for l in range(4)) / 2)
                 for k in range(4)] for j in range(4)] for i in range(4)]
        # Tenseur de Ricci R_{jk} = ∂_i Γ^i_{jk} − ∂_k Γ^i_{ji} + Γ^i_{il} Γ^l_{jk} − Γ^i_{kl} Γ^l_{ji}
        Ric = sp.zeros(4, 4)
        for j in range(4):
            for k in range(j, 4):
                e = sum(sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k]) for i in range(4))
                e += sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for i in range(4) for l in range(4))
                Ric[j, k] = Ric[k, j] = sp.cancel(e)
        Rs = sp.cancel(sum(ginv[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
        if Q_ == 0:
            residu = max(abs(float(Ric[i, j].subs({r: sp.Rational(7, 3), x: sp.Rational(2, 7)}))) for i in range(4) for j in range(4))
            nul = all(Ric[i, j] == 0 for i in range(4) for j in range(4))
            sortie[nom] = {"ricci_identiquement_nul": bool(nul), "residu_max_point_test": residu}
        else:
            A = [-Q_ * r / S, 0, 0, Q_ * r * a_ * s2 / S]     # potentiel A_μ
            F = sp.zeros(4, 4)
            for i in range(4):
                for j in range(4):
                    F[i, j] = sp.diff(A[j], coords[i]) - sp.diff(A[i], coords[j])
            Fup = (ginv * F * ginv).applyfunc(sp.cancel)        # F^{μν}
            F2 = sp.cancel(sum(F[i, j] * Fup[i, j] for i in range(4) for j in range(4)))
            Fmix = (F * ginv).applyfunc(sp.cancel)              # F_μ^α
            T2 = sp.zeros(4, 4)
            for i in range(4):
                for j in range(4):
                    T2[i, j] = 2 * (sum(Fmix[i, k] * F[j, k] for k in range(4)) - g[i, j] * F2 / 4)
            Ein = Ric - g * Rs / 2
            diff = (Ein - T2).applyfunc(sp.cancel)
            nul = all(diff[i, j] == 0 for i in range(4) for j in range(4))
            sortie[nom] = {"einstein_maxwell_identiquement_verifie": bool(nul), "scalaire_de_ricci_nul": bool(Rs == 0)}
    return sortie


t0 = time.time()
symb = verification_symbolique()
print(f"  (vérification symbolique en {time.time() - t0:.1f} s)")
val.verifier_vrai("Kerr : R_μν ≡ 0 (calcul formel exact, a = 3/5)", symb["Kerr a=3/5"]["ricci_identiquement_nul"])
val.verifier_vrai("Kerr-Newman : G_μν ≡ 8πT_μν(EM) (calcul formel exact, a = 3/5, Q = 1/2)",
                  symb["Kerr-Newman a=3/5 Q=1/2"]["einstein_maxwell_identiquement_verifie"])
val.verifier_vrai("Kerr-Newman : scalaire de Ricci R ≡ 0", symb["Kerr-Newman a=3/5 Q=1/2"]["scalaire_de_ricci_nul"])

# ---------------------------------------------------------------------------
# 3. Figure 1 — cartes 2D (plan méridien, coordonnées de Kerr-Schild), feuillet r > 0
# ---------------------------------------------------------------------------
cas = [("Kerr, a = 0,5 M", 0.5, 0.0), ("Kerr, a = 0,9 M", 0.9, 0.0), ("Kerr, a = 0,998 M", 0.998, 0.0),
       ("Kerr-Newman, a = 0,6 M, Q = 0,6 M", 0.6, 0.6)]
fig, axes = plt.subplots(2, 2, figsize=(12, 11.5))
th_c = np.linspace(0, np.pi, 721)
for ax, (nom, a_, Q_) in zip(axes.ravel(), cas):
    L = 3.2
    xs = np.linspace(-L, L, 601)
    zs = np.linspace(-L, L, 601)
    XX, ZZ = np.meshgrid(xs, zs)
    r_, th_ = bl_depuis_rz(np.abs(XX), ZZ, a_)
    w = omega_entrainement(r_, th_, a_, Q_) / omega_horizon(a_, Q_)
    rp_, rm_ = horizons(a_, Q_)
    w = np.where(r_ >= rp_, w, np.nan)       # on ne colore que l'extérieur de l'horizon
    pc = ax.pcolormesh(XX, ZZ, w, cmap="magma", norm=LogNorm(vmin=1e-2, vmax=1.0), shading="auto")
    ax.set_facecolor("#d9d9d9")
    for signe in (+1, -1):
        rE_p, rE_m = ergosurfaces(th_c, a_, Q_)
        for rr_, c, ls, lab in ((np.full_like(th_c, rp_), col["ciel"], "-", "horizon externe $r_+$"),
                                (np.full_like(th_c, rm_), col["bleu"], "--", "horizon interne $r_-$"),
                                (rE_p, col["vert"], "-", "ergosurface externe ($g_{tt}=0$)"),
                                (rE_m, col["jaune"], "--", "ergosurface interne")):
            rho_c, z_c = kerr_schild_rz(rr_, th_c, a_)
            ax.plot(signe * rho_c, z_c, color=c, ls=ls, lw=1.8, label=lab if signe > 0 else None)
    ax.plot([-a_, a_], [0, 0], "o", color=col["rouge"], ms=5, label="singularité annulaire (ρ = a, z = 0)")
    ax.plot([-a_, a_], [0, 0], color=col["rouge"], lw=0.8, ls=":")
    ax.annotate("", xy=(0, L * 0.95), xytext=(0, L * 0.7), arrowprops=dict(arrowstyle="->", color="white", lw=1.5))
    ax.text(0.08, L * 0.8, "axe de rotation", color="white", fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlim(-L, L)
    ax.set_ylim(-L, L)
    ax.set_xlabel("ρ / M  (coordonnée de Kerr-Schild)")
    ax.set_ylabel("z / M")
    ax.set_title(f"{nom}\n$r_+$ = {rp_:.3f} M, $r_-$ = {rm_:.3f} M, $\\Omega_H$ = {omega_horizon(a_, Q_):.3f} c/M".replace(".", ","), fontsize=10)
    ax.grid(False)
    cb = fig.colorbar(pc, ax=ax, fraction=0.046, pad=0.03)
    cb.set_label(r"entraînement $\omega/\Omega_H$ (échelle log.)")
axes[0, 0].legend(loc="lower left", fontsize=7.5, framealpha=0.9)
cc.titre(fig, "S02 — Kerr et Kerr-Newman, plan méridien (feuillet r > 0) : horizons, ergosurfaces, vitesse d'entraînement ω(r, θ)")
cc.sauver_figure(fig, FIG / "S02_fig1_cartes_meridiennes.png", rect=(0, 0.03, 1, 0.94))

# ---------------------------------------------------------------------------
# 4. Figure 2 — région g_φφ < 0 (CTC), y compris r < 0
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16, 5.6))
# (a) g_φφ sur l'équateur
ax = axes[0]
r_lin = np.linspace(-2.5, 2.5, 5001)
r_lin = r_lin[np.abs(r_lin) > 1e-3]
for (nom, a_, Q_), c in zip(cas, (col["bleu"], col["vert"], col["rouge"], col["violet"])):
    gpp = metrique(r_lin, np.pi / 2, a_, Q_)[2]
    gpp[np.abs(np.diff(r_lin, prepend=r_lin[0])) > 1e-2] = np.nan     # coupe la courbe en r = 0
    ax.plot(r_lin, gpp, color=c, lw=1.8, label=nom)
ax.axhline(0, color="k", lw=0.8)
ax.axvline(0, color=col["gris"], lw=0.8, ls=":")
ax.axhspan(-30, 0, color=col["rouge"], alpha=0.08)
ax.text(-2.4, -6.5, "$g_{\\varphi\\varphi}$ < 0 :\n∂φ est de genre temps\n→ cercles t, r, θ = const.\n= courbes de genre\ntemps fermées (CTC)", fontsize=8.5, color=col["rouge"])
ax.set_ylim(-8, 8)
ax.set_xlabel("r / M  (r < 0 : extension analytique au-delà du disque)")
ax.set_ylabel(r"$g_{\varphi\varphi}/M^2$ dans le plan équatorial")
ax.set_title("(a) $g_{\\varphi\\varphi}(r)$, θ = π/2")
ax.legend(fontsize=7.5, loc="upper left")
# (b) et (c) : cartes dans le plan (r, cos θ) — coordonnées de Boyer-Lindquist, r des deux signes
resume_ctc = {}
for ax, (nom, a_, Q_) in zip(axes[1:], (("Kerr, a = 0,9 M", 0.9, 0.0), ("Kerr-Newman, a = 0,6 M, Q = 0,6 M", 0.6, 0.6))):
    r_g = np.linspace(-2.0, 2.5, 1201)
    mu_g = np.linspace(-1, 1, 801)
    RR, MU = np.meshgrid(r_g, mu_g)
    TH = np.arccos(MU)
    g_tt, g_tp, g_pp, g_rr, _ = metrique(RR, TH, a_, Q_)
    zone = np.zeros_like(RR)
    zone[g_tt > 0] = 1                              # ergorégion (∂t de genre espace)
    D_ = Delta(RR, a_, Q_)
    zone[D_ < 0] = 2                                # entre les horizons (r de genre temps)
    zone[g_pp < 0] = 3                              # région CTC
    cmap = plt.matplotlib.colors.ListedColormap(["#f7f7f7", "#b2df8a", "#a6cee3", "#e31a1c"])
    ax.pcolormesh(RR, MU, zone, cmap=cmap, vmin=-0.5, vmax=3.5, shading="auto")
    rp_, rm_ = horizons(a_, Q_)
    ax.axvline(rp_, color=col["bleu"], lw=1.5)
    ax.axvline(rm_, color=col["bleu"], lw=1.5, ls="--")
    ax.plot(0, 0, "o", color="k", ms=6)
    ax.annotate("singularité\nannulaire\n(r = 0, θ = π/2)", (0, 0), textcoords="offset points", xytext=(-75, 35), fontsize=8,
                arrowprops=dict(arrowstyle="->", lw=0.8))
    ax.axvline(0, color="k", lw=0.6, ls=":")
    rn, rpz = rayon_ctc_equatorial(a_, Q_)
    aire = float(np.sum(g_pp < 0) * (r_g[1] - r_g[0]) * (mu_g[1] - mu_g[0]))
    resume_ctc[nom] = {"a": a_, "Q": Q_, "r_ctc_equateur_negatif_M": rn, "r_ctc_equateur_positif_M": rpz,
                       "r_plus_M": rp_, "r_moins_M": rm_, "region_ctc_derriere_horizon_interne": bool(rpz < rm_)}
    ax.set_xlabel("r / M")
    ax.set_ylabel("cos θ")
    ax.set_title(f"({'b' if Q_ == 0 else 'c'}) {nom}\nrégion CTC équatoriale : {rn:.3f} M < r < {rpz:.3f} M".replace(".", ","), fontsize=10)
    ax.grid(False)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc="#e31a1c", label="$g_{\\varphi\\varphi}$ < 0 : région à CTC"),
                       Patch(fc="#a6cee3", label="Δ < 0 : entre les horizons"),
                       Patch(fc="#b2df8a", label="$g_{tt}$ > 0 : ergorégion"),
                       plt.Line2D([], [], color=col["bleu"], label="horizon externe $r_+$"),
                       plt.Line2D([], [], color=col["bleu"], ls="--", label="horizon interne $r_-$")],
              loc="lower right", fontsize=7.5, framealpha=0.95)
cc.titre(fig, "S02 — Région où $g_{\\varphi\\varphi}$ < 0 (courbes de genre temps fermées) : elle est confinée près de l'anneau, derrière l'horizon interne")
cc.sauver_figure(fig, FIG / "S02_fig2_region_ctc.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 5. Figure 3 — entraînement et basculement des cônes de lumière (plan équatorial)
# ---------------------------------------------------------------------------


def dessiner_cone(ax, x0, y0, g_tt, g_tp, g_pp, taille=0.33):
    """Dessine, autour de (x0, y0), les directions de genre temps du plan (φ, t).

    Abscisse locale : déplacement azimutal propre R·dφ (R = sqrt|g_φφ|) ; ordonnée : dt.
    Les secteurs où g_tt dt² + 2 g_tφ dt dφ + g_φφ dφ² < 0 sont remplis."""
    R = np.sqrt(abs(g_pp))
    alpha = np.linspace(0, 2 * np.pi, 1441)
    dphi = np.cos(alpha) / R
    dt = np.sin(alpha)
    q = g_tt * dt**2 + 2 * g_tp * dt * dphi + g_pp * dphi**2
    temps = q < 0
    # découpe en secteurs contigus
    idx = np.where(np.diff(temps.astype(int)) != 0)[0]
    bornes = np.concatenate([[0], idx + 1, [len(alpha) - 1]])
    for i0, i1 in zip(bornes[:-1], bornes[1:]):
        if temps[i0:i1].all() and i1 - i0 > 1:
            al = alpha[i0:i1 + 1]
            pts = np.column_stack([np.concatenate([[x0], x0 + taille * np.cos(al)]),
                                   np.concatenate([[y0], y0 + taille * np.sin(al)])])
            futur = np.mean(np.sin(al)) > 0
            ax.add_patch(Polygon(pts, closed=True, fc=col["orange"] if futur else col["ciel"], ec="k", lw=0.6, alpha=0.9))


a_f = 0.9
rp_f, rm_f = horizons(a_f)
fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.6), gridspec_kw={"width_ratios": [1.1, 1.25, 1.0]})
ax = axes[0]
r_ext = np.linspace(rp_f + 1e-4, 6, 2000)
Om_m, Om_p = vitesses_angulaires_nulles(r_ext, np.pi / 2, a_f)
ax.fill_between(r_ext, Om_m, Om_p, color=col["orange"], alpha=0.25, label="vitesses angulaires permises (genre temps)")
ax.plot(r_ext, Om_p, color=col["rouge"], lw=1.8, label=r"$\Omega_+$ (photon prograde)")
ax.plot(r_ext, Om_m, color=col["bleu"], lw=1.8, label=r"$\Omega_-$ (photon rétrograde)")
ax.plot(r_ext, omega_entrainement(r_ext, np.pi / 2, a_f), color="k", ls="--", lw=1.5, label=r"$\omega = -g_{t\varphi}/g_{\varphi\varphi}$")
ax.axhline(omega_horizon(a_f), color=col["gris"], ls=":", lw=1)
ax.text(4.2, omega_horizon(a_f) + 0.01, f"$\\Omega_H$ = {omega_horizon(a_f):.3f} c/M".replace(".", ","), color=col["gris"], fontsize=8.5)
ax.axvline(2.0, color=col["vert"], lw=1.2)
ax.text(2.03, -0.33, "ergosurface\n(r = 2M) :\n$\\Omega_-$ = 0", color=col["vert"], fontsize=8.5)
ax.axvline(rp_f, color=col["ciel"], lw=1.5)
ax.text(rp_f + 0.04, -0.2, "horizon $r_+$", color=col["bleu"], fontsize=8.5, rotation=90)
ax.axhline(0, color="k", lw=0.6)
ax.set_xlim(1.2, 6)
ax.set_ylim(-0.4, 0.62)
ax.set_xlabel("r / M (plan équatorial)")
ax.set_ylabel("vitesse angulaire dφ/dt  [c/M]")
ax.set_title(f"(a) Cône des vitesses angulaires, Kerr a = 0,9 M")
ax.legend(fontsize=7.5, loc="upper right")

ax = axes[1]
rayons = [-1.6, -0.75, -0.35, 0.25, 0.42, 1.55, 1.75, 2.0, 3.0, 5.0]
positions = np.arange(len(rayons))
for x0, r_ in zip(positions, rayons):
    g_tt, g_tp, g_pp, _, _ = metrique(r_, np.pi / 2, a_f)
    dessiner_cone(ax, x0, 0.0, g_tt, g_tp, g_pp, taille=0.42)
    etiquette = "CTC" if g_pp < 0 else ("ergo" if g_tt > 0 else "")
    ax.text(x0, -0.56, f"r = {r_:+.2f} M".replace(".", ","), ha="center", va="top", fontsize=7.5, rotation=60)
    if etiquette:
        ax.text(x0, 0.52, etiquette, ha="center", fontsize=8, color=col["rouge"] if etiquette == "CTC" else col["vert"], weight="bold")
ax.axhline(0, color=col["gris"], lw=0.6)
ax.axvspan(4.5, 4.5, color="k")
ax.text(4.5, 0.74, "← r < $r_-$ (intérieur)   |   r > $r_+$ (extérieur) →", ha="center", fontsize=8.5)
ax.axvline(4.5, color=col["bleu"], ls="--", lw=1)
ax.set_xlim(-0.7, len(rayons) - 0.3)
ax.set_ylim(-0.95, 0.9)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("abscisse locale de chaque cône : déplacement azimutal propre R dφ →\n"
              "Dans l'ergorégion le cône bascule au point d'exclure dφ = 0 ; là où $g_{\\varphi\\varphi}$ < 0 (r < 0, près de l'anneau)\n"
              "il contient la direction horizontale dt = 0 : le cercle φ ∈ [0, 2π] à t constant est de genre temps (CTC).", fontsize=8)
ax.set_ylabel("ordonnée locale : dt ↑")
ax.set_title("(b) Cônes de lumière dans le plan (φ, t) : orange = futur, bleu = passé")
ax.title.set_fontsize(9.5)
ax.grid(False)

ax = axes[2]
for a_, c in ((0.5, col["bleu"]), (0.9, col["vert"]), (0.998, col["rouge"])):
    rp_, _ = horizons(a_)
    r_e = np.logspace(np.log10(rp_ * 1.0001), 2, 600)
    ax.loglog(r_e, omega_entrainement(r_e, np.pi / 2, a_), color=c, lw=1.8, label=f"a = {a_} M".replace(".", ","))
    ax.loglog(r_e, 2 * a_ / r_e**3, color=c, lw=1, ls=":")
ax.plot([], [], color="k", ls=":", lw=1, label=r"champ faible : $2J/r^3$ (Lense-Thirring)")
ax.set_xlabel("r / M (plan équatorial)")
ax.set_ylabel(r"$\omega$  [c/M]")
ax.set_title("(c) Décroissance de l'entraînement : ω ∝ $r^{-3}$")
ax.legend(fontsize=8)
cc.titre(fig, "S02 — Entraînement des référentiels et basculement des cônes de lumière dans Kerr (a = 0,9 M)")
cc.sauver_figure(fig, FIG / "S02_fig3_cones_entrainement.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Figure 4 — rendu 3D (coordonnées de Kerr-Schild, quart ôté)
# ---------------------------------------------------------------------------
a3 = 0.9
rp3, rm3 = horizons(a3)
fig = plt.figure(figsize=(10.5, 9))
ax = fig.add_subplot(111, projection="3d")
th3 = np.linspace(0, np.pi, 91)
ph3 = np.linspace(0, 1.5 * np.pi, 91)
TH3, PH3 = np.meshgrid(th3, ph3)
rE_p3, rE_m3 = ergosurfaces(TH3, a3)
for rr_, c, al, lab in ((rE_p3, col["vert"], 0.22, "ergosurface externe"), (np.full_like(TH3, rp3), col["ciel"], 0.55, "horizon externe $r_+$"),
                        (np.full_like(TH3, rm3), col["bleu"], 0.75, "horizon interne $r_-$"), (rE_m3, col["jaune"], 0.9, "ergosurface interne")):
    rho3, z3 = kerr_schild_rz(rr_, TH3, a3)
    ax.plot_surface(rho3 * np.cos(PH3), rho3 * np.sin(PH3), z3, color=c, alpha=al, linewidth=0, rstride=2, cstride=2, shade=True)
    ax.plot([], [], [], color=c, lw=6, alpha=max(al, 0.5), label=lab)
pp = np.linspace(0, 2 * np.pi, 200)
ax.plot(a3 * np.cos(pp), a3 * np.sin(pp), 0 * pp, color=col["rouge"], lw=3, zorder=20, label="singularité annulaire (rayon a)")
ax.plot([0, 0], [0, 0], [-2.6, 2.6], color="k", lw=1, ls="--")
ax.text(0, 0, 2.7, "axe de rotation", fontsize=8.5)
ax.set_xlabel("x / M")
ax.set_ylabel("y / M")
ax.set_zlabel("z / M")
ax.set_box_aspect((1, 1, 1))
lim = 2.3
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim, lim)
ax.view_init(elev=22, azim=-58)
ax.legend(loc="upper left", fontsize=8.5)
cc.titre(fig, "S02 — Trou noir de Kerr (a = 0,9 M) en coordonnées de Kerr-Schild : surfaces emboîtées, quart ôté")
cc.sauver_figure(fig, FIG / "S02_fig4_rendu_3d.png", rect=(0, 0.03, 1, 0.94))

# ---------------------------------------------------------------------------
# 7. Tableau d'échelles en mètres pour M = 10² … 10¹² kg
# ---------------------------------------------------------------------------
masses = [cc.REVENDICATIONS["masse_unite_kg"] / 2] + [10.0**k for k in range(2, 13)] + [cc.C**2 / cc.G]
lignes = []
a_ref = 0.9
for Mkg in masses:
    rg = cc.G * Mkg / cc.C**2
    rp_, rm_ = horizons(a_ref)
    spin = np.sqrt(1 - a_ref**2)
    lignes.append({
        "M_kg": Mkg,
        "r_g_m": rg,
        "r_plus_a0p9_m": rp_ * rg,
        "r_moins_a0p9_m": rm_ * rg,
        "ergosurface_equatoriale_m": 2 * rg,
        "rayon_anneau_a0p9_m": a_ref * rg,
        "rayon_anneau_max_extremal_m": rg,
        "etendue_region_ctc_a0p9_m": abs(rayon_ctc_equatorial(a_ref)[0]) * rg,
        "Omega_H_a0p9_rad_s": omega_horizon(a_ref) * cc.C / rg,
        "J_max_kg_m2_s": cc.G * Mkg**2 / cc.C,
        "J_max_en_hbar": cc.G * Mkg**2 / cc.C / cc.HBAR,
        "Q_max_C": Mkg * np.sqrt(4 * np.pi * cc.EPS0 * cc.G),
        "T_Hawking_a0p9_K": cc.HBAR * cc.C**3 / (8 * np.pi * cc.G * Mkg * cc.K_B) * 2 * spin / (1 + spin),
        "omega_LT_a_1m_extremal_rad_s": 2 * cc.G * (cc.G * Mkg**2 / cc.C) / (cc.C**2 * 1.0**3),
    })
entetes = list(lignes[0].keys())
with open(RES / "S02_echelles_metres.csv", "w", encoding="utf-8") as f:
    f.write(",".join(entetes) + "\n")
    for L_ in lignes:
        f.write(",".join(f"{L_[k]:.6e}" for k in entetes) + "\n")
print(f"  résultats : {RES / 'S02_echelles_metres.csv'}")

# Figure 5 : échelles
fig, ax = plt.subplots(figsize=(10.5, 6.2))
Mx = np.logspace(1.5, 28, 200)
rgx = cc.G * Mx / cc.C**2
ax.loglog(Mx, 2 * rgx, color=col["vert"], lw=2, label="ergosurface équatoriale $2GM/c^2$")
ax.loglog(Mx, horizons(a_ref)[0] * rgx, color=col["ciel"], lw=2, label="horizon externe $r_+$ (a = 0,9 M)")
ax.loglog(Mx, a_ref * rgx, color=col["rouge"], lw=2, label="rayon de l'anneau a (a = 0,9 M)")
ax.loglog(Mx, abs(rayon_ctc_equatorial(a_ref)[0]) * rgx, color=col["violet"], lw=2, ls="--", label="étendue radiale de la région CTC (r < 0)")
for y, nom, c in ((cc.L_PLANCK, "longueur de Planck", col["gris"]), (cc.R_PROTON, "rayon du proton", col["orange"]),
                  (1e-10, "atome (1 Å)", col["bleu"]), (1.0, "1 m (échelle humaine)", "k")):
    ax.axhline(y, color=c, ls=":", lw=1.2)
    ax.text(40, y * 1.6, nom, color=c, fontsize=8.5)
ax.axvspan(1e2, 1e12, color=col["jaune"], alpha=0.25, label="plage étudiée : $10^2$ – $10^{12}$ kg")
ax.axvline(cc.REVENDICATIONS["masse_unite_kg"] / 2, color=col["bleu"], ls="--", lw=1.2)
ax.text(cc.REVENDICATIONS["masse_unite_kg"] / 2 * 1.4, 1e-3, "113 kg", color=col["bleu"], fontsize=8.5)
M_1m = cc.C**2 / cc.G
ax.plot(M_1m, 1.0, "o", color="k")
ax.annotate(f"$r_g$ = 1 m ⇔ M = {cc.sci(M_1m)} kg\n(≈ {M_1m / cc.M_JUPITER:.2f} masse de Jupiter)".replace(".", ","), (M_1m, 1.0),
            textcoords="offset points", xytext=(-230, 22), fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("masse M [kg]")
ax.set_ylabel("longueur [m]")
ax.set_ylim(1e-37, 1e6)
ax.legend(loc="lower right", fontsize=8.5)
cc.titre(fig, "S02 — Échelles de longueur de la géométrie de Kerr en mètres, en fonction de la masse")
cc.sauver_figure(fig, FIG / "S02_fig5_echelles.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 8. Sauvegarde
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S02_kerr_geometrie",
    "avertissement": cc.MENTION,
    "unites": "géométriques (G = c = 1, M = 1) sauf mention ; r_g = GM/c²",
    "cas_etudies": [{"nom": n, "a": a_, "Q": Q_, "r_plus": horizons(a_, Q_)[0], "r_moins": horizons(a_, Q_)[1],
                     "Omega_H": omega_horizon(a_, Q_), "ergo_equateur": float(ergosurfaces(np.pi / 2, a_, Q_)[0])}
                    for n, a_, Q_ in cas],
    "region_ctc": resume_ctc,
    "rayon_ctc_equatorial_kerr": {f"a={a_}": rayon_ctc_equatorial(a_)[0] for a_ in (0.1, 0.5, 0.9, 0.998, 1.0)},
    "verification_symbolique": symb,
    "echelles_metres": lignes,
    "masse_pour_r_g_1m_kg": M_1m,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S02_resultats.json", resultats)
val.imprimer_bilan()
print("S02 terminé.")
