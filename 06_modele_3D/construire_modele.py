#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — construction des maillages et exports 3D.

    modele_c204.json  ──►  exports/*.glb, *.obj (+ .mtl), *.stl

Trois configurations de la variante A (coffre) :
    ferme            coffre fermé (télécommande rangée, non représentée)
    ouvert_interne   couvercle ouvert, composants internes ; dans le GLB, les enveloppes sont translucides
    eclate           vue éclatée
plus la variante B (écorché DOC-005 : enveloppe translucide et volumes principaux) et, à titre de
comparaison, la variante A′ (autre disposition interne hypothétique) en configuration ouverte.

Couleurs : par classement (DOC bleu, DÉD orange, HYP rose), légèrement modulées par la clarté de la
pièce pour que les marquages restent lisibles. Le STL ne porte pas de couleur (limite du format).
Axes : OBJ et STL en Z vers le haut (repère du modèle, en mètres) ; GLB converti en Y vers le haut
(convention glTF).

Rappel : reconstruction d'un objet DÉCRIT par des documents non authentifiés ; rien n'atteste qu'il
ait existé ni fonctionné.

Usage : python construire_modele.py [--modele modele_c204.json] [--sans-rendus]
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon

ICI = Path(__file__).resolve().parent
SECTIONS = 40          # facettes des cylindres


# ------------------------------------------------------------------------------------------------
# Maillage d'une primitive
# ------------------------------------------------------------------------------------------------
def maillage_primitive(p):
    t = p["type"]
    if t == "boite":
        return trimesh.creation.box(extents=p["dimensions"])
    if t == "cylindre":
        return trimesh.creation.cylinder(radius=p["rayon"], height=p["hauteur"], sections=SECTIONS)
    if t == "sphere":
        m = trimesh.creation.uv_sphere(radius=p["rayon"], count=[18, 28])
        if "echelle" in p:
            m.apply_scale(p["echelle"])
        return m
    if t == "tore":
        return trimesh.creation.torus(major_radius=p["rayon_majeur"], minor_radius=p["rayon_mineur"], major_sections=SECTIONS, minor_sections=12)
    if t == "prisme":
        poly = Polygon(p["profil"], p.get("trous", []))
        if not poly.is_valid:
            poly = poly.buffer(0)
        m = trimesh.creation.extrude_polygon(poly, p["hauteur"])
        m.apply_translation([0, 0, -p["hauteur"] / 2])
        return m
    raise ValueError(f"primitive inconnue : {t}")


def matrice_piece(piece):
    """Matrice 4×4 de la pièce en position fermée (R = Rz·Ry·Rx, puis translation)."""
    x, y, z, w = piece["quaternion"]
    T = trimesh.transformations.quaternion_matrix([w, x, y, z])
    T[:3, 3] = piece["position"]
    return T


def matrice_etat(piece, variante, etat):
    """Transformation supplémentaire due à l'état (ouverture du couvercle, éclatement)."""
    e = variante["etats"][etat]
    T = np.eye(4)
    if piece["liaison"] == "couvercle" and "couvercle" in variante["articulations"] and e["angle_couvercle_deg"]:
        art = variante["articulations"]["couvercle"]
        T = trimesh.transformations.rotation_matrix(math.radians(e["angle_couvercle_deg"]), art["axe"], art["point"])
    if e["eclate"]:
        D = np.eye(4)
        D[:3, 3] = np.array(piece["eclate"]) * e["eclate"]
        T = D @ T
    return T


def maillage_piece(piece, variante, etat):
    m = maillage_primitive(piece["primitive"])
    m.apply_transform(matrice_etat(piece, variante, etat) @ matrice_piece(piece))
    return m


def pieces_visibles(variante, etat, filtre=None):
    for p in variante["pieces"]:
        if etat in p.get("masque", []):
            continue
        if filtre and not filtre(p):
            continue
        yield p


# ------------------------------------------------------------------------------------------------
# Couleurs
# ------------------------------------------------------------------------------------------------
def hex_rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255.0


def clarte(rgb):
    return float(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])


def couleur_piece(piece, modele, mode="classement"):
    """RGB (0–1) selon le mode : 'classement', 'aspect' ou 'systeme'."""
    aspect = hex_rgb(piece["couleur"])
    if mode == "aspect":
        return aspect
    base = hex_rgb(modele["meta"]["classements"][piece["classement"]]["couleur"]) if mode == "classement" \
        else hex_rgb(modele["meta"]["systemes"][piece["systeme"]]["couleur"])
    return np.clip(base * (0.62 + 0.55 * clarte(aspect)), 0, 1)


# ------------------------------------------------------------------------------------------------
# Exports
# ------------------------------------------------------------------------------------------------
ZUP_VERS_YUP = trimesh.transformations.rotation_matrix(-math.pi / 2, [1, 0, 0])


def exporter(modele, cle_variante, etat, nom, dossier, fantomes_translucides=False):
    variante = modele["variantes"][cle_variante]
    pieces = list(pieces_visibles(variante, etat))
    mailles = [maillage_piece(p, variante, etat) for p in pieces]

    # --- GLB : un nœud par pièce, matériau PBR coloré par classement -------------------------
    scene = trimesh.Scene()
    for p, m in zip(pieces, mailles):
        rgb = couleur_piece(p, modele, "classement")
        alpha = p.get("opacite", 1.0)
        if fantomes_translucides and p.get("fantome"):
            alpha = min(alpha, 0.22)
        mat = trimesh.visual.material.PBRMaterial(
            name=f"{p['classement']}_{p['id']}", baseColorFactor=[float(rgb[0]), float(rgb[1]), float(rgb[2]), float(alpha)],
            metallicFactor=0.1, roughnessFactor=0.75, alphaMode="BLEND" if alpha < 0.999 else "OPAQUE", doubleSided=alpha < 0.999)
        g = m.copy()
        g.apply_transform(ZUP_VERS_YUP)
        g.visual = trimesh.visual.TextureVisuals(material=mat)
        g.metadata.update({"id": p["id"], "nom": p["nom"], "classement": p["classement"], "source": p["source"], "repere": p["repere"]})
        nom_noeud = f"{p['id']} [{p['classement']}] {p['nom']}"
        scene.add_geometry(g, node_name=nom_noeud, geom_name=nom_noeud)
    (dossier / f"{nom}.glb").write_bytes(scene.export(file_type="glb"))

    # --- OBJ + MTL : un groupe par pièce, trois matériaux de classement (+ translucides) -----
    mtl, vus = [], set()
    obj = [f"# Programme C204 — Équipe E — {variante['nom']} — état : {etat}",
           "# Reconstruction documentaire d'un objet DÉCRIT ; rien n'atteste qu'il ait existé ni fonctionné.",
           "# Unité : mètre ; Z vers le haut. Matériaux = classement (DOC / DED / HYP).", f"mtllib {nom}.mtl"]
    decal = 1
    for p, m in zip(pieces, mailles):
        cl = {"DOC": "DOC", "DÉD": "DED", "HYP": "HYP"}[p["classement"]]
        translucide = p.get("opacite", 1.0) < 0.999 or (fantomes_translucides and p.get("fantome"))
        nom_mat = cl + ("_translucide" if translucide else "")
        if nom_mat not in vus:
            vus.add(nom_mat)
            rgb = hex_rgb(modele["meta"]["classements"][p["classement"]]["couleur"])
            mtl += [f"newmtl {nom_mat}", "Kd %.4f %.4f %.4f" % tuple(rgb), "Ka 0.1 0.1 0.1", "Ks 0.05 0.05 0.05", "Ns 20",
                    f"d {0.25 if translucide else 1.0}", ""]
        obj.append(f"o {p['id']}_{''.join(ch if ch.isalnum() else '_' for ch in p['nom'])[:60]}")
        obj.append(f"usemtl {nom_mat}")
        obj += ["v %.6f %.6f %.6f" % tuple(v) for v in m.vertices]
        obj += ["f %d %d %d" % tuple(f + decal) for f in m.faces]
        decal += len(m.vertices)
    (dossier / f"{nom}.obj").write_text("\n".join(obj) + "\n", encoding="utf-8")
    (dossier / f"{nom}.mtl").write_text("\n".join(mtl), encoding="utf-8")

    # --- STL binaire : maillage unique (sans couleur) -----------------------------------------
    tout = trimesh.util.concatenate(mailles)
    tout.export(dossier / f"{nom}.stl")
    return {"fichier": nom, "pieces": len(pieces), "triangles": int(sum(len(m.faces) for m in mailles)),
            "etendue_m": [round(float(v), 3) for v in (tout.bounds[1] - tout.bounds[0])]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modele", default=str(ICI / "modele_c204.json"))
    ap.add_argument("--sans-rendus", action="store_true", help="ne pas lancer rendre_vues.py après les exports")
    args = ap.parse_args()
    modele = json.loads(Path(args.modele).read_text(encoding="utf-8"))
    dossier = ICI / "exports"
    dossier.mkdir(exist_ok=True)
    bilan = [
        exporter(modele, "A", "ferme", "c204_A_ferme", dossier),
        exporter(modele, "A", "ouvert", "c204_A_ouvert_interne", dossier, fantomes_translucides=True),
        exporter(modele, "A", "eclate", "c204_A_eclate", dossier),
        exporter(modele, "A2", "ouvert", "c204_A2_ouvert_interne_disposition_I2", dossier, fantomes_translucides=True),
        exporter(modele, "B", "ouvert", "c204_B_ecorche_DOC-005", dossier, fantomes_translucides=True),
    ]
    for b in bilan:
        print("%-42s %4d pièces %7d triangles  étendue %s m" % (b["fichier"], b["pieces"], b["triangles"], b["etendue_m"]))
    (dossier / "LISEZ-MOI.txt").write_text(
        "Exports du modèle 3D C204 (Équipe E) — générés par construire_modele.py à partir de modele_c204.json.\n"
        "Reconstruction documentaire d'un objet DÉCRIT par des documents non authentifiés ; rien n'atteste qu'il ait existé ni fonctionné.\n\n"
        "Unité : mètre. OBJ et STL : Z vers le haut (repère du modèle). GLB : Y vers le haut (convention glTF).\n"
        "Couleurs (GLB, OBJ+MTL) : classement — DOC bleu #0072B2, DÉD orange #E69F00, HYP rose #CC79A7. Le STL ne porte pas de couleur.\n"
        "Dans les fichiers « ouvert_interne » et « B », les enveloppes sont translucides (GLB, MTL) pour laisser voir l'intérieur.\n\n"
        + "\n".join("%s : %d pièces, %d triangles, étendue %s m" % (b["fichier"], b["pieces"], b["triangles"], b["etendue_m"]) for b in bilan) + "\n",
        encoding="utf-8")
    if not args.sans_rendus:
        import rendre_vues
        rendre_vues.main(modele)


if __name__ == "__main__":
    main()
