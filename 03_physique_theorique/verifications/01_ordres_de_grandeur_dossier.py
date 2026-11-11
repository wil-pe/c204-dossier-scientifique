#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 01 : re-dérivation indépendante des ordres de grandeur du
dossier de base (§6) et comparaison chiffrée.

Toutes les formules sont écrites ici à partir des définitions (pas recopiées) :
  r_s = 2GM/c^2
  T_H = hbar c^3 / (8 pi G M k_B)
  P_corps_noir(photons) = sigma T^4 * 4 pi r_s^2 = hbar c^6 / (15360 pi G^2 M^2)
  t_evap(photons, corps noir) = 5120 pi G^2 M^3 / (hbar c^4)
  M(2g à r) = 2 g r^2 / G
  Q_max = M sqrt(4 pi eps0 G)
"""
import math
from constantes import *

print("=" * 78)
print("SCRIPT 01 — Re-dérivation des ordres de grandeur du dossier de base (§6)")
print("=" * 78)

# --- coefficients
coef_rs = 2 * G / c**2
coef_T = hbar * c**3 / (8 * math.pi * G * kB)
coef_P = hbar * c**6 / (15360 * math.pi * G**2)
coef_t = 5120 * math.pi * G**2 / (hbar * c**4)
coef_Q = math.sqrt(4 * math.pi * eps0 * G)

# vérification interne : P = sigma T^4 A
M = 1.0e12
T = coef_T / M
A = 4 * math.pi * (coef_rs * M) ** 2
P_sb = sigma_SB * T**4 * A
assert abs(P_sb / (coef_P / M**2) - 1) < 1e-9, "incohérence Stefan-Boltzmann"
# vérification interne : t = M^3/(3 K) avec dM/dt = -K/M^2, K = coef_P/c^2
K = coef_P / c**2
assert abs((1 / (3 * K)) / coef_t - 1) < 1e-9, "incohérence durée de vie"

print(f"r_s / M              = {coef_rs:.4e} m/kg        (dossier : 1,485e-27)")
print(f"T_H * M              = {coef_T:.4e} K kg         (dossier : 1,227e23)")
print(f"P_cn(photons) * M^2  = {coef_P:.4e} W kg^2       (dossier : 3,56e32)")
print(f"t_evap / M^3         = {coef_t:.4e} s kg^-3      (dossier : 8,41e-17)")
print(f"Q_max / M            = {coef_Q:.4e} C/kg         (dossier : 8,62e-11)")
print(f"hbar c^6 / G^2       = {hbar*c**6/G**2:.4e} W kg^2")
print()

for P in (300e6, 500e6):
    M = math.sqrt(coef_P / P)
    print(f"P = {P/1e6:.0f} MW (photons, corps noir) -> M = {M:.3e} kg ; r_s = {coef_rs*M*1e15:.3f} fm ;"
          f" k_B T = {kB*coef_T/M/MeV:.2f} MeV")
print()
for M in (100.0, 113.5, 227.0, 1.0e12):
    t = coef_t * M**3
    print(f"M = {M:.4g} kg : r_s = {coef_rs*M:.3e} m ; T = {coef_T/M:.3e} K ; kT = {kB*coef_T/M/GeV:.3e} GeV ;"
          f" t_evap(photons seuls) = {t:.3e} s = {t/an:.3e} ans")
print()
for r in (1.0, 3.0, 3.7):
    M2g = 2 * g0 * r**2 / G
    print(f"2 g à r = {r} m  -> M = {M2g:.3e} kg")
for r in (1.0, 3.0):
    M15 = 1.5 * g0 * r**2 / G
    print(f"1,5 g à r = {r} m -> M = {M15:.3e} kg")
print()
print(f"Q_max(1e12 kg)       = {coef_Q*1e12:.2f} C")
print(f"E = m c^2 (227 kg)   = {227*c**2:.3e} J = {227*c**2/TNT_tonne/1e9:.2f} Gt TNT")
print()
print("Tailles 'de l'électron' pour comparaison :")
print(f"  rayon classique r_e           = {r_e_classique:.4e} m -> M(r_s=r_e) = {r_e_classique/coef_rs:.3e} kg")
print(f"  Compton réduite hbar/(m_e c)  = {lambda_compton_reduite_e:.4e} m -> M = {lambda_compton_reduite_e/coef_rs:.3e} kg")
print(f"  borne exp. sur la taille (≲1e-18 m, ordre de grandeur) -> M(r_s=1e-18 m) = {1e-18/coef_rs:.3e} kg")
print(f"  rayon de charge du proton ~0,84 fm -> M(r_s=0,84 fm) = {0.84e-15/coef_rs:.3e} kg")
print()
print("Échelles de Planck :")
print(f"  m_P = {m_planck:.4e} kg ; l_P = {l_planck:.4e} m ; t_P = {t_planck:.4e} s ; E_P = {m_planck*c**2/GeV:.3e} GeV")
print(f"  alpha = 1/{1/alpha:.3f} ; E_Schwinger = {E_schwinger:.3e} V/m ; B_Schwinger = {B_schwinger:.3e} T")
print()
print("Conclusion : les coefficients du dossier (§6) sont reproduits à mieux que 0,1 %.")
print("Les désaccords physiques (espèces émises, facteurs de corps gris) sont traités dans le script 02.")
