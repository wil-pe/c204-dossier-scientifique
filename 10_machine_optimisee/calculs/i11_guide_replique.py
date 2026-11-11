#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i11 : données de construction de la « réplique inerte » du coffre C204 (guide, partie A).

Relit (lecture seule) les cotes de l'Équipe E (06_modele_3D/parametres.json : chaque cote = rapport × référence)
et celles de l'Équipe A (02_reconstruction/dimensions.json), et produit pour une longueur L donnée :

  guide/replique_cotes.csv            toutes les cotes utiles, en mm, avec leur statut (DOC / DÉD / HYP) et leur règle
  guide/replique_debit.csv            liste de débit des panneaux (contreplaqué), variantes « modèle E » et « photos A »
  schemas/replique_platine_gabarit.svg gabarit coté de la platine supérieure (vue de dessus, avant en bas)

Rien de ceci n'est le plan d'une machine : c'est une maquette de présentation d'un objet DÉCRIT par des documents
non authentifiés ; aucune cote n'est mesurée sur un objet réel (échelle : confiance faible).

Usage : python i11_guide_replique.py [L_en_metres]      (défaut : 0,85)
"""
import json
import math
import sys
from html import escape
from pathlib import Path

from i00_commun import RACINE, SCH, ecrire_csv, ecrire_txt

GUIDE = RACINE / "guide"
GUIDE.mkdir(exist_ok=True)
SRC_E = RACINE.parent / "06_modele_3D" / "parametres.json"
SRC_A = RACINE.parent / "02_reconstruction" / "dimensions.json"
E_PANNEAU = 0.009      # contreplaqué de 9 mm pour le corps et le couvercle [choix de maquette]
E_PLATINE = 0.003      # contreplaqué ou PVC expansé de 3 mm pour la platine [choix de maquette]
RHO_CP = 600.0         # kg/m³, contreplaqué de peuplier ou d'okoumé [estimation]
mm = lambda v: round(1000 * v)


# Nomenclature de la réplique : désignation, quantité, prix bas €, prix haut € (ESTIMATIONS 2026, non vérifiées), statut documentaire
REPLIQUE = [
    ("Contreplaqué de 9 mm (≈ 1,0 m² utile : un panneau de 1 220 × 1 220 mm)", "1", 30, 50, "matériau de maquette (le coffre réel n'est pas identifié)"),
    ("Contreplaqué ou PVC expansé de 3 mm (≈ 0,25 m²)", "1", 8, 15, "matériau de maquette"),
    ("Tasseaux de 10 × 10 mm", "2,5 m", 4, 6, "inventé pour la maquette (support de platine)"),
    ("Charnières (2 de ≈ 60 mm) ou charnière à piano", "2", 8, 15, "DOC : deux charnières sur DOC-007 ; une tringle continue sur DOC-004"),
    ("Fermoirs à levier (2) et poignées encastrées (2)", "4", 20, 35, "DÉD : fermoirs visibles en façade ; position incertaine"),
    ("Compas ou chaînette de retenue du couvercle (ouverture ≈ 108°)", "1", 5, 8, "inventé pour la maquette"),
    ("Apprêt et peinture satinée très sombre (noir ou vert-noir)", "1", 15, 25, "DOC : extérieur sombre sur les photos ; teinte exacte inconnue"),
    ("Ruban de signalisation jaune et noir de 50 mm (ou pochoir)", "1 rouleau", 6, 10, "DOC : bandes de danger ; largeur réelle discutée (2 ou 3 pouces)"),
    ("Étiquettes imprimées sur papier adhésif (plaque 7, blanche à liseré rouge, orange, jaune)", "1 planche", 8, 12, "DOC (présence) ; textes ILLISIBLES : contenu inventé ou laissé vide"),
    ("Pupitre factice : bouton rouge, interrupteur à bascule, 18 pastilles, plaquette rouge", "1 lot", 12, 20, "DOC (disposition) ; nature des organes supposée"),
    ("Deux « dômes » noirs à sommet jaune de 60 à 80 mm (demi-sphères en plastique)", "2", 6, 12, "DOC : DOC-013 ; diamètre 45 à 60 mm selon l'Équipe A"),
    ("Télécommande : boîtier ≈ 82 × 86 × 25 mm, clavier 4 × 4 factice, cordon spiralé", "1", 12, 20, "DOC : boîtier et cordon ; épaisseur supposée"),
    ("Colle à bois, vis, pâte à bois, abrasifs", "1 lot", 8, 12, "—"),
]


def charger_cotes(L):
    """Recalcule toutes les cotes proportionnelles de l'Équipe E pour la longueur L (m)."""
    p = json.loads(SRC_E.read_text(encoding="utf-8"))
    plat, cotes = {}, {}
    for sec, d in p.items():
        if sec.startswith("_") or not isinstance(d, dict):
            continue
        for k, v in d.items():
            if isinstance(v, dict) and "valeur" in v:
                plat[k] = dict(v, section=sec)
    plat["L"]["valeur"] = L

    def resoudre(k, pile=()):
        if k in cotes:
            return cotes[k]
        v = plat[k]
        if "rapport" in v and v.get("reference") in plat and k not in pile:
            ref = resoudre(v["reference"], pile + (k,))
            r = v["rapport"]
            cotes[k] = [x * ref for x in r] if isinstance(r, list) else r * ref
        else:
            cotes[k] = v["valeur"]
        return cotes[k]

    for k in plat:
        resoudre(k)
    return cotes, plat


