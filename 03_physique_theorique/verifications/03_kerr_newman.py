#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 03 : trou noir de Kerr et de Kerr-Newman.

Partie A (symbolique, sympy) :
  A1. la métrique de Kerr-Newman (coordonnées de Boyer-Lindquist, x = cos θ) et le potentiel
      A = -(Q r/Σ)(dt - a sin²θ dφ) satisfont les équations d'Einstein-Maxwell
      R_{μν} = 2 (F_{μα} F_ν^α - ¼ g_{μν} F²)   (G = c = 1, charge géométrisée) et ∂_μ(√-g F^{μν}) = 0 ;
  A2. cas Q = 0 : Kerr est Ricci-plat ;
  A3. g_φφ sur le plan équatorial -> région à courbes temporelles fermées (CTC) de Carter ;
  A4. horizons, ergosphère, température, masse irréductible ;
  A5. t (Boyer-Lindquist) est une fonction de temps pour r > r+ (hypothèse : existence d'un horizon) ;
  A6. temps de Kerr-Schild : fonction de temps hors d'un tube entourant l'anneau, sans hypothèse d'horizon.
Partie B (numérique) : ordres de grandeur pour les masses pertinentes (227 kg ... 1e12 kg ... 1e27 kg).
"""
import math
import time

import sympy as sp

from constantes import *

t0 = time.time()
print("=" * 78)
print("SCRIPT 03 — Kerr / Kerr-Newman : vérifications symboliques et ordres de grandeur")
print("=" * 78)

# ----------------------------------------------------------------------------
# Partie A — symbolique
# ----------------------------------------------------------------------------
t, r, x, ph = sp.symbols("t r x phi", real=True)
M, a, Q = sp.symbols("M a Q", positive=True)
coords = [t, r, x, ph]
Sigma = r**2 + a**2 * x**2
Delta = r**2 - 2 * M * r + a**2 + Q**2
s2 = 1 - x**2     # sin²θ

# ds² = -(Δ/Σ)(dt - a s2 dφ)² + (s2/Σ)((r²+a²)dφ - a dt)² + (Σ/Δ)dr² + (Σ/s2)dx²
g = sp.zeros(4, 4)
g[0, 0] = -(Delta - a**2 * s2) / Sigma
g[0, 3] = g[3, 0] = (Delta * a * s2 - a * s2 * (r**2 + a**2)) / Sigma
g[3, 3] = (-Delta * a**2 * s2**2 + s2 * (r**2 + a**2) ** 2) / Sigma
g[1, 1] = Sigma / Delta
g[2, 2] = Sigma / s2
# inverse écrit sous forme close puis VÉRIFIÉ (g · g^{-1} = 1) : bien plus rapide que g.inv()
ginv = sp.zeros(4, 4)
ginv[0, 0] = -((r**2 + a**2) ** 2 - Delta * a**2 * s2) / (Delta * Sigma)
ginv[0, 3] = ginv[3, 0] = -a * (r**2 + a**2 - Delta) / (Delta * Sigma)
ginv[3, 3] = (Delta - a**2 * s2) / (Delta * Sigma * s2)
ginv[1, 1] = Delta / Sigma
ginv[2, 2] = s2 / Sigma
assert (g * ginv).applyfunc(sp.cancel) == sp.eye(4), "inverse de la métrique incorrect"


def christoffel(g, ginv, coords):
    n = len(coords)
    Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(j, n):
                expr = 0
                for l in range(n):
                    if ginv[i, l] != 0:
                        expr += ginv[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                Gam[i][j][k] = Gam[i][k][j] = sp.cancel(expr / 2)
    return Gam


def ricci(g, ginv, coords):
    n = len(coords)
    Gam = christoffel(g, ginv, coords)
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(j, n):
            expr = 0
            for i in range(n):
                expr += sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k])
                for l in range(n):
                    expr += Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i]
            Ric[j, k] = Ric[k, j] = sp.cancel(sp.together(expr))
    return Ric


print("\n[A1] Kerr-Newman : équations d'Einstein-Maxwell")
Ric = ricci(g, ginv, coords)
# potentiel et tenseur de Faraday
A = [-Q * r / Sigma, 0, 0, Q * r * a * s2 / Sigma]
F = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        F[i, j] = sp.diff(A[j], coords[i]) - sp.diff(A[i], coords[j])
Fup = (ginv * F * ginv).applyfunc(sp.cancel)          # F^{μν}
F2 = sp.cancel(sum(F[i, j] * Fup[i, j] for i in range(4) for j in range(4)))
Tm = sp.zeros(4, 4)
Fmix = (F * ginv).applyfunc(sp.cancel)                # F_{μ}^{ α}
for i in range(4):
    for j in range(4):
        Tm[i, j] = sp.cancel(2 * (sum(Fmix[i, k] * F[j, k] for k in range(4)) - sp.Rational(1, 4) * g[i, j] * F2))
residu = (Ric - Tm).applyfunc(sp.cancel)
print("  R_{μν} - 2(F_{μα}F_ν^α - ¼ g_{μν}F²) =", "0 (vérifié, les 10 composantes)" if residu == sp.zeros(4, 4) else residu)
detg = sp.factor(g.det())
print("  det g =", detg, "  -> sqrt(-g) = Σ (en coordonnée x = cos θ)")
sqrtmg = Sigma
maxwell = [sp.cancel(sum(sp.diff(sqrtmg * Fup[m, n], coords[m]) for m in range(4))) for n in range(4)]
print("  ∂_μ(√-g F^{μν}) =", maxwell, "(équations de Maxwell sans source)")
print("  invariant F_{μν}F^{μν} =", sp.factor(F2))
print(f"  [temps écoulé {time.time()-t0:.0f} s]")

print("\n[A2] Kerr (Q = 0) : tenseur de Ricci")
RicK = Ric.subs(Q, 0).applyfunc(sp.cancel)
print("  R_{μν}(Q=0) =", "0 (vérifié)" if RicK == sp.zeros(4, 4) else RicK)

print("\n[A3] Coefficient g_φφ et région à CTC")
gpp = sp.factor(g[3, 3])
print("  g_φφ =", gpp)
gpp_eq = sp.cancel(g[3, 3].subs(x, 0))
print("  plan équatorial (x = 0) : g_φφ =", sp.expand(gpp_eq), " = r² + a² + a²(2Mr - Q²)/r²")
assert sp.simplify(gpp_eq - (r**2 + a**2 + a**2 * (2 * M * r - Q**2) / r**2)) == 0
print("  Kerr (Q=0), r>0 : g_φφ = r² + a² + 2Ma²/r > 0 ; pour r<0 petit : 2Ma²/r -> -∞ : g_φφ < 0  => ∂_φ de genre temps (CTC)")
print("  Kerr-Newman (Q≠0) : -a²Q²/r² domine quand r -> 0 des DEUX côtés : CTC aussi pour r > 0 petit")
# exemple numérique, M = 1
for (aa, QQ) in ((0.9, 0.0), (0.6, 0.6)):
    f = sp.lambdify(r, gpp_eq.subs({M: 1, a: aa, Q: QQ}), "math")
    vals = ", ".join(f"r={rr:+.2f}: {f(rr):+.3f}" for rr in (-1.0, -0.5, -0.2, -0.05, 0.05, 0.2, 0.5, 1.0))
    print(f"   a={aa}, Q={QQ} (M=1) : g_φφ(équateur) -> {vals}")
# bord de la région CTC côté r<0 pour Kerr : r³ + a² r + 2 M a² = 0
for aa in (0.5, 0.9, 0.998):
    racines = sp.Poly(r**3 + aa**2 * r + 2 * aa**2, r).nroots()
    rr = [float(sp.re(z)) for z in racines if abs(sp.im(z)) < 1e-12]
    print(f"   Kerr a/M={aa} : g_φφ(équateur) < 0 pour {rr[0]:.4f} M < r < 0")

print("\n[A4] Horizons, ergosphère, thermodynamique (unités géométriques)")
rp = M + sp.sqrt(M**2 - a**2 - Q**2)
rm = M - sp.sqrt(M**2 - a**2 - Q**2)
print("  r± = M ± sqrt(M² - a² - Q²) ; r+ r- = a² + Q² ; r+ + r- = 2M")
print("  d r-/dQ =", sp.simplify(sp.diff(rm, Q)), " (> 0 : ajouter de la charge agrandit l'horizon interne)")
print("  d r+/dQ =", sp.simplify(sp.diff(rp, Q)), " (< 0 : et réduit l'horizon externe)")
print("  ergosphère (g_tt = 0) : r_E(θ) = M + sqrt(M² - Q² - a² cos²θ)")
gtt_num = sp.cancel(-(g[0, 0]) * Sigma)
print("   contrôle : -g_tt Σ =", sp.expand(gtt_num))
A_h = 4 * sp.pi * (rp**2 + a**2)
kappa = (rp - rm) / (2 * (rp**2 + a**2))
print("  aire A = 4π(r+² + a²) ; gravité de surface κ = (r+ - r-)/(2(r+² + a²)) ; T = κ/2π (-> 0 à l'extrémalité)")
print("   contrôle Schwarzschild : κ =", sp.simplify(kappa.subs({a: 0, Q: 0})), "(= 1/4M)")
Mirr2 = A_h / (16 * sp.pi)
print("  masse irréductible M_irr² = A/16π :")
print("   Kerr extrémal (a=M, Q=0)  : M_irr/M =", sp.nsimplify(sp.sqrt(Mirr2.subs(Q, 0)).subs(a, M) / M), "-> énergie de rotation extractible ≤", f"{(1-1/math.sqrt(2))*100:.1f} %")
MirrRN = sp.sqrt(sp.simplify(Mirr2.subs(a, 0))).subs(Q, M)
print("   RN extrémal (Q=M, a=0)    : M_irr/M =", sp.nsimplify(sp.simplify(MirrRN / M)), "-> énergie électrostatique = 50 % de M c²")
print(f"  [temps écoulé {time.time()-t0:.0f} s]")

print("\n[A5] Aucune anomalie causale hors de l'horizon externe : t est une fonction de temps globale pour r > r+")
num_gtt = (r**2 + a**2) ** 2 - Delta * a**2 * s2          # g^{tt} = -num_gtt / (Δ Σ)
assert sp.cancel(ginv[0, 0] + num_gtt / (Delta * Sigma)) == 0
decomp = r**2 * (r**2 + a**2) + a**2 * (2 * M * r - Q**2) + Delta * a**2 * x**2
print("  g^{tt} = -N/(ΔΣ) avec N = (r²+a²)² - Δ a² sin²θ = r²(r²+a²) + a²(2Mr - Q²) + Δ a² cos²θ :",
      "identité vérifiée" if sp.expand(num_gtt - decomp) == 0 else "ÉCHEC")
print("  pour r > r+ : Δ > 0 et 2Mr - Q² > 2M r+ - Q² = r+² + a² > 0, donc N > 0 et g^{tt} < 0 :")
print("  le gradient de t est partout de genre temps ; t croît strictement le long de toute courbe causale dirigée vers le futur.")
print("  => la région extérieure (r > r+) est stablement causale : AUCUNE courbe temporelle fermée n'y passe.")
import random
random.seed(2)
pire = 1e99
for _ in range(20000):
    aa = random.uniform(0.0, 0.999)
    QQ = random.uniform(0.0, math.sqrt(1 - aa**2) * 0.999)
    rplus = 1 + math.sqrt(1 - aa**2 - QQ**2)
    rr = rplus * (1 + 10 ** random.uniform(-6, 3))
    xx_ = random.uniform(-1, 1)
    De = rr**2 - 2 * rr + aa**2 + QQ**2
    Nn = (rr**2 + aa**2) ** 2 - De * aa**2 * (1 - xx_**2)
    pire = min(pire, Nn / rr**4)
print(f"  balayage numérique (20 000 points, 0 ≤ a, Q, a²+Q² < M², r > r+) : min de N/r⁴ = {pire:.3f} > 0")
print(f"  [temps écoulé {time.time()-t0:.0f} s]")

print("\n[A6] Sans hypothèse d'horizon (correction n° 19) : temps de Kerr-Schild  dt_KS = dt + (2Mr - Q²)/Δ dr")
gtt_KS = sp.cancel(ginv[0, 0] + ((2 * M * r - Q**2) / Delta) ** 2 * ginv[1, 1])
ident = sp.cancel(gtt_KS + 1 + (2 * M * r - Q**2) / Sigma)
print("  g^{tt}_KS = g^{tt} + [(2Mr - Q²)/Δ]² g^{rr} = -(1 + (2Mr - Q²)/Σ) :", "identité vérifiée" if ident == 0 else ident)
print("  => t_KS est une fonction temporelle partout où Σ + 2Mr - Q² > 0, y compris sur le feuillet r < 0 et SANS horizon ;")
print("     elle ne cesse de l'être que dans le tube (r + M)² + a² cos²θ <= M² + Q² entourant l'anneau (taille fixée par M et Q, pas par a).")
print("     Toute courbe causale fermée d'un Kerr-Newman sur-extrémal doit donc traverser ce tube.")
print(f"  [temps écoulé {time.time()-t0:.0f} s]")

# ----------------------------------------------------------------------------
# Partie B — ordres de grandeur
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("Partie B — ordres de grandeur (SI)")
print("-" * 78)
print(f"{'M (kg)':>11} {'r_g=GM/c² (m)':>14} {'a_max=r_g (m)':>14} {'J_max (J s)':>12} {'J_max/hbar':>11} {'Ω_H extr. (rad/s)':>18} {'hbar Ω_H':>12} {'t_traversée r_g/c (s)':>22}")
for Mk in (113.5, 227.0, 1e9, 1e12, 4e12, M_terre, M_jupiter, M_soleil):
    rg = G * Mk / c**2
    J = G * Mk**2 / c
    OmH = c / (2 * rg)
    E = hbar * OmH / eV
    Es = f"{E/1e9:.3g} GeV" if E > 1e9 else (f"{E/1e6:.3g} MeV" if E > 1e6 else f"{E:.3g} eV")
    print(f"{Mk:>11.4g} {rg:>14.3e} {rg:>14.3e} {J:>12.3e} {J/hbar:>11.2e} {OmH:>18.3e} {Es:>12} {rg/c:>22.3e}")

print("\nRayon de l'anneau singulier (rayon coordonné a ≤ GM/c²) : masse minimale pour un anneau de rayon donné")
for rayon in (1e-15, 1e-10, 1e-3, 1.0, 2.0, 3.7):
    Mmin = rayon * c**2 / G
    print(f"  a = {rayon:.3g} m -> M ≥ {Mmin:.3e} kg = {Mmin/M_terre:.3g} M_Terre = {Mmin/M_jupiter:.3g} M_Jupiter ;"
          f" énergie de masse {Mmin*c**2:.2e} J")

print("\nMarées à l'horizon de Schwarzschild : accélération différentielle 2GM L/r_s³ = c^6 L /(4 G² M²)")
for Mk in (227.0, 1e12, 1.35e27, M_soleil, 4.3e6 * M_soleil):
    grad = c**6 / (4 * G**2 * Mk**2)
    print(f"  M = {Mk:.3e} kg : {grad:.3e} s^-2  -> sur 1 m : {grad/g0:.2e} g ; sur 1 fm : {grad*1e-15/g0:.2e} g")

print("\nHorizon interne dû à la charge (Reissner-Nordström) : r- ≈ r_Q²/r_s, r_Q² = G Q²/(4π ε0 c^4)")
for Mk in (1e12, 4e12):
    rs = 2 * G * Mk / c**2
    Qext = Mk * math.sqrt(4 * math.pi * eps0 * G)
    for nom, Qc in (("1 e", e), ("6,14 e (rms, Page 1977)", 6.14 * e), ("137 e (borne ≈ e/α)", e / alpha), ("1 µC", 1e-6), ("1 C", 1.0), (f"extrémale {Qext:.1f} C", Qext)):
        rQ2 = G * Qc**2 / (4 * math.pi * eps0 * c**4)
        disc = (rs / 2) ** 2 - rQ2
        rmoins = rs / 2 - math.sqrt(max(disc, 0.0)) if rQ2 > 1e-12 * (rs / 2) ** 2 else rQ2 / rs
        print(f"  M = {Mk:.0e} kg, Q = {nom:>24} : r- = {rmoins:.3e} m  (r- / l_Planck = {rmoins/l_planck:.2e} ; r-/r_s = {rmoins/rs:.2e})")

print("\nCoût énergétique de la charge : pour un RN extrémal, la moitié de M c² est électrostatique")
for Mk in (113.5, 1e12):
    Qext = Mk * math.sqrt(4 * math.pi * eps0 * G)
    rg = G * Mk / c**2
    V = Qext / (4 * math.pi * eps0 * rg)
    print(f"  M = {Mk:.4g} kg : Q_ext = {Qext:.3e} C = {Qext/e:.2e} e ; potentiel à l'horizon = {V:.3e} V ;"
          f" énergie par électron injecté (fin de charge) = {e*V:.3e} J ; énergie électrostatique totale = {0.5*Mk*c**2:.3e} J ;"
          f" masse au repos des électrons = {Qext/e*m_e:.3e} kg")

print("\nMoment magnétique d'un trou noir de Kerr-Newman (g = 2) : μ = Q J / M = Q a c")
for Mk in (1e12,):
    rg = G * Mk / c**2
    for nom, Qc in (("6,14 e (typique)", 6.14 * e), ("137 e (borne)", e / alpha), ("extrémale-moitié 61 C", Mk * math.sqrt(4 * math.pi * eps0 * G) / math.sqrt(2))):
        aa = rg / math.sqrt(2) if nom.startswith("extr") else rg
        mu = Qc * aa * c
        J = Mk * aa * c
        B = 10.0
        print(f"  M = {Mk:.0e} kg, Q = {nom} : μ = {mu:.3e} A m² ({mu/9.2740100783e-24:.3g} magnétons de Bohr) ;"
              f" dans B = {B} T : couple {mu*B:.2e} N m ; vitesse de précession μB/J = {mu*B/J:.2e} rad/s")

print(f"\nTemps de calcul : {time.time()-t0:.0f} s")
