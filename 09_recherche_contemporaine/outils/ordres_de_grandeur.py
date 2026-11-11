#!/usr/bin/env python3
"""Ordres de grandeur du RAPPORT_H.md (§0 bis et valeurs chiffrées des §1 à §12) — Équipe H, programme C204.

Usage : python -I ordres_de_grandeur.py > ../donnees_brutes/ordres_de_grandeur.txt

Ajouté en phase 7 (correction demandée par la Red Team : le tableau du §0 bis n'était adossé à aucun script).
Calculs ILLUSTRATIFS : ils ne valident aucune affirmation du récit, ils chiffrent ce qu'elle impliquerait.
Les coefficients d'émission (Page 1976-1977, MacGibbon 1991) sont cités de mémoire ; le résumé de Page (1976)
relu par la Red Team confirme 2×10⁻⁴ et la répartition 81 / 17 / 2 %.
"""
import datetime
import math

# --- constantes (CODATA 2018, SI) ---
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB = 1.380649e-23
e = 1.602176634e-19
eps0 = 8.8541878128e-12
me = 9.1093837015e-31
alpha = e**2 / (4 * math.pi * eps0 * hbar * c)
g0 = 9.80665
MeV = 1e6 * e
AN = 365.25 * 86400.0
UA = 1.495978707e11


def titre(t):
    print("\n== " + t + " ==")


def rs(M):
    return 2 * G * M / c**2


def kT_MeV(M):
    return hbar * c**3 / (8 * math.pi * G * M) / MeV


# coefficient de perte de masse (MacGibbon 1991, de mémoire) : dM/dt = -5,34e25 f(M) / M² g/s, M en g
K_MASSLESS = 5.34e25 * 1e-9          # kg³/s pour f = 1 (photons, gravitons négligés, 3 familles de neutrinos)
F_E = 1.569                          # f pour γ + 3 ν + e± (10¹⁵ g < M < 10¹⁷ g)
F_SM = 15.35                         # f pour tout le Modèle standard (très petites masses), de mémoire


def P_tot(M, f=F_E):
    return K_MASSLESS * f * c**2 / M**2


def duree_vie(M, f=F_E):
    return M**3 / (3 * K_MASSLESS * f)


titre("1. Échelle de Planck et LHC")
MP = math.sqrt(hbar * c / G)
EP = MP * c**2
ELHC = 13.6e12 * e
print(f"masse de Planck            : {MP:.3e} kg = {EP / (1e9 * e):.3e} GeV")
print(f"énergie LHC Run 3 (13,6 TeV): {ELHC:.2e} J  <=> {ELHC / c**2:.2e} kg ; E_P/E_LHC = {EP / ELHC:.1e}")

titre("2. Puissance de Hawking")
K_hbar = hbar * c**6 / G**2
naif = K_hbar / (15360 * math.pi)
print(f"hbar c^6/G^2                         : {K_hbar:.4e} W kg²")
print(f"formule naïve (photons, corps noir)  : P M² = {naif:.3e} W kg²")
print(f"toutes espèces légères (f = {F_E})  : P M² = {K_MASSLESS * F_E * c**2:.3e} W kg²  (rapport {K_MASSLESS * F_E * c**2 / naif:.1f})")
page4 = 2.011e-4 * K_hbar                    # Page 1976 : γ + gravitons + 4 espèces de neutrinos
page6 = page4 * (0.167 + 0.019 + 0.814 * 1.5)  # passage à 6 espèces de neutrinos
print(f"recoupement Page 1976 (6 esp. de ν)  : P M² = {page6:.3e} W kg² contre {K_MASSLESS * c**2:.3e} (écart {abs(page6 / (K_MASSLESS * c**2) - 1) * 100:.1f} %)")
nu, gam, grav, el = 0.814 * 1.5, 0.167, 0.019, 0.569 * (0.167 + 0.019 + 0.814 * 1.5)
tot = nu + gam + grav + el
print(f"répartition (f = 1,569)              : ν {nu / tot * 100:.0f} % ; e± {el / tot * 100:.0f} % ; γ {gam / tot * 100:.0f} % ; gravitons {grav / tot * 100:.0f} %")
for P in (3e8, 5e8):
    M = math.sqrt(K_MASSLESS * F_E * c**2 / P)
    print(f"P = {P / 1e6:.0f} MW -> M = {M:.2e} kg ; kT = {kT_MeV(M):.2f} MeV ; pic photons ≈ 5,77 kT = {5.77 * kT_MeV(M):.0f} MeV ; "
          f"r_s = {rs(M) * 1e15:.1f} fm ; durée de vie = {duree_vie(M) / AN:.1e} ans ; g(1 m) = {G * M / g0:.0f} g0 ; "
          f"dM/dt = {P / c**2:.1e} kg/s")
M10 = hbar * c**3 / (8 * math.pi * G * (1e4 * e))
print(f"trou « à rayons X » (kT = 10 keV)    : M = {M10:.1e} kg ; P (f = 1) = {P_tot(M10, 1.0):.1e} W")
print(f"trou de 227 kg (f = {F_SM}, de mémoire) : durée de vie = {duree_vie(227.0, F_SM):.1e} s ; énergie = {227 * c**2:.1e} J")
Mref = 4.5e12
print(f"énergie de masse de {Mref:.1e} kg    : {Mref * c**2:.1e} J = {Mref * c**2 / 6e20:.0e} années de consommation mondiale (6e20 J/an)")

