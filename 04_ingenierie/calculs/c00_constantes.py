# -*- coding: utf-8 -*-
"""Programme C204 — Équipe C (ingénierie). Constantes et utilitaires communs.

Constantes : CODATA (via scipy.constants) ; grandeurs astronomiques : valeurs nominales UAI.
Toutes les grandeurs sont en unités SI sauf mention contraire.
"""
import json
import os
import scipy.constants as k

G = k.G                      # m^3 kg^-1 s^-2
c = k.c                      # m/s
hbar = k.hbar                # J s
kB = k.k                     # J/K
e = k.e                      # C
eps0 = k.epsilon_0           # F/m
mu0 = k.mu_0                 # H/m
me = k.m_e                   # kg
mp = k.m_p                   # kg
sigma_SB = k.sigma           # W m^-2 K^-4
alpha_fs = k.alpha           # constante de structure fine
g0 = 9.80665                 # m/s^2 (pesanteur normale)
MeV = 1e6 * k.e              # J
GeV = 1e9 * k.e              # J
an = 365.25 * 86400.0        # s (année julienne)
Msol = 1.98847e30            # kg
Lsol = 3.828e26              # W (luminosité solaire nominale UAI 2015)
Mt_TNT = 4.184e15            # J
kWh = 3.6e6                  # J
TWh = 3.6e15                 # J
EJ = 1e18                    # J
uGal = 1e-8                  # m/s^2
Eotvos = 1e-9                # s^-2

# Grandeurs dérivées utiles
K_HAWKING = hbar * c**6 / G**2          # W kg^2  : P = alpha * K_HAWKING / M^2
RS_PAR_KG = 2 * G / c**2                # m/kg    : r_s = RS_PAR_KG * M
T_HAWKING_KG = hbar * c**3 / (8 * k.pi * G * kB)   # K kg : T = T_HAWKING_KG / M
QM_MAX = (4 * k.pi * eps0 * G) ** 0.5   # C/kg    : Q_max = QM_MAX * M (Reissner-Nordström extrémal)
E_SCHWINGER = me**2 * c**3 / (e * hbar) # V/m

ICI = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------------------------------------------
# Géométrie du coffre (corrections post-validation n° 31 et 32).
# Valeurs nominales FIGÉES : Équipe A, 02_reconstruction/dimensions.json, version 1.1 du 10 novembre 2026 (23 h 40)
# ([DÉD] sur étalons [HYP], confiance faible) : L = 0,85 m ; P = 0,26 m ; H (couvercle fermé) = 0,285 m ;
# H du corps = 0,22 m ; diamètre des logements = 0,080 m ; entraxe des logements = 0,091 m.
# (La fiche de corrections de la Red Team citait la version 1.0 : 0,077 m et 0,098 m ; l'Équipe A les a re-mesurés.)
# Paramétrage : définir la variable d'environnement C204_GEOM=A pour relire le fichier de l'Équipe A (lecture seule),
# ou C204_GEOM=H1 pour rejouer l'ancienne hypothèse du dossier de base (§7). Par défaut : valeurs figées ci-dessous,
# afin que tous les scripts d'une même série utilisent exactement la même géométrie.
# ---------------------------------------------------------------------------------------------------------------
COFFRE_H1 = (1.20, 0.36, 0.30)                       # m, ancienne hypothèse H1 [HYP]
_GEOM = dict(L=0.85, P=0.26, H_ferme=0.285, H_corps=0.22, D_log=0.080, entraxe_log=0.091)
SOURCE_GEOMETRIE = "Équipe A, dimensions.json v1.1 (valeurs figées dans c00_constantes.py)"
_MODE = os.environ.get("C204_GEOM", "")
_chemin_A = os.path.join(os.path.dirname(os.path.dirname(ICI)), "02_reconstruction", "dimensions.json")
ECART_AVEC_FICHIER_A = {}
try:
    with open(_chemin_A, encoding="utf-8") as _f:
        _lu = {c["id"]: float(c["valeur"]) for c in json.load(_f)["cotes"]
               if c.get("id") in _GEOM and isinstance(c.get("valeur"), (int, float))}
    ECART_AVEC_FICHIER_A = {k_: (_GEOM[k_], v) for k_, v in _lu.items() if abs(_GEOM[k_] - v) > 1e-9}
    if _MODE == "A":
        _GEOM.update(_lu)
        SOURCE_GEOMETRIE = "02_reconstruction/dimensions.json relu à l'exécution (C204_GEOM=A)"
