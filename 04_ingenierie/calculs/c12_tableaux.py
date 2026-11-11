# -*- coding: utf-8 -*-
"""C204 — Équipe C. Construit les deux tableaux de synthèse à partir des résultats c01-c10 :
  ../tableau_faisabilite.csv          (composant par composant : Q8 et Q9)
  ../tableau_exigences_ecarts.csv     (exigence revendiquée <-> meilleure technologie réelle <-> écart en décades)
"""
import csv
import os
from math import log10
import c00_constantes as K

C1 = K.charger_json("c01_hawking.json")
C2 = K.charger_json("c02_confinement.json")
C3 = K.charger_json("c03_injection_rotation.json")
C5 = K.charger_json("c05_refroidissement.json")
C6 = K.charger_json("c06_alimentation.json")
C7 = K.charger_json("c07_capteurs_horloges.json")
C9 = K.charger_json("c09_structure.json")
C10 = K.charger_json("c10_Q4.json")
RACINE = os.path.dirname(K.ICI)

m44 = [x for x in C2["par_masse"] if abs(x["M_kg"] - 4.4e12) < 1][0]
i44 = [x for x in C3["injection_par_masse"] if abs(x["M_kg"] - 4.4e12) < 1][0]
B_req = C2["penning"]["B_min_extremal_T"]
E_lev = C2["E_sustentation_extremal_V_par_m"]
Q_ref = C5["charges_thermiques_W"]["réf. x2 : 2 singularités, 400 MW chacune (dépôt γ + e±)"]
bl = C5["blindage_requis_a_1m"]["1 mSv sur le trajet (limite annuelle du public)"]
dose1 = C5["doses_sans_blindage"][0]["debit_dose_photons_primaires_Gy_s"]
flux5 = C5["flux_parietal_reference"]["flux_W_m2"]          # carter au rayon documentaire (Équipe A)
P49 = C5["puissance_coffre_a_T_revendiquee_W"]["49 °C"]
eau6h = [d for d in C5["debits"] if d["charge"].startswith("réf. x2") and "vaporisée" in d["fluide"]][0]
pompe = [d for d in C5["debits"] if d["charge"].startswith("réf. x2") and d["fluide"].startswith("eau liquide")][0]
E_crea = C6["creation_scenario_A_J"]
cap = C7["capteur_dans_le_champ"]["2,94e11 kg (2 g à 1 m), capteur à 0.3 m"]
blog = C5["blindage_logeable"]
bproche = C5["blindage_logeable_par_direction"]["profondeur, vers la face la plus proche (DOC-007)"]
vmv = C9["verdict_masse_volume"]
q5071 = C7["quatre_5071A"]
P38 = C5["puissance_coffre_a_T_revendiquee_W"]["38 °C"]
E_2g = C6["creation_2g_J"]


def fr(x, n=2):
    """Nombre en notation française à n chiffres significatifs."""
    return f"{x:.{n}g}".replace(".", ",")


RC, DP = fr(K.R_CARTER * 100, 3), fr(K.D_PAIRE * 100, 3)      # cm
M_RES = 2 * K.V_RESERVOIR_SCHEMA * 990.0                      # kg d'eau dans les deux réservoirs à l'échelle du schéma
ep_etroit = bl["faisceau_etroit"]["15 MeV"]

# ----------------------------------------------------------------------------- tableau des écarts
ecarts = []


def ecart(ss, exigence, val_req, unite, techno, val_reel, ref, note="", petit_est_mieux=False):
    """Écart en décades entre l'exigence et le réel. petit_est_mieux=True pour une résolution ou une tolérance
    (l'exigence est alors une valeur maximale admissible)."""
    d = log10(val_reel / val_req) if petit_est_mieux else log10(val_req / val_reel)
    ecarts.append(dict(sous_systeme=ss, exigence_revendiquee_ou_deduite=exigence, valeur_requise=f"{val_req:.3g}",
                       unite=unite, meilleure_technologie_reelle=techno, valeur_reelle=f"{val_reel:.3g}",
                       ecart_en_ordres_de_grandeur=f"{d:+.1f}",
                       verdict=("satisfait" if d <= 0 else ("accessible avec effort" if d < 1 else
                                ("hors de portée" if d < 6 else "hors de portée, sans voie connue"))),
                       reference=ref, remarque=note))


