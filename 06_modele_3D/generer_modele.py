#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — génération du modèle paramétrique.

    parametres.json  ──►  modele_c204.json

Le modèle est une LISTE DE PIÈCES ; chaque pièce = une primitive (boîte, cylindre, sphère, tore,
prisme extrudé) + une transformation + un nom + un repère d'origine + un document source +
un classement (DOC / DÉD / HYP) + une fonction REVENDIQUÉE + un décalage de vue éclatée.

Rappel : il s'agit de la reconstruction d'un objet tel qu'il est DÉCRIT par des documents non
authentifiés. Rien n'atteste que l'objet ait existé ni fonctionné.

Conventions (reprises dans modele_c204.json → meta.conventions) :
  - repère : origine au coin avant-gauche-bas du corps ; X longueur, Y profondeur (charnière à
    l'arrière), Z hauteur ; unité : mètre ;
  - boîte    : dimensions [dx, dy, dz], centrée ;
  - cylindre : rayon, hauteur ; axe local Z ; centré ;
  - sphère   : rayon, échelle optionnelle [sx, sy, sz] (ellipsoïde) ;
  - tore     : rayon_majeur, rayon_mineur ; axe local Z ;
  - prisme   : profil [[u, v], ...] dans le plan local XY (+ trous éventuels), hauteur selon Z local, centré ;
  - rotation_deg = [rx, ry, rz] : R = Rz · Ry · Rx (rotations successives autour des axes FIXES X, Y, Z) ;
    le quaternion [x, y, z, w] équivalent est fourni pour éviter toute ambiguïté ;
  - liaison « couvercle » : la pièce tourne autour de la charnière (articulations.couvercle) ;
  - les positions sont données COUVERCLE FERMÉ, sans éclatement.

Usage : python generer_modele.py [--parametres parametres.json] [--sortie modele_c204.json]
"""
import argparse
import datetime
import json
import math
from pathlib import Path

import numpy as np
from shapely.geometry import Polygon, box as rectangle

ICI = Path(__file__).resolve().parent

CLASSEMENTS = {
    "DOC": {"libelle": "Documenté", "couleur": "#0072B2",
            "definition": "Forme et position lisibles directement sur un document source archivé. Pour une pièce relevée sur la seule vue de dessus DOC-007, "
                          "seule l'emprise en plan est documentée : épaisseur et relief sont supposés."},
    "DÉD": {"libelle": "Déduit", "couleur": "#E69F00",
            "definition": "Existence documentée (image ou texte) ; forme ou position inférée en croisant plusieurs documents."},
    "HYP": {"libelle": "Hypothétique", "couleur": "#CC79A7",
            "definition": "Forme, taille ou position supposées par l'Équipe E ; volume générique non étayé par les sources."},
}
SYSTEMES = {
    "structure": {"libelle": "Structure et habillage", "couleur": "#6b7280"},
    "signalisation": {"libelle": "Signalisation et étiquetage", "couleur": "#d4a017"},
    "commande": {"libelle": "Commande et affichage", "couleur": "#2f9e8f"},
    "singularites": {"libelle": "Logements des « singularités »", "couleur": "#7c3aed"},
    "champ_magnetique": {"libelle": "Champ magnétique", "couleur": "#c2410c"},
    "electrons": {"libelle": "Injection d'électrons", "couleur": "#2563eb"},
    "refroidissement": {"libelle": "Refroidissement", "couleur": "#0891b2"},
    "capteurs": {"libelle": "Capteurs de gravité (VGL)", "couleur": "#65a30d"},
    "horloges": {"libelle": "Horloges", "couleur": "#be185d"},
    "calcul": {"libelle": "Calculateurs", "couleur": "#4338ca"},
    "energie": {"libelle": "Énergie électrique", "couleur": "#b91c1c"},
    "inconnu": {"libelle": "Fonction inconnue (DOC-005 sans légende)", "couleur": "#78716c"},
}
C = {  # couleurs d'aspect (photos DOC-001/002/003 pour le jaune, l'orange, le sombre ; neutres ailleurs)
    "coque": "#2e3430", "coque_int": "#3b423d", "platine": "#8b908a", "platine_claire": "#c9ccc6", "blanc": "#ecebe4",
    "noir": "#151515", "jaune": "#e0bd35", "orange": "#dc7a22", "rouge": "#c92a2a", "gris": "#9aa0a6",
    "metal": "#b7bcc3", "acier": "#7d858e", "cuivre": "#b87333", "fluide": "#4f9ac9", "elec": "#3b6fd4",
    "vert": "#6f9a3a", "violet": "#7c5cc4", "magenta": "#b0508a", "brun": "#8a6d4b", "papier": "#d6d3c4",
}


# ------------------------------------------------------------------------------------------------
# Paramètres
# ------------------------------------------------------------------------------------------------
def _arrondi(v, n=4):
    if isinstance(v, list):
        return [round(float(x), n) for x in v]
    return round(float(v), n)


def charger_parametres(chemin):
    """Lit parametres.json, résout les cotes proportionnelles et renvoie (brut, cotes, infos)."""
    brut = json.loads(Path(chemin).read_text(encoding="utf-8"))
    infos = {}
    for section, contenu in brut.items():
        if section.startswith("_") or not isinstance(contenu, dict):
            continue
        for nom, p in contenu.items():
            if isinstance(p, dict) and "etiquette" in p:
                if nom in infos:
                    raise ValueError(f"cote en double : {nom}")
                p["_section"] = section
                infos[nom] = p
    cotes = {}

    def resoudre(nom, pile=()):
        if nom in cotes:
            return cotes[nom]
        if nom in pile:
            raise ValueError("référence circulaire : " + " → ".join(pile + (nom,)))
        p = infos[nom]
        if "rapport" in p:
            ref = resoudre(p["reference"], pile + (nom,))
            r = p["rapport"]
            v = [x * ref for x in r] if isinstance(r, list) else r * ref
            p["valeur"] = _arrondi(v)
            p["incertitude"] = _arrondi(p.get("incertitude_rapport", 0.0) * abs(ref))
        else:
            v = p["valeur"]
        cotes[nom] = v
        return v

    for nom in infos:
        resoudre(nom)
    for p in infos.values():
        p.pop("_section", None)
    return brut, cotes, infos


def ecrire_parametres(brut, chemin):
    """Réécrit parametres.json (valeurs recalculées) en gardant une cote par ligne."""
    def sur_une_ligne(d):
        return isinstance(d, dict) and ("etiquette" in d or "fx" in d)

    def dump(o, niv):
        pad = " " * niv
        if isinstance(o, dict) and not sur_une_ligne(o):
            if not o:
                return "{}"
            corps = ",\n".join(f"{pad} {json.dumps(k, ensure_ascii=False)}: {dump(v, niv + 1)}" for k, v in o.items())
            return "{\n" + corps + "\n" + pad + "}"
        if isinstance(o, list) and o and isinstance(o[0], dict):
            corps = ",\n".join(f"{pad} {dump(v, niv + 1)}" for v in o)
            return "[\n" + corps + "\n" + pad + "]"
        return json.dumps(o, ensure_ascii=False)

    Path(chemin).write_text(dump(brut, 0) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------------
# Géométrie élémentaire
# ------------------------------------------------------------------------------------------------
def matrice_rotation(rot_deg):
    rx, ry, rz = (math.radians(a) for a in rot_deg)
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def quaternion(R):
    """Quaternion [x, y, z, w] d'une matrice de rotation."""
    t = np.trace(R)
    if t > 0:
        s = math.sqrt(t + 1.0) * 2
        w, x, y, z = 0.25 * s, (R[2, 1] - R[1, 2]) / s, (R[0, 2] - R[2, 0]) / s, (R[1, 0] - R[0, 1]) / s
    elif R[0, 0] > R[1, 1] and R[0, 0] > R[2, 2]:
        s = math.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
        w, x, y, z = (R[2, 1] - R[1, 2]) / s, 0.25 * s, (R[0, 1] + R[1, 0]) / s, (R[0, 2] + R[2, 0]) / s
    elif R[1, 1] > R[2, 2]:
        s = math.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
        w, x, y, z = (R[0, 2] - R[2, 0]) / s, (R[0, 1] + R[1, 0]) / s, 0.25 * s, (R[1, 2] + R[2, 1]) / s
    else:
        s = math.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
        w, x, y, z = (R[1, 0] - R[0, 1]) / s, (R[0, 2] + R[2, 0]) / s, (R[1, 2] + R[2, 1]) / s, 0.25 * s
    return [round(float(v), 6) for v in (x, y, z, w)]


AXE = {"X": (0.0, 90.0, 0.0), "Y": (-90.0, 0.0, 0.0), "Z": (0.0, 0.0, 0.0)}   # oriente l'axe local Z


def boite(dx, dy, dz):
    return {"type": "boite", "dimensions": [dx, dy, dz]}


def cylindre(r, h):
    return {"type": "cylindre", "rayon": r, "hauteur": h}


def sphere(r, echelle=None):
    p = {"type": "sphere", "rayon": r}
    if echelle:
        p["echelle"] = list(echelle)
    return p


def tore(R, r):
    return {"type": "tore", "rayon_majeur": R, "rayon_mineur": r}


def prisme(profil, h, trous=None):
    p = {"type": "prisme", "profil": [[float(u), float(v)] for u, v in profil], "hauteur": h}
    if trous:
        p["trous"] = [[[float(u), float(v)] for u, v in t] for t in trous]
    return p


def cercle(cx, cy, r, n=40):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def volume_primitive(p):
    t = p["type"]
    if t == "boite":
        a, b, c = p["dimensions"]
        return a * b * c
    if t == "cylindre":
        return math.pi * p["rayon"] ** 2 * p["hauteur"]
    if t == "sphere":
        s = p.get("echelle", [1, 1, 1])
        return 4 / 3 * math.pi * p["rayon"] ** 3 * s[0] * s[1] * s[2]
    if t == "tore":
        return 2 * math.pi ** 2 * p["rayon_majeur"] * p["rayon_mineur"] ** 2
    if t == "prisme":
        aire = Polygon(p["profil"], p.get("trous", [])).area
        return aire * p["hauteur"]
    raise ValueError(t)


class Modele:
    def __init__(self, prefixe):
        self.prefixe = prefixe
        self.pieces = []

    def ajouter(self, nom, primitive, position, rotation=(0, 0, 0), *, ensemble, classement, source,
                repere="—", existence=None, fonction="", systeme="structure", liaison="corps",
                eclate=(0, 0, 0), couleur="#888888", opacite=1.0, notes="", masque=(), fantome=False):
        assert classement in CLASSEMENTS, classement
        assert systeme in SYSTEMES, systeme
        R = matrice_rotation(rotation)
        piece = {
            "id": f"{self.prefixe}-{len(self.pieces) + 1:03d}",
            "nom": nom,
            "ensemble": ensemble,
            "repere": repere,
            "source": source,
            "classement": classement,
            "existence": existence or {"DOC": "DOC image", "DÉD": "DOC image", "HYP": "HYP"}[classement],
            "fonction_revendiquee": fonction or "—",
            "systeme": systeme,
            "primitive": {k: (_arrondi(v, 5) if isinstance(v, (int, float)) and not isinstance(v, bool) else
                              ([_arrondi(x, 5) for x in v] if isinstance(v, list) and v and isinstance(v[0], (int, float)) else v))
                          for k, v in primitive.items()},
            "position": _arrondi(list(position), 5),
            "rotation_deg": [float(a) for a in rotation],
            "quaternion": quaternion(R),
            "liaison": liaison,
            "eclate": _arrondi(list(eclate), 4),
            "couleur": couleur,
            "opacite": opacite,
            "volume_m3": float(f"{volume_primitive(primitive):.4g}"),
        }
        if fantome:
            piece["fantome"] = True      # enveloppe : rendue translucide dans les vues intérieures
        if masque:
            piece["masque"] = list(masque)
        if notes:
            piece["notes"] = notes
        self.pieces.append(piece)
        return piece

    def plaque(self, nom, x0, x1, y0, y1, z0, z1, **kw):
        """Boîte alignée sur les axes, donnée par ses bornes."""
        return self.ajouter(nom, boite(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)),
                            ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2), **kw)

    def prisme_plan(self, nom, points, z0, z1, trous=None, **kw):
        """Prisme d'axe Z à partir d'un contour donné en coordonnées absolues (x, y)."""
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        prof = [(x - cx, y - cy) for x, y in points]
        tr = [[(x - cx, y - cy) for x, y in t] for t in trous] if trous else None
        return self.ajouter(nom, prisme(prof, abs(z1 - z0), tr), (cx, cy, (z0 + z1) / 2), **kw)


