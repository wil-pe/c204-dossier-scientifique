#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 5. Construit 08_red_team/audit_references.csv à partir du tirage (graine 20261110),
des résumés récupérés en ligne (verif_en_ligne2/resumes*.json) et du JUGEMENT de la Red Team (table ci-dessous).
Classes : conforme / approximatif / mal employé / introuvable (résumé indisponible, ou chiffre attribué absent du résumé)."""
import csv, json, os
V = _RACINE + "/08_red_team/verif_en_ligne2"
r1 = json.load(open(f"{V}/resumes.json", encoding="utf-8")); r2 = json.load(open(f"{V}/resumes_complement.json", encoding="utf-8"))
C, A, M, I = "conforme", "approximatif", "mal employé", "introuvable"
J = {  # clé : (classe, ce que le rapport lui fait dire, constat)
 # ---- tirage, Équipe H
 "HKS23": (A, "« singularités de marée génériques » des trous noirs extrémaux (H §3.2)", "le résumé limite le résultat à Λ < 0 (effet plus faible pour Λ > 0, absent pour Λ = 0) : qualificatif AdS omis"),
 "Heavner14": (C, "fontaine primaire au césium (H §8.1)", "résumé concordant (NIST-F2)"),
 "Penington19": (C, "courbe de Page par surfaces extrémales quantiques (H §2.1)", "résumé concordant"),
 "HR15": (C, "transition trou noir → trou blanc (H §7.1)", "résumé concordant"),
 "Choi17": (C, "observation d'un cristal temporel discret (H §11)", "résumé concordant"),
 "Asenbaum17": (C, "courbure d'espace-temps à l'échelle d'une fonction d'onde (H §9.1)", "résumé concordant"),
 "Bidel18": (C, "gravimétrie marine par interférométrie atomique (H §9.1)", "résumé concordant"),
 "BLSS09": (C, "objection de linéarité au modèle de Deutsch (H §6.3)", "résumé concordant"),
 "Menoret18": (C, "gravimètre quantique transportable sous 10⁻⁹ g (H §9.1)", "résumé : stabilité < 10 nm/s² (1 µGal)"),
 "McGrew18": (C, "horloges Yb « au-delà de la limite géodésique » (H §8.1)", "contenu concordant ; le CSV porte le titre de la prépublication avec la référence de la version publiée (titre publié différent)"),
 "MMP18": (C, "trou de ver « long » qui ne conduit pas à des violations de causalité (H §4.1)", "citation exacte du résumé"),
 "GW250114spec": (C, "spectroscopie du trou noir final, accord avec Kerr à quelques dizaines de % (H §3.1)", "résumé concordant"),
 "PSSY19": (C, "trous de ver de répliques (H §2.1)", "résumé concordant"),
 "APS06": (C, "rebond remplaçant le big bang en cosmologie quantique à boucles (H §7.1)", "résumé concordant"),
 # ---- tirage, Équipe B
 "B-l125": (C, "revue des restes de trous noirs, statut spéculatif (B §4.7)", "résumé concordant"),
 "B-l100": (C, "référence de contexte (B) ; aucun chiffre attribué par B", "résumé concordant avec le sujet"),
 "B-l277": (I, "ouvrage de vulgarisation (Thorne 1994), liste seulement", "pas de résumé en ligne ; existence confirmée (notice) ; aucun contenu attribué"),
 "B-l190": (C, "trous de ver traversables plus longs que le trajet extérieur, sans machine temporelle (B §6.2)", "résumé concordant"),
 "B-l194": (C, "mesure de l'effet Casimir (B §6.2)", "résumé concordant (accord à 5 %)"),
 "B-l152": (C, "contexte (horloges optiques)", "résumé concordant"),
 "B-l71": (C, "solutions électrostatiques de Majumdar (B §3.5)", "résumé concordant"),
 "B-l139": (C, "complément (topologie et causalité)", "résumé concordant"),
 # ---- tirage, Équipe C
 "C-n76": (C, "décompte de Borda en fusion de classifieurs (C fiche F7)", "résumé concordant (« Borda count »)"),
 "C-n63": (M, "« la navigation gravimétrique réelle (Jekeli 2006) suppose une carte préalable » (C fiche F6)", "le résumé traite de la compensation IN SITU par gradiomètre embarqué, précisément sans carte ; l'article est cité à contre-emploi (C signale « contenu non relu »)"),
 "C-n35": (C, "laser le plus intense réalisé, 10²³ W/cm² (C fiche F5)", "résumé : (1,1 ± 0,2)×10²³ W/cm²"),
 "C-n29": (C, "champ de 1 200 T par compression de flux (C)", "résumé concordant"),
 "C-n15": (I, "facteur √6 de Bardeen 1970 (C fiche F3)", "aucun résumé en ligne ; C marque déjà ce contenu [N] ; résultat classique, plausible"),
 "C-n12": (C, "impossibilité de surcharger un trou noir (liste)", "résumé concordant"),
 # ---- tirage, Équipe F
 "F-l210": (A, "un trou de ~10¹² kg émet vers 10 MeV (F EXP-11, avec Hawking et Page)", "MacGibbon & Webber traitent les températures de 0,02 à 100 GeV (jets) : pertinent pour M ≲ 5×10¹¹ kg, pas pour 2–10 MeV"),
 "F-l188": (C, "gomme quantique à double fente, y compris effacement retardé (F EXP-10)", "résumé concordant"),
 "F-l199": (C, "revue des expériences à choix retardé (F EXP-10)", "résumé concordant"),
 "F-l88": (I, "effet Casimir acoustique (F EXP-05)", "pas de résumé en ligne ; titre concordant avec l'usage"),
 "F-l65": (C, "couplage gravitationnel entre masses de 90 mg (F EXP-03)", "résumé concordant"),
 "F-l67": (C, "valeurs CODATA 2022 (liste)", "résumé concordant ; les scripts de F utilisent CODATA 2018 (sans effet)"),
 # ---- références majeures, Équipe H (et autres équipes qui les partagent)
 "Page76a": (C, "P = 2,011×10⁻⁴ ħc⁶/G²M² ; 81 % ν, 17 % γ, 2 % gravitons (B, C, D, H)", "résumé : 2×10⁻⁴, 81/17/2 % ; recalcul indépendant Red Team : accord 0,02–0,4 %"),
 "Page77": (C, "charge rms 6,14 e (C) ; la charge fluctue autour de zéro (H) ; quelques e (B)", "résumé : « 6.14e for GMμ/ħc = 0 … 2.34e for ≫ 1 »"),
 "Gibbons75": (A, "« au-delà de 2 à 3 charges élémentaires la création de paires … neutralise le trou [Gibbons75] » (H §1.2)", "le résumé distingue deux régimes de part et d'autre de 10¹⁷ g et ne donne aucun seuil en nombre de charges : le « 2 à 3 e » est un calcul de H"),
 "MW90": (A, "« 3,9–5,0×10¹² kg, kT ≈ 2–3 MeV [Page76a], [MW90] » (H §13)", "référence sur les jets à T = 0,02–100 GeV ; ne porte pas le chiffre à 2–3 MeV (c'est Page 1976-1977)"),
 "MCP08": (C, "les particules émises ne forment pas de photosphère (H §1.1)", "résumé concordant"),
 "Carter68": (C, "CTC dans la région r < 0 de Kerr ; géodésiques atteignant l'anneau confinées à l'équateur (B, H)", "résumé concordant ; il ajoute que SANS horizon la violation de causalité est totale (cas non couvert par l'annexe D4 de B)"),
 "Tipler74": (C, "le cylindre infini engendre des CTC par tout événement (B, D, H)", "résumé concordant"),
 "Tipler77": (A, "CTC créées dans une région finie avec conditions d'énergie ⇒ singularités (H §3.3 ; B §3.4)", "le résumé parle de changement de topologie et de théorèmes de singularité ; l'énoncé précis est celui de Tipler 1976 (PRL 37, 879), que B cite aussi"),
 "Hawking92": (C, "horizon de Cauchy compactement engendré ⇒ violation de la condition d'énergie faible moyennée (B, H)", "résumé concordant ; attention : « sans singularité de courbure » et « surface initiale non compacte » (le résumé exécutif de H omet ces conditions)"),
 "NH09": (C, "pas d'équilibre stationnaire de deux trous noirs alignés (B, H)", "résumé concordant"),
 "DL17": (A, "« Théorème : … prolongement génériquement singulier » ; « la région derrière l'anneau n'est pas attendue dans un trou noir réel » (H §0, §3.2, §3.5)", "le théorème est la STABILITÉ C⁰ de l'horizon de Cauchy (prolongement continu possible : la censure cosmique forte C⁰ serait fausse) ; le caractère singulier est « suggéré par la preuve ». Conclusion de H plus forte que la source ; B la formule correctement"),
 "Zilberman22": (C, "flux quantiques génériquement divergents sur l'horizon interne de Kerr (H)", "résumé concordant"),
 "GJW17": (C, "trou de ver traversable qui « ne peut pas servir à violer la causalité » (H, B)", "citation exacte du résumé"),
 "FR96": (C, "les inégalités quantiques contraignent sévèrement les trous de ver (B, H)", "résumé concordant"),
 "PF97": (C, "paroi de quelques centaines de longueurs de Planck ; énergie inaccessible (B, D, H)", "résumé concordant ; le chiffre −6,2×10⁶² kg utilisé par D n'est pas dans le résumé"),
 "OE05": (C, "réfutation de Mallett : singularité sur l'axe, CTC au-delà de l'univers visible (B, H)", "résumé concordant"),
 "Polchinski91": (C, "mécanique quantique non linéaire ⇒ communication EPR ou entre branches (B, H, G)", "résumé concordant"),
 "Deutsch91": (C, "modèle de CTC quantiques, lecture « mondes multiples » (B, H)", "résumé concordant"),
 "Everett04": (C, "lecture « mondes multiples » viable seulement si les objets macroscopiques sont fragmentés (B, H)", "résumé concordant"),
 "Ori05": (C, "modèle à cœur de vide respectant les conditions d'énergie ; stabilité ouverte (B, H)", "résumé concordant"),
 "Bothwell22": (C, "décalage gravitationnel résolu sur 1 mm ; 7,6×10⁻²¹ (B, F, H)", "résumé concordant"),
 "Prezens10": (C, "unique occurrence de « Tipler sinusoid » (H §3.4)", "recherche en texte intégral refaite sur INSPIRE : 1 résultat (arXiv:1008.3244) ; 0 pour « off-set Tipler » et « negative time event horizon ». Contenu détaillé du texte non relu par la Red Team"),
 "KRW97": (C, "pas d'état de Hadamard aux points de base d'un horizon compactement engendré (B, H)", "résumé concordant"),
 "PBH2505": (C, "taux d'explosion local < 181 pc⁻³ an⁻¹ (H)", "résumé concordant (99 % de confiance)"),
 "CMS26": (C, "exclusion jusqu'à 8,4–11,4 TeV, 138 fb⁻¹ (H)", "résumé concordant"),
 "GW250114LVK": (C, "S/B 80 ; 33,6 et 32,2 M☉ ; fréquences à ±30 % de Kerr ; loi des aires (H)", "résumé concordant"),
 "Lu26": (C, "1,2 et 1,3×10⁻¹⁹ ; accord (−0,1 ± 5,7 ± 1,0)×10⁻¹⁹ (H)", "résumé concordant"),
 "QCTRL26": (C, "navigation gravimétrique quantique sans GNSS sur 83 km, ~300 m (H)", "résumé concordant (prépublication d'entreprise, signalée comme telle)"),
 "Kugel24": (A, "« ni fabricable (4×10²⁹ J, [Kugel24]) » (H §15)", "l'article exclut la formation d'un horizon PAR CONCENTRATION DE LUMIÈRE ; il ne traite pas la fabrication en général (emploi correct au §1.1)"),
 "SW17": (C, "impossibilité de sur-charger ou sur-tourner un trou de Kerr-Newman (H)", "résumé concordant"),
 "Olum98": (C, "le transport supraluminique exige de l'énergie négative (H)", "résumé concordant"),
 "SSV22": (C, "toute métrique de distorsion raisonnable viole les conditions d'énergie (B, H)", "résumé concordant"),
 "CW09": (C, "trou noir artificiel comme source d'énergie « à la limite du possible » (H)", "résumé concordant"),
 "Westphal21": (C, "gravité de deux sphères d'or de 90 mg (B, H)", "résumé concordant"),
 "Bollinger89": (C, "non-linéarité bornée à 4×10⁻²⁷ (B, H)", "résumé concordant (fraction de l'énergie de liaison par nucléon)"),
 "GPB11": (C, "−37,2 ± 7,2 mas/an contre −39,2 prédits (B, D, H)", "résumé concordant"),
}
J2 = {  # complément : références majeures de B, C, D, F
 "Hahn2019": (C, "record de champ continu 45,5 T (B, C)", "résumé concordant (14,4 T dans 31,1 T)"),
 "LeahyUnruh1979": (A, "« anisotropie modérée pour Kerr (Leahy & Unruh 1979), jamais un cône » (B §4.2)", "l'article ne traite que l'asymétrie d'émission des NEUTRINOS ; « modérée » et « jamais un cône » sont des extrapolations de B"),
 "PressTeukolsky1972": (I, "gain de superradiance scalaire ~0,3 % (B §4.6)", "pas de résumé en ligne ; valeur non vérifiée"),
 "TeukolskyPress1974": (C, "gains maximaux 4,4 % (EM) et 138 % (gravitationnel) (B §4.6)", "résumé concordant"),
 "ChambersHiscockTaylor1997": (M, "« un trou en rotation rapide perd son moment cinétique plus vite que sa masse (… Chambers, Hiscock & Taylor 1997) » (B §4.6)", "l'article montre au contraire qu'avec des champs scalaires l'évolution tend vers a/M ≈ 0,555 non nul ; H l'emploie correctement comme exception ; la bonne référence est Page 1976 II"),
 "Andreasson2008": (C, "2GM/(Rc²) ≤ 8/9 si p_r + 2p_t ≤ ρc² (B annexe D5)", "résumé concordant (cas Ω = 1)"),
 "Aeppli2024": (C, "horloge à réseau Sr à 8,1×10⁻¹⁹ (B, H)", "résumé concordant"),
 "Peters1964": (C, "puissance rayonnée et temps de coalescence (B, D)", "résumé concordant ; formules recalculées"),
 "PoissonIsrael1990": (C, "inflation de masse à l'horizon de Cauchy (B, G, H)", "résumé concordant"),
 "Carr2010": (I, "f(M→0) = 15,35 ; τ(10⁷ kg) = 407 s ; M* = 5,1×10¹⁴ g, repères de validation de D (S01)", "ces chiffres ne figurent pas dans le résumé (corps de l'article non consulté) ; D les signale « de mémoire »"),
 "MacGibbon1991": (I, "coefficient 5,34×10²⁵ g³/s et paramétrisation f(M) (D, G, H)", "absents du résumé (qui donne M* ≈ 4–6×10¹⁴ g) ; recoupés à 1,3 % par les coefficients de Page recalculés"),
 "Middlemiss2016": (I, "gravimètre MEMS à 40 µGal/√Hz (C fiche F6)", "pas de résumé en ligne ; notice concordante"),
 "Torres2017": (C, "superradiance d'un vortex : 14 ± 8 % (F, H)", "valeur de la version publiée ; le résumé de la prépublication indique 20 % (F signale ne pas avoir relu l'article)"),
 "LyonsVanderkulk1962": (C, "redondance modulaire triple à vote 2 sur 3 (C, F, H)", "résumé concordant"),
 "MudawarBowers1999": (I, "flux critique record de 276 MW/m² (C)", "pas de résumé en ligne ; C marque cette valeur [E] (vue dans un extrait)"),
 "Unruh1976": (C, "section efficace de Dirac = 1/8 de celle du scalaire (C)", "résumé concordant"),
 "Page1976b": (C, "le moment cinétique est émis plusieurs fois plus vite que l'énergie (B, C, H)", "citation quasi littérale du résumé"),
 "FordRoman1995": (C, "inégalité quantique à échantillonnage lorentzien (B §6.2)", "le résumé décrit le cadre ; la borne 4D est confirmée par le résumé de Ford & Roman 1996 (« recently derived »)"),
 "Gott1991": (C, "CTC si γ sin(4πGμ/c²) > 1 (B, H)", "résumé concordant"),
}
rows = []
for k, v in r1.items():
    if k not in J: raise SystemExit("jugement manquant : " + k)
    cl, usage, constat = J[k]
    rows.append([k, v["equipe"], "tirage (graine 20261110)" if not v.get("majeure") else "conclusion majeure", v["ref"][:220].strip("| "), v["doi"], v["arxiv"], v["source"], len(v["resume"]), usage, cl, constat])
for k, v in r2.items():
    if k.startswith("recherche") or k == "Yao2017_hors": continue
    cl, usage, constat = J2[k]
    rows.append([k, v["equipe"], "conclusion majeure (complément B, C, D, F)", v["titre"][:220], v["doi"], "", v["source"], len(v["resume"]), usage, cl, constat])
out = _RACINE + "/08_red_team/audit_references.csv"
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["cle", "equipe", "mode_de_selection", "reference", "doi", "arxiv", "source_du_resume", "longueur_resume_car", "ce_que_le_rapport_lui_fait_dire", "classe", "constat"])
    w.writerows(rows)
from collections import Counter
print(len(rows), "usages audités ;", Counter(r[9] for r in rows))
print("tirage :", Counter(r[9] for r in rows if r[2].startswith("tirage")))
print("majeures :", Counter(r[9] for r in rows if not r[2].startswith("tirage")))
print("références distinctes (DOI/arXiv) :", len({(r[4].lower() or r[5]) for r in rows}))