ecart("1 confinement", "champ magnétique d'un piège de Penning tenant la pesanteur (charge extrémale, excursion 1 cm)",
      B_req, "T", "champ continu record (insert HTS, NHMFL 2019)", 45.5, "Hahn et al. 2019",
      "indépendant de M ; la charge extrémale est elle-même intenable")
ecart("1 confinement", "idem avec la charge réaliste (6 e, Page 1977), M = 4,4e12 kg",
      m44["B_Penning_charge_6e_T"], "T", "champ continu record", 45.5, "Hahn et al. 2019 ; Page 1977")
ecart("1 confinement", "champ continu soutenable par un matériau (σ = 130 GPa)", B_req, "T",
      "limite B = sqrt(2 μ0 σ)", C2["B_max_materiau_T"]["sigma = 130 GPa"], "calcul c02",
      "limite de la liaison chimique, pas seulement technologique")
ecart("1 confinement", "champ électrique de sustentation (charge extrémale)", E_lev, "V/m",
      "gradient accélérateur RF bande X (CLIC)", 1e8, "CLIC CDR", "indépendant de M")
ecart("1 confinement", "idem, comparé au champ d'évaporation du tungstène", E_lev, "V/m",
      "évaporation par effet de champ (57 V/nm)", 5.7e10, "Seidman 2007", "les électrodes s'évaporent")
ecart("1 confinement", "gradient magnétique sur le dipôle maximal (M = 4,4e12 kg)", m44["gradient_B_requis_T_par_m"],
      "T/m", "pointes micromagnétiques [HYP]", 1e6, "ordre de grandeur")
ecart("1 confinement", "force de sustentation, M = 4,4e12 kg", m44["poids_N"], "N",
      "charge utile d'un pick-up (1500 kg) [HYP]", 1500 * K.g0, "—")
ecart("1 confinement", f"pression de réaction sur un carter de {RC} cm de rayon (M = 4,4e12 kg)",
      m44["pression_reaction_carter_Pa"], "Pa", "acier à haute résistance", 2e9, "ordre de grandeur")
ecart("1 confinement", f"force séparant deux singularités de 4,4e12 kg à {DP} cm (entraxe de DOC-007, Équipe A)",
      m44["attraction_mutuelle_N"], "N", "poids d'une des singularités", m44["poids_N"], "calcul c02",
      f"elles orbiteraient en {fr(m44['periode_orbitale_mutuelle_s'] * 1e3)} ms")
ecart("2 injection", "charge à injecter pour +1 % de masse (M = 4,4e12 kg)", i44["charge_correspondante_C"], "C",
      "photo-injecteur record 65 mA pendant 6 h", 0.065 * K.DUREE_TRAJET, "Dunham et al. 2013")
ecart("2 injection", "énergie par électron pour atteindre l'horizon d'un trou noir extrémal",
      C3["energie_electron_pour_franchir_barriere_extremale_eV"], "eV", "LHC, par proton", 6.8e12, "CERN")
ecart("2 injection", "probabilité de capture requise ≈ 1 (tache de 1 µm², M = 4,4e12 kg)", 1.0, "—",
      "σ_capture / aire de la tache", i44["fraction_capturee[microfaisceau 1 µm²]"], "calcul c03")
ecart("3 rotation", "vitesse de réorientation de l'axe ~1 rad/s [HYP]", 1.0, "rad/s",
      "précession magnétique à 45,5 T (charge extrémale)", C3["rotation"][0]["precession_45p5T_charge_extremale_rad_s"],
      "calcul c03")
ecart("4 refroidissement", "puissance thermique à évacuer du coffre (2 x 400 MW, dépôt γ + e±)", Q_ref, "W",
      f"coffre de {fr(K.COFFRE_S, 3)} m² à 49 °C (convection naturelle + rayonnement)", P49, "calcul c05",
      f"la température revendiquée correspond à {fr(P38 / 1e3)}-{fr(P49 / 1e3)} kW")
ecart("4 refroidissement", "densité de puissance volumique du coffre", Q_ref / K.COFFRE_V / 1e9, "MW/L",
      "cœur du réacteur HFIR (cœur seul, hors circuits)", 1.7, "Chandler et al. 2018")
ecart("4 refroidissement", f"flux pariétal sur un carter de {RC} cm de rayon", flux5, "W/m²",
      "flux critique record en eau sous-refroidie", 276e6, "Mudawar & Bowers 1999")