def raies_obliques(x0, x1, ya, yb, pente, periode, epaisseur, phase, miroir_P=None):
    """Polygones des raies noires d'une bande de danger, découpés au rectangle [x0,x1]×[ya,yb].
    miroir_P : si fourni, symétrie y → P − y (intérieur du couvercle, position fermée)."""
    rect = rectangle(x0, ya, x1, yb)
    w = x1 - x0
    polys = []
    for k in range(-3, 8):
        y0 = phase + k * periode
        para = Polygon([(x0, y0), (x1, y0 + pente * w), (x1, y0 + pente * w + epaisseur), (x0, y0 + epaisseur)])
        if miroir_P is not None:
            para = Polygon([(x, miroir_P - y) for x, y in para.exterior.coords[:-1]])
        inter = para.intersection(rect)
        if inter.is_empty or inter.area < 1e-7:
            continue
        geoms = [inter] if inter.geom_type == "Polygon" else [g for g in inter.geoms if g.geom_type == "Polygon"]
        for g in geoms:
            polys.append([(float(x), float(y)) for x, y in g.exterior.coords[:-1]])
    polys.sort(key=lambda pts: min(p[1] for p in pts))
    return polys


# ------------------------------------------------------------------------------------------------
# VARIANTE A — coffre plat à couvercle articulé (DOC-001/002/003/004/007 + composants de DOC-008)
# ------------------------------------------------------------------------------------------------
def construire_variante_A(c, brut, disposition, prefixe="A"):
    M = Modele(prefixe)
    pres = brut["presentation"]
    L, P, Hc, Hv, e = c["L"], c["P"], c["H_corps"], c["H_couvercle"], c["e_rebord"]
    ef, epl, em = c["e_fond"], c["e_platine"], c["e_marquage"]
    zp = Hc - c["retrait_platine"]              # dessus de la platine
    zpi = zp - epl                              # dessous de la platine
    Hi = zpi - ef                               # hauteur intérieure utile
    ecl_int = (0, 0, pres["eclate_internes_z_sur_L"] * L)
    ecl_pl = (0, 0, pres["eclate_platine_z_sur_L"] * L)
    ecl_mq = (0, 0, pres["eclate_marquages_z_sur_L"] * L)
    ecl_cv = tuple(v * L for v in pres["eclate_couvercle_sur_L"])
    ecl_mc = tuple(v * L for v in pres["eclate_marquages_couvercle_sur_L"])
    dy_ens, dy_bob, dy_cal = (pres[k] * L for k in ("eclate_ensembles_y_sur_L", "eclate_bobines_y_sur_L", "eclate_calottes_y_sur_L"))
    S47 = "DOC-004 ; DOC-007"
    PH = "DOC-001 ; DOC-002 ; DOC-003"

    # ---------------- corps ------------------------------------------------------------------
    kw = dict(ensemble="Coffre — corps", classement="DOC", source=S47 + " ; " + PH, systeme="structure",
              couleur=C["coque"], fantome=True,
              fonction="Enveloppe de l'unité (« C204 gravity distortion time displacement unit », DOC-006).",
              notes="Proportions L/P de DOC-007, hauteur de DOC-004. Coins arrondis de DOC-007 non modélisés ; épaisseur de paroi inconnue.")
    M.plaque("Corps — fond", 0, L, 0, P, 0, ef, **{**kw, "classement": "HYP", "notes": "Aucun document ne montre le fond."})
    M.plaque("Corps — paroi avant", 0, L, 0, e, ef, Hc, **kw)
    M.plaque("Corps — paroi arrière", 0, L, P - e, P, ef, Hc, **kw)
    M.plaque("Corps — paroi d'extrémité gauche", 0, e, e, P - e, ef, Hc, **kw)
    M.plaque("Corps — paroi d'extrémité droite", L - e, L, e, P - e, ef, Hc, **kw)

    # accastillage
    kwa = dict(ensemble="Coffre — accastillage", systeme="structure", couleur=C["metal"])
    for i, nomx in enumerate(("x_loquet1", "x_loquet2"), 1):
        M.plaque(f"Loquet de fermeture avant n°{i}", c[nomx] - c["loquet_largeur"] / 2, c[nomx] + c["loquet_largeur"] / 2,
                 -0.008, 0, Hc - c["loquet_hauteur"] * 0.75, Hc + c["loquet_hauteur"] * 0.25, classement="DÉD",
                 source="DOC-004 (face avant) ; DOC-002 / DOC-003 (ferrures)", fonction="Verrouillage du couvercle (interprétation ; non légendé).",
                 notes="Pièce claire visible sur la face avant ; nombre et position incertains (2 ou 3).", **kwa)
    pl, ph = c["poignee_largeur"], c["poignee_hauteur"]
    M.plaque("Poignée encastrée d'extrémité gauche", -0.004, 0, P / 2 - pl / 2, P / 2 + pl / 2, Hc * 0.55 - ph / 2, Hc * 0.55 + ph / 2,
             classement="DÉD", source="DOC-004 (face d'extrémité gauche)", fonction="Manutention (interprétation ; non légendé).",
             notes="Renfoncement sombre sur la face gauche.", **{**kwa, "couleur": C["noir"]})
    M.plaque("Poignée encastrée d'extrémité droite", L, L + 0.004, P / 2 - pl / 2, P / 2 + pl / 2, Hc * 0.55 - ph / 2, Hc * 0.55 + ph / 2,
             classement="HYP", source="Symétrie supposée (face droite jamais visible)", fonction="Manutention (supposée).",
             notes="Ajoutée par symétrie : aucune vue de la face droite.", **{**kwa, "couleur": C["noir"]})
    for i, (a, b) in enumerate((("x_charniere1_debut", "x_charniere1_fin"), ("x_charniere2_debut", "x_charniere2_fin")), 1):
        M.ajouter(f"Charnière n°{i}", cylindre(c["r_charniere"], c[b] - c[a]), ((c[a] + c[b]) / 2, P + c["r_charniere"] * 0.5, Hc),
                  AXE["X"], classement="DOC", source="DOC-007 (pavés noirs entre couvercle et corps)",
                  fonction="Articulation du couvercle sur le grand côté arrière.",
                  notes="DOC-004 montre plutôt une tringle claire continue sur toute la longueur (écart E6).", **kwa)

    # ---------------- couvercle (position fermée ; liaison « couvercle ») -----------------------
    zc0, zc1 = Hc, Hc + Hv
    zin = zc1 - c["e_plaque_couvercle"]          # face intérieure du couvercle
    kwc = dict(ensemble="Coffre — couvercle", classement="DOC", source=S47 + " ; " + PH, systeme="structure",
               couleur=C["coque"], liaison="couvercle", eclate=ecl_cv, fantome=True,
               fonction="Couvercle articulé ; porte à l'intérieur les bandes de danger et la plaque d'instructions.",
               notes="Profondeur du couvercle estimée sur DOC-004 (incertitude forte). Aspect extérieur fermé : aucun document.")
    M.plaque("Couvercle — dessus", 0, L, 0, P, zin, zc1, **kwc)
    M.plaque("Couvercle — rebord avant", 0, L, 0, e, zc0, zin, **kwc)
    M.plaque("Couvercle — rebord arrière", 0, L, P - e, P, zc0, zin, **kwc)
    M.plaque("Couvercle — rebord gauche", 0, e, e, P - e, zc0, zin, **kwc)
    M.plaque("Couvercle — rebord droit", L - e, L, e, P - e, zc0, zin, **kwc)

    kwm = dict(liaison="couvercle", eclate=ecl_mc, systeme="signalisation")
    args_b = (c["bande_pente"], c["bande_periode"], c["bande_epaisseur_noire"], c["bande_phase"])
    for i, (a, b) in enumerate((("x_bande1_debut", "x_bande1_fin"), ("x_bande2_debut", "x_bande2_fin")), 1):
        M.plaque(f"Couvercle — bande de danger n°{i} (fond)", c[a], c[b], e, P - e, zin - em, zin, ensemble=f"Couvercle — bande de danger n°{i}",
                 classement="DOC", source="DOC-007 (position) ; " + PH + " (jaune et noir)", couleur=C["jaune"],
                 fonction="Marquage de danger (non légendé).",
                 notes="Photos : bande 2 plus à gauche (≈ 0,45–0,52 L) et 2–3 raies seulement (écarts E4, E5).", **kwm)
        for k, pts in enumerate(raies_obliques(c[a], c[b], e, P - e, *args_b, miroir_P=P), 1):
            M.prisme_plan(f"Couvercle — bande n°{i}, raie noire {k}", pts, zin - 2 * em, zin - em, ensemble=f"Couvercle — bande de danger n°{i}",
                          classement="DOC", source="DOC-007", couleur=C["noir"], fonction="Marquage de danger (non légendé).", **kwm)
    yv = lambda v: P - v      # distance à la charnière → ordonnée couvercle fermé
    M.plaque("Plaque d'instructions de commande (7)", c["x_plaque7_debut"], c["x_plaque7_fin"], yv(c["v_plaque7_fin"]), yv(c["v_plaque7_debut"]),
             zin - 2 * em, zin, ensemble="Couvercle — plaques et étiquettes", repere="DOC-007 n°7", classement="DOC",
             source="DOC-007 ; DOC-004 ; " + PH, couleur=C["papier"],
             fonction="« UNIT CONTROL INSTRUCTIONS » : instructions de commande de l'unité (texte illisible sur toutes les copies).", **kwm)
    M.plaque("Étiquette blanche centrale à liseré rouge", c["x_etiq_centrale_debut"], c["x_etiq_centrale_fin"], yv(c["v_etiq_blanche_fin"]),
             yv(c["v_etiq_blanche_debut"]), zin - 2 * em, zin, ensemble="Couvercle — plaques et étiquettes", repere="—", classement="DOC",
             source=PH + " ; DOC-004", couleur=C["blanc"], fonction="Inconnue (étiquette d'avertissement probable ; texte illisible).",
             notes="Absente de DOC-007. Position transposée entre les bandes de DOC-007.", **kwm)
    M.plaque("Étiquette orange centrale", c["x_etiq_centrale_debut"] - 0.004, c["x_etiq_centrale_fin"] + 0.008, yv(c["v_etiq_orange_fin"]),
             yv(c["v_etiq_orange_debut"]), zin - 2 * em, zin, ensemble="Couvercle — plaques et étiquettes", repere="—", classement="DOC",
             source=PH, couleur=C["orange"], fonction="Inconnue (texte illisible).", notes="Absente de DOC-007 et indistincte sur DOC-004.", **kwm)
    M.plaque("Étiquette jaune (haut gauche)", c["x_etiq_jaune_debut"], c["x_etiq_jaune_fin"], yv(c["v_etiq_jaune_fin"]), yv(c["v_etiq_jaune_debut"]),
             zin - 2 * em, zin, ensemble="Couvercle — plaques et étiquettes", repere="—", classement="DOC", source=PH + " ; DOC-004",
             couleur=C["jaune"], fonction="Inconnue (texte illisible).", notes="Absente de DOC-007.", **kwm)
    M.plaque("Élément gris sous l'étiquette jaune", c["x_boitier_gris_debut"], c["x_boitier_gris_fin"], yv(c["v_boitier_gris_fin"]),
             yv(c["v_boitier_gris_debut"]), zin - 6 * em, zin, ensemble="Couvercle — plaques et étiquettes", repere="—", classement="DÉD",
             source="DOC-002 ; DOC-003 ; DOC-004", couleur=C["gris"], fonction="Inconnue.",
             notes="Étiquette ou petit boîtier : indéterminé (résolution insuffisante). Absent de DOC-007.", **kwm)

    # ---------------- platine supérieure (DOC-007) ------------------------------------------------
    ya, yb = e, P - e
    xs = {k: c[k] for k in ("x_division_gauche", "x_bande1_debut", "x_bande1_fin", "x_cadre_debut", "x_cadre_fin", "x_bande2_debut",
                             "x_bande2_fin", "x_zone4_fin", "x_panneau5_fin", "x_panneau8_fin")}
    kwp = dict(classement="DOC", source="DOC-007", systeme="structure", eclate=ecl_pl, couleur=C["platine"])

    def dalle(nom, x0, x1, y0=ya, y1=yb, **k):
        return M.plaque(nom, x0, x1, y0, y1, zpi, zp, **{**kwp, **k})

    dalle("Platine — zone tramée gauche (a)", e, xs["x_division_gauche"], ensemble="Platine — zones non légendées",
          fonction="Non légendée.", notes="DOC-004 la montre blanche (zone tramée sur DOC-007).")
    dalle("Platine — zone tramée gauche (b)", xs["x_division_gauche"], xs["x_bande1_debut"], ensemble="Platine — zones non légendées",
          fonction="Non légendée.", notes="Séparée de (a) par un trait : trappe d'accès possible (interprétation).")
    for i, (a, b) in enumerate((("x_bande1_debut", "x_bande1_fin"), ("x_bande2_debut", "x_bande2_fin")), 1):
        dalle(f"Platine — bande de danger n°{i} (fond)", c[a], c[b], ensemble=f"Platine — bande de danger n°{i}", systeme="signalisation",
              couleur=C["jaune"], source="DOC-007 (position) ; " + PH + " (jaune et noir)", fonction="Marquage de danger (non légendé).")
        for k, pts in enumerate(raies_obliques(c[a], c[b], ya, yb, *args_b), 1):
            M.prisme_plan(f"Platine — bande n°{i}, raie noire {k}", pts, zp, zp + em, ensemble=f"Platine — bande de danger n°{i}",
                          classement="DOC", source="DOC-007", systeme="signalisation", eclate=ecl_mq, couleur=C["noir"],
                          fonction="Marquage de danger (non légendé).")
    dalle("Platine — zone tramée centre-gauche", xs["x_bande1_fin"], xs["x_cadre_debut"], ensemble="Platine — zones non légendées",
          fonction="Non légendée.")
    dalle("Platine — zone tramée centre-droite", xs["x_cadre_fin"], xs["x_bande2_debut"], ensemble="Platine — zones non légendées",
          fonction="Non légendée.")
    # étiquettes à repères d'angle visibles sur DOC-004 de part et d'autre des logements
    for nom, x0, x1 in (("gauche", xs["x_bande1_fin"], xs["x_cadre_debut"]), ("droite", xs["x_cadre_fin"], xs["x_bande2_debut"])):
        m = 0.12 * (x1 - x0)
        M.plaque(f"Étiquette claire à repères d'angle ({nom} des logements)", x0 + m, x1 - m, 0.30 * P, 0.70 * P, zp, zp + em,
                 ensemble="Platine — plaques et étiquettes", classement="DÉD", source="DOC-004", systeme="signalisation", eclate=ecl_mq,
                 couleur=C["blanc"], fonction="Inconnue (non légendée).",
                 notes="Visible sur DOC-004 seulement (rectangle clair avec marques en équerre) ; absente de DOC-007. Contour approximatif.")

    # cadre des logements : prisme percé de deux trous circulaires
    xw, rw = c["x_logements"], c["r_logement"]
    y1w, y2w = c["y_logement_principal"], c["y_logement_direction"]
    x0c, x1c, y0c, y1c = xs["x_cadre_debut"], xs["x_cadre_fin"], c["y_cadre_avant"], c["y_cadre_arriere"]
    M.prisme_plan("Platine — cadre des deux logements", [(x0c, y0c), (x1c, y0c), (x1c, y1c), (x0c, y1c)], zpi, zp,
                  trous=[cercle(xw, y1w, rw), cercle(xw, y2w, rw)], ensemble="Logements des singularités (platine)",
                  repere="DOC-007 n°1 et n°2", classement="DOC", source=S47, systeme="singularites", eclate=ecl_pl, couleur=C["platine_claire"],
                  fonction="Cadre portant les logements « MAIN SINGULARITY » (arrière) et « STEERING SINGULARITY » (avant).",
                  notes="Deux logements alignés en PROFONDEUR (DOC-007, confirmé par DOC-004), au tiers gauche.")
    M.plaque("Platine — barrette entre les logements", x0c, x1c, c["y_cadre_separation"] - 0.004, c["y_cadre_separation"] + 0.004, zp, zp + em,
             ensemble="Logements des singularités (platine)", classement="DOC", source="DOC-007", systeme="singularites", eclate=ecl_mq,
             couleur=C["blanc"], fonction="Non légendée (séparation des deux logements).")
    dalle("Platine — zone devant le cadre", x0c, x1c, ya, y0c, ensemble="Platine — zones non légendées", fonction="Non légendée.")
    dalle("Platine — zone derrière le cadre", x0c, x1c, y1c, yb, ensemble="Platine — zones non légendées", fonction="Non légendée.")
    M.plaque("Plaquette signalétique devant les logements", xw - 0.0375 * L, xw + 0.0375 * L, ya + 0.010 * L, ya + 0.033 * L, zp, zp + em,
             ensemble="Platine — plaques et étiquettes", classement="DÉD", source="DOC-004", systeme="signalisation", eclate=ecl_mq,
             couleur=C["papier"], fonction="Inconnue (plaquette striée, texte illisible).", notes="Visible sur DOC-004 seulement.")
    for nom, yw, rep, fct in (("principale", y1w, "DOC-007 n°1", "« MAIN SINGULARITY » : logement de la singularité principale (revendiqué)."),
                              ("de direction", y2w, "DOC-007 n°2", "« STEERING SINGULARITY » : logement de la singularité de direction (revendiqué).")):
        M.ajouter(f"Collerette du logement — singularité {nom}", tore(rw + 0.003, 0.003), (xw, yw, zp + 0.001),
                  ensemble="Logements des singularités (platine)", repere=rep, classement="DOC", source=S47, systeme="singularites",
                  eclate=ecl_mq, couleur=C["noir"], fonction=fct,
                  notes="Disque noir sur DOC-007 ; ouverture circulaire laissant voir une forme bombée sur DOC-004.")
        M.prisme_plan(f"Fût du logement — singularité {nom}", cercle(xw, yw, rw + 0.003), zpi - c["garde_sous_platine"], zpi,
                      trous=[cercle(xw, yw, rw)], ensemble="Logements des singularités (platine)", repere=rep, classement="DÉD",
                      source="DOC-004 (relief) ; DOC-007", systeme="singularites", eclate=ecl_pl, couleur=C["noir"], fonction=fct,
                      notes="Profondeur du fût inconnue : limitée ici au jeu platine/enveloppe.")

    # zone 4 : écran de visualisation de secours
    dalle("Platine — zone 4 (support de l'écran de secours)", xs["x_bande2_fin"], xs["x_zone4_fin"], ensemble="Écran de visualisation de secours (4)",
          repere="DOC-007 n°4", systeme="commande", fonction="Zone tramée portant l'« EMERGENCY VIEW SCREEN ».")
    M.plaque("Écran de visualisation de secours (4) — fente", c["x_fente_ecran"] - c["l_fente_ecran"] / 2, c["x_fente_ecran"] + c["l_fente_ecran"] / 2,
             0.05 * P, 0.90 * P, zp, zp + em, ensemble="Écran de visualisation de secours (4)", repere="DOC-007 n°4", classement="DOC",
             source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=C["noir"],
             fonction="« EMERGENCY VIEW SCREEN » : écran de visualisation de secours (revendiqué).",
             notes="Dessiné comme un double trait étroit sur presque toute la profondeur : nature exacte indéterminée.")
    # panneau 5 : coupure d'urgence
    E5 = "Coupure d'urgence (5)"
    dalle("Panneau 5 — fond blanc", xs["x_zone4_fin"], xs["x_panneau5_fin"], ensemble=E5, repere="DOC-007 n°5", systeme="commande",
          couleur=C["blanc"], fonction="Panneau de l'« EMERGENCY DISCONNECT ».")
    M.plaque("Panneau 5 — fenêtre d'affichage", c["x_afficheur5_debut"], c["x_afficheur5_fin"], c["y_afficheur5_avant"], c["y_afficheur5_arriere"],
             zp, zp + em, ensemble=E5, repere="DOC-007 n°5", classement="DOC", source="DOC-007 ; DOC-002 (lueur rouge à cet endroit)",
             systeme="commande", eclate=ecl_mq, couleur=C["rouge"], fonction="Non légendée (fenêtre sombre ; affichage ou voyant probable).",
             notes="[DÉD] La lueur rouge de DOC-002 se situe à l'aplomb de cette fenêtre (sous le bord gauche de la plaque 7).")
    for suff, y0, y1 in (("arrière", c["y_hachures5a_avant"], c["y_hachures5a_arriere"]), ("avant", c["y_hachures5b_avant"], c["y_hachures5b_arriere"])):
        M.plaque(f"Panneau 5 — pavé hachuré {suff}", c["x_afficheur5_debut"], c["x_afficheur5_fin"], y0, y1, zp, zp + em, ensemble=E5,
                 repere="DOC-007 n°5", classement="DOC", source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=C["jaune"],
                 fonction="Non légendé (hachures de mise en garde autour de l'organe de coupure).")
    M.ajouter("Organe rond de coupure d'urgence (5)", cylindre(c["r_interrupteur5"] * 0.7, c["h_interrupteur5"]),
              (c["x_interrupteur5"], c["y_interrupteur5"], zp + c["h_interrupteur5"] / 2), ensemble=E5, repere="DOC-007 n°5", classement="DOC",
              source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=C["rouge"],
              fonction="« EMERGENCY DISCONNECT » : déconnexion d'urgence (revendiqué).", notes="Hauteur en relief supposée [HYP].")
    M.ajouter("Organe rond de coupure d'urgence (5) — couronne", tore(c["r_interrupteur5"], 0.0025), (c["x_interrupteur5"], c["y_interrupteur5"], zp + 0.002),
              ensemble=E5, repere="DOC-007 n°5", classement="DOC", source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=C["noir"],
              fonction="« EMERGENCY DISCONNECT » (couronne extérieure du dessin).")
    # panneau 8 + 6
    E8, E6 = "Commandes d'urgence (8)", "Interrupteur général marche/arrêt (6)"
    dalle("Panneau 8/6 — fond", xs["x_panneau5_fin"], xs["x_panneau8_fin"], ensemble=E8, repere="DOC-007 n°8", systeme="commande",
          fonction="Panneau des « EMERGENCY CONTROLS » et du « MAIN UNIT ON/OFF SWITCH ».")
    M.plaque("Panneau 8 — plage blanche des touches", c["x_clavier_debut"], c["x_clavier_fin"], c["y_clavier_avant"], c["y_clavier_arriere"],
             zp, zp + em, ensemble=E8, repere="DOC-007 n°8", classement="DOC", source="DOC-007", systeme="commande", eclate=ecl_mq,
             couleur=C["blanc"], fonction="« EMERGENCY CONTROLS » : commandes d'urgence (revendiqué).")
    n = 0
    for col, ys_ in (("x_touches_col_isolee", c["y_touches_col_isolee"]), ("x_touches_col1", c["y_touches_col1"]), ("x_touches_col2", c["y_touches_col2"])):
        for yk in ys_:
            n += 1
            M.plaque(f"Panneau 8 — touche ou voyant {n:02d}", c[col] - c["l_touche"] / 2, c[col] + c["l_touche"] / 2, yk - c["p_touche"] / 2,
                     yk + c["p_touche"] / 2, zp + em, zp + em + c["h_relief_commandes"], ensemble=E8, repere="DOC-007 n°8", classement="DOC",
                     source="DOC-007 ; DOC-004 (touches claires)", systeme="commande", eclate=ecl_mq, couleur=C["noir"],
                     fonction="« EMERGENCY CONTROLS » : touche ou voyant (18 pastilles dessinées ; rôle individuel non légendé).")
    hr = c["h_relief_commandes"]
    M.plaque("Interrupteur général (6) — boîtier", c["x_marche_arret_debut"], c["x_marche_arret_fin"], c["y_marche_arret_avant"], c["y_marche_arret_arriere"],
             zp, zp + hr, ensemble=E6, repere="DOC-007 n°6", classement="DOC", source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=C["acier"],
             fonction="« MAIN UNIT ON/OFF SWITCH » : interrupteur général marche/arrêt (revendiqué).")
    xm = (c["x_marche_arret_debut"] + c["x_marche_arret_fin"]) / 2
    ym = (c["y_marche_arret_avant"] + c["y_marche_arret_arriere"]) / 2
    lm = (c["x_marche_arret_fin"] - c["x_marche_arret_debut"]) * 0.36
    pm = (c["y_marche_arret_arriere"] - c["y_marche_arret_avant"]) * 0.5
    for suff, dx, coul in (("gauche", -lm * 0.6, C["blanc"]), ("droit", lm * 0.6, C["noir"])):
        M.plaque(f"Interrupteur général (6) — poussoir {suff}", xm + dx - lm / 2, xm + dx + lm / 2, ym - pm / 2, ym + pm / 2, zp + hr, zp + 2 * hr,
                 ensemble=E6, repere="DOC-007 n°6", classement="DOC", source="DOC-007", systeme="commande", eclate=ecl_mq, couleur=coul,
                 fonction="« MAIN UNIT ON/OFF SWITCH » (deux petits carrés dessinés dans le boîtier).")
    # logement de rangement 9
    E9 = "Logement de rangement de la télécommande (9)"
    x9a, x9b = xs["x_panneau8_fin"], L - e
    z9 = zp - c["profondeur_rangement"]
    kw9 = dict(ensemble=E9, repere="DOC-007 n°9", source=S47, systeme="commande", eclate=ecl_pl, couleur=C["coque_int"],
               fonction="« REMOTE STORAGE UNIT » : rangement de la télécommande (revendiqué).")
    M.plaque("Rangement 9 — fond", x9a, x9b, ya, yb, z9 - 0.003, z9, classement="HYP", notes="Profondeur du rangement non documentée.", **kw9)
    M.plaque("Rangement 9 — cloison gauche", x9a, x9a + 0.003, ya, yb, z9, zp, classement="DÉD",
             notes="Compartiment ouvert d'où sort le cordon (DOC-004) ; zone claire sur DOC-007.", **kw9)
    M.plaque("Rangement 9 — cloison avant", x9a + 0.003, x9b, ya, ya + 0.003, z9, zp, classement="DÉD", **kw9)
    M.plaque("Rangement 9 — cloison arrière", x9a + 0.003, x9b, yb - 0.003, yb, z9, zp, classement="DÉD", **kw9)

    # ---------------- télécommande et cordon (objet mobile) --------------------------------------
    ET = "Télécommande filaire (3)"
    tx, ty, tl, tL, te = c["tc_x_centre"], c["tc_y_centre"], c["tc_largeur"], c["tc_longueur"], c["tc_epaisseur"]
    kwt = dict(ensemble=ET, repere="DOC-007 n°3", liaison="telecommande", systeme="commande", masque=("ferme",),
               fonction="« REMOTE CONTROL UNIT » : télécommande reliée à l'unité par un cordon (revendiqué).")
    M.plaque("Télécommande — boîtier", tx - tl / 2, tx + tl / 2, ty - tL / 2, ty + tL / 2, 0, te, classement="DOC",
             source="DOC-007 ; DOC-004 ; " + PH, couleur=C["coque"],
             notes="Contour de DOC-007 ; épaisseur supposée. Posée devant l'unité comme sur DOC-007 (objet mobile).", **kwt)
    M.plaque("Télécommande — fenêtre d'affichage", tx - tl * 0.40, tx + tl * 0.15, ty + tL * 0.20, ty + tL * 0.42, te, te + em, classement="DOC",
             source="DOC-007", couleur=C["blanc"], notes="Rectangle en haut du boîtier sur DOC-007.", **kwt)
    M.ajouter("Télécommande — voyant ou bouton rond", cylindre(0.0045, 0.004), (tx + tl * 0.36, ty + tL * 0.36, te + 0.002), classement="DOC",
              source="DOC-007", couleur=C["rouge"], notes="Petit cercle en haut à droite du boîtier.", **kwt)
    for k, dx in enumerate((-0.27, 0.02), 1):
        M.plaque(f"Télécommande — volet inférieur {k}", tx + tl * (dx - 0.13), tx + tl * (dx + 0.13), ty - tL * 0.42, ty + tL * 0.08, te, te + em,
                 classement="DOC", source="DOC-007", couleur=C["gris"], notes="Deux rectangles accolés sous la fenêtre.", **kwt)
    for k, dy in enumerate((0.0, -0.22), 1):
        M.plaque(f"Télécommande — touche latérale {k}", tx + tl * 0.30, tx + tl * 0.45, ty + tL * (dy - 0.07), ty + tL * (dy + 0.07), te, te + 0.004,
                 classement="DOC", source="DOC-007", couleur=C["blanc"], notes="Deux petits carrés sur le bord droit.", **kwt)
    kl, kL = c["tc_connecteur_largeur"], c["tc_connecteur_longueur"]
    yk = ty - tL / 2 - kL / 2
    M.plaque("Télécommande — bloc de raccordement", tx - kl / 2 + 0.004, tx + kl / 2 + 0.004, yk - kL / 2, yk + kL / 2, 0, te * 0.8, classement="DOC",
             source="DOC-007", couleur=C["acier"], notes="Bloc d'où part le câble (bas du dessin).", **kwt)
    # cordon : chaîne de cylindres le long d'une polyligne
    rc, xc, ycb = c["r_cordon"], c["x_cable"], c["y_cable"]
    chemin = [(tx + kl / 2 + 0.004, ycb, rc), (xc, ycb, rc), (xc, -0.035, rc), (xc, -0.012, Hc * 0.55), (xc, -0.010, Hc + 0.004),
              (xc, e + 0.02, Hc + 0.006), (xc, 0.30 * P, zp - 0.03)]
    for k in range(len(chemin) - 1):
        a, b = np.array(chemin[k]), np.array(chemin[k + 1])
        d = b - a
        lg = float(np.linalg.norm(d))
        u = d / lg
        ry = math.degrees(math.atan2(math.hypot(u[0], u[1]), u[2]))
        rz = math.degrees(math.atan2(u[1], u[0]))
        M.ajouter(f"Cordon spiralé — tronçon {k + 1}", cylindre(rc, lg + rc), tuple((a + b) / 2), (0.0, ry, rz), classement="DÉD",
                  existence="DOC image", source="DOC-007 (tracé en plan) ; DOC-004 ; " + PH + " (cordon spiralé)", couleur=C["noir"],
                  notes="Le cordon est documenté (trait simple sur DOC-007, cordon spiralé sur DOC-004 et les photos), mais son tracé 3D, sa longueur et "
                        "son diamètre (16 mm, étalon E4 de l'Équipe A) sont déduits ou supposés : pièce classée [DÉD] (correction n° 48 de la Red Team).",
                  **{**kwt, "ensemble": "Cordon de la télécommande"})

    # ---------------- noyau : carters sphériques sous les logements (DOC-008 + DOC-007) ----------
    D = c["D_ref"]
    R = D / 2
    zc = zpi - c["garde_sous_platine"] - R          # altitude de l'axe des carters
    S8 = "DOC-008 (forme, proportions) ; DOC-007 (position des logements)"
    note_noyau = ("DOC-008 dessine les deux carters côte à côte ; lu comme une élévation vue depuis une extrémité du coffre, "
                  "ce « côte à côte » devient l'alignement en profondeur de DOC-007. L'entraxe du schéma (1,62 D) est ramené à celui de DOC-007 (1,16 D).")
    for nom, court, yu, rep7 in (("principale", "P", y1w, "DOC-007 n°1"), ("de direction", "D", y2w, "DOC-007 n°2")):
        ens = f"Ensemble singularité {nom}"
        kwn = dict(ensemble=ens, eclate=(0, dy_ens if court == "P" else -dy_ens, ecl_int[2]))
        M.ajouter(f"Carter d'entraînement de singularité (1) — {nom}", sphere(R * c["k_carter"]), (xw, yu, zc), repere="DOC-008 n°1 ; " + rep7,
                  classement="DÉD", source=S8, systeme="singularites", couleur=C["violet"],
                  fonction="« Singularity drive housing » : carter censé contenir et entraîner une micro-singularité (revendiqué ; aucune réalité physique établie).",
                  notes=note_noyau + " Répartition carter (1) / enveloppe (8) ambiguë sur le schéma.", **kwn)
        M.ajouter(f"Enveloppe de refroidissement (8) — {nom}", sphere(R), (xw, yu, zc), repere="DOC-008 n°8", classement="DÉD", source=S8,
                  systeme="refroidissement", couleur=C["fluide"], opacite=0.35,
                  fonction="« Singularity cooling housing » : enveloppe de refroidissement entourant le carter (revendiqué).",
                  notes="Anneau noir de DOC-008. Diamètre extérieur pris égal au diamètre du logement de DOC-007 [DÉD].", **kwn)
        k = 0
        for s in (-1, 1):
            for a in c["bobines_positions"]:
                k += 1
                Rm = math.sqrt(max(R * R - (a * R) ** 2, 1e-9)) + c["r_fil_bobine"]
                M.ajouter(f"Bobine de champ magnétique (2) — {nom}, spire {k}", tore(Rm, c["r_fil_bobine"]), (xw, yu + s * a * R, zc), AXE["Y"],
                          repere="DOC-008 n°2", classement="DÉD", source=S8, systeme="champ_magnetique", couleur=C["cuivre"],
                          fonction="« Singularity magnetic field coil » : bobine du confinement magnétique (revendiqué).",
                          notes="Six barres noires par carter sur DOC-008, interprétées comme des spires coaxiales. Axe orienté selon Y [DÉD].",
                          **{**kwn, "eclate": (0, kwn["eclate"][1] + s * dy_bob, kwn["eclate"][2])})
        for s in (-1, 1):
            M.ajouter(f"Calotte d'extrémité des bobines — {nom}, côté {'arrière' if s > 0 else 'avant'}", sphere(0.35 * R, (1, 0.25, 1)),
                      (xw, yu + s * (c["k_calotte"] - 0.0875) * R, zc), repere="DOC-008 n°2", classement="DÉD", source="DOC-008",
                      systeme="champ_magnetique", couleur=C["metal"],
                      fonction="Non légendée (arcs clairs aux deux bouts du bobinage : flasque ou pièce polaire, interprétation).",
                      **{**kwn, "eclate": (0, kwn["eclate"][1] + s * dy_cal, kwn["eclate"][2])})
        M.ajouter(f"Raccord supérieur du carter — {nom}", cylindre(c["raccord_sup_r"], c["raccord_sup_h"]), (xw, yu, zc + R + c["raccord_sup_h"] / 2 - 0.002),
                  repere="DOC-008 (non numéroté)", classement="DÉD", source="DOC-008 ; DOC-004 (forme bombée visible dans le logement)",
                  systeme="refroidissement", couleur=C["metal"],
                  fonction="Non légendé : pavé blanc au sommet du carter où aboutissent le trait mixte (fluide) et le trait plein vers le régulateur 5.", **kwn)
        ac = c["amplificateur_cote"]
        da = (R + ac * 0.45) * math.sqrt(0.5)
        M.ajouter(f"Amplificateur de capteur de singularité (7) — {nom}", boite(ac, ac, ac), (xw, yu - da, zc + da), (45.0, 0, 0),
                  repere="DOC-008 n°7", classement="DÉD", source="DOC-008", systeme="capteurs", couleur=C["vert"],
                  fonction="« Singularity sensor booster » : amplificateur du capteur de singularité (revendiqué).",
                  notes="Carré gris incliné à 45° en haut à droite de chaque carter ; le sens (avant/arrière) est arbitraire [HYP].", **kwn)
        for j, dy in enumerate((-0.11 * D, 0.0, 0.11 * D), 1):
            z_haut, z_bas = zc - 0.25 * R, zc + c["collecteur_dz"]
            M.ajouter(f"Collecteur d'injection (4) — {nom}, tube {j}", cylindre(c["r_tube_injection"], z_haut - z_bas), (xw, yu + dy, (z_haut + z_bas) / 2),
                      repere="DOC-008 n°4", classement="DÉD", source="DOC-008", systeme="electrons", couleur=C["elec"],
                      fonction="« Electron mass injector manifold » : collecteur d'injection d'électrons censé modifier masse et charge (revendiqué).", **kwn)
    kwi = dict(eclate=ecl_int)
    M.ajouter("Collecteur d'injection (4) — rampe commune", cylindre(c["r_tube_injection"], (y1w - y2w) + 0.3 * D), (xw, (y1w + y2w) / 2, zc + c["collecteur_dz"]),
              AXE["Y"], ensemble="Injection d'électrons (4, 5, 6)", repere="DOC-008 n°4", classement="DÉD", source="DOC-008", systeme="electrons",
              couleur=C["elec"], fonction="« Electron mass injector manifold » : rampe reliant les tubes des deux carters au régulateur 5 (revendiqué).", **kwi)
    rl, rh = c["regul_electrons_l"], c["regul_electrons_h"]
    M.ajouter("Régulateur d'électrons (5)", boite(rl, rl, rh), (xw, (y1w + y2w) / 2, zc + c["regul_electrons_dz"]), ensemble="Injection d'électrons (4, 5, 6)",
              repere="DOC-008 n°5", classement="DÉD", source="DOC-008", systeme="electrons", couleur=C["elec"],
              fonction="« Electron regulator » : régulateur du flux d'électrons (revendiqué).",
              notes="Entre les deux carters et en dessous, comme sur DOC-008. Troisième dimension supposée égale à la largeur.", **kwi)
    for nom, yu in (("principale", y1w), ("de direction", y2w)):
        M.ajouter(f"Générateur / régulateur de champ magnétique (3) — {nom}", boite(c["regul_champ_p"], c["regul_champ_l"], c["regul_champ_h"]),
                  (xw, yu, zc + c["regul_champ_dz"]), ensemble="Générateurs / régulateurs de champ (3)", repere="DOC-008 n°3", classement="DÉD",
                  source="DOC-008", systeme="champ_magnetique", couleur=C["cuivre"],
                  fonction="« Magnetic field generator / regulator » : alimentation régulée des bobines (revendiqué).",
                  notes="Sous chaque carter comme sur DOC-008 ; profondeur du boîtier supposée.", **kwi)

    # ---------------- composants à emplacement HYPOTHÉTIQUE (disposition interne) ----------------
    disp = brut["disposition_interne"]["dispositions"][disposition]
    note_disp = f"Emplacement [HYP] (disposition {disposition}) : aucun document ne montre l'intérieur. Taille d'après les proportions relatives de DOC-008 (schéma non garanti à l'échelle)."
    zsol = ef + 0.004

    def zc_de(d, h):
        return zsol + h / 2 if d["fz"] == "sol" else ef + d["fz"] * Hi

    # batterie (12)
    d = disp["batterie"]
    bl, bh, bp = c["batterie_l"], c["batterie_h"], c["batterie_p"]
    zb = zc_de(d, bh)
    for k in range(6):
        yk = d["fy"] * P - bl / 2 + (k + 0.5) * bl / 6
        M.ajouter(f"Batterie (12) — élément {k + 1}", boite(bp, bl / 6 * 0.94, bh), (d["fx"] * L, yk, zb), ensemble="Batterie (12)", repere="DOC-008 n°12",
                  classement="HYP", existence="DOC image", source="DOC-008 ; texte (« alimentation par batteries »)", systeme="energie",
                  couleur=C["rouge"], fonction="« Battery supply » : alimentation électrique par batterie (revendiqué).", notes=note_disp, **kwi)
    for k, s in enumerate((-1, 1), 1):
        M.ajouter(f"Batterie (12) — borne {'+' if s < 0 else '−'}", cylindre(0.006, 0.012), (d["fx"] * L, d["fy"] * P + s * bl * 0.42, zb + bh / 2 + 0.006),
                  ensemble="Batterie (12)", repere="DOC-008 n°12", classement="HYP", existence="DOC image", source="DOC-008", systeme="energie",
                  couleur=C["metal"], fonction="« Battery supply » : borne (deux bornes dessinées, reliées par un trait épais).", notes=note_disp, **kwi)
    # réservoirs (10)
    d = disp["reservoirs"]
    rr, rhh = c["reservoir_diametre"] / 2, c["reservoir_hauteur"]
    for k, s in enumerate((-1, 1), 1):
        yk = (d["fy"] + s * d["ecart_fy"]) * P
        zr = zsol + rhh / 2
        kwr = dict(ensemble="Réservoirs de fluide de refroidissement (10)", repere="DOC-008 n°10", classement="HYP", existence="DOC image",
                   source="DOC-008", systeme="refroidissement", couleur=C["fluide"],
                   fonction="« Singularity cooling supply » : réserve de fluide de refroidissement (revendiqué ; nature du fluide non précisée).",
                   notes=note_disp, **kwi)
        M.ajouter(f"Réservoir de refroidissement (10) n°{k} — virole", cylindre(rr, rhh - 2 * rr), (d["fx"] * L, yk, zr), **kwr)
        M.ajouter(f"Réservoir de refroidissement (10) n°{k} — fond bombé bas", sphere(rr), (d["fx"] * L, yk, zr - (rhh / 2 - rr)), **kwr)
        M.ajouter(f"Réservoir de refroidissement (10) n°{k} — fond bombé haut", sphere(rr), (d["fx"] * L, yk, zr + (rhh / 2 - rr)), **kwr)
        M.ajouter(f"Réservoir de refroidissement (10) n°{k} — col", cylindre(0.05 * D, 0.12 * D), (d["fx"] * L, yk, zr + rhh / 2 + 0.05 * D), **kwr)
    # pompe (9)
    d = disp["pompe"]
    M.ajouter("Pompe de refroidissement (9)", boite(c["pompe_l"], c["pompe_p"], c["pompe_h"]), (d["fx"] * L, d["fy"] * P, zc_de(d, c["pompe_h"])),
              ensemble="Pompe de refroidissement (9)", repere="DOC-008 n°9", classement="HYP", existence="DOC image", source="DOC-008",
              systeme="refroidissement", couleur=C["fluide"],
              fonction="« Singularity cooling pump » : pompe du circuit de refroidissement (revendiqué).", notes=note_disp, **kwi)
    # générateur d'électrons (6)
    d = disp["generateur"]
    gl, gh, gp = c["generateur_l"], c["generateur_h"], c["generateur_p"]
    zg = zc_de(d, gh)
    kwg = dict(ensemble="Injection d'électrons (4, 5, 6)", repere="DOC-008 n°6", classement="HYP", existence="DOC image", source="DOC-008",
               systeme="electrons", fonction="« Electron generator » : source d'électrons alimentant le régulateur 5 (revendiqué).", notes=note_disp, **kwi)
    M.ajouter("Générateur d'électrons (6) — boîtier", boite(gl, gp, gh), (d["fx"] * L, d["fy"] * P, zg), couleur=C["blanc"], **kwg)
    M.ajouter("Générateur d'électrons (6) — bande noire médiane", boite(gl + 0.002, gp + 0.002, c["generateur_bande_h"]), (d["fx"] * L, d["fy"] * P, zg),
              couleur=C["noir"], **kwg)
    # capteurs de gravité (11)
    d = disp["capteurs"]
    ml, mh, mp = c["capteurs_module_l"], c["capteurs_module_h"], c["capteurs_module_p"]
    zm = zc_de(d, mh)
    kwv = dict(ensemble="Unité de capteurs de gravité (11)", repere="DOC-008 n°11", classement="HYP", existence="DOC image",
               source="DOC-008 ; texte (système « VGL », variable gravity lock)", systeme="capteurs", couleur=C["vert"],
               fonction="« Gravity sensor unit » : capteurs de gravité, système VGL censé verrouiller la position sur la gravité locale (revendiqué).",
               notes=note_disp, **kwi)
    M.ajouter("Capteurs de gravité (11) — socle du module", boite(ml, mp, mh * 0.62), (d["fx"] * L, d["fy"] * P, zm - mh * 0.19), **kwv)
    for k, s in enumerate((-1, 1), 1):
        M.ajouter(f"Capteurs de gravité (11) — tambour {k}", cylindre(0.2 * D, mh * 0.38), (d["fx"] * L + s * 0.26 * ml, d["fy"] * P, zm + mh * 0.31), **kwv)
    M.ajouter("Capteurs de gravité (11) — capsule", cylindre(c["capteurs_capsule_diametre"] / 2, c["capteurs_capsule_hauteur"]),
              (d["fx"] * L - ml / 2 - 0.25 * D, d["fy"] * P, zm), **kwv)
    # horloges (texte seul) et calculateurs (texte seul)
    d = disp["horloges"]
    for k in range(4):
        M.ajouter(f"Horloge au césium n°{k + 1} (volume générique)", boite(c["horloge_l"] * 0.9, c["horloge_p"], c["horloge_h"]),
                  ((d["fx"] + k * d["pas_fx"]) * L, d["fy"] * P, zc_de(d, c["horloge_h"])), ensemble="Horloges principales (texte)", repere="texte, système 5",
                  classement="HYP", existence="DOC texte", source="Texte du 2 nov. 2000 (« 4 horloges au césium ») ; aucune image", systeme="horloges",
                  couleur=C["magenta"], fonction="« Main clocks » : quatre horloges au césium servant de base de temps (revendiqué).",
                  notes="Forme, taille et emplacement entièrement [HYP]. Une horloge atomique au césium compacte du commerce est nettement plus volumineuse.", **kwi)
    d = disp["calculateurs"]
    for k in range(3):
        M.ajouter(f"Calculateur n°{k + 1} (volume générique)", boite(c["calculateur_l"], c["calculateur_p"], c["calculateur_h"]),
                  ((d["fx"] + k * d["pas_fx"]) * L, d["fy"] * P, zc_de(d, c["calculateur_h"])), ensemble="Calculateurs principaux (texte)", repere="texte, système 6",
                  classement="HYP", existence="DOC texte", source="Texte du 2 nov. 2000 (« 3 calculateurs », protocole de vote dit « Borda ») ; aucune image",
                  systeme="calcul", couleur=C["elec"], fonction="« Main computer units » : trois calculateurs à vote majoritaire (revendiqué).",
                  notes="Forme, taille et emplacement entièrement [HYP].", **kwi)

    for p in M.pieces:      # couche d'affichage : coque / couvercle / platine / interne / mobile
        if p["liaison"] == "couvercle":
            p["couche"] = "couvercle"
        elif p["liaison"] == "telecommande":
            p["couche"] = "mobile"
        elif p["ensemble"].startswith("Coffre"):
            p["couche"] = "coque"
        elif p["eclate"][2] >= ecl_pl[2] - 1e-3:      # tolérance : les décalages sont arrondis à 0,1 mm
            p["couche"] = "platine"
        else:
            p["couche"] = "interne"

    etats = {"ferme": {"libelle": "Fermé", "angle_couvercle_deg": 0, "eclate": 0},
             "ouvert": {"libelle": "Ouvert", "angle_couvercle_deg": c["angle_ouverture_deg"], "eclate": 0},
             "eclate": {"libelle": "Éclaté", "angle_couvercle_deg": c["angle_ouverture_deg"], "eclate": 1},
             "a_plat": {"libelle": "Couvercle à plat (DOC-007)", "angle_couvercle_deg": c["angle_a_plat_deg"], "eclate": 0}}
    return {"pieces": M.pieces, "etats": etats,
            "articulations": {"couvercle": {"point": _arrondi([0, P, Hc]), "axe": [-1, 0, 0],
                                            "note": "Rotation d'angle positif autour de l'axe −X passant par ce point (arête arrière haute du corps)."}},
            "emprise": {"min": [0, c["y_cable"] - 0.02, 0], "max": [L, P, Hc + Hv]},
            "cotes_cles": {"L": L, "P": P, "H_corps": Hc, "H_couvercle": Hv, "z_platine": zp, "z_axe_carters": zc, "D_ref": D}}


