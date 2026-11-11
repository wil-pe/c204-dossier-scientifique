#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 05 : « deux micro-trous noirs en rotation » — que produisent-ils réellement
à l'échelle du mètre ?

  B1. champ faible à r = 1-4 m pour M de 100 kg à 5e12 kg : potentiel, pesanteur, marée,
      dilatation du temps, entraînement des référentiels dû au SPIN d'un trou isolé (spin extrémal)
  B2. masse nécessaire pour un facteur de dilatation donné à une distance donnée
  B3. binaire en orbite : pulsation, vitesse, puissance gravitationnelle (quadrupôle),
      temps de coalescence de Peters (1964), « sinusoïde » newtonienne de champ proche à 2ω ;
      séparations : 0,098 m (entraxe documentaire, Équipe A, [DÉD] confiance faible) et 0,30 m ([HYP])
  B3bis. entraînement des référentiels dû au moment cinétique ORBITAL de la paire (correction n° 17)
  B4. équilibre statique : Majumdar-Papapetrou (Q = M sqrt(4π ε0 G)) et limite de Schwinger ;
      charge maximale tenable par un micro-trou noir ; force de « strut » ; interaction spin-spin
  B5. cordes de Gott : contrôle numérique de la condition γ sin(4πGμ/c²) > 1 par holonomie SO(2,1)
  B6. cohérence « 300-500 MW » / « 1,5-2 g » selon le nombre de singularités (correction n° 18)