ecart("4 refroidissement", "eau vaporisée sur 6 h (circuit ouvert)", eau6h["masse_pour_6h_circuit_ouvert_kg"], "kg",
      "deux réservoirs de 0,25 L (échelle du schéma, Équipes E et I)", M_RES, "DOC-008",
      "avec l'ancienne hypothèse de 2 x 15 L (86 % du volume utile) : écart réduit de 1,8 décade")
ecart("4 refroidissement", "puissance de pompage (eau, ΔT = 50 K)", pompe["puissance_pompe_W"], "W",
      "pack Li-ion 50 kg en régime soutenu [HYP]", 25e3, "calcul c05/c06")
ecart("4 rayonnement", "débit de dose γ à 1 m sans blindage, rapporté à 1 mSv par trajet de 6 h", dose1, "Gy/s",
      "limite annuelle du public répartie sur 6 h", 1e-3 / K.DUREE_TRAJET, "CIPR 103")
ecart("4 rayonnement", "atténuation requise du blindage", bl["facteur_attenuation"], "—",
      f"atténuation de {fr(blog['epaisseur_plomb_m'] * 100)} cm de plomb (logeable, cas favorable)",
      blog["attenuation"], "NCRP 151",
      f"vers la face la plus proche : {fr(bproche['epaisseur_plomb_m'] * 100)} cm seulement")
ecart("4 rayonnement", "masse du blindage sphérique en plomb (couche de déci-transmission en faisceau large)",
      bl["masse_sphere_plomb_kg"], "kg", "masse totale de l'unité", K.MASSE_UNITE, "calcul c05",
      f"faisceau étroit à 15 MeV : {fr(ep_etroit['epaisseur_plomb_m'] * 100)} cm, {fr(ep_etroit['masse_sphere_plomb_kg'] / 1e3)} t")
ecart("5 alimentation", "auxiliaires en configuration logeable (CSAC, 3 calculateurs, CG-6, pupitre), 6 h",
      C6["auxiliaires_configuration_logeable"]["energie_6h_kWh"], "kWh", "pack LiFePO4 logeable (4 L, 9,5 kg)", 1.34,
      "calcul c06 ; Équipe I", "réaliste et logeable")
ecart("8 structure", "volume des périphériques dimensionnés sans contrainte de place",
      vmv["volume_configuration_genereuse_L"], "L", "volume intérieur utile du coffre (Équipes E et I)",
      vmv["volume_utile_L"], "calcul c09", "la masse (%.0f kg) passe, le volume non" % vmv["masse_configuration_genereuse_kg"])
ecart("8 structure", "masse volumique moyenne exigée par 227 kg dans l'enveloppe du coffre",
      vmv["masse_volumique_requise_dans_l_enveloppe_kg_m3"], "kg/m³",
      "masse volumique de la configuration logeable (Équipe I, R1)",
      vmv["masse_volumique_configuration_logeable_kg_m3"], "calcul c09", "il manque ~190 kg de matière dense")
ecart("4 rayonnement", "fraction du rayonnement canalisée dans un cône de 30° (revendiqué : ~100 %)", 1.0, "—",
      "fraction géométrique d'une émission isotrope", C5["cone_collimation"]["demi-angle 30°"]["fraction_angle_solide"],
      "calcul c05")
ecart("5 alimentation", "auxiliaires (horloges, calculateurs, capteurs, canon), hypothèse haute, 6 h",
      C6["auxiliaires_W"]["energie_6h_kWh_max"], "kWh", "pack Li-ion 50 kg", 7.5, "calcul c06", "réaliste")
ecart("5 alimentation", "énergie de création des deux singularités (2 x 4,4e12 kg)", E_crea, "J",
      "production mondiale d'électricité en un an (2023)", 29925 * K.TWh, "Energy Institute 2024")
ecart("5 alimentation", "idem, rapportée à la batterie", E_crea, "J", "pack Li-ion 50 kg", 7.5 * K.kWh, "calcul c06")
ecart("5 alimentation", "énergie de création de deux singularités donnant 2 g à 1 m à elles deux (2 x 1,47e11 kg)",
      E_2g, "J", "production mondiale d'électricité en un an (2023)", 29925 * K.TWh, "Energy Institute 2024",
      "égale à l'énergie de la question Q4")