# ------------------------------------------------------------------------------------------------
# VARIANTE B — écorché DOC-005 (prisme à extrémités biseautées) : enveloppe et volumes principaux
# ------------------------------------------------------------------------------------------------
def construire_variante_B(c, brut):
    M = Modele("B")
    L, P, H = c["B_L"], c["B_P"], c["B_H"]
    cg, cgh, cd = c["B_biseau_gauche"], c["B_biseau_gauche_h"], c["B_biseau_droit"]
    S = "DOC-005"
    inconnu = "Inconnue : DOC-005 porte 35 repères mais AUCUNE légende dans la copie archivée."
    # enveloppe : profil dans le plan (X, Z), extrudé selon Y. Rotation Rx(+90°) : y_local → Z, z_local → −Y.
    profil = [(cg, 0), (L - cd, 0), (L, H), (0, H), (0, cgh)]
    cx, cz = L / 2, H / 2
    M.ajouter("Enveloppe prismatique à extrémités biseautées", prisme([(x - cx, z - cz) for x, z in profil], P), (cx, P / 2, cz), (90.0, 0, 0),
              ensemble="Enveloppe (DOC-005)", repere="—", classement="DOC", source=S, systeme="structure", couleur=C["coque"], opacite=0.16, fantome=True,
              fonction="Enveloppe de l'ensemble « MAJOR SYSTEMS DESCRIPTION — ARMY MODEL GE / C204 » (titre du dessin).",
              notes="Forme lue sur l'écorché : dessus plan, extrémité droite fuyante sur toute la hauteur, extrémité gauche biseautée en partie basse. "
                    "Rapports H/L mesuré, P/L très incertain (0,24–0,49). Échelle absolue ARBITRAIRE (L pris égal à la variante A). Pas de couvercle visible.")
    for k, (fx, fy) in enumerate(((cg / L + 0.035, 0.08), (cg / L + 0.035, 0.92), (1 - cd / L - 0.035, 0.08), (1 - cd / L - 0.035, 0.92)), 1):
        M.plaque(f"Patin d'appui n°{k}", fx * L - 0.035 * L, fx * L + 0.035 * L, fy * P - 0.03, fy * P + 0.03, -0.022, 0.0, ensemble="Enveloppe (DOC-005)",
                 repere="—", classement="DÉD", source=S, systeme="structure", couleur=C["noir"], fonction="Non légendé (masses noires aux angles inférieurs : patins ou sabots).",
                 notes="Trois masses noires visibles ; la quatrième est supposée par symétrie.")
    for v in brut["variante_B"]["B_volumes"]["liste"]:
        pos = (v["fx"] * L, v["fy"] * P, v["fz"] * H)
        rot = (0, 0, 0)
        if v["type"] == "boite":
            prim = boite(v["lx"] * L, v["ly"] * P, v["lz"] * H)
        elif v["type"] == "cylindre":
            h = v["h"] * {"X": L, "Y": P, "Z": H}[v["axe"]]
            prim, rot = cylindre(v["r"] * L, h), AXE[v["axe"]]
        elif v["type"] == "sphere":
            prim = sphere(v["r"] * L, (1, 1, v.get("ez", 1.0)))
        elif v["type"] == "tore":
            prim, rot = tore(v["r"] * L, v["r2"] * L), AXE[v["axe"]]
        else:
            raise ValueError(v["type"])
        pupitre = v["id"] in ("pont_pupitre", "fente_15", "plaque_16", "panneau_17", "afficheur_17", "bouton_17", "barre_pupitre", "cadre_35", "inter_35")
        structure = v["id"].startswith("cloison") or v["id"] == "pont_pupitre" or v["id"] == "barre_pupitre"
        coul = C["acier"] if structure else (C["platine_claire"] if pupitre else C["brun"])
        if v["id"] in ("fente_15", "afficheur_17", "inter_35"):
            coul = C["noir"]
        if v["id"] == "bouton_17":
            coul = C["rouge"]
        note = "Volume générique approché d'après l'unique vue ; profondeur (fy) supposée."
        if v["id"] in ("panneau_17", "afficheur_17", "bouton_17", "cadre_35", "inter_35", "fente_15", "plaque_16"):
            note += (" Rapprochement [DÉD, confiance faible à moyenne] avec le pupitre de DOC-007 : fente (15) ↔ écran de secours (4) ; "
                     "fenêtre + bouton rond (17) ↔ coupure d'urgence (5) ; interrupteur encadré (35) ↔ marche/arrêt (6) ; plaque (16) ↔ rangement (9).")
        M.ajouter(v["nom"], prim, pos, rot, ensemble="Pupitre d'extrémité droite (DOC-005)" if pupitre else "Volumes internes (DOC-005)",
                  repere=("DOC-005 n°" + v["reperes"]) if v["reperes"] != "—" else "DOC-005 (non numéroté)", classement="DÉD", source=S,
                  systeme="commande" if (pupitre and not structure) else ("structure" if structure else "inconnu"), couleur=coul,
                  fonction=inconnu, notes=note, eclate=(0, 0, 0.0 if structure else (0.35 * L if not pupitre else 0.46 * L)))
    for p in M.pieces:
        if p["ensemble"].startswith("Enveloppe"):
            p["couche"] = "coque"
        elif p["ensemble"].startswith("Pupitre"):
            p["couche"] = "platine"
        else:
            p["couche"] = "interne"
    etats = {"ferme": {"libelle": "Fermé", "angle_couvercle_deg": 0, "eclate": 0},
             "ouvert": {"libelle": "Ouvert", "angle_couvercle_deg": 0, "eclate": 0},
             "eclate": {"libelle": "Éclaté", "angle_couvercle_deg": 0, "eclate": 1},
             "a_plat": {"libelle": "Couvercle à plat (DOC-007)", "angle_couvercle_deg": 0, "eclate": 0}}
    return {"pieces": M.pieces, "etats": etats, "articulations": {},
            "emprise": {"min": [0, 0, -0.022], "max": [L, P, H * 1.05]},
            "cotes_cles": {"L": L, "P": P, "H": H}}


