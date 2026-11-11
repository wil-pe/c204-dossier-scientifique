#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 04 : cylindre de van Stockum / Tipler.

Métrique (van Stockum 1937 ; Tipler 1974), signature (-+++), G = c = 1 :
    ds² = H (dr² + dz²) + L dφ² + 2 M dφ dt - F dt²
Intérieur (poussière en rotation rigide, 0 ≤ r ≤ R) :
    H = exp(-a² r²),  L = r² (1 - a² r²),  M = a r²,  F = 1
Extérieur (vide), trois cas selon aR :
    aR < 1/2 : fonctions hyperboliques de θ = sqrt(1 - 4a²R²) ln(r/R)
    aR = 1/2 : fonctions de ln(r/R)
    aR > 1/2 : fonctions SINUSOÏDALES de γ = sqrt(4a²R² - 1) ln(r/R)

Vérifications symboliques :
  V1. intérieur : G_{μν} = 8π ρ u_μ u_ν avec u = ∂_t, 8πρ = 4 a² exp(a² r²) ; vorticité sur l'axe = a
  V2. les trois extérieurs sont des solutions du vide (R_{μν} = 0)
  V3. raccord C¹ en r = R (métrique et dérivées radiales continues)
  V4. F L + M² = r² (coordonnées canoniques) ; signe de L = g_φφ -> zones à CTC
