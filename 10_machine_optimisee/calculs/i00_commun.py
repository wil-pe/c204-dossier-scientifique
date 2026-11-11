# -*- coding: utf-8 -*-
"""Équipe I — Programme C204 — module commun des calculs de la machine optimisée (Phase 6).

Constantes CODATA (scipy.constants), paramètres terrestres, palette graphique validée, utilitaires
d'écriture. Tous les scripts i01…i09 importent ce module ; leurs sorties vont dans calculs/resultats/.

Règle du programme : les chiffres des rapports viennent de scripts exécutés. Les valeurs « de fiche
technique » non relues en ligne par nous sont marquées « estimation » dans les tableaux produits.
"""
import csv
import json
import math
from pathlib import Path

from scipy import constants as K

# ---------------------------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------------------------
G = K.G
c = K.c
hbar = K.hbar
kB = K.k
g0 = K.g                       # 9,80665 m/s²
eV = K.e
m_mu_MeV = K.physical_constants["muon mass energy equivalent in MeV"][0]   # 105,658 MeV
m_p_MeV = K.physical_constants["proton mass energy equivalent in MeV"][0]
m_e_MeV = K.physical_constants["electron mass energy equivalent in MeV"][0]
tau_mu = 2.1969811e-6          # s, durée de vie moyenne du muon (PDG ; valeur usuelle)
AN = 365.25 * 86400.0
M_SOLEIL = 1.98847e30
GM_TERRE = 3.986004418e14      # m³/s²
R_TERRE = 6.371e6              # m (rayon moyen)
OMEGA_TERRE = 7.2921150e-5     # rad/s

# Valeurs REVENDIQUÉES par le corpus (affirmations, pas des faits) — dossier de base §4
GAMMA_REVENDIQUE = 10 * 365.25 * 24          # 87 660 : « 10 ans par heure »
MASSE_UNITE = 227.0                          # kg (« about 500 pounds »)
DEPL_REVENDIQUE_S_PAR_H = 10 * AN            # 3,156e8 s par heure

# Géométrie du coffre : rapports sans dimension du modèle de l'Équipe E (06_modele_3D/parametres.json,
# relu le 10/11/2026 après passage à L = 0,85 m) et variante de l'Équipe A (02_reconstruction/dimensions.json)
RAPPORTS_E = dict(P_sur_L=0.3058, Hc_sur_L=0.246, Hcouv_sur_P=0.125, rebord_sur_L=0.0175,
                  x_log=0.382, y_main=0.757, y_steer=0.401, r_log=0.0476)
RAPPORTS_A = dict(P_sur_L=1 / 3.30, Hc_sur_P=0.85, Hcouv_sur_P=0.25, d_log=0.090, entraxe=0.115)
L_NOMINAL = 0.85
L_PLAGE = [0.60, 0.70, 0.85, 1.00, 1.15, 1.20]

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
RES = ICI / "resultats"
FIG = RACINE / "figures"
SCH = RACINE / "schemas"
for _d in (RES, FIG, SCH):
    _d.mkdir(exist_ok=True)

# Palette catégorielle validée (compétence « dataviz », scripts/validate_palette.js, mode clair :
# toutes les vérifications passent ; contraste < 3:1 pour 3 teintes ⇒ étiquettes directes obligatoires).
PALETTE = {"revendique": "#2a78d6", "original": "#eb6834", "R1": "#1baf7a", "R2": "#eda100", "R3": "#e87ba4"}
ENCRE = "#0b0b0b"
ENCRE2 = "#52514e"
SURFACE = "#fcfcfb"
GRILLE = "#dcdbd6"


def fr(x, n=3):
    """Nombre → chaîne française (virgule décimale), n chiffres significatifs, puissances de dix lisibles."""
    if x is None:
        return "—"
    if isinstance(x, str):
        return x
    if x == 0:
        return "0"
    if not math.isfinite(x):
        return "∞" if x > 0 else "−∞"
    a = abs(x)
    if 1e-3 <= a < 1e5:
        s = f"{x:.{n}g}"
        if "e" in s:
            s = f"{x:.0f}"
    else:
        m, e = f"{x:.{n - 1}e}".split("e")
        s = f"{m}×10^{int(e)}"
    return s.replace(".", ",").replace("-", "−")


def ecrire_json(nom, donnees):
    p = RES / nom
    p.write_text(json.dumps(donnees, ensure_ascii=False, indent=1, default=float), encoding="utf-8")
    return p


def ecrire_csv(chemin, entetes, lignes, delim=","):
    with open(chemin, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=delim)
        w.writerow(entetes)
        for l in lignes:
            w.writerow(l)
    return chemin


def ecrire_txt(nom, lignes):
    p = RES / nom
    p.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))
    return p


def geometrie_coffre(L, source="E"):
    """Dimensions extérieures et intérieures utiles du coffre pour une longueur L (m).

    source = 'E' : rapports du modèle 3D de l'Équipe E (hauteur fermée 0,284·L) ;
    source = 'A' : rapports de l'Équipe A (hauteur fermée 0,333·L ; plus favorable).
    Parois : rebord 0,0175·L (E), fond 8 mm, platine à 12 mm sous le bord, dessus de couvercle 6 mm.
    """
    if source == "E":
        P = RAPPORTS_E["P_sur_L"] * L
        Hc = RAPPORTS_E["Hc_sur_L"] * L
        Hcouv = RAPPORTS_E["Hcouv_sur_P"] * P
    else:
        P = RAPPORTS_A["P_sur_L"] * L
        Hc = RAPPORTS_A["Hc_sur_P"] * P
        Hcouv = RAPPORTS_A["Hcouv_sur_P"] * P
    e = RAPPORTS_E["rebord_sur_L"] * L
    Li, Pi = L - 2 * e, P - 2 * e
    Hi_sous_platine = Hc - 0.008 - 0.012 - 0.004        # fond, retrait, épaisseur de platine
    Hi_ferme = Hc + Hcouv - 0.008 - 0.006               # si la platine est ajourée (baie traversante)
    return dict(L=L, P=P, H_corps=Hc, H_couvercle=Hcouv, H_ferme=Hc + Hcouv, e_paroi=e,
                L_int=Li, P_int=Pi, H_int_sous_platine=Hi_sous_platine, H_int_ferme=Hi_ferme,
                V_ext=L * P * (Hc + Hcouv), V_int=Li * Pi * Hi_sous_platine,
                surface_ext=2 * (L * P + L * (Hc + Hcouv) + P * (Hc + Hcouv)),
                d_logement=2 * RAPPORTS_E["r_log"] * L,
                entraxe_logements=(RAPPORTS_E["y_main"] - RAPPORTS_E["y_steer"]) * P)
