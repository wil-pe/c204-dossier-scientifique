#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-12 — Banc d'essai « C204 de substitution » : coffre instrumenté pour tester honnêtement,
en aveugle, les affirmations MESURABLES autour d'un dispositif CANDIDAT présenté par un promoteur.

Le banc ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible.

Version 2 (corrections post-validation n° 51 à 56 de la Red Team n° 2) :
  - masses retenues : 3,9–5,1e12 kg par singularité, soit 7,8e12–1,02e13 kg pour la paire (n° 51) ;
  - rayonnement en deux lectures : littérale (400 MW de X) et spectre de Hawking (γ primaires) (n° 52) ;
  - chaque voie porte son RÉGIME (permanent / pendant le fonctionnement / commutable), le CONTRASTE de mesure
    valide (dispositif − leurre ou mesure absolue ; marche − arrêt) et l'ORIGINE du signal (texte / déduit) (n° 53) ;
  - entraînement des référentiels : spin seul et paire en orbite (n° 54) ;
  - seuils donnés pour le protocole réellement décrit (64 cycles), résolutions N1 réalistes, dérive thermique
    des accéléromètres budgétée (n° 55) ;
  - surface du coffre à l'échelle révisée : 1,07 m² (n° 56).

Calcule :
  1. pour chaque voie : résolution (N1, N2), systématique, signal impliqué, marge signal/5σ, verdict possible ;
  2. le seuil de détection du protocole à 64 cycles (statistique ⊕ systématique) ;
  3. la fiabilité d'un vote majoritaire 2 parmi 3 ;
  4. la puissance statistique du protocole en aveugle (Monte-Carlo ILLUSTRATIF) ;
  5. le budget matériel indicatif.

Les « signaux impliqués » sont des implications chiffrées d'affirmations NON tenues pour vraies ; plusieurs sont
des déductions de l'institut (modèle de Hawking, seuils choisis), non des affirmations du texte : c'est indiqué.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

