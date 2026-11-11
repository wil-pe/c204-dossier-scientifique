#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i12 : données du guide de construction, parties B (« C204-R1 Lite ») et C (C204-R1 complet).

  nomenclature_R1_Lite.csv            nomenclature d'initiation, avec fourchette de prix (ESTIMATIONS 2026, non vérifiées sur devis)
  guide/implantation_R1.csv           position et encombrement de chaque sous-ensemble dans le coffre (tirés de modele_c204_R1.json)
  guide/protections_R1.csv            départs électriques : puissance, courant, fusible, section de câble
  guide/synthese_constructions.csv    coût, durée et niveau des trois constructions
  schemas/cablage_distribution_R1.svg schéma de câblage et de distribution du palier R1 (très basse tension)
  schemas/synoptique_R1_Lite.svg      synoptique de la version d'initiation

Tout ce qui est prix, masse ou performance est une ESTIMATION ; rien n'a été construit ni essayé par l'Équipe I.
"""
import csv
import json
import math

from i00_commun import RACINE, RES, SCH, ecrire_csv, ecrire_json, ecrire_txt
from i09_schemas_svg import Svg, fv

GUIDE = RACINE / "guide"
GUIDE.mkdir(exist_ok=True)

# id, sous-ensemble, désignation, élément C204 correspondant, quantité, prix unitaire bas €, prix unitaire haut €, tension, remarque
LITE = [
    ("L-01", "temps", "Récepteur GNSS à sortie 1 PPS (module à monter) + antenne active", "horloges", 1, 20, 45, "3,3–5 V", "référence de temps et de position ; le PPS est asservi au temps GNSS : il ne « voit » pas le décalage du porteur"),
    ("L-02", "temps", "Oscillateur à quartz compensé en température, sortie 1 Hz / 32 kHz (module d'horloge temps réel de précision)", "horloges", 2, 4, 10, "3,3 V", "±2 ppm typiquement (estimation) : deux « horloges » locales à comparer"),
    ("L-03", "temps", "Oscillateur thermostaté 10 MHz d'occasion (optionnel)", "horloges", 1, 15, 40, "5–12 V", "troisième référence, plus stable (10⁻⁹ à 10⁻¹⁰ sur une seconde, estimation)"),
    ("L-04", "calcul", "Microcontrôleur n° 1 (famille A, par exemple à cœur ARM Cortex-M0+)", "3 calculateurs à vote", 1, 5, 10, "3,3 V", "trois familles différentes pour éviter la panne de mode commun"),
    ("L-05", "calcul", "Microcontrôleur n° 2 (famille B, par exemple à cœur Xtensa ou RISC-V avec Wi-Fi coupé)", "3 calculateurs à vote", 1, 6, 12, "3,3 V", ""),
    ("L-06", "calcul", "Microcontrôleur n° 3 (famille C, par exemple à cœur AVR ou ARM Cortex-M3)", "3 calculateurs à vote", 1, 5, 25, "5 V ou 3,3 V", ""),
    ("L-07", "calcul", "Nano-ordinateur à carte unique (voteur logiciel, enregistrement, affichage) + carte mémoire", "voteur, pupitre", 1, 25, 60, "5 V", "exécute logiciel/voteur.py et decalage_relativiste.py"),
    ("L-08", "capteurs", "Centrale inertielle à microsystèmes (accéléromètre + gyromètre 3 axes)", "capteurs de gravité, singularité de direction", 1, 5, 20, "3,3 V", "pesanteur à ~10⁻³ m/s² au mieux : aucune gravimétrie fine"),
    ("L-09", "capteurs", "Baromètre numérique (altitude à ~1 m près en relatif)", "capteurs de gravité", 1, 4, 12, "3,3 V", "altitude pour le calcul du décalage"),
    ("L-10", "muons", "Détecteur de muons : scintillateur plastique 5 × 5 × 1 cm + photomultiplicateur au silicium + carte de mise en forme", "singularité principale, « évent »", 2, 90, 160, "5 V (≈ 30 V produits sur la carte)", "le résumé d'Axani et al. (2018) annonce moins de 100 $ de matériel par détecteur ; prix 2026 non vérifiés ; deux détecteurs pour la coïncidence"),
    ("L-11", "affichage", "Afficheur OLED ou LCD, 3 boutons, 3 voyants, avertisseur sonore", "pupitre, écran de secours", 1, 10, 25, "3,3–5 V", ""),
    ("L-12", "énergie", "Batterie externe USB 5 V, 10 à 20 Ah, protégée", "batterie", 1, 20, 40, "5 V", "aucune cellule nue : la protection est intégrée"),
    ("L-13", "énergie", "Interrupteur général, fusible 3 A sous porte-fusible, répartiteur 5 V", "arrêt d'urgence, distribution", 1, 8, 15, "5 V", ""),
    ("L-14", "structure", "Boîtier ou réplique A, platine de montage, entretoises", "coffre", 1, 15, 40, "—", "hors réplique complète (voir partie A)"),
    ("L-15", "câblage", "Plaques d'essai ou circuit imprimé, connecteurs, fils, câble coaxial court pour le PPS", "—", 1, 25, 50, "—", ""),
]

RENDEMENT_CONV = 0.85
U_BATT = 12.8
# départs du palier R1 : (repère, désignation, lignes de nomenclature alimentées, tension du rail)
DEPARTS = [
    ("F1", "Calculateurs ×3, voteur, GNSS", ("R1-10", "R1-11", "R1-08"), "5 V"),
    ("F2", "Horloges ×4 et comparateur de phase (rail bas bruit)", ("R1-06", "R1-07"), "3,3 V / 5 V"),
    ("F3", "Enceinte des horloges (Peltier, bobines de compensation)", ("R1-09",), "12 V"),
    ("F4", "Boucle thermique : pompe, ventilateur", ("R1-17",), "12 V"),
    ("F5", "Logements : télescope à muons, gyromètre, cartes de proximité", ("R1-14", "R1-15", "R1-16"), "5 V"),
    ("F6", "Capteurs : accéléromètres, ambiance, dosimètre", ("R1-12", "R1-13", "R1-18"), "5 V"),
    ("F7", "Pupitre et télécommande", ("R1-19", "R1-20"), "12 V / 5 V"),
    ("F8", "Sécurité et distribution (pertes, relais)", ("R1-04", "R1-05"), "12 V"),
]
CALIBRES = [0.5, 1, 2, 3, 5, 7.5, 10, 15, 20]


def calibre(i):
    """Calibre normalisé immédiatement supérieur à 1,6 fois le courant nominal (marge d'appel de courant)."""
    return next(c for c in CALIBRES if c >= 1.6 * i)


def section(c):
    return 0.5 if c <= 3 else (0.75 if c <= 5 else (1.5 if c <= 10 else 2.5))


def main():
    L = ["i12 — DONNÉES DU GUIDE : VERSION LITE, IMPLANTATION ET CÂBLAGE DU PALIER R1", "=" * 95]
    # ------------------------------------------------------------------ nomenclature Lite
    lignes, bas, haut = [], 0.0, 0.0
    par_ss = {}
    for (i, ss, d, o, q, pb, ph, u, rem) in LITE:
        lignes.append([i, ss, d, o, q, pb, ph, q * pb, q * ph, u, "estimation 2026, non vérifiée sur devis", rem])
        bas += q * pb; haut += q * ph
        par_ss.setdefault(ss, [0, 0]); par_ss[ss][0] += q * pb; par_ss[ss][1] += q * ph
    ecrire_csv(RACINE / "nomenclature_R1_Lite.csv",
               ["id", "sous_ensemble", "designation", "element_C204_correspondant", "quantite", "prix_unitaire_bas_EUR", "prix_unitaire_haut_EUR",
                "total_bas_EUR", "total_haut_EUR", "tension", "statut_des_prix", "remarque"], lignes)
    sans_muons = (bas - 2 * 90, haut - 2 * 160)
    un_muon = (bas - 90, haut - 160)
    L.append("C204-R1 Lite : %.0f à %.0f € avec deux détecteurs de muons ; %.0f à %.0f € avec un seul ; %.0f à %.0f € sans détecteur de muons (estimations)"
             % (bas, haut, un_muon[0], un_muon[1], sans_muons[0], sans_muons[1]))
    for k, (b_, h_) in par_ss.items():
        L.append("   %-10s %4.0f à %4.0f €" % (k, b_, h_))
    # consommation de la version Lite (estimations) : nano-ordinateur 2,5 W, 3 microcontrôleurs 0,6 W, GNSS 0,2 W, muons 2 × 0,3 W, divers 0,6 W
    p_lite = 2.5 + 0.6 + 0.2 + 0.6 + 0.6
    auto = 10 * 5 * 0.8 / p_lite            # batterie 10 Ah sous 5 V, rendement 0,8
    L.append("   consommation ≈ %.1f W (estimation) → ≈ %.0f h sur une batterie USB de 10 Ah" % (p_lite, auto))

    # ------------------------------------------------------------------ implantation R1 (depuis le modèle 3D)
    modele = json.loads((RACINE / "modele_c204_R1.json").read_text(encoding="utf-8"))
    impl = []
    for p in modele["variantes"]["R1A"]["pieces"]:
        if p["couche"] != "interne":
            continue
        pr = p["primitive"]
        if pr["type"] == "boite":
            dims = pr["dimensions"]
        elif pr["type"] == "cylindre":
            dims = [2 * pr["rayon"], 2 * pr["rayon"], pr["hauteur"]]
        elif pr["type"] == "tore":
            d_ = 2 * (pr["rayon_majeur"] + pr["rayon_mineur"])
            dims = [d_, d_, 2 * pr["rayon_mineur"]]
        else:
            dims = [0, 0, 0]
        x, y, z = p["position"]
        impl.append([p["repere"], p["nom"], p["ensemble"], round(x * 1000), round(y * 1000), round(z * 1000), round(dims[0] * 1000), round(dims[1] * 1000), round(dims[2] * 1000),
                     round((z - dims[2] / 2) * 1000), "dans une enceinte" if p.get("contenu") else ""])
    impl.sort(key=lambda r: (r[3], r[4]))
    ecrire_csv(GUIDE / "implantation_R1.csv",
               ["repere_nomenclature", "piece", "sous_ensemble", "x_centre_mm", "y_centre_mm", "z_centre_mm", "dx_mm", "dy_mm", "dz_mm", "z_dessous_mm", "remarque"], impl)
    L.append("Implantation R1 : %d pièces internes exportées (origine : coin avant-gauche-bas du corps ; x longueur, y profondeur vers la charnière, z hauteur)" % len(impl))

    # ------------------------------------------------------------------ protections R1
    nomen = {r["id"]: r for r in csv.DictReader(open(RACINE / "nomenclature_R1.csv", encoding="utf-8"))}
    prot, ptot = [], 0.0
    for rep_, des, ids, rail in DEPARTS:
        p_w = sum(float(nomen[i]["puissance_mesure_W"]) for i in ids)
        i_a = p_w / RENDEMENT_CONV / U_BATT
        cal = calibre(i_a)
        prot.append([rep_, des, "+".join(ids), rail, f"{p_w:.1f}", f"{i_a:.2f}", cal, section(cal)])
        ptot += p_w
    i_tot = ptot / RENDEMENT_CONV / U_BATT
    f0 = calibre(i_tot)
    prot.insert(0, ["F0", "Fusible général, à moins de 15 cm de la borne + de la batterie (fort pouvoir de coupure)", "tout", "12,8 V", f"{ptot:.1f}", f"{i_tot:.2f}", f0, section(f0)])
    ecrire_csv(GUIDE / "protections_R1.csv",
               ["repere", "depart", "lignes_de_nomenclature", "rail", "puissance_W", "courant_cote_batterie_A", "calibre_fusible_A", "section_cuivre_mm2"], prot)
    L.append("Protections R1 : %.1f W au total → %.1f A côté batterie (rendement de conversion %.2f) ; fusible général %g A ; câble %g mm²"
             % (ptot, i_tot, RENDEMENT_CONV, f0, section(f0)))
    for r in prot[1:]:
        L.append("   %s %-62s %5s W  %5s A → fusible %g A, %g mm²" % (r[0], r[1][:62], r[4], r[5], r[6], r[7]))
    L.append("   Règle : calibre normalisé ≥ 1,6 × courant nominal ; sections indicatives (≤ 3 A : 0,5 mm² ; ≤ 10 A : 1,5 mm² ; au-delà : 2,5 mm²), à vérifier selon la norme applicable.")

    # ------------------------------------------------------------------ synthèse des trois constructions
    r2 = json.loads((RES / "i02_bilans_R1.json").read_text(encoding="utf-8"))
    r11 = json.loads((RES / "i11_replique.json").read_text(encoding="utf-8"))
    synth = [
        ["A", "Réplique inerte du coffre", "bricolage du bois, peinture", f"{r11['cout_bas_EUR']:.0f}", f"{r11['cout_haut_EUR']:.0f}", "15 à 25", "aucune fonction ; maquette de présentation", "≈ 6 à 8 kg"],
        ["B", "C204-R1 Lite", "électronique d'amateur, programmation", f"{bas:.0f}", f"{haut:.0f}", "40 à 80", "calcule et affiche le décalage relativiste du trajet ; compare des oscillateurs ; vote à trois voies ; compte des muons ; ne mesure aucun effet relativiste", "≈ 1 à 2 kg hors boîtier"],
        ["C", "C204-R1 complet (configuration A, coffre seul)", "électronique confirmée, mécanique, métrologie du temps", f"{r2['R1-A']['cout_EUR'] * 0.9:.0f}", f"{r2['R1-A']['cout_EUR'] * 1.3:.0f}",
         "300 à 600", "idem, avec quatre horloges atomiques miniatures, comparaison à mieux que 0,1 ns et gyromètre à fibre ; ne mesure toujours pas le décalage de son trajet", f"≈ {r2['R1-A']['masse_kg']:.0f} kg"],
    ]
    ecrire_csv(GUIDE / "synthese_constructions.csv", ["construction", "nom", "competences", "cout_bas_EUR_estimation", "cout_haut_EUR_estimation", "duree_h_estimation", "ce_que_fait_l_objet", "masse_estimation"], synth)
    L.append("Synthèse : A %.0f–%.0f € ; B %.0f–%.0f € ; C ≈ %.0f k€ (fourchette %.0f–%.0f k€), estimations" % (r11["cout_bas_EUR"], r11["cout_haut_EUR"], bas, haut, r2['R1-A']['cout_EUR'] / 1000, r2['R1-A']['cout_EUR'] * 0.9 / 1000, r2['R1-A']['cout_EUR'] * 1.3 / 1000))
    ecrire_json("i12_guide.json", dict(lite=dict(cout_bas=bas, cout_haut=haut, sans_muons=sans_muons, un_detecteur=un_muon, puissance_W=p_lite, autonomie_h=auto),
                                       protections=dict(puissance_totale_W=ptot, courant_A=i_tot, fusible_general_A=f0), synthese=synth))

    # ------------------------------------------------------------------ schéma de câblage R1
    s = Svg(1500, 900, "C204-R1 — câblage et distribution (très basse tension)",
            ["Une seule source (batterie 12,8 V), un fusible général au plus près de la borne +, un coupe-batterie, une chaîne d'arrêt d'urgence à double canal, puis des départs protégés un par un.",
             "Aucune tension supérieure à ≈ 30 V (polarisation des photodétecteurs, produite sur leur carte). Calibres : script i12, guide/protections_R1.csv. Estimations — rien n'a été construit."])
    s.boite("batt", 30, 120, 230, 100, "Batterie LiFePO4 12,8 V", ["4 éléments en série, 1,34 kWh", "BMS intégré (surcharge, décharge,", "court-circuit, température)", "dans un bac, loin des horloges"], "energie")
    s.boite("f0", 300, 135, 170, 70, f"F0 : fusible {f0:g} A", ["à < 15 cm de la borne +", "fort pouvoir de coupure"], "securite")
    s.boite("cb", 510, 135, 170, 70, "Coupe-batterie", ["manuel, accessible", "coffre fermé"], "securite")
    s.boite("rs", 720, 120, 230, 100, "Relais de sécurité (R1-05)", ["double canal, contacts guidés", "piloté par l'arrêt d'urgence du", "pupitre et de la télécommande ;", "réarmement manuel"], "securite")
    s.boite("barre", 990, 135, 200, 70, "Barre + 12 V protégée", [f"{ptot:.0f} W ; {fv(i_tot, 1)} A en mesure", "départs F1 à F8"], "energie")
    s.boite("masse", 1230, 120, 240, 100, "0 V : point de masse unique", ["retours en étoile sur une barre 0 V", "reliée au châssis en UN seul point ;", "blindages reliés côté source ;", "châssis relié au véhicule (tresse)"], "neutre")
    s.fleche("batt", "d", "f0", "g"); s.fleche("f0", "d", "cb", "g"); s.fleche("cb", "d", "rs", "g"); s.fleche("rs", "d", "barre", "g")
    y0 = 300
    cols = [("F1", 30), ("F2", 400), ("F3", 770), ("F4", 1140)]
    dep = {r[0]: r for r in prot}
    textes = {"F1": ["convertisseur 12 → 5 V", "3 calculateurs dissemblables,", "voteur, récepteur GNSS"], "F2": ["convertisseur bas bruit 12 → 5 / 3,3 V", "4 horloges au césium miniatures,", "comparateur de phase"],
              "F3": ["12 V direct", "régulation Peltier de l'enceinte,", "bobines de compensation (< 1 mT)"], "F4": ["12 V direct", "micro-pompe, ventilateur ;", "détecteur de fuite dans le bac"],
              "F5": ["convertisseur 12 → 5 V", "télescope à muons, gyromètre,", "cartes de proximité"], "F6": ["convertisseur 12 → 5 V", "accéléromètres, ambiance,", "dosimètre à semi-conducteur"],
              "F7": ["12 V et 5 V", "pupitre, télécommande (bus CAN),", "avertisseur"], "F8": ["12 V", "bobines du relais de sécurité,", "pertes des convertisseurs"]}
    for j, rep_ in enumerate(["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8"]):
        x = 30 + (j % 4) * 370
        y = y0 + (j // 4) * 150
        r = dep[rep_]
        s.boite(rep_, x, y, 330, 110, f"{rep_} : fusible {str(r[6]).replace('.', ',')} A — {r[4].replace('.', ',')} W ({r[5].replace('.', ',')} A)", textes[rep_] + [f"câble {str(r[7]).replace('.', ',')} mm²"],
                {"F1": "calcul", "F2": "temps", "F3": "temps", "F4": "thermique", "F5": "principal", "F6": "gravite", "F7": "securite", "F8": "securite"}[rep_])
    s.e.append(f'<line x1="1090" y1="205" x2="1090" y2="{y0 - 28}" stroke="#52514e" stroke-width="1.6"/>')
    s.e.append(f'<line x1="195" y1="{y0 - 28}" x2="1305" y2="{y0 - 28}" stroke="#52514e" stroke-width="1.6"/>')
    for j in range(4):
        x = 30 + j * 370 + 165
        s.e.append(f'<line x1="{x}" y1="{y0 - 28}" x2="{x}" y2="{y0}" stroke="#52514e" stroke-width="1.6"/>')
    s.texte(1100, y0 - 36, "distribution + 12 V (les départs F5 à F8 se raccordent à la même barre)", 11)
    # signaux
    ys = y0 + 330
    s.boite("sig1", 30, ys, 330, 150, "Signaux de temps (câble coaxial 50 Ω)", ["10 MHz et 1 PPS de chaque horloge → comparateur", "1 PPS du GNSS → comparateur et calculateurs", "longueurs égales à ±5 cm (0,25 ns)", "blindage relié à la masse côté source seulement", "aucun câble de puissance dans la même gaine"], "temps")
    s.boite("sig2", 400, ys, 330, 150, "Données", ["comparateur → 3 calculateurs : 3 liaisons série", "isolées (optocoupleurs) : pas de masse commune", "capteurs : un jeu par calculateur si possible,", "sinon bus partagé (mode commun à signaler)", "calculateurs → voteur → pupitre : bus CAN"], "calcul")
    s.boite("sig3", 770, ys, 330, 150, "Chaîne d'arrêt d'urgence (câblée)", ["2 boutons à accrochage en série (pupitre,", "télécommande), double contact à ouverture ;", "ouvre le relais de sécurité : tout hors tension", "sauf la batterie elle-même ; aucun logiciel", "dans la chaîne ; essai avant chaque sortie"], "securite")
    s.boite("sig4", 1140, ys, 330, 150, "Séparations", ["baie gauche : énergie ; centre : logements et", "boucle d'eau ; droite : temps et calcul ;", "eau et électronique jamais au même niveau ;", "pompe arrêtée pendant les mesures fines ;", "horloges à plus de 25 cm de la batterie"], "neutre")
    s.legende(30, 852, [("energie", "énergie"), ("securite", "sécurité")])
    s.legende(250, 852, [("temps", "temps"), ("calcul", "calcul")])
    s.legende(470, 852, [("thermique", "thermique"), ("gravite", "capteurs")])
    s.ecrire("cablage_distribution_R1.svg")

    # ------------------------------------------------------------------ synoptique Lite
    s = Svg(1300, 700, "C204-R1 Lite — synoptique de la version d'initiation",
            [f"≈ {bas:.0f} à {haut:.0f} € (estimation), 5 V uniquement. Elle CALCULE et affiche le décalage relativiste du trajet ; elle ne peut pas le mesurer (oscillateurs 10⁴ à 10⁷ fois trop instables).",
             "Même architecture que le palier R1 : plusieurs références de temps comparées, trois calculateurs à vote, capteurs, détecteur de muons. Rien n'a été construit par l'Équipe I."])
    s.boite("gnss", 30, 110, 280, 76, "Récepteur GNSS (L-01)", ["position, altitude, vitesse, cap ; 1 PPS", "(référence : temps GNSS, au géoïde)"], "temps")
    s.boite("osc", 30, 200, 280, 76, "2 à 3 oscillateurs locaux (L-02, L-03)", ["1 Hz / 10 MHz ; écarts au PPS mesurés", "par capture de minuterie (~10 à 100 ns)"], "temps")
    s.boite("imu", 30, 310, 280, 62, "Inertie, baromètre (L-08, L-09)", ["inclinaison, virages, altitude relative"], "gravite")
    s.boite("mu", 30, 400, 280, 90, "2 détecteurs de muons (L-10)", ["scintillateur + photomultiplicateur au", "silicium, superposés : coïncidences", "(quelques dizaines à centaines par heure)"], "principal")
    s.boite("c1", 400, 110, 250, 62, "Microcontrôleur 1 (L-04)", ["famille A — même calcul"], "calcul")
    s.boite("c2", 400, 190, 250, 62, "Microcontrôleur 2 (L-05)", ["famille B — même calcul"], "calcul")
    s.boite("c3", 400, 270, 250, 62, "Microcontrôleur 3 (L-06)", ["famille C — même calcul"], "calcul")
    s.boite("vote", 740, 150, 250, 110, "Voteur et journal (L-07)", ["vote médian sur les 3 voies,", "voie fautive signalée ;", "logiciel/voteur.py"], "calcul")
    s.boite("aff", 1040, 110, 230, 110, "Affichage (L-11)", ["décalage CALCULÉ du trajet", "(ns/h et cumul) ; écarts des", "oscillateurs ; taux de muons"], "sortie")
    s.boite("lim", 1040, 250, 230, 130, "Ce que Lite ne fait pas", ["mesurer le décalage (≈ 10⁻¹³) ;", "gravimétrie fine ; dater mieux", "que ~0,1 µs ; elle n'est la", "cause d'aucun décalage"], "contredit")
    s.boite("alim", 400, 520, 590, 70, "Alimentation 5 V (L-12, L-13)", ["batterie USB protégée → interrupteur → fusible 3 A → répartiteur", f"≈ {fv(p_lite, 1)} W ; ≈ {auto:.0f} h sur 10 Ah (estimation)"], "energie")
    for a in ("c1", "c2", "c3"):
        s.fleche(a, "d", "vote", "g")
    s.fleche("gnss", "d", "c1", "g", "", coude=[(355, 148), (355, 141)])
    s.fleche("osc", "d", "c2", "g", "", coude=[(355, 238), (355, 221)])
    s.fleche("imu", "d", "c3", "g", "", coude=[(355, 341), (355, 301)])
    s.fleche("mu", "d", "vote", "b", "comptage", coude=[(865, 445)], tb=0.5)
    s.fleche("vote", "d", "aff", "g", "", coude=[(1015, 205), (1015, 165)])
    s.texte(30, 630, "Chaque microcontrôleur reçoit les mêmes mesures (GNSS, oscillateurs, capteurs) et refait le même calcul : seule la flèche principale est tracée.", 11.5)
    s.texte(30, 650, "Sécurité : 5 V uniquement, batterie USB protégée, aucune cellule au lithium nue, aucune source radioactive, aucune haute tension accessible.", 11.5)
    s.ecrire("synoptique_R1_Lite.svg")
    L.append("Schémas écrits : schemas/cablage_distribution_R1.svg, schemas/synoptique_R1_Lite.svg")
    ecrire_txt("i12_guide.txt", L)


if __name__ == "__main__":
    main()
