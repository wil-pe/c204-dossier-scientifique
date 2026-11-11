#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 07 : le champ électromagnétique comme source de gravité ; énergie négative.

  E1. univers magnétique de Melvin : vérification symbolique des équations d'Einstein-Maxwell
      (Reissner-Nordström est couvert par le script 03, cas a = 0)
  E2. intensité de champ nécessaire pour une courbure à l'échelle L : B = c² sqrt(μ0/4πG) / L
      tableau pour les champs réels (laboratoire, astres), limite de Schwinger
  E3. anneau laser (Mallett) : ordre de grandeur de l'entraînement des référentiels
  E4. effet Casimir : densité d'énergie et pression ; inégalité quantique de Ford-Roman ;
      besoin d'un trou de ver de gorge 1 m
  E5. bulle d'Alcubierre : densité d'énergie dérivée de la contrainte hamiltonienne (sympy),
      énergie totale E = -(c⁴/12G)(v/c)² (R²/Δ + Δ/12)
"""
import math

import sympy as sp

from constantes import *

print("=" * 78)
print("SCRIPT 07 — Champs électromagnétiques et gravité ; énergie négative")
print("=" * 78)

# ---------------------------------------------------------------- E1
print("\n[E1] Univers magnétique de Melvin (G = c = 1, unités gaussiennes géométrisées)")
t, ph, z = sp.symbols("t phi z", real=True)
rho = sp.symbols("rho", positive=True)
B = sp.symbols("B", positive=True)
coords = [t, rho, ph, z]
Lam = 1 + B**2 * rho**2 / 4
g = sp.diag(-Lam**2, Lam**2, rho**2 / Lam**2, Lam**2)
gi = g.inv()
n = 4
Gam = [[[0] * n for _ in range(n)] for _ in range(n)]
for i in range(n):
    for j in range(n):
        for k in range(j, n):
            e_ = 0
            for l in range(n):
                if gi[i, l] != 0:
                    e_ += gi[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
            Gam[i][j][k] = Gam[i][k][j] = sp.cancel(e_ / 2)
Ric = sp.zeros(n, n)
for j in range(n):
    for k in range(j, n):
        e_ = 0
        for i in range(n):
            e_ += sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k])
            for l in range(n):
                e_ += Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i]
        Ric[j, k] = Ric[k, j] = sp.cancel(sp.together(e_))
A = [0, 0, B * rho**2 / (2 * Lam), 0]
F = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        F[i, j] = sp.diff(A[j], coords[i]) - sp.diff(A[i], coords[j])
Fup = (gi * F * gi).applyfunc(sp.cancel)
F2 = sp.cancel(sum(F[i, j] * Fup[i, j] for i in range(4) for j in range(4)))
Fmix = (F * gi).applyfunc(sp.cancel)
T = sp.zeros(4, 4)
for i in range(4):
    for j in range(4):
        T[i, j] = sp.cancel(2 * (sum(Fmix[i, k] * F[j, k] for k in range(4)) - sp.Rational(1, 4) * g[i, j] * F2))
res = (Ric - T).applyfunc(sp.cancel)
print("  ds² = Λ²(-dt² + dρ² + dz²) + ρ²/Λ² dφ²,  Λ = 1 + B²ρ²/4,  A_φ = Bρ²/(2Λ)")
print("  R_{μν} - 2(F_{μα}F_ν^α - ¼ g_{μν}F²) =", "0 (vérifié)" if res == sp.zeros(4, 4) else res)
sqrtmg = sp.simplify(sp.sqrt(-g.det()))
maxw = [sp.cancel(sum(sp.diff(sqrtmg * Fup[m, nn], coords[m]) for m in range(4))) for nn in range(4)]
print("  Maxwell : ∂_μ(√-g F^{μν}) =", maxw)
circ = 2 * sp.pi * rho / Lam
rho_max = sp.solve(sp.diff(circ, rho), rho)
print("  circonférence propre 2πρ/Λ maximale en ρ =", rho_max, "(rayon de Melvin ρ_M = 2/B) puis décroissante : la géométrie « se referme »")
print("  champ mesuré localement : B/Λ² ; flux total = ∫F_ρφ dρ dφ =", sp.simplify(sp.integrate(sp.diff(A[2], rho), (rho, 0, sp.oo)) * 2 * sp.pi))

# ---------------------------------------------------------------- E2
print("\n[E2] Intensité de champ et échelle de courbure (SI)")
kB_ = math.sqrt(4 * math.pi * eps0 * G) / c      # B_géom [1/m] = kB_ * B [T]
coefL = c**2 * math.sqrt(mu0 / (4 * math.pi * G))    # L = coefL / B
print(f"  conversion : B_géométrique = sqrt(4π ε0 G)/c × B = {kB_:.3e} m⁻¹ par tesla")
print(f"  échelle de courbure L définie par 8πG u/c⁴ = 1/L², u = B²/2μ0 :  L = c² sqrt(μ0/4πG) / B = {coefL:.3e} m·T / B")
print(f"  rayon de Melvin ρ_M = 2/B_géom = {2/kB_:.3e} m·T / B")
print(f"  {'champ':<46} {'B (T)':>10} {'u (J/m³)':>11} {'u/c² (kg/m³)':>13} {'L (m)':>10} {'L (années-lumière)':>19}")
al = c * an
champs = [
    ("champ terrestre", 5e-5),
    ("IRM clinique", 3.0),
    ("record continu (Hahn et al. 2019)", 45.5),
    ("impulsionnel non destructif (~100 T)", 100.0),
    ("record en laboratoire fermé (Nakamura 2018)", 1200.0),
    ("pulsar ordinaire (~1e8 T)", 1e8),
    ("champ critique de Schwinger B_S", B_schwinger),
    ("magnétar (~1e11 T)", 1e11),
]
for nom, Bt in champs:
    u = Bt**2 / (2 * mu0)
    L = coefL / Bt
    print(f"  {nom:<46} {Bt:>10.3g} {u:>11.3e} {u/c**2:>13.3e} {L:>10.3e} {L/al:>19.3e}")
for L in (1.0, 3.7):
    Bn = coefL / L
    u = Bn**2 / (2 * mu0)
    print(f"  pour L = {L} m : B = {Bn:.3e} T ; E équivalent = cB = {c*Bn:.3e} V/m = {c*Bn/E_schwinger:.1e} E_Schwinger ;"
          f" u = {u:.2e} J/m³ = {u/c**2:.2e} kg/m³ ; énergie dans une sphère de rayon L : {u*4/3*math.pi*L**3:.2e} J"
          f" = {u*4/3*math.pi*L**3/c**2/M_jupiter:.2f} M_Jupiter c²")
uS = eps0 * E_schwinger**2 / 2
print(f"  champ électrique maximal dans le vide (Schwinger, {E_schwinger:.2e} V/m) : u = {uS:.2e} J/m³ -> L ≥ {c**2/math.sqrt(8*math.pi*G*uS):.2e} m")
print("  Effet réel d'un aimant de laboratoire : 45,5 T dans 1 litre")
U = 45.5**2 / (2 * mu0) * 1e-3
print(f"   énergie {U:.2e} J ; masse équivalente {U/c**2:.2e} kg ; à 10 cm : Φ/c² = {G*U/c**2/(0.1*c**2):.1e} ; g = {G*U/c**2/0.01:.1e} m/s²")
print(f"   pression magnétique B²/2μ0 : 45,5 T -> {45.5**2/(2*mu0):.2e} Pa ; 1200 T -> {1200**2/(2*mu0):.2e} Pa (au-delà de la tenue de tout matériau)")
print(f"  potentiel électrostatique donnant une courbure d'ordre 1 : V = c²/sqrt(4π ε0 G) = {c**2/math.sqrt(4*math.pi*eps0*G):.3e} V"
      f" (= sqrt(α) × énergie de Planck / e = {math.sqrt(alpha)*m_planck*c**2/e:.3e} V)")

# ---------------------------------------------------------------- E3
print("\n[E3] Anneau de lumière (Mallett) : entraînement des référentiels au centre, ordre de grandeur Ω ~ 4π G P / (c⁴ R)")
for P, nom in ((1.0, "1 W"), (1e3, "1 kW"), (1e6, "1 MW circulant"), (1e15, "1 PW (laser impulsionnel)")):
    R = 0.1
    Om = 4 * math.pi * G * P / (c**4 * R)
    print(f"  P = {nom:<26} R = {R} m : Ω ~ {Om:.1e} rad/s ; masse linéique de la lumière P/c³ = {P/c**3:.1e} kg/m")
print(f"  comparaison : effet Lense-Thirring de la Terre mesuré par Gravity Probe B ≈ 5,7e-15 rad/s (à ~19 % près)")
print(f"  puissance pour que la masse linéique lumineuse atteigne le seuil de Tipler c²/8G : P = c⁵/(8G) = {c**5/(8*G):.2e} W")

# ---------------------------------------------------------------- E4
print("\n[E4] Effet Casimir (plaques parfaitement conductrices) : u = -π² ħ c /(720 d⁴),  P = -π² ħ c /(240 d⁴)")
for d in (1e-6, 1e-7, 1e-8, 1e-9):
    u = -math.pi**2 * hbar * c / (720 * d**4)
    Pp = -math.pi**2 * hbar * c / (240 * d**4)
    print(f"  d = {d:.0e} m : u = {u:.2e} J/m³ ({u/c**2:.1e} kg/m³) ; pression {Pp:.2e} Pa ; énergie négative par m² de plaques = {u*d:.1e} J/m²")
print(f"  à comparer à l'énergie de masse POSITIVE des plaques elles-mêmes : 1 µm d'or ≈ 0,019 kg/m² = {0.0193*c**2:.1e} J/m² par plaque")
print("  Trou de ver de Morris-Thorne, gorge de rayon b : tension requise τ = c⁴/(8πG b²)")
for b in (1.0, 1e3):
    tau = c**4 / (8 * math.pi * G * b**2)
    d_eq = (math.pi**2 * hbar * c / (720 * tau)) ** 0.25
    tq = (3 * hbar * c / (32 * math.pi**2 * tau)) ** 0.25 / c
    print(f"  b = {b:.0f} m : |ρ| c² ~ τ = {tau:.2e} J/m³ ; écart de plaques Casimir donnant cette densité : d = {d_eq:.1e} m ;"
          f" durée d'échantillonnage maximale permise par l'inégalité quantique pour cette densité : τ0 ≲ {tq:.1e} s ;"
          f" « masse exotique » ~ -b c²/G = {-b*c**2/G:.1e} kg")
print("  Inégalité quantique (champ scalaire sans masse, échantillonnage lorentzien de durée τ0) : <ρ> ≥ -3 ħ /(32 π² c³ τ0⁴)")
for t0_ in (1e-15, 1e-9, 1e-3):
    print(f"   τ0 = {t0_:.0e} s : <ρ> ≥ {-3*hbar/(32*math.pi**2*c**3*t0_**4):.1e} J/m³")

# ---------------------------------------------------------------- E5
print("\n[E5] Bulle d'Alcubierre : densité d'énergie eulérienne par la contrainte hamiltonienne (tranches plates)")
xx, yy, zz, v = sp.symbols("x y z v", real=True)
f = sp.Function("f")
r_s = sp.sqrt(xx**2 + yy**2 + zz**2)
beta = sp.Matrix([-v * f(r_s), 0, 0])                # vecteur de décalage (au temps où la bulle est centrée à l'origine)
X = [xx, yy, zz]
K = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        K[i, j] = sp.Rational(1, 2) * (sp.diff(beta[i], X[j]) + sp.diff(beta[j], X[i]))   # au signe près (sans effet sur K² - K_ij K^ij)
trK = K.trace()
rhoE = sp.simplify((trK**2 - sum(K[i, j] ** 2 for i in range(3) for j in range(3))) / (16 * sp.pi))
print("  ρ_E = (K² - K_ij K^ij)/16π =", rhoE)
print("   = -(v²/32π) (y² + z²)/r² (df/dr)²  ≤ 0 partout  (Alcubierre 1994)")
print("  intégrale : E = -(v²/12) ∫ r² f'(r)² dr ; profil linéaire d'épaisseur Δ : E = -(v²/12)(R²/Δ + Δ/12)   [G = c = 1]")
rr, Rb, Dl = sp.symbols("r R Delta", positive=True)
I = sp.integrate(rr**2 / Dl**2, (rr, Rb - Dl / 2, Rb + Dl / 2))
print("   contrôle : ∫ r² f'² dr =", sp.expand(I))
for Rm, Dm in ((3.7, 1.0), (3.7, 0.01), (3.7, 100 * l_planck)):
    E = -(c**4 / (12 * G)) * (Rm**2 / Dm + Dm / 12)
    print(f"  R = {Rm} m, Δ = {Dm:.3g} m, v = c : E = {E:.2e} J = {E/c**2:.2e} kg = {E/c**2/M_soleil:.2e} M_soleil")
print("  (Δ ~ 100 longueurs de Planck est l'épaisseur maximale compatible avec l'inégalité quantique selon Pfenning & Ford 1997)")
