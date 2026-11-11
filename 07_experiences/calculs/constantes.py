# -*- coding: utf-8 -*-
"""Constantes physiques (SI, CODATA 2018) et utilitaires communs — Équipe F.

Tous les scripts calcNN_*.py importent ce module. Les résultats numériques sont
écrits dans calculs/resultats/ (JSON + texte) et les figures dans calculs/figures/.
Les figures sont des CALCULS ILLUSTRATIFS, pas des mesures.
"""
import json
import math
import os

# --- constantes fondamentales
G = 6.67430e-11            # m^3 kg^-1 s^-2
c = 2.99792458e8           # m/s
hbar = 1.054571817e-34     # J s
h_planck = 2 * math.pi * hbar
kB = 1.380649e-23          # J/K
eps0 = 8.8541878128e-12    # F/m
mu0 = 1.25663706212e-6     # N/A^2
e_ch = 1.602176634e-19     # C
m_e = 9.1093837015e-31     # kg
sigma_SB = 5.670374419e-8  # W m^-2 K^-4
g0 = 9.80665               # m/s^2 (pesanteur normale conventionnelle)

# --- Terre, Soleil
GM_terre = 3.986004418e14  # m^3/s^2
M_terre = GM_terre / G
R_terre = 6.371e6          # m (rayon moyen)
R_equateur = 6.378137e6    # m
Omega_terre = 7.2921150e-5 # rad/s
J_terre = 5.86e33          # kg m^2/s (moment cinétique)
W0_geoide = 62636856.0     # m^2/s^2 (potentiel du géoïde, UAI 2000)
M_soleil = 1.98847e30
R_soleil = 6.957e8

# --- valeurs revendiquées (dossier de base §4) — ce sont des AFFIRMATIONS, pas des faits
C204 = {
    "masse_unite_kg": 227.0,
    "puissance_W": (300e6, 500e6),
    "g_ressenti": (1.5, 2.0),
    "temperature_C": (38.0, 49.0),
    "taux_temps": 87660.0,      # dt_ext/dtau pour « 10 ans par heure »
    "champ_m": (3.0, 3.7),
    # Masse DÉDUITE (jamais revendiquée telle quelle) pour une puissance de Hawking de 300–500 MW :
    #   valeur retenue par le programme (dossier v1.2, erratum E2 ; Équipe B ; Red Team n° 2) : 3,9–5,1e12 kg PAR singularité
    "masse_TN_kg": (3.9e12, 5.1e12),
    "masse_TN_centrale_kg": 4.4e12,
    #   ancienne fourchette (dossier v1 §6, formule « photons seuls », sous-estimée d'un facteur ≈ 21 en puissance)
    "masse_TN_ancienne_kg": (1e11, 1e12),
}
N_SINGULARITES = 2                       # « deux micro-singularités » [DOC texte]
M_PAIRE = tuple(N_SINGULARITES * m for m in C204["masse_TN_kg"])     # 7,8e12 à 1,02e13 kg
ENTRAXE_M = (0.098, 0.30)                # 0,098 m : valeur documentaire (Équipe A) ; 0,30 m : hypothèse de B, D, G
FRACTION_PHOTONS_HAWKING = 0.075         # part de la puissance de Hawking émise en photons à ces masses (valeur retenue)
E_PHOTON_HAWKING = "15 MeV"              # photons de 12–16 MeV (valeur retenue)
# Coffre à l'échelle révisée (dossier v1.2, erratum E12 ; Équipe A) : L = 0,85 m ; P = 0,26 m ; H fermée = 0,285 m
COFFRE = {"L": 0.85, "P": 0.26, "H": 0.285}
COFFRE["S"] = 2 * (COFFRE["L"] * COFFRE["P"] + COFFRE["L"] * COFFRE["H"] + COFFRE["P"] * COFFRE["H"])   # ≈ 1,07 m²
# Charge qu'un micro-trou noir peut retenir (erratum E14) : ≈ 6 e (valeur quadratique moyenne), borne ≈ 137 e
CHARGE_TENABLE_E = (6.0, 137.0)

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_RES = os.path.join(ICI, "resultats")
DOSSIER_FIG = os.path.join(ICI, "figures")
os.makedirs(DOSSIER_RES, exist_ok=True)
os.makedirs(DOSSIER_FIG, exist_ok=True)


def sauver(nom, donnees, lignes):
    """Écrit resultats/<nom>.json et resultats/<nom>.txt, et affiche le texte."""
    with open(os.path.join(DOSSIER_RES, nom + ".json"), "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2, default=float)
    texte = "\n".join(lignes)
    with open(os.path.join(DOSSIER_RES, nom + ".txt"), "w", encoding="utf-8") as f:
        f.write(texte + "\n")
    print(texte)


def fig_chemin(nom):
    return os.path.join(DOSSIER_FIG, nom)


def sci(x, n=3):
    """Notation scientifique compacte à la française (virgule décimale)."""
    if x == 0:
        return "0"
    s = f"{x:.{n-1}e}"
    mant, expo = s.split("e")
    return f"{mant.replace('.', ',')}e{int(expo)}"