titre("3. Charge (corrigé en phase 7 : errata E14 du dossier)")
Qmax = Mref * math.sqrt(4 * math.pi * eps0 * G)
Ec = me**2 * c**3 / (e * hbar)
rg = G * Mref / c**2
print(f"charge extrémale ({Mref:.1e} kg)       : {Qmax:.0f} C = {Qmax / e:.1e} e ; champ à l'horizon extrémal = {Qmax / (4 * math.pi * eps0 * rg**2) / Ec:.0e} E_Schwinger")
print(f"paramètre de Page GMμ/ħc (électron)  : {G * Mref * me / (hbar * c):.4f}  (<< 0,16 : régime « sans masse », rms 6,14 e selon le résumé de Page 1977)")
for n, lab in ((6.14, "valeur quadratique moyenne (Page 1977)"), (1 / alpha, "borne d'ordre de grandeur Zα ≈ 1")):
    q = n * e / Qmax
    print(f"Q = {n:6.1f} e  [{lab}] : Q/Q_max = {q:.1e} ; r_- ≈ (GM/c²) q²/2 = {rg * q**2 / 2:.0e} m")
print(f"longueur de Planck                   : {math.sqrt(hbar * G / c**3):.1e} m ; longueur de Compton réduite de l'électron : {hbar / (me * c):.2e} m ; r_s = {rs(Mref):.2e} m")
print(f"[estimation propre à l'Équipe H, non issue de Gibbons 1975, peu adaptée car r_s << ħ/m_e c] "
      f"e²/(4πε0 r_s) = {e * e / (4 * math.pi * eps0 * rs(Mref)) / MeV:.2f} MeV par charge ; m_e c² = 0,511 MeV")

titre("4. Dilatation du temps et horloges")
print(f"décalage gravitationnel terrestre g/c² : {g0 / c**2:.3e} par m = {g0 / c**2 / 1e3:.2e} par mm")
M2g = 2 * g0 / G
print(f"masse donnant 2 g à 1 m                : {M2g:.1e} kg ; potentiel GM/(r c²) = {G * M2g / c**2:.1e}")
ratio = 10 * AN / 3600.0
print(f"« 10 ans par heure »                   : rapport = {ratio:.0f} ; exige 1 − r_s/r = {1 / ratio**2:.1e}")
tau = 6 * 3600.0
print(f"horloge à 5e-13 (ordre de grandeur)    : {5e-13 * tau:.1e} s en 6 h de temps propre ; x {ratio:.0f} = {5e-13 * tau * ratio:.1e} s ; "
      f"1 % de 60 ans = {0.01 * 60 * AN:.1e} s = {0.01 * 60 * 365.25:.0f} jours ; rapport = {0.01 * 60 * AN / (5e-13 * tau * ratio):.0e}")

titre("5. Gravimétrie")
for r in (1e3, 1e4, 1e5):
    a = G * 2 * Mref / r**2
    print(f"2 x {Mref:.1e} kg à {r / 1e3:5.0f} km : a = {a:.1e} m/s² = {a / 1e-8:.0f} µGal")
print(f"champ propre de {Mref:.1e} kg : {G * Mref / g0:.0f} g0 à 1 m ; {G * Mref / 0.09 / g0:.0f} g0 à 0,3 m ; gradient 2GM/r³ à 1 m = {2 * G * Mref:.0f} s⁻² (Terre : 3,1e-6 s⁻²)")
print(f"potentiel de 227 kg à 1 m : GM/(r c²) = {G * 227 / c**2:.1e}")

titre("6. Divers")
J = 0.5 * 100 * 0.1**2 * 1e4
print(f"entraînement des référentiels, rotor J = {J:.0e} kg m²/s à 1 m : Ω = 2GJ/(c² r³) = {2 * G * J / c**2:.1e} rad/s ; Terre (39 mas/an) = {39e-3 / 3600 * math.pi / 180 / AN:.1e} rad/s")
d = 1e-7
rho = math.pi**2 * hbar * c / (720 * d**4)
print(f"Casimir, plaques à 100 nm : ρ = −{rho:.1f} J/m³ = −{rho / c**2:.0e} kg/m³")
print(f"écart de masse : log10(1e12 kg / 0,4 mg) = {math.log10(1e12 / 4e-7):.1f} ; log10(1e12 kg / 90 mg) = {math.log10(1e12 / 9e-5):.1f}")
rho_dm = 0.4e9 * e / c**2 * 1e6
n = rho_dm / Mref
print(f"matière noire locale 0,4 GeV/cm³ = {rho_dm:.1e} kg/m³ ; si faite de trous de {Mref:.1e} kg : un par cube de {(1 / n) ** (1 / 3) / UA:.1f} UA de côté")
print(f"dernier instant d'un time_t signé de 32 bits : {datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=2**31 - 1)} UTC")