except Exception:                                   # fichier absent ou illisible : valeurs figées
    pass
if _MODE == "H1":
    _GEOM.update(L=COFFRE_H1[0], P=COFFRE_H1[1], H_ferme=COFFRE_H1[2], H_corps=COFFRE_H1[2], D_log=0.10, entraxe_log=0.15)
    SOURCE_GEOMETRIE = "ancienne hypothèse H1 du dossier de base (C204_GEOM=H1)"
COFFRE_L, COFFRE_P, COFFRE_H = _GEOM["L"], _GEOM["P"], _GEOM["H_ferme"]     # m
COFFRE_H_CORPS = _GEOM["H_corps"]                    # m, hauteur du corps sans couvercle
COFFRE_V = COFFRE_L * COFFRE_P * COFFRE_H           # m^3 (enveloppe extérieure, couvercle fermé)
COFFRE_S = 2 * (COFFRE_L * COFFRE_P + COFFRE_L * COFFRE_H + COFFRE_P * COFFRE_H)  # m^2
VOLUME_UTILE = 0.035 if _MODE != "H1" else 0.102     # m^3 : volume intérieur utile (Équipes E et I : 35–36 L ; 102 L à H1)
R_CARTER = _GEOM["D_log"] / 2                        # m : rayon du logement circulaire de DOC-007 (Équipe A)
D_PAIRE = _GEOM["entraxe_log"]                       # m : entraxe des deux logements (Équipe A, DOC-007)
V_RESERVOIR_SCHEMA = 0.25e-3                         # m^3 : un réservoir à l'échelle du schéma (Équipe E : Ø 53 x 107 mm)
V_RESERVOIR_BORNE_HAUTE = 15e-3                      # m^3 : ancienne hypothèse généreuse [HYP]
MASSE_UNITE = 500 * 0.45359237                       # kg (« environ 500 livres »)
DUREE_TRAJET = 6 * 3600.0                            # s (≈ 60 ans à 10 ans/h)

RES = os.path.join(ICI, "resultats")
os.makedirs(RES, exist_ok=True)


def sauver_json(nom, donnees):
    chemin = os.path.join(RES, nom)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2, default=float)
    return chemin


def charger_json(nom):
    with open(os.path.join(RES, nom), encoding="utf-8") as f:
        return json.load(f)


def sci(x, n=3):
    """Notation scientifique compacte."""
    return f"{x:.{n}e}"


if __name__ == "__main__":
    d = dict(G=G, c=c, hbar=hbar, kB=kB, e=e, eps0=eps0, mu0=mu0, me=me, g0=g0,
             K_HAWKING_W_kg2=K_HAWKING, RS_PAR_KG=RS_PAR_KG, T_HAWKING_K_kg=T_HAWKING_KG,
             QM_MAX_C_par_kg=QM_MAX, E_SCHWINGER_V_par_m=E_SCHWINGER,
             COFFRE_L_m=COFFRE_L, COFFRE_P_m=COFFRE_P, COFFRE_H_m=COFFRE_H, COFFRE_H_CORPS_m=COFFRE_H_CORPS,
             COFFRE_V_m3=COFFRE_V, COFFRE_S_m2=COFFRE_S, VOLUME_UTILE_m3=VOLUME_UTILE,
             R_CARTER_m=R_CARTER, D_PAIRE_m=D_PAIRE, source_geometrie=SOURCE_GEOMETRIE,
             ecart_avec_le_fichier_de_l_equipe_A={k_: list(v) for k_, v in ECART_AVEC_FICHIER_A.items()},
             COFFRE_H1_m=list(COFFRE_H1), COFFRE_H1_V_m3=COFFRE_H1[0] * COFFRE_H1[1] * COFFRE_H1[2],
             COFFRE_H1_S_m2=2 * (COFFRE_H1[0] * COFFRE_H1[1] + COFFRE_H1[0] * COFFRE_H1[2] + COFFRE_H1[1] * COFFRE_H1[2]),
             MASSE_UNITE_kg=MASSE_UNITE, masse_volumique_moyenne_kg_m3=MASSE_UNITE / COFFRE_V)
    print(json.dumps(d, indent=2))
    sauver_json("c00_constantes.json", d)
