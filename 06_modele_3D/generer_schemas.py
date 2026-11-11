#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — schémas générés par script.

    architecture_fonctionnelle.svg       schéma-blocs des flux (énergie, électrons, fluide de refroidissement,
                                         signaux capteurs / horloges / calculateurs, commande)
    schema_electrique_hypothetique.svg   schéma unifilaire HYPOTHÉTIQUE (batterie → régulateurs → charges)

Dans les deux schémas, les liaisons RELEVÉES sur DOC-008 (traits pleins, tiretés, mixtes du document) sont
distinguées des liaisons AJOUTÉES par l'Équipe E (hypothèses). Aucune tension, aucun courant, aucune
puissance ne figure dans les documents : les schémas sont topologiques, non dimensionnés.

Usage : python generer_schemas.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ICI = Path(__file__).resolve().parent

FLUX = {   # couleur par nature de flux
    "energie": ("#c0392b", "Énergie électrique"),
    "electrons": ("#1f5fbf", "Électrons (injection)"),
    "fluide": ("#0e8a9c", "Fluide de refroidissement"),
    "signal": ("#3d8b2f", "Signaux (capteurs, horloges)"),
    "commande": ("#7a3fb0", "Commande"),
    "rayonnement": ("#b8860b", "Rayons X / chaleur (texte)"),
    "indetermine": ("#555555", "Nature non légendée (DOC-008)"),
}
STATUT = {   # style de trait par statut documentaire
    "doc": ("", 2.6, "Liaison dessinée sur DOC-008"),
    "texte": ("2 5", 2.2, "Affirmée par le texte seulement"),
    "hyp": ("9 6", 1.7, "Ajout hypothétique de l'Équipe E"),
}
CLASSE = {"DOC": "#0072B2", "DÉD": "#E69F00", "HYP": "#CC79A7", "TXT": "#8a8f98"}


