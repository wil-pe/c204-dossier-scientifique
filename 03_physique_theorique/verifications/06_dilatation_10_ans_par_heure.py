#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 06 : « 10 ans par heure » = facteur de dilatation Γ = dt/dτ ≈ 87 660.

  D1. voie cinématique (relativité restreinte) : vitesse, énergie, durée d'accélération
  D2. voie gravitationnelle (Schwarzschild, observateur statique) : r/r_s, accélération propre
  D3. identité exacte (espace-temps statique) : accélération propre des observateurs statiques
      a = c² |∇ ln N|   (vérification symbolique) ; conséquence : ln Γ ≤ ∫ a dl / c²
      -> incompatibilité interne entre « 1,5-2 g », « zone de 3-4 m » et « 10 ans/heure »
  D4. intérieur d'une coquille mince (conditions de jonction d'Israel) : condition d'énergie
      dominante => Γ ≤ 5 ; étoile de densité constante : p_c ≤ ρ c² => Γ_centre ≤ 4
  D5. repères expérimentaux
"""
import math

import sympy as sp

from constantes import *

print("=" * 78)
print("SCRIPT 06 — « 10 ans par heure » : Γ = dt/dτ")
print("=" * 78)

Gam = 10 * 365.25 * 24.0
print(f"\nΓ = 10 ans / 1 h = {Gam:.0f}   ;   ln Γ = {math.log(Gam):.4f}")

# ---------------------------------------------------------------- D1
print("\n[D1] Voie cinématique : Γ = γ = (1 - v²/c²)^(-1/2)")
un_moins_beta = 1 / (2 * Gam**2)
print(f"  1 - v/c = {un_moins_beta:.3e}  (v = c - {un_moins_beta*c*100:.2f} cm/s)")
print(f"  énergie cinétique par kilogramme : (γ - 1) c² = {(Gam-1)*c**2:.3e} J/kg")
E_monde = 6.0e20   # J/an, ordre de grandeur de la consommation mondiale d'énergie primaire (≈ 600 EJ/an)
L_soleil = 3.828e26
for m in (227.0, 2500.0):
    E = (Gam - 1) * m * c**2
    print(f"  m = {m:.0f} kg : E_c = {E:.3e} J = {E/TNT_tonne/1e9:.2e} Gt TNT = {E/E_monde:.2e} années de consommation mondiale"
          f" (~6e20 J/an) = {E/L_soleil:.3f} s de luminosité solaire")
a2g = 2 * g0
tau_acc = c / a2g * math.acosh(Gam)
print(f"  à accélération propre constante de 2 g, atteindre γ = Γ demande τ = (c/a) acosh Γ = {tau_acc:.3e} s = {tau_acc/an:.2f} ans de temps propre")
tau = 3600.0
x = a2g * tau / c
dt = c / a2g * math.sinh(x)
print(f"  inversement, 1 h de temps propre à 2 g constants : t_ext - τ = {dt - tau:.3e} s (≈ τ (aτ/c)²/6 = {tau*x*x/6:.3e} s), pas 10 ans")

# ---------------------------------------------------------------- D2
print("\n[D2] Voie gravitationnelle : observateur statique de Schwarzschild, Γ = (1 - r_s/r)^(-1/2)")
eps = 1 / (Gam**2 - 1)
print(f"  r/r_s - 1 = 1/(Γ² - 1) = {eps:.3e}")
for M, nom in ((1e12, "1e12 kg"), (M_terre, "Terre"), (M_soleil, "Soleil"), (4.3e6 * M_soleil, "Sgr A*")):
    rs = 2 * G * M / c**2
    r = rs * (1 + eps)
    a = G * M / r**2 * Gam
    print(f"  M = {nom:>8} : r_s = {rs:.3e} m ; station à {rs*eps:.3e} m au-dessus de l'horizon ; accélération propre requise = {a:.3e} m/s² = {a/g0:.2e} g")
print("  (la surface d'une étoile à neutrons donne Γ ≈ 1,2-1,3 ; aucune station statique ne s'approche de Γ ~ 1e5)")

# ---------------------------------------------------------------- D3
print("\n[D3] Identité a = c² ∇ ln N pour un observateur statique (métrique statique quelconque, partie spatiale diagonale)")
t, x1, x2, x3 = sp.symbols("t x1 x2 x3", real=True)
N = sp.Function("N", positive=True)(x1, x2, x3)
h1 = sp.Function("h1", positive=True)(x1, x2, x3)
h2 = sp.Function("h2", positive=True)(x1, x2, x3)
h3 = sp.Function("h3", positive=True)(x1, x2, x3)
coords = [t, x1, x2, x3]
g = sp.diag(-N**2, h1, h2, h3)
gi = g.inv()
# a^μ = Γ^μ_tt (u^t)², u^t = 1/N ; a_i = g_ii a^i
acc_bas = []
for i in range(1, 4):
    Gam_i_tt = sp.Rational(1, 2) * gi[i, i] * (-sp.diff(g[0, 0], coords[i]))
    a_haut = Gam_i_tt / N**2
    acc_bas.append(sp.simplify(g[i, i] * a_haut - sp.diff(sp.log(N), coords[i])))
print("  a_i - ∂_i ln N =", acc_bas, " -> identité vérifiée (c = 1)")
print("  Conséquence : entre deux horloges statiques A et B, ln(N_B/N_A) = ∫_A^B ∇ln N · dl  ≤  ∫ |a| dl / c²")
for L in (3.0, 3.7):
    for ng in (1.5, 2.0):
        borne = ng * g0 * L / c**2
        print(f"   |a| ≤ {ng} g sur L = {L} m  =>  Γ - 1 ≤ {borne:.2e}   (revendiqué : 8,8e4)")
for L in (3.0, 3.7):
    amoy = c**2 * math.log(Gam) / L
    print(f"   pour ln Γ = {math.log(Gam):.2f} sur L = {L} m : accélération moyenne requise = {amoy:.2e} m/s² = {amoy/g0:.1e} g")
L_rindler = c**2 * math.log(Gam) / (2 * g0)
print(f"   à 2 g uniformes, la profondeur de champ nécessaire serait c² ln Γ / a = {L_rindler:.2e} m = {L_rindler/(c*an):.2f} années-lumière")

# ---------------------------------------------------------------- D4
print("\n[D4] Bornes par les conditions d'énergie (G = c = 1)")
k = sp.symbols("k", positive=True)      # k = sqrt(1 - 2M/R) = facteur de lapse à la surface = 1/Γ_intérieur
Rr = sp.symbols("R", positive=True)
# coquille mince statique de rayon R : intérieur plat, extérieur Schwarzschild (jonction d'Israel)
sigma = (1 - k) / (4 * sp.pi * Rr)
MsurR = (1 - k**2) / 2
p = ((1 - MsurR) / k - 1) / (8 * sp.pi * Rr)
print("  coquille mince : σ = (1 - k)/(4πR) ; p = [(1 - M/R)/k - 1]/(8πR) =", sp.simplify(p), " avec k = sqrt(1 - 2M/R)")
print("   p/σ =", sp.simplify(p / sigma))
sol = sp.solve(sp.Eq(sp.simplify(p / sigma), 1), k)
print("   condition d'énergie dominante p ≤ σ  <=>  k ≥", sol, " =>  Γ_intérieur = 1/k ≤ 5  (R ≥ 25/24 r_s)")
# étoile de densité constante (Schwarzschild intérieur)
Nc = (3 * k - 1) / 2
pc_sur_rho = (1 - k) / (3 * k - 1)
solk = sp.solve(sp.Eq(pc_sur_rho, 1), k)
print("  étoile homogène : lapse central N_c = (3k - 1)/2 ; p_c/ρ = (1 - k)/(3k - 1) ; p_c ≤ ρ  <=>  k ≥", solk,
      " => Γ_centre = 1/N_c ≤", 1 / Nc.subs(k, solk[0]))
print("   (borne de Buchdahl : p_c -> ∞ quand k -> 1/3, soit R -> 9/8 r_s ; Γ de surface ≤ 3)")
for Rm in (3.7,):
    Mshell = Rm * c**2 / (2 * G) * (1 - 1 / 25)
    print(f"  coquille limite (Γ = 5) de rayon {Rm} m : M = {Mshell:.2e} kg = {Mshell/M_jupiter:.2f} M_Jupiter ; densité surfacique d'énergie σ c² = pression de surface = "
          f"{(1-0.2)/(4*math.pi*Rm)*c**4/G:.2e} J/m² (N/m)")

# ---------------------------------------------------------------- D5
print("\n[D5] Repères expérimentaux (dilatation du temps réellement mesurée)")
print(f"  électron de 45,6 GeV (LEP, pôle du Z) : γ = {45.6e9/510998.95:.0f}  <- du même ordre que Γ = 87 660")
print(f"  proton de 6,8 TeV (LHC)               : γ = {6.8e12/938.272e6:.0f}")
print(f"  muons de l'anneau du CERN (Bailey et al. 1977) : γ ≈ 29,3")
print(f"  rayon cosmique de 3e20 eV (proton)    : γ ≈ {3e20/938.272e6:.1e}")
phi_sol = G * M_terre / (6.371e6 * c**2)
print(f"  surface de la Terre : GM/(Rc²) = {phi_sol:.2e} ; gradient g/c² = {g0/c**2:.3e} par mètre (mesuré jusqu'à l'échelle du mm : Bothwell et al. 2022)")
h_gps = 20.2e6
v_gps = math.sqrt(G * M_terre / (6.371e6 + h_gps))
grav = G * M_terre / c**2 * (1 / 6.371e6 - 1 / (6.371e6 + h_gps))
cin = v_gps**2 / (2 * c**2)
print(f"  GPS (h = 20 200 km) : +{grav*86400*1e6:.1f} µs/j (gravitation) - {cin*86400*1e6:.1f} µs/j (vitesse) = +{(grav-cin)*86400*1e6:.1f} µs/j")
print("  Dans tous les cas dτ > 0 et dt > 0 : la dilatation change le RYTHME, jamais le SENS.")