# ------------------------------------------------------------------------------------------------
def bilan(pieces):
    b = {k: 0 for k in CLASSEMENTS}
    for p in pieces:
        b[p["classement"]] += 1
    return b


PHOTOS_ILLUSTRATION = ("DOC-001", "DOC-002", "DOC-003", "DOC-004")


def appui_documentaire(piece):
    """Nature des documents cités comme source : dessin du manuel seul, photo ou illustration, schéma, texte."""
    src = piece["source"]
    photo = any(d in src for d in PHOTOS_ILLUSTRATION)
    if "DOC-005" in src:
        return "écorché DOC-005"
    if "DOC-008" in src:
        return "schéma DOC-008" + (" + dessin DOC-007" if "DOC-007" in src else "")
    if "DOC-007" in src:
        return "dessin DOC-007 + photo ou illustration" if photo else "dessin DOC-007 seul"
    if photo:
        return "photo ou illustration seule"
    if "exte" in src:
        return "texte seul"
    return "aucun document (supposition)"


def est_marquage_repete(piece):
    """Raies noires, fonds de bande et pastilles du pupitre : motifs répétés qui gonflent le décompte [DOC]."""
    n = piece["nom"]
    return "raie noire" in n or "bande de danger" in n and "(fond)" in n or "touche ou voyant" in n