from constantes import (G, c, g0, C204, M_PAIRE, ENTRAXE_M, COFFRE, FRACTION_PHOTONS_HAWKING, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-12 — BANC D'ESSAI « C204 DE SUBSTITUTION » : SENSIBILITÉS, VOTE, PROTOCOLE AVEUGLE (version 2)")
L.append("=" * 72)
L.append("Le banc s'applique à un dispositif CANDIDAT. Il ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible.")
L.append("")

# ---------------------------------------------------------------- grandeurs dérivées
M_p_lo, M_p_hi = M_PAIRE                                   # 7,8e12 – 1,02e13 kg (la paire)
m_hi = C204["masse_TN_kg"][1]
P_lo, P_hi = C204["puissance_W"]
S_coffre = COFFRE["S"]
mu_en_100keV, mu_en_15MeV = 2.546e-3, 1.441e-3             # m²/kg (NIST, eau)
dose_A_3m = 400e6 / (4 * math.pi * 9) * mu_en_100keV       # lecture littérale : 400 MW de X de 100 keV
dose_B_3m = FRACTION_PHOTONS_HAWKING * 400e6 / (4 * math.pi * 9) * mu_en_15MeV   # γ primaires de Hawking (borne basse)
B_dipole_3m = 1.0 * (0.10 / 3.0)**3                        # [HYP] source de 1 T sur 10 cm de rayon, vue à 3 m
spin_max = 2 * G * (G * m_hi**2 / c) / c**2                # Kerr extrémal isolé de 5,1e12 kg, à 1 m
orbital_max = 2 * G * ((m_hi / 2) * math.sqrt(2 * G * m_hi * max(ENTRAXE_M))) / c**2   # paire en orbite, à 1 m

PERM = "permanent"                  # selon le récit, les singularités ne « s'éteignent » pas
FONC = "pendant le fonctionnement"  # revendiqué seulement pendant le déplacement
COMM = "commutable"
C_ABS = "dispositif − leurre, ou mesure absolue rapportée au fond"
C_MA = "marche − arrêt"

# voie, capteur, σ_N2, σ_N1, systématique N2, systématique N1, unité, signal, régime, contraste, origine, libellé du signal
VOIES = [
    ("Pesanteur ressentie « 1,5–2 g »", "accéléromètres", 2e-4, 2e-3, 1e-4, 5e-3, "m/s²",
     0.5 * g0, FONC, C_MA, "texte", "Δg ≥ 0,5 g pendant le trajet"),
    ("Pesanteur propre des singularités, à 1 m", "accéléromètres", 2e-4, 2e-3, 1e-4, 5e-3, "m/s²",
     G * M_p_lo, PERM, C_ABS, "déduit (modèle de Hawking)", "G·M/r² pour la paire (7,8e12 kg)"),
    ("Masse de l'appareil", "plateau de pesée", 0.1, 0.5, 0.0, 0.0, "kg",
     M_p_hi, PERM, "pesée absolue", "déduit (modèle de Hawking)", "7,8e12–1,02e13 kg pour la paire"),
    ("Marche d'une horloge « 10 ans/heure »", "horloge atomique ou quartz contre GPS", 1e-11, 1e-7, 0.0, 0.0, "(Δf/f)",
     C204["taux_temps"], FONC, C_MA, "texte", "dt_ext/dτ ≈ 87 660"),
    ("Décalage gravitationnel d'horloge réel", "idem", 1e-11, 1e-7, 0.0, 0.0, "(Δf/f)",
     G * M_p_hi / c**2, PERM, C_ABS, "déduit", "GM/(rc²) de la paire à 1 m"),
    ("Champ magnétique des bobines", "magnétomètres", 2e-8, 2e-7, 2e-8, 1e-7, "T",
     B_dipole_3m, COMM, C_MA, "déduit [HYP : 1 T sur 10 cm]", "le texte ne chiffre pas le champ"),
    ("Rayonnement — lecture littérale", "Geiger + scintillateur", 0.02e-6 / 3600, 0.05e-6 / 3600, 0.0, 0.0, "Sv/s",
     dose_A_3m, PERM, C_ABS, "texte, lecture littérale", "400 MW entièrement en X de 100 keV, à 3 m"),
    ("Rayonnement — spectre de Hawking", "Geiger + scintillateur", 0.02e-6 / 3600, 0.05e-6 / 3600, 0.0, 0.0, "Sv/s",
     dose_B_3m, PERM, C_ABS, "déduit (C, G ; borne basse)", "γ primaires (7,5 %), à 3 m"),
    ("Température de surface", "sondes + caméra thermique", 0.1, 0.2, 0.0, 0.0, "K",
     18.0, FONC, C_MA, "texte", "« 100–120 °F » : +18 à +29 K"),
    ("Puissance dissipée", "bilan thermique + wattmètre", 5.0, 20.0, 0.0, 0.0, "W",
     P_lo, PERM, "bilan thermique absolu", "texte", "« 300–500 MW »"),
    ("Faisceau laser « courbé »", "laser classe 2 + détecteur à 2 m", 5e-6, 2e-5, 5e-6, 2e-5, "rad",
     math.radians(1.0), FONC, C_MA, "texte/photo ; seuil choisi", "≥ 1° (≈ 55° apparents sur DOC-012)"),
    ("Déviation gravitationnelle réelle", "idem", 5e-6, 2e-5, 5e-6, 2e-5, "rad",
     4 * G * M_p_hi / c**2, PERM, C_ABS, "déduit", "4GM/(c²b), paire, b = 1 m"),
    ("Entraînement — spin seul", "gyromètre", 5e-6, 5e-5, 0.0, 0.0, "rad/s",
     spin_max, PERM, C_ABS, "déduit", "Kerr extrémal 5,1e12 kg, à 1 m"),
    ("Entraînement — paire en orbite", "gyromètre", 5e-6, 5e-5, 0.0, 0.0, "rad/s",
     orbital_max, PERM, C_ABS, "déduit (borne supérieure)", "2 × 5,1e12 kg, entraxe 0,30 m, à 1 m"),
]

def verdict_de(marge):
    if marge >= 10:
        return "réfutable en 1 cycle"
    if marge >= 1:
        return "réfutable (moyennage)"
    return "NON testable par ce banc"

L.append("1. Voies de mesure (σ par cycle de 100 s ; N2 : banc complet ; N1 : mini-banc)")
L.append(f"   {'voie':<44}{'σ N2':>9}{'σ N1':>9} {'unité':<7}{'signal':>10}{'sig/5σ N2':>11}{'sig/5σ N1':>11}  régime ; contraste valide ; origine")
D["voies"] = []
for voie, capteur, s2, s1, y2, y1, unite, signal, regime, contraste, origine, lib in VOIES:
    m2 = signal / (5 * math.hypot(s2, y2))
    m1 = signal / (5 * math.hypot(s1, y1))
    D["voies"].append({"voie": voie, "capteur": capteur, "sigma_N2": s2, "sigma_N1": s1, "sys_N2": y2, "sys_N1": y1,
                       "unite": unite, "signal": signal, "marge_N2": m2, "marge_N1": m1, "verdict_N2": verdict_de(m2),
                       "verdict_N1": verdict_de(m1), "regime": regime, "contraste": contraste, "origine": origine,
                       "libelle_signal": lib})
    L.append(f"   {voie:<44}{sci(s2,2):>9}{sci(s1,2):>9} {unite:<7}{sci(signal,2):>10}{m2:>11.1e}{m1:>11.1e}  "
             f"{regime} ; {contraste} ; {origine} — {lib}")
L.append("   (marge = signal / [5 × √(σ² + systématique²)] ; systématiques : dérive thermique des accéléromètres,")
L.append("    champ ambiant, turbulence de l'air sur le faisceau)")
L.append(f"   Masse : marge {M_p_lo/(5*0.1):.1e} à {M_p_hi/(5*0.1):.1e} (N2). Pesanteur propre de la paire à 1 m : "
         f"{G*M_p_lo:.0f}–{G*M_p_hi:.0f} m/s² ({G*M_p_lo/g0:.0f}–{G*M_p_hi/g0:.0f} g).")
L.append("   Lecture :")
L.append("   • grandeurs PERMANENTES selon le récit (masse, pesanteur propre, rayonnement, puissance des singularités, qui ne")
L.append("     « s'éteignent » pas) : une différence marche − arrêt nulle ne réfuterait RIEN ; le contraste valide est")
L.append("     dispositif − leurre, ou une mesure absolue (pesée, débit de dose au-dessus du fond, bilan thermique) ;")
L.append("   • grandeurs revendiquées PENDANT LE FONCTIONNEMENT (1,5–2 g, 10 ans/heure, lumière courbée, 38–49 °C) : contraste")
L.append("     marche − arrêt ; un banc extérieur ne les voit que si l'appareil reste dans le laboratoire pendant l'essai,")
L.append("     ce qui est déjà une réfutation d'un autre ordre ;")
L.append("   • effets relativistes RÉELS des masses retenues (décalage 6–8e-15, déviation 2–3e-14 rad, entraînement 9e-21 à")
L.append("     5e-14 rad/s) : hors de portée ; le banc ne teste pas la relativité générale, il teste des affirmations d'ingénierie ;")
L.append("   • plusieurs « signaux » sont des implications déduites par l'institut (modèle de Hawking pour la masse et la dose,")
L.append("     seuil de 1° pour la lumière, 1 T pour les bobines), non des affirmations du texte : colonne « origine ».")
L.append("")

# ---------------------------------------------------------------- 2. seuils du protocole réellement décrit (64 cycles)
K = 11                                               # comparaisons planifiées (z varie de 5,40 à 5,47 pour K = 9 à 13)
alpha_global = stats.norm.sf(5.0)                    # 5σ unilatéral
z_voie = stats.norm.isf(alpha_global / K)            # correction de Bonferroni
N_CYCLES = 64
sd_N = math.sqrt(1 / (N_CYCLES / 2) + 1 / (N_CYCLES / 2))      # écart-type de la différence des moyennes, en unités de σ
L.append(f"2. Seuils de détection pour le protocole décrit : {N_CYCLES} cycles de 100 s, état tiré au sort (≈ 32 / 32)")
L.append(f"   seuil global 5σ (p = {alpha_global:.1e}) réparti sur {K} comparaisons (Bonferroni) → z = {z_voie:.2f} par comparaison")
L.append(f"   (z = {stats.norm.isf(alpha_global/9):.2f} pour 9 comparaisons, {stats.norm.isf(alpha_global/13):.2f} pour 13 : sans conséquence)")
L.append(f"   seuil statistique = {z_voie:.2f} × {sd_N:.2f}σ = {z_voie*sd_N:.2f}σ par cycle ; borne supérieure à 95 % en cas de résultat nul : {1.645*sd_N:.2f}σ")
L.append("   seuil total = √[(seuil statistique)² + (3 × systématique)²]  — la systématique ne se moyenne pas")
L.append(f"   {'voie':<44}{'seuil N2':>11}{'seuil N1':>11}  unité")
D["seuils_64"] = {}
for v in D["voies"]:
    if v["voie"] in ("Décalage gravitationnel d'horloge réel", "Déviation gravitationnelle réelle", "Entraînement — paire en orbite",
                     "Rayonnement — spectre de Hawking", "Pesanteur propre des singularités, à 1 m"):
        continue                                     # même capteur qu'une voie déjà listée
    t2 = math.hypot(z_voie * sd_N * v["sigma_N2"], 3 * v["sys_N2"])
    t1 = math.hypot(z_voie * sd_N * v["sigma_N1"], 3 * v["sys_N1"])
    D["seuils_64"][v["capteur"]] = {"N2": t2, "N1": t1, "unite": v["unite"]}
    L.append(f"   {v['capteur']:<44}{sci(t2,2):>11}{sci(t1,2):>11}  {v['unite']}")
seuil_g_N2 = D["seuils_64"]["accéléromètres"]["N2"]
seuil_g_N1 = D["seuils_64"]["accéléromètres"]["N1"]
seuil_gravi = math.hypot(z_voie * sd_N * 5e-8, 3 * 3e-8)       # gravimètre 5 µGal ; systématique 3 µGal (1 cm de hauteur)
L.append("   Dérive thermique des accéléromètres (budget) : coefficient ≈ 1e-3 m/s² par K (MEMS bas bruit), 1e-2 m/s² par K")
L.append("   (téléphone) ; écart de température résiduel entre les deux états, après écran thermique et régression sur la")
L.append("   température mesurée : 0,1 K (N2), 0,5 K (N1) → systématiques 1e-4 et 5e-3 m/s². Le LEURRE doit dissiper la même")
L.append("   puissance que le dispositif, sinon l'échauffement mime un signal corrélé à la clé.")
L.append(f"   → masse cachée exclue à 1 m (contraste dispositif − leurre) : > {sci(seuil_g_N2/G)} kg (N2) ; > {sci(seuil_g_N1/G)} kg (N1) ;")
L.append(f"     avec un gravimètre de terrain (5 µGal ; systématique de hauteur 3 µGal) : > {seuil_gravi/G:.0f} kg.")
D["masse_exclue_kg"] = {"N2": seuil_g_N2 / G, "N1": seuil_g_N1 / G, "gravimetre": seuil_gravi / G}
D["protocole_64"] = {"K": K, "z": z_voie, "seuil_sigma": z_voie * sd_N, "borne95_sigma": 1.645 * sd_N}
L.append("   (La version 1 donnait des seuils « à 5σ en 100 cycles » calculés pour 100 PAIRES marche/arrêt, soit une durée")
L.append("    triple de celle du protocole : ces chiffres sont retirés.)")
L.append("")

# ---------------------------------------------------------------- 3. vote majoritaire
L.append("3. Enregistrement à trois voies redondantes, vote majoritaire (2 parmi 3)")
L.append("   probabilité qu'une donnée votée soit fausse, pour des pannes INDÉPENDANTES de probabilité p par voie :")
L.append("   P = 3p²(1-p) + p³")
D["vote"] = []
for p in (1e-1, 1e-2, 1e-3, 1e-4):
    P = 3 * p**2 * (1 - p) + p**3
    D["vote"].append({"p": p, "P_vote": P, "gain": p / P})
    L.append(f"     p = {p:.0e} → P = {P:.2e}  (gain ×{p/P:.0f})")
beta = 0.02
L.append(f"   Si une fraction β = {beta:.0%} des pannes est de MODE COMMUN (alimentation, parasite électromagnétique de l'appareil")
L.append("   testé, erreur logicielle partagée), P ≈ β·p + 3[(1-β)p]² : le mode commun domine dès que p < β/3.")
for p in (1e-2, 1e-3):
    P = beta * p + 3 * ((1 - beta) * p)**2
    L.append(f"     p = {p:.0e} → P ≈ {P:.2e}")
L.append("   → d'où : trois enregistreurs de conception DIFFÉRENTE, alimentations séparées, isolation optique, horodatage")
L.append("     par 1PPS GPS, et pour les grandeurs continues la MÉDIANE des trois voies plutôt qu'un vote binaire.")
L.append("   Remarque : la méthode de Borda est une règle de vote par classement (théorie du choix social), non un")
L.append("   protocole de tolérance aux pannes ; avec 3 votants et 2 options elle se réduit au vote majoritaire. Le")
L.append("   « protocole de Borda » des calculateurs revendiqués n'a pas d'équivalent identifié en sûreté de fonctionnement.")
L.append("")

# ---------------------------------------------------------------- 4. puissance statistique
L.append("4. Puissance statistique du protocole en aveugle (état A/B tiré au sort par un tiers, clé scellée)")
rng = np.random.default_rng(12)
def simulation(effet_en_sigma, N, n_essais=4000):
    """Proportion d'essais où la différence moyenne entre les deux états dépasse le seuil par comparaison."""
    etat = rng.integers(0, 2, size=(n_essais, N)).astype(bool)
    y = rng.normal(0, 1, size=(n_essais, N)) + effet_en_sigma * etat
    n_on = etat.sum(axis=1)
    n_off = N - n_on
    ok = (n_on > 1) & (n_off > 1)
    m_on = np.where(etat, y, 0).sum(axis=1)[ok] / n_on[ok]
    m_off = np.where(~etat, y, 0).sum(axis=1)[ok] / n_off[ok]
    z = (m_on - m_off) / np.sqrt(1 / n_on[ok] + 1 / n_off[ok])
    return float(np.mean(z > z_voie))
L.append("   probabilité de détecter — Monte-Carlo ILLUSTRATIF, bruit gaussien unité par cycle, sans systématique :")
L.append(f"   {'effet (en σ par cycle)':>24} | " + " | ".join(f"N = {N:>3}" for N in (16, 32, 64, 128)))
D["puissance"] = {}
for eff in (0.0, 0.5, 1.0, 2.0, 5.0):
    ligne = f"   {eff:>24.1f} | "
    D["puissance"][str(eff)] = {}
    for N in (16, 32, 64, 128):
        pw = simulation(eff, N)
        D["puissance"][str(eff)][str(N)] = pw
        ligne += f"{pw:>7.3f} | "
    L.append(ligne)
L.append("   (ligne « effet 0 » = taux de fausses alarmes : nul à la précision de la simulation)")
L.append(f"   Avec {N_CYCLES} cycles de 100 s (≈ 1,8 h ; 3,6 h avec les temps morts), un effet ≥ 2σ par cycle est détecté à > 99 %.")
L.append("   Les deux contrastes (marche/arrêt ; dispositif/leurre) demandent chacun leur série de 64 cycles : pour le second,")
L.append("   c'est le chariot de capteurs qui alterne entre deux postes symétriques (dispositif / leurre), pas l'appareil.")
L.append("")

# ---------------------------------------------------------------- 5. bilan thermique à l'échelle révisée et budget
h_conv = 10.0
P_coffre = [h_conv * S_coffre * (Tc - 20) for Tc in C204["temperature_C"]]
L.append(f"5. Bilan thermique : coffre à l'échelle révisée (L = 0,85 m, S = {S_coffre:.2f} m²) à 38–49 °C dans de l'air à 20 °C :")
L.append(f"   h·S·ΔT = {P_coffre[0]:.0f}–{P_coffre[1]:.0f} W, à comparer aux {P_lo/1e6:.0f}–{P_hi/1e6:.0f} MW revendiqués (rapport {P_lo/P_coffre[1]:.0e} à {P_hi/P_coffre[0]:.0e}).")
D["thermique"] = {"S_coffre_m2": S_coffre, "puissance_coffre_W": P_coffre}
L.append("")

BUDGET = {
    "N1 — mini-banc (≤ 500 €)": [
        ("smartphone avec phyphox (accéléromètre, magnétomètre, gyromètre) — déjà possédé", 0),
        ("compteur Geiger du commerce avec sortie de données", 110),
        ("2 accéléromètres MEMS bas bruit + microcontrôleurs enregistreurs", 120),
        ("6 sondes de température numériques + enregistreur", 45),
        ("module GPS avec sortie 1PPS (horodatage commun)", 35),
        ("pointeur laser classe 2 + webcam (position du faisceau)", 40),
        ("pèse-personne ×4 ou plateau de pesée d'occasion", 80),
        ("batteries, câbles, boîtier", 60),
    ],
    "N2 — banc complet de salle de TP": [
        ("3 chaînes d'acquisition indépendantes (3 conceptions différentes) + stockage", 600),
        ("3 accéléromètres triaxiaux bas bruit + 1 sismomètre/géophone", 700),
        ("GPSDO + rubidium d'occasion + compteur d'intervalles de temps", 900),
        ("horloge atomique miniature (CSAC), optionnelle", 4000),
        ("3 magnétomètres (dont 1 fluxgate triaxial)", 900),
        ("2 Geiger de tubes différents + spectromètre à scintillation", 900),
        ("12 sondes Pt100/thermistances + caméra thermique d'entrée de gamme", 700),
        ("plateau de pesée 600 kg / 0,1 kg étalonné", 350),
        ("laser classe 2 + détecteur de position", 250),
        ("gyromètre à fibre de TP ou MEMS tactique", 1500),
        ("coffre, blindage CEM, isolations optiques, alimentations séparées", 1200),
    ],
    "N3 — version laboratoire (compléments)": [
        ("gravimètre relatif de terrain (achat ; ou prêt d'un laboratoire de géophysique)", 100000),
        ("étalon à césium ou accès à un maser + lien de temps étalonné", 60000),
        ("spectromètre gamma HPGe et chambre d'ionisation", 50000),
        ("magnétomètre à pompage optique", 20000),
    ],
}
def milliers(n):
    return f"{n:,}".replace(",", " ")

L.append("6. Budget matériel indicatif (ordres de grandeur 2026, hors main-d'œuvre ; prix à confirmer)")
D["budget"] = {}
for version, postes in BUDGET.items():
    tot = sum(p for _, p in postes)
    D["budget"][version] = {"total": tot, "postes": postes}
    L.append(f"   {version} : total ≈ {milliers(tot)} €")
    for nom, prix in postes:
        L.append(f"       {milliers(prix):>7} €  {nom}")
L.append("")
L.append("Critères de réfutation (fixés AVANT les essais), pour un dispositif candidat :")
L.append("  • grandeur commutable ou revendiquée pendant le fonctionnement : différence marche − arrêt ;")
L.append("  • grandeur permanente selon le récit (masse, pesanteur propre, rayonnement et puissance des singularités) :")
L.append("    différence dispositif − leurre, ou mesure absolue rapportée au fond ;")
L.append("  • l'implication est réfutée si la différence (ou l'écart au fond) est compatible avec zéro ET que sa borne")
L.append("    supérieure à 95 % est inférieure d'au moins un facteur 100 au signal impliqué ;")
L.append("  • une « détection » n'est retenue que si elle dépasse le seuil corrigé sur ≥ 2 capteurs de conception différente,")
L.append("    suit la clé aléatoire, disparaît avec le leurre et survit à l'échange des capteurs. Même alors, elle établirait")
L.append("    une anomalie instrumentale à expliquer, PAS un voyage dans le temps.")
L.append("Ce que l'on réfute ainsi, ce sont des conséquences chiffrées — certaines déduites par l'institut — pour l'appareil")
L.append("présenté ; rien n'est établi sur l'objet de 2000-2001.")

sauver("calc12_banc_essai", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.0))
ax = axes[0]
noms = [v["voie"] for v in D["voies"]]
m2 = np.array([v["marge_N2"] for v in D["voies"]])
m1 = np.array([v["marge_N1"] for v in D["voies"]])
ypos = np.arange(len(noms))
coul = ["#2e8b57" if m >= 1 else "#d1495b" for m in m2]
ax.barh(ypos - 0.2, m2, height=0.38, color=coul, label="banc N2")
ax.barh(ypos + 0.2, m1, height=0.38, color=coul, alpha=0.45, label="mini-banc N1")
ax.set_xscale("log")
ax.set_yticks(ypos)
ax.set_yticklabels([f"{n}\n[{v['regime']}]" for n, v in zip(noms, D["voies"])], fontsize=6.6)
ax.invert_yaxis()
ax.axvline(1, color="k", lw=1)
ax.set_xlabel("signal impliqué / (5 × résolution par cycle de 100 s)")
ax.set_title("Marge de réfutation par voie (vert : testable ; rouge : hors de portée)\n"
             "régime entre crochets : il fixe le contraste de mesure valide", fontsize=9.5)
ax.legend(fontsize=8, loc="lower right")
ax.grid(True, which="both", axis="x", alpha=0.25)

ax = axes[1]
effets = np.linspace(0, 3, 13)
for N, col in ((16, "#f6ae2d"), (64, "#33658a"), (128, "#2e8b57")):
    ax.plot(effets, [simulation(e, N, 2000) for e in effets], "o-", color=col, label=f"N = {N} cycles")
ax.axvline(z_voie * sd_N, color="#33658a", ls=":", lw=1)
ax.text(z_voie * sd_N + 0.04, 0.05, f"seuil à 64 cycles\n{z_voie*sd_N:.2f}σ", fontsize=8, color="#33658a")
ax.set_xlabel("effet réel (en écarts-types par cycle)")
ax.set_ylabel("probabilité de détection au seuil corrigé")
ax.set_title("Puissance du protocole en aveugle\n(Monte-Carlo illustratif, bruit gaussien, sans systématique)", fontsize=9.5)
ax.legend(fontsize=8)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc12_banc_essai.png"), dpi=150)
print("figure :", fig_chemin("calc12_banc_essai.png"))