class Svg:
    def __init__(self, w, h, titre):
        self.w, self.h = w, h
        self.e = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(titre)}" '
                  f'font-family="Helvetica, Arial, sans-serif">',
                  f"<title>{escape(titre)}</title>", "<defs>"]
        for cle, (coul, _) in FLUX.items():
            self.e.append(f'<marker id="f-{cle}" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto-start-reverse">'
                          f'<path d="M0,0 L10,5 L0,10 z" fill="{coul}"/></marker>')
        self.e.append('<pattern id="hachures" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">'
                      '<rect width="10" height="10" fill="#fff"/><rect width="3" height="10" fill="#f6e3ee"/></pattern>')
        self.e.append("</defs>")
        self.e.append(f'<rect width="{w}" height="{h}" fill="#ffffff"/>')

    def texte(self, x, y, t, taille=13, gras=False, ancre="middle", coul="#16181d", italique=False):
        self.e.append(f'<text x="{x}" y="{y}" font-size="{taille}" text-anchor="{ancre}" fill="{coul}"'
                      + (' font-weight="700"' if gras else "") + (' font-style="italic"' if italique else "") + f">{escape(t)}</text>")

    def bloc(self, x, y, w, h, lignes, classe, rep="", fond="#fbfbfc"):
        coul = CLASSE[classe]
        self.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fond}" stroke="{coul}" stroke-width="2.4"/>')
        self.e.append(f'<rect x="{x}" y="{y}" width="9" height="{h}" rx="3" fill="{coul}"/>')
        n = len(lignes)
        y0 = y + h / 2 - (n - 1) * 8 + 4.5
        for i, l in enumerate(lignes):
            self.texte(x + w / 2 + 4, y0 + i * 16, l, 12.5 if i else 13, gras=(i == 0))
        if rep:
            self.e.append(f'<rect x="{x + w - 78}" y="{y - 10}" width="74" height="18" rx="9" fill="#fff" stroke="{coul}" stroke-width="1.3"/>')
            self.texte(x + w - 41, y + 3.5, rep, 10.5, coul="#333")

    def lien(self, pts, flux, statut, fleche=True, deux_sens=False, etiquette=None, pos=None):
        coul = FLUX[flux][0]
        tirets, ep, _ = STATUT[statut]
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        self.e.append(f'<path d="{d}" fill="none" stroke="{coul}" stroke-width="{ep}"' + (f' stroke-dasharray="{tirets}"' if tirets else "")
                      + (f' marker-end="url(#f-{flux})"' if fleche else "") + (f' marker-start="url(#f-{flux})"' if deux_sens else "")
                      + ' stroke-linejoin="round"/>')
        if etiquette:
            x, y = pos
            larg = 6.1 * len(etiquette) + 10
            self.e.append(f'<rect x="{x - larg / 2}" y="{y - 11}" width="{larg}" height="15" fill="#ffffff" opacity="0.92"/>')
            self.texte(x, y, etiquette, 10.5, coul=coul, italique=True)

    def legende(self, x, y, flux=True, largeur=None):
        cx = x
        self.texte(cx, y, "Nature du flux", 12, gras=True, ancre="start")
        yy = y + 18
        for cle, (coul, lib) in FLUX.items():
            self.e.append(f'<line x1="{cx}" y1="{yy - 4}" x2="{cx + 34}" y2="{yy - 4}" stroke="{coul}" stroke-width="3"/>')
            self.texte(cx + 42, yy, lib, 11.5, ancre="start")
            yy += 17
        cx = x + 250
        self.texte(cx, y, "Statut de la liaison", 12, gras=True, ancre="start")
        yy = y + 18
        for cle, (tirets, ep, lib) in STATUT.items():
            self.e.append(f'<line x1="{cx}" y1="{yy - 4}" x2="{cx + 44}" y2="{yy - 4}" stroke="#222" stroke-width="{ep}"' + (f' stroke-dasharray="{tirets}"' if tirets else "") + "/>")
            self.texte(cx + 52, yy, lib, 11.5, ancre="start")
            yy += 17
        cx = x + 520
        self.texte(cx, y, "Classement du bloc", 12, gras=True, ancre="start")
        yy = y + 18
        for cle, lib in (("DOC", "[DOC] visible sur DOC-007 (pupitre)"), ("DÉD", "[DÉD] composant de DOC-008, placé sous les logements"),
                         ("HYP", "[HYP] composant de DOC-008, emplacement supposé"), ("TXT", "Cité par le texte seul (aucune image)")):
            self.e.append(f'<rect x="{cx}" y="{yy - 11}" width="16" height="12" rx="3" fill="#fbfbfc" stroke="{CLASSE[cle]}" stroke-width="2.4"/>')
            self.texte(cx + 24, yy, lib, 11.5, ancre="start")
            yy += 17

    def sortie(self, chemin):
        self.e.append("</svg>")
        Path(chemin).write_text("\n".join(self.e), encoding="utf-8")


AVERT = "Reconstruction documentaire d'un objet DÉCRIT (documents non authentifiés) : rien n'atteste qu'il ait existé ni fonctionné. Les fonctions sont celles REVENDIQUÉES par les légendes et le texte."


