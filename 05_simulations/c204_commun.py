# -*- coding: utf-8 -*-
"""Module commun de l'Équipe D (mathématiques et simulation numérique) — programme C204.

Contient : constantes physiques (SI), valeurs revendiquées par le corpus « Titor » (étiquetées
[DOC texte], jamais tenues pour vraies), utilitaires de figures (mention « simulation
illustrative » systématique), registre de tests de validation et écriture JSON.

AVERTISSEMENT : toutes les simulations de ce dossier sont ILLUSTRATIVES. Elles traduisent des
hypothèses en nombres ; elles ne constituent en aucun cas une preuve expérimentale.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")  # moteur de rendu sans affichage (obligatoire pour run_all.sh)
import matplotlib.pyplot as plt  # noqa: E402

# ---------------------------------------------------------------------------
# Constantes physiques (SI). CODATA 2018 ; G, c, ħ, k_B identiques au dossier de base §6.
# ---------------------------------------------------------------------------
G = 6.67430e-11            # constante de gravitation [m^3 kg^-1 s^-2]
C = 299_792_458.0          # vitesse de la lumière [m/s] (exacte)
HBAR = 1.054_571_817e-34   # constante de Planck réduite [J s]
K_B = 1.380_649e-23        # constante de Boltzmann [J/K] (exacte)
EPS0 = 8.854_187_8128e-12  # permittivité du vide [F/m]
MU0 = 1.256_637_062_12e-6  # perméabilité du vide [H/m]
E_CHARGE = 1.602_176_634e-19  # charge élémentaire [C] (exacte)
M_ELECTRON = 9.109_383_7015e-31  # masse de l'électron [kg]
M_PROTON = 1.672_621_923_69e-27  # masse du proton [kg]
G0 = 9.806_65              # pesanteur normale [m/s^2]

# Unités et conversions
HEURE = 3600.0
JOUR = 86400.0
ANNEE = 365.25 * JOUR      # année julienne [s]
LIVRE = 0.453_592_37       # livre avoirdupois [kg]
PIED = 0.3048              # pied [m]
EV = E_CHARGE              # électron-volt [J]
MEV = 1e6 * EV
GEV = 1e9 * EV

# Constantes dérivées
SIGMA_SB = math.pi**2 * K_B**4 / (60.0 * HBAR**3 * C**2)   # Stefan-Boltzmann [W m^-2 K^-4]
M_PLANCK = math.sqrt(HBAR * C / G)                          # masse de Planck [kg]
L_PLANCK = math.sqrt(HBAR * G / C**3)                       # longueur de Planck [m]
T_PLANCK = L_PLANCK / C                                     # temps de Planck [s]
K_COULOMB = 1.0 / (4.0 * math.pi * EPS0)                    # constante de Coulomb
R_ELECTRON_CLASSIQUE = K_COULOMB * E_CHARGE**2 / (M_ELECTRON * C**2)  # 2,818e-15 m
LAMBDA_COMPTON_E_REDUITE = HBAR / (M_ELECTRON * C)          # 3,862e-13 m
R_ELECTRON_BORNE_EXP = 1e-18   # ordre de grandeur de la borne expérimentale (électron ponctuel) [m]
R_PROTON = 0.841e-15           # rayon de charge du proton [m]
E_SCHWINGER = M_ELECTRON**2 * C**3 / (E_CHARGE * HBAR)      # champ critique de Schwinger [V/m]

# Masses de référence
M_SOLEIL = 1.988_47e30
M_TERRE = 5.9722e24
M_JUPITER = 1.898_13e27
AGE_UNIVERS = 13.8e9 * ANNEE

# ---------------------------------------------------------------------------
# Valeurs revendiquées par le corpus (dossier de base §4) — [DOC texte], NON tenues pour vraies.
# ---------------------------------------------------------------------------
REVENDICATIONS = {
    "masse_unite_kg": 500.0 * LIVRE,                 # « environ 500 livres »
    "puissance_W": (300e6, 500e6),                   # « 300–500 mégawatts »
    "pesanteur_g": (1.5, 2.0),                       # « 1,5 à 2 g »
    "distance_m": (1.0, 3.0),                        # plage d'évaluation demandée (1 à 3 m)
    "zone_effet_m": (10 * PIED, 12 * PIED),          # « 10–12 ft de part et d'autre »
    "taux_temporel": 10.0 * ANNEE / HEURE,           # « 10 ans par heure » → dt/dτ ≈ 87 660
    "portee_ans": (50.0, 60.0),                      # « 50–60 ans par saut »
    "temperature_C": ((100 - 32) / 1.8, (120 - 32) / 1.8),  # « 100 à 120 degrés » (°F)
}

MENTION = ("Simulation illustrative — ce n'est PAS une preuve expérimentale "
           "(Équipe D, programme C204 ; aucune affirmation « Titor » n'est tenue pour vraie)")
MENTION_COURTE = "simulation illustrative, non une preuve expérimentale"

# Palette commune (lisible en niveaux de gris, compatible daltonisme — palette d'Okabe-Ito)
COULEURS = {
    "bleu": "#0072B2", "orange": "#E69F00", "vert": "#009E73", "rouge": "#D55E00",
    "violet": "#CC79A7", "ciel": "#56B4E9", "jaune": "#F0E442", "noir": "#000000",
    "gris": "#7F7F7F",
}


def configurer_matplotlib() -> None:
    """Réglages graphiques communs à toutes les figures."""
    plt.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "legend.fontsize": 8.5,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "axes.axisbelow": True,
        "figure.constrained_layout.use": False,
        "mathtext.default": "regular",
    })


def dossiers(fichier_script: str) -> tuple[Path, Path]:
    """Retourne (dossier figures, dossier resultats) du script appelant, en les créant."""
    base = Path(fichier_script).resolve().parent
    fig = base / "figures"
    res = base / "resultats"
    fig.mkdir(parents=True, exist_ok=True)
    res.mkdir(parents=True, exist_ok=True)
    return fig, res


def titre(fig, texte: str, **kw) -> None:
    """Titre général portant la mention obligatoire « simulation illustrative »."""
    fig.suptitle(f"{texte}\n({MENTION_COURTE})", **kw)


def sauver_figure(fig, chemin: Path, rect=(0, 0.035, 1, 0.94)) -> None:
    """Ajoute la mention de bas de page puis enregistre la figure en PNG."""
    try:
        fig.tight_layout(rect=rect)
    except Exception:  # certaines figures 3D refusent tight_layout
        pass
    fig.text(0.5, 0.008, MENTION, ha="center", va="bottom", fontsize=7.5, color="#444444",
             style="italic")
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    print(f"  figure : {chemin}")


def _convertir(o):
    """Conversion des types numpy pour json."""
    if isinstance(o, (np.floating,)):
        v = float(o)
        return v if math.isfinite(v) else str(v)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, Path):
        return str(o)
    if isinstance(o, complex):
        return {"re": o.real, "im": o.imag}
    raise TypeError(f"type non sérialisable : {type(o)}")


def _nettoyer(o):
    """Remplace NaN/inf (non valides en JSON strict) par des chaînes."""
    if isinstance(o, dict):
        return {str(k): _nettoyer(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_nettoyer(v) for v in o]
    if isinstance(o, np.ndarray):
        return _nettoyer(o.tolist())
    if isinstance(o, (float, np.floating)):
        v = float(o)
        return v if math.isfinite(v) else str(v)
    return o


def ecrire_json(chemin: Path, objet) -> None:
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(_nettoyer(objet), f, ensure_ascii=False, indent=2, default=_convertir)
    print(f"  résultats : {chemin}")


def lire_json(chemin: Path):
    with open(chemin, "r", encoding="utf-8") as f:
        return json.load(f)


class Validation:
    """Registre de tests de validation (comparaison à des limites analytiques ou de référence).

    Seuls les TESTS (méthodes `verifier`, `verifier_vrai`) entrent dans le décompte de validation : un
    test confronte le code à une réponse connue indépendamment et peut échouer. Les éléments consignés
    par `consigner` (contrôles de l'ajustement sur lui-même, résultats, repères non vérifiés, biais de
    modèle documentés) sont enregistrés À PART et ne sont jamais comptés comme validations
    (correction n° 39 de la Red Team, phase 7)."""

    def __init__(self, simulation: str):
        self.simulation = simulation
        self.tests: list[dict] = []
        self.hors_decompte: list[dict] = []

    def consigner(self, categorie: str, nom: str, valeur, attendu=None, commentaire: str = "", constat=None) -> None:
        """Enregistre un élément HORS décompte de validation.

        categorie : « contrôle » (cohérence interne, ne peut guère échouer), « résultat » (énoncé d'une
        conclusion), « repère non vérifié » (valeur de référence non contrôlée à la source),
        « biais de modèle » (écart systématique connu et documenté)."""
        def _num(v):
            if isinstance(v, (bool, np.bool_)):
                return bool(v)
            try:
                return float(v)
            except (TypeError, ValueError):
                return v
        d = {"categorie": categorie, "element": nom, "valeur": _num(valeur), "attendu": _num(attendu) if attendu is not None else None,
             "constat": constat if constat is None else bool(constat), "commentaire": commentaire}
        self.hors_decompte.append(d)
        val_txt = f"{d['valeur']:.6g}" if isinstance(d["valeur"], float) else str(d["valeur"])
        att_txt = "" if attendu is None else (f", référence {d['attendu']:.6g}" if isinstance(d["attendu"], float) else f", référence {d['attendu']}")
        cst_txt = "" if constat is None else (" → oui" if constat else " → NON")
        print(f"  [{categorie} — hors décompte] {nom} : {val_txt}{att_txt}{cst_txt}{(' — ' + commentaire) if commentaire else ''}")

    def verifier(self, nom: str, valeur, attendu, tol_rel: float = 1e-6,
                 tol_abs: float = 0.0, commentaire: str = "") -> bool:
        valeur = float(valeur)
        attendu = float(attendu)
        ecart = abs(valeur - attendu)
        seuil = tol_abs + tol_rel * abs(attendu)
        ok = bool(ecart <= seuil) and math.isfinite(valeur)
        self.tests.append({
            "test": nom, "valeur": valeur, "attendu": attendu, "ecart_abs": ecart,
            "ecart_rel": (ecart / abs(attendu)) if attendu != 0 else None,
            "tol_rel": tol_rel, "tol_abs": tol_abs, "passe": ok, "commentaire": commentaire,
        })
        print(f"  [{'OK  ' if ok else 'ÉCHEC'}] {nom} : obtenu {valeur:.6g}, attendu {attendu:.6g}"
              f" (écart {ecart:.3g}, seuil {seuil:.3g})")
        return ok

    def verifier_vrai(self, nom: str, condition: bool, commentaire: str = "") -> bool:
        ok = bool(condition)
        self.tests.append({"test": nom, "valeur": ok, "attendu": True, "passe": ok,
                           "commentaire": commentaire})
        print(f"  [{'OK  ' if ok else 'ÉCHEC'}] {nom} {('— ' + commentaire) if commentaire else ''}")
        return ok

    def bilan(self) -> dict:
        n_ok = sum(1 for t in self.tests if t["passe"])
        return {"simulation": self.simulation, "n_tests": len(self.tests), "n_passes": n_ok,
                "n_echecs": len(self.tests) - n_ok, "tests": self.tests,
                "n_hors_decompte": len(self.hors_decompte), "hors_decompte": self.hors_decompte}

    def imprimer_bilan(self) -> None:
        b = self.bilan()
        suite = f" ; {b['n_hors_decompte']} contrôles, résultats ou repères hors décompte" if b["n_hors_decompte"] else ""
        print(f"  Bilan validation {self.simulation} : {b['n_passes']}/{b['n_tests']} tests passés{suite}")


_EXPOSANTS = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(x: float, n: int = 3) -> str:
    """Notation scientifique française courte, p. ex. 1,23×10¹² (exposants Unicode)."""
    x = float(x)
    if x == 0 or not math.isfinite(x):
        return str(x)
    e = int(math.floor(math.log10(abs(x))))
    m = round(x / 10**e, n - 1)
    if abs(m) >= 10:   # arrondi ayant fait basculer la mantisse
        m /= 10
        e += 1
    return f"{m:.{n - 1}f}".replace(".", ",") + "×10" + str(e).translate(_EXPOSANTS)


def sci_tex(x: float, n: int = 2) -> str:
    """Notation scientifique pour mathtext, p. ex. $1{,}2\\times10^{12}$."""
    if x == 0 or not math.isfinite(x):
        return str(x)
    e = int(math.floor(math.log10(abs(x))))
    m = x / 10**e
    ms = f"{m:.{n - 1}f}".replace(".", "{,}")
    return rf"${ms}\times10^{{{e}}}$"