ecart("5 alimentation", "énergie par collision pour former un trou noir (masse de Planck, 4 dimensions)",
      C6["croissance"]["energie_de_Planck_GeV"], "GeV", "LHC (13,6 TeV)", 13600.0, "CERN")
ecart("6 capteurs", "résolution pour détecter un bloc de 1 m³ à 2 m — instrument seul, au repos", 4.0, "µGal",
      "écart-type Scintrex CG-6", 5.0, "fiche constructeur", "réaliste au repos, à 1 g, sous 45 °C",
      petit_est_mieux=True)
ecart("6 capteurs", "stabilité de position capteur/singularité pour résoudre 1 µGal (2 g à 1 m, capteur à 0,3 m)",
      cap["stabilite_de_position_requise_m"], "m", "dilatation de 0,3 m d'aluminium pour 1 K",
      cap["dilatation_aluminium_par_K_m"], "calcul c07", petit_est_mieux=True)
ecart("6 horloges", "exactitude relative pour dater à 1 jour près sur 60 ans",
      C7["erreur_temps"]["précision relative pour viser un jour donné à 60 ans"], "—",
      "étalon à jet de césium 5071A", 5e-13, "Microchip 5071A",
      "un quartz suffirait : l'exigence est satisfaite avec 8 décades de marge", petit_est_mieux=True)
ecart("6 horloges", "exactitude pour résoudre le potentiel des singularités (à 10 cm de 4,4e12 kg)",
      C7["decalage_gravitationnel_relatif"]["4,4e12 kg, r = 0.1 m"], "—",
      "étalon à jet de césium 5071A", 5e-13, "Microchip 5071A",
      "les horloges au césium ne « voient » pas le champ", petit_est_mieux=True)
ecart("8 structure", "pression sous les pneus (2 x 4,4e12 kg)", C9["charge_vehicule_et_sol"][3]["pression_sous_les_pneus_Pa"],
      "Pa", "résistance en compression du granite", 200e6, "ordre de grandeur")
ecart("9 Q4", "énergie électromagnétique pour 2 g à 1 m", C10["energie_requise_J"], "J",
      "énergie magnétique totale d'ITER (51 GJ)", 51e9, "ITER")
ecart("9 Q4", "idem, rapportée à un an de production électrique mondiale", C10["energie_requise_J"], "J",
      "production mondiale 2023", 29925 * K.TWh, "Energy Institute 2024")

