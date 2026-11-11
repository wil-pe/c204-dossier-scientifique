#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 2. Construit 08_red_team/coherence_inter_equipes.csv.
Chaque ligne : grandeur ; équipe ; valeur de l'équipe ; fichier et numéro de ligne (retrouvé par expression régulière,
pour éviter toute erreur de report) ; recalcul Red Team (04_recalcul_grandeurs.py) ; valeur retenue ; commentaire."""
import csv, json, os, re
R = _RACINE + ""
ICI = os.path.dirname(os.path.abspath(__file__))
F = {"base": "00_DOSSIER_DE_BASE.md", "A": "02_reconstruction/DOSSIER_TECHNIQUE.md", "B": "03_physique_theorique/RAPPORT_B.md",
     "C": "04_ingenierie/RAPPORT_C.md", "CF1": "04_ingenierie/fiches/F1_singularites_logement_magnetique.md", "CF4": "04_ingenierie/fiches/F4_refroidissement_rayonnement.md",
     "CF5": "04_ingenierie/fiches/F5_alimentation_bilan_energetique.md", "CF6": "04_ingenierie/fiches/F6_capteurs_gravite_horloges.md",
     "D": "05_simulations/RAPPORT_D.md", "DS5": "05_simulations/S05_champ_faible_c204/README.md", "DS6": "05_simulations/S06_confinement_em/README.md",
     "DS7": "05_simulations/S07_energie_negative/README.md", "E": "06_modele_3D/RAPPORT_E.md", "F": "07_experiences/RAPPORT_F.md",
     "F11": "07_experiences/fiches/EXP-11_rayonnement_bruit_de_fond.md", "F12": "07_experiences/fiches/EXP-12_banc_d_essai_C204_de_substitution.md",
     "F03": "07_experiences/fiches/EXP-03_cavendish_test_nul_electromagnetique.md", "F05": "07_experiences/fiches/EXP-05_effet_casimir.md",
     "G": "08_red_team/RAPPORT_RED_TEAM_1.md", "H": "09_recherche_contemporaine/RAPPORT_H.md"}
TXT = {k: open(os.path.join(R, v), encoding="utf-8").read().splitlines() for k, v in F.items()}
def lig(k, motif):
    for i, l in enumerate(TXT[k], 1):
        if re.search(motif, l):
            return f"{F[k]}:{i}"
    raise SystemExit(f"motif introuvable : {k} / {motif}")
L = []
def g(grandeur, recalcul, retenu, lignes):
    for (eq, val, k, motif, com) in lignes:
        L.append([grandeur, eq, val, lig(k, motif), recalcul, retenu, com])

g("Masse d'une singularité pour 300–500 MW (Hawking)", "3,92–5,06×10¹² kg (toutes espèces, e± compris) ; 0,84–1,09×10¹² kg (photons, corps noir) ; 4,9–6,3×10¹² kg si neutrinos de Dirac",
  "3,9–5,1×10¹² kg par singularité (kT = 2,1–2,7 MeV ; r_s = 5,8–7,5 fm) ; +24 % si neutrinos de Dirac", [
  ("base §6", "0,84–1,1×10¹² kg (photons seuls)", "base", r"P = 300–500 MW ⇔", "formule photons, corps noir : sous-estime la puissance d'un facteur 21,6 ; corrigé par l'errata E2"),
  ("base errata E2", "3,9–5,1×10¹² kg", "base", r"\| E2 \|", "conforme"),
  ("B", "3,9–5,1×10¹² kg", "B", r"totale de 300–500 MW correspond", "conforme (corps gris recalculés, accord 0,02 % avec notre recalcul indépendant)"),
  ("C", "3,9–5,1×10¹² kg", "C", r"Masse pour 300–500 MW au total", "conforme"),
  ("D", "3,9–5,0×10¹² kg (toutes espèces) ; 8,4×10¹¹–1,1×10¹² (photons)", "D", r"Idem en comptant toutes les espèces", "conforme (paramétrisation f(M) de mémoire ; 2 % sous B et C)"),
  ("F", "10¹¹–10¹² kg, « voire 4–5×10¹² kg »", "F", r"trou noir rayonnant 300–500 MW \(10¹¹–10¹² kg", "À CORRIGER : valeur obsolète conservée dans le résumé, le §2.1, le §4 et EXP-12 (« 10¹¹ kg »)"),
  ("F (EXP-12)", "10¹¹ kg", "F12", r"Masse de l'appareil \| 0,1 kg \| 10¹¹ kg", "À CORRIGER : 7,8×10¹²–1,0×10¹³ kg pour les deux singularités"),
  ("G (rapport 1)", "0,84–1,09×10¹² kg (photons) ou 3,9–5,1×10¹² kg (Page)", "G", r"0,84–1,09×10¹² kg chacune", "conforme"),
  ("H", "5,0–3,9×10¹² kg", "H", r"Masse pour 300–500 MW \|", "conforme (coefficient cité de mémoire, recoupé)")])

g("Masse (totale) donnant 1,5–2 g à 1–3 m", "2,20×10¹¹ kg (1,5 g, 1 m) ; 2,94×10¹¹ kg (2 g, 1 m) ; 1,98–2,64×10¹² kg (3 m) ; 4,02×10¹² kg (2 g, 3,7 m)",
  "2,2×10¹¹ à 2,6×10¹² kg AU TOTAL (les deux singularités ensemble) ; 4,0×10¹² kg à 3,7 m", [
  ("base §6", "2,9×10¹¹ kg (1 m) ; 2,6×10¹² kg (3 m)", "base", r"2 g à la distance r", "conforme"),
  ("B", "2,2×10¹¹–4,0×10¹² kg (1–3,7 m)", "B", r"« 1,5–2 g » à 1–3,7 m", "conforme"),
  ("C", "2,94×10¹¹ kg (2 g, 1 m)", "C", r"\| Masse pour 2 g à 1 m \|", "conforme ; mais voir « énergie de fabrication » (C double cette masse)"),
  ("D", "2,2×10¹¹–2,6×10¹² kg", "D", r"Masse donnant 1,5–2 g entre 1 et 3 m", "conforme"),
  ("G (rapport 1)", "2,94×10¹¹ kg (les deux ensemble)", "G", r"2 g à 1 m ⇒ M = 2g r²/G", "conforme"),
  ("H", "(indirect) 26–34 g₀ à 1 m d'une singularité de 3,9–5,0×10¹² kg", "H", r"Pesanteur d'une singularité à 1 m", "conforme (26,5–34,7 g₀)")])

g("Cohérence interne « 300–500 MW » ↔ « 1,5–2 g »", "une singularité de 3,9–5,1×10¹² kg donne 26,5–34,7 g à 1 m, 6,6–8,7 g à 2 m, 2 g à 3,6–4,2 m ; deux singularités : 53–69 g à 1 m, 2 g à 5,2–5,9 m",
  "cohérence à UN ORDRE DE GRANDEUR près seulement (errata E1) ; vraie uniquement pour une seule singularité et un occupant à ≥ 3,7 m", [
  ("base errata E1", "cohérents à un ordre de grandeur près ; 14 à 60 g à 1 m", "base", r"\| E1 \|", "conforme"),
  ("B", "« confirmé et renforcé » ; masse cohérente ~4×10¹² kg avec « 2 g à 3–3,7 m »", "B", r"\*\*confirmé et renforcé\*\*", "À NUANCER : suppose UNE singularité et le bord du champ (3,7 m) ; contredit l'errata E1 et les rapports C, D, G, H"),
  ("C", "27–34 g à 1 m ; accord à un ou deux ordres de grandeur près", "C", r"masses de 300–500 MW donnent 27–34 g à 1 m", "conforme"),
  ("D", "accord seulement en lecture « photons, corps noir » ; se défait (facteur 1,5 à 20) sinon", "D", r"cet accord se défait", "conforme"),
  ("G (rapport 1)", "60 g à 1 m pour deux trous de 4,4×10¹² kg", "G", r"deux de 4,4×10¹² kg donnent \*\*60 g\*\*", "conforme (59,9 g)"),
  ("H", "26–34 g par singularité à 1 m : « incohérent »", "H", r"\| 18 \| 1,5 à 2 g ressentis", "conforme")])

g("Durée de vie d'un trou noir de 100 kg", "3,97×10⁻¹³ s (Modèle standard complet, 4 scalaires) ; 4,14×10⁻¹³ s (décompte de B) ; 3,9×10⁻¹² s avec le facteur 21 des grandes masses ; 8,4×10⁻¹¹ s en corps noir photons",
  "≈ 4×10⁻¹³ s (B, C, D) ; la valeur 4×10⁻¹² s de G est erronée (errata E3 confirmé)", [
  ("base §6", "~10⁻¹⁰ s", "base", r"M = 100 kg : ~10⁻¹⁰ s", "photons seuls : facteur ≈ 210 trop long ; corrigé par E3"),
  ("B", "4,1×10⁻¹³ s", "B", r"\| Durée de vie, 100 kg \|", "conforme"),
  ("C", "4,0×10⁻¹³ s", "C", r"\| Durée de vie d'un trou noir de 100 kg \|", "conforme"),
  ("G (rapport 1), §5 D3", "4×10⁻¹² s", "G", r"Idem 100 kg : 4×10⁻¹² s", "ERRONÉ : applique à 100 kg le facteur 21 valable vers 10¹² kg"),
  ("G (rapport 1), F1", "8×10⁻¹¹ s", "G", r"un trou noir de 100 kg vit 8×10⁻¹¹ s", "ERRONÉ et contradictoire avec le §5 du même rapport (formule photons seuls)")])

g("Durée de vie à 113 kg et 227 kg", "113,5 kg : 5,8–6,0×10⁻¹³ s ; 227 kg : 4,6–4,8×10⁻¹² s", "6×10⁻¹³ s (113,5 kg) ; 4,7×10⁻¹² s (227 kg), à ±4 % selon le décompte des degrés de liberté", [
  ("B", "6,0×10⁻¹³ s (113,5 kg) ; 4,8×10⁻¹² s (227 kg)", "B", r"\| 113,5 kg \| 1,7 × 10⁻²⁵ m", "conforme"),
  ("D", "5,9×10⁻¹³ s (113 kg)", "D", r"Trou noir de 113 kg : durée de vie", "conforme"),
  ("H", "~10⁻¹² s (227 kg)", "H", r"un trou de 227 kg s'évaporerait en ~10⁻¹² s", "approximatif : 4,7×10⁻¹² s (arrondi à la décade inférieure)")])

g("Durée de vie d'un trou noir de 10¹² kg", "1,24×10¹¹ ans (α constant, régime e±) ; 2,7×10¹² ans en corps noir photons", "≈ 1,1–1,2×10¹¹ ans", [
  ("base §6", "~3×10¹² ans", "base", r"M = 10¹² kg : ~3×10¹² ans", "photons seuls ; corrigé par E3"),
  ("B", "1,2×10¹¹ ans", "B", r"\| 10¹² kg \| 1,5 × 10⁻¹⁵ m \| 10,6 MeV", "conforme"),
  ("C", "1,2×10¹¹ ans", "C", r"10¹² kg → \*\*1,2×10¹¹ ans\*\*", "conforme"),
  ("D", "1,1×10¹¹ ans", "D", r"1,1×10¹¹ ans pour 10¹² kg", "conforme (f(M) variable)"),
  ("G (rapport 1)", "~1,2×10¹¹ ans", "G", r"avec l'émission complète ~1,2×10¹¹ ans", "conforme"),
  ("H", "~10¹³ ans à 4–5×10¹² kg", "H", r"durée de vie ~10¹³ ans", "conforme (7,9×10¹²–1,5×10¹³ ans)")])

g("Température et énergie des photons (300–500 MW)", "kT = 2,09–2,70 MeV ; pic de puissance des photons à 6,04 kT = 12,6–16,3 MeV ; trou « à rayons X » (kT = 10 keV) : 1,06×10¹⁵ kg, 4,4 kW",
  "kT = 2,1–2,7 MeV ; photons de 12–16 MeV (gamma, pas X)", [
  ("base §5.4", "~10¹¹ K, dizaines de MeV", "base", r"rayonne vers ~10¹¹ K", "valable pour 10¹² kg ; pour 4–5×10¹² kg : 2,4–3,1×10¹⁰ K (errata)"),
  ("B", "kT = 2,1–2,7 MeV ; pic des photons 13–16 MeV", "B", r"puissance totale ⇒ M = 5,1–3,9", "conforme"),
  ("C", "kT = 2,1–2,7 MeV ; γ de 5 à 70 MeV, médiane 15 MeV", "C", r"7,5 % de gamma de 5 à 70 MeV", "conforme"),
  ("D", "kT = 10,6 MeV à 10¹² kg", "D", r"k_BT = 10,6 MeV \(γ, e±, ν", "conforme (autre masse)"),
  ("G (rapport 1)", "kT ≈ 2–13 MeV selon le modèle", "G", r"kT ≈ 2–13 MeV", "conforme"),
  ("H", "kT = 2,1–2,7 MeV ; pic 12–16 MeV", "H", r"Pic d'émission photonique", "conforme")])

g("Répartition de la puissance (neutrinos / e± / photons / gravitons)", "54,97 % / 36,64 % / 7,53 % / 0,86 % (3 saveurs de neutrinos à 2 états, e± sans masse)", "55 % / 37 % / 7,5 % / 0,9 %", [
  ("B", "55 % / 37 % / 7,5 % / 0,9 %", "B", r"neutrinos 55 %, e± 37 %, photons 7,5 %", "conforme"),
  ("C", "55 % / 37 % / 7,5 % / 0,9 %", "C", r"α = 4,47×10⁻⁴ \(ν 55 %", "conforme"),
  ("D", "photons ≈ 7 %", "D", r"les photons ne portent qu'environ 7 %", "conforme"),
  ("G (rapport 1)", "30 / 146 / 221 MW sur 400 MW", "G", r"30 MW de photons, 146 MW d'e±, 221 MW de neutrinos", "conforme (7,5 / 36,5 / 55 %)"),
  ("H", "ν ≈ 55 % ; e± ≈ 36 % ; γ ≈ 8 % ; gravitons ≈ 1 %", "H", r"Répartition de la puissance", "conforme (arrondis)")])

g("Charge maximale tenable par un micro-trou noir", "fluctuation thermique simple : 1/√(4πα) = 3,3 e ; Page 1977 (résumé vérifié en ligne) : 6,14 e rms pour GMμ/ħc → 0 ; instabilité du vide d'une charge ponctuelle : ~1/α = 137 e ; critère de H à 4,5×10¹² kg : 2,4 e (0,5 e à 10¹² kg)",
  "charge TYPIQUE ≈ 6 e rms (Page 1977) ; borne SUPÉRIEURE d'ordre de grandeur ≈ 137 e ; le « 2–3 e » de H n'est ni l'un ni l'autre", [
  ("B", "≤ ~137 e (2,2×10⁻¹⁷ C) ; « quelques e » en équilibre", "B", r"ne retient pas plus de ~e/α ≈ 137", "borne supérieure correcte (ordre de grandeur) ; à présenter comme telle"),
  ("C", "~6 e (6,14 e rms, Page 1977)", "C", r"charge réelle ~6 e", "conforme à la source (résumé relu : 6,14 e)"),
  ("C (fiche F1)", "3,3 e (estimation propre) ; 6,14 e retenu", "CF1", r"Z_rms ≈ 3,3 e", "conforme"),
  ("D", "~137 e (ordre de grandeur)", "D", r"Charge réellement soutenable par un micro-trou noir", "borne supérieure ; libellé « réellement soutenable » trop fort"),
  ("G (rapport 1)", "≲ 170 e", "G", r"est ≲ 170 e", "même ordre que B et D (critère Z ≈ 170 des noyaux étendus)"),
  ("H", "≈ 2 charges (2 à 3)", "H", r"Charge maximale durable", "À REFORMULER : critère énergétique e·Q/(4πε₀r_s) < m_e c², dépendant de M et inadapté quand r_s ≪ ħ/m_e c ; attribué à tort à Gibbons 1975")])

g("Champ électrique de sustentation", "charge extrémale : 1,138×10¹¹ V/m (indépendant de M) ; 137 e : 4,5×10²⁹ V/m (10¹² kg), 1,8×10³⁰ V/m (4×10¹² kg) ; 6,14 e : 4,4×10³¹ V/m (4,4×10¹² kg)",
  "1,14×10¹¹ V/m (cas extrémal, irréaliste) ; 4×10²⁹–4×10³¹ V/m avec une charge tenable, soit 10¹¹–10¹³ fois le champ de Schwinger", [
  ("B", "2×10³⁰ V/m (4×10¹² kg, 137 e)", "B", r"le champ électrique de sustentation vaut", "conforme"),
  ("C", "1,14×10¹¹ V/m ; 10²¹ à 4×10³¹ V/m (6 e)", "C", r"\| Champ électrique de sustentation \(charge maximale\)", "conforme"),
  ("D", "1,1×10¹¹ V/m ; 4×10²⁹ V/m (10¹² kg, 137 e)", "D", r"Champ de lévitation et piège de Penning", "conforme"),
  ("F", "≥ 1,1×10¹¹ V/m", "F", r"champ de sustentation ≥ 1,1 × 10¹¹ V/m", "conforme (cas favorable)"),
  ("G (rapport 1)", "3,6×10²⁹ V/m (170 e) ; 1,1×10¹¹ V/m (extrémal)", "G", r"champ électrique de lévitation \*\*3,6×10²⁹ V/m\*\*", "conforme")])

g("Champ magnétique de piège de Penning (charge extrémale)", "B_min = √(2g/d)/(Q/M) : 5,14×10¹¹ T (d = 1 cm) ; 7,27×10¹¹ T (d = 5 mm)", "5–7×10¹¹ T selon l'excursion tolérée (les deux valeurs sont correctes)", [
  ("C", "5,1×10¹¹ T (excursion 1 cm)", "C", r"\| Champ magnétique de piège de Penning", "conforme"),
  ("D", "7×10¹¹ T (affaissement 10 % de 5 cm)", "D", r"Champ de lévitation et piège de Penning", "conforme (hypothèse d'excursion différente)")])

g("Débit de dose sans blindage", "γ primaires seuls, une singularité de 400 MW : 3,45×10³ Gy/s à 1 m, 3,8×10² Gy/s à 3 m (μ_en/ρ eau, 15 MeV) ; lecture littérale « 400 MW de rayons X de 100 keV » : 8,1×10⁴ Gy/s à 1 m, 9,0×10³ Gy/s à 3 m ; e± non arrêtés : ~2×10⁵ Gy/s à 1 m",
  "référence physique : 3,3–3,8×10³ Gy/s à 1 m et ≈ 3,8×10² Gy/s à 3 m par singularité (γ primaires : BORNE BASSE) ; la valeur de F est une lecture littérale à étiqueter comme telle", [
  ("B", "~10³ Gy/s à 1 m (ordre de grandeur)", "B", r"débit de dose de l'ordre de 10³ Gy/s", "conforme"),
  ("C", "3 300 Gy/s à 1 m ; 370 Gy/s à 3 m (γ) ; 1,4×10⁵ Gy/s γ + e± (fiche F4)", "C", r"\*\*Doses\*\* : 3 300 Gy/s", "conforme (μ_en/ρ à 20 MeV)"),
  ("F", "9×10³ Gy/s à 3 m (400 MW entièrement en X de 100 keV)", "F", r"9 × 10³ Gy/s à 3 m ; dose létale", "calcul exact SOUS SON HYPOTHÈSE, mais 24 fois la valeur du spectre de Hawking ; à étiqueter et à compléter"),
  ("F (EXP-11)", "8,1×10⁴ / 5,0×10⁴ Gy/s à 1 m (100 keV / 10 MeV, 400 MW de photons)", "F11", r"\| 1 m \| 8,1 × 10⁴ Gy/s", "idem"),
  ("G (rapport 1)", "3,8×10³ Gy/s à 1 m (photons primaires seuls)", "G", r"photons primaires seuls : \*\*3,8×10³ Gy/s\*\*", "conforme (coefficient approximatif, +10 %)")])

g("Blindage en plomb pour un trajet à 1 mSv", "faisceau étroit à ~15 MeV : ≈ 25 longueurs d'atténuation ≈ 39 cm ; faisceau large (couche de déci-transmission ≈ 5,7 cm) : 62 cm", "40–60 cm de plomb, 6–15 t : ordre de grandeur seulement (aucun calcul de transport)", [
  ("C", "62 cm, sphère de 14 t", "C", r"62 cm de plomb \(14 t\)", "hypothèse de faisceau large, prudente"),
  ("F", "58 cm (15 t) à 10 MeV", "F", r"58 cm \(15 t\) à 10 MeV", "cohérent avec C"),
  ("G (rapport 1)", "≥ 36 cm (2 à 6 t)", "G", r"≥ 36 cm de plomb", "faisceau étroit : borne basse")])

g("Γ − 1 = GM/(rc²) à 1 m", "2,18×10⁻¹⁶ (masse donnant 2 g à 1 m) ; 7,43×10⁻¹⁶ (10¹² kg) ; 1,49×10⁻¹⁵ (2×10¹² kg) ; 2,97×10⁻¹⁵ (4×10¹² kg) ; 6,5×10⁻¹⁵ (2 × 4,4×10¹² kg) ; borne 2gL/c² = 8,07×10⁻¹⁶ (L = 3,7 m)",
  "2×10⁻¹⁶ à 7×10⁻¹⁵ selon la masse retenue : toutes les valeurs sont exactes, chacune pour sa masse ; écart au facteur revendiqué 87 660 : 19 à 20,6 ordres de grandeur", [
  ("B", "7,4×10⁻¹⁶ (10¹² kg) ; borne ≤ 8×10⁻¹⁶", "B", r"Φ/c² = 7,4 × 10⁻¹⁶, entraînement", "conforme"),
  ("C (fiche F6)", "2,2×10⁻¹⁶ (2 g sur 1 m)", "CF6", r"2 g sur 1 m correspond à 2,2×10⁻¹⁶", "conforme"),
  ("D", "1,5×10⁻¹⁵ (2 × 10¹² kg)", "D", r"Dilatation à 1 m de 2 × 10¹² kg", "conforme"),
  ("F", "7,4×10⁻¹⁶ (10¹² kg)", "F", r"\| Décalage d'horloge GM/\(rc²\)", "conforme pour 10¹² kg ; ×4 à 5 pour la masse corrigée"),
  ("G (rapport 1)", "1,5×10⁻¹⁵ (2×10¹² kg)", "G", r"GM/\(rc²\) = \*\*1,5×10⁻¹⁵\*\*", "conforme"),
  ("H", "2,2×10⁻¹⁶ (2 g à 1 m)", "H", r"Potentiel d'une masse donnant 2 g à 1 m", "conforme")])

g("Entraînement des référentiels à 1 m", "spin extrémal d'UN trou de 10¹² kg : 3,3×10⁻²² rad/s ; moment cinétique ORBITAL de la paire (d = 0,3 m) : 4,7×10⁻¹⁵ rad/s (2 × 10¹² kg), 4,3×10⁻¹⁴ rad/s (2 × 4,4×10¹² kg)",
  "≤ 5×10⁻¹⁴ rad/s (D) : le terme orbital domine de 7 à 8 ordres de grandeur ; la « borne » 3×10⁻²² de B et F ne vaut que pour un trou isolé", [
  ("B", "≤ 3×10⁻²² rad/s (spin maximal)", "B", r"entraînement des référentiels ≤ 3 × 10⁻²² rad/s", "À CORRIGER : n'est pas une borne pour une paire en orbite (que B étudie au §3.5 d)"),
  ("D", "≤ 5×10⁻¹⁴ rad/s (orbital)", "D", r"Entraînement des référentiels à 1 m ; ondes", "conforme"),
  ("F", "≤ 3,3×10⁻²² rad/s ; « 9 ordres de grandeur » sous un gyrolaser géant", "F", r"\| Entraînement des référentiels \(Kerr extrémal\)", "À CORRIGER : avec le terme orbital l'écart au gyrolaser (7×10⁻¹³ rad/s) n'est que de 1 à 2 ordres de grandeur")])

g("Masse pour une zone à CTC (anneau de Kerr) d'un mètre", "a = GM/c² = 1 m ⇒ M = c²/G = 1,347×10²⁷ kg = 0,71 M_Jupiter ; ergosphère de 3,35 m : 2,26×10²⁷ kg ; seuil de Tipler c²/8G = 1,68×10²⁶ kg/m", "1,35×10²⁷ kg (0,71 masse de Jupiter) par mètre de rayon", [
  ("B", "1,35×10²⁷ kg", "B", r"Un anneau de rayon 1 m exige", "conforme"),
  ("D", "1,35×10²⁷ kg (0,71 M_Jupiter)", "D", r"Masse pour une structure de Kerr d'un mètre", "conforme"),
  ("G (rapport 1)", "2,3×10²⁷ kg pour une ergosphère de 3,35 m", "G", r"ergosphère de 3,35 m demande", "conforme (autre définition)")])

g("Champ magnétique « gravitant »", "courbure d'ordre 1 à l'échelle L = 1 m : 3,48×10¹⁸ T ; énergie équivalente à la masse donnant 2 g à 1 m (2,64×10²⁸ J) logée dans 10 cm : 3,98×10¹² T (dans 1 m : 1,3×10¹¹ T) ; champ « pesant » autant que l'eau : 1,50×10⁷ T",
  "trois définitions différentes, toutes exactes : à ne pas confondre dans la synthèse (3,5×10¹⁸ T = courbure forte ; 10¹¹–4×10¹² T = 2 g à 1 m ; 1,5×10⁷ T = densité de l'eau)", [
  ("B", "3,5×10¹⁸ T (courbure à l'échelle du mètre)", "B", r"demande B ≈ 3,5 × 10¹⁸ T", "conforme"),
  ("C", "4×10¹² T (2,64×10²⁸ J dans 10 cm de rayon)", "C", r"Loger cette énergie dans 10 cm de rayon", "conforme"),
  ("F", "1,5×10⁷ T (champ « pesant » autant que l'eau)", "F", r"Champ « pesant » autant que l'eau", "conforme")])

g("Énergie de fabrication des singularités (Σ M c²)", "2,64×10²⁸ J (2,94×10¹¹ kg au total) ; 1,80×10²⁹ J (2 × 10¹² kg) ; 7,0–9,2×10²⁹ J (2 × 3,9–5,1×10¹² kg) ; 2,04×10¹⁹ J (227 kg)",
  "2,6×10²⁸ J (minimum : 2 g à 1 m) à 7–9×10²⁹ J (deux singularités de 300–500 MW) ; la valeur 1,8×10²⁹ J de G repose sur la masse « photons seuls », obsolète", [
  ("B", "3,6×10²⁹ J pour 4×10¹² kg (une singularité)", "B", r"3,6 × 10²⁹ J pour 4 × 10¹² kg", "conforme"),
  ("C", "5×10²⁸ à 8×10²⁹ J", "C", r"\| Énergie de création des deux singularités \|", "borne haute conforme ; borne basse À CORRIGER (voir ligne suivante)"),
  ("C", "5,3×10²⁸ J pour « deux singularités donnant 2 g à 1 m » (2 × 2,94×10¹¹ kg)", "C", r"Fabriquer deux singularités donnant 2 g à 1 m", "ERREUR D'UN FACTEUR 2 : 2 g à 1 m exigent 2,94×10¹¹ kg AU TOTAL (2,64×10²⁸ J, valeur que C donne lui-même pour Q4)"),
  ("G (rapport 1)", "1,8×10²⁹ J (2×10¹² kg) ; 2,6×10²⁸ J (steelman)", "G", r"Mc² pour 2×10¹² kg : \*\*1,8×10²⁹ J\*\*", "la première valeur correspond à la masse photons seuls ; à remplacer par 7–9×10²⁹ J"),
  ("H", "4,0×10²⁹ J pour 4,5×10¹² kg (une singularité)", "H", r"Énergie de masse de 4,5×10¹² kg", "conforme")])

g("Temps de coalescence de la paire (Peters)", "2 × 10¹² kg, d = 0,3 m : 6,44×10³² s = 2,04×10²⁵ ans ; 2 × 4,4×10¹² kg : 2,4×10²³ ans ; à l'entraxe de l'Équipe A (0,098 m) : 2,3×10²³ ans et 2,7×10²¹ ans",
  "6×10³² s = 2×10²⁵ ans (2 × 10¹² kg à 0,3 m) : G et B donnent LA MÊME valeur dans deux unités ; ≥ 10²¹ ans dans tous les cas", [
  ("B", "6×10³² s (10¹² kg, 0,3 m)", "B", r"\| 10¹² kg \| 0,3 m \| 70 rad/s", "conforme"),
  ("D", "≥ 10²³ ans ; 2,0×10²⁵ ans (hypothèse D)", "DS5", r"\| D : 10¹² kg \| 13,2 g", "conforme"),
  ("G (rapport 1)", "10²⁵ ans", "G", r"temps d'inspiral 10²⁵ ans", "conforme (ordre de grandeur de 2×10²⁵ ans)")])

g("Énergie négative requise", "Morris-Thorne, gorge de 1 m : tension 4,8×10⁴² Pa, masse −6,7×10²⁶ kg ; Alcubierre R = 3,7 m, paroi linéaire 1 m : −1,55×10²⁷ kg ; R = 3 m, paroi 0,25 m : −2,7×10²⁷ kg (profil tanh) à −4,0×10²⁷ kg (profil linéaire) ; −Rc²/G (3 m) : −4,0×10²⁷ kg",
  "−10²⁷ kg à un facteur 3 près (−0,35 à −2 masses de Jupiter) ; les écarts viennent des géométries et profils de paroi, non d'erreurs", [
  ("B", "4,8×10⁴² Pa ; −1,5×10²⁷ kg (R = 3,7 m, paroi 1 m)", "B", r"R = 3,7 m, Δ = 1 m, v = c", "conforme"),
  ("D", "−6,7×10²⁶ kg (trou de ver 1 m) ; −2,7×10²⁷ kg (bulle 3 m, paroi 0,25 m)", "D", r"Énergie négative : trou de ver de 1 m", "conforme (profil tanh)"),
  ("F", "il manque ≈ 3×10⁴⁷ (Casimir, 1 m² à 10 nm)", "F", r"Énergie de Casimir, 1 m² à 10 nm", "conforme avec M = bc²/G (facteur 2 au-dessus de Morris-Thorne)"),
  ("G (rapport 1)", "−4×10²⁷ kg pour 3 m", "G", r"−Rc²/G ≈ −4×10²⁷ kg", "conforme (ordre de grandeur)")])

g("Puissance thermique compatible avec 38–49 °C", "convection naturelle (h = 5 W/m²K) + rayonnement (ε = 0,9), ambiance 25 °C : 252–479 W pour 1,80 m² (H1) ; 151–286 W pour 1,07 m² (dimensions A) ; 137–261 W pour 0,98 m² (dimensions E)",
  "0,15–0,30 kW avec L = 0,85 m (0,25–0,5 kW avec H1) : dans tous les cas 10⁶ fois moins que 300–500 MW", [
  ("C", "0,25–0,5 kW (1,8 m²)", "C", r"38–49 °C sur 1,8 m² ⇔ 0,25–0,5 kW", "conforme pour H1 ; ×0,6 avec L = 0,85 m"),
  ("F", "≈ 320–520 W (1,8 m²)", "F", r"≈ 320–520 W dissipés", "cohérent (ambiance plus froide) ; ×0,6 avec L = 0,85 m"),
  ("B", "équilibre radiatif à 6 000–6 800 K pour 44 % de 300–500 MW sur 1,8 m²", "B", r"équilibre radiatif à 6 000–6 800 K", "conforme pour H1 ; 6 800–7 750 K avec L = 0,85 m"),
  ("G (rapport 1)", "6 000–6 800 K", "G", r"\*\*6 000–6 800 K\*\*", "idem")])

g("Dimensions du coffre (L × P × H fermé)", "A : 0,85 × 0,258 × 0,283 m, 62 L, 3 660 kg/m³ pour 227 kg ; E : 0,85 × 0,260 × 0,242 m, 53 L, 4 250 kg/m³ ; H1 : 1,20 × 0,36 × 0,30 m, 130 L, 1 750 kg/m³",
  "L = 0,85 m (médiane ; intervalle central 0,74–1,05 m ; plage 0,65–1,25 m) ; P = L/3,3 ; hauteur fermée 0,24–0,29 m À HARMONISER entre A et E", [
  ("base §7 (H1)", "1,20 × 0,36 × 0,30 m ; 0,13 m³", "base", r"Hypothèse de travail H1", "hypothèse non mesurée ; au-dessus de 4 estimations sur 5"),
  ("A", "0,85 ± 0,20 m × 0,26 × 0,285 m ; 0,063 m³", "A", r"\| Longueur L \| \*\*0,85 m\*\*", "défendable comme fourchette, pas comme écart-type (voir rapport §6)"),
  ("E", "0,85 × 0,26 × 0,24 m (note de la direction) ; corps du rapport encore à 1,20 m", "E", r"Note de la direction", "hauteur fermée 0,24 m contre 0,285 m chez A (couvercle 0,125 P contre 0,25 P) ; rapport non mis à jour"),
  ("C", "1,20 × 0,36 × 0,30 m ; 1,8 m² ; 0,13 m³", "C", r"Hypothèses géométriques", "À METTRE À JOUR (voir rapport §2 f)"),
  ("F (EXP-12)", "≈ 1,2 × 0,4 × 0,3 m (coffre du banc) ; 1,8 m²", "F12", r"COFFRE INSTRUMENTÉ", "sans conséquence pour le banc ; 1,8 m² à mettre à jour dans le bilan thermique")])

g("Séparation des deux singularités", "A : entraxe 0,115 L = 0,098 m ; E : 0,356 P = 0,093 m à L = 0,85 m (0,131 m à 1,20 m)", "≈ 0,10 m (documents) ; 0,15 m et 0,30 m sont des hypothèses sans appui documentaire", [
  ("A", "0,098 m ± 0,025", "A", r"\| Entraxe des logements \|", "seule valeur issue des documents (DOC-007)"),
  ("C", "0,15 m [HYP]", "C", r"entraxe 15 cm", "à remplacer par 0,10 m : attraction mutuelle ×2,3, période orbitale ÷1,9"),
  ("D", "0,3 m [HYP]", "DS5", r"\*\*Séparation\*\* d = 0,3 m", "à remplacer : temps de coalescence ÷88, entraînement orbital ×0,57 ; conclusions inchangées"),
  ("B", "0,3 m", "B", r"\| 10¹² kg \| 0,3 m \| 70 rad/s", "idem"),
  ("G (rapport 1)", "0,3 m (0,15–0,30 m)", "G", r"Deux trous noirs de 10¹² kg à 0,3 m", "idem")])

out = os.path.join(R, "08_red_team", "coherence_inter_equipes.csv")
with open(out, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["grandeur", "equipe", "valeur_de_l_equipe", "fichier_et_ligne", "recalcul_red_team", "valeur_retenue", "commentaire"])
    w.writerows(L)
print(len(L), "lignes ;", len({l[0] for l in L}), "grandeurs →", out)
