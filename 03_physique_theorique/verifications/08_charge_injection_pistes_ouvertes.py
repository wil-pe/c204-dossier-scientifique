#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 08 : compléments chiffrés.

  C1. « injecter des électrons » : débit d'émission e± du trou noir, section efficace d'absorption,
      variation de masse réellement obtenue
  C2. capacité calorifique négative ; superradiance (énergies caractéristiques)
  C3. création : énergie de masse, conjecture du cerceau, collisionneur nécessaire
  C4. piste ouverte : trou noir extrémal à charge MAGNÉTIQUE (froid, piégeable magnétiquement)
  C5. restes (« remnants ») à la masse de Planck
  C6. « divergence mesurée par gravimétrie » : ordres de grandeur gravimétriques réels
  C7. modèles de causalité : point fixe de Deutsch (D-CTC) et post-sélection (P-CTC) sur le
      circuit du « paradoxe du grand-père » — illustration numérique
"""
import math

import numpy as np

from constantes import *

print("=" * 78)
print("SCRIPT 08 — Injection d'électrons, création, pistes ouvertes, modèles de causalité")
print("=" * 78)

# coefficients calculés par le script 02 (par degré de liberté, spin 1/2, unités hbar c^6/G²M² et c³/GM)
C12_P = 4.0916e-05
C12_N = 2.4284e-04
coefP = hbar * c**6 / G**2
coefN = c**3 / G

# ---------------------------------------------------------------- C1
print("\n[C1] « Injecter des électrons sur la surface » d'un micro-trou noir")
for M in (1e12, 5e12):
    rs = 2 * G * M / c**2
    rg = rs / 2
    kT = hbar * c**3 / (8 * math.pi * G * M)
    Ndot = 4 * C12_N * coefN / M            # e- et e+ (4 ddl), régime relativiste
    Pe = 4 * C12_P * coefP / M**2
    U1 = alpha * hbar * c / rs              # énergie électrostatique d'une charge e à r_s auprès d'une charge e
    sig_go = 27 * math.pi * rg**2
    sig_bas = 2 * math.pi * rg**2           # fermions de basse énergie (ordre de grandeur, Unruh 1976)
    j = 1.0 / 1e-12                         # 1 A focalisé sur 1 µm²
    taux_abs = j * sig_go / e
    print(f"  M = {M:.0e} kg : r_s = {rs:.2e} m ; kT = {kT/MeV:.2f} MeV ; émission propre d'e± : {Ndot:.2e} par seconde ({Pe:.2e} W)")
    print(f"     énergie coulombienne par unité de charge du trou : α ħc / r_s = {U1/MeV:.3f} MeV  (à comparer à kT)")
    print(f"     section efficace de capture : 27π r_g² = {sig_go:.2e} m² = {sig_go/1e-28:.1f} barn (haute énergie) ; 2π r_g² = {sig_bas/1e-28:.2f} barn (basse énergie)")
    print(f"     faisceau de 1 A focalisé sur 1 µm² : {taux_abs:.1e} électrons absorbés par seconde, soit {taux_abs/Ndot:.1e} × l'émission propre")
    Z_eq = (1.0 / e) / (Ndot / 2 * U1 / kT)
    print(f"     même si 1 A entier (6,2e18 e/s) était absorbé : charge d'équilibre Z ~ I/(e N_e U1/kT) ≈ {Z_eq:.1f} e (le trou se neutralise par émission préférentielle)")
print("  Variation de masse par injection : dM/dt = I m_e / e + P_faisceau / c²")
I = 1.0
print(f"     I = 1 A : {I*m_e/e:.2e} kg/s (masse au repos) ; faisceau de 1 MW : {1e6/c**2:.2e} kg/s ; perte par rayonnement de Hawking à 400 MW : {4e8/c**2:.2e} kg/s")
print(f"     en 1 heure, 1 MW : ΔM/M = {1e6/c**2*3600/4e12:.1e} pour M = 4e12 kg -> aucun effet sur « la masse et la gravité »")
print(f"  longueur de Compton réduite de l'électron / r_s(4e12 kg) = {lambda_compton_reduite_e/(2*G*4e12/c**2):.0f} : un électron lent ne « voit » pas le trou noir")

# ---------------------------------------------------------------- C2
print("\n[C2] Thermodynamique : capacité calorifique C = dE/dT = -8π G k_B M² / (ħ c) < 0")
for M in (4e12,):
    C = -8 * math.pi * G * kB * M**2 / (hbar * c)
    print(f"  M = {M:.0e} kg : C = {C:.2e} J/K  -> retirer de l'énergie (« refroidir ») ÉLÈVE la température ; il n'y a rien à refroidir dans le trou noir lui-même")
print("  Superradiance (trou de Kerr) : amplification des ondes de pulsation ω < m Ω_H ; pour un trou extrémal ħΩ_H = ħc³/(2GM)")
for M in (1e12, 4e12):
    print(f"   M = {M:.0e} kg : ħΩ_H = {hbar*c**3/(2*G*M)/MeV:.1f} MeV ; longueur d'onde utile ~ r_g = {G*M/c**2:.1e} m ;"
          f" pour un photon X de 10 keV : ω r_g/c = {1e4*eV*G*M/(hbar*c**3)/c**0:.1e}")
print("   gains maximaux par passage (littérature : Press & Teukolsky 1972 ; Teukolsky & Press 1974) : ~0,3 % (scalaire), 4,4 % (électromagnétique), 138 % (gravitationnel)")
print("   énergie de rotation extractible ≤ 29,3 % de M c² (script 03)")

# ---------------------------------------------------------------- C3
print("\n[C3] Création d'un micro-trou noir")
E_monde = 6.0e20
for M in (m_planck, 227.0, 1e9, 4e12):
    print(f"  M = {M:.3e} kg : M c² = {M*c**2:.2e} J = {M*c**2/E_monde:.2e} années de consommation mondiale d'énergie primaire (~6e20 J/an)")
E_LHC = 13.6e12 * eV
print(f"  Conjecture du cerceau : il faut concentrer E = M c² dans r_s. Masse minimale (4D) ~ masse de Planck : E = {m_planck*c**2/GeV:.2e} GeV = {m_planck*c**2:.2e} J par collision")
print(f"   LHC : {E_LHC/GeV:.2e} GeV par collision -> il manque un facteur {m_planck*c**2/E_LHC:.1e}")
R_coll = (m_planck * c**2 / GeV) / (0.2998 * 8.33)
print(f"   anneau à dipôles de 8,33 T atteignant l'énergie de Planck : rayon p/(0,3 B) = {R_coll:.1e} m = {R_coll/(c*an):.0f} années-lumière")
M_tev = 5e12 * eV / c**2
print(f"   scénarios à dimensions supplémentaires (gravité au TeV, non confirmés) : trous noirs de ~5 TeV = {M_tev:.1e} kg, durée de vie ~1e-26 s, jamais observés")
print(f"   « machine Z » (Sandia) : ~2 MJ de rayons X par tir (ordre de grandeur) = {2e6/c**2:.1e} kg d'équivalent masse")

# ---------------------------------------------------------------- C4
print("\n[C4] Piste ouverte : trou noir extrémal à charge magnétique (T = 0, pas d'évaporation, piégeable par un champ magnétique)")
gD = h / (mu0 * e)                       # charge de Dirac en A·m (convention F = g B)
coefM = math.sqrt(mu0 / (4 * math.pi * G))   # M_extrémal = coefM * g   [kg par A·m]
print(f"  charge de Dirac g_D = h/(μ0 e) = {gD:.3e} A·m ; extrémalité : G M² = μ0 g²/4π  =>  M = g sqrt(μ0/4πG) = {coefM:.2f} kg par A·m")
print(f"  masse par unité de Dirac : {coefM*gD:.3e} kg = {coefM*gD/m_planck:.2f} masses de Planck (= 1/(2 sqrt(α)) = {1/(2*math.sqrt(alpha)):.2f})")
B_lev = g0 * coefM
print(f"  champ de sustentation dans la pesanteur terrestre : B = M g0 / g = g0 sqrt(μ0/4πG) = {B_lev:.0f} T, indépendant de la masse")
for M in (113.5, 2.9e11, 4e12):
    gm = M / coefM
    rg = G * M / c**2
    print(f"   M = {M:.3g} kg : g = {gm:.2e} A·m ({gm/gD:.1e} unités de Dirac) ; r+ = GM/c² = {rg:.1e} m ; champ magnétique à 1 m : {mu0*gm/(4*math.pi):.2e} T ;"
          f" pesanteur à 1 m : {G*M/g0:.2e} g")
print(f"  relation universelle pour un tel objet : B(r) / g_grav(r) = sqrt(μ0/4πG) = {coefM:.1f} T par m/s²  -> « 2 g » implique B ≈ {2*g0*coefM:.0f} T au même endroit")
print("  Conditions : existence de monopôles magnétiques (jamais observés) ; stabilité seulement si aucun monopôle léger ne permet la décharge (Maldacena 2021).")

# ---------------------------------------------------------------- C5
print("\n[C5] Restes à la masse de Planck (hypothétiques)")
print(f"  m_P = {m_planck*1e9:.1f} µg ; r_s ~ {2*G*m_planck/c**2:.1e} m ; pesanteur à 1 m : {G*m_planck:.1e} m/s² ; énergie de masse {m_planck*c**2:.2e} J")
print(f"  nombre de restes pour 227 kg : {227/m_planck:.1e} ; pour « 2 g à 1 m » : {2.9e11/m_planck:.1e}")

# ---------------------------------------------------------------- C6
print("\n[C6] « Divergence en % mesurée par gravimétrie » : ce que mesure réellement un gravimètre")
print(f"  marées terrestres : ~3e-7 g crête à crête ; gradient vertical à l'air libre : 3,086e-6 s⁻² = {3.086e-6/g0*100:.1e} % de g par mètre")
print(f"  écart équateur-pôle : (9,832 - 9,780)/9,81 = {(9.832-9.780)/9.81*100:.2f} %")
print(f"  un véhicule de 2500 kg à 3 m : {G*2500/9/g0:.1e} g ; résolution d'un gravimètre absolu moderne : ~1e-9 g")
dh = 0.01 * g0 / 3.086e-6
print(f"  une variation de 1 % de g correspond à un changement d'altitude de {dh/1e3:.0f} km, ou à ΔM_Terre/M_Terre = 1 %")
for M in (1e12, 4e12):
    print(f"  et le champ propre de l'unité à 0,5 m de ses singularités (M = {M:.0e} kg) : {G*M/0.25/g0:.0f} g -> un « capteur de gravité » embarqué serait saturé par l'unité elle-même")

# ---------------------------------------------------------------- C7
print("\n[C7] Modèles quantiques de CTC sur le circuit du « paradoxe du grand-père »")
X = np.array([[0, 1], [1, 0]], dtype=complex)
I2 = np.eye(2, dtype=complex)


def deutsch_point_fixe(U, rho_in, n_iter=2000):
    """Itère ρ -> Tr_CR[U (ρ_in ⊗ ρ) U†] en moyennant (convergence vers un point fixe de Deutsch)."""
    rho = np.array([[1, 0], [0, 0]], dtype=complex)
    moy = np.zeros((2, 2), dtype=complex)
    for _ in range(n_iter):
        tot = U @ np.kron(rho_in, rho) @ U.conj().T
        tot = tot.reshape(2, 2, 2, 2)
        rho = np.einsum("iaib->ab", tot)       # trace partielle sur le système chronologique (CR)
        moy += rho
    return moy / n_iter


# (a) paradoxe pur : le qubit qui remonte le temps subit NON (il « s'empêche d'exister »)
U_par = np.kron(I2, X)
rho_cr = np.array([[1, 0], [0, 0]], dtype=complex)
rho_fix = deutsch_point_fixe(U_par, rho_cr)
print("  (a) évolution NON sur la boucle : condition classique x = NON(x) sans solution (paradoxe).")
print("      Deutsch : point fixe ρ = Tr[U(ρ_in⊗ρ)U†] ->", np.round(rho_fix.real, 3).tolist(), " (état maximalement mélangé : cohérent, mais non unitaire)")
print(f"      P-CTC (Lloyd et al.) : amplitude ∝ Tr_CTC(U) = {np.trace(X).real:.0f} -> probabilité nulle : l'histoire paradoxale est post-sélectionnée hors du réel")
# (b) non-linéarité : CNOT (contrôle CR, cible CTC) puis SWAP
CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
U = SWAP @ CNOT


def sortie_cr(U, rho_in):
    rho = deutsch_point_fixe(U, rho_in, 400)
    tot = (U @ np.kron(rho_in, rho) @ U.conj().T).reshape(2, 2, 2, 2)
    return np.einsum("aibi->ab", tot)          # trace partielle sur la boucle


zero = np.array([[1, 0], [0, 0]], dtype=complex)
un = np.array([[0, 0], [0, 1]], dtype=complex)
melange = 0.5 * zero + 0.5 * un
out_melange = sortie_cr(U, melange)
out_moy = 0.5 * sortie_cr(U, zero) + 0.5 * sortie_cr(U, un)
print("  (b) non-linéarité du modèle de Deutsch (U = SWAP·CNOT) : une application linéaire vérifierait S(½ρ0 + ½ρ1) = ½S(ρ0) + ½S(ρ1).")
print("      S(½|0><0| + ½|1><1|) =", np.round(out_melange.real, 3).tolist(), " ; ½[S(|0><0|) + S(|1><1|)] =", np.round(out_moy.real, 3).tolist())
print("      -> inégalité : l'évolution effective du monde « chronologique » n'est ni linéaire ni unitaire (d'où les critiques de Bennett et al. 2009)")
print("  Lecture everettienne (Deutsch 1991) : le voyageur quitte une branche et émerge dans une autre ; c'est le seul modèle publié")
print("  qui ressemble à la « divergence de ligne d'univers » — mais il présuppose l'existence d'une CTC, qu'il ne fournit pas.")