"""
import math

import numpy as np

from constantes import *

print("=" * 78)
print("SCRIPT 05 — Deux trous noirs : champs réels à l'échelle du mètre")
print("=" * 78)

# ---------------------------------------------------------------- B1
print("\n[B1] Champ d'UN trou noir de masse M à la distance r (champ faible ; pour deux trous noirs, additionner)")
print(f"{'M (kg)':>9} {'r (m)':>6} {'Φ/c² = GM/rc²':>14} {'g = GM/r² (m/s²)':>17} {'g/g0':>10} {'marée 2GM/r³ (s⁻²)':>19} "
      f"{'retard d horloge (s/heure)':>27} {'Ω spin seul (rad/s)':>20}")
for M in (100.0, 227.0, 1e6, 1e9, 1e12, 5e12):
    for r in (1.0, 4.0):
        phi = G * M / (r * c**2)
        g = G * M / r**2
        maree = 2 * G * M / r**3
        J = G * M**2 / c                       # spin extrémal
        omega_LT = 2 * G * J / (c**2 * r**3)   # sur l'axe : Ω = 2GJ/(c² r³)
        print(f"{M:>9.3g} {r:>6.1f} {phi:>14.3e} {g:>17.3e} {g/g0:>10.3e} {maree:>19.3e} {phi*3600:>27.3e} {omega_LT:>20.3e}")
print("  (Ω spin seul : spin extrémal d'un trou ISOLÉ ; le terme orbital d'une paire, bien plus grand, est en [B3bis].)")
print("  Référence : meilleure exactitude d'horloge optique publiée ~1e-18 ; Gravity Probe B a mesuré 37 mas/an = "
      f"{37e-3/3600*math.pi/180/an:.2e} rad/s pour la Terre entière.")
print(f"  Rapport revendiqué dt/dτ - 1 = 87 659 ; rapport réel pour 1e12 kg à 1 m : {G*1e12/c**2:.1e}  -> écart de "
      f"{math.log10(87659/(G*1e12/c**2)):.0f} ordres de grandeur.")

# ---------------------------------------------------------------- B2
print("\n[B2] Masse (Schwarzschild, observateur statique) donnant un facteur de dilatation Γ = dt/dτ à la distance r")
print("     Γ = (1 - r_s/r)^(-1/2)  =>  M = (r c² / 2G) (1 - Γ⁻²)")
for eps_ in (1e-15, 1e-9, 1e-3, 1.0, 87659.0):          # eps_ = Γ - 1
    for r in (1.0, 3.7):
        Gam = 1 + eps_
        un_moins = eps_ * (2 + eps_) / Gam**2            # 1 - Γ⁻² sans perte de précision
        M = r * c**2 / (2 * G) * un_moins
        acc = G * M / r**2 * Gam               # accélération propre de l'observateur statique
        print(f"  Γ - 1 = {eps_:<8.3g} r = {r:>3} m : M = {M:.3e} kg ({M/M_terre:.3g} M_Terre) ; accélération propre pour rester statique = {acc/g0:.3e} g")

# ---------------------------------------------------------------- B3
D_DOC = 0.098     # entraxe des deux logements, Équipe A (02_reconstruction/dimensions.json : 0,098 ± 0,025 m, [DÉD], confiance faible)
D_HYP = 0.30      # séparation utilisée dans la version 1 du rapport : [HYP] de l'Équipe B
print("\n[B3] Binaire circulaire de deux masses égales M séparées de d")
print(f"     d = {D_DOC} m : entraxe documentaire (Équipe A, [DÉD], confiance faible) ; d = {D_HYP} m : [HYP] de la version 1")
print(f"{'M (kg)':>9} {'d (m)':>6} {'ω orb (rad/s)':>14} {'v (m/s)':>10} {'P_GW (W)':>11} {'t Peters (s)':>13} {'t Peters (ans)':>15} {'t Peters / âge univers':>23} "
      f"{'force mutuelle (N)':>19} {'δΦ/c² à 2ω, r=2 m':>19}")
age_univers = 13.8e9 * an
for M in (113.5, 1e9, 1e12, 4.4e12, 5e12):
    for d in (D_DOC, D_HYP):
        Mt = 2 * M
        om = math.sqrt(G * Mt / d**3)
        v = om * d / 2
        P = (32 / 5) * G**4 * (M * M) ** 2 * Mt / (c**5 * d**5)
        tP = (5 / 256) * c**5 * d**4 / (G**3 * M * M * Mt)
        F = G * M * M / d**2
        dphi = 3 * G * M * d**2 / (8 * 2.0**3) / c**2      # amplitude du terme en cos 2(φ - ωt) à r = 2 m
        print(f"{M:>9.3g} {d:>6.3f} {om:>14.3e} {v:>10.3e} {P:>11.3e} {tP:>13.3e} {tP/an:>15.3e} {tP/age_univers:>23.3e} {F:>19.3e} {dphi:>19.3e}")
print("  Champ proche newtonien (la seule « sinusoïde » réelle de deux masses en rotation) :")
print("    Φ(r, φ, t) = -2GM/r - (G M d²/4r³)(3cos²ψ - 1),  ψ = φ - ωt  ->  terme oscillant -(3 G M d²/8r³) cos 2(φ - ωt)")
print("  Pour que la coalescence prenne ~1 heure avec d = 0,3 m il faudrait M ≈ "
      f"{((5/256)*c**5*0.3**4/(G**3*2*3600))**(1/3):.2e} kg par trou noir.")

# ---------------------------------------------------------------- B3bis
print("\n[B3bis] Entraînement des référentiels par le moment cinétique ORBITAL de la paire (moyenne temporelle)")
print("     J_orb = 2 M (d/2)² ω = M d² ω / 2 ;  sur l'axe, à la hauteur z (analogue gravitomagnétique d'une spire) :")
print("     Ω(z) = 2 G J_orb / [c² (d²/4 + z²)^(3/2)]  ->  2 G J / (c² z³) à grande distance ; plan orbital : -G J/(c² r³)")
print(f"{'M (kg)':>9} {'d (m)':>6} {'J_orb (J s)':>12} {'J_orb / J_spin max':>19} {'Ω orb, z=1 m (rad/s)':>21} {'Ω orb, z=4 m (rad/s)':>21} {'Ω spin seul, 1 m':>17} {'h_0φ ~ Ω z / c (1 m)':>21}")
omega_GPB = 37e-3 / 3600 * math.pi / 180 / an
for M in (1e12, 3.918e12, 4.4e12, 5.058e12):
    for d in (D_DOC, D_HYP):
        om = math.sqrt(2 * G * M / d**3)
        J_orb = M * d**2 * om / 2
        J_spin = G * M**2 / c
        Om1 = 2 * G * J_orb / (c**2 * (d**2 / 4 + 1.0) ** 1.5)
        Om4 = 2 * G * J_orb / (c**2 * (d**2 / 4 + 16.0) ** 1.5)
        Oms = 2 * G * J_spin / c**2
        print(f"{M:>9.4g} {d:>6.3f} {J_orb:>12.3e} {J_orb/J_spin:>19.2e} {Om1:>21.3e} {Om4:>21.3e} {Oms:>17.3e} {Om1*1.0/c:>21.2e}")
print(f"  Comparaison : Gravity Probe B, Terre entière : {omega_GPB:.2e} rad/s. Le terme orbital d'une paire de quelques 1e12 kg est du même")
print("  ordre ou jusqu'à ~10 fois plus grand ; le terme de spin d'un trou isolé est 1e7 fois plus petit.")
print("  Portée causale : nulle. La composante de métrique associée, h_0φ ~ Ω z / c ~ 1e-22, reste << 1/8 (proposition D3 b).")

# ---------------------------------------------------------------- B4
print("\n[B4] Équilibre statique de deux trous noirs")
qm = math.sqrt(4 * math.pi * eps0 * G)
print(f"  Majumdar-Papapetrou : Q/M = sqrt(4π ε0 G) = {qm:.4e} C/kg (répulsion électrostatique = attraction newtonienne, à toute distance)")
M = 1e12
Q = qm * M
print(f"   contrôle : F_e/F_g = {Q**2/(4*math.pi*eps0)/(G*M**2):.6f}")
rg = G * M / c**2
E_h = Q / (4 * math.pi * eps0 * rg**2)
print(f"  Champ électrique à l'horizon d'un trou noir extrémal de {M:.0e} kg : {E_h:.3e} V/m = {E_h/E_schwinger:.2e} × champ de Schwinger")
M_crit = c**4 / (G**1.5 * math.sqrt(4 * math.pi * eps0) * E_schwinger)
print(f"  Masse au-dessus de laquelle le champ d'horizon d'un RN extrémal passe sous le champ de Schwinger : {M_crit:.2e} kg = {M_crit/M_soleil:.1e} M_soleil")
print("   (ordre de grandeur de Gibbons 1975 : ~1e5 M_soleil ; en dessous, la charge fuit par création de paires e+e-)")
Zmax = 1 / alpha
print(f"  Micro-trou noir (r_s << longueur de Compton de l'électron, {lambda_compton_reduite_e:.2e} m) : il se comporte comme un noyau ponctuel ;")
print(f"   le vide devient instable pour Z α ≳ 1, soit |Q| ≲ e/α ≈ {Zmax:.0f} e = {Zmax*e:.2e} C")
print("   (borne SUPÉRIEURE d'ordre de grandeur, pas une valeur attendue)")
Ztyp = 6.14   # valeur quadratique moyenne de la charge pour G M μ / (ħ c) -> 0 (Page 1977, résumé relu sur INSPIRE)
print(f"  Valeur TYPIQUE : la charge fluctue avec une valeur quadratique moyenne de {Ztyp} e (Page 1977), soit {Ztyp*e:.2e} C ;")
print(f"   paramètre G M m_e/(ħ c) = {G*4.4e12*m_e/(hbar*c):.4f} pour 4,4e12 kg (régime -> 0) ; estimation thermique indépendante 1/sqrt(4π α) = {1/math.sqrt(4*math.pi*alpha):.1f} e")
for M in (113.5, 1e12, 4e12):
    Qext = qm * M
    print(f"   M = {M:.4g} kg : Q_extrémale = {Qext:.3e} C ; Q/Q_extrémale : typique {Ztyp*e/Qext:.1e}, borne {Zmax*e/Qext:.1e} ;"
          f" F_e/F_g entre deux tels trous : typique {(Ztyp*e/Qext)**2:.1e}, borne {(Zmax*e/Qext)**2:.1e}")
print("  Sustentation dans la pesanteur terrestre par un champ électrique agissant sur la charge du trou :")
for M in (113.5, 1e12, 4e12):
    print(f"   M = {M:.4g} kg : E = M g / Q = {M*g0/(Ztyp*e):.2e} V/m (charge typique) ; {M*g0/(Zmax*e):.2e} V/m (borne 137 e) ;"
          f" {M*g0/(qm*M):.2e} V/m (charge extrémale, intenable) ; champ de Schwinger : {E_schwinger:.2e} V/m")
print("  Force de « strut » (Bach-Weyl) entre deux trous noirs statiques ≈ force newtonienne G M²/d² :")
for M, d in ((1e12, D_DOC), (1e12, D_HYP), (5e12, D_DOC), (5e12, D_HYP)):
    F = G * M**2 / d**2
    S = G * M**2 / c
    Fss = 6 * G * S * S / (c**2 * d**4)       # ordre de grandeur de la force spin-spin (spins alignés sur l'axe, Wald 1972)
    print(f"   M = {M:.0e} kg, d = {d} m : F = {F:.2e} N ; force spin-spin maximale ~ 6 G S²/(c² d⁴) = {Fss:.2e} N (rapport {Fss/F:.1e})")
print("  -> la répulsion spin-spin est 26 à 28 ordres de grandeur trop faible pour équilibrer deux trous de Kerr séparés")
print("     (cohérent avec le théorème de non-existence de Neugebauer & Hennig 2009).")

# ---------------------------------------------------------------- B5
print("\n[B5] Cordes de Gott : holonomie SO(2,1) de deux particules ponctuelles en gravité 2+1")
print("     Une corde de masse linéique μ = déficit angulaire δ = 8π G μ/c² (demi-angle α = 4π G μ/c²).")
print("     Critère : la holonomie totale est un boost (|trace| > 3) <=> γ sin α > 1  (Gott 1991 ; Deser-Jackiw-'t Hooft 1992)")


def rot(delta):
    cth, sth = math.cos(delta), math.sin(delta)
    return np.array([[1, 0, 0], [0, cth, -sth], [0, sth, cth]], dtype=float)   # coordonnées (t, x, y)


def boost_x(xi):
    ch, sh = math.cosh(xi), math.sinh(xi)
    return np.array([[ch, sh, 0], [sh, ch, 0], [0, 0, 1]], dtype=float)


n_ok = 0
n_tot = 0
rng = np.random.default_rng(1)
for _ in range(20000):
    alpha_demi = rng.uniform(0.01, math.pi / 2 - 0.01)       # demi-angle de déficit
    xi = rng.uniform(0.0, 4.0)                               # rapidité de chaque corde dans le référentiel du centre
    T1 = boost_x(xi) @ rot(2 * alpha_demi) @ boost_x(-xi)
    T2 = boost_x(-xi) @ rot(2 * alpha_demi) @ boost_x(xi)
    tr = np.trace(T1 @ T2)
    crit = math.cosh(xi) * math.sin(alpha_demi)
    if abs(crit - 1) < 1e-6:
        continue
    n_tot += 1
    hyperbolique = tr > 3.0 + 1e-9
    if hyperbolique == (crit > 1):
        n_ok += 1
print(f"     {n_ok}/{n_tot} tirages aléatoires : (trace de la holonomie > 3) coïncide avec (γ sin α > 1)")
# formule fermée : trace = 1 + 2 cos(δ_tot) avec cos(δ_tot/2) = 1 - 2 sin²α cosh²ξ
alpha_demi, xi = 0.3, 0.7
T = boost_x(xi) @ rot(2 * alpha_demi) @ boost_x(-xi) @ boost_x(-xi) @ rot(2 * alpha_demi) @ boost_x(xi)
c_half = 1 - 2 * math.sin(alpha_demi) ** 2 * math.cosh(xi) ** 2
print(f"     contrôle de la formule cos(δ_tot/2) = 1 - 2 sin²α cosh²ξ : trace = {np.trace(T):.10f} ; 1 + 2(2c²-1) = {1 + 2*(2*c_half**2 - 1):.10f}")
for Gmu in (1e-6, 1e-7, 1e-11):
    al = 4 * math.pi * Gmu
    gam = 1 / math.sin(al)
    mu = Gmu * c**2 / G
    print(f"     G μ/c² = {Gmu:.0e} (μ = {mu:.2e} kg/m) : il faut γ > {gam:.3e}  (1 - v/c < {1/(2*gam**2):.1e})")
print("     Borne actuelle (ordre de grandeur) sur les cordes cosmiques : G μ/c² ≲ 1e-7 (CMB) à ~1e-11 (réseaux de pulsars, selon le modèle).")

# ---------------------------------------------------------------- B6
print("\n[B6] Cohérence « 300-500 MW » / « 1,5-2 g » selon le nombre de singularités (correction n° 18)")
M500, M300 = 3.918e12, 5.058e12     # masses donnant 500 MW et 300 MW de puissance totale de Hawking (script 02)
lectures = [
    ("UNE singularité de 300-500 MW", (M500, M300)),
    ("DEUX singularités de 300-500 MW chacune", (2 * M500, 2 * M300)),
    ("DEUX singularités totalisant 300-500 MW (150-250 MW chacune)", (2 * M500 * math.sqrt(2), 2 * M300 * math.sqrt(2))),
]
for nom, (Ma, Mb) in lectures:
    gs = "  ".join(f"{r} m : {G*Ma/r**2/g0:.1f}-{G*Mb/r**2/g0:.1f} g" for r in (1.0, 2.0, 3.0, 3.7))
    r2a, r2b = math.sqrt(G * Ma / (2 * g0)), math.sqrt(G * Mb / (2 * g0))
    r15a, r15b = math.sqrt(G * Ma / (1.5 * g0)), math.sqrt(G * Mb / (1.5 * g0))
    print(f"  {nom} : masse totale {Ma:.2e}-{Mb:.2e} kg")
    print(f"     pesanteur : {gs}")
    print(f"     2 g atteints à {r2a:.2f}-{r2b:.2f} m ; 1,5 g à {r15a:.2f}-{r15b:.2f} m")
print("  Inversement, « 2 g à 1 m » = 2,9e11 kg AU TOTAL ; « 2 g à 3,7 m » = 4,0e12 kg AU TOTAL.")
print("  -> accord seulement pour UNE singularité et un occupant à >= 3,6 m ; pour deux singularités, écart d'un facteur 7 à 35")
print("     à 1-2 m : la cohérence n'est acquise qu'à un ordre de grandeur près (errata E1 du dossier de base).")
