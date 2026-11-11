#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i07 : table de correspondance composant par composant et indicateur de « proximité à la C204 ».

Pour chacun des 14 éléments de l'architecture d'origine : fonction revendiquée → verdict physique (repris des
Équipes B et C) → remplaçant réel le plus proche à chaque palier → ce qu'il accomplit effectivement (chiffres
lus dans les sorties des scripts i01 à i05).

GRILLE DE PROXIMITÉ — NOTES SUBJECTIVES de l'Équipe I (correction post-validation I-1 : l'indice ne doit jamais être
cité sans cette réserve ; règles explicites, toutes les notes figurent dans grille_proximite_detail.csv) :
  A  Architecture conservée : par élément, 1 = même nature et même rôle ; 0,75 = même nature, technologie changée ;
     0,5 = même emplacement et rôle analogue, nature physique différente ; 0,25 = emplacement conservé, rôle nominal ;
     0 = absent. Moyenne pondérée (poids 2 pour les deux singularités, 1 ailleurs).
  F  Fonctions effectivement remplies : dix fonctions revendiquées, pondérées ; l'ampleur du décalage relativiste
     est notée sur une échelle logarithmique entre ce que produit la masse propre de l'unité (0) et « 10 ans par heure » (1).
     RÉSERVE : pour R1 et R2 ce décalage est celui du TRAJET (tout objet le subit) ; la machine n'en est pas la cause.
     Le script calcule donc aussi l'indice SANS cette fonction (colonne « sans l'ampleur du trajet »).
  C  Cohérence physique : Démontré = 1 ; Théoriquement possible = 0,6 ; Spéculatif = 0,2 ; Contredit = 0.
  D  Constructibilité : niveau de maturité technologique (TRL 0 à 9) divisé par 9.
  Indice de proximité = moyenne géométrique de A, F, C, D (un zéro sur un axe annule l'indice).
  Indice « strict » = indice × (TRL minimal / 9) × (cohérence minimale) : la chaîne vaut son maillon le plus faible.

Sorties : ../correspondance_composants.csv, ../grille_proximite.csv, ../grille_proximite_detail.csv,
          resultats/i07_proximite.json / .txt
"""
import json
import math

from i00_commun import RES, RACINE, DEPL_REVENDIQUE_S_PAR_H, ecrire_csv, ecrire_json, ecrire_txt, fr

r1 = json.loads((RES / "i01_deplacement.json").read_text(encoding="utf-8"))
r3d = json.loads((RES / "i03_demonstrateurs.json").read_text(encoding="utf-8"))
r4 = json.loads((RES / "i04_palier2.json").read_text(encoding="utf-8"))
r5 = json.loads((RES / "i05_palier3.json").read_text(encoding="utf-8"))
r2 = json.loads((RES / "i02_bilans_R1.json").read_text(encoding="utf-8"))
A1 = r2["R1-A"]
T_coffre = r2["thermique"]["R1-A mesure (géométrie E)"]["temperature_C"]

D_car = r1["scenarios"]["S05"]["D_futur_ns_par_h"]
D_tgv = r1["scenarios"]["S08"]["D_futur_ns_par_h"]
D_alt = r1["scenarios"]["S01"]["avance_horloge_ns_par_h"]
mu10 = r3d["muons"]["geometries"]["d=10cm"]
sag = r3d["sagnac"]["rotation terrestre, composante verticale à 45°"]
D_self = r1["potentiel_propre_227kg_1m"]["s_par_h"]
g_bh = r5["b_trou_noir"]["gamma_final"]["eta=0.44,R=1001"]

STATUT = {"Démontré": 1.0, "Théoriquement possible": 0.6, "Spéculatif": 0.2, "Contredit": 0.0}

# Chaque élément : nom, repères, fonction revendiquée, verdict (statut, justification chiffrée, source),
# puis pour R1, R2, R3 : (remplaçant, ce qu'il accomplit, ce qu'il ne fait pas, note A, statut physique, TRL)
# et pour l'original : (note A = 1), statut de la fonction revendiquée, TRL de la fonction revendiquée.
ELEMENTS = [
    dict(nom="Singularité principale", repere="DOC-007 r.1 ; DOC-008 r.1", poids=2,
         fonction="micro-trou noir « chaud » (300–500 MW) : source de la distorsion de gravité",
         verdict=("Contredit", "300–500 MW ⇒ 3,9–5,1×10¹² kg ; 227 kg ⇒ évaporation en 4,8 ps (2×10¹⁹ J)", "Équipe B §4 ; Équipe C §4.1"), trl0=0,
         R1=("Télescope à muons cosmiques (2 scintillateurs superposés sous le logement)",
             f"compte {mu10['par_heure']:.0f} muons/h dans un cône de ±{mu10['demi_angle_max_deg']:.0f}° ; montre une dilatation du temps d'un facteur ≳ 7 à 40 sur des particules naturelles (sans dilatation : ×{r3d['muons']['rapport_sans_dilatation_dh=2000']:.0f} entre 2 000 m et la plaine)",
             "ne produit aucune gravité ni aucune dilatation ; il observe celle de particules venues d'ailleurs", 0.5, "Démontré", 8),
         R2=("Horloge optique à ion unique n° 1 (piège de Paul sous ultravide)",
             "étalon de fréquence à 10⁻¹⁸–10⁻¹⁹ : résout 1 cm puis 1 mm de dénivelé (décalage gravitationnel réel)",
             "ne courbe rien : elle mesure la courbure existante", 0.5, "Démontré", 5),
         R3=("Trou noir de ~10⁹ kg (vaisseau de Crane & Westmoreland)",
             "6×10¹⁶ W de rayonnement de Hawking pendant ~15 ans (calcul de l'Équipe B)", "infabricable (≥ 9×10²⁵ J) ; ne crée aucune courbe temporelle fermée", 1.0, "Théoriquement possible", 1)),
    dict(nom="Singularité de direction", repere="DOC-007 r.2", poids=2,
         fonction="second micro-trou noir : oriente le « sinusoïde », déplace le centre de masse",
         verdict=("Contredit", "aucun équilibre de deux trous de Kerr (théorème) ; précession ≤ 4×10⁻⁹ rad/s même à charge extrémale", "Équipe B §3.5 ; Équipe C §4.3"), trl0=0,
         R1=("Gyromètre Sagnac à fibre optique (deux ondes contrarotatives, bobine de 500 m)",
             f"mesure la rotation : Δt = {sag['decalage_temporel_s']:.1e} s entre les deux ondes pour la rotation terrestre ; donne le cap, qui fixe le SIGNE du décalage cinématique du trajet ({D_car:+.2f} ns/h vers l'est, {r1['scenarios']['S06']['D_futur_ns_par_h']:+.2f} ns/h vers l'ouest à 130 km/h)",
             "n'oriente aucun champ ; un récepteur GNSS suffirait pour le cap", 0.5, "Démontré", 7),
         R2=("Horloge optique à ion unique n° 2, à hauteur réglable",
             f"comparée à la n° 1 : Δf/f = 1,09×10⁻¹⁸ par centimètre de surélévation ; résolution {r4['M1']['Ion unique ¹⁷⁶Lu⁺ (Arnold et al. 2026)']['incertitude']:.1e}",
             "ne « dirige » rien", 0.5, "Démontré", 5),
         R3=("Absorbeur anisotrope du rayonnement (direction de la poussée)", "poussée ≤ P/c = 2×10⁸ N pour 10⁹ kg", "pas de second trou noir", 0.5, "Théoriquement possible", 1)),
    dict(nom="Logements et bobines de champ magnétique (avec générateur / régulateur de champ)", repere="DOC-008 r.1-2-3", poids=1,
         fonction="confiner, séparer et orienter les singularités chargées",
         verdict=("Contredit", "charge tenable ≤ 137 e ; champ requis 5×10¹¹ T (record continu 45,5 T) ; Earnshaw", "Équipe B §4.5 ; Équipe C §4.1"), trl0=0,
         R1=("Carters transparents des deux démonstrateurs ; bobine de fibre du gyromètre ; blindage mu-métal et bobines de compensation des horloges",
             "protège les horloges du champ ambiant (sensibilité d'une CSAC : ~10⁻¹⁰ par gauss, estimation) ; champ < 1 mT",
             "ne confine aucune particule", 0.5, "Démontré", 8),
         R2=("Piège de Paul radiofréquence + bobines de champ de quantification, enceinte ultravide",
             "confine UN ion (q/m ~ 10⁶ C/kg) pendant des jours : confinement électromagnétique réel d'une charge",
             "q/m d'un trou noir : ≤ 8,6×10⁻¹¹ C/kg — 17 ordres de grandeur en dessous", 0.75, "Démontré", 6),
         R3=("Aucun confinement possible : le vaisseau « suit » le trou noir (attraction mutuelle, structure à distance)",
             "—", "aucun champ ne tient 10⁹ kg concentrés dans 10⁻¹⁸ m", 0.25, "Spéculatif", 1)),
    dict(nom="Générateur, régulateur et collecteur d'injection d'électrons", repere="DOC-008 r.4-5-6", poids=1,
         fonction="modifier la masse et la gravité des singularités ; agrandir l'horizon interne",
         verdict=("Contredit", "ΔM/M ≤ 4,9×10⁻²² ; barrière 10²⁷ eV ; r₋ ~ 10⁻⁵³ m", "Équipe B §4.5 ; Équipe C §4.2"), trl0=0,
         R1=("Chaîne d'alimentation très basse tension : convertisseurs, régulateurs, barres de distribution",
             f"distribue ~{A1['puissance_mesure_W']:.0f} W sous ≤ 24 V (≈ 30 V pour la seule polarisation des photodétecteurs) : les seuls électrons « générés, régulés et distribués » sont ceux du courant",
             "aucun faisceau d'électrons libre (haute tension exclue du palier 1)", 0.25, "Démontré", 9),
         R2=("Canon à électrons d'ionisation / photo-ionisation pour charger le piège",
             "crée l'ion à partir d'un atome neutre : une « injection » de charge réelle, un électron à la fois",
             "ne change ni masse ni gravité (10⁻³⁰ kg par électron)", 0.5, "Démontré", 8),
         R3=("Alimentation en matière du trou noir", "0,7 kg/s à faire avaler à un objet de 10⁻¹⁸ m pour 10⁹ kg",
             "aucun procédé connu (pression de rayonnement, section de capture)", 0.5, "Spéculatif", 1)),
    dict(nom="Capteur de singularité (« sensor booster »)", repere="DOC-008 r.7", poids=1,
         fonction="mesurer l'état des singularités",
         verdict=("Spéculatif", "position déductible du champ, mais aucun capteur ne survit à > 10³ Gy/s", "Équipe C, tableau de faisabilité"), trl0=1,
         R1=("Photomultiplicateurs au silicium (muons) et photodiode (gyromètre), électronique de proximité",
             "détecte chaque muon (impulsion de quelques dizaines de mV) et un déphasage optique de ~10⁻⁵ rad",
             "—", 0.5, "Démontré", 9),
         R2=("Photomultiplicateur / caméra à comptage de photons lisant la fluorescence de l'ion",
             "lit l'état quantique d'UN ion : c'est réellement un « amplificateur de capteur »", "—", 0.75, "Démontré", 9),
         R3=("Spectromètres γ et gravimètres durcis", "masse, moment cinétique et charge déduits du spectre de Hawking", "—", 0.75, "Théoriquement possible", 3)),
    dict(nom="Refroidissement (enveloppe, pompe, deux réservoirs)", repere="DOC-008 r.8-9-10", poids=1,
         fonction="refroidir les singularités",
         verdict=("Contredit", "133–1 000 MW à évacuer de 0,13 m³ ; capacité calorifique d'un trou noir négative", "Équipe B §4.2 ; Équipe C §4.4"), trl0=0,
         R1=("Boucle thermique à eau glycolée : micro-pompe 12 V, deux réservoirs tampons, plaque froide, ventilateur",
             f"évacue ~{A1['puissance_mesure_W']:.0f} W ; tient l'enceinte des horloges à ±0,1 K (objectif de conception) ; coffre à ~{T_coffre:.0f} °C pour 20 °C d'ambiance",
             "rien à refroidir d'autre que l'électronique", 0.75, "Démontré", 9),
         R2=("Refroidissement laser de l'ion (≈ mK) ; machine cryogénique éventuelle",
             "amène la particule piégée à ~10⁻³ K : un « refroidissement de la singularité » réel, mais d'un ion",
             "—", 0.5, "Démontré", 8),
         R3=("Radiateurs de l'absorbeur (10¹⁶ W)", "—", "flux ≫ limite des matériaux", 0.75, "Théoriquement possible", 2)),
    dict(nom="« Évent à rayons X » (cône ou zone)", repere="DOC-009 r.5", poids=1,
         fonction="canaliser le rayonnement vers l'arrière",
         verdict=("Contredit", "émission isotrope de γ (5–70 MeV), e±, ν (55 %) ; X < 10⁻⁶ ; 3 300 Gy/s à 1 m", "Équipe C §4.4 ; errata E5"), trl0=0,
         R1=("Cône d'ACCEPTANCE du télescope à muons + dosimètre à semi-conducteur du fond naturel + évent d'air tiède",
             "n'émet rien ; reçoit le rayonnement cosmique dans un cône de ±35° ; dosimètre à semi-conducteur du fond naturel (~0,1 µSv/h, ordre de grandeur) ; aucune source, aucune tension > 30 V",
             "aucun rayon X émis", 0.5, "Démontré", 9),
         R2=("Hodoscope à muons (durée de vie du muon au repos, taux selon l'altitude)", "mesure τ = 2,2 µs et γ par comparaison de taux", "—", 0.25, "Démontré", 9),
         R3=("Échappement dirigé de γ et e± (≤ 44 % de la puissance)", "poussée du vaisseau", "neutrinos (55 %) non dirigeables", 0.75, "Théoriquement possible", 2)),
    dict(nom="Capteurs de gravité (système VGL)", repere="DOC-008 r.11", poids=1,
         fonction="« verrouiller » la position par un instantané du champ de gravité local",
         verdict=("Contredit", "mesurer g est Démontré (1–5 µGal) ; « verrou » : problème inverse non unique, 8 nombres par point", "Équipe C §4.6"), trl0=0,
         R1=("Triade d'accéléromètres à quartz (classe milligal) ; en option gravimètre relatif de classe microgal, amovible",
             "mesure g à ~1 mGal en continu, 5 µGal à l'arrêt avec l'option (1 µGal ↔ 3 mm de dénivelé) ; fournit la prédiction classique ΔW = ∫g·dh du décalage d'horloge",
             "ne verrouille aucune position ; ne mesure pas le potentiel (seule une horloge le fait)", 0.75, "Démontré", 9),
         R2=("Gravimètre absolu et gradiomètre à atomes froids",
             f"1 µGal de stabilité ; gradient à 20 E ; détecte une tonne à {r4['M2']['portee_3sigma_masse_1000kg_m']:.1f} m",
             "idem", 0.75, "Démontré", 8),
         R3=("Navigation gravimétrique / pulsars", "—", "—", 0.5, "Démontré", 9)),
    dict(nom="Quatre horloges au césium", repere="texte (2 nov. 2000)", poids=1,
         fonction="base de temps du calcul de déplacement",
         verdict=("Démontré", "4 étalons permettent d'écarter une horloge fautive ; 4 CSAC = 140 g", "Équipe C §4.6"), trl0=9,
         R1=("4 horloges atomiques miniatures au césium (CSAC) + comparateur de phase à 6 voies ; module externe optionnel de 1 à 3 étalons à jet de césium",
             f"datent à ~1 µs sur 48 h ; les CSAC ne voient pas le décalage relativiste du trajet (S/B ≈ {r1['detectabilite_48h']['CSAC au césium (SA.45s)']['SB']['1000']:.3f}) ; avec le module à jet de césium : S/B ≈ {r1['detectabilite_48h']['Césium à jet 5071A, tube haute performance']['SB']['1000']:.1f} pour 1 000 m et 48 h",
             "sans module externe : aucune mesure relativiste ; la mesure exige en outre une référence restée au sol (3 étalons ou un lien de temps étalonné)", 1.0, "Démontré", 9),
         R2=("Deux horloges optiques + oscillateur volant (maser ou cavité) + CSAC de secours",
             "résolution 10⁻¹⁸ : 3,6×10⁻¹⁵ s par heure", "fonctionnement intermittent : mesure un taux, pas une durée cumulée", 0.75, "Démontré", 6),
         R3=("Horloges optiques ou nucléaires embarquées", "—", "—", 1.0, "Démontré", 9)),
    dict(nom="Trois calculateurs à vote (« Borda »)", repere="texte (2 nov. 2000)", poids=1,
         fonction="calcul redondant et correction d'erreurs",
         verdict=("Démontré", "redondance modulaire triple : défaillance sur 6 h de 6×10⁻⁴ à 1×10⁻⁶ ; « Borda » n'est pas un protocole de tolérance aux pannes", "Équipe C §4.7"), trl0=9,
         R1=("3 calculateurs d'architectures différentes + voteur médian matériel + chien de garde",
             "tolère une panne franche ; pas une panne byzantine (il en faudrait 4)", "—", 1.0, "Démontré", 9),
         R2=("Idem + acquisition en aveugle (clé scellée, comme EXP-12)", "idem", "—", 1.0, "Démontré", 9),
         R3=("Idem", "—", "—", 1.0, "Démontré", 9)),
    dict(nom="Batterie", repere="DOC-008 r.12", poids=1,
         fonction="alimentation électrique de l'unité",
         verdict=("Contredit", "suffisante pour les auxiliaires (0,2–0,9 kW) ; 22,5 ordres de grandeur trop faible comme source de l'effet", "Équipe C §4.5"), trl0=5,
         R1=("Batterie LiFePO4 12,8 V 1,34 kWh", f"{A1['autonomie_mesure_h']:.0f} h en mesure, {A1['autonomie_transport_h']:.0f} h en transport ({A1['puissance_mesure_W']:.0f} W / {A1['puissance_transport_W']:.0f} W)", "—", 1.0, "Démontré", 9),
         R2=("Secteur + onduleur (plusieurs kW)", "—", "plus d'autonomie sur batterie", 0.25, "Démontré", 9),
         R3=("Le trou noir est la source", "—", "—", 0.25, "Théoriquement possible", 1)),
    dict(nom="Télécommande filaire", repere="DOC-007 r.3, r.9", poids=1,
         fonction="commande déportée", verdict=("Démontré", "aucune difficulté", "Équipe C §7"), trl0=9,
         R1=("Boîtier à écran et clavier, bus CAN", "saisie du scénario, lecture des écarts d'horloge", "—", 1.0, "Démontré", 9),
         R2=("Poste de commande", "—", "—", 0.75, "Démontré", 9), R3=("—", "—", "—", 0.5, "Démontré", 9)),
    dict(nom="Arrêt d'urgence, interrupteur général, écran de secours", repere="DOC-007 r.4-5-6-8", poids=1,
         fonction="mise en sécurité",
         verdict=("Contredit", "le circuit est constructible, mais couper l'alimentation n'éteint ni gravité ni rayonnement : pas d'état sûr", "Équipe C §4.7"), trl0=4,
         R1=("Coupe-batterie, relais de sécurité à double canal, avertisseur", "état sûr réel : tout hors tension, aucune énergie dangereuse stockée hors batterie", "—", 1.0, "Démontré", 9),
         R2=("Chaîne d'arrêt + interverrouillages laser et haute tension", "état sûr réel", "—", 1.0, "Démontré", 9),
         R3=("Aucun état sûr : un trou noir ne s'éteint pas", "—", "—", 0.25, "Spéculatif", 1)),
    dict(nom="Coffre transportable de 227 kg dans un véhicule", repere="DOC-001 à 004, 013 ; texte", poids=1,
         fonction="unité « à masse stationnaire » portable entre véhicules",
         verdict=("Contredit", "227 kg dans 0,063 m³ = 3 600 kg/m³ ; les masses exigées par les autres chiffres vont de 3×10¹¹ à 10¹³ kg", "Équipe A I-09 ; Équipe C §4.8"), trl0=5,
         R1=(f"Coffre de 0,85 × 0,26 × 0,24–0,29 m, {A1['masse_kg']:.0f} kg (R1-A) ; {r2['R1-B_total']['masse_kg']:.0f} kg avec le module césium hors coffre (R1-B)", "transportable à deux personnes ; ≈ 600 kg/m³", "ne pèse pas 227 kg, et n'a aucune raison de les peser", 1.0, "Démontré", 9),
         R2=("Remorque ou laboratoire (plusieurs tonnes, kW)", "—", "non portable", 0.25, "Démontré", 6),
         R3=("Vaisseau de ≥ 10⁹ kg", "—", "—", 0.0, "Théoriquement possible", 1)),
]

# Fonctions revendiquées : (libellé, poids, {conception: note 0–1})
D_r3 = (g_bh - 1) * 3600
ech = lambda v: max(0.0, min(1.0, (math.log10(v) - math.log10(D_self)) / (math.log10(DEPL_REVENDIQUE_S_PAR_H) - math.log10(D_self))))
D_R1 = D_tgv * 1e-9
D_R2 = D_car * 1e-9
FONCTIONS = [
    ("Ampleur du décalage relativiste subi sur le trajet nominal (échelle logarithmique) — pour R1 et R2 : effet du TRAJET, non imputable à la machine", 3,
     {"O": ech(D_self), "R1": ech(D_R1), "R2": ech(D_R2), "R3": ech(D_r3)},
     f"O : {D_self:.1e} s/h (masse propre) ; R1 : {D_R1:.1e} s/h (train vers l'est) ; R2 : {D_R2:.1e} s/h (remorque à 130 km/h vers l'est) ; R3 : {D_r3:.1e} s/h (γ = {g_bh:.1f})"),
    ("Déplacement vers le PASSÉ", 3, {"O": 0, "R1": 0, "R2": 0, "R3": 0}, "aucune conception : interdit par la structure causale (Équipe B §5.5)"),
    ("Déplacement vers le futur", 1, {"O": 1, "R1": 1, "R2": 1, "R3": 1}, "toute horloge en mouvement ou plus bas dans un potentiel"),
    ("Changement de « ligne d'univers »", 1, {"O": 0, "R1": 0, "R2": 0, "R3": 0}, "aucune définition physique"),
    ("Mesure effective du décalage relativiste de son propre trajet", 2, {"O": 0, "R1": 0.5, "R2": 1, "R3": 1},
     "O : horloges au césium 15 à 2 300 fois trop peu exactes (Équipe C) ; R1 : seulement avec le module externe ; R2 : oui, à 10⁻¹⁸"),
    ("Unité immobile pendant le déplacement (« masse stationnaire »)", 1, {"O": 1, "R1": 0.5, "R2": 0.5, "R3": 0},
     "R1/R2 : vrai pour les scénarios d'altitude seulement (où l'unité vieillit PLUS)"),
    ("Autonomie sur batterie, transport dans un véhicule", 1, {"O": 1, "R1": 1, "R2": 0.25, "R3": 0}, ""),
    ("Mesure du champ de gravité local", 1, {"O": 1, "R1": 0.75, "R2": 1, "R3": 1}, "R1 : milligal en natif, microgal avec l'option"),
    ("Datation par horloges atomiques redondantes et calcul à vote", 1, {"O": 1, "R1": 1, "R2": 1, "R3": 1}, ""),
    ("Mise en sécurité effective", 1, {"O": 1, "R1": 1, "R2": 1, "R3": 0}, "O : la maquette inerte est sûre ; la machine revendiquée ne le serait pas"),
]
# Niveau de maturité de l'intégration d'ensemble (jamais assemblée)
TRL_INTEGRATION = {"O": 0, "R1": 6, "R2": 4, "R3": 1}


def main():
    L = ["i07 — CORRESPONDANCE ET PROXIMITÉ", "=" * 100]
    # ---- correspondance
    lignes = []
    for e in ELEMENTS:
        st, just, src = e["verdict"]
        lignes.append([e["nom"], e["repere"], e["fonction"], st, just, src,
                       e["R1"][0], e["R1"][1], e["R1"][2], e["R2"][0], e["R2"][1], e["R2"][2], e["R3"][0], e["R3"][1], e["R3"][2]])
    ecrire_csv(RACINE / "correspondance_composants.csv",
               ["element_d_origine", "reperes", "fonction_revendiquee", "verdict_physique", "justification_chiffree", "source_du_verdict",
                "remplacant_R1", "R1_accomplit_reellement", "R1_ne_fait_pas", "remplacant_R2", "R2_accomplit_reellement", "R2_ne_fait_pas",
                "equivalent_R3", "R3_accomplit", "R3_limite"], lignes)

    # ---- grille
    det = []
    res = {}
    concepts = ["O", "R1", "R2", "R3"]
    FONCTIONS_SANS_AMPLEUR = FONCTIONS[1:]
    lib = {"O": "C204 d'origine (fonctions revendiquées, physique réelle)", "R1": "C204-R1 (constructible aujourd'hui)",
           "R2": "C204-R2 (laboratoire de recherche)", "R3": "C204-R3 (limite théorique : vaisseau à trou noir)"}
    for k in concepts:
        sw = sa = sc = sd = 0.0
        cmin, dmin = 1.0, 9.0
        for e in ELEMENTS:
            w = e["poids"]
            if k == "O":
                a, c_, d = 1.0, STATUT[e["verdict"][0]], e["trl0"]
            else:
                a, c_, d = e[k][3], STATUT[e[k][4]], e[k][5]
            sw += w; sa += w * a; sc += w * c_; sd += w * d / 9
            cmin, dmin = min(cmin, c_), min(dmin, d)
            det.append([lib[k], "élément", e["nom"], w, a, c_, d])
        dmin = min(dmin, TRL_INTEGRATION[k])
        A, C, D = sa / sw, sc / sw, sd / sw
        fw = sum(p for _l, p, _n, _c in FONCTIONS)
        F = sum(p * n[k] for _l, p, n, _c in FONCTIONS) / fw
        for l_, p, n, com in FONCTIONS:
            det.append([lib[k], "fonction", l_, p, n[k], "", com])
        det.append([lib[k], "intégration", "assemblage d'ensemble", "", "", "", TRL_INTEGRATION[k]])
        idx = 100 * (A * F * C * D) ** 0.25
        strict = idx * (dmin / 9) * cmin
        F2 = sum(p * n[k] for _l, p, n, _c in FONCTIONS_SANS_AMPLEUR) / sum(p for _l, p, _n, _c in FONCTIONS_SANS_AMPLEUR)
        res[k] = dict(libelle=lib[k], A=100 * A, F=100 * F, C=100 * C, D=100 * D, indice=idx, coherence_min=cmin, TRL_min=dmin, indice_strict=strict,
                      F_sans_ampleur_du_trajet=100 * F2, indice_sans_ampleur_du_trajet=100 * (A * F2 * C * D) ** 0.25)
    # variante : original « tel que revendiqué » (F = 100 par définition)
    o = res["O"]
    res["O_rev"] = dict(libelle="C204 d'origine, fonctions prises telles que revendiquées (pour mémoire)", A=o["A"], F=100.0, C=o["C"], D=o["D"],
                        indice=100 * (o["A"] / 100 * 1.0 * o["C"] / 100 * o["D"] / 100) ** 0.25, coherence_min=o["coherence_min"], TRL_min=o["TRL_min"], indice_strict=0.0,
                        F_sans_ampleur_du_trajet=100.0, indice_sans_ampleur_du_trajet=100 * (o["A"] / 100 * 1.0 * o["C"] / 100 * o["D"] / 100) ** 0.25)
    L.append("INDICE DE PROXIMITÉ — NOTES SUBJECTIVES de l'Équipe I (à ne pas citer sans cette réserve ; grille à rejouer)")
    L.append("%-72s %6s %6s %6s %6s | %7s | %5s %5s | %7s | %s" % ("conception", "A", "F", "C", "D", "indice", "Cmin", "TRLmin", "strict", "indice sans l'ampleur du trajet"))
    ordre = ["O_rev", "O", "R1", "R2", "R3"]
    for k in ordre:
        d = res[k]
        L.append("%-72s %6.0f %6.0f %6.0f %6.0f | %7.0f | %5.1f %5.0f | %7.0f | %6.0f" % (d["libelle"][:72], d["A"], d["F"], d["C"], d["D"], d["indice"], d["coherence_min"], d["TRL_min"], d["indice_strict"], d["indice_sans_ampleur_du_trajet"]))
    ecrire_csv(RACINE / "grille_proximite.csv",
               ["conception", "A_architecture_conservee_sur_100_(note_subjective)", "F_fonctions_remplies_sur_100_(note_subjective)", "C_coherence_physique_sur_100",
                "D_constructibilite_sur_100_(note_subjective)", "indice_de_proximite_moyenne_geometrique_(NOTES_SUBJECTIVES)", "coherence_minimale_0_1", "TRL_minimal",
                "indice_strict_maillon_faible_(NOTES_SUBJECTIVES)", "indice_sans_l_ampleur_du_decalage_du_trajet_(NOTES_SUBJECTIVES)", "reserve"],
               [[res[k]["libelle"], f"{res[k]['A']:.0f}", f"{res[k]['F']:.0f}", f"{res[k]['C']:.0f}", f"{res[k]['D']:.0f}", f"{res[k]['indice']:.0f}",
                 f"{res[k]['coherence_min']:.1f}", f"{res[k]['TRL_min']:.0f}", f"{res[k]['indice_strict']:.0f}", f"{res[k]['indice_sans_ampleur_du_trajet']:.0f}",
                 "notes subjectives de l'Équipe I : ne pas citer l'indice sans cette réserve ; le décalage relativiste de R1 et R2 est celui du trajet, pas de la machine"] for k in ordre])
    ecrire_csv(RACINE / "grille_proximite_detail.csv", ["conception", "type", "element_ou_fonction", "poids", "note_A_ou_F", "coherence_C", "TRL_ou_commentaire"], det)
    # sensibilité : moyenne arithmétique
    for k in ordre:
        d = res[k]
        d["indice_moyenne_arithmetique"] = (d["A"] + d["F"] + d["C"] + d["D"]) / 4
    L.append("")
    L.append("Sensibilité — moyenne arithmétique des quatre axes : " + " ; ".join("%s %.0f" % (k, res[k]["indice_moyenne_arithmetique"]) for k in ordre))
    L.append("Classement (indice géométrique) : " + " > ".join(sorted(["O", "R1", "R2", "R3"], key=lambda k: -res[k]["indice"])))
    L.append("Classement (indice strict)      : " + " > ".join(sorted(["O", "R1", "R2", "R3"], key=lambda k: -res[k]["indice_strict"])))
    res["echelle_fonction_1"] = dict(zero_s_par_h=D_self, un_s_par_h=DEPL_REVENDIQUE_S_PAR_H, R1_s_par_h=D_R1, R2_s_par_h=D_R2, R3_s_par_h=D_r3)
    ecrire_json("i07_proximite.json", res)
    ecrire_txt("i07_proximite.txt", L)


if __name__ == "__main__":
    main()
