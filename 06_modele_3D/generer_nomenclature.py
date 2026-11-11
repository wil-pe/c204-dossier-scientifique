#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — nomenclature des composants.

    modele_c204.json  ──►  NOMENCLATURE.md  +  nomenclature.csv

Le fichier Markdown croise les repères des documents (9 de DOC-007, 12 de DOC-008, 35 de DOC-005),
les six systèmes du texte et les éléments visibles sur les photos avec les pièces du modèle ; le CSV
liste toutes les pièces (variantes A et B) plus les éléments documentés mais NON modélisés.

Usage : python generer_nomenclature.py
"""
import csv
import json
from collections import OrderedDict, Counter
from pathlib import Path

ICI = Path(__file__).resolve().parent

DOC007 = [   # n°, légende d'origine, traduction, fragment d'ensemble ou de nom, remarque
    (1, "MAIN SINGULARITY", "Singularité principale", ["logement — singularité principale"],
     "Logement circulaire côté charnière (fy = 0,757 P) : collerette [DOC] et fût [DÉD], dans le cadre commun [DOC]. L'ensemble placé dessous (carter, enveloppe, bobines : 15 pièces [DÉD]) vient de DOC-008."),
    (2, "STEERING SINGULARITY", "Singularité de direction", ["logement — singularité de direction"],
     "Logement circulaire côté avant (fy = 0,401 P). Entraxe des deux logements : 0,356 P = 1,16 diamètre. Même remarque que pour le repère 1."),
    (3, "REMOTE CONTROL UNIT", "Télécommande", ["Télécommande —", "Cordon spiralé"],
     "Boîtier filaire [DOC] (épaisseur [HYP]) ; cordon [DÉD] : spiralé sur DOC-004 et les photos, trait simple sur DOC-007, tracé 3D déduit."),
    (4, "EMERGENCY VIEW SCREEN", "Écran de visualisation de secours", ["Écran de visualisation de secours (4)", "Platine — zone 4"],
     "Double trait étroit sur presque toute la profondeur : nature exacte indéterminée."),
    (5, "EMERGENCY DISCONNECT", "Coupure (déconnexion) d'urgence", ["Panneau 5", "Organe rond de coupure"],
     "Panneau blanc : fenêtre sombre à l'arrière, organe rond entre deux pavés hachurés à l'avant. Lueur rouge de DOC-002 à l'aplomb de la fenêtre [DÉD]."),
    (6, "MAIN UNIT ON/OFF SWITCH", "Interrupteur général marche/arrêt", ["Interrupteur général (6)"],
     "Boîtier carré contenant deux petits carrés, à l'avant du panneau 8."),
    (7, "UNIT CONTROL INSTRUCTIONS", "Instructions de commande de l'unité", ["Plaque d'instructions de commande (7)"],
     "Plaque à l'intérieur du couvercle (texte illisible sur toutes les copies)."),
    (8, "EMERGENCY CONTROLS", "Commandes d'urgence", ["Panneau 8", "Panneau 8/6"],
     "Plage blanche portant 18 pastilles (touches ou voyants) : 2 isolées + colonnes de 11 et de 5."),
    (9, "REMOTE STORAGE UNIT", "Logement de rangement de la télécommande", ["Rangement 9"],
     "Compartiment ouvert à l'extrémité droite ; profondeur [HYP]."),
]
DOC008 = [   # n°, légende (confiance moyenne), traduction, fragment de nom, remarque
    (1, "Singularity drive housing", "Carter d'entraînement de singularité", "Carter d'entraînement de singularité (1)",
     "2 carters sphériques ; position sous les logements de DOC-007 [DÉD]."),
    (2, "Singularity magnetic field coil", "Bobine de champ magnétique de singularité", "Bobine de champ magnétique (2)",
     "6 barres noires par carter, lues comme des spires coaxiales ; + 2 calottes d'extrémité par carter."),
    (3, "Magnetic field generator / regulator", "Générateur / régulateur de champ magnétique", "Générateur / régulateur de champ magnétique (3)",
     "2 boîtiers sous les carters, reliés aux bobines par des tirets."),
    (4, "Electron mass injector manifold", "Collecteur d'injection de masse d'électrons", "Collecteur d'injection (4)",
     "3 tubes par carter + rampe commune vers le régulateur 5."),
    (5, "Electron regulator", "Régulateur d'électrons", "Régulateur d'électrons (5)", "Entre les deux carters, en dessous."),
    (6, "Electron generator", "Générateur d'électrons", "Générateur d'électrons (6)", "Grand rectangle à bande noire ; emplacement [HYP]."),
    (7, "Singularity sensor booster", "Amplificateur de capteur de singularité", "Amplificateur de capteur de singularité (7)",
     "Petit carré gris incliné à 45° sur chaque carter."),
    (8, "Singularity cooling housing", "Enveloppe de refroidissement de singularité", "Enveloppe de refroidissement (8)",
     "Anneau noir entourant chaque carter ; rendu translucide."),
    (9, "Singularity cooling pump", "Pompe de refroidissement", "Pompe de refroidissement (9)", "Rectangle gris sur le trait mixte ; emplacement [HYP]."),
    (10, "Singularity cooling supply", "Réserve de fluide de refroidissement", "Réservoir de refroidissement (10)",
     "2 réservoirs à fonds bombés ; nature du fluide non précisée ; emplacement [HYP]."),
    (11, "Gravity sensor unit", "Unité de capteurs de gravité", "Capteurs de gravité (11)", "Capsule + module à deux tambours ; emplacement [HYP]."),
    (12, "Battery supply", "Alimentation par batterie", "Batterie (12)", "6 éléments, 2 bornes ; emplacement [HYP]."),
]
SYSTEMES_TEXTE = [   # n°, intitulé du texte, correspondance, modélisation, classement, remarque
    (1, "Logements magnétiques des deux micro-singularités", "DOC-007 n°1, n°2 ; DOC-008 n°1, n°2, n°3",
     "Carters, bobines, calottes, générateurs/régulateurs de champ, logements de la platine", "DOC (logements) / DÉD (carters, bobines)",
     "Seul système décrit à la fois par le texte, DOC-007 et DOC-008."),
    (2, "Collecteur d'injection d'électrons (modifie masse et gravité)", "DOC-008 n°4, n°5, n°6",
     "Tubes, rampe, régulateur, générateur d'électrons", "DÉD (4, 5) / HYP (emplacement de 6)", "Aucune trace sur DOC-007 ni sur les photos."),
    (3, "Refroidissement et évacuation des rayons X", "DOC-008 n°8, n°9, n°10 ; DOC-009 n°5 (cône)",
     "Enveloppes, pompe, réservoirs. ÉVACUATION DES RAYONS X : NON MODÉLISÉE", "DÉD (8) / HYP (9, 10) / — (rayons X)",
     "Aucun organe d'évacuation (trappe, cône, blindage) n'est visible sur le coffre : rien à modéliser sans inventer."),
    (4, "Capteurs de gravité (système VGL, variable gravity lock)", "DOC-008 n°11 (et n°7 ?)",
     "Capsule + module à tambours ; amplificateurs de capteur sur les carters", "HYP (emplacement de 11) / DÉD (7)",
     "Le lien entre le « sensor booster » (7) et le VGL n'est pas établi par les documents."),
    (5, "Horloges principales (4 au césium)", "Aucune image", "4 volumes génériques", "HYP (existence : DOC texte)",
     "Forme, taille et emplacement entièrement supposés."),
    (6, "Calculateurs principaux (3, vote dit « Borda »)", "Aucune image", "3 volumes génériques", "HYP (existence : DOC texte)",
     "Forme, taille et emplacement entièrement supposés."),
]
PHOTOS = [   # élément, documents, modélisation, classement, remarque
    ("Coffre sombre, couvercle ouvert proche de la verticale", "DOC-001, 002, 003, 004", "Corps + couvercle (10 pièces)", "DOC", "Angle retenu : 108° (DOC-004)."),
    ("Bandes de danger jaunes à raies noires (couvercle et platine)", "DOC-001, 002, 003 ; DOC-004 ; DOC-007", "4 fonds + 20 raies", "DOC",
     "Position et nombre de raies d'après DOC-007 ; les photos montrent 2–3 raies et une bande 2 plus à gauche (écarts E4, E5)."),
    ("Plaque d'instructions gris clair, lignée", "DOC-001, 002, 003 ; DOC-004 ; DOC-007 n°7", "1 pièce", "DOC", "—"),
    ("Étiquette blanche à liseré rouge + étiquette orange (centre du couvercle)", "DOC-001, 002, 003 ; DOC-004 (rectangle clair en deux parties)", "2 pièces", "DOC",
     "Absentes de DOC-007."),
    ("Étiquette jaune et élément gris (haut gauche du couvercle)", "DOC-001, 002, 003 ; DOC-004", "2 pièces", "DOC / DÉD", "Élément gris : étiquette ou boîtier, indéterminé."),
    ("Lueur rouge sur la platine (DOC-002) et reflet rouge au bas de la plaque", "DOC-002 ; DOC-003", "Fenêtre du panneau 5 teintée en rouge", "DÉD",
     "À l'aplomb de la fenêtre du panneau 5 de DOC-007."),
    ("Cordon spiralé noir et clair sortant à droite", "DOC-001, 002, 003 ; DOC-004", "6 tronçons cylindriques", "DÉD (existence : DOC image)", "Tracé, longueur et diamètre déduits ou supposés ; pas de spires modélisées (cylindre lisse)."),
    ("Boîtier de télécommande à étiquettes jaunes, posé devant l'unité", "DOC-002, 003 ; DOC-004 ; DOC-007 n°3", "Boîtier + 7 détails", "DOC", "Détails d'après DOC-007."),
    ("Ferrures rondes claires sur la face avant", "DOC-002, 003 ; DOC-004 (pièce claire près du bord gauche)", "2 loquets", "DÉD", "Nombre (2 ou 3) et positions incertains."),
    ("Renfoncement sombre sur la face d'extrémité gauche", "DOC-004", "Poignée gauche (+ droite par symétrie)", "DÉD / HYP", "—"),
    ("Étiquettes claires à repères d'angle de part et d'autre des logements ; plaquette striée devant", "DOC-004", "3 pièces", "DÉD", "Absentes de DOC-007."),
    ("Formes bombées visibles au fond des logements", "DOC-004", "Sommet des carters et raccords supérieurs", "DÉD", "—"),
    ("Tringle claire continue le long de la charnière", "DOC-004", "NON MODÉLISÉE (2 charnières de DOC-007 retenues)", "—", "Écart E6."),
    ("Banquette bleue à sangles, objets divers, habitacle", "DOC-001, 002, 003", "NON MODÉLISÉS (hors de l'unité)", "—", "Pistes d'étalonnage d'échelle pour l'Équipe A (sangle ≈ 47–50 mm)."),
]
DOC005_REPERES = OrderedDict()   # rempli à partir du modèle


def md_table(entetes, lignes):
    out = ["| " + " | ".join(entetes) + " |", "|" + "|".join("---" for _ in entetes) + "|"]
    for l in lignes:
        out.append("| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in l) + " |")
    return "\n".join(out)


def dims(p):
    g = p["primitive"]
    mm = lambda v: f"{v * 1000:.0f}"
    if g["type"] == "boite":
        return "boîte " + " × ".join(mm(v) for v in g["dimensions"]) + " mm"
    if g["type"] == "cylindre":
        return f"cylindre Ø {mm(2 * g['rayon'])} × {mm(g['hauteur'])} mm"
    if g["type"] == "sphere":
        return ("ellipsoïde, rayon " if "echelle" in g else "sphère Ø ") + mm(g["rayon"] * (1 if "echelle" in g else 2)) + " mm"
    if g["type"] == "tore":
        return f"tore Ø moy. {mm(2 * g['rayon_majeur'])}, fil Ø {mm(2 * g['rayon_mineur'])} mm"
    return f"prisme {len(g['profil'])} sommets, ép. {g['hauteur'] * 1000:.1f} mm"


def classements(pieces):
    c = Counter(p["classement"] for p in pieces)
    return " / ".join(f"{k} ×{v}" for k, v in c.items()) if len(c) > 1 else (next(iter(c)) if c else "—")


def main():
    modele = json.loads((ICI / "modele_c204.json").read_text(encoding="utf-8"))
    A, B = modele["variantes"]["A"], modele["variantes"]["B"]
    pa, pb = A["pieces"], B["pieces"]
    c = modele["cotes"]

    def trouve(frags):
        return [p for p in pa if any(f in p["nom"] or f in p["ensemble"] for f in frags)]

    L = []
    L.append("# Nomenclature du modèle 3D « C204 » — Équipe E\n")
    L.append(f"Générée le {modele['meta']['genere_le']} par `generer_nomenclature.py` à partir de `modele_c204.json` (ne pas modifier à la main).\n")
    L.append("> " + modele["meta"]["avertissement"] + "\n")
    L.append("**Classement** (appliqué à la pièce TELLE QUE MODÉLISÉE, forme + position) : "
             + " ; ".join(f"**[{k}]** {v['libelle'].lower()} — {v['definition']}" for k, v in modele["meta"]["classements"].items()) + "\n")
    L.append("La colonne « existence » précise d'où vient le composant lui-même : *DOC image* (visible sur un document), *DOC texte* (cité dans les messages seulement), *HYP* (ajouté par nous).\n")
    L.append(f"Dimensions à l'échelle hypothétique retenue (L = {c['L']['valeur']:.2f} m ± {c['L']['incertitude']:.2f} m) : toute cote absolue hérite de cette incertitude (voir parametres.json).\n".replace(".", ",", 2))

    # --- bilan -------------------------------------------------------------------------------
    L.append("## 1. Bilan\n")
    L.append(md_table(["Variante", "Pièces", "[DOC]", "[DÉD]", "[HYP]", "Contenu"],
                      [[k, len(v["pieces"]), v["bilan_classement"]["DOC"], v["bilan_classement"]["DÉD"], v["bilan_classement"]["HYP"], v["nom"]]
                       for k, v in modele["variantes"].items()]) + "\n")
    # bilan par couche (correction n° 47 de la Red Team) : extérieur visible / intérieur jamais montré
    bc = A["bilan_couches"]
    L.append("### Bilan par couche (variante A)\n")
    L.append(md_table(["Couche", "[DOC]", "[DÉD]", "[HYP]", "Ce que montrent les documents"],
                      [["Extérieur (coque, couvercle, platine, télécommande)", f"**{bc['exterieur']['DOC']}**", bc["exterieur"]["DÉD"], bc["exterieur"]["HYP"],
                        "photos DOC-001/002/003, illustration DOC-004, dessin DOC-007"],
                       ["**Intérieur (tout ce qui est sous la platine)**", f"**{bc['interieur']['DOC']}**", bc["interieur"]["DÉD"], bc["interieur"]["HYP"],
                        "rien : schéma de principe DOC-008 et texte seulement"]]) + "\n")
    dd = bc["detail_DOC"]
    ap = dd["par_appui"]
    L.append(f"**Aucune pièce intérieure n'est [DOC].** Le total de {dd['total']} pièces [DOC] ne doit pas être lu comme « la moitié de l'objet est documentée » : "
             f"{dd['marquages_repetes']} d'entre elles sont des motifs répétés ({dd['dont_raies_noires']} raies noires, {dd['dont_fonds_de_bande']} fonds de bande, "
             f"{dd['dont_pastilles_du_pupitre']} pastilles du pupitre) ; {ap.get('dessin DOC-007 seul', 0)} n'ont pour source que le dessin DOC-007 "
             f"(« [DOC] dessin »), que les photos contredisent sur la position des bandes ; {ap.get('dessin DOC-007 + photo ou illustration', 0)} s'appuient à la fois sur le dessin "
             f"et sur une photo ou sur DOC-004, et {ap.get('photo ou illustration seule', 0)} sur les photos seules (« [DOC] photo »). "
             "Pour toute pièce relevée sur la seule vue de dessus, seule l'emprise en plan est documentée : épaisseur et relief sont supposés. "
             "La colonne `appui` de `nomenclature.csv` donne ce détail pièce par pièce.\n")
    bv = A["bilan_volumique"]
    fr = lambda x, n=1: f"{x:.{n}f}".replace(".", ",")
    L.append(f"Volume intérieur utile du coffre (variante A) : {fr(bv['volume_interieur_m3'] * 1000)} L. Composants de DOC-008, à l'échelle de leur schéma : "
             f"{fr(bv['volume_composants_DOC008_m3'] * 1000)} L, soit **{fr(bv['taux_occupation_DOC008'] * 100, 0)} %** ; avec les volumes génériques [HYP] du texte "
             f"(horloges, calculateurs : {fr(bv['volume_volumes_generiques_texte_m3'] * 1000)} L) : {fr(bv['volume_composants_m3'] * 1000)} L, soit "
             f"**{fr(bv['taux_occupation'] * 100, 0)} %**. " + bv["note"] + "\n")

    # --- DOC-007 -----------------------------------------------------------------------------
    L.append("## 2. Les 9 repères de DOC-007 (vue de dessus, légende nette)\n")
    lignes = []
    for n, leg, trad, frags, rem in DOC007:
        ps = trouve(frags)
        lignes.append([n, f"« {leg} »", trad, len(ps), classements(ps), rem])
    L.append(md_table(["N°", "Légende d'origine", "Traduction", "Pièces", "Classement", "Remarques"], lignes) + "\n")

    # --- DOC-008 -----------------------------------------------------------------------------
    L.append("## 3. Les 12 repères de DOC-008 (« BASIC COMPONENTS », légende de confiance moyenne)\n")
    lignes = []
    for n, leg, trad, frag, rem in DOC008:
        ps = [p for p in pa if frag in p["nom"]]
        princ = max(ps, key=lambda p: p["volume_m3"]) if ps else None
        lignes.append([n, f"« {leg} »", trad, len(ps), "DOC image", classements(ps), dims(princ) if princ else "—", rem])
    L.append(md_table(["N°", "Légende (lecture)", "Traduction", "Pièces", "Existence", "Classement de la pièce", "Pièce principale", "Remarques"], lignes) + "\n")
    L.append("Éléments de DOC-008 **non numérotés** et modélisés : raccord supérieur de chaque carter (pavé blanc), calottes d'extrémité des bobines. "
             "Liaisons (traits pleins, tiretés, mixtes) : relevées dans `schema_electrique_hypothetique.svg` et `architecture_fonctionnelle.svg`, non modélisées en 3D (hormis le collecteur 4).\n")

    # --- systèmes du texte -------------------------------------------------------------------
    L.append("## 4. Les six systèmes du texte (message du 2 novembre 2000)\n")
    L.append(md_table(["N°", "Système (texte)", "Correspondance documentaire", "Modélisation", "Classement", "Remarques"], SYSTEMES_TEXTE) + "\n")

    # --- photos ------------------------------------------------------------------------------
    L.append("## 5. Éléments visibles sur les photos (DOC-001/002/003) et sur DOC-004\n")
    L.append(md_table(["Élément observé", "Documents", "Modélisation", "Classement", "Remarques"], PHOTOS) + "\n")

    # --- variante B --------------------------------------------------------------------------
    L.append("## 6. Variante B — les 35 repères de DOC-005 (écorché sans légende)\n")
    L.append("Aucune légende n'accompagne la copie archivée : toutes les fonctions sont **inconnues**. Les volumes sont des approximations génériques [DÉD] "
             "lues sur une vue unique ; leur profondeur est supposée. L'échelle est arbitraire (longueur prise égale à celle de la variante A).\n")
    attrib = {}
    for p in pb:
        if p["repere"].startswith("DOC-005 n°"):
            for n in p["repere"].replace("DOC-005 n°", "").split(","):
                attrib.setdefault(int(n.strip()), []).append(p)
    lignes = []
    for n in range(1, 36):
        ps = attrib.get(n, [])
        if ps:
            lignes.append([n, " ; ".join(sorted({p["nom"] for p in ps})), dims(ps[0]), "DÉD"])
        else:
            lignes.append([n, "NON MODÉLISÉ — " + {8: "long tube oblique entre les repères 7 et 9 (élément mince, profondeur indéterminable)"}.get(n, "élément non identifié"), "—", "—"])
    L.append(md_table(["N° DOC-005", "Volume du modèle", "Primitive (échelle arbitraire)", "Classement"], lignes) + "\n")
    autres = [p for p in pb if not p["repere"].startswith("DOC-005 n°")]
    L.append("Pièces de la variante B sans repère : " + " ; ".join(f"{p['nom']} [{p['classement']}]" for p in autres) + ".\n")

    # --- nomenclature complète par ensemble (variante A) -------------------------------------
    L.append("## 7. Nomenclature complète de la variante A, par ensemble\n")
    ens = OrderedDict()
    for p in pa:
        ens.setdefault(p["ensemble"], []).append(p)
    lignes = []
    for e, ps in ens.items():
        srcs = "; ".join(sorted({s.strip() for p in ps for s in p["source"].replace("(", ";").split(";") if s.strip().startswith("DOC-") or s.strip().startswith("Texte")}))[:90]
        lignes.append([e, len(ps), classements(ps), sorted({p["repere"] for p in ps})[0] if len({p["repere"] for p in ps}) == 1 else "divers", srcs or ps[0]["source"][:60],
                       ps[0]["fonction_revendiquee"][:150]])
    L.append(md_table(["Ensemble", "Pièces", "Classement", "Repère", "Documents", "Fonction revendiquée (1re pièce)"], lignes) + "\n")
    L.append(f"La variante A′ (`A2`) contient les mêmes {len(pa)} pièces ; seuls changent les emplacements [HYP] (batterie, réservoirs, pompe, générateur d'électrons, capteurs, horloges, calculateurs).\n")
    L.append("Détail pièce par pièce (dimensions, positions, notes) : `nomenclature.csv` et fiches de `visionneuse.html`.\n")
    (ICI / "NOMENCLATURE.md").write_text("\n".join(L), encoding="utf-8")

    # --- CSV ---------------------------------------------------------------------------------
    cols = ["variante", "id", "nom", "ensemble", "repere", "source", "classement", "existence", "appui", "systeme", "couche", "fonction_revendiquee",
            "primitive", "dimensions", "x_m", "y_m", "z_m", "volume_m3", "notes"]
    with open(ICI / "nomenclature.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cols)
        for cle, v in (("A", A), ("B", B)):
            for p in v["pieces"]:
                w.writerow([cle, p["id"], p["nom"], p["ensemble"], p["repere"], p["source"], p["classement"], p["existence"], p["appui"],
                            modele["meta"]["systemes"][p["systeme"]]["libelle"], p["couche"], p["fonction_revendiquee"], p["primitive"]["type"], dims(p),
                            *(f"{x:.4f}".replace(".", ",") for x in p["position"]), f"{p['volume_m3']:.3g}".replace(".", ","), p.get("notes", "")])
        nm = [("Évacuation des rayons X", "texte (système 3) ; DOC-009 n°5", "Aucun organe visible sur le coffre : non modélisé."),
              ("Tringle continue de charnière", "DOC-004", "Écart E6 : deux charnières de DOC-007 retenues."),
              ("Liaisons électriques et fluidiques de DOC-008", "DOC-008", "Représentées dans les schémas SVG, pas en 3D (sauf collecteur 4)."),
              ("Long tube oblique (repère 8)", "DOC-005 n°8", "Variante B : élément mince non modélisé."),
              ("Coins arrondis du coffre", "DOC-007", "Simplification : arêtes vives."),
              ("Texte des plaques et étiquettes", "DOC-007 n°7 ; photos", "Illisible sur toutes les copies."),
              ("Banquette, sangles, habitacle du véhicule", "DOC-001 ; DOC-002 ; DOC-003", "Hors de l'unité ; pistes d'étalonnage pour l'Équipe A.")]
        for k, (nom, src, note) in enumerate(nm, 1):
            w.writerow(["—", f"NM-{k:02d}", nom, "Éléments documentés NON modélisés", "—", src, "—", "DOC", "—", "—", "—", "—", "—", "—", "", "", "", "", note])
    print(f"écrit : NOMENCLATURE.md, nomenclature.csv ({len(pa) + len(pb)} pièces + éléments non modélisés)")


if __name__ == "__main__":
    main()