ecarts.sort(key=lambda e_: e_["sous_systeme"][0])      # tri stable par numéro de sous-système
with open(os.path.join(RACINE, "tableau_exigences_ecarts.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ecarts[0].keys()))
    w.writeheader()
    w.writerows(ecarts)

# ----------------------------------------------------------------------------- tableau de faisabilité
COL = ["repere", "composant", "fonction_revendiquee", "exigence_chiffree", "meilleure_technologie_reelle",
       "ecart_ordres_de_grandeur", "statut_physique", "constructible_aujourd_hui", "fondamentalement_impossible",
       "justification", "comment_le_construire", "confiance"]
T = []


def comp(*vals):
    T.append(dict(zip(COL, vals)))


comp("DOC-007 r.1-2 ; DOC-008 r.1", "Deux micro-singularités (trous noirs)", "source d'énergie et de gravité",
     "300-500 MW chacune ⇒ 3,9 à 5,1e12 kg ; 2 g à 1 m ⇒ 2,9e11 kg ; unité de 227 kg",
     "aucune : aucun trou noir n'a jamais été produit ni détecté en laboratoire (LHC : exclusion jusqu'à ~10 TeV dans les modèles à dimensions supplémentaires)",
     f"{log10(E_crea / (29925 * K.TWh)):+.1f} (énergie de création / production électrique mondiale annuelle)",
     "Contredit (dans l'enveloppe revendiquée) ; trou noir primordial de 1e12 kg : Spéculatif",
     "non", "oui",
     "Aucune masse ne satisfait à la fois transportabilité, puissance, pesanteur et durée de vie (c09) ; 100 kg s'évaporent en 4e-13 s en libérant 9e18 J ; un trou noir de moins de ~1e11 kg ne peut pas être alimenté plus vite qu'il ne s'évapore (c06)",
     "—", "élevée")
comp("DOC-008 r.1", "Carter de singularité (enceinte sous vide)", "loger la singularité",
     f"enceinte sphérique de ~{fr(2 * K.R_CARTER * 100)} cm (logement de DOC-007), vide poussé", "enceintes ultravide courantes (1e-9 Pa)", "0 (enceinte seule)",
     "Démontré (l'enceinte) ; Contredit (tenir 4e13 N)", "oui (l'enceinte vide)", "oui pour la fonction de supportage",
     f"réaction du poids sur {RC} cm de rayon : {m44['pression_reaction_carter_Pa']:.1e} Pa, soit 6 à 7 décades au-delà de tout matériau",
     "sphère inox ou aluminium, brides CF, pompage ionique", "élevée")
comp("DOC-008 r.2", "Bobines de champ magnétique", "confiner et positionner la singularité",
     f"{B_req:.1e} T (piège de Penning, charge extrémale) ; aucun couplage si le trou noir est neutre",
     "45,5 T continu ; 100,75 T pulsé non destructif ; 1200 T destructif",
     f"{log10(B_req / 45.5):+.1f}", "Contredit", "oui (bobines de 1 à 20 T)", "oui pour la fonction",
     "q/m ≤ 8,6e-11 C/kg ; charge réelle limitée à quelques e (Page 1977) ; théorème d'Earnshaw ; limite des matériaux ~570 T",
     "solénoïdes HTS (REBCO) refroidis par cryoréfrigérateur, 5 à 20 T dans quelques cm", "élevée")
comp("DOC-008 r.3", "Générateur / régulateur de champ", "alimenter et réguler les bobines",
     "courant stabilisé ; dizaines de MW pour un aimant résistif de 45 T", "alimentations d'aimants ppm, mode persistant",
     "0 (pour des bobines réelles)", "Démontré", "oui", "non",
     "technologie standard ; seule la puissance (MW) est incompatible avec une batterie",
     "alimentation à découpage + commutateur de persistance", "élevée")
comp("DOC-008 r.4", "Collecteur d'injection d'électrons (« electron mass injector manifold »)",
     "modifier la masse et la gravité des singularités",
     f"+1 % de masse = {i44['electrons_pour_1pc_de_masse']:.1e} électrons = {i44['charge_correspondante_C']:.1e} C",
     "65 mA moyen (photo-injecteur) ; faisceaux focalisés à 41 nm (ATF2)",
     f"{log10(i44['charge_correspondante_C'] / (0.065 * K.DUREE_TRAJET)):+.1f}", "Contredit",
     "oui (une ligne de faisceau sous vide)", "oui pour la fonction",
     f"la charge maximale est atteinte pour ΔM/M = {C3['delta_M_sur_M_a_charge_extremale_par_electrons']:.1e} ; barrière jusqu'à 1e27 eV ; un seul électron en excès suffit à repousser le suivant plus fort que la gravité ne l'attire",
     "tube sous vide, lentilles électrostatiques, déflecteurs", "élevée")
comp("DOC-008 r.5", "Régulateur d'électrons", "régler le courant injecté", "µA à mA, stabilité 1e-3",
     "régulation de courant de faisceau courante", "0", "Démontré", "oui", "non", "électronique standard",
     "wehnelt + asservissement du courant d'émission", "élevée")
comp("DOC-008 r.6", "Générateur d'électrons", "produire le faisceau", "10 à 100 keV, ≤ 1 mA (100 W)",
     "canons thermo-ioniques et photocathodes (jusqu'à 65 mA moyens à 4-5 MeV)", "0", "Démontré", "oui", "non",
     "technologie centenaire (tube cathodique)", "cathode LaB6 ou tungstène, alimentation HT 100 kV", "élevée")
comp("DOC-008 r.7", "Capteur de singularité (« sensor booster »)", "mesurer les paramètres de la singularité",
     "position, masse, charge, rotation d'un objet de 1e-15 m", "gradiométrie (20 E), spectrométrie γ",
     "non chiffrable", "Théoriquement possible (position par gravimétrie) ; Spéculatif (charge, rotation)",
     "partiel", "non",
     "la position d'une masse de 1e11-1e12 kg se déduit trivialement de son champ, mais aucun capteur ne survit à > 1e3 Gy/s et à des MW thermiques",
     "accéléromètres + détecteurs γ durcis (si la source était 1e9 fois moins intense)", "moyenne")
comp("DOC-008 r.8", "Enveloppe de refroidissement", "extraire la chaleur des singularités",
     f"{Q_ref/1e6:.0f} MW (130 à 1000 MW) ; flux pariétal {flux5:.1e} W/m²",
     "flux critique record 276 MW/m² ; divertor ITER 10-20 MW/m²", f"{log10(flux5 / 276e6):+.1f} (flux) ; "
     f"{log10(Q_ref / P49):+.1f} (puissance / coffre à 49 °C)", f"Contredit (dans {fr(K.COFFRE_V, 2)} m³)",
     "oui (jusqu'à ~0,1 à 1 MW dans ce volume)", "non (limite d'ingénierie, mais 6 décades)",
     "les γ et e± de 5 à 70 MeV déposent leur énergie en volume ; un absorbeur de tungstène fond en ~10 ms",
     "chemise d'eau à micro-canaux, quelques centaines de kW", "élevée")
comp("DOC-008 r.9", "Pompe de refroidissement", "faire circuler le caloporteur",
     f"{pompe['debit_kg_s']:.0f} kg/s d'eau, {pompe['puissance_pompe_W']/1e6:.1f} MW",
     "turbopompe SSME : 53,7 MW pour 352 kg (plus que la masse de l'unité)", "+2,0 (puissance / batterie)",
     "Démontré (ailleurs) ; Contredit (dans l'unité)", "oui (pompe de quelques kW)", "non",
     "débit et puissance d'une centrale thermique de 300 MWe", "pompe centrifuge 24 V, 1 kW", "élevée")
comp("DOC-008 r.10", "Réservoirs de caloporteur (x2)", "réserve de fluide",
     f"{eau6h['masse_pour_6h_circuit_ouvert_kg']:.1e} kg d'eau vaporisée sur 6 h (circuit ouvert)",
     "2 x 0,25 L à l'échelle du schéma (Équipes E et I) ; 2 x 15 L en borne haute [HYP], soit 86 % du volume utile",
     f"{log10(eau6h['masse_pour_6h_circuit_ouvert_kg'] / M_RES):+.1f}", "Contredit", "oui (les réservoirs)", "non",
     f"vidés en {fr(eau6h['autonomie_reservoirs_s'] * 1e3)} ms (borne haute : {fr(eau6h['autonomie_reservoirs_borne_haute_s'])} s) ; en circuit fermé il faut un radiateur de 700 m² à 1500 K par tranche de 177 MW",
     "bouteilles inox", "élevée")
comp("DOC-008 r.11", "Unité de capteurs de gravité (VGL)", "« instantané » du champ local servant de référence de position",
     "4,0 µGal (bloc de 2,4 t à 2 m) à 7,4 µGal (mur de 10 t à 3 m) ; une tonne à 2-3 m ne donne que 1,7-0,7 µGal ; fonctionnement à 2 g et 38-49 °C",
     "FG5-X 2 µGal (150 kg, 20-30 °C) ; CG-6 5 µGal (5,5 kg, ≤ 45 °C) ; iGrav 0,3 µGal/√Hz ; AQG 2 µGal",
     "0 (au repos, à 1 g) ; +6 (dans le champ des singularités)",
     "Démontré (détection de masses proches) ; Contredit (référence de position, mesure à côté des singularités)",
     "oui (détection au repos d'un obstacle de plusieurs tonnes à 2-3 m ; l'instrument de 10,8 L occupe 31 % du volume utile)",
     "non (mais la fonction « verrou de position » n'a pas de base physique)",
     "8 nombres mesurables en un point (g et son gradient) ne définissent pas une position ; plage du CG-6 = 1/123 de g ; tenue de position requise ~1e-12 m",
     "gravimètre relatif + gradiomètre, mesure véhicule à l'arrêt, moteur coupé, plusieurs minutes", "élevée")
comp("DOC-008 r.12", "Batterie", "alimentation électrique de l'unité",
     f"auxiliaires : {C6['auxiliaires_W']['min']:.0f} à {C6['auxiliaires_W']['max']:.0f} W ; pompe et aimants : MW ; création : {E_crea:.0e} J",
     "Li-ion 150-180 Wh/kg (pack) ; 50 kg = 7,5 kWh mais ~30 L (86 % du volume utile) ; pack logeable : 1,34 kWh, 9,5 kg, 4 L (Équipe I)",
     "-0,1 (auxiliaires) ; +2 (pompe) ; +22,5 (création)",
     "Démontré (auxiliaires) ; Contredit (le reste)", "oui (pour l'électronique)", "oui comme source primaire",
     "conservation de l'énergie : 27 MJ contre 1e13 J rayonnés et 8e29 J de création",
     "pack LiFePO4 logeable de 1,34 kWh avec BMS (auxiliaires réduits : 0,75 kWh par trajet) ; 7,5 kWh seulement hors du coffre",
     "élevée")
comp("texte", "Quatre horloges au césium", "base de temps du calcul (« l'unité est la seconde »)",
     "exactitude ≤ 5e-5 pour dater à 1 jour sur 60 ans",
     "5071A : 5e-13 (30 kg, 50 W, 0-50 °C) ; CSAC : 3e-10 à 1 s (35 g, 0,12 W, -10 à +70 °C)", "-8 (largement satisfait)",
     "Démontré", "oui", "non",
     f"4 horloges permettent de détecter et d'écarter une horloge fautive (GPS Block II/IIA : 2 Cs + 2 Rb ; Galileo : 4 horloges). En 2000 : 4 x 30 kg = {q5071['fraction_du_volume_coffre']*100:.0f} % du volume du coffre (un seul étalon, long de 52 cm, n'y entre pas) ; depuis 2011 : 140 g",
     "4 CSAC SA.45s + comparateur de phase + vote", "élevée")
comp("texte", "Trois calculateurs à vote (« Borda »)", "calcul redondant, déclenchement du VGL",
     "tolérer une panne de calculateur sur 6 h", "TMR (Boeing 777 : triple-triple), accord byzantin",
     "0", "Démontré (TMR) ; aucun « protocole de Borda » connu", "oui", "non",
     "défaillance sur 6 h : 6e-4 (simplex) → 1e-6 (TMR) pour λ = 1e-4/h ; un décompte de Borda laisse un calculateur fautif renverser deux calculateurs sains (c08)",
     "3 calculateurs dissemblables, voteur médian matériel, chien de garde", "élevée")
comp("DOC-007 r.3", "Télécommande filaire", "commande déportée, affichage", "liaison série sur cordon spiralé",
     "pupitres filaires industriels", "0", "Démontré", "oui", "non", "aucune difficulté",
     "boîtier à écran + bus CAN/RS-485", "élevée")
comp("DOC-007 r.4-6, 8", "Arrêt d'urgence, interrupteur général, écran de secours", "mise en sécurité",
     "atteindre un état sûr", "ISO 13850 / IEC 60204-1 (catégories d'arrêt 0 et 1)", "0 (le circuit)",
     "Démontré (le circuit) ; Contredit (l'état sûr)", "oui", "oui pour la fonction",
     "couper l'alimentation n'éteint ni la gravité ni le rayonnement de Hawking ; le texte dit lui-même que la perte du confinement est catastrophique : il n'existe pas d'état de repli sûr",
     "chaîne d'arrêt câblée à double canal", "élevée")
comp("DOC-009 r.5", "« Cône d'évacuation des rayons X »", "canaliser le rayonnement vers l'arrière",
     "~100 % du rayonnement dans un cône ; rayons X", "collimateurs = absorbeurs ; optiques X ≤ ~80 keV",
     "+1,2 (fraction dans un cône de 30°)", "Contredit", "non", "oui",
     "émission de Hawking isotrope (Schwarzschild) ou large (Kerr) ; 55 % de neutrinos indéviables ; γ de 5-70 MeV ni réfléchis ni réfractés ; seuls les e± (37 %) sont guidables par un champ ≥ 10 T",
     "—", "élevée")
comp("(absent)", "Blindage radiologique", "protéger l'équipage (non mentionné par la source)",
     f"{fr(ep_etroit['epaisseur_plomb_m']*100)} à {bl['epaisseur_plomb_m']*100:.0f} cm de plomb (faisceau étroit à large), {fr(ep_etroit['masse_sphere_plomb_kg']/1e3)} à {bl['masse_sphere_plomb_kg']/1e3:.0f} t (1 mSv par trajet)",
     f"{fr(bproche['epaisseur_plomb_m']*100)} à {fr(blog['epaisseur_plomb_m']*100)} cm logeables dans le coffre (reste {bproche['debit_dose_residuel_photons_1m_Gy_s']:.0f} à {blog['debit_dose_residuel_photons_1m_Gy_s']:.0f} Gy/s à 1 m)", f"{log10(bl['facteur_attenuation'] / C5['blindage_logeable']['attenuation']):+.1f} (atténuation manquante)",
     "Démontré (physique du blindage) ; Contredit (dans 227 kg)", "non (dans l'enveloppe)", "non (masse et volume)",
     f"sans blindage : {dose1:.0f} Gy/s à 1 m (γ seuls), dose létale en ~1 ms",
     "—", "moyenne (TVL extrapolés au-delà de 20 MV)")
comp("texte", "Mise en rotation et orientation de l'axe polaire", "modeler le « sinusoïde »",
     "J jusqu'à GM²/c ; réorientation en un temps opérationnel", "aucune",
     f"{log10(1.0 / C3['rotation'][0]['precession_45p5T_charge_extremale_rad_s']):+.1f} (précession)", "Contredit",
     "non", "oui",
     "énergie de rotation jusqu'à 0,29 M c² ; précession magnétique ≤ 4e-9 rad/s à 45,5 T même à charge extrémale ; avec 6 e : 1e-29 rad/s",
     "—", "élevée")
comp("texte", "Véhicule porteur à suspension « rigide »", "porter l'unité",
     "227 kg (revendiqué) ou 3e11 à 9e12 kg (exigé par les autres chiffres)", "charge utile ~0,7 à 1,5 t [HYP]",
     "-0,6 (227 kg) ; +8 à +10 (masses exigées)", "Démontré (227 kg) ; Contredit (masse réelle)",
     "oui (227 kg)", "oui (masse réelle)",
     "227 kg = 3 passagers : aucune suspension spéciale requise ; la masse exigée traverserait le véhicule et le sol (24 à 720 TPa sous les pneus)",
     "arrimage 4 points, plancher renforcé", "élevée (calcul) ; charge utile exacte non confirmée")
comp("DOC-004/007/008 ; texte", "Ensemble des périphériques dans le coffre (budget masse + volume)",
     "tout loger dans une unité de 227 kg",
     f"227 kg dans {fr(K.COFFRE_V*1e3)} L d'enveloppe ({fr(K.VOLUME_UTILE*1e3)} L utiles) : {vmv['masse_volumique_requise_dans_l_enveloppe_kg_m3']:.0f} kg/m³",
     f"périphériques sans contrainte de place : {vmv['masse_configuration_genereuse_kg']:.0f} kg et {vmv['volume_configuration_genereuse_L']:.0f} L ; version logeable (Équipe I, palier R1) : {vmv['configuration_logeable']['masse_kg']:.0f} kg, {vmv['configuration_logeable']['occupation']*100:.0f} % du volume utile",
     f"masse : {log10(vmv['masse_configuration_genereuse_kg'] / K.MASSE_UNITE):+.2f} (passe) ; volume : {log10(vmv['rapport_volume_sur_volume_utile']):+.2f} (x {fr(vmv['rapport_volume_sur_volume_utile'])}, ne passe pas)",
     "Démontré (chaque composant) ; Contredit (l'ensemble dans ce volume, et 227 kg pour ce qui s'y loge)",
     "oui en version réduite seulement (réservoirs, batterie et bobines réduits ; gravimètre amovible)",
     "non (limite d'encombrement)",
     f"le budget de masse seul ({vmv['masse_configuration_genereuse_kg']:.0f} kg) ne suffit pas : {vmv['volume_configuration_genereuse_L']:.0f} L à loger dans {vmv['volume_utile_L']:.0f} L ; ce qui tient pèse {vmv['configuration_logeable']['masse_kg']:.0f} kg ; atteindre 227 kg demande ~{vmv['lest_pour_atteindre_227kg']['masse_kg']:.0f} kg de matière dense",
     "palier R1 de l'Équipe I (10_machine_optimisee/RAPPORT_I.md)", "moyenne (volumes [HYP] ; échelle du coffre à ± 0,2 m)")

with open(os.path.join(RACINE, "tableau_faisabilite.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COL)
    w.writeheader()
    w.writerows(T)

print(f"{len(ecarts)} lignes -> tableau_exigences_ecarts.csv ; {len(T)} lignes -> tableau_faisabilite.csv")
for e_ in ecarts:
    print(f"{e_['sous_systeme']:18s} {e_['exigence_revendiquee_ou_deduite'][:70]:70s} {e_['valeur_requise']:>9s} {e_['unite']:6s} "
          f"vs {e_['valeur_reelle']:>9s}  Δ = {e_['ecart_en_ordres_de_grandeur']}")
