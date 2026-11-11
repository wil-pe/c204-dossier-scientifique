#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G — 06_mesures_graphiques.py : deux mesures géométriques simples sur les documents.

(1) Proportions du couvercle : rapport R = (écart entre les centres des deux bandes de danger) /
    (écart entre le centre de la bande droite et le centre du panneau de texte « instructions »).
    - photos JT2, JT3 : centres des bandes détectés automatiquement (02_analyse_images.py, seuillage HSV du jaune) ;
      centre du panneau de texte relevé À LA MAIN sur les agrandissements x4 (incertitude ±4 à ±5 px d'origine) ;
    - DOC-007 : relevés À LA MAIN sur l'agrandissement x4 (incertitude ±10 px à l'échelle x4).
    R est un rapport de longueurs adjacentes sur une même droite : peu sensible à l'échelle, modérément à la perspective.
(2) Ouverture du « cône d'évacuation des rayons X » de DOC-009 (deux segments en tirets issus du centre), et fraction
    d'angle solide correspondante.
Incertitudes par tirage Monte-Carlo sur les relevés manuels. Résultats INDICATIFS (copies basse résolution).
"""
import json, math, numpy as np
rng = np.random.default_rng(1)
J = json.load(open(_RACINE + "/08_red_team/calculs/resultats_images.json", encoding="utf-8"))

def R_mc(s1, s2, p, sig_s, sig_p, n=20000):
    a = rng.normal(s1, sig_s, n); b = rng.normal(s2, sig_s, n); c_ = rng.normal(p, sig_p, n)
    r = (b - a)/(c_ - b); return float(np.median(r)), float(np.percentile(r, 16)), float(np.percentile(r, 84))

print("(1) Rapport R = (bande1→bande2) / (bande2→panneau de texte)")
mes = {}
for key, panneau, sp in (("MT7011__JT2.jpeg", 183.5, 4.0), ("MT7012__JT3.jpg", 384.0, 5.0)):
    seg = J[key]["bandes_jaunes_x"]; s1, s2 = seg[0][2], seg[1][2]
    m, lo, hi = R_mc(s1, s2, panneau, 1.5, sp); mes[key] = (m, lo, hi)
    print(f"   {key:22s}: bandes à x = {s1:.1f} et {s2:.1f} px, panneau à {panneau:.1f} px -> R = {m:.2f} [{lo:.2f} ; {hi:.2f}]")
# DOC-007, coordonnées x4 relevées à la main : bord du couvercle 195..1620 ; bandes 390..530 et 960..1095 ; panneau 1210..1430
s1, s2, p = (390+530)/2, (960+1095)/2, (1210+1430)/2
m, lo, hi = R_mc(s1, s2, p, 10, 10); mes["DOC-007"] = (m, lo, hi)
print(f"   DOC-007 (vue de dessus): bandes à {s1:.0f} et {s2:.0f}, panneau à {p:.0f} (px x4) -> R = {m:.2f} [{lo:.2f} ; {hi:.2f}]")
print(f"   positions relatives sur DOC-007 : bande 1 à {(s1-195)/1425:.2f} L, bande 2 à {(s2-195)/1425:.2f} L, panneau à {(p-195)/1425:.2f} L ; "
      f"logements des singularités à {(740-195)/1425:.2f} L")
print(f"   écart DOC-007 / photos : x{mes['DOC-007'][0]/np.mean([mes['MT7011__JT2.jpeg'][0], mes['MT7012__JT3.jpg'][0]]):.2f}")
print("   Effet de perspective maximal plausible : les largeurs apparentes des deux bandes diffèrent de "
      f"{abs(1-(seg[1][1]-seg[1][0])/(seg[0][1]-seg[0][0]))*100:.0f} % sur JT3, donc la perspective ne peut pas expliquer un facteur ~1,5.")

print("\n(2) Cône d'évacuation de DOC-009 (coordonnées en px d'origine, lues sur les agrandissements)")
apex = (141.0, 149.0); haut = (36.0, 60.0); bas = (17.5, 245.0)
a_h = math.degrees(math.atan2(apex[1]-haut[1], apex[0]-haut[0])); a_b = math.degrees(math.atan2(bas[1]-apex[1], apex[0]-bas[0]))
demi = (a_h + a_b)/2
print(f"   demi-angle supérieur {a_h:.1f}°, inférieur {a_b:.1f}° -> ouverture totale {a_h+a_b:.0f}° (±6°), demi-angle moyen {demi:.0f}°")
frac = (1-math.cos(math.radians(demi)))/2
print(f"   fraction d'angle solide d'un cône de demi-angle {demi:.0f}° : {100*frac:.0f} % de 4π "
      f"-> {100*(1-frac):.0f} % d'une émission isotrope partirait hors du cône")
json.dump(dict(R=mes, cone_demi_angle_deg=demi, cone_fraction_4pi=frac),
          open(_RACINE + "/08_red_team/calculs/resultats_mesures_graphiques.json", "w"), indent=1)
