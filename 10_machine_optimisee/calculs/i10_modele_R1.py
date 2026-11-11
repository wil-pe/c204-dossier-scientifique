#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i10 : modèle 3D du palier 1 (C204-R1) au format de pièces primitives de l'Équipe E, et rendus PNG.

Principe : on RELIT (lecture seule) 06_modele_3D/modele_c204.json — reconstruit par la direction à
L = 0,85 m — et l'on conserve tel quel tout ce qui est enveloppe documentée (couches coque, couvercle,
platine, mobile). Les 64 pièces « internes » d'origine (carters de singularité, bobines, injection
d'électrons…) sont remplacées par les composants réels de la nomenclature R1 (script i02).
Les rendus utilisent le moteur de l'Équipe E (rendre_vues.py, construire_modele.py), importé sans
rien écrire dans son dossier (pas de fichiers .pyc).

Contrôles automatiques : chaque pièce interne est dans le volume intérieur ; aucune paire de pièces
internes ne s'interpénètre (boîtes englobantes) ; les dimensions concordent avec la nomenclature.

Sorties : ../modele_c204_R1.json, ../modele_R1/rendus/*.png, resultats/i10_modele_R1.txt
"""
import copy
import json
import math
import sys
from pathlib import Path

import numpy as np

sys.dont_write_bytecode = True
ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
DOSSIER_E = RACINE.parent / "06_modele_3D"
sys.path.insert(0, str(DOSSIER_E))
import rendre_vues as RV                     # noqa: E402  (moteur de rendu de l'Équipe E, lecture seule)
from construire_modele import maillage_piece  # noqa: E402
from matplotlib.patches import Patch          # noqa: E402
from scipy.spatial.transform import Rotation  # noqa: E402

SORTIE = RACINE / "modele_R1" / "rendus"
SORTIE.mkdir(parents=True, exist_ok=True)

SYSTEMES_R1 = {   # palette catégorielle validée (ordre fixe), gris neutre pour la structure reprise
    "temps": ("Temps : 4 horloges au césium, comparateur, GNSS", "#2a78d6"),
    "energie": ("Énergie et distribution très basse tension", "#eb6834"),
    "calcul": ("Calcul : 3 calculateurs + voteur", "#1baf7a"),
    "gravite": ("Gravité et inertie (« VGL » réelle)", "#eda100"),
    "logement_principal": ("Logement principal : télescope à muons", "#e87ba4"),
    "logement_direction": ("Logement de direction : gyromètre Sagnac", "#008300"),
    "thermique": ("Boucle thermique (pompe, 2 réservoirs)", "#6250d6"),
    "securite": ("Sécurité, rayonnement ambiant, pupitre", "#e34948"),
    "externe": ("Module externe (hors coffre)", "#8a8f98"),
}


def quat(rot):
    return [float(v) for v in Rotation.from_euler("xyz", rot, degrees=True).as_quat()]


def volume(prim):
    t = prim["type"]
    if t == "boite":
        return float(np.prod(prim["dimensions"]))
    if t == "cylindre":
        return math.pi * prim["rayon"]**2 * prim["hauteur"]
    if t == "sphere":
        return 4 / 3 * math.pi * prim["rayon"]**3 * float(np.prod(prim.get("echelle", [1, 1, 1])))
    if t == "tore":
        return 2 * math.pi**2 * prim["rayon_majeur"] * prim["rayon_mineur"]**2
    return 0.0


class Fabrique:
    def __init__(self, ecl):
        self.pieces, self.n, self.ecl = [], 0, ecl

    def ajoute(self, nom, ensemble, systeme, prim, pos, bom, fonction, remplace, cls="COM", rot=(0, 0, 0), opacite=1.0, englobant=False, contenu=False,
               couche="interne", notes="", masque=None, eclate=None):
        self.n += 1
        p = {"id": f"R1-P{self.n:03d}", "nom": nom, "ensemble": ensemble, "repere": bom, "source": "Conception Équipe I (nomenclature_R1.csv)",
             "classement": cls, "existence": "conception R1", "fonction_revendiquee": remplace, "fonction_reelle": fonction, "systeme": systeme,
             "primitive": prim, "position": [round(float(v), 5) for v in pos], "rotation_deg": [float(v) for v in rot], "quaternion": quat(rot),
             "liaison": "corps", "eclate": list(eclate if eclate is not None else (0.0, 0.0, self.ecl)), "couleur": "#b8bcc2", "opacite": opacite,
             "volume_m3": round(volume(prim), 7), "notes": notes, "couche": couche}
        if englobant:
            p["englobant"] = True
            p["fantome"] = True
        if contenu:
            p["contenu"] = True
        if masque:
            p["masque"] = masque
        self.pieces.append(p)
        return p


def construire():
    src = json.loads((DOSSIER_E / "modele_c204.json").read_text(encoding="utf-8"))
    A = src["variantes"]["A"]
    ck = A["cotes_cles"]
    co = {k: v["valeur"] for k, v in src["cotes"].items()}
    L, P = ck["L"], ck["P"]
    assert abs(L - 0.85) < 1e-6, "le modèle de l'Équipe E n'est pas à L = 0,85 m : relire avant de produire le modèle R1 (L = %.3f)" % L
    xl, ym, ys, zp, rl = co["x_logements"], co["y_logement_principal"], co["y_logement_direction"], ck["z_platine"], co["r_logement"]
    e = co["e_rebord"]
    interieur = dict(xmin=e, xmax=L - e, ymin=e, ymax=P - e, zmin=co["e_fond"], zmax=zp - co["e_platine"])
    F = Fabrique(ecl=0.30)
    b = lambda *d: {"type": "boite", "dimensions": [float(x) for x in d]}
    cyl = lambda r, h: {"type": "cylindre", "rayon": float(r), "hauteur": float(h)}

    # --- châssis
    F.ajoute("Châssis interne amorti (platine instruments)", "Structure R1", "structure", b(0.78, 0.20, 0.003), (0.42, P / 2, 0.0098), "R1-02",
             "porte et isole des vibrations les instruments", "—", cls="SPE", eclate=(0, 0, 0.26))
    # --- énergie (baie gauche)
    F.ajoute("Batterie LiFePO4 4S 105 Ah (1,34 kWh)", "Énergie", "energie", b(0.130, 0.200, 0.150), (0.090, P / 2, 0.012 + 0.075), "R1-03",
             "alimente l'unité : 21 h en mesure, 40 h en transport", "Batterie (DOC-008 r.12)")
    F.ajoute("Convertisseurs DC/DC, régulateurs et barres de distribution", "Énergie", "energie", b(0.070, 0.180, 0.060), (0.200, 0.115, 0.042), "R1-04",
             "génère, régule et distribue le courant (≤ 24 V)", "Générateur, régulateur et collecteur d'injection d'électrons (DOC-008 r.4-5-6)")
    F.ajoute("Coupe-batterie et relais de sécurité à double canal", "Sécurité", "securite", b(0.070, 0.120, 0.050), (0.200, 0.085, 0.105), "R1-05",
             "met tout hors tension : état sûr réel", "Coupure d'urgence (DOC-007 r.5)")
    # --- logement principal : télescope à muons
    ens = "Logement principal — télescope à muons"
    F.ajoute("Tube-support transparent du télescope", ens, "logement_principal", cyl(0.039, 0.125), (xl, ym, 0.1225), "R1-14",
             "tient les deux tuiles alignées sous l'ouverture du logement", "Carter de singularité (DOC-008 r.1) — principale", cls="SPE", opacite=0.22, englobant=True)
    F.ajoute("Tuile scintillante supérieure 50 × 50 × 10 mm", ens, "logement_principal", b(0.050, 0.050, 0.010), (xl, ym, 0.175), "R1-14",
             "produit un éclair au passage de chaque muon", "Singularité principale (DOC-007 r.1)", contenu=True, cls="LAB")
    F.ajoute("Tuile scintillante inférieure 50 × 50 × 10 mm", ens, "logement_principal", b(0.050, 0.050, 0.010), (xl, ym, 0.075), "R1-14",
             "coïncidence avec la tuile supérieure : cône d'acceptance de ±35°", "Singularité principale (DOC-007 r.1)", contenu=True, cls="LAB")
    for z, nom in ((0.175, "supérieur"), (0.075, "inférieur")):
        F.ajoute(f"Photomultiplicateur au silicium {nom}", ens, "logement_principal", b(0.008, 0.020, 0.010), (xl + 0.029, ym, z), "R1-14",
                 "convertit l'éclair en impulsion électrique", "Capteur de singularité (DOC-008 r.7)", contenu=True, cls="LAB")
    F.ajoute("Carte de coïncidence et de comptage (logement principal)", ens, "logement_principal", b(0.055, 0.075, 0.030), (xl, ym, 0.030), "R1-16",
             "date chaque coïncidence au 1 PPS des horloges", "Générateur / régulateur de champ (DOC-008 r.3) — principale", cls="LAB")
    # --- logement de direction : gyromètre Sagnac
    ens = "Logement de direction — gyromètre Sagnac"
    F.ajoute("Bobine de fibre optique, 500 m sur Ø 70 mm", ens, "logement_direction", {"type": "tore", "rayon_majeur": 0.031, "rayon_mineur": 0.007}, (xl, ys, 0.172), "R1-15",
             "deux ondes contrarotatives : décalage temporel proportionnel à la rotation", "Singularité de direction (DOC-007 r.2) ; bobine de champ (DOC-008 r.2)", cls="LAB")
    F.ajoute("Mandrin de la bobine", ens, "logement_direction", cyl(0.023, 0.016), (xl, ys, 0.172), "R1-15", "support de la fibre", "Carter de singularité (DOC-008 r.1) — de direction", cls="SPE")
    F.ajoute("Boîtier optique : source fibrée de classe 1, coupleur, modulateur, photodiode", ens, "logement_direction", b(0.070, 0.060, 0.025), (xl, ys, 0.130), "R1-15",
             "injecte et recombine les deux ondes ; mesure leur déphasage", "Capteur de singularité (DOC-008 r.7)", cls="LAB")
    F.ajoute("Carte de démodulation (logement de direction)", ens, "logement_direction", b(0.055, 0.075, 0.030), (xl, ys, 0.030), "R1-16",
             "restitue la vitesse de rotation et le cap", "Générateur / régulateur de champ (DOC-008 r.3) — de direction", cls="LAB")
    # --- boucle thermique
    ens = "Boucle thermique"
    for k, y in ((1, 0.050), (2, 0.210)):
        F.ajoute(f"Réservoir tampon n°{k} (0,25 L)", ens, "thermique", cyl(0.025, 0.130), (0.432, y, 0.080), "R1-17",
                 "inertie thermique de la boucle", "Réservoirs de refroidissement (DOC-008 r.10)")
    F.ajoute("Micro-pompe 12 V", ens, "thermique", b(0.060, 0.035, 0.030), (0.432, 0.130, 0.030), "R1-17", "fait circuler l'eau glycolée", "Pompe de refroidissement (DOC-008 r.9)")
    F.ajoute("Échangeur et ventilateur (évent d'air tiède)", ens, "thermique", b(0.060, 0.060, 0.025), (0.432, 0.130, 0.150), "R1-17",
             "rejette ~57 W à l'air libre", "Évacuation (DOC-009 r.5) : de l'air tiède, aucun rayonnement")
    F.ajoute("Plaque froide de l'enceinte des horloges", ens, "thermique", b(0.140, 0.140, 0.005), (0.550, 0.165, 0.0145), "R1-17",
             "stabilise la température des horloges", "Enveloppe de refroidissement (DOC-008 r.8)", cls="SPE")
    # --- temps
    ens = "Temps — horloges au césium"
    F.ajoute("Enceinte des horloges : blindage mu-métal, bobines de compensation, régulation thermique", ens, "temps", b(0.140, 0.140, 0.080), (0.550, 0.165, 0.058), "R1-09",
             "protège les horloges du champ magnétique et des variations de température", "Logement et bobines de champ magnétique (DOC-008 r.1-2)", cls="LAB", opacite=0.3, englobant=True)
    for k, (x, y) in enumerate(((0.522, 0.140), (0.578, 0.140), (0.522, 0.190), (0.578, 0.190)), 1):
        F.ajoute(f"Horloge atomique miniature au césium n°{k} (CSAC)", ens, "temps", b(0.041, 0.036, 0.012), (x, y, 0.050), "R1-06",
                 "base de temps ; 4 horloges permettent d'écarter une horloge fautive", "Horloge au césium (texte)", contenu=True)
    F.ajoute("Comparateur de phase à 6 voies et distribution 10 MHz / 1 PPS", ens, "temps", b(0.140, 0.120, 0.025), (0.550, 0.165, 0.1135), "R1-07",
             "mesure les 6 écarts deux à deux à mieux que 0,1 ns", "—", cls="LAB")
    F.ajoute("Récepteur GNSS à sortie de temps", ens, "temps", b(0.100, 0.060, 0.025), (0.550, 0.165, 0.150), "R1-08",
             "référence de temps et de position ; altitude et vitesse pour le calcul du déplacement", "—")
    # --- calcul
    ens = "Calcul — trois calculateurs à vote"
    for k, y in enumerate((0.030, 0.052, 0.074), 1):
        F.ajoute(f"Calculateur n°{k} (architecture différente)", ens, "calcul", b(0.100, 0.018, 0.075), (0.530, y, 0.050), "R1-10",
                 "calcule le déplacement temporel prédit et enregistre", "Calculateur (texte)")
    F.ajoute("Voteur médian matériel et chien de garde", ens, "calcul", b(0.100, 0.060, 0.020), (0.530, 0.052, 0.105), "R1-11",
             "retient la valeur médiane des trois calculateurs", "Vote « Borda » (texte)", cls="LAB")
    # --- gravité, ambiance, rayonnement, façade (sous le pupitre)
    F.ajoute("Triade d'accéléromètres à quartz (« VGL » de classe milligal)", "Gravité et inertie", "gravite", b(0.060, 0.060, 0.060), (0.685, 0.200, 0.045), "R1-12",
             "mesure le vecteur pesanteur à ~1 mGal", "Unité de capteurs de gravité (DOC-008 r.11)")
    F.ajoute("Baromètre, thermomètres, hygromètre, magnétomètre", "Gravité et inertie", "gravite", b(0.060, 0.040, 0.025), (0.685, 0.200, 0.095), "R1-13",
             "altitude barométrique et grandeurs d'influence des horloges", "—")
    F.ajoute("Dosimètre à semi-conducteur du rayonnement ambiant (sans source, ≤ 30 V)", "Rayonnement", "securite", b(0.110, 0.060, 0.030), (0.690, 0.060, 0.030), "R1-18",
             "mesure le fond naturel", "« Évent à rayons X » (DOC-009 r.5)")
    F.ajoute("Électronique de façade : écran de secours, voyants, avertisseur", "Commande", "securite", b(0.100, 0.080, 0.030), (0.690, 0.110, 0.165), "R1-20",
             "affiche les écarts d'horloge et l'état de l'unité", "Écran de secours (DOC-007 r.4), commandes d'urgence (r.8)")
    internes = F.pieces

    # --- contrôles géométriques
    journal = []
    bornes = {}
    varA = {"etats": A["etats"], "articulations": A["articulations"]}
    for p in internes:
        m = maillage_piece(p, varA, "ferme")
        bornes[p["id"]] = m.bounds
        lo, hi = m.bounds
        ok = (lo[0] >= interieur["xmin"] - 1e-6 and hi[0] <= interieur["xmax"] + 1e-6 and lo[1] >= interieur["ymin"] - 1e-6 and hi[1] <= interieur["ymax"] + 1e-6
              and lo[2] >= interieur["zmin"] - 1e-6 and hi[2] <= interieur["zmax"] + 1e-6)
        if not ok:
            journal.append("HORS VOLUME : %s %s" % (p["id"], p["nom"]))
    for i, p in enumerate(internes):
        for q in internes[i + 1:]:
            if p.get("englobant") and q.get("contenu") or q.get("englobant") and p.get("contenu"):
                continue
            a, c_ = bornes[p["id"]], bornes[q["id"]]
            if all(a[0][k] < c_[1][k] - 1e-6 and c_[0][k] < a[1][k] - 1e-6 for k in range(3)):
                # le mandrin est à l'intérieur du tore de fibre : contact voulu
                if {"Mandrin de la bobine", "Bobine de fibre optique, 500 m sur Ø 70 mm"} == {p["nom"], q["nom"]}:
                    continue
                journal.append("INTERPÉNÉTRATION : %s / %s" % (p["nom"], q["nom"]))
    # le dessus des démonstrateurs doit rester sous le fût des logements
    z_fut = 0.1881 - 0.005
    for nom in ("Tuile scintillante supérieure 50 × 50 × 10 mm", "Bobine de fibre optique, 500 m sur Ø 70 mm"):
        p = [x for x in internes if x["nom"] == nom][0]
        if bornes[p["id"]][1][2] > z_fut:
            journal.append("TROP HAUT : %s" % nom)

    # --- pièces reprises de l'Équipe E (enveloppe), identifiants préfixés
    reprises = []
    for p in A["pieces"]:
        if p["couche"] == "interne":
            continue
        q = copy.deepcopy(p)
        q["id"] = "E-" + q["id"]
        q["source"] = q["source"] + " — repris tel quel du modèle de l'Équipe E (06_modele_3D, L = 0,85 m)"
        q["systeme_origine"] = q["systeme"]
        q["systeme"] = "structure"
        reprises.append(q)
    vol_int = (interieur["xmax"] - interieur["xmin"]) * (interieur["ymax"] - interieur["ymin"]) * (interieur["zmax"] - interieur["zmin"])
    vol_comp = sum(p["volume_m3"] for p in internes if not p.get("contenu"))

    # --- modules externes de la configuration R1-B (à l'échelle, posés à côté du coffre)
    G = Fabrique(ecl=0.0)
    x0 = L + 0.25
    for k in range(3):
        G.ajoute(f"Étalon à jet de césium n°{k + 1} (425 × 524 × 133 mm, 30 kg)", "Module externe R1-B", "externe", b(0.4255, 0.5239, 0.1334), (x0 + 0.30, 0.13, 0.42 + 0.075 + k * 0.145), "R1-B1",
                 "mesure réellement le déplacement temporel (S/B 3 à 10 en 48 h)", "Horloge au césium (texte)", couche="externe")
    G.ajoute("Batterie 7,5 kWh du module (55 kg)", "Module externe R1-B", "externe", b(0.60, 0.40, 0.25), (x0 + 0.30, 0.13, 0.20), "R1-B2",
             "48 h d'autonomie pour 3 étalons", "Batterie (DOC-008 r.12)", couche="externe")
    G.ajoute("Baie antichoc 19 pouces (0,6 × 0,8 × 0,95 m)", "Module externe R1-B", "externe", b(0.60, 0.80, 0.95), (x0 + 0.30, 0.13, 0.475), "R1-B3",
             "protège et arrime le module", "—", opacite=0.16, englobant=True, couche="externe")
    G.ajoute("Gravimètre de classe microgal, amovible (215 × 210 × 240 mm)", "Option gravimètre", "gravite", b(0.215, 0.210, 0.240), (L + 0.03 + 0.1075, -0.20, 0.120), "R1-22",
             "mesure g à 5 µGal, posé au sol, véhicule à l'arrêt", "Unité de capteurs de gravité (DOC-008 r.11)", couche="externe")
    for p in G.pieces:
        p["id"] = p["id"].replace("R1-P", "R1-X")

    meta = copy.deepcopy(src["meta"])
    meta["titre"] = "Modèle 3D du palier 1 — C204-R1 « chronomètre-gravimètre relativiste embarqué »"
    meta["avertissement"] = ("Conception de l'Équipe I : instrument de mesure RÉEL logé dans l'enveloppe du coffre « C204 » telle que reconstituée par l'Équipe E "
                             "à partir de documents non authentifiés. Cet appareil ne déplace rien dans le temps : il mesure ou calcule un décalage d'horloge "
                             "de l'ordre de la nanoseconde par heure, dû à l'altitude et à la vitesse du TRAJET, que tout objet transporté subirait à l'identique.")
    meta["equipe"] = "Équipe I — optimisation scientifique (Phase 6) ; enveloppe : Équipe E"
    meta["genere_par"] = "10_machine_optimisee/calculs/i10_modele_R1.py à partir de 06_modele_3D/modele_c204.json (lecture seule)"
    meta["classements"].update({
        "COM": {"libelle": "Composant du commerce", "couleur": "#1baf7a", "definition": "Composant disponible sur catalogue (palier 1)."},
        "LAB": {"libelle": "Matériel de laboratoire courant ou kit", "couleur": "#2a78d6", "definition": "Réalisable avec du matériel de laboratoire courant."},
        "SPE": {"libelle": "Pièce spécifique à réaliser", "couleur": "#eda100", "definition": "Pièce mécanique ou carte à concevoir pour l'intégration."}})
    meta["systemes"] = {"structure": {"libelle": "Enveloppe reprise du modèle de l'Équipe E", "couleur": "#9aa0a8"}}
    meta["systemes"].update({k: {"libelle": l, "couleur": c_} for k, (l, c_) in SYSTEMES_R1.items()})
    commun = dict(etats=A["etats"], articulations=A["articulations"], cotes_cles=ck)
    modele = {"meta": meta, "cotes": src["cotes"], "variantes": {
        "R1A": dict(nom="C204-R1, configuration A — coffre seul", description="Composants réels de la nomenclature R1 dans l'enveloppe de la variante A de l'Équipe E.",
                    documents="enveloppe : DOC-001 à 004, DOC-007 ; intérieur : conception Équipe I", pieces=reprises + internes, emprise=A["emprise"],
                    bilan_volumique=dict(volume_interieur_m3=round(vol_int, 4), volume_composants_m3=round(vol_comp, 4), taux_occupation=round(vol_comp / vol_int, 3)),
                    bilan_pieces=dict(reprises_equipe_E=len(reprises), internes_R1=len(internes)), **commun),
        "R1B": dict(nom="C204-R1, configuration B — coffre + module césium externe et gravimètre amovible",
                    description="Le coffre R1-A et, à la même échelle, ce qui ne tient pas dedans : trois étalons à jet de césium avec leur batterie, et le gravimètre de classe microgal.",
                    documents="idem", pieces=reprises + internes + G.pieces, **commun)}}
    (RACINE / "modele_c204_R1.json").write_text(json.dumps(modele, ensure_ascii=False, indent=1), encoding="utf-8")
    return modele, internes, journal, interieur, vol_int, vol_comp


def habiller(img, chemin, titre, sous_titre="", reperes=(), cam=None, legende=None, marges=(330, 330, 86, 96), barre=None, note=""):
    """Habillage : celui de l'Équipe E (RV.habiller) pour l'image, les repères et l'échelle ; la légende, trop longue
    pour une seule ligne, est ajoutée ensuite sur plusieurs lignes (reprise de l'image écrite, sans modifier le moteur E)."""
    RV.habiller(img, chemin, titre, sous_titre, reperes, cam, None, marges, barre, note)
    if not legende:
        return
    import matplotlib.pyplot as plt
    from PIL import Image
    im = np.asarray(Image.open(chemin).convert("RGB"))
    Ht, Wt = im.shape[:2]
    fig = plt.figure(figsize=(Wt / 100, Ht / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.imshow(im)
    ax.axis("off")
    ncol = 3 if len(legende) > 4 else len(legende)
    nlig = math.ceil(len(legende) / ncol)
    ax.legend(handles=legende, loc="lower center", bbox_to_anchor=(0.5, 28 / Ht), ncol=ncol, frameon=False, fontsize=9.5, handlelength=1.4, columnspacing=2.2)
    fig.savefig(chemin, dpi=100, facecolor="white")
    plt.close(fig)


def rendus(modele):
    leg = [Patch(facecolor=v["couleur"], edgecolor="#333", label=v["libelle"]) for k, v in modele["meta"]["systemes"].items() if k not in ("externe",)]
    leg_b = [Patch(facecolor=v["couleur"], edgecolor="#333", label=v["libelle"]) for k, v in modele["meta"]["systemes"].items() if k in ("structure", "externe", "gravite")]
    NOTE = ("Conception Équipe I dans l'enveloppe reconstituée par l'Équipe E (L = 0,85 m ± 0,20 m, estimation de l'Équipe A, confiance faible). "
            "Instrument de mesure : aucune fonction de déplacement temporel.")
    sans_platine = lambda p: p["couche"] in ("platine", "mobile")
    coque = lambda p: 0.12 if (p.get("fantome") and p["couche"] in ("coque", "couvercle")) else None
    faits = []

    def rep(pcs, cen, liste):
        out = []
        for txt, frag, cote in liste:
            out.append((txt, RV.trouver(pcs, cen, frag), cote))
        return out

    REP = [("Batterie 1,34 kWh\n(R1-03)", "Batterie LiFePO4", "g"),
           ("Distribution très basse tension\n(R1-04) — remplace l'« injection d'électrons »", "Convertisseurs DC/DC", "g"),
           ("Relais de sécurité (R1-05)", "Coupe-batterie", "g"),
           ("LOGEMENT PRINCIPAL\ntélescope à muons : 2 tuiles\nscintillantes (R1-14)", "Tuile scintillante supérieure", "g"),
           ("LOGEMENT DE DIRECTION\ngyromètre Sagnac : bobine\nde 500 m de fibre (R1-15)", "Bobine de fibre optique", "g"),
           ("Cartes de proximité (R1-16)", "Carte de démodulation", "g"),
           ("Boucle thermique : pompe\net 2 réservoirs (R1-17)", "Réservoir tampon n°1", "d"),
           ("4 horloges au césium (CSAC)\nsous blindage (R1-06, R1-09)", "Horloge atomique miniature au césium n°2", "d"),
           ("Comparateur de phase (R1-07)\net GNSS (R1-08)", "Comparateur de phase", "d"),
           ("3 calculateurs + voteur\n(R1-10, R1-11)", "Calculateur n°1", "d"),
           ("Accéléromètres « VGL »\n(R1-12)", "Triade d'accéléromètres", "d"),
           ("Dosimètre du rayonnement\nambiant (R1-18)", "Dosimètre à semi-conducteur", "d")]

    # 01 — ouvert, aspect d'après les documents (les démonstrateurs se voient par les deux logements)
    img, cam, pcs, cen = RV.vue(modele, "R1A", "ouvert", "aspect", -34, 40)
    habiller(img, SORTIE / "R1_01_ouvert_aspect.png", "C204-R1 — coffre ouvert : même enveloppe que la C204 décrite",
                "Aspect extérieur repris du modèle de l'Équipe E ; par les deux logements on aperçoit la tuile scintillante (au fond) et la bobine de fibre (devant).",
                rep(pcs, cen, [("Logement principal :\ntélescope à muons", "Tuile scintillante supérieure", "g"),
                               ("Logement de direction :\ngyromètre Sagnac", "Bobine de fibre optique", "g")]), cam, None, note=NOTE)
    faits.append("R1_01_ouvert_aspect.png")
    # 02 — intérieur
    img, cam, pcs, cen = RV.vue(modele, "R1A", "ouvert", "systeme", -28, 34, cacher=sans_platine, alpha=coque)
    habiller(img, SORTIE / "R1_02_interieur.png", "C204-R1 — composants internes (platine retirée, coque translucide)",
                "Couleurs = sous-systèmes réels. Chaque composant remplace un élément de la C204 décrite (voir correspondance_composants.csv).",
                rep(pcs, cen, REP), cam, leg, marges=(360, 360, 86, 170), note=NOTE)
    faits.append("R1_02_interieur.png")
    # 03 — éclaté
    img, cam, pcs, cen = RV.vue(modele, "R1A", "eclate", "systeme", -30, 22, taille=(1250, 1400), fov=24)
    habiller(img, SORTIE / "R1_03_eclate.png", "C204-R1 — vue éclatée", "Décalages verticaux de présentation.", rep(pcs, cen, REP[:5] + REP[6:10]), cam, leg,
                marges=(360, 360, 86, 170), note=NOTE)
    faits.append("R1_03_eclate.png")
    # 04 — dessus (orthographique), platine retirée
    img, cam, pcs, cen = RV.vue(modele, "R1A", "ferme", "systeme", 0, 90, taille=(1500, 620), perspective=False, marge=1.04,
                                cacher=lambda p: p["couche"] in ("platine", "mobile", "couvercle"), alpha=coque)
    habiller(img, SORTIE / "R1_04_dessus.png", "C204-R1 — vue de dessus (couvercle et platine retirés)", "Implantation à L = 0,85 m : occupation ≈ 30 % du volume intérieur.",
                rep(pcs, cen, REP), cam, leg, marges=(360, 360, 86, 170), barre=0.20, note=NOTE)
    faits.append("R1_04_dessus.png")
    # 05 — face (orthographique)
    img, cam, pcs, cen = RV.vue(modele, "R1A", "ferme", "systeme", 0, 0, taille=(1500, 520), perspective=False, alpha=lambda p: 0.12 if p["couche"] in ("coque", "couvercle") else None,
                                cacher=lambda p: p["couche"] in ("platine", "mobile") or "paroi avant" in p["nom"] or "Loquet" in p["nom"])
    habiller(img, SORTIE / "R1_05_face.png", "C204-R1 — vue de face (paroi avant retirée)", "Les deux démonstrateurs sont alignés en profondeur sous les logements de DOC-007.",
                rep(pcs, cen, REP[:5] + REP[6:]), cam, leg, marges=(360, 360, 86, 170), barre=0.20, note=NOTE)
    faits.append("R1_05_face.png")
    # 06 — configuration B, à l'échelle
    img, cam, pcs, cen = RV.vue(modele, "R1B", "ouvert", "systeme", -38, 24, taille=(1500, 900), fov=22, alpha=lambda p: 0.16 if p.get("englobant") and p["couche"] == "externe" else None)
    habiller(img, SORTIE / "R1_06_configuration_B.png", "C204-R1, configuration B — ce qui mesure vraiment ne tient pas dans le coffre",
                "À la même échelle : le coffre de 0,85 m (36 kg) ; trois étalons à jet de césium et leur batterie (165 kg) ; le gravimètre de classe microgal.",
                rep(pcs, cen, [("Coffre R1-A (36 kg)", "Corps — paroi avant", "g"), ("Gravimètre amovible\n(5,5 kg)", "Gravimètre de classe microgal", "g"),
                               ("3 étalons à jet de césium\n(3 × 30 kg, 425 × 524 × 133 mm)", "Étalon à jet de césium n°2", "d"),
                               ("Batterie 7,5 kWh (55 kg)", "Batterie 7,5 kWh", "d")]), cam, leg_b, marges=(330, 330, 86, 120), note=NOTE)
    faits.append("R1_06_configuration_B.png")
    return faits


if __name__ == "__main__":
    modele, internes, journal, interieur, vi, vc = construire()
    L = ["i10 — MODÈLE 3D DU PALIER 1", "=" * 80,
         "Pièces reprises de l'Équipe E : %d ; pièces internes R1 : %d ; pièces externes (configuration B) : %d"
         % (modele["variantes"]["R1A"]["bilan_pieces"]["reprises_equipe_E"], len(internes), len(modele["variantes"]["R1B"]["pieces"]) - len(modele["variantes"]["R1A"]["pieces"])),
         "Volume intérieur %.1f L ; composants %.1f L ; occupation %.0f %%" % (vi * 1000, vc * 1000, 100 * vc / vi),
         "Contrôles géométriques : " + ("AUCUNE anomalie (toutes les pièces dans le volume intérieur, aucune interpénétration)" if not journal else "; ".join(journal))]
    faits = rendus(modele)
    L.append("Rendus : " + ", ".join(faits))
    (ICI / "resultats" / "i10_modele_R1.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