def architecture():
    s = Svg(1560, 1070, "C204 — architecture fonctionnelle (flux revendiqués)")
    s.texte(780, 34, "C204 — architecture fonctionnelle : flux d'énergie, d'électrons, de fluide, de signaux et de commande", 19, gras=True)
    s.texte(780, 56, AVERT, 11.5, coul="#555", italique=True)
    B = {}

    def bloc(cle, x, y, w, h, lignes, classe, rep=""):
        B[cle] = (x, y, w, h)
        s.bloc(x, y, w, h, lignes, classe, rep)

    # rangée haute : commande et mesure
    bloc("pupitre", 60, 100, 230, 74, ["Pupitre et télécommande", "commandes d'urgence 8, écran 4,", "télécommande 3"], "DOC", "DOC-007")
    bloc("horloges", 345, 100, 220, 74, ["Horloges ×4", "« au césium » (texte)"], "TXT", "texte")
    bloc("calc", 640, 100, 240, 74, ["Calculateurs ×3", "vote dit « Borda » (texte)"], "TXT", "texte")
    bloc("capteurs", 960, 100, 260, 74, ["Unité de capteurs de gravité", "système VGL (texte)"], "HYP", "DOC-008 n°11")
    # colonne gauche : énergie
    bloc("marche", 60, 262, 230, 64, ["Interrupteur général", "marche / arrêt"], "DOC", "DOC-007 n°6")
    bloc("batterie", 60, 412, 230, 70, ["Batterie", "« battery supply », 6 éléments"], "HYP", "DOC-008 n°12")
    bloc("coupure", 60, 566, 230, 64, ["Coupure d'urgence", "« emergency disconnect »"], "DOC", "DOC-007 n°5")
    # colonne 2
    bloc("regP", 345, 258, 220, 72, ["Générateur / régulateur", "de champ magnétique", "(singularité principale)"], "DÉD", "DOC-008 n°3")
    bloc("gen", 345, 412, 220, 70, ["Générateur d'électrons"], "HYP", "DOC-008 n°6")
    bloc("regD", 345, 562, 220, 72, ["Générateur / régulateur", "de champ magnétique", "(singularité de direction)"], "DÉD", "DOC-008 n°3")
    # colonne 3
    bloc("bobP", 640, 262, 240, 64, ["Bobines de champ ×6", "(singularité principale)"], "DÉD", "DOC-008 n°2")
    bloc("regE", 640, 412, 240, 70, ["Régulateur d'électrons"], "DÉD", "DOC-008 n°5")
    bloc("bobD", 640, 566, 240, 64, ["Bobines de champ ×6", "(singularité de direction)"], "DÉD", "DOC-008 n°2")
    # colonne 4 : carters
    bloc("carP", 960, 248, 260, 92, ["Carter d'entraînement 1", "+ enveloppe de refroidissement 8", "+ amplificateur de capteur 7", "SINGULARITÉ PRINCIPALE"], "DÉD", "DOC-007 n°1")
    bloc("coll", 960, 412, 260, 70, ["Collecteur d'injection", "d'électrons"], "DÉD", "DOC-008 n°4")
    bloc("carD", 960, 552, 260, 92, ["Carter d'entraînement 1", "+ enveloppe de refroidissement 8", "+ amplificateur de capteur 7", "SINGULARITÉ DE DIRECTION"], "DÉD", "DOC-007 n°2")
    # bas : refroidissement
    bloc("reserv", 640, 742, 240, 70, ["Réservoirs de fluide ×2", "« cooling supply »"], "HYP", "DOC-008 n°10")
    bloc("pompe", 960, 742, 260, 70, ["Pompe de refroidissement"], "HYP", "DOC-008 n°9")
    # droite : rayons X
    bloc("rx", 1320, 412, 190, 70, ["Évacuation des rayons X", "« vers l'arrière » (texte)", "organe NON localisé"], "TXT", "DOC-009 n°5")

    # --- liaisons RELEVÉES sur DOC-008 ---------------------------------------------------------
    s.lien([(290, 432), (318, 432), (318, 304), (345, 304)], "energie", "doc")
    s.lien([(290, 462), (318, 462), (318, 584), (345, 584)], "energie", "doc")
    s.lien([(290, 447), (345, 447)], "energie", "doc")
    s.lien([(565, 294), (640, 294)], "energie", "doc", etiquette="tirets", pos=(602, 286))
    s.lien([(565, 598), (640, 598)], "energie", "doc", etiquette="tirets", pos=(602, 590))
    s.lien([(880, 294), (960, 294)], "energie", "doc", fleche=False, etiquette="champ", pos=(920, 286))
    s.lien([(880, 598), (960, 598)], "energie", "doc", fleche=False, etiquette="champ", pos=(920, 590))
    s.lien([(565, 447), (640, 447)], "electrons", "doc", etiquette="2 traits", pos=(602, 439))
    s.lien([(880, 447), (960, 447)], "electrons", "doc")
    s.lien([(1090, 412), (1090, 340)], "electrons", "doc")
    s.lien([(1090, 482), (1090, 552)], "electrons", "doc")
    # trait plein en T reliant le sommet des deux carters au régulateur 5 (nature non légendée)
    s.lien([(720, 412), (720, 380), (1252, 380), (1252, 300), (1220, 300)], "indetermine", "doc", etiquette="trait plein en T vers le sommet des carters", pos=(990, 372))
    s.lien([(720, 482), (720, 514), (1252, 514), (1252, 590), (1220, 590)], "indetermine", "doc")
    # fluide : réservoirs → pompe → enveloppes (trait mixte de DOC-008)
    s.lien([(880, 777), (960, 777)], "fluide", "doc", etiquette="trait mixte", pos=(920, 769))
    s.lien([(1060, 742), (1060, 644)], "fluide", "doc")
    s.lien([(1220, 777), (1282, 777), (1282, 320), (1220, 320)], "fluide", "doc")
    # trait fin continu 11 → 9 contournant tout le schéma (nature non légendée)
    s.lien([(1220, 137), (1535, 137), (1535, 880), (1120, 880), (1120, 812)], "indetermine", "doc",
           etiquette="trait fin continu 11 → 9 contournant tout DOC-008 (nature non légendée)", pos=(1330, 872))
    # --- affirmations du texte -----------------------------------------------------------------
    s.lien([(1220, 266), (1415, 266), (1415, 412)], "rayonnement", "texte")
    s.lien([(1220, 626), (1415, 626), (1415, 482)], "rayonnement", "texte", etiquette="rayons X, chaleur", pos=(1415, 660))
    # --- ajouts hypothétiques ------------------------------------------------------------------
    s.lien([(565, 137), (640, 137)], "signal", "hyp", etiquette="temps", pos=(602, 129))
    s.lien([(960, 137), (880, 137)], "signal", "hyp", etiquette="gravité", pos=(920, 129))
    s.lien([(1110, 248), (1110, 214), (840, 214), (840, 174)], "signal", "hyp", etiquette="capteurs de singularité (7)", pos=(980, 206))
    s.lien([(175, 100), (175, 78), (760, 78), (760, 100)], "commande", "hyp", deux_sens=True, etiquette="consignes, affichage", pos=(460, 70))
    s.lien([(680, 174), (680, 232), (300, 232), (300, 700)], "commande", "hyp", fleche=False)
    s.lien([(300, 274), (345, 274)], "commande", "hyp")
    s.lien([(300, 392), (780, 392), (780, 412)], "commande", "hyp")
    s.lien([(300, 620), (345, 620)], "commande", "hyp")
    s.lien([(300, 700), (1000, 700), (1000, 742)], "commande", "hyp", etiquette="commande des régulateurs et de la pompe", pos=(650, 692))
    s.lien([(175, 326), (175, 412)], "commande", "hyp", etiquette="mise sous tension", pos=(175, 372))
    s.lien([(175, 566), (175, 482)], "commande", "hyp", etiquette="coupure", pos=(175, 528))

    s.e.append('<rect x="50" y="842" width="560" height="62" rx="8" fill="#fff8e6" stroke="#d9b24c"/>')
    for i, l in enumerate(["DOC-008 ne dessine AUCUNE alimentation pour la pompe (9), les capteurs (11) et les amplificateurs (7) ;",
                           "le texte ne décrit ni horloges ni calculateurs au-delà de leur nombre. Les liaisons correspondantes",
                           "sont proposées dans schema_electrique_hypothetique.svg et restent des hypothèses."]):
        s.texte(62, 862 + i * 16, l, 11.5, ancre="start", coul="#5b4500")
    s.legende(60, 930)
    s.sortie(ICI / "architecture_fonctionnelle.svg")