def main(L=0.85):
    c, meta = charger_cotes(L)
    A = {x["id"]: x for x in json.loads(SRC_A.read_text(encoding="utf-8"))["cotes"]}
    kA = L / A["L"]["valeur"]                       # mise à l'échelle des cotes de l'Équipe A
    P, Hc, Hl, e = c["P"], c["H_corps"], c["H_couvercle"], c["e_rebord"]
    journal = ["i11 — RÉPLIQUE INERTE : cotes et débit pour L = %.3f m" % L, "=" * 90]

    # ------------------------------------------------------------------ 1. cotes
    regle = lambda k: (("%s × %s" % (str(meta[k]["rapport"]).replace(".", ","), meta[k]["reference"])) if "rapport" in meta[k] and not isinstance(meta[k]["rapport"], list) else "valeur fixe (ne suit pas L)")
    lignes = []
    utiles = [("Enveloppe", ["L", "P", "H_corps", "H_couvercle", "e_rebord", "retrait_platine", "angle_ouverture_deg"]),
              ("Platine — zones (abscisses depuis l'extrémité gauche)", ["x_division_gauche", "x_bande1_debut", "x_bande1_fin", "x_cadre_debut", "x_cadre_fin", "x_bande2_debut",
                                                                         "x_bande2_fin", "x_fente_ecran", "l_fente_ecran", "x_zone4_fin", "x_panneau5_fin", "x_panneau8_fin"]),
              ("Platine — cadre des logements (ordonnées depuis l'avant)", ["y_cadre_avant", "y_cadre_separation", "y_cadre_arriere"]),
              ("Logements", ["x_logements", "y_logement_direction", "y_logement_principal", "r_logement"]),
              ("Bandes de danger", ["bande_pente", "bande_periode", "bande_epaisseur_noire", "bande_phase"]),
              ("Pupitre", ["x_afficheur5_debut", "x_afficheur5_fin", "y_afficheur5_avant", "y_afficheur5_arriere", "x_interrupteur5", "y_interrupteur5", "r_interrupteur5",
                           "x_clavier_debut", "x_clavier_fin", "y_clavier_avant", "y_clavier_arriere", "x_touches_col_isolee", "x_touches_col1", "x_touches_col2",
                           "l_touche", "p_touche", "x_marche_arret_debut", "x_marche_arret_fin", "y_marche_arret_avant", "y_marche_arret_arriere", "profondeur_rangement"]),
              ("Intérieur du couvercle (v : depuis la charnière)", ["x_plaque7_debut", "x_plaque7_fin", "v_plaque7_debut", "v_plaque7_fin", "x_charniere1_debut", "x_charniere1_fin",
                                                                    "x_charniere2_debut", "x_charniere2_fin", "x_etiq_centrale_debut", "x_etiq_centrale_fin", "v_etiq_blanche_debut",
                                                                    "v_etiq_blanche_fin", "v_etiq_orange_debut", "v_etiq_orange_fin", "x_etiq_jaune_debut", "x_etiq_jaune_fin",
                                                                    "v_etiq_jaune_debut", "v_etiq_jaune_fin", "x_boitier_gris_debut", "x_boitier_gris_fin", "v_boitier_gris_debut", "v_boitier_gris_fin"]),
              ("Télécommande", ["tc_largeur", "tc_longueur", "tc_epaisseur", "tc_connecteur_largeur", "tc_connecteur_longueur", "r_cordon"]),
              ("Accastillage", ["x_loquet1", "x_loquet2", "loquet_largeur", "loquet_hauteur", "poignee_largeur", "poignee_hauteur"])]
    for groupe, cles in utiles:
        for k in cles:
            v = c[k]
            unite = meta[k].get("unite", "m")
            val = ("%.3g" % v).replace(".", ",") if unite != "m" else str(mm(v))
            lignes.append([groupe, k, val, "mm" if unite == "m" else unite, meta[k].get("etiquette", ""), regle(k), meta[k].get("source", "")[:160]])
    # cotes de l'Équipe A, mises à la même longueur, pour comparaison
    for k, nom in (("P", "profondeur"), ("H_corps", "hauteur du corps"), ("e_couv", "profondeur de coque du couvercle"), ("H_ferme", "hauteur fermée"),
                   ("D_log", "diamètre des logements"), ("entraxe_log", "entraxe des logements"), ("tele_l", "télécommande, largeur"), ("tele_h", "télécommande, hauteur")):
        lignes.append(["Comparaison — Équipe A (photos), à la même longueur", k + " : " + nom, str(mm(A[k]["valeur"] * kA)), "mm", "DÉD (confiance faible)",
                       "proportionnel à L", "02_reconstruction/dimensions.json"])
    ecrire_csv(GUIDE / "replique_cotes.csv", ["groupe", "cote", "valeur", "unite", "statut", "regle_de_proportion", "source"], lignes)
    journal.append("Enveloppe (modèle E) : L %d × P %d × H corps %d + couvercle %d = hauteur fermée %d mm"
                   % (mm(L), mm(P), mm(Hc), mm(Hl), mm(Hc + Hl)))
    journal.append("Enveloppe (photos A) : P %d ; H corps %d ; couvercle %d ; hauteur fermée %d mm ; logements Ø %d, entraxe %d mm"
                   % (mm(A["P"]["valeur"] * kA), mm(A["H_corps"]["valeur"] * kA), mm(A["e_couv"]["valeur"] * kA), mm(A["H_ferme"]["valeur"] * kA),
                      mm(A["D_log"]["valeur"] * kA), mm(A["entraxe_log"]["valeur"] * kA)))
    journal.append("Logements (modèle E) : Ø %d mm, centres à x = %d mm ; y = %d mm (direction, côté avant) et %d mm (principal, côté charnière) ; entraxe %d mm"
                   % (mm(2 * c["r_logement"]), mm(c["x_logements"]), mm(c["y_logement_direction"]), mm(c["y_logement_principal"]),
                      mm(c["y_logement_principal"] - c["y_logement_direction"])))
    angle = math.degrees(math.atan(c["bande_pente"]))
    journal.append("Bandes : raies noires inclinées de %.1f° sur le grand axe ; pas %d mm et épaisseur %d mm mesurés selon la profondeur ; 4 raies par bande"
                   % (angle, mm(c["bande_periode"]), mm(c["bande_epaisseur_noire"])))

    # ------------------------------------------------------------------ 2. liste de débit (deux variantes de hauteur)
    debit = []
    variantes = {"modèle E": (P, Hc, Hl), "photos A": (A["P"]["valeur"] * kA, A["H_corps"]["valeur"] * kA, A["e_couv"]["valeur"] * kA)}
    surfaces = {}
    for nom, (p_, hc, hl) in variantes.items():
        ep = E_PANNEAU
        pieces = [
            ("Corps — fond", 1, L, p_, ep, "DOC (emprise) / HYP (le fond n'est jamais montré)"),
            ("Corps — grands côtés (avant, arrière)", 2, L, hc - ep, ep, "DOC (proportions)"),
            ("Corps — extrémités", 2, p_ - 2 * ep, hc - ep, ep, "DOC (proportions)"),
            ("Couvercle — dessus", 1, L, p_, ep, "DOC (emprise)"),
            ("Couvercle — grands côtés", 2, L, hl - ep, ep, "DÉD (profondeur de coque incertaine)"),
            ("Couvercle — extrémités", 2, p_ - 2 * ep, hl - ep, ep, "DÉD"),
            ("Platine supérieure (percée de 2 logements)", 1, L - 2 * ep, p_ - 2 * ep, E_PLATINE, "DOC (plan DOC-007)"),
            ("Rangement 9 — fond", 1, L - ep - c["x_panneau8_fin"], p_ - 2 * ep, E_PLATINE, "DOC (existence) / HYP (profondeur)"),
            ("Rangement 9 — cloison", 1, c["profondeur_rangement"], p_ - 2 * ep, E_PLATINE, "HYP"),
            ("Tasseaux 10 × 10 mm sous la platine (longueur totale)", 1, 2 * (L - 2 * ep) + 2 * (p_ - 2 * ep - 0.02), 0.010, 0.010, "inventé pour la maquette"),
            ("Télécommande — boîtier (bloc plein ou boîtier du commerce)", 1, c["tc_largeur"], c["tc_longueur"], c["tc_epaisseur"], "DOC (contour) / HYP (épaisseur)"),
        ]
        s9 = sum(q * a * b for (_n, q, a, b, t, _s) in pieces if abs(t - ep) < 1e-9)
        s3 = sum(q * a * b for (_n, q, a, b, t, _s) in pieces if abs(t - E_PLATINE) < 1e-9)
        surfaces[nom] = dict(surface_9mm_m2=s9, surface_3mm_m2=s3, masse_bois_kg=RHO_CP * (s9 * ep + s3 * E_PLATINE))
        for (n, q, a, b, t, st) in pieces:
            debit.append([nom, n, q, mm(a), mm(b), mm(t), st])
        journal.append("Débit « %s » : %.2f m² de contreplaqué de 9 mm, %.2f m² de 3 mm ; masse de bois ≈ %.1f kg (estimation)"
                       % (nom, s9, s3, surfaces[nom]["masse_bois_kg"]))
    ecrire_csv(GUIDE / "replique_debit.csv", ["variante_de_hauteur", "piece", "quantite", "longueur_mm", "largeur_mm", "epaisseur_mm", "statut"], debit)

    # ------------------------------------------------------------------ 3. gabarit SVG de la platine (1 mm = 1,5 px ; avant en bas)
    k = 1.5
    ox, oy = 70, 150
    W, H = int(L * 1000 * k) + 2 * ox, int(P * 1000 * k) + oy + 190
    X = lambda x: ox + x * 1000 * k
    Y = lambda y: oy + (P - y) * 1000 * k           # y = 0 à l'avant (en bas du dessin), charnière en haut
    S = []
    S.append(f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>')
    S.append(f'<text x="24" y="34" font-size="19" font-weight="700" fill="#0b0b0b">Réplique inerte — gabarit de la platine supérieure (L = {str(mm(L))} mm, cotes en mm)</text>')
    S.append('<text x="24" y="56" font-size="12.5" fill="#52514e">Vue de dessus, avant en bas, charnière en haut. Proportions relevées sur DOC-007 par l\'Équipe E ; échelle absolue hypothétique (confiance faible).</text>')
    S.append('<text x="24" y="74" font-size="12.5" fill="#52514e">Maquette de présentation : aucune fonction. Statut de chaque cote (documenté, déduit, supposé) : guide/replique_cotes.csv.</text>')
    rect = lambda x0, y0, x1, y1, fill, stroke="#0b0b0b", sw=1, extra="": f'<rect x="{X(x0):.1f}" y="{Y(y1):.1f}" width="{(x1 - x0) * 1000 * k:.1f}" height="{(y1 - y0) * 1000 * k:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
    S.append('<defs><pattern id="raies" width="{0:.1f}" height="{0:.1f}" patternUnits="userSpaceOnUse" patternTransform="rotate({1:.1f})"><rect width="{0:.1f}" height="{0:.1f}" fill="#f2c200"/><rect width="{0:.1f}" height="{2:.1f}" fill="#111"/></pattern></defs>'.format(
        c["bande_periode"] * 1000 * k * math.cos(math.radians(angle)), -angle, c["bande_epaisseur_noire"] * 1000 * k * math.cos(math.radians(angle))))
    S.append(rect(0, 0, L, P, "#e9e8e3", sw=2))                                         # contour extérieur du corps
    S.append(rect(e, e, L - e, P - e, "#f6f5f1"))                                       # platine
    S.append(rect(e, e, c["x_bande1_debut"], P - e, "#d9d8d2"))                          # zone tramée gauche
    S.append(f'<line x1="{X(c["x_division_gauche"]):.1f}" y1="{Y(e):.1f}" x2="{X(c["x_division_gauche"]):.1f}" y2="{Y(P - e):.1f}" stroke="#0b0b0b" stroke-width="1"/>')
    for a_, b_ in (("x_bande1_debut", "x_bande1_fin"), ("x_bande2_debut", "x_bande2_fin")):
        S.append(rect(c[a_], e, c[b_], P - e, "url(#raies)"))
    S.append(rect(c["x_cadre_debut"], c["y_cadre_avant"], c["x_cadre_fin"], c["y_cadre_arriere"], "#ffffff", sw=1.5))
    S.append(f'<line x1="{X(c["x_cadre_debut"]):.1f}" y1="{Y(c["y_cadre_separation"]):.1f}" x2="{X(c["x_cadre_fin"]):.1f}" y2="{Y(c["y_cadre_separation"]):.1f}" stroke="#0b0b0b"/>')
    for yk, lab in (("y_logement_principal", "1 · logement « MAIN »"), ("y_logement_direction", "2 · logement « STEERING »")):
        S.append(f'<circle cx="{X(c["x_logements"]):.1f}" cy="{Y(c[yk]):.1f}" r="{c["r_logement"] * 1000 * k:.1f}" fill="#111"/>')
        S.append(f'<line x1="{X(c["x_logements"]) - 8:.1f}" y1="{Y(c[yk]):.1f}" x2="{X(c["x_logements"]) + 8:.1f}" y2="{Y(c[yk]):.1f}" stroke="#fff"/><line x1="{X(c["x_logements"]):.1f}" y1="{Y(c[yk]) - 8:.1f}" x2="{X(c["x_logements"]):.1f}" y2="{Y(c[yk]) + 8:.1f}" stroke="#fff"/>')
    S.append(rect(c["x_fente_ecran"], 0.05 * P, c["x_fente_ecran"] + c["l_fente_ecran"], 0.90 * P, "#111"))            # fente de l'écran de secours (4)
    S.append(rect(c["x_zone4_fin"], e, c["x_panneau5_fin"], P - e, "#ffffff"))                                           # panneau 5
    S.append(rect(c["x_afficheur5_debut"], c["y_afficheur5_avant"], c["x_afficheur5_fin"], c["y_afficheur5_arriere"], "#c8322b"))
    S.append(f'<circle cx="{X(c["x_interrupteur5"]):.1f}" cy="{Y(c["y_interrupteur5"]):.1f}" r="{c["r_interrupteur5"] * 1000 * k:.1f}" fill="#c8322b" stroke="#0b0b0b"/>')
    S.append(rect(c["x_panneau5_fin"], e, c["x_panneau8_fin"], P - e, "#ffffff"))                                        # panneau 8
    S.append(rect(c["x_clavier_debut"], c["y_clavier_avant"], c["x_clavier_fin"], c["y_clavier_arriere"], "#f6f5f1"))
    for xk, yk in (("x_touches_col1", "y_touches_col1"), ("x_touches_col2", "y_touches_col2"), ("x_touches_col_isolee", "y_touches_col_isolee")):
        for yy in c[yk]:
            S.append(rect(c[xk] - c["l_touche"] / 2, yy - c["p_touche"] / 2, c[xk] + c["l_touche"] / 2, yy + c["p_touche"] / 2, "#111"))
    S.append(rect(c["x_marche_arret_debut"], c["y_marche_arret_avant"], c["x_marche_arret_fin"], c["y_marche_arret_arriere"], "#9aa0a8"))
    S.append(rect(c["x_panneau8_fin"], e, L - e, P - e, "#d9d8d2", extra='stroke-dasharray="5 3"'))                      # rangement 9
    # repères
    def rep(x, y, txt, dx=0, dy=0, anc="middle"):
        S.append(f'<text x="{X(x) + dx:.1f}" y="{Y(y) + dy:.1f}" font-size="11.5" fill="#0b0b0b" text-anchor="{anc}" stroke="#fcfcfb" stroke-width="3" paint-order="stroke">{escape(txt)}</text>')
    rep(c["x_logements"], c["y_logement_principal"], "1", 0, -16); rep(c["x_logements"], c["y_logement_direction"], "2", 0, -16)
    S[-2] = S[-2].replace('fill="#0b0b0b"', 'fill="#ffffff"').replace('stroke="#fcfcfb" stroke-width="3" paint-order="stroke"', "")
    S[-1] = S[-1].replace('fill="#0b0b0b"', 'fill="#ffffff"').replace('stroke="#fcfcfb" stroke-width="3" paint-order="stroke"', "")
    rep((c["x_zone4_fin"] + c["x_panneau5_fin"]) / 2, 0.55 * P, "5"); rep(c["x_fente_ecran"], 0.95 * P, "4", 0, -2)
    rep((c["x_panneau5_fin"] + c["x_clavier_debut"]) / 2, 0.62 * P, "8", -2, 0); rep((c["x_marche_arret_debut"] + c["x_marche_arret_fin"]) / 2, c["y_marche_arret_avant"], "6", 0, 16)
    rep((c["x_panneau8_fin"] + L - e) / 2, P / 2, "9")
    # cotes en abscisse (sous le dessin)
    yb = Y(0) + 22
    xs = [("0", 0), (str(mm(c["x_bande1_debut"])), c["x_bande1_debut"]), (str(mm(c["x_bande1_fin"])), c["x_bande1_fin"]), (str(mm(c["x_cadre_debut"])), c["x_cadre_debut"]),
          (str(mm(c["x_logements"])), c["x_logements"]), (str(mm(c["x_cadre_fin"])), c["x_cadre_fin"]), (str(mm(c["x_bande2_debut"])), c["x_bande2_debut"]),
          (str(mm(c["x_bande2_fin"])), c["x_bande2_fin"]), (str(mm(c["x_fente_ecran"])), c["x_fente_ecran"]), (str(mm(c["x_zone4_fin"])), c["x_zone4_fin"]),
          (str(mm(c["x_panneau5_fin"])), c["x_panneau5_fin"]), (str(mm(c["x_panneau8_fin"])), c["x_panneau8_fin"]), (str(mm(L)), L)]
    S.append(f'<line x1="{X(0):.1f}" y1="{yb}" x2="{X(L):.1f}" y2="{yb}" stroke="#52514e"/>')
    for i, (t, x) in enumerate(xs):
        S.append(f'<line x1="{X(x):.1f}" y1="{Y(0):.1f}" x2="{X(x):.1f}" y2="{yb + 5}" stroke="#52514e" stroke-width="0.7"/>')
        S.append(f'<text x="{X(x):.1f}" y="{yb + (20 if i % 2 == 0 else 34)}" font-size="11" fill="#0b0b0b" text-anchor="middle">{t}</text>')
    S.append(f'<text x="{X(L / 2):.1f}" y="{yb + 54}" font-size="11.5" fill="#52514e" text-anchor="middle">abscisses depuis l\'extrémité gauche (mm)</text>')
    # cotes en ordonnée (à gauche)
    xg = X(0) - 14
    S.append(f'<line x1="{xg}" y1="{Y(0):.1f}" x2="{xg}" y2="{Y(P):.1f}" stroke="#52514e"/>')
    for t, y in (("0", 0), (str(mm(c["y_logement_direction"])), c["y_logement_direction"]), (str(mm(c["y_cadre_separation"])), c["y_cadre_separation"]),
                 (str(mm(c["y_logement_principal"])), c["y_logement_principal"]), (str(mm(P)), P)):
        S.append(f'<line x1="{xg - 5}" y1="{Y(y):.1f}" x2="{X(0):.1f}" y2="{Y(y):.1f}" stroke="#52514e" stroke-width="0.7"/>')
        S.append(f'<text x="{xg - 9}" y="{Y(y) + 4:.1f}" font-size="11" fill="#0b0b0b" text-anchor="end">{t}</text>')
    yl = yb + 82
    leg = [f"Logements : 2 perçages Ø {mm(2 * c['r_logement'])} mm, entraxe {mm(c['y_logement_principal'] - c['y_logement_direction'])} mm (Équipe A, d'après les photos : Ø {mm(A['D_log']['valeur'] * kA)} mm, entraxe {mm(A['entraxe_log']['valeur'] * kA)} mm).",
           f"Bandes de danger : raies noires de {mm(c['bande_epaisseur_noire'])} mm tous les {mm(c['bande_periode'])} mm (mesurés selon la profondeur), inclinées de {angle:.0f}° ; les photos montrent un ruban plus étroit, à 2 ou 3 raies.".replace(".", ",", 0),
           "1 singularité principale · 2 singularité de direction · 4 écran de secours (fente) · 5 coupure d'urgence · 6 marche/arrêt · 8 commandes d'urgence (18 pastilles) · 9 rangement de la télécommande.",
           "Les intitulés sont ceux des légendes du document ; ils ne décrivent aucune fonction réelle."]
    for i, t in enumerate(leg):
        S.append(f'<text x="24" y="{yl + 17 * i}" font-size="11.5" fill="#52514e">{escape(t)}</text>')
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="DejaVu Sans, Arial, Helvetica, sans-serif">\n' + "\n".join(S) + "\n</svg>\n"
    (SCH / "replique_platine_gabarit.svg").write_text(svg, encoding="utf-8")
    journal.append("Gabarit écrit : schemas/replique_platine_gabarit.svg (%d × %d px, 1 mm = %.1f px)" % (W, H, k))
    cout = (sum(r[2] for r in REPLIQUE), sum(r[3] for r in REPLIQUE))
    ecrire_csv(GUIDE / "replique_nomenclature.csv", ["designation", "quantite", "prix_bas_EUR_estimation", "prix_haut_EUR_estimation", "statut_documentaire"], REPLIQUE)
    journal.append("Nomenclature de la réplique : %d lignes ; %d à %d € (estimation)" % (len(REPLIQUE), cout[0], cout[1]))
    (RACINE / "calculs" / "resultats" / "i11_replique.json").write_text(json.dumps(dict(L=L, cotes={k_: v for k_, v in c.items()}, surfaces=surfaces, cout_bas_EUR=cout[0], cout_haut_EUR=cout[1]), ensure_ascii=False, indent=1), encoding="utf-8")
    ecrire_txt("i11_replique.txt", journal)


if __name__ == "__main__":
    main(float(sys.argv[1].replace(",", ".")) if len(sys.argv) > 1 else 0.85)
