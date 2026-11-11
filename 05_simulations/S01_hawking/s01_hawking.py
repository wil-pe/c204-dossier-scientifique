# -*- coding: utf-8 -*-
"""S01 — Thermodynamique d'un micro-trou noir (Hawking) et carte de contraintes « C204 ».

SIMULATION ILLUSTRATIVE : calcul semi-classique standard appliqué aux valeurs revendiquées par
le corpus « Titor ». Ce n'est pas une preuve expérimentale ; le rayonnement de Hawking lui-même
n'a jamais été observé pour un trou noir.

Exécution (depuis la racine du projet) :
    .venv/bin/python 05_simulations/S01_hawking/s01_hawking.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402

cc.configurer_matplotlib()
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S01_hawking")

# ---------------------------------------------------------------------------
# 1. Modèle
# ---------------------------------------------------------------------------
# Variable : M, masse du trou noir de Schwarzschild [kg] (charge et rotation négligées ici ;
# elles réduisent T et P, donc renforcent les conclusions sur la puissance).
# Unité naturelle de puissance×M² : ħ c^6 / G^2 ; de perte de masse×M² : ħ c^4 / G^2.
U_P = cc.HBAR * cc.C**6 / cc.G**2      # [W kg^2]
U_MDOT = cc.HBAR * cc.C**4 / cc.G**2   # [kg^3 / s]

# (a) Corps noir « naïf » : photons seuls, surface 4π r_s², loi de Stefan-Boltzmann.
COEF_CORPS_NOIR = 1.0 / (15360.0 * np.pi)          # = 2,072e-5

# (b) Coefficients de Page (1976, Phys. Rev. D 13, 198), facteurs de corps gris inclus,
#     en unités ħc^6/(G²M²) : spin 1/2 (une espèce de neutrino à 2 composantes ν+ν̄), spin 1
#     (photon, 2 polarisations), spin 2 (graviton, 2 polarisations).
PAGE_SPIN_DEMI = 8.183e-5
PAGE_SPIN_1 = 3.366e-5
PAGE_SPIN_2 = 3.84e-6
PAGE_TOTAL_1976 = 2 * PAGE_SPIN_DEMI + PAGE_SPIN_1 + PAGE_SPIN_2   # 2 espèces ν connues en 1976

# (c) Facteur d'espèces f(M) de MacGibbon (1991, Phys. Rev. D 44, 376) :
#     dM/dt = -5,34e25 f(M) / M² [g/s, M en g] ; f = 1 pour photons + 3 neutrinos + graviton.
ALPHA_MACGIBBON = 5.34e25 * 1e-9      # [kg^3/s]  (1 g^3 = 1e-9 kg^3)
# (nom, poids f_j, masse-seuil M_j en grammes) : terme f_j · exp(-M / M_j)
ESPECES_1991 = [
    ("électron e±", 0.569, 9.42e16),
    ("muon μ±", 0.569, 4.53e14),
    ("quarks u, d", 6 * 0.569, 1.60e14),
    ("quark s", 3 * 0.569, 9.60e13),
    ("quark c", 3 * 0.569, 2.56e13),
    ("tau τ±", 0.569, 2.68e13),
    ("quark b", 3 * 0.569, 9.07e12),
    ("quark t (100 GeV supposé en 1991)", 3 * 0.569, 0.48e12),
    ("gluons", 0.963, 1.10e14),
]
# Extension [HYP de l'Équipe D] : secteur électrofaible ajouté avec la même recette
# (poids par degré de liberté : spin 1 → 0,060 ; spin 0 → 0,267 ; M_j = β_s·1,06e13 g·GeV/m_j,
#  β_1 = 6,04 ; β_0 = 2,66). W± et Z : 6 d.d.l. transverses (spin 1) ; Higgs + 3 modes
#  longitudinaux : 4 d.d.l. scalaires. Total haute énergie f = 15,35, valeur citée par
#  Carr, Kohri, Sendouda & Yokoyama (2010, Phys. Rev. D 81, 104019). Effet < 10 % sur f,
#  uniquement pour M < 10^9 kg.
ESPECES_EXTENSION = [
    ("W± transverses (4 d.d.l.)", 4 * 0.060, 6.04 * 1.06e13 / 80.38),
    ("Z transverse (2 d.d.l.)", 2 * 0.060, 6.04 * 1.06e13 / 91.19),
    ("Higgs + 3 modes longitudinaux (4 d.d.l. scalaires)", 4 * 0.267, 2.66 * 1.06e13 / 125.25),
]


def rayon_schwarzschild(M):
    """r_s = 2GM/c² [m]."""
    return 2.0 * cc.G * M / cc.C**2


def temperature_hawking(M):
    """T = ħc³/(8πGMk_B) [K]."""
    return cc.HBAR * cc.C**3 / (8.0 * np.pi * cc.G * M * cc.K_B)


def puissance_corps_noir(M):
    """Photons seuls, corps noir de surface 4πr_s² : P = ħc^6/(15360πG²M²) [W]."""
    return COEF_CORPS_NOIR * U_P / M**2


def puissance_photons_page(M):
    """Photons seuls avec facteurs de corps gris (Page 1976) [W]."""
    return PAGE_SPIN_1 * U_P / M**2


def facteur_especes(M, etendu=True):
    """f(M) de MacGibbon (1991) ; M en kg. etendu=True ajoute W, Z, H ([HYP])."""
    Mg = np.asarray(M, dtype=float) * 1e3   # en grammes
    f = np.ones_like(Mg)
    for _, poids, seuil in ESPECES_1991 + (ESPECES_EXTENSION if etendu else []):
        f = f + poids * np.exp(-Mg / seuil)
    return f


def puissance_totale(M, etendu=True):
    """Puissance totale toutes espèces : P = α f(M) c² / M² [W]."""
    return ALPHA_MACGIBBON * facteur_especes(M, etendu) * cc.C**2 / np.asarray(M, float)**2


def duree_de_vie_corps_noir(M):
    """τ = 5120 π G² M³ / (ħ c⁴) [s] (photons seuls, corps noir)."""
    return 5120.0 * np.pi * cc.G**2 * M**3 / (cc.HBAR * cc.C**4)


def duree_de_vie_especes(M0, etendu=True, M_fin=None):
    """τ(M0) = ∫ M² dM / (α f(M)) de M_fin (masse de Planck par défaut) à M0 [s], par quadrature.

    On intègre en variable u = ln M pour couvrir de nombreuses décades."""
    M_fin = cc.M_PLANCK if M_fin is None else M_fin
    if M0 <= M_fin:
        return 0.0
    integrande = lambda u: np.exp(3 * u) / (ALPHA_MACGIBBON * float(facteur_especes(np.exp(u), etendu)))
    bornes = np.linspace(np.log(M_fin), np.log(M0), 60)
    total = 0.0
    for a, b in zip(bornes[:-1], bornes[1:]):
        total += quad(integrande, a, b, epsabs=0, epsrel=1e-10)[0]
    return total


def masse_pour_duree(t, etendu=True):
    """Masse initiale dont la durée de vie vaut t [s] (toutes espèces)."""
    return 10**brentq(lambda lm: duree_de_vie_especes(10**lm, etendu) - t, -7.0, 20.0, xtol=1e-12)


def integrer_evaporation(M0, etendu=True, regularise=True, n=400, M_arret=None):
    """Intègre dM/dt = -α f(M)/M² depuis M(0) = M0 jusqu'à M_arret (masse de Planck par défaut).

    regularise=True : variable x = M³ (dx/dt = -3 α f, régulier) ;
    regularise=False : variable M directe (dM/dt → -∞ quand M → 0 : singularité en temps fini).
    Condition initiale : M(0) = M0. Arrêt : événement M = M_arret (la masse de Planck est la
    limite de validité du calcul semi-classique)."""
    tau = duree_de_vie_especes(M0, etendu)
    M_arret = cc.M_PLANCK if M_arret is None else M_arret
    if regularise:
        f = lambda t, x: [-3 * ALPHA_MACGIBBON * float(facteur_especes(max(x[0], 0.0)**(1 / 3) + 1e-300, etendu))]
        ev = lambda t, x: x[0] - M_arret**3
        ev.terminal = True
        sol = solve_ivp(f, (0, 1.5 * tau), [M0**3], method="RK45", rtol=1e-10, atol=0.0,
                        events=ev, dense_output=True)
        t_fin = sol.t_events[0][0] if len(sol.t_events[0]) else sol.t[-1]
        t = t_fin * (1 - np.logspace(-12, 0, n)[::-1])
        t = np.concatenate([t, [t_fin]])
        M = np.maximum(sol.sol(t)[0], M_arret**3) ** (1 / 3)
    else:
        f = lambda t, y: [-ALPHA_MACGIBBON * float(facteur_especes(y[0], etendu)) / y[0]**2]
        ev = lambda t, y: y[0] - M_arret
        ev.terminal = True
        sol = solve_ivp(f, (0, 1.5 * tau), [M0], method="LSODA", rtol=1e-10, atol=0.0, events=ev)
        t_fin = sol.t_events[0][0] if len(sol.t_events[0]) else sol.t[-1]
        t, M = sol.t, sol.y[0]
    return t, M, t_fin, sol


# ---------------------------------------------------------------------------
# 2. Tests de validation
# ---------------------------------------------------------------------------
print("S01 — tests de validation")
# 2.1 Coefficients numériques du dossier de base §6 (re-dérivation indépendante)
val.verifier("r_s par kg (dossier : 1,485e-27 m/kg)", rayon_schwarzschild(1.0), 1.485e-27, tol_rel=1e-3)
val.verifier("T×M (dossier : 1,227e23 K·kg)", temperature_hawking(1.0), 1.227e23, tol_rel=1e-3)
val.verifier("P×M² corps noir (dossier : 3,56e32 W·kg²)", puissance_corps_noir(1.0), 3.56e32, tol_rel=2e-3)
val.verifier("τ/M³ corps noir (dossier : 8,41e-17 s/kg³)", duree_de_vie_corps_noir(1.0), 8.41e-17, tol_rel=2e-3)
# 2.2 Cohérence interne : P corps noir = σ·(4π r_s²)·T⁴
M_test = 1e12
val.verifier("P corps noir = σ·A·T⁴ (M = 1e12 kg)",
             cc.SIGMA_SB * 4 * np.pi * rayon_schwarzschild(M_test)**2 * temperature_hawking(M_test)**4,
             puissance_corps_noir(M_test), tol_rel=1e-9)
# 2.3 Cohérence Page (1976) : total = 2,011e-4 ; fractions 81,4 % / 16,7 % / 1,9 %
val.verifier("Somme des coefficients de Page (1976)", PAGE_TOTAL_1976, 2.011e-4, tol_rel=1e-3)
val.verifier("Fraction photons (Page 1976 : 16,7 %)", PAGE_SPIN_1 / PAGE_TOTAL_1976, 0.167, tol_rel=1e-2)
# 2.4 Cohérence MacGibbon (f = 1) ↔ Page (photons + 3 espèces ν + graviton)
coef_macgibbon = ALPHA_MACGIBBON / U_MDOT
coef_page_3nu = 3 * PAGE_SPIN_DEMI + PAGE_SPIN_1 + PAGE_SPIN_2
val.verifier("α(MacGibbon, f=1) ≈ Page(γ + 3ν + graviton)", coef_macgibbon, coef_page_3nu, tol_rel=0.03,
             commentaire="deux sources indépendantes, accord attendu à quelques %")
# 2.5 Durée de vie : quadrature ↔ formule analytique à f constant (M très grand : f → 1)
M_grand = 1e18
val.verifier("τ(quadrature) = M³/(3αf) pour f ≈ 1 (M = 1e18 kg)",
             duree_de_vie_especes(M_grand), M_grand**3 / (3 * ALPHA_MACGIBBON), tol_rel=1e-3)
# 2.6 Intégration temporelle ↔ quadrature (deux formulations)
for M0 in (cc.REVENDICATIONS["masse_unite_kg"] / 2, 1e9, 1e12):
    tq = duree_de_vie_especes(M0)
    _, _, t_reg, _ = integrer_evaporation(M0, regularise=True)
    val.verifier(f"τ ODE régularisée (x = M³) ↔ quadrature, M0 = {M0:.3g} kg", t_reg, tq, tol_rel=1e-6)
# Formulation naïve (variable M) : dM/dt diverge comme -(τ - t)^(-2/3) ; on documente son échec
# quand on vise la masse de Planck, puis on la valide sur un arrêt à 1e-4·M0 (où elle reste gérable).
divergence_naive = {}
try:
    _, _, t_naif_pl, sol_naif_pl = integrer_evaporation(1e9, regularise=False)
    divergence_naive["jusqu_a_M_Planck"] = {"reussi": True, "tau_s": t_naif_pl, "n_evaluations": int(sol_naif_pl.nfev)}
except Exception as exc:  # noqa: BLE001 — l'échec est précisément le résultat documenté
    divergence_naive["jusqu_a_M_Planck"] = {"reussi": False, "erreur": f"{type(exc).__name__}: {exc}"}
    print(f"  [note] intégration naïve jusqu'à M_Planck : ÉCHEC attendu et documenté ({type(exc).__name__})")
_, _, t_naif, sol_naif = integrer_evaporation(1e9, regularise=False, M_arret=1e5)
divergence_naive["jusqu_a_1e-4_M0"] = {"reussi": True, "tau_s": t_naif, "n_evaluations": int(sol_naif.nfev)}
val.verifier("τ ODE naïve (variable M, LSODA, arrêt à 1e-4·M0) ↔ quadrature, M0 = 1e9 kg", t_naif,
             duree_de_vie_especes(1e9) - duree_de_vie_especes(1e5), tol_rel=1e-6,
             commentaire=f"{sol_naif.nfev} évaluations ; la formulation naïve échoue si l'on vise M_Planck")
# 2.7 Repères de la littérature sur les trous noirs primordiaux
#  (a) τ ≈ 407 s·(f/15,35)^-1·(M/1e10 g)³ (Carr et al. 2010) : même constante α, f(∞) = 15,35
val.verifier("f(M→0) étendu = 15,35 (Carr et al. 2010)", float(facteur_especes(1e-3)), 15.35, tol_rel=5e-3)
val.verifier("τ(M = 1e7 kg, f = 15,35) = 407 s (Carr et al. 2010)", (1e7)**3 / (3 * ALPHA_MACGIBBON * 15.35), 407.0, tol_rel=5e-3)
#  (b) masse initiale s'évaporant en un âge d'Univers. Estimation « f gelé à 1,9 » (Carr et al.
#      2010 : M* ≈ 5,1e14 g), puis intégration complète de la paramétrisation de 1991.
M_etoile_f_gele = (3 * ALPHA_MACGIBBON * 1.9 * cc.AGE_UNIVERS) ** (1 / 3)
val.verifier("M* avec f gelé à 1,9 ≈ 5,1e11 kg (Carr et al. 2010)", M_etoile_f_gele, 5.1e11, tol_rel=0.01)
M_etoile = masse_pour_duree(cc.AGE_UNIVERS, etendu=False)
# Correction n° 42 (Red Team, phase 7) : l'écart de +6,8 % avec la valeur de 2008 est un BIAIS DU MODÈLE (seuils hadroniques
# approchés de la paramétrisation de 1991 ; l'Équipe B, avec le même modèle, trouve aussi 5,3e11 kg). Ce n'est pas une
# « réussite à 10 % » : la comparaison est consignée hors décompte. (Historique : tolérance de 6 % → échec à 6,8 % ;
# tolérance portée après coup à 10 % ; désormais retirée du registre de validation.)
val.consigner("biais de modèle", "M* intégré (τ = 13,8 Ga) contre 5,0e11 kg (MacGibbon, Carr & Page 2008)", M_etoile, 5.0e11,
              commentaire=f"écart {100 * (M_etoile / 5.0e11 - 1):+.1f} % : biais de la paramétrisation f(M) de 1991, commun à l'Équipe B",
              constat=None)
# 2.8 Loi d'échelle : P ∝ M⁻² (corps noir) vérifiée numériquement
pente = np.polyfit(np.log([1e3, 1e6, 1e9]), np.log(puissance_corps_noir(np.array([1e3, 1e6, 1e9]))), 1)[0]
val.verifier("Pente d ln P / d ln M (corps noir)", pente, -2.0, tol_abs=1e-9)

# ---------------------------------------------------------------------------
# 3. Valeurs revendiquées et inversions
# ---------------------------------------------------------------------------
R = cc.REVENDICATIONS
M_UNITE = R["masse_unite_kg"]
P_MIN, P_MAX = R["puissance_W"]
G_MIN, G_MAX = R["pesanteur_g"]
D_MIN, D_MAX = R["distance_m"]


def masse_pour_puissance(P, modele):
    if modele == "corps_noir":
        return np.sqrt(COEF_CORPS_NOIR * U_P / P)
    if modele == "photons_page":
        return np.sqrt(PAGE_SPIN_1 * U_P / P)
    if modele == "total_especes":
        return 10**brentq(lambda lm: float(puissance_totale(10**lm)) - P, 0.0, 18.0, xtol=1e-12)
    raise ValueError(modele)


bandes_puissance = {m: (masse_pour_puissance(P_MAX, m), masse_pour_puissance(P_MIN, m))
                    for m in ("corps_noir", "photons_page", "total_especes")}
# Pesanteur a = G M / r² → M = a r² / G
M_g_min = G_MIN * cc.G0 * D_MIN**2 / cc.G
M_g_max = G_MAX * cc.G0 * D_MAX**2 / cc.G
# Durées de mission (hypothèses explicites [HYP])
DUREES = {
    "un saut de 60 ans à 10 ans/h (6 h)": 6 * cc.HEURE,
    "une année de service": cc.ANNEE,
    "trente ans de service": 30 * cc.ANNEE,
}
M_duree = {k: masse_pour_duree(t) for k, t in DUREES.items()}
# « Taille d'un électron » : trois définitions possibles
TAILLES_ELECTRON = {
    "rayon classique de l'électron (2,82 fm)": cc.R_ELECTRON_CLASSIQUE,
    "longueur de Compton réduite (386 fm)": cc.LAMBDA_COMPTON_E_REDUITE,
    "borne expérimentale ~1e-18 m (électron ponctuel)": cc.R_ELECTRON_BORNE_EXP,
}
M_taille = {k: r * cc.C**2 / (2 * cc.G) for k, r in TAILLES_ELECTRON.items()}

# Valeurs aux masses repères
reperes = {}
for nom, M in {"unité entière (227 kg)": M_UNITE, "demi-unité (113 kg)": M_UNITE / 2,
               "1e9 kg": 1e9, "1e11 kg": 1e11, "1e12 kg": 1e12, "4,4e12 kg": 4.4e12}.items():
    reperes[nom] = {
        "M_kg": M, "r_s_m": rayon_schwarzschild(M), "T_K": temperature_hawking(M),
        "kT_MeV": cc.K_B * temperature_hawking(M) / cc.MEV,
        "P_corps_noir_W": puissance_corps_noir(M), "P_photons_page_W": puissance_photons_page(M),
        "P_totale_especes_W": float(puissance_totale(M)), "f_especes": float(facteur_especes(M)),
        "duree_vie_corps_noir_s": duree_de_vie_corps_noir(M), "duree_vie_especes_s": duree_de_vie_especes(M),
        "energie_de_masse_J": M * cc.C**2,
        "acceleration_a_1m_g": cc.G * M / 1.0**2 / cc.G0,
    }

# Flux et température d'équilibre à 1 m pour 300–500 MW (ordre de grandeur, corps noir absorbant)
flux_1m = np.array([P_MIN, P_MAX]) / (4 * np.pi * 1.0**2)
T_equilibre_1m = (flux_1m / cc.SIGMA_SB) ** 0.25

# ---------------------------------------------------------------------------
# 4. Intersections de contraintes
# ---------------------------------------------------------------------------


def intersection(*intervalles):
    bas = max(i[0] for i in intervalles)
    haut = min(i[1] for i in intervalles)
    return (bas, haut) if bas < haut else None


INF = 1e30
contraintes = {
    "C1 masse ≤ unité de 227 kg (2 singularités ≤ 113 kg chacune)": (cc.M_PLANCK, M_UNITE / 2),
    "C2a P = 300–500 MW (photons, corps noir)": bandes_puissance["corps_noir"],
    "C2b P = 300–500 MW (photons, Page 1976)": bandes_puissance["photons_page"],
    "C2c P = 300–500 MW (toutes espèces, MacGibbon 1991)": bandes_puissance["total_especes"],
    "C3 1,5–2 g entre 1 et 3 m": (M_g_min, M_g_max),
    "C4 durée de vie ≥ 6 h": (M_duree["un saut de 60 ans à 10 ans/h (6 h)"], INF),
    "C4' durée de vie ≥ 30 ans": (M_duree["trente ans de service"], INF),
    "C5 r_s < rayon classique de l'électron": (cc.M_PLANCK, M_taille["rayon classique de l'électron (2,82 fm)"]),
    "C5' r_s < 1e-18 m": (cc.M_PLANCK, M_taille["borne expérimentale ~1e-18 m (électron ponctuel)"]),
}
cles = list(contraintes)
inter = {
    "sans_C1_photons_corps_noir (C2a∩C3∩C4'∩C5)": intersection(contraintes[cles[1]], contraintes[cles[4]],
                                                              contraintes[cles[6]], contraintes[cles[7]]),
    "sans_C1_photons_page (C2b∩C3∩C4'∩C5)": intersection(contraintes[cles[2]], contraintes[cles[4]],
                                                        contraintes[cles[6]], contraintes[cles[7]]),
    "sans_C1_toutes_especes (C2c∩C3∩C4'∩C5)": intersection(contraintes[cles[3]], contraintes[cles[4]],
                                                          contraintes[cles[6]], contraintes[cles[7]]),
    "sans_C1_toutes_especes_sans_taille (C2c∩C3∩C4')": intersection(contraintes[cles[3]], contraintes[cles[4]],
                                                                   contraintes[cles[6]]),
    "avec_C1_photons_corps_noir (C1∩C2a∩C3∩C4∩C5)": intersection(contraintes[cles[0]], contraintes[cles[1]],
                                                                contraintes[cles[4]], contraintes[cles[5]],
                                                                contraintes[cles[7]]),
    "C1∩C4 (masse d'unité et durée de vie ≥ 6 h)": intersection(contraintes[cles[0]], contraintes[cles[5]]),
    "C1∩C2a (masse d'unité et puissance)": intersection(contraintes[cles[0]], contraintes[cles[1]]),
    "C1∩C3 (masse d'unité et pesanteur)": intersection(contraintes[cles[0]], contraintes[cles[4]]),
    "C5'∩C3 (rayon < 1e-18 m et pesanteur)": intersection(contraintes[cles[8]], contraintes[cles[4]]),
}
ecart_decades = np.log10(bandes_puissance["corps_noir"][0] / (M_UNITE / 2))
val.verifier_vrai("Intersection C1∩C2∩C3 vide (résultat attendu du dossier §6)",
                  inter["C1∩C2a (masse d'unité et puissance)"] is None
                  and inter["C1∩C3 (masse d'unité et pesanteur)"] is None)

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
M = np.logspace(-7.5, 16, 800)
col = cc.COULEURS

# --- Figure 1 : température et rayon -------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
ax1.loglog(M, temperature_hawking(M), color=col["rouge"], lw=2, label=r"$T = \hbar c^3/(8\pi G M k_B)$")
ax1.set_xlabel("masse M du trou noir [kg]")
ax1.set_ylabel("température de Hawking T [K]")
axe_ev = ax1.secondary_yaxis("right", functions=(lambda T: cc.K_B * T / cc.EV, lambda E: E * cc.EV / cc.K_B))
axe_ev.set_ylabel(r"$k_B T$ [eV]")
for nom, Mv, c, dec, ha in (("113 kg (demi-unité)", M_UNITE / 2, col["bleu"], (8, 8), "left"),
                            ("$10^{12}$ kg", 1e12, col["vert"], (-8, 10), "right")):
    ax1.axvline(Mv, color=c, ls="--", lw=1.2)
    ax1.plot(Mv, temperature_hawking(Mv), "o", color=c)
    ax1.annotate(f"{nom}\nT = {cc.sci(temperature_hawking(Mv))} K\n"
                 f"$k_BT$ = {cc.sci(cc.K_B * temperature_hawking(Mv) / cc.MEV)} MeV",
                 (Mv, temperature_hawking(Mv)), textcoords="offset points", xytext=dec, fontsize=8, color=c, ha=ha)
ax1.axhspan(1e6, 1e9, color=col["jaune"], alpha=0.35, label="domaine des rayons X thermiques (~0,1–100 keV)")
ax1.axvline(cc.M_PLANCK, color=col["gris"], ls=":", lw=1)
ax1.text(cc.M_PLANCK * 1.3, 1e9, "masse de Planck\n(limite de validité)", fontsize=7.5, color=col["gris"])
ax1.set_title("Température de Hawking")
ax1.legend(loc="lower left")

ax2.loglog(M, rayon_schwarzschild(M), color=col["noir"], lw=2, label=r"$r_s = 2GM/c^2$")
for (nom, r), c in zip(TAILLES_ELECTRON.items(), (col["rouge"], col["orange"], col["violet"])):
    ax2.axhline(r, color=c, ls="--", lw=1.2)
    ax2.text(2e-7, r * 1.6, nom, color=c, fontsize=8)
    ax2.plot(r * cc.C**2 / (2 * cc.G), r, "o", color=c)
ax2.axhline(cc.R_PROTON, color=col["vert"], ls=":", lw=1.2)
ax2.text(2e-7, cc.R_PROTON * 0.08, "rayon de charge du proton (0,84 fm)", color=col["vert"], fontsize=8)
ax2.axhline(cc.L_PLANCK, color=col["gris"], ls=":", lw=1)
ax2.text(1e5, cc.L_PLANCK * 1.5, "longueur de Planck", color=col["gris"], fontsize=8)
ax2.axvline(M_UNITE / 2, color=col["bleu"], ls="--", lw=1.2)
ax2.text(M_UNITE / 2 * 1.5, 1e-31, f"113 kg :\n$r_s$ = {cc.sci(rayon_schwarzschild(M_UNITE / 2))} m", color=col["bleu"], fontsize=8)
ax2.axvspan(*bandes_puissance["corps_noir"], color=col["vert"], alpha=0.3)
ax2.text(bandes_puissance["corps_noir"][0] * 0.02, 3e-22, "M pour 300–500 MW\n(photons, corps noir)", color=col["vert"], fontsize=8)
ax2.set_xlabel("masse M du trou noir [kg]")
ax2.set_ylabel("rayon de Schwarzschild $r_s$ [m]")
ax2.set_title("Rayon d'horizon et « taille d'un électron »")
ax2.legend(loc="lower right")
cc.titre(fig, "S01 — Micro-trou noir : température de Hawking et rayon d'horizon en fonction de la masse")
cc.sauver_figure(fig, FIG / "S01_fig1_temperature_rayon.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : puissance ---------------------------------------------------------------------
fig, (ax1, axz, ax2) = plt.subplots(1, 3, figsize=(15.5, 5.4), gridspec_kw={"width_ratios": [1.25, 1.1, 0.9]})
for ax in (ax1, axz):
    ax.loglog(M, puissance_corps_noir(M), color=col["bleu"], lw=2, label="photons seuls, corps noir $4\\pi r_s^2$ (dossier §6)")
    ax.loglog(M, puissance_photons_page(M), color=col["ciel"], lw=2, ls="--", label="photons seuls, corps gris (Page 1976)")
    ax.loglog(M, puissance_totale(M), color=col["rouge"], lw=2, label="toutes espèces, f(M) (MacGibbon 1991 + W, Z, H [HYP])")
    ax.axhspan(P_MIN, P_MAX, color=col["orange"], alpha=0.45, label="revendication : 300–500 MW")
    ax.set_xlabel("masse M du trou noir [kg]")
ax1.axvline(M_UNITE / 2, color=col["noir"], ls="--", lw=1.2)
ax1.annotate(f"113 kg (demi-unité) :\nP ≈ {cc.sci(float(puissance_totale(M_UNITE / 2)))} W\n(toutes espèces)",
             (M_UNITE / 2, float(puissance_totale(M_UNITE / 2))), textcoords="offset points", xytext=(10, 0), fontsize=8)
ax1.set_xlim(1e-7, 1e16)
ax1.set_ylim(1e-2, 1e50)
ax1.set_ylabel("puissance rayonnée P [W]")
ax1.set_title("Puissance de Hawking : vue d'ensemble")
ax1.legend(loc="lower left", fontsize=7.5)
for m, c, y in (("corps_noir", col["bleu"], 3e6), ("photons_page", col["ciel"], 1.5e5), ("total_especes", col["rouge"], 3e6)):
    b_ = bandes_puissance[m]
    axz.axvspan(*b_, color=c, alpha=0.25)
    axz.text(np.sqrt(b_[0] * b_[1]), y, f"{cc.sci(b_[0], 2)}\nà\n{cc.sci(b_[1], 2)} kg", color=c, fontsize=7.5, ha="center")
axz.set_xlim(2e11, 2e13)
axz.set_ylim(1e5, 3e11)
axz.set_title("Zoom : masses donnant 300–500 MW")
ax2.semilogx(M, facteur_especes(M, etendu=False), color=col["noir"], lw=2, label="f(M), MacGibbon 1991")
ax2.semilogx(M, facteur_especes(M, etendu=True), color=col["rouge"], lw=1.5, ls="--", label="f(M) + W, Z, H ([HYP] Équipe D)")
ax2.axvline(M_UNITE / 2, color=col["bleu"], ls="--", lw=1)
ax2.text(M_UNITE / 2 * 2, 10.5, "113 kg", color=col["bleu"], fontsize=8)
ax2.axvspan(*bandes_puissance["total_especes"], color=col["rouge"], alpha=0.25)
ax2.set_xlim(1e-3, 1e16)
ax2.set_xlabel("masse M [kg]")
ax2.set_ylabel("f(M)  (f = 1 : γ + 3ν + graviton)")
ax2.set_title("Facteur d'espèces émises")
ax2.legend(loc="lower left", fontsize=7.5)
cc.titre(fig, "S01 — Puissance de Hawking P(M) et facteur d'espèces, comparés aux « 300–500 MW » revendiqués")
cc.sauver_figure(fig, FIG / "S01_fig2_puissance.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : évaporation -------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5.2))
evap = {}
x_lin = np.linspace(0.0, 1.0, 600)
for M0, c in ((M_UNITE / 2, col["bleu"]), (1e9, col["vert"]), (1e12, col["rouge"])):
    _, _, t_fin, sol = integrer_evaporation(M0)
    M_num = np.maximum(sol.sol(np.minimum(x_lin * t_fin, sol.t[-1]))[0], 0.0) ** (1 / 3)
    evap[f"{M0:.4g}"] = {"duree_vie_s": t_fin, "energie_liberee_J": M0 * cc.C**2,
                         "puissance_initiale_W": float(puissance_totale(M0))}
    ax1.plot(x_lin, M_num / M0, color=c, lw=2, label=f"$M_0$ = {cc.sci(M0, 2)} kg ; τ = {cc.sci(t_fin, 2)} s")
ax1.plot(x_lin, (1 - x_lin) ** (1 / 3), color=col["noir"], ls=":", lw=1.5,
         label=r"limite analytique à f constant : $(1 - t/\tau)^{1/3}$")
ax1.set_xlabel("temps réduit t/τ")
ax1.set_ylabel("$M(t)/M_0$")
ax1.set_title("Évaporation : intégration de $dM/dt = -\\alpha f(M)/M^2$ (variable régularisée $x = M^3$)")
ax1.title.set_fontsize(9.5)
ax1.legend(loc="lower left", fontsize=8)
ax1.text(0.03, 0.42, "La pente devient infinie en t = τ\n(singularité en temps fini ;\n"
         "calcul semi-classique invalide\nsous la masse de Planck).", transform=ax1.transAxes, fontsize=8,
         bbox=dict(fc="white", ec=col["gris"], alpha=0.9))

M0s = np.logspace(0, 13.5, 120)
tau_bb = duree_de_vie_corps_noir(M0s)
tau_esp = np.array([duree_de_vie_especes(m) for m in M0s])
ax2.loglog(M0s, tau_bb, color=col["bleu"], lw=2, label="photons seuls, corps noir (dossier §6)")
ax2.loglog(M0s, tau_esp, color=col["rouge"], lw=2, label="toutes espèces (quadrature)")
for (nom, tdur), c, fy in zip(DUREES.items(), (col["orange"], col["vert"], col["violet"]), (0.02, 0.02, 4.0)):
    ax2.axhline(tdur, color=c, ls="--", lw=1.2)
    ax2.text(1.5, tdur * fy, f"{nom} → M ≥ {cc.sci(M_duree[nom], 2)} kg", color=c, fontsize=8)
ax2.axhline(cc.AGE_UNIVERS, color=col["gris"], ls=":", lw=1.2)
ax2.text(1.5, cc.AGE_UNIVERS * 3, "âge de l'Univers", color=col["gris"], fontsize=8)
ax2.axvline(M_UNITE / 2, color=col["noir"], ls="--", lw=1.2)
ax2.annotate(f"113 kg : τ ≈ {cc.sci(duree_de_vie_especes(M_UNITE / 2), 2)} s", (M_UNITE / 2, duree_de_vie_especes(M_UNITE / 2)),
             textcoords="offset points", xytext=(10, -2), fontsize=8)
ax2.set_xlabel("masse initiale $M_0$ [kg]")
ax2.set_ylabel("durée de vie τ [s]")
ax2.set_title("Durée de vie et durées de mission")
ax2.legend(loc="lower right", fontsize=8)
cc.titre(fig, "S01 — Évaporation d'un micro-trou noir : M(t) et durée de vie")
cc.sauver_figure(fig, FIG / "S01_fig3_evaporation.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 4 : carte de contraintes (axe des masses) ---------------------------------------
fig, ax = plt.subplots(figsize=(12.5, 6.4))
lignes = [
    ("C1 — masse d'une singularité ≤ 113 kg\n(unité de 227 kg, deux singularités)", contraintes[cles[0]], col["bleu"]),
    ("C2a — P = 300–500 MW\n(photons, corps noir)", contraintes[cles[1]], col["orange"]),
    ("C2b — P = 300–500 MW\n(photons, Page 1976)", contraintes[cles[2]], col["orange"]),
    ("C2c — P = 300–500 MW\n(toutes espèces)", contraintes[cles[3]], col["rouge"]),
    ("C3 — 1,5 à 2 g\nentre 1 et 3 m", contraintes[cles[4]], col["vert"]),
    ("C4 — durée de vie ≥ 6 h\n(un saut)", contraintes[cles[5]], col["violet"]),
    ("C4' — durée de vie ≥ 30 ans", contraintes[cles[6]], col["violet"]),
    ("C5 — $r_s$ < rayon classique\nde l'électron (2,8 fm)", contraintes[cles[7]], col["ciel"]),
    ("C5' — $r_s$ < $10^{-18}$ m\n(borne expérimentale)", contraintes[cles[8]], col["ciel"]),
]
XMIN, XMAX = 1e-8, 1e16
for i, (nom, (a, b), c) in enumerate(lignes):
    y = len(lignes) - 1 - i
    a_, b_ = max(a, XMIN), min(b, XMAX)
    ax.barh(y, b_ - a_, left=a_, height=0.6, color=c, alpha=0.8, edgecolor="k", lw=0.6)
    borne = []
    if a > XMIN:
        borne.append(f"≥ {cc.sci(a, 2)} kg")
    if b < XMAX:
        borne.append(f"≤ {cc.sci(b, 2)} kg")
    ax.text(XMAX * 2, y, " ; ".join(borne), va="center", fontsize=8)
ax.set_yticks(range(len(lignes)))
ax.set_yticklabels([l[0] for l in lignes][::-1], fontsize=8.5)
ax.set_xscale("log")
ax.set_xlim(XMIN, XMAX)
i_bb = inter["sans_C1_photons_corps_noir (C2a∩C3∩C4'∩C5)"]
if i_bb:
    ax.axvspan(*i_bb, color=col["jaune"], alpha=0.6, zorder=0)
    ax.text(1e-7, -0.95, f"bande jaune : intersection C2a∩C3∩C4'∩C5 (sans C1) = {cc.sci(i_bb[0], 2)} à {cc.sci(i_bb[1], 2)} kg",
            ha="left", fontsize=8.5, bbox=dict(fc=col["jaune"], alpha=0.6, ec="none"))
ax.annotate("", xy=(M_UNITE / 2, len(lignes) - 0.45), xytext=(bandes_puissance["corps_noir"][0], len(lignes) - 0.45),
            arrowprops=dict(arrowstyle="<->", color="k", lw=1.5))
ax.text(np.sqrt(M_UNITE / 2 * bandes_puissance["corps_noir"][0]), len(lignes) - 0.3,
        f"écart C1 ↔ C2/C3 : ≈ {ecart_decades:.1f} ordres de grandeur — AUCUNE intersection".replace(".", ","),
        ha="center", fontsize=9.5, color=col["rouge"], weight="bold")
ax.set_ylim(-1.3, len(lignes) + 0.3)
ax.set_xlabel("masse M d'une singularité [kg]")
ax.grid(axis="y", visible=False)
cc.titre(fig, "S01 — Carte de contraintes : existe-t-il une masse M satisfaisant simultanément les revendications ?")
cc.sauver_figure(fig, FIG / "S01_fig4_carte_contraintes.png", rect=(0, 0.035, 0.88, 0.92))

# --- Figure 5 : carte (r, M) --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.8, 6.8))
r = np.logspace(-1, np.log10(5), 300)
Mg = np.logspace(0, 14, 400)
RR, MM = np.meshgrid(r, Mg)
acc_g = cc.G * MM / RR**2 / cc.G0
pc = ax.pcolormesh(RR, MM, np.log10(acc_g), cmap="viridis", shading="auto", vmin=-12, vmax=4)
cb = fig.colorbar(pc, ax=ax, pad=0.02)
cb.set_label(r"$\log_{10}(a/g_0)$, avec $a = GM/r^2$")
ax.fill_between(r, G_MIN * cc.G0 * r**2 / cc.G, G_MAX * cc.G0 * r**2 / cc.G, color="white", alpha=0.85,
                label="pesanteur comprise entre 1,5 g et 2 g")
r_b = np.linspace(D_MIN, D_MAX, 50)
ax.fill_between(r_b, G_MIN * cc.G0 * r_b**2 / cc.G, G_MAX * cc.G0 * r_b**2 / cc.G, color=col["vert"], alpha=0.95,
                label="… et distance entre 1 et 3 m (contrainte C3)")
ax.axvline(D_MIN, color="white", ls="--", lw=1)
ax.axvline(D_MAX, color="white", ls="--", lw=1)
ax.fill_between([r[0], r[-1]], *bandes_puissance["corps_noir"], color=col["orange"], alpha=0.75,
                label="P = 300–500 MW (photons, corps noir)")
ax.fill_between([r[0], r[-1]], *bandes_puissance["total_especes"], color=col["rouge"], alpha=0.75,
                label="P = 300–500 MW (toutes espèces)")
ax.axhline(M_UNITE / 2, color=col["ciel"], lw=2.5, label="C1 : M = 113 kg (demi-unité)")
ax.text(0.11, M_UNITE / 2 * 2.5, f"M = 113 kg  →  a(1 m) = {cc.sci(cc.G * M_UNITE / 2 / cc.G0, 2)} g", color="white", fontsize=9)
ax.axhline(M_taille["rayon classique de l'électron (2,82 fm)"], color=col["violet"], ls="--", lw=1.5,
           label="$r_s$ = rayon classique de l'électron")
ax.axhline(M_duree["trente ans de service"], color="white", ls=":", lw=1.5, label="durée de vie = 30 ans")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(r[0], r[-1])
ax.set_ylim(Mg[0], Mg[-1])
ax.set_xticks([0.1, 0.2, 0.5, 1, 2, 3, 5])
ax.set_xticklabels(["0,1", "0,2", "0,5", "1", "2", "3", "5"])
ax.minorticks_off()
ax.set_xlabel("distance r à la singularité [m]")
ax.set_ylabel("masse M [kg]")
ax.legend(loc="center left", bbox_to_anchor=(0.02, 0.36), fontsize=8, framealpha=0.9)
ax.grid(False)
cc.titre(fig, "S01 — Plan (distance, masse) : pesanteur produite, bande « 1,5–2 g entre 1 et 3 m » et bandes de puissance")
cc.sauver_figure(fig, FIG / "S01_fig5_plan_distance_masse.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Sauvegarde des résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S01_hawking",
    "avertissement": cc.MENTION,
    "constantes": {"G": cc.G, "c": cc.C, "hbar": cc.HBAR, "k_B": cc.K_B, "sigma_SB": cc.SIGMA_SB,
                   "M_Planck_kg": cc.M_PLANCK, "g0": cc.G0},
    "coefficients": {
        "r_s_par_kg_m": rayon_schwarzschild(1.0), "T_fois_M_K_kg": temperature_hawking(1.0),
        "P_fois_M2_corps_noir_W_kg2": puissance_corps_noir(1.0),
        "P_fois_M2_photons_page_W_kg2": puissance_photons_page(1.0),
        "P_fois_M2_total_f1_W_kg2": ALPHA_MACGIBBON * cc.C**2,
        "tau_sur_M3_corps_noir_s_kg3": duree_de_vie_corps_noir(1.0),
        "coef_adim_corps_noir": COEF_CORPS_NOIR, "coef_adim_page_photons": PAGE_SPIN_1,
        "coef_adim_macgibbon_f1": coef_macgibbon,
    },
    "masse_pour_300_500_MW_kg": {k: list(v) for k, v in bandes_puissance.items()},
    "rayon_s_pour_300_500_MW_m": {k: [rayon_schwarzschild(v[0]), rayon_schwarzschild(v[1])] for k, v in bandes_puissance.items()},
    "masse_pour_1p5_2g_entre_1_et_3m_kg": [M_g_min, M_g_max],
    "masse_min_pour_duree_kg": M_duree,
    "masse_pour_taille_electron_kg": M_taille,
    "masse_evaporation_age_univers_kg": M_etoile,
    "reperes": reperes,
    "flux_a_1m_W_m2": flux_1m.tolist(),
    "temperature_equilibre_corps_noir_a_1m_K": T_equilibre_1m.tolist(),
    "contraintes_kg": {k: list(v) for k, v in contraintes.items()},
    "intersections_kg": {k: (list(v) if v else None) for k, v in inter.items()},
    "ecart_decades_C1_vs_C2": ecart_decades,
    "evaporation": evap,
    "divergence_formulation_naive": divergence_naive,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S01_resultats.json", resultats)

# Table CSV T(M), P(M), τ(M)
Mt = np.logspace(0, 14, 57)
table = np.column_stack([Mt, rayon_schwarzschild(Mt), temperature_hawking(Mt), puissance_corps_noir(Mt),
                         puissance_photons_page(Mt), puissance_totale(Mt), facteur_especes(Mt),
                         duree_de_vie_corps_noir(Mt), [duree_de_vie_especes(m) for m in Mt]])
np.savetxt(RES / "S01_table_M.csv", table, delimiter=",", fmt="%.6e",
           header="M_kg,r_s_m,T_K,P_corps_noir_W,P_photons_Page_W,P_totale_W,f_especes,tau_corps_noir_s,tau_especes_s",
           comments="")
val.imprimer_bilan()
print("S01 terminé.")