def unifilaire():
    s = Svg(1700, 1010, "C204 — schéma électrique unifilaire HYPOTHÉTIQUE")
    s.e.append('<text x="850" y="560" font-size="150" text-anchor="middle" fill="#cc79a7" opacity="0.10" font-weight="700" transform="rotate(-18 850 560)">HYPOTHÉTIQUE</text>')
    s.texte(850, 34, "C204 — schéma électrique unifilaire HYPOTHÉTIQUE (topologie seule, sans tension ni courant)", 19, gras=True)
    s.texte(850, 56, AVERT, 11.5, coul="#555", italique=True)
    s.e.append('<rect x="40" y="70" width="1620" height="34" rx="8" fill="#fbe9f2" stroke="#cc79a7" stroke-width="1.5"/>')
    s.texte(850, 92, "SCHÉMA HYPOTHÉTIQUE — seuls les éléments en trait plein NOIR sont relevés sur DOC-008 ; tout ce qui est en tirets ROSES est un ajout de l'Équipe E. "
            "Aucune tension, aucun courant, aucune puissance n'est documenté.", 12, gras=True, coul="#7a2a55")
    N, R = "#111111", "#c2478a"

    def trait(pts, doc=True, ep=None, tirets=None):
        d = "M" + " L".join(f"{x},{y}" for x, y in pts)
        coul = N if doc else R
        dash = tirets if tirets is not None else ("" if doc else "9 6")
        s.e.append(f'<path d="{d}" fill="none" stroke="{coul}" stroke-width="{ep or (2.4 if doc else 1.9)}"' + (f' stroke-dasharray="{dash}"' if dash else "") + ' stroke-linejoin="round"/>')

    def charge(x, y, w, h, lignes, doc=True, rep="", classe=None):
        coul = N if doc else R
        s.e.append(f'<rect x="{x - w / 2}" y="{y}" width="{w}" height="{h}" rx="6" fill="{"#ffffff" if doc else "url(#hachures)"}" stroke="{coul}" stroke-width="{2.2 if doc else 1.8}"'
                   + ("" if doc else ' stroke-dasharray="9 6"') + "/>")
        y0 = y + h / 2 - (len(lignes) - 1) * 7.5 + 4
        for i, l in enumerate(lignes):
            s.texte(x, y0 + i * 15, l, 11.8 if i else 12.3, gras=(i == 0))
        if rep:
            s.texte(x, y - 6, rep, 10.5, coul="#444")

    def point(x, y, doc=True):
        s.e.append(f'<circle cx="{x}" cy="{y}" r="4.2" fill="{N if doc else R}"/>')

    def interrupteur(x, y, etiquette, rep):
        """Symbole d'interrupteur en série sur un conducteur horizontal (position dans le circuit : HYP)."""
        s.e.append(f'<circle cx="{x - 22}" cy="{y}" r="3.6" fill="#fff" stroke="{R}" stroke-width="1.8"/>')
        s.e.append(f'<circle cx="{x + 22}" cy="{y}" r="3.6" fill="#fff" stroke="{R}" stroke-width="1.8"/>')
        s.e.append(f'<line x1="{x - 20}" y1="{y - 2}" x2="{x + 16}" y2="{y - 20}" stroke="{R}" stroke-width="2"/>')
        s.texte(x, y + 24, etiquette, 11.5, gras=True)
        for i, l in enumerate(rep):
            s.texte(x, y + 39 + i * 14, l, 10.5, coul="#444")

    yb = 190
    # batterie (DOC-008 n°12) : 6 éléments
    bx, by = 60, 150
    s.e.append(f'<rect x="{bx}" y="{by}" width="150" height="80" rx="6" fill="#fff" stroke="{N}" stroke-width="2.2"/>')
    for k in range(1, 6):
        s.e.append(f'<line x1="{bx + k * 25}" y1="{by + 6}" x2="{bx + k * 25}" y2="{by + 74}" stroke="{N}" stroke-width="1"/>')
    s.texte(bx + 75, by + 100, "12 · Batterie (6 éléments)", 12.3, gras=True)
    s.texte(bx + 75, by + 115, "relevé sur DOC-008", 10.5, coul="#444")
    s.texte(bx + 14, by + 20, "+", 15, gras=True)
    s.texte(bx + 136, by + 20, "−", 15, gras=True)
    trait([(210, yb), (268, yb)], doc=False)
    interrupteur(290, yb, "Interrupteur général", ["DOC-007 n°6", "place dans le circuit : HYP"])
    trait([(312, yb), (428, yb)], doc=False)
    interrupteur(450, yb, "Coupure d'urgence", ["DOC-007 n°5", "place dans le circuit : HYP"])
    trait([(472, yb), (540, yb)], doc=False)
    # barre de distribution (trait épais de DOC-008 joignant les deux bornes)
    trait([(540, yb), (1010, yb)], doc=True, ep=6)
    trait([(1010, yb), (1640, yb)], doc=False, ep=5, tirets="14 7")
    s.texte(775, yb - 16, "Barre de distribution — trait épais de DOC-008 joignant les deux bornes de la batterie", 11.5, coul="#111")
    s.texte(1325, yb - 16, "prolongement supposé de la barre", 11.5, coul=R, italique=True)

    # départs relevés sur DOC-008
    for x, nom in ((590, "principale"), (765, "de direction")):
        point(x, yb)
        trait([(x, yb), (x, 290)])
        charge(x, 290, 164, 66, ["3 · Générateur /", "régulateur de champ", f"({nom})"], rep="")
        trait([(x, 356), (x, 450)], tirets="7 5")
        s.texte(x + 8, 408, "tirets (DOC-008)", 10.5, ancre="start", coul="#444", italique=True)
        # symbole de bobine
        d = f"M{x - 48},{480}" + "".join(f" q8,-26 16,0" for _ in range(6))
        s.e.append(f'<path d="{d}" fill="none" stroke="{N}" stroke-width="2.2"/>')
        trait([(x, 450), (x, 466)], tirets="7 5")
        s.texte(x, 506, "2 · Bobines de champ ×6", 12.3, gras=True)
        s.texte(x, 521, f"autour du carter 1 ({nom})", 10.8, coul="#444")
    x = 960
    point(x, yb)
    trait([(x, yb), (x, 290)])
    charge(x, 290, 164, 66, ["6 · Générateur", "d'électrons"])
    trait([(x - 8, 356), (x - 8, 420)])
    trait([(x + 8, 356), (x + 8, 420)])
    s.texte(x + 18, 392, "2 traits pleins", 10.5, ancre="start", coul="#444", italique=True)
    charge(x, 420, 164, 56, ["5 · Régulateur", "d'électrons"])
    trait([(x, 476), (x, 540)], ep=1.6)
    charge(x, 540, 164, 56, ["4 · Collecteur", "d'injection"])
    trait([(x, 596), (x, 640), (700, 640), (700, 690)], ep=1.6)
    trait([(x, 640), (x, 690)], ep=1.6)
    charge(700, 690, 240, 70, ["Carter 1 + enveloppe 8", "SINGULARITÉ PRINCIPALE", "(DOC-007 n°1)"])
    charge(990, 690, 240, 70, ["Carter 1 + enveloppe 8", "SINGULARITÉ DE DIRECTION", "(DOC-007 n°2)"])
    s.texte(770, 632, "traits fins (DOC-008)", 10.5, coul="#444", italique=True)
    # trait plein en T : sommet des carters ↔ régulateur 5 (nature non légendée)
    trait([(878, 448), (846, 448), (846, 800), (700, 800), (700, 760)], ep=1.4)
    trait([(846, 800), (990, 800), (990, 760)], ep=1.4)
    s.texte(560, 818, "trait plein en T de DOC-008 reliant le sommet des deux carters au régulateur 5 (nature non légendée)", 10.5, ancre="start", coul="#444", italique=True)

    # départs HYPOTHÉTIQUES
    x = 1130
    point(x, yb, doc=False)
    trait([(x, yb), (x, 290)], doc=False)
    charge(x, 290, 150, 56, ["Protection", "(fusible ou disjoncteur)"], doc=False)
    trait([(x, 346), (x, 420)], doc=False)
    s.e.append(f'<circle cx="{x}" cy="454" r="34" fill="#fff" stroke="{N}" stroke-width="2.2"/>')
    s.texte(x, 461, "M", 22, gras=True)
    s.texte(x, 508, "9 · Pompe de", 12.3, gras=True)
    s.texte(x, 523, "refroidissement", 12.3, gras=True)
    s.texte(x, 539, "(DOC-008 ; alimentation", 10.5, coul="#444")
    s.texte(x, 553, "non dessinée)", 10.5, coul="#444")
    x = 1420
    point(x, yb, doc=False)
    trait([(x, yb), (x, 290)], doc=False)
    charge(x, 290, 210, 56, ["Convertisseur / régulateur", "basse tension"], doc=False)
    trait([(x, 346), (x, 400)], doc=False)
    trait([(1215, 400), (1655, 400)], doc=False, ep=3.2)
    s.texte(1435, 392, "distribution basse tension (supposée)", 10.8, coul=R, italique=True, ancre="start")
    charges = [(1400, ["Calculateurs", "×3 (texte)"], False, 450), (1400, ["Horloges", "×4 (texte)"], False, 560),
               (1262, ["11 · Capteurs", "de gravité"], True, 450), (1262, ["7 · Amplificateurs", "de capteur ×2"], True, 560),
               (1560, ["Pupitre : 8, 4", "(DOC-007)"], True, 450), (1560, ["3 · Télécommande", "(DOC-007)"], True, 560)]
    for cx, lignes, doc, cy in charges:
        dx = -46 if cy == 450 else 46
        trait([(cx + dx, 400), (cx + dx, cy)], doc=False)
        point(cx + dx, 400, doc=False)
        charge(cx, cy, 128, 52, lignes, doc=doc)
    s.texte(1435, 640, "Composants en trait plein noir : dessinés (DOC-008, DOC-007) ;", 10.8, coul="#444")
    s.texte(1435, 655, "leur alimentation, en tirets roses, est supposée.", 10.8, coul="#444")
    # liaison 11 → 9 de DOC-008 (trait fin continu, nature non légendée)
    trait([(1198, 468), (1163, 460)], ep=1.3)
    s.texte(1435, 672, "Le trait fin entre 11 et 9 est relevé sur DOC-008 (nature non légendée).", 10.8, coul="#444")

    # encadrés
    s.e.append('<rect x="40" y="850" width="790" height="140" rx="8" fill="#f6f7f9" stroke="#c9ced6"/>')
    s.texte(54, 870, "Topologie RELEVÉE sur DOC-008 (confiance moyenne : copie de 415 × 580 px)", 12.3, gras=True, ancre="start")
    for i, l in enumerate([
        "a) trait épais joignant les deux bornes de la batterie 12 — lu ici comme une barre de distribution (littéralement : un court-circuit) ;",
        "b) traits pleins de cette barre vers les deux générateurs / régulateurs de champ 3 et vers le générateur d'électrons 6 ;",
        "c) tirets de chaque 3 vers les bobines 2 du carter correspondant ;  d) deux traits pleins entre 6 et 5 ;",
        "e) traits fins 5 → 4 → base de chaque carter ;  f) trait plein en T entre le sommet des deux carters et 5 ;",
        "g) trait mixte 10 → 9 → carters (fluide : voir architecture_fonctionnelle.svg) ;  h) trait fin continu 11 → 9 contournant le schéma.",
        "Aucune liaison n'aboutit aux amplificateurs de capteur 7 ; aucune alimentation n'est dessinée pour 9 ni pour 11."]):
        s.texte(54, 890 + i * 16.5, l, 11.2, ancre="start", coul="#222")
    s.e.append('<rect x="850" y="850" width="810" height="140" rx="8" fill="#fbe9f2" stroke="#cc79a7"/>')
    s.texte(864, 870, "AJOUTS hypothétiques de l'Équipe E (non étayés par les sources)", 12.3, gras=True, ancre="start", coul="#7a2a55")
    for i, l in enumerate([
        "• place de l'interrupteur général (6) et de la coupure d'urgence (5) en série entre batterie et barre ;",
        "• prolongement de la barre, protection et départ de la pompe 9 ;",
        "• convertisseur basse tension et distribution vers calculateurs, horloges, capteurs 11, amplificateurs 7, pupitre et télécommande ;",
        "• sens de l'énergie (de la batterie vers les charges) : jamais indiqué par des flèches sur DOC-008.",
        "Ordre de grandeur à garder en tête : le texte prête 300–500 MW aux « singularités », sans rapport possible avec une batterie",
        "embarquée dans un coffre de 227 kg (voir les Équipes B et C). Ce schéma ne dit rien de la faisabilité."]):
        s.texte(864, 890 + i * 16.5, l, 11.2, ancre="start", coul="#3a1a2c")
    # légende
    s.e.append(f'<line x1="60" y1="330" x2="120" y2="330" stroke="{N}" stroke-width="2.4"/>')
    s.texte(130, 334, "relevé sur DOC-008 (ou composant visible sur DOC-007)", 11.5, ancre="start")
    s.e.append(f'<line x1="60" y1="352" x2="120" y2="352" stroke="{R}" stroke-width="1.9" stroke-dasharray="9 6"/>')
    s.texte(130, 356, "ajout hypothétique de l'Équipe E", 11.5, ancre="start", coul="#7a2a55")
    s.e.append(f'<line x1="60" y1="374" x2="120" y2="374" stroke="{N}" stroke-width="2.4" stroke-dasharray="7 5"/>')
    s.texte(130, 378, "tirets d'origine de DOC-008 (3 → 2)", 11.5, ancre="start")
    s.sortie(ICI / "schema_electrique_hypothetique.svg")


def main():
    architecture()
    unifilaire()
    print("écrit : architecture_fonctionnelle.svg, schema_electrique_hypothetique.svg")


if __name__ == "__main__":
    main()