def bilan_couches(pieces):
    """Bilan de classement séparant l'extérieur (ce que montrent les images) de l'intérieur (sous la platine)."""
    out = {"exterieur": {k: 0 for k in CLASSEMENTS}, "interieur": {k: 0 for k in CLASSEMENTS}}
    for p in pieces:
        out["interieur" if p["couche"] == "interne" else "exterieur"][p["classement"]] += 1
    doc = [p for p in pieces if p["classement"] == "DOC"]
    appuis = {}
    for p in doc:
        appuis[p["appui"]] = appuis.get(p["appui"], 0) + 1
    out["detail_DOC"] = {"total": len(doc), "marquages_repetes": sum(est_marquage_repete(p) for p in doc),
                         "dont_raies_noires": sum("raie noire" in p["nom"] for p in doc),
                         "dont_fonds_de_bande": sum("(fond)" in p["nom"] and "bande de danger" in p["nom"] for p in doc),
                         "dont_pastilles_du_pupitre": sum("touche ou voyant" in p["nom"] for p in doc),
                         "par_appui": appuis}
    out["note"] = ("Extérieur = coque, couvercle, platine, télécommande ; intérieur = tout ce qui est sous la platine. Aucune pièce intérieure n'est [DOC]. "
                   "Pour les pièces relevées sur la seule vue de dessus DOC-007, la troisième dimension (épaisseur, relief) est supposée.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--parametres", default=str(ICI / "parametres.json"))
    ap.add_argument("--sortie", default=str(ICI / "modele_c204.json"))
    args = ap.parse_args()

    brut, c, infos = charger_parametres(args.parametres)
    ecrire_parametres(brut, args.parametres)
    di = brut["disposition_interne"]

    A = construire_variante_A(c, brut, di["retenue"], "A")
    A2 = construire_variante_A(c, brut, di["alternative"], "A2")
    B = construire_variante_B(c, brut)

    for v in (A, A2, B):
        for p in v["pieces"]:
            p["appui"] = appui_documentaire(p)
        v["bilan_couches"] = bilan_couches(v["pieces"])

    # taux d'occupation du volume intérieur par les composants de DOC-008 (variante A)
    vol_int = (c["L"] - 2 * c["e_rebord"]) * (c["P"] - 2 * c["e_rebord"]) * (c["H_corps"] - c["retrait_platine"] - c["e_platine"] - c["e_fond"])
    internes = [p for p in A["pieces"] if p["systeme"] not in ("structure", "signalisation", "commande") and "(platine)" not in p["ensemble"]
                and "Enveloppe de refroidissement" not in p["nom"] and "Carter d'entraînement" not in p["nom"]]
    vol_comp = sum(p["volume_m3"] for p in internes) + sum(p["volume_m3"] for p in A["pieces"] if "Enveloppe de refroidissement" in p["nom"])
    vol_texte = sum(p["volume_m3"] for p in internes if p["existence"] == "DOC texte")
    A["bilan_volumique"] = {"volume_interieur_m3": round(vol_int, 5), "volume_composants_m3": round(vol_comp, 5),
                            "taux_occupation": round(vol_comp / vol_int, 3),
                            "volume_composants_DOC008_m3": round(vol_comp - vol_texte, 5),
                            "taux_occupation_DOC008": round((vol_comp - vol_texte) / vol_int, 3),
                            "volume_volumes_generiques_texte_m3": round(vol_texte, 5),
                            "note": "Composants de DOC-008 dimensionnés à l'échelle du schéma calée sur le diamètre des logements : "
                                    "ils n'occupent qu'une faible part du volume intérieur. Indice que DOC-008 n'est pas à l'échelle, "
                                    "ou que l'essentiel du volume (et des 227 kg revendiqués) n'est pas décrit. Les horloges et calculateurs "
                                    "(texte seul) sont des volumes génériques [HYP], proportionnels à L : le taux ne dépend presque pas de l'échelle."}

    modele = {
        "meta": {
            "titre": "Modèle 3D paramétrique de l'unité « C204 » — reconstruction documentaire",
            "avertissement": "Reconstruction d'un objet tel qu'il est DÉCRIT par des documents non authentifiés (messages « John Titor », 2000-2001). "
                             "Rien n'atteste que l'objet ait existé ni fonctionné. Les « fonctions revendiquées » sont celles des légendes et du texte : "
                             "elles ne sont ni vérifiées ni physiquement établies.",
            "equipe": "Équipe E — ingénierie inverse et reconstruction 3D",
            "genere_le": datetime.date.today().isoformat(),
            "genere_par": "generer_modele.py à partir de parametres.json",
            "unite": "m",
            "conventions": {
                "repere": brut["_meta"]["repere"],
                "primitives": {"boite": "dimensions [dx, dy, dz], centrée", "cylindre": "rayon, hauteur, axe local Z, centré",
                               "sphere": "rayon, échelle optionnelle [sx, sy, sz]", "tore": "rayon_majeur, rayon_mineur, axe local Z",
                               "prisme": "profil [[u, v]…] dans le plan local XY, trous optionnels, hauteur selon Z local, centré"},
                "rotation": "rotation_deg = [rx, ry, rz], R = Rz·Ry·Rx (axes fixes) ; quaternion = [x, y, z, w] équivalent",
                "etats": "positions données couvercle fermé ; état = rotation des pièces « couvercle » autour de la charnière + facteur d'éclatement × eclate",
                "masque": "liste des états où la pièce n'est pas représentée (télécommande rangée à l'état fermé)",
                "fantome": "pièce d'enveloppe rendue translucide dans les vues intérieures",
                "couche": "coque | couvercle | platine | interne | mobile : regroupement d'affichage (masquage par couche dans la visionneuse et les rendus)",
                "appui": "nature des documents cités en source (dessin DOC-007 seul, photo ou illustration, schéma DOC-008, texte seul…) : distingue le « [DOC] dessin » du « [DOC] photo »",
                "classement": "classement de la pièce TELLE QUE MODÉLISÉE (forme + position) ; « existence » précise si le composant figure sur une image, dans le texte seul, ou est supposé",
            },
            "classements": CLASSEMENTS,
            "systemes": SYSTEMES,
        },
        "cotes": {k: {"valeur": infos[k]["valeur"], "incertitude": infos[k].get("incertitude"), "unite": infos[k].get("unite", "m"),
                      "etiquette": infos[k]["etiquette"], "source": infos[k]["source"]} for k in infos},
        "variantes": {
            "A": {"nom": "Variante A — coffre plat à couvercle articulé",
                  "description": "Coffre de DOC-001/002/003/004/007 ; composants internes de DOC-008 et du texte. Disposition interne " + di["dispositions"][di["retenue"]]["nom"] + ".",
                  "documents": "DOC-001, DOC-002, DOC-003, DOC-004, DOC-007, DOC-008, texte", **A, "bilan_classement": bilan(A["pieces"])},
            "A2": {"nom": "Variante A′ — même coffre, autre disposition interne",
                   "description": "Identique à la variante A sauf l'emplacement des composants [HYP]. Disposition interne " + di["dispositions"][di["alternative"]]["nom"] + ".",
                   "documents": "idem variante A", **A2, "bilan_classement": bilan(A2["pieces"])},
            "B": {"nom": "Variante B — écorché DOC-005 (prisme biseauté)",
                  "description": "Enveloppe et volumes principaux de l'écorché « MAJOR SYSTEMS DESCRIPTION — ARMY MODEL GE / C204 », modélisé SÉPARÉMENT car incohérent avec le coffre plat. Échelle arbitraire.",
                  "documents": "DOC-005", **B, "bilan_classement": bilan(B["pieces"])},
        },
    }
    Path(args.sortie).write_text(json.dumps(modele, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in modele["variantes"].items():
        print(f"variante {k:2s} : {len(v['pieces']):3d} pièces  {v['bilan_classement']}")
    print("bilan volumique A :", A["bilan_volumique"])
    print("cotes clés A :", {k: round(v, 4) for k, v in A["cotes_cles"].items()})
    print("écrit :", args.sortie)


if __name__ == "__main__":
    main()