Ordres de grandeur (SI) : masse linéique, densité, vitesse angulaire.
"""
import math
import time

import sympy as sp

from constantes import *

t0 = time.time()
print("=" * 78)
print("SCRIPT 04 — Cylindre de van Stockum / Tipler")
print("=" * 78)

t, r, ph, z = sp.symbols("t r phi z", real=True)
a, R = sp.symbols("a R", positive=True)
coords = [t, r, ph, z]


def metrique(H, L, Mf, F):
    g = sp.zeros(4, 4)
    g[0, 0] = -F
    g[0, 2] = g[2, 0] = Mf
    g[2, 2] = L
    g[1, 1] = H
    g[3, 3] = H
    return g


def inverse(g, simp=True):
    """Inverse par blocs (bloc (t, φ) 2x2 ; r et z diagonaux)."""
    gi = sp.zeros(4, 4)
    D = g[0, 0] * g[2, 2] - g[0, 2] ** 2
    if simp:
        D = sp.simplify(D)
    gi[0, 0] = g[2, 2] / D
    gi[2, 2] = g[0, 0] / D
    gi[0, 2] = gi[2, 0] = -g[0, 2] / D
    gi[1, 1] = 1 / g[1, 1]
    gi[3, 3] = 1 / g[3, 3]
    return gi


def ricci(g, gi, simp=True):
    """Tenseur de Ricci ; simp=False : expressions brutes (pour évaluation numérique à haute précision)."""
    f = sp.simplify if simp else (lambda e: e)
    n = 4
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(j, n):
                e = 0
                for l in range(n):
                    if gi[i, l] != 0:
                        e += gi[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                Gam[i][j][k] = Gam[i][k][j] = f(e / 2)
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(j, n):
            e = 0
            for i in range(n):
                e += sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k])
                for l in range(n):
                    e += Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i]
            Ric[j, k] = Ric[k, j] = f(e)
    return Ric


# ---------------------------------------------------------------- V1 : intérieur
print("\n[V1] Intérieur de van Stockum")
Hi, Li, Mi, Fi = sp.exp(-a**2 * r**2), r**2 * (1 - a**2 * r**2), a * r**2, sp.Integer(1)
g_in = metrique(Hi, Li, Mi, Fi)
gi_in = inverse(g_in)
assert (g_in * gi_in).applyfunc(sp.simplify) == sp.eye(4)
Ric = ricci(g_in, gi_in)
Rs = sp.simplify(sum(gi_in[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Gein = (Ric - g_in * Rs / 2).applyfunc(sp.simplify)
u_bas = sp.Matrix([g_in[i, 0] for i in range(4)])          # u^μ = (1,0,0,0) -> u_μ = g_{μ t}
rho8pi = 4 * a**2 * sp.exp(a**2 * r**2)
residu = (Gein - rho8pi * (u_bas * u_bas.T)).applyfunc(sp.simplify)
print("  G_{μν} - 8πρ u_μ u_ν =", "0 (vérifié)" if residu == sp.zeros(4, 4) else residu)
print("  avec 8πGρ/c² = 4 a² exp(a² r²)  -> sur l'axe : ρ0 = a² c² / (2π G)")
print("  scalaire de Ricci R =", Rs, "(= -8π T = 8πρ pour une poussière)")
# vorticité : ω^μ = (1/2) ε^{μνρσ} u_ν ∂_ρ u_σ ; ici seule ω^z ≠ 0
sqrtmg = sp.simplify(sp.sqrt(-g_in.det()))
# ε^{z t r φ} : (μ,ν,ρ,σ) = (z,t,r,φ) et (z,φ,r,t)... calcul direct de la composante z
# ω^z = (1/(2 sqrt(-g))) * [ε_{ztrφ}-somme] = (1/sqrt(-g)) * (1/2) * (u_t (∂_r u_φ - ∂_φ u_r) + u_φ (∂_t u_r - ∂_r u_t) + u_r(...))
u_t, u_r, u_ph, u_z = u_bas
omega_z = sp.simplify((u_t * (sp.diff(u_ph, r)) - u_ph * sp.diff(u_t, r)) / (2 * sqrtmg))
omega_norme = sp.simplify(sp.sqrt(g_in[3, 3]) * sp.Abs(omega_z))
print("  sqrt(-g) =", sqrtmg, " ; vorticité |ω| =", omega_norme, " -> sur l'axe |ω| = a  (rotation locale de la matière)")
print("  g_φφ = L = r²(1 - a² r²) : négatif pour a r > 1  => cercles (t, r, z constants) de genre temps si R > 1/a")
print(f"  [temps {time.time()-t0:.0f} s]")

# ---------------------------------------------------------------- V2/V3 : extérieurs
print("\n[V2-V3] Extérieurs (vide) et raccord en r = R")
lnr = sp.log(r / R)

# cas aR < 1/2
n_ = sp.sqrt(1 - 4 * a**2 * R**2)
eps = sp.atanh(n_)
th = n_ * lnr
H1 = sp.exp(-a**2 * R**2) * (r / R) ** (-2 * a**2 * R**2)
L1 = R * r * sp.sinh(3 * eps + th) / (2 * sp.sinh(2 * eps) * sp.cosh(eps))
M1 = r * sp.sinh(eps + th) / sp.sinh(2 * eps)
F1 = r * sp.sinh(eps - th) / (R * sp.sinh(eps))

# cas aR > 1/2
m_ = sp.sqrt(4 * a**2 * R**2 - 1)
bet = sp.atan(m_)
gam = m_ * lnr
H3 = H1
L3 = R * r * sp.sin(3 * bet + gam) / (2 * sp.sin(2 * bet) * sp.cos(bet))
M3 = r * sp.sin(bet + gam) / sp.sin(2 * bet)
F3 = r * sp.sin(bet - gam) / (R * sp.sin(bet))

# cas aR = 1/2
H2 = sp.exp(-sp.Rational(1, 4)) * (r / R) ** (-sp.Rational(1, 2))
L2 = R * r * (3 + lnr) / 4
M2 = r * (1 + lnr) / 2
F2 = (r / R) * (1 - lnr)


def controle(nom, H, L, Mf, F, valeurs, aR_fixe=None):
    """Contrôle numérique exact (rationnels) du vide et du raccord, pour plusieurs valeurs de a et R."""
    ok_vide, ok_raccord, ok_can = True, True, True
    residu_max = [0.0]
    for (av, Rv) in valeurs:
        sub = {a: av, R: Rv}
        g = metrique(*(e.subs(sub) for e in (H, L, Mf, F)))
        gi = inverse(g, simp=False)
        Ric = ricci(g, gi, simp=False)
        for rv in (sp.Rational(3, 2) * Rv, 4 * Rv, 11 * Rv):
            vals = [abs(complex(sp.N(Ric[i, j].subs(r, rv), 40))) for i in range(4) for j in range(4)]
            if max(vals) > 1e-25:
                ok_vide = False
            residu_max[0] = max(residu_max[0], max(vals))
        # raccord C1
        for ext, inte in ((H, Hi), (L, Li), (Mf, Mi), (F, Fi)):
            d0 = (ext - inte).subs(sub).subs(r, Rv).evalf(30)
            d1 = sp.diff(ext - inte, r).subs(sub).subs(r, Rv).evalf(30)
            if abs(complex(d0)) > 1e-20 or abs(complex(d1)) > 1e-20:
                ok_raccord = False
        can = (F * L + Mf**2 - r**2).subs(sub).subs(r, 3 * Rv).evalf(30)
        if abs(complex(can)) > 1e-20:
            ok_can = False
    print(f"  {nom:<10} : vide R_μν=0 : {'OK' if ok_vide else 'ÉCHEC'} ; raccord C¹ en r=R : {'OK' if ok_raccord else 'ÉCHEC'} ;"
          f" F L + M² = r² : {'OK' if ok_can else 'ÉCHEC'} ; max |R_μν| numérique (40 chiffres) = {residu_max[0]:.1e}")


controle("aR < 1/2", H1, L1, M1, F1, [(sp.Rational(1, 5), 1), (sp.Rational(2, 5), 1), (sp.Rational(1, 7), 2)])
controle("aR = 1/2", H2.subs(R, R), L2, M2, F2, [(sp.Rational(1, 2), 1), (sp.Rational(1, 4), 2)])
controle("aR > 1/2", H3, L3, M3, F3, [(sp.Rational(3, 5), 1), (1, 1), (sp.Rational(3, 4), 2)])
print(f"  [temps {time.time()-t0:.0f} s]")

# ---------------------------------------------------------------- V4 : zones à CTC, structure sinusoïdale
print("\n[V4] Structure causale extérieure pour aR > 1/2 : L = g_φφ ∝ r sin(3β + γ(r)),  γ = sqrt(4a²R² - 1) ln(r/R)")
print("     -> coquilles concentriques alternées g_φφ < 0 (∂_φ de genre temps : CTC) / g_φφ > 0, en progression géométrique")
for aR in (0.51, 0.6, 0.75, 1.0, 2.0):
    m = math.sqrt(4 * aR**2 - 1)
    b = math.atan(m)
    zeros = []
    n = 0
    while len(zeros) < 4:
        n += 1
        val = (n * math.pi - 3 * b) / m
        if val >= -1e-12:
            zeros.append(math.exp(max(val, 0.0)))
    signe_initial = math.sin(3 * b + 1e-9)
    etat = "g_φφ>0" if signe_initial > 0 else "g_φφ<0 (CTC)"
    print(f"  aR = {aR:<4} : zéros de g_φφ à r/R = " + ", ".join(f"{zv:.4g}" for zv in zeros)
          + f" ; rapport entre zéros successifs = exp(π/sqrt(4a²R²-1)) = {math.exp(math.pi/m):.4g} ; juste hors du cylindre : {etat}")
print("  aR < 1/2 : L = g_φφ ∝ r sinh(3ε + θ) > 0 partout : pas de CTC (et F > 0 jusqu'à θ = ε).")

# ---------------------------------------------------------------- ordres de grandeur
print("\n" + "-" * 78)
print("Ordres de grandeur (SI) — seuil d'apparition des CTC extérieures : aR = 1/2")
print("-" * 78)
print("  masse linéique (mesurée dans le référentiel de la matière) μ = a²R² c² / (2G) ; au seuil μ = c²/(8G)")
mu_seuil = c**2 / (8 * G)
print(f"  μ_seuil = {mu_seuil:.3e} kg/m  = {mu_seuil/M_terre:.1f} masses terrestres par mètre = {mu_seuil/M_soleil*1e3:.3e} M_soleil par km")
print(f"  {'R':>10} {'ω = c/(2R) (rad/s)':>20} {'ρ0 = ω²/(2πG) (kg/m³)':>24} {'masse d un tronçon de longueur 10 R (kg)':>42}")
for Rm in (1e-15, 0.15, 1.0, 1e4):
    om = c / (2 * Rm)
    rho0 = om**2 / (2 * math.pi * G)
    print(f"  {Rm:>10.3g} {om:>20.3e} {rho0:>24.3e} {mu_seuil*10*Rm:>42.3e}")
print("  (R = 10 km : ρ0 ≈ 5e17 kg/m³, soit environ deux fois la densité de saturation nucléaire ≈ 2,3e17 kg/m³)")
print("  Pour des CTC DANS la matière (a r > 1) il faudrait R > 1/a, soit μ > c²/(2G) = " + f"{c**2/(2*G):.3e} kg/m")
print()
print("  « Le même environnement sans la masse » : invariance d'échelle du vide. Si g est solution du vide,")
print("  λ² g l'est aussi, avec M -> λM (ou μ inchangé pour un cylindre), longueurs -> λ × longueurs.")
print("  Toute longueur caractéristique vaut donc GM/c² × f(sans dimension) : une zone à CTC de taille ℓ exige M ~ ℓ c²/G.")
for ell in (1.0, 3.7):
    print(f"   ℓ = {ell} m -> M ~ {ell*c**2/G:.2e} kg")
print(f"\nTemps de calcul : {time.time()-t0:.0f} s")
