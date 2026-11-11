#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i02 : nomenclature chiffrée du palier 1 (C204-R1), bilans de masse / énergie / thermique,
et test d'encombrement en fonction de la longueur L du coffre (0,60 à 1,20 m ; nominal 0,85 m).

Deux configurations :
  R1-A « coffre seul »          : tout tient dans le coffre ; mesure g, rotation, muons, environnement ;
                                   CALCULE son déplacement temporel mais ne peut pas le MESURER (voir i01).
  R1-B « coffre + module césium » : ajoute hors du coffre 1 à 3 étalons à jet de césium et leur batterie ;
                                   MESURE le déplacement (S/B 3 à 10 par aller-retour de 48 h).

Statut des valeurs : « vérifié C » = fiche constructeur relue par l'Équipe C (04_ingenierie/REFERENCES.md) ;
« résumé vérifié » = chiffre lu dans le résumé d'un article vérifié par API ; « estimation » = ordre de
grandeur de notre part (prix 2026 indicatifs, masses et encombrements typiques) — à confirmer sur devis.

Sorties : ../nomenclature_R1.csv, resultats/i02_bilans_R1.json, resultats/i02_bilans_R1.txt,
          ../encombrement_selon_L.csv
"""
import itertools
import math

from i00_commun import (L_NOMINAL, L_PLAGE, MASSE_UNITE, RACINE, ecrire_csv, ecrire_json, ecrire_txt, geometrie_coffre)

# id, sous-système, désignation, élément d'origine remplacé, quantité, (dx, dy, dz) mm unitaire, masse unitaire kg,
# puissance unitaire W (mode mesure), puissance W (mode transport), coût unitaire € (estimation), origine, statut des valeurs, sécurité
NOMENCLATURE_A = [
    ("R1-01", "structure", "Coffre de transport à couvercle articulé, 0,85 × 0,26 × 0,24–0,29 m, platine supérieure découpée", "coffre (DOC-004/007)", 1, (850, 260, 285), 9.0, 0, 0, 600, "commerce", "estimation", "arrimage 4 points"),
    ("R1-02", "structure", "Châssis interne amorti (profilés aluminium, platine instruments)", "—", 1, (780, 200, 20), 4.0, 0, 0, 400, "atelier courant", "estimation", ""),
    ("R1-03", "énergie", "Batterie LiFePO4 4S 105 Ah (12,8 V ; 1,34 kWh), cellules prismatiques couchées, BMS", "batterie (DOC-008 r.12)", 1, (130, 200, 150), 9.5, 0, 0, 450, "commerce", "estimation", "très basse tension ; fusible, BMS, bac de rétention"),
    ("R1-04", "énergie", "Convertisseurs DC/DC isolés, barres de distribution, fusibles", "générateur / régulateur / collecteur d'injection d'électrons (r.4-5-6)", 1, (70, 180, 60), 1.2, 4.0, 2.0, 300, "commerce", "estimation", "distribution ≤ 24 V ; aucun faisceau d'électrons libre ; seule tension supérieure dans le coffre : ≈ 30 V de polarisation des photodétecteurs au silicium (R1-14, R1-18), produite localement sous quelques microampères"),
    ("R1-05", "sécurité", "Coupe-batterie, relais de sécurité à double canal, bouton d'arrêt d'urgence", "coupure d'urgence (DOC-007 r.5), interrupteur général (r.6)", 1, (70, 120, 50), 0.6, 1.0, 1.0, 250, "commerce", "estimation", "arrêt de catégorie 0 : état sûr réel (tout hors tension)"),
    ("R1-06", "temps", "Horloge atomique miniature au césium (CSAC SA.45s)", "4 horloges au césium (texte)", 4, (41, 36, 12), 0.035, 0.12, 0.12, 6000, "commerce", "masse, puissance, 3e-10 à 1 s : vérifié C ; prix : estimation", ""),
    ("R1-07", "temps", "Carte porteuse, comparateur de phase à 6 voies (résolution < 0,1 ns), distribution 10 MHz / 1 PPS", "—", 1, (140, 120, 25), 0.5, 5.0, 5.0, 3000, "laboratoire courant", "estimation", ""),
    ("R1-08", "temps", "Récepteur GNSS bifréquence à sortie de temps + antenne (référence et navigation)", "—", 1, (100, 60, 25), 0.3, 2.0, 2.0, 1500, "commerce", "estimation", ""),
    ("R1-09", "temps", "Enceinte des horloges : blindage mu-métal 2 couches, bobines de compensation 3 axes (basse tension), régulation thermique à effet Peltier", "logement et bobines de champ magnétique (r.1-2), générateur/régulateur de champ (r.3)", 1, (140, 140, 80), 1.5, 8.0, 6.0, 1200, "laboratoire courant", "estimation", "champ < 1 mT ; aucun aimant permanent fort"),
    ("R1-10", "calcul", "Calculateur embarqué (3 architectures différentes : ARM, x86, microcontrôleur)", "3 calculateurs à vote (texte)", 3, (100, 18, 75), 0.25, 5.0, 2.0, 250, "commerce", "estimation", ""),
    ("R1-11", "calcul", "Voteur médian matériel, chien de garde, enregistrement chaîné par empreinte", "vote « Borda » (texte)", 1, (100, 60, 20), 0.3, 2.0, 2.0, 500, "laboratoire courant", "estimation", ""),
    ("R1-12", "gravité", "Triade d'accéléromètres pendulaires à quartz + numériseur 24 bits (« VGL » de classe milligal)", "capteurs de gravité VGL (r.11)", 1, (60, 60, 60), 0.5, 2.0, 0.5, 9000, "commerce", "estimation", ""),
    ("R1-13", "gravité", "Baromètre de précision, thermomètres, hygromètre, magnétomètre 3 axes", "—", 1, (60, 40, 25), 0.3, 1.0, 0.5, 1500, "commerce", "estimation", ""),
    ("R1-14", "logement principal", "Télescope à muons cosmiques : 2 tuiles scintillantes 50 × 50 × 10 mm à photomultiplicateurs au silicium, coïncidence", "singularité principale (DOC-007 r.1) ; « évent à rayons X » (DOC-009 r.5)", 1, (60, 60, 120), 0.45, 0.6, 0.6, 450, "commerce / kit", "matériel < 100 $ par détecteur : résumé vérifié (Axani et al. 2018) ; reste : estimation", "polarisation ≈ 30 V sous quelques microampères, produite sur la carte ; aucune source radioactive"),
    ("R1-15", "logement de direction", "Gyromètre Sagnac à fibre optique : bobine 500 m sur Ø 70 mm, source fibrée 1 550 nm de classe 1, coupleur, modulateur, détection", "singularité de direction (DOC-007 r.2)", 1, (80, 80, 60), 0.6, 3.0, 0.0, 2500, "laboratoire courant", "estimation", "laser de classe 1 entièrement fibré"),
    ("R1-16", "logements", "Électronique de proximité des deux logements (2 cartes)", "générateurs / régulateurs de champ (r.3), capteur de singularité (r.7)", 2, (55, 75, 30), 0.15, 1.0, 0.3, 300, "laboratoire courant", "estimation", ""),
    ("R1-17", "thermique", "Boucle thermique : micro-pompe 12 V, 2 réservoirs tampons 0,25 L, plaque froide, échangeur et ventilateur (évent d'air tiède)", "enveloppe, pompe et réservoirs de refroidissement (r.8-9-10)", 1, (70, 200, 130), 1.6, 6.0, 3.0, 350, "commerce", "estimation", "eau glycolée 0,5 L ; bac de rétention"),
    # Correction post-validation I-2 : le tube Geiger-Müller (polarisé en interne à plusieurs centaines de volts) est remplacé par un
    # dosimètre à semi-conducteur, pour que « aucune tension supérieure à 30 V » soit vrai sans exception.
    ("R1-18", "rayonnement", "Dosimètre à semi-conducteur du rayonnement ambiant (diode PIN au silicium + enregistreur), sans source", "« évent à rayons X » (DOC-009 r.5)", 1, (110, 60, 30), 0.3, 0.3, 0.3, 500, "commerce", "estimation", "mesure du fond naturel uniquement ; polarisation ≤ 30 V (pas de tube Geiger-Müller) ; statistique plus lente qu'un tube (de l'ordre de l'heure pour 10 %, estimation)"),
    ("R1-19", "commande", "Télécommande filaire (écran, clavier 4 × 4, bus CAN)", "télécommande (DOC-007 r.3)", 1, (82, 86, 35), 0.4, 2.0, 0.0, 300, "commerce", "estimation", ""),
    ("R1-20", "commande", "Pupitre : écran de secours, voyants, avertisseur sonore, électronique de façade", "écran de secours (r.4), commandes d'urgence (r.8)", 1, (100, 80, 30), 0.5, 3.0, 0.5, 300, "commerce", "estimation", ""),
    ("R1-21", "structure", "Câblage, connectique, visserie, mousses", "—", 1, (0, 0, 0), 3.0, 0, 0, 500, "commerce", "estimation", ""),
]
# Option du palier 1 : gravimètre de classe microgal (amovible)
OPTION_GRAVI = ("R1-22", "gravité (option)", "Gravimètre relatif de terrain de classe microgal (type CG-6), amovible", "capteurs de gravité VGL (r.11)", 1, (215, 210, 240), 5.5, 5.2, 0.0, 100000, "commerce", "masse, puissance, écart-type < 5 µGal : vérifié C ; encombrement et prix : estimation", "posé au sol pour la mesure, véhicule à l'arrêt")
# Module externe de la configuration R1-B
MODULE_B = [
    ("R1-B1", "temps (module externe)", "Étalon de fréquence à jet de césium (type 5071A, tube haute performance)", "4 horloges au césium (texte)", 3, (425.5, 523.9, 133.4), 30.0, 50.0, 50.0, 80000, "commerce", "dimensions, masse, puissance : vérifié C ; prix : estimation", ""),
    ("R1-B2", "énergie (module externe)", "Batterie LiFePO4 7,5 kWh (autonomie 48 h de 3 étalons)", "batterie (r.12)", 1, (600, 400, 250), 55.0, 0, 0, 3500, "commerce", "estimation", "BMS, fusibles, ventilation"),
    ("R1-B3", "structure (module externe)", "Baie antichoc 19 pouces (0,6 × 0,8 × 0,95 m) et arrimage", "—", 1, (600, 800, 950), 20.0, 0, 0, 1500, "commerce", "estimation", ""),
]
# Correction post-validation I-3 : l'essai T6 compare 3 étalons emportés à une RÉFÉRENCE restée au sol, qu'il faut chiffrer.
REFERENCE_SOL = [
    ("R1-B4", "temps (station de référence au sol, hors véhicule)", "Étalon de fréquence à jet de césium de RÉFÉRENCE, resté au point de départ (essai T6, option a)", "—", 3, (425.5, 523.9, 133.4), 30.0, 50.0, 50.0, 80000, "commerce", "dimensions, masse, puissance : vérifié C ; prix : estimation", "sur secteur, en local tempéré"),
]
VARIANTE_LIEN = ("R1-B5", "temps (variante de R1-B4)", "VARIANTE de R1-B4 : lien de temps par GNSS vers une échelle de temps de laboratoire, 2 récepteurs étalonnés (essai T6, option b) — non additionnée", "—", 1, (0, 0, 0), 4.0, 20.0, 20.0, 15000, "commerce + accord avec un laboratoire de temps", "estimation ; bruit du lien 0,2 à 1 ns par comparaison : estimation non vérifiée", "")
ENTETES = ["id", "sous_systeme", "designation", "element_C204_remplace", "quantite", "dimensions_unitaires_mm", "masse_unitaire_kg", "masse_totale_kg",
           "puissance_mesure_W", "puissance_transport_W", "cout_unitaire_EUR_estimation", "cout_total_EUR_estimation", "origine", "statut_des_valeurs", "securite"]

H_CONV = 8.5       # W/m²/K : convection naturelle + rayonnement, valeur centrale (plage 7–10, cohérente avec la fiche F4 de l'Équipe C)
T_AMB = 20.0
RENDEMENT_BATT = 0.90
TAUX_REMPLISSAGE_MAX = 0.60   # fraction du volume intérieur réellement utilisable (accès, câbles, fixations) [HYP]


def totaux(items):
    m = sum(q * mu for (_i, _s, _d, _o, q, _dim, mu, *_r) in items)
    pm = sum(it[4] * it[7] for it in items)
    pt = sum(it[4] * it[8] for it in items)
    co = sum(it[4] * it[9] for it in items)
    vol = sum(it[4] * it[5][0] * it[5][1] * it[5][2] * 1e-9 for it in items)
    return m, pm, pt, co, vol


def tient(dim, boite):
    """Vrai si le parallélépipède dim (mm) entre dans la boîte (m) dans une orientation parallèle aux axes."""
    d = [x / 1000 for x in dim]
    return any(all(a <= b + 1e-9 for a, b in zip(perm, boite)) for perm in itertools.permutations(d))


def main():
    L = ["i02 — NOMENCLATURE ET BILANS DU PALIER 1 (C204-R1)", "=" * 100]
    lignes = []
    for it in NOMENCLATURE_A + [OPTION_GRAVI] + MODULE_B + REFERENCE_SOL + [VARIANTE_LIEN]:
        i, s, d, o, q, dim, mu, pm, pt, co, orig, stat, secu = it
        lignes.append([i, s, d, o, q, "×".join(str(x) for x in dim) if any(dim) else "—", mu, round(q * mu, 3), round(q * pm, 2), round(q * pt, 2), co, q * co, orig, stat, secu])
    ecrire_csv(RACINE / "nomenclature_R1.csv", ENTETES, lignes)

    # hors coffre lui-même, châssis (fait sur mesure : il suit L) et télécommande (rangée dans la baie 9)
    internes = [it for it in NOMENCLATURE_A if it[0] not in ("R1-01", "R1-02", "R1-19")]
    mA, pmA, ptA, coA, _ = totaux(NOMENCLATURE_A)
    _, _, _, _, volA = totaux(internes)
    mG, pmG, _, coG, _ = totaux([OPTION_GRAVI])
    mB, pmB, ptB, coB, _ = totaux(MODULE_B)
    volB = 0.6 * 0.8 * 0.95      # la baie contient les étalons et la batterie
    E_batt = 1340.0   # Wh
    res = {"R1-A": dict(masse_kg=mA, puissance_mesure_W=pmA, puissance_transport_W=ptA, cout_EUR=coA, volume_composants_L=volA * 1000,
                        autonomie_mesure_h=E_batt * RENDEMENT_BATT / pmA, autonomie_transport_h=E_batt * RENDEMENT_BATT / ptA),
           "option_gravimetre": dict(masse_kg=mG, cout_EUR=coG),
           "module_B": dict(masse_kg=mB, puissance_W=pmB, cout_EUR=coB, volume_L=volB * 1000,
                            autonomie_h=7500 * RENDEMENT_BATT / pmB),
           "R1-B_total": dict(masse_kg=mA + mG + mB, cout_EUR=coA + coG + coB, ecart_a_227kg=MASSE_UNITE - (mA + mG + mB))}
    mR, pR, _, coR, _ = totaux(REFERENCE_SOL)
    res["reference_au_sol_T6"] = dict(masse_hors_vehicule_kg=mR, puissance_W=pR, cout_EUR=coR)
    res["R1-B_avec_reference_au_sol"] = dict(masse_embarquee_kg=mA + mG + mB, masse_au_sol_kg=mR, cout_EUR=coA + coG + coB + coR)
    res["R1-B_avec_lien_de_temps"] = dict(masse_embarquee_kg=mA + mG + mB + VARIANTE_LIEN[6], cout_EUR=coA + coG + coB + VARIANTE_LIEN[9])
    L.append("R1-A (coffre seul)   : masse %.1f kg ; puissance %.0f W (mesure) / %.0f W (transport) ; coût ≈ %.0f k€ (estimation)"
             % (mA, pmA, ptA, coA / 1000))
    L.append("                       autonomie %.0f h (mesure) / %.0f h (transport) sur 1,34 kWh ; volume des composants %.1f L"
             % (res["R1-A"]["autonomie_mesure_h"], res["R1-A"]["autonomie_transport_h"], volA * 1000))
    L.append("Option gravimètre µGal : + %.1f kg ; + %.0f k€" % (mG, coG / 1000))
    L.append("Module B (3 césiums) : %.0f kg ; %.0f W ; %.0f L ; autonomie %.0f h sur 7,5 kWh ; ≈ %.0f k€"
             % (mB, pmB, volB * 1000, res["module_B"]["autonomie_h"], coB / 1000))
    L.append("R1-B complet         : %.0f kg (revendiqué pour la C204 : 227 kg ; écart %.0f kg) ; ≈ %.0f k€"
             % (mA + mG + mB, MASSE_UNITE - (mA + mG + mB), (coA + coG + coB) / 1000))
    L.append("Référence au sol de l'essai T6 (3 étalons, hors véhicule) : + %.0f kg au sol ; + %.0f k€ → R1-B complet avec sa référence : ≈ %.0f k€"
             % (mR, coR / 1000, res["R1-B_avec_reference_au_sol"]["cout_EUR"] / 1000))
    L.append("   variante : lien de temps GNSS étalonné à la place des 3 étalons de référence : ≈ %.0f k€ au total (estimation)"
             % (res["R1-B_avec_lien_de_temps"]["cout_EUR"] / 1000))
    L.append("  → un chronomètre relativiste RÉEL à étalons de césium, autonome 48 h, pèse l'ordre de grandeur des « 500 livres » annoncées,")
    L.append("    mais il n'entre pas dans le coffre (voir l'encombrement ci-dessous). Coïncidence d'ordre de grandeur, sans valeur probante.")

    # Bilan de masse par sous-système
    par_ss = {}
    for it in NOMENCLATURE_A:
        par_ss.setdefault(it[1], [0.0, 0.0])
        par_ss[it[1]][0] += it[4] * it[6]
        par_ss[it[1]][1] += it[4] * it[7]
    L.append("")
    L.append("Bilan R1-A par sous-système :")
    for k, (m, p) in par_ss.items():
        L.append("   %-24s %6.2f kg  %6.1f W" % (k, m, p))
    res["R1-A"]["par_sous_systeme"] = {k: dict(masse_kg=v[0], puissance_W=v[1]) for k, v in par_ss.items()}

    # Thermique
    L.append("")
    L.append("Bilan thermique (convection naturelle + rayonnement, h = %.1f W/m²/K, 5 faces libres, ambiance %.0f °C) :" % (H_CONV, T_AMB))
    res["thermique"] = {}
    for src in ("E", "A"):
        g = geometrie_coffre(L_NOMINAL, src)
        S5 = g["surface_ext"] - g["L"] * g["P"]
        for nom, P in (("R1-A mesure", pmA), ("R1-A transport", ptA)):
            dT = P / (H_CONV * S5)
            res["thermique"][f"{nom} (géométrie {src})"] = dict(surface_m2=S5, puissance_W=P, echauffement_K=dT, temperature_C=T_AMB + dT)
            L.append("   géométrie %s, %-15s : %.2f m², %.0f W → +%.1f K, soit %.1f °C" % (src, nom, S5, P, dT, T_AMB + dT))
        # Puissance qui donnerait les « 100 à 120 °F » revendiqués (38–49 °C)
        P38, P49 = H_CONV * S5 * (37.8 - T_AMB), H_CONV * S5 * (48.9 - T_AMB)
        res["thermique"][f"puissance_pour_38_49C (géométrie {src})"] = [P38, P49]
        L.append("   géométrie %s : la température revendiquée (38–49 °C) correspondrait à %.0f–%.0f W dissipés" % (src, P38, P49))
    # Module B : baie 0,6 × 0,8 × 0,95 m
    S5b = 2 * (0.6 * 0.95 + 0.8 * 0.95) + 0.6 * 0.8
    dTb = pmB / (H_CONV * S5b)
    res["thermique"]["module_B"] = dict(surface_m2=S5b, puissance_W=pmB, echauffement_K=dTb)
    L.append("   module B (baie 0,6 × 0,8 × 0,95 m) : %.2f m², %.0f W → +%.1f K" % (S5b, pmB, dTb))

    # Encombrement selon L
    L.append("")
    L.append("ENCOMBREMENT SELON LA LONGUEUR L DU COFFRE (rapports de forme : E = modèle 3D de l'Équipe E ; A = Équipe A)")
    L.append("%5s %3s | %6s %6s %6s %6s | %7s | %6s | %-9s %-9s %-11s %-10s %-9s" %
             ("L", "src", "P_int", "H_ss_p", "H_fermé", "Ø log.", "V_int L", "occup.", "R1-A", "CG-6", "Cs 5071A", "baie 19\"", "batt 2×"))
    enc_csv, res["encombrement"] = [], {}
    for Lg in L_PLAGE:
        for src in ("E", "A"):
            g = geometrie_coffre(Lg, src)
            boite = (g["L_int"], g["P_int"], g["H_int_sous_platine"])
            boite_f = (g["L_int"], g["P_int"], g["H_int_ferme"])
            non = [it[0] for it in internes if any(it[5]) and not tient(it[5], boite)]
            occ = volA / g["V_int"]
            okA = (not non) and occ <= TAUX_REMPLISSAGE_MAX
            ok_cg6 = tient(OPTION_GRAVI[5], boite_f) and (volA + 0.0108) / g["V_int"] <= TAUX_REMPLISSAGE_MAX + 0.15 and \
                OPTION_GRAVI[5][2] / 1000 <= g["H_int_ferme"]
            ok_cs = tient(MODULE_B[0][5], boite_f)
            ok_19 = tient((430, 450, 133), boite_f)       # tiroir de baie 19 pouces 3U le plus court [estimation]
            ok_2b = (volA + 0.0039) / g["V_int"] <= TAUX_REMPLISSAGE_MAX
            res["encombrement"][f"L={Lg:.2f} ({src})"] = dict(g, occupation=occ, R1A_tient=okA, pieces_trop_grandes=non, CG6_tient=ok_cg6,
                                                               cesium_tient=ok_cs, tiroir_19p_tient=ok_19, deuxieme_batterie=ok_2b)
            o = lambda b: "oui" if b else "NON"
            L.append("%5.2f %3s | %6.3f %6.3f %6.3f %6.3f | %7.1f | %5.0f%% | %-9s %-9s %-11s %-10s %-9s" %
                     (Lg, src, g["P_int"], g["H_int_sous_platine"], g["H_int_ferme"], g["d_logement"], g["V_int"] * 1000, occ * 100,
                      o(okA) + ("" if not non else " (" + ",".join(non) + ")"), o(ok_cg6), o(ok_cs), o(ok_19), o(ok_2b)))
            enc_csv.append([f"{Lg:.2f}", src, f"{g['P']:.3f}", f"{g['H_ferme']:.3f}", f"{g['L_int']:.3f}", f"{g['P_int']:.3f}", f"{g['H_int_sous_platine']:.3f}",
                            f"{g['H_int_ferme']:.3f}", f"{g['d_logement'] * 1000:.0f}", f"{g['entraxe_logements'] * 1000:.0f}", f"{g['V_ext'] * 1000:.1f}",
                            f"{g['V_int'] * 1000:.1f}", f"{occ * 100:.0f}", o(okA), ";".join(non), o(ok_cg6), o(ok_cs), o(ok_19), o(ok_2b),
                            f"{MASSE_UNITE / g['V_ext']:.0f}"])
    ecrire_csv(RACINE / "encombrement_selon_L.csv",
               ["L_m", "rapports_de_forme", "P_ext_m", "H_fermee_m", "L_int_m", "P_int_m", "H_int_sous_platine_m", "H_int_couvercle_ferme_m",
                "diametre_logement_mm", "entraxe_logements_mm", "volume_ext_L", "volume_int_L", "occupation_R1A_pct", "R1A_tient",
                "pieces_trop_grandes", "gravimetre_CG6_tient", "cesium_5071A_tient", "tiroir_19_pouces_tient", "deuxieme_batterie_possible",
                "masse_volumique_si_227kg_kg_m3"], enc_csv)
    # Longueur minimale pour chaque élément critique (géométrie E)
    def L_min(test):
        for k in range(400, 2001):
            Lg = k / 1000
            if test(geometrie_coffre(Lg, "E")):
                return Lg
        return None
    lmin = {
        "R1-A complet (toutes pièces + occupation ≤ 60 %)": L_min(lambda g: all(tient(it[5], (g["L_int"], g["P_int"], g["H_int_sous_platine"])) for it in internes if any(it[5])) and volA / g["V_int"] <= TAUX_REMPLISSAGE_MAX),
        "gravimètre de classe CG-6 debout, couvercle fermé": L_min(lambda g: tient(OPTION_GRAVI[5], (g["L_int"], g["P_int"], g["H_int_ferme"])) and 0.240 <= g["H_int_ferme"]),
        "étalon à jet de césium 5071A": L_min(lambda g: tient(MODULE_B[0][5], (g["L_int"], g["P_int"], g["H_int_ferme"]))),
        "tiroir de baie 19 pouces (430 × 450 × 133 mm)": L_min(lambda g: tient((430, 450, 133), (g["L_int"], g["P_int"], g["H_int_ferme"]))),
    }
    res["L_minimale_m (géométrie E)"] = lmin
    L.append("")
    L.append("Longueur minimale du coffre (rapports de forme de l'Équipe E) pour loger :")
    for k, v in lmin.items():
        L.append("   %-55s L ≥ %s m" % (k, ("%.2f" % v) if v else "> 2,00"))
    L.append("  → dans toute la plage plausible 0,60–1,20 m, AUCUN étalon à césium en baie 19 pouces n'entre dans le coffre :")
    L.append("    la conclusion « le coffre seul ne peut pas mesurer son propre déplacement temporel » ne dépend pas de l'échelle.")
    ecrire_json("i02_bilans_R1.json", res)
    ecrire_txt("i02_bilans_R1.txt", L)


if __name__ == "__main__":
    main()
