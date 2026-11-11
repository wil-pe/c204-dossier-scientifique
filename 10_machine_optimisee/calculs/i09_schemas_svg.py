#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i09 : schémas fonctionnels SVG des trois paliers (générés par script, valeurs lues dans les résultats).

  schemas/schema_fonctionnel_R1.svg   chaîne de mesure du palier 1 (coffre seul + options hors coffre)
  schemas/schema_fonctionnel_R2.svg   quatre modules du palier 2 et ce que chacun mesure ou simule
  schemas/schema_fonctionnel_R3.svg   voies du palier 3, statut physique et verrou de chaque voie
  schemas/correspondance_C204_R1.svg  correspondance visuelle : élément d'origine → remplaçant R1

Code couleur des cadres : sous-système (mêmes teintes que le modèle 3D). Trait plein = flux de données ou d'énergie ;
tirets = option hors coffre ; pointillé rouge = chaîne de sécurité. Aucun flux « temporel » n'est représenté, car il n'y en a pas.
"""
import json
from html import escape

from i00_commun import RES, SCH

r1 = json.loads((RES / "i01_deplacement.json").read_text(encoding="utf-8"))
r2 = json.loads((RES / "i02_bilans_R1.json").read_text(encoding="utf-8"))
r3 = json.loads((RES / "i03_demonstrateurs.json").read_text(encoding="utf-8"))
r5 = json.loads((RES / "i05_palier3.json").read_text(encoding="utf-8"))
r8 = json.loads((RES / "i08_bilans_R2.json").read_text(encoding="utf-8"))

COL = {"temps": "#2a78d6", "energie": "#eb6834", "calcul": "#1baf7a", "gravite": "#eda100", "principal": "#e87ba4", "direction": "#008300",
       "thermique": "#6250d6", "securite": "#e34948", "neutre": "#6b7280", "sortie": "#0b0b0b",
       "demontre": "#1baf7a", "possible": "#eda100", "speculatif": "#e87ba4", "contredit": "#e34948"}
ENCRE, ENCRE2, FOND = "#0b0b0b", "#52514e", "#fcfcfb"
fv = lambda x, n=2: (f"{x:.{n}f}").replace(".", ",").replace("-", "−")


def sci(x):
    m, e = f"{x:.1e}".split("e")
    return m.replace(".", ",") + "×10" + str(int(e)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


class Svg:
    def __init__(self, w, h, titre, sous_titre):
        self.w, self.h, self.e, self.boites = w, h, [], {}
        self.e.append(f'<rect width="{w}" height="{h}" fill="{FOND}"/>')
        self.e.append(f'<text x="24" y="36" font-size="20" font-weight="700" fill="{ENCRE}">{escape(titre)}</text>')
        for i, l in enumerate(sous_titre):
            self.e.append(f'<text x="24" y="{60 + 18 * i}" font-size="13" fill="{ENCRE2}">{escape(l)}</text>')

    def boite(self, cle, x, y, w, h, titre, lignes=(), coul="neutre", tirets=False, plein=False):
        c = COL[coul]
        self.boites[cle] = (x, y, w, h)
        dash = ' stroke-dasharray="7 4"' if tirets else ""
        fill = c if plein else "#ffffff"
        tcol = "#ffffff" if plein else ENCRE
        self.e.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{c}" stroke-width="2.2"{dash}/>')
        if not plein:
            self.e.append(f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3" fill="{c}"/>')
        self.e.append(f'<text x="{x + 16}" y="{y + 20}" font-size="13" font-weight="700" fill="{tcol}">{escape(titre)}</text>')
        if 6.6 * len(titre) > w - 22:
            print("  [largeur] titre trop long pour", cle, ":", titre, "(%d > %d)" % (6.6 * len(titre), w - 22))
        for l in lignes:
            if 5.7 * len(l) > w - 22:
                print("  [largeur] ligne trop longue pour", cle, ":", l, "(%d > %d)" % (5.7 * len(l), w - 22))
        if lignes and 38 + 15.5 * (len(lignes) - 1) > h - 6:
            print("  [hauteur] trop de lignes pour", cle)
        for i, l in enumerate(lignes):
            self.e.append(f'<text x="{x + 16}" y="{y + 38 + 15.5 * i}" font-size="11.5" fill="{tcol if plein else ENCRE2}">{escape(l)}</text>')

    def ancre(self, cle, cote, t=0.5):
        x, y, w, h = self.boites[cle]
        return {"g": (x, y + h * t), "d": (x + w, y + h * t), "h": (x + w * t, y), "b": (x + w * t, y + h)}[cote]

    def fleche(self, a, ca, b_, cb, etiquette="", tirets=False, coul=None, ta=0.5, tb=0.5, coude=None, style=None):
        (x1, y1), (x2, y2) = self.ancre(a, ca, ta), self.ancre(b_, cb, tb)
        c = coul or ENCRE2
        if coude is None:
            pts = [(x1, y1), (x2, y2)] if (abs(x1 - x2) < 1 or abs(y1 - y2) < 1) else ([(x1, y1), ((x1 + x2) / 2, y1), ((x1 + x2) / 2, y2), (x2, y2)] if ca in "gd" else [(x1, y1), (x1, (y1 + y2) / 2), (x2, (y1 + y2) / 2), (x2, y2)])
        else:
            pts = [(x1, y1)] + coude + [(x2, y2)]
        d = " ".join(("M" if i == 0 else "L") + f"{px:.1f},{py:.1f}" for i, (px, py) in enumerate(pts))
        dash = ' stroke-dasharray="6 4"' if tirets else (' stroke-dasharray="2 4"' if style == "pointille" else "")
        mid = "fl" + c.strip("#")
        self.e.insert(1, f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker></defs>')
        self.e.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="1.6"{dash} marker-end="url(#{mid})"/>')
        if etiquette:
            k = len(pts) // 2
            mx, my = (pts[k - 1][0] + pts[k][0]) / 2, (pts[k - 1][1] + pts[k][1]) / 2
            self.e.append(f'<text x="{mx:.1f}" y="{my - 5:.1f}" font-size="10.5" fill="{ENCRE2}" text-anchor="middle" stroke="{FOND}" stroke-width="4" paint-order="stroke">{escape(etiquette)}</text>')

    def texte(self, x, y, t, taille=11.5, gras=False, coul=None, ancre="start", italique=False):
        self.e.append(f'<text x="{x}" y="{y}" font-size="{taille}" {"font-weight=\"700\" " if gras else ""}{"font-style=\"italic\" " if italique else ""}fill="{coul or ENCRE2}" text-anchor="{ancre}">{escape(t)}</text>')

    def legende(self, x, y, items):
        for i, (c, l) in enumerate(items):
            self.e.append(f'<rect x="{x}" y="{y + 20 * i - 10}" width="14" height="12" rx="2" fill="{COL[c]}"/>')
            self.texte(x + 22, y + 20 * i, l, 11.5, coul=ENCRE)

    def ecrire(self, nom):
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" font-family="DejaVu Sans, Arial, Helvetica, sans-serif">\n'
             + "\n".join(self.e) + "\n</svg>\n")
        (SCH / nom).write_text(s, encoding="utf-8")
        return nom


def schema_R1():
    A = r2["R1-A"]
    S = r1["scenarios"]
    mu = r3["muons"]["geometries"]["d=10cm"]
    det = r1["detectabilite_48h"]
    s = Svg(1500, 980, "C204-R1 — schéma fonctionnel du « chronomètre-gravimètre relativiste embarqué »",
            ["Palier 1 : dans le coffre de 0,85 m, sur batterie. L'unité CALCULE le décalage relativiste de son trajet (≈ ns/h) ; elle ne le MESURE qu'avec le module externe et une référence au sol (tirets).",
             "Ce décalage est celui de tout objet transporté : l'unité n'en est pas la cause. Jamais vers le passé. Valeurs : scripts i01 à i03."])
    # colonne capteurs
    s.boite("csac", 30, 110, 300, 92, "4 horloges au césium miniatures (R1-06)", ["3×10⁻¹⁰ à 1 s ; 0,48 W ; 140 g", "sous blindage magnétique et régulation", "thermique (R1-09)"], "temps")
    s.boite("gnss", 30, 216, 300, 62, "Récepteur GNSS à sortie de temps (R1-08)", ["position, altitude, vitesse, cap ; 1 PPS"], "temps")
    s.boite("csext", 30, 292, 300, 92, "HORS COFFRE : césiums à jet (R1-B1)", ["30 kg et 425 × 524 × 133 mm chacun : hors coffre", f"S/B ≈ {fv(det['Césium à jet 5071A, tube haute performance']['SB']['1000'], 1)} pour 48 h à +1 000 m (1 horloge)", "+ référence au sol : 3 étalons ou lien de temps"], "temps", tirets=True)
    s.boite("acc", 30, 420, 300, 62, "Accéléromètres à quartz « VGL » (R1-12)", ["pesanteur à ~1 mGal ; inclinaison"], "gravite")
    s.boite("baro", 30, 496, 300, 62, "Baromètre, magnétomètre (R1-13)", ["altitude, grandeurs d'influence"], "gravite")
    s.boite("grav", 30, 572, 300, 76, "OPTION : gravimètre µGal (R1-22)", ["5 µGal, à l'arrêt, posé au sol", "tient dans le coffre seulement si L ≥ 0,9 m"], "gravite", tirets=True)
    s.boite("sagnac", 30, 684, 300, 92, "LOGEMENT DE DIRECTION", ["gyromètre Sagnac à fibre (R1-15)", "Δt = " + sci(r3['sagnac']['rotation terrestre, composante verticale à 45°']['decalage_temporel_s']) + " s (rotation terrestre)", "→ vitesse de rotation, cap"], "direction")
    s.boite("muons", 30, 790, 300, 92, "LOGEMENT PRINCIPAL", ["télescope à muons cosmiques (R1-14)", f"{mu['par_heure']:.0f} coïncidences/h ; cône de ±{mu['demi_angle_max_deg']:.0f}°", "→ dilatation du temps de particules naturelles"], "principal")
    s.boite("geiger", 30, 896, 300, 56, "Dosimètre à semi-conducteur (R1-18)", ["fond naturel ; aucune source ; ≤ 30 V"], "securite")
    # centre
    s.boite("comp", 420, 150, 290, 92, "Comparateur de phase à 6 voies (R1-07)", ["écarts d'horloges deux à deux", "résolution < 0,1 ns ; détection d'une", "horloge fautive (vote sur 4)"], "temps")
    s.boite("calc", 420, 420, 290, 150, "3 calculateurs dissemblables (R1-10)", ["+ voteur médian matériel (R1-11)", "y = ΔW/c² − v²/2c² − Ω·R·cosφ·v_est/c²", "intégration le long du trajet ;", "enregistrement chaîné par empreinte ;", "tolère une panne franche (pas byzantine)"], "calcul")
    s.boite("stat", 420, 760, 290, 92, "Comptage et datation des muons (R1-16)", ["taux selon l'altitude ;", "sans dilatation : ×" + f"{r3['muons']['rapport_sans_dilatation_dh=2000']:.0f}" + " entre 2 000 m", "et la plaine (attendu : ×1,3 à 2)"], "principal")
    # sorties
    s.boite("pred", 800, 330, 330, 110, "DÉCALAGE RELATIVISTE DU TRAJET (calculé)", [f"+1 000 m : l'objet vieillit {fv(S['S01']['avance_horloge_ns_par_h'])} ns/h de plus", f"130 km/h vers l'est : {fv(S['S05']['D_futur_ns_par_h'])} ns/h de moins", f"130 km/h vers l'ouest : {fv(abs(S['S06']['D_futur_ns_par_h']))} ns/h de plus", "même valeur pour un lest : l'unité n'y est pour rien"], "sortie")
    s.boite("mes", 800, 150, 330, 110, "DÉCALAGE MESURÉ (écart d'horloges)", ["coffre seul : NON (CSAC : S/B ≈ " + f"{det['CSAC au césium (SA.45s)']['SB']['1000']:.3f}".replace(".", ",") + ")", "module césium + référence au sol :", "19 ns en 48 h à +1 000 m", "jamais d'inversion de l'ordre des événements"], "sortie")
    s.boite("dil", 800, 760, 330, 92, "DILATATION OBSERVÉE (muons naturels)", ["facteur effectif ≳ 7 d'après le rapport de taux", "(Frisch & Smith 1963 : 8,8 ± 0,8)", "l'unité observe, elle ne produit rien"], "sortie")
    s.boite("ihm", 1210, 250, 260, 110, "Pupitre, télécommande (R1-19, 20)", ["écran de secours, clavier, voyants,", "avertisseur ; saisie du scénario ;", "affichage prédit / mesuré"], "securite")
    s.boite("comparaison", 1210, 420, 260, 92, "Test : mesuré − prédit", ["écart nul attendu (relativité générale) ;", "protocole en aveugle de l'expérience", "EXP-12 (Équipe F)"], "calcul")
    # servitudes
    s.boite("batt", 800, 560, 200, 76, "Batterie 1,34 kWh (R1-03)", [f"{A['autonomie_mesure_h']:.0f} h en mesure ({A['puissance_mesure_W']:.0f} W)", f"{A['autonomie_transport_h']:.0f} h en transport ({A['puissance_transport_W']:.0f} W)"], "energie")
    s.boite("dist", 1030, 560, 210, 76, "Distribution ≤ 24 V (R1-04)", ["vers tous les sous-ensembles ;", "≈ 30 V au plus (photodétecteurs)"], "energie")
    s.boite("au", 1270, 560, 200, 76, "Arrêt d'urgence (R1-05)", ["coupe la batterie :", "état sûr réel"], "securite")
    s.boite("therm", 800, 656, 385, 62, "Boucle thermique : pompe, 2 réservoirs (R1-17)", [f"évacue {A['puissance_mesure_W']:.0f} W ; coffre à ~{r2['thermique']['R1-A mesure (géométrie E)']['temperature_C']:.0f} °C pour 20 °C d'ambiance"], "thermique")
    # flèches
    s.fleche("csac", "d", "comp", "g", "10 MHz, 1 PPS", tb=0.35)
    s.fleche("gnss", "d", "comp", "g", "", tb=0.7)
    s.fleche("csext", "d", "comp", "g", "hors coffre", tirets=True, tb=0.9)
    s.fleche("gnss", "d", "calc", "g", "h, v, cap", ta=0.8, tb=0.12, coude=[(375, 265.6), (375, 438)])
    s.fleche("acc", "d", "calc", "g", "g", tb=0.3)
    s.fleche("baro", "d", "calc", "g", "", tb=0.55)
    s.fleche("grav", "d", "calc", "g", "g (µGal)", tirets=True, tb=0.75, coude=[(385, 610), (385, 532.5)])
    s.fleche("sagnac", "d", "calc", "g", "Ω, cap", tb=0.92, coude=[(395, 730), (395, 558)])
    s.fleche("muons", "d", "stat", "g", "impulsions")
    s.fleche("comp", "d", "mes", "g", "écarts (ns)", tb=0.4)
    s.fleche("comp", "b", "calc", "h", "temps de l'unité")
    s.fleche("calc", "d", "pred", "g", "", tb=0.7, coude=[(755, 495), (755, 407)])
    s.fleche("stat", "d", "dil", "g", "")
    s.fleche("mes", "d", "ihm", "g", "", tb=0.3, coude=[(1170, 205), (1170, 283)])
    s.fleche("pred", "d", "ihm", "g", "", tb=0.75, coude=[(1170, 385), (1170, 332.5)])
    s.fleche("pred", "d", "comparaison", "g", "", ta=0.9, coude=[(1185, 429), (1185, 466)])
    s.fleche("batt", "d", "dist", "g", "")
    s.fleche("au", "g", "dist", "d", "coupure", coul=COL["securite"], style="pointille")
    s.fleche("therm", "g", "calc", "b", "refroidit horloges et calculateurs", coude=[(565, 687)])
    s.legende(1210, 720, [("temps", "temps"), ("calcul", "calcul et vote"), ("gravite", "gravité, inertie"), ("direction", "logement de direction"),
                          ("principal", "logement principal"), ("energie", "énergie"), ("thermique", "thermique"), ("securite", "sécurité, pupitre")])
    s.texte(1210, 890, "Tirets : option hors coffre.", 11)
    s.texte(1210, 906, "Cadre noir : grandeur de sortie.", 11)
    s.texte(1210, 922, f"Masse R1-A : {A['masse_kg']:.0f} kg ; coût ≈ {A['cout_EUR'] / 1000:.0f} k€ (estimation).", 11)
    return s.ecrire("schema_fonctionnel_R1.svg")


def schema_R2():
    T = r8["total"]
    s = Svg(1500, 900, "C204-R2 — schéma fonctionnel du palier « laboratoire de recherche »",
            ["Quatre modules et des communs ; ≈ " + fv(T['masse_kg'] / 1000, 1) + " t, ≈ " + fv(T['puissance_W'] / 1000, 1) + " kW, ≈ " + fv(T['cout_kEUR'] / 1000, 1) + " M€ (estimations). M1 et M2 MESURENT ; M3 et M4 SIMULENT.",
             "Aucun module ne transmet d'information vers le passé. Valeurs : scripts i04 et i08 ; performances d'horloges et de gravimètres : résumés d'articles vérifiés."])
    y0 = 110
    s.boite("m1a", 30, y0, 330, 110, "M1 — Horloge optique à ion n° 1 (R2-01)", ["piège de Paul, refroidissement laser,", "canon d'ionisation, photomultiplicateur", "incertitude 10⁻¹⁸ à 10⁻¹⁹", "(= « singularité principale »)"], "temps")
    s.boite("m1b", 30, y0 + 124, 330, 110, "M1 — Horloge optique à ion n° 2 (R2-02)", ["identique, sur plateforme réglable 0–1 m", "Δf/f = 1,09×10⁻¹⁶ par mètre", "(= « singularité de direction »)"], "temps")
    s.boite("lien", 400, y0 + 40, 280, 76, "Lien fibré stabilisé (R2-03)", ["comparaison de fréquence < 10⁻¹⁸", "+ horloge à iode de 35 L (volant)"], "temps")
    s.boite("s1", 740, y0, 360, 124, "MESURE : décalage gravitationnel et cinématique", ["résolution 3,6×10⁻¹⁵ s par heure (10⁻¹⁸)", "9 mm de dénivelé à 10⁻¹⁸ ; 0,9 mm à 10⁻¹⁹", "signal du palier 1 (10⁻¹³) vu à ~10⁵ σ", "verrait 2 × 4,4×10¹² kg jusqu'à 6,5 km"], "sortie")
    s.boite("m2", 30, y0 + 270, 330, 110, "M2 — Gravimètre et gradiomètre atomiques", ["absolu : stabilité < 1 µGal (R2-06)", "gradient : 20 E, 0,1 E à long terme (R2-07)", "nivellement, GNSS géodésique (R2-09)"], "gravite")
    s.boite("s2", 740, y0 + 270, 360, 110, "MESURE : pesanteur ; PRÉDICTION ΔW = ∫g·dh", ["1 µGal ↔ 3,2 mm de dénivelé", "une tonne détectée à 1,5 m (3 σ)", "prédiction du décalage d'horloge à ~10⁻⁵ près"], "sortie")
    s.boite("test", 1150, y0 + 110, 320, 124, "TEST DE LA RELATIVITÉ GÉNÉRALE", ["horloges (M1) contre géodésie (M2) :", "le rapport doit valoir 1 ;", "toute « distorsion de gravité » locale", "au-delà de 10⁻¹⁸ serait vue"], "calcul")
    s.boite("m3", 30, y0 + 420, 330, 124, "M3 — Cuve à deux vortex (R2-10 à R2-13)", ["3 m × 1,5 m, h = 6,25 cm, 2 orifices", "batteur à houle, profilométrie optique", "(= « deux singularités dans un", "champ de Kerr », DOC-009)"], "thermique")
    s.boite("s3", 740, y0 + 420, 360, 124, "SIMULATION ANALOGIQUE : ondes sur écoulement", ["horizon et ergorégion pour des ONDES DE SURFACE", "superradiance : jusqu'à 20 % (un vortex, publié)", "inédit : couplage de deux ergorégions", "ne dit rien de la gravité ni du temps"], "sortie")
    s.boite("m4", 30, y0 + 584, 330, 124, "M4 — Banc de causalité quantique (R2-14, 15)", ["paires de photons, post-sélection ;", "processeur quantique en nuage", "P-CTC, D-CTC simulées,", "interrupteur quantique"], "principal")
    s.boite("s4", 740, y0 + 584, 360, 124, "SIMULATION : cohérence logique d'une boucle", ["« grand-père » : 0 essai post-sélectionné", "Deutsch : discrimination parfaite de |0⟩ et |−⟩", "(impossible en mécanique quantique linéaire)", "circuits ordonnés : rien ne remonte le temps"], "sortie")
    s.boite("com", 1150, y0 + 624, 320, 110, "Communs", ["3 calculateurs à vote, acquisition en", "aveugle (R2-18) ; hodoscope à muons ;", "centrale inertielle ; abri climatisé ;", "interverrouillages et arrêt d'urgence"], "calcul")
    s.fleche("m1a", "d", "lien", "g", "", tb=0.3)
    s.fleche("m1b", "d", "lien", "g", "", tb=0.7)
    s.fleche("lien", "d", "s1", "g", "")
    s.fleche("m2", "d", "s2", "g", "g, gradient vertical, dénivelés")
    s.fleche("s1", "d", "test", "g", "")
    s.fleche("s2", "d", "test", "b", "", coude=[(1310, 435)])
    s.fleche("m3", "d", "s3", "g", "champ de hauteur de la surface")
    s.fleche("m4", "d", "s4", "g", "coïncidences post-sélectionnées")
    s.legende(1150, y0 + 420, [("temps", "horloges (mesure)"), ("gravite", "gravimétrie (mesure)"), ("thermique", "analogue hydrodynamique (simulation)"),
                                ("principal", "optique quantique (simulation)"), ("calcul", "calcul, vote, test"), ("sortie", "résultat")])
    s.texte(1150, y0 + 560, "Simulation ≠ expérience sur l'espace-temps :", 11.5, gras=True, coul=ENCRE)
    s.texte(1150, y0 + 578, "M3 et M4 reproduisent des équations,", 11.5)
    s.texte(1150, y0 + 594, "pas une courbure ni une boucle causale.", 11.5)
    return s.ecrire("schema_fonctionnel_R2.svg")


def schema_R3():
    k998 = [d for d in r5["a2_gravite"] if "a/M = 0.998" in d["nom"]][0]
    s = Svg(1500, 860, "C204-R3 — palier « limite théorique » : voies que la physique connue n'interdit pas",
            ["Chaque voie : principe → valeur atteignable → verrou. Vert : démontré ; jaune : théoriquement possible ; rose : spéculatif ; rouge : contredit.",
             "Seule la colonne de droite concerne le passé, et elle exige une physique que rien n'indique aujourd'hui. Valeurs : script i05."])
    s.boite("but", 30, 110, 250, 120, "But revendiqué", ["Γ = 87 660 (« 10 ans par heure »)", "vers le passé, dans 227 kg,", "sur batterie"], "contredit", plein=True)
    cols = [
        ("a1", 320, "(a1) Vitesse", "demontre", ["dilatation cinématique γ", "muons en anneau : γ = 29,3 (réalisé)", "électrons du LEP : γ = 89 000 (réalisé)", "rendement : τ/(m·c²), indépendant de γ"],
         ["227 kg à Γ revendiqué : 1,8×10²⁴ J", "(2 900 ans d'énergie mondiale)", "à 1 g : 11,7 ans d'accélération", "anneau « habitable » à 1 g :", "rayon de 830 années-lumière (γ = 29)"], "VERS LE FUTUR SEULEMENT"),
        ("a2", 610, "(a2) Gravité", "possible", ["orbite stable autour d'un trou noir", "de Kerr a/M = 0,998 : Γ = " + fv(k998['Gamma'], 1), "sans poussée ni pesanteur ressentie", "coût du retour : " + fv(k998['cout_retour_fraction_mc2']) + " m·c²"],
         ["Γ revendiqué : 1 − a/M = 4,6×10⁻¹⁵", "(limite admise : ~2×10⁻³)", "immobile près d'un horizon :", "3×10¹⁰ g de poussée", "trou noir supermassif à ~26 000 a.l."], "VERS LE FUTUR SEULEMENT"),
        ("b", 900, "(b) Trou noir moteur", "possible", ["rayonnement de Hawking :", "10⁹ kg → 6×10¹⁶ W pendant ~15 ans", "poussée ≤ P/c = 2×10⁸ N", "γ final ≈ 10 (η = 0,44 ; R = 1 000)"],
         ["fabrication ≥ 9×10²⁵ J ; pas de", "trou noir par concentration de lumière", "(Álvarez-Domínguez et al. 2024)", "aucun confinement ; aucun état sûr", "jamais observé"], "VERS LE FUTUR SEULEMENT"),
        ("c", 1190, "(c) Trou de ver", "speculatif", ["gorge de 2,5 m : −1,7×10²⁷ kg", "d'énergie négative (0,9 Jupiter)", "tension 8×10⁴¹ Pa", "décalage ≤ durée de fonctionnement"],
         ["inégalités quantiques : 10⁻²⁶ s", "condition d'énergie nulle moyennée", "protection chronologique", "jamais avant la mise en service :", "2036 → 1975 exclu par construction"], "PASSÉ : SEULEMENT SI ÉNERGIE NÉGATIVE MACROSCOPIQUE"),
    ]
    for cle, x, titre, coul, l1, l2, concl in cols:
        s.boite(cle, x, 110, 270, 120, titre, l1, coul)
        s.boite(cle + "v", x, 290, 270, 130, "Verrou", l2, "neutre")
        s.boite(cle + "c", x, 480, 270, 60, concl if len(concl) < 30 else "PASSÉ : seulement si…", (["énergie négative macroscopique"] if len(concl) >= 30 else []),
                "speculatif" if cle == "c" else "demontre", plein=True)
        s.fleche(cle, "b", cle + "v", "h")
        s.fleche(cle + "v", "b", cle + "c", "h")
    s.boite("d", 30, 600, 1430, 200, "(d) Ce qu'il faudrait découvrir pour qu'un déplacement vers le passé devienne envisageable — et les expériences qui le verraient", [
        "1. Une violation macroscopique et durable de la condition d'énergie nulle moyennée (énergie négative) → pesée de l'énergie du vide, géométries de Casimir, états comprimés : aucune indication.",
        "2. Une mécanique quantique non linéaire (interaction entre branches d'Everett) → tests de linéarité (Polkovnikov et al. 2023 ; Broz et al. 2023) : effets nuls à ce jour.",
        "3. L'échec de la protection chronologique en gravité quantique → aucun test direct ; indices théoriques contraires (holographie).",
        "4. Un prolongement régulier au-delà de l'horizon interne de Kerr → mathématiquement défavorisé (Dafermos & Luk 2025) ; inobservable de l'extérieur.",
        "5. Une échelle de Planck abaissée ou des trous noirs primordiaux légers (source de « micro-singularités ») → LHC (exclusion jusqu'à ~10 TeV), LHAASO (< 181 explosions par pc³ et par an) : rien.",
        "6. Une violation de l'invariance de Lorentz ou une propagation supraluminique → GW170817 (10⁻¹⁴), sursauts gamma : rien.",
        "Aucun de ces six résultats ne suffirait seul : il faudrait en outre une source d'énergie de l'ordre de la masse de Jupiter. Sources : Équipes B et H (références vérifiées)."], "neutre")
    s.fleche("but", "d", "a1", "g", "")
    s.legende(40, 290, [("demontre", "démontré"), ("possible", "théoriquement possible"), ("speculatif", "spéculatif"), ("contredit", "contredit")])
    return s.ecrire("schema_fonctionnel_R3.svg")


def schema_correspondance():
    paires = [
        ("Singularité principale (r.1)", "contredit", "Télescope à muons cosmiques", "principal"),
        ("Singularité de direction (r.2)", "contredit", "Gyromètre Sagnac à fibre", "direction"),
        ("Logements et bobines magnétiques", "contredit", "Carters, bobine de fibre, blindage des horloges", "temps"),
        ("Injection d'électrons (r.4-5-6)", "contredit", "Distribution électrique ≤ 24 V", "energie"),
        ("Capteur de singularité (r.7)", "speculatif", "Photodétecteurs des deux démonstrateurs", "principal"),
        ("Refroidissement (r.8-9-10)", "contredit", "Boucle thermique : pompe, 2 réservoirs", "thermique"),
        ("« Évent à rayons X »", "contredit", "Cône d'acceptance + dosimètre du fond naturel", "securite"),
        ("Capteurs de gravité VGL (r.11)", "contredit", "Accéléromètres ; gravimètre amovible en option", "gravite"),
        ("4 horloges au césium", "demontre", "4 horloges au césium miniatures (+ module externe)", "temps"),
        ("3 calculateurs à vote", "demontre", "3 calculateurs dissemblables + voteur médian", "calcul"),
        ("Batterie (r.12)", "contredit", "Batterie LiFePO4 1,34 kWh", "energie"),
        ("Télécommande (r.3)", "demontre", "Télécommande filaire à bus CAN", "securite"),
        ("Arrêt d'urgence (r.5)", "contredit", "Relais de sécurité : état sûr réel", "securite"),
        ("Coffre de 227 kg", "contredit", "Coffre de 36 kg (206 kg avec module césium)", "neutre"),
    ]
    s = Svg(1240, 150 + 46 * len(paires), "Correspondance : élément de la C204 décrite → composant réel du palier R1",
            ["À gauche, la fonction revendiquée et son verdict physique (rouge : contredit ; rose : spéculatif ; vert : démontré). À droite, ce qui la remplace.",
             "Détail chiffré : correspondance_composants.csv."])
    for i, (g, st, d, c) in enumerate(paires):
        y = 100 + 46 * i
        s.boite(f"g{i}", 40, y, 420, 36, g, [], st)
        s.boite(f"d{i}", 640, y, 560, 36, d, [], c)
        s.fleche(f"g{i}", "d", f"d{i}", "g")
    return s.ecrire("correspondance_C204_R1.svg")


if __name__ == "__main__":
    print("schémas écrits :", schema_R1(), schema_R2(), schema_R3(), schema_correspondance())
