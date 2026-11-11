#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — produit ../references_I.csv à partir de resultats_verification.json (réponses des API Crossref / arXiv).
Chaque ligne dit si la référence est NOUVELLE (introduite par l'Équipe I) ou RÉUTILISÉE (déjà vérifiée par une autre
équipe ; nous avons relu sa notice et, quand il existe, son résumé), et ce que nous en tirons.
Usage : python -I generer_references.py"""
import csv, json
from pathlib import Path

ICI = Path(__file__).resolve().parent
R = json.loads((ICI / "resultats_verification.json").read_text(encoding="utf-8"))
ORIGINE = {  # clé : (origine, usage dans le rapport, chiffre repris et sa provenance)
    "RossiHall41": ("nouvelle (Équipe I)", "§3.4 muons : première mesure de la désintégration en vol selon l'impulsion", "aucun chiffre repris (résumé absent de la notice)"),
    "FrischSmith63": ("nouvelle (Équipe I)", "§3.4 muons", "facteur de dilatation 8,8 ± 0,8 ; vitesses 0,9950–0,9954 c : lus dans le résumé"),
    "CosmicWatch18": ("nouvelle (Équipe I)", "§3.4 télescope à muons du commerce / kit", "coût matériel < 100 $ par détecteur, alimentation USB : lus dans le résumé"),
    "PDG24": ("nouvelle (Équipe I)", "§3.4 intensité des muons au sol", "70 m⁻² s⁻¹ sr⁻¹ et énergie moyenne ≈ 4 GeV : cités DE MÉMOIRE, non relus dans le texte"),
    "Bailey77": ("réutilisée (Équipe B, V-CR)", "§5.1 muons en anneau de stockage", "γ = 29,3 et 64,4 µs : recalculés (i05) à partir de p = 3,094 GeV/c, valeur citée de mémoire"),
    "Bennett06": ("nouvelle (Équipe I)", "§5.1 anneau à muons de Brookhaven", "aucun chiffre repris"),
    "Aguillard23": ("nouvelle (Équipe I)", "§5.1 anneau à muons de Fermilab", "aucun chiffre repris"),
    "Botermann14": ("nouvelle (Équipe I)", "§5.1 test de la dilatation sur ions stockés", "aucun chiffre repris"),
    "Koller17": ("nouvelle (Équipe I)", "§4.1 horloge à réseau transportable", "7×10⁻¹⁷ : lu dans le TITRE"),
    "BPT72": ("nouvelle (Équipe I)", "§5.2 orbites circulaires de Kerr (formules de r_ISCO, E, dt/dτ)", "formules citées de mémoire, contrôlées numériquement (a = 0 : r = 6, dt/dτ = √2 ; a = 0,998 : 10,79 comme l'Équipe D)"),
    "CW09": ("réutilisée (Équipe H)", "§5.3 vaisseau à trou noir", "« à la limite du possible » : lu dans le résumé ; aucun chiffre de l'article repris"),
    "Roslund24": ("réutilisée (Équipe H)", "§3.3, §4.1 horloge optique à iode", "35 L ; 3 horloges ; 20 jours en mer ; < 300 ps/jour : lus dans le résumé"),
    "Grotti18": ("réutilisée (Équipe H)", "§4.1 géodésie chronométrique de terrain", "aucun chiffre repris"),
    "Torres17": ("réutilisée (Équipe H)", "§4.3 superradiance d'un vortex", "20 % à 3,70 Hz, h = 6,25 cm : lus dans le résumé arXiv (version publiée : 14 ± 8 % selon l'Équipe F)"),
    "Svancara24": ("réutilisée (Équipe H)", "§4.3 vortex quantique géant", "aucun chiffre repris"),
    "Lloyd11a": ("réutilisée (Équipe H)", "§4.4 P-CTC", "principe ; probabilités recalculées (i04)"),
    "Ringbauer14": ("réutilisée (Équipe H)", "§4.4 D-CTC simulées", "principe ; détail du protocole cité de mémoire"),
    "Procopio15": ("réutilisée (Équipe H)", "§4.4 interrupteur quantique", "un seul usage de chaque porte : lu dans le résumé"),
    "MM20": ("réutilisée (Équipe H)", "§5.4 trous de ver « humainement traversables »", "cadre Randall-Sundrum : lu dans le résumé"),
    "MMP18": ("réutilisée (Équipe H)", "§5.4 trou de ver à quatre dimensions", "« ne conduit pas à des violations de causalité » : lu dans le résumé"),
    "Kugel24": ("réutilisée (Équipe H)", "§5.3 pas de trou noir par concentration de lumière", "conclusion lue dans le résumé"),
    "VKD03": ("réutilisée (Équipe H)", "§5.4 quantité de matière exotique", "conclusion lue dans le résumé"),
    "Janvier22": ("réutilisée (Équipe H)", "§4.2 gradiomètre différentiel", "0,1 E à long terme : lu dans le résumé"),
    "Templier22": ("réutilisée (Équipe H)", "§4.2 accéléromètre hybride", "aucun chiffre repris"),
    "ASMY23": ("réutilisée (Équipe H)", "§4.4 avantage métrologique simulé", "aucun chiffre repris"),
    "Huang26": ("réutilisée (Équipe H)", "§4.4 P-CTC sur processeurs en nuage", "principe lu dans le résumé"),
    "Takamoto20": ("réutilisée (Équipe H)", "§4.1 deux horloges transportables", "aucun chiffre repris (résumé absent)"),
    "Menoret18": ("réutilisée (Équipe H)", "§4.2 gravimètre absolu", "stabilité < 10 nm/s² (1 µGal) : lue dans le résumé"),
    "Stray22": ("réutilisée (Équipe H)", "§4.2 gradiomètre de terrain", "20 E ; tunnel de 2 m détecté à S/B 8 : lus dans le résumé"),
    "Chou10": ("réutilisée (Équipe H)", "§4.1 relativité à l'échelle du mètre", "10 m/s et ~1 m : lus dans le résumé de la revue"),
    "HK72b": ("réutilisée (Équipes F, H)", "§3.2 contrôle du calcul", "−59 ± 10 ns et +273 ± 7 ns : lus dans le résumé"),
    "Wu19": ("réutilisée (Équipe H)", "§4.2", "aucun chiffre repris"),
    "Bidel20": ("réutilisée (Équipe H)", "§4.2", "aucun chiffre repris"),
    "QCTRL26": ("réutilisée (Équipe H)", "§4.2 navigation gravimétrique (prépublication)", "aucun chiffre repris"),
    "Bothwell22": ("réutilisée (Équipe H)", "§4.1", "aucun chiffre repris"),
    "Lu26": ("réutilisée (Équipe H)", "§4.1 références Lu⁺", "1,2×10⁻¹⁹ ; 4,8×10⁻¹⁶/√τ ; ~200 h : lus dans le résumé"),
    "Marshall25": ("réutilisée (Équipe H)", "§4.1 horloge Al⁺", "5,5×10⁻¹⁹ ; 3,5×10⁻¹⁶/√τ : lus dans le résumé"),
    "Goswami18": ("réutilisée (Équipe H)", "§4.4 interrupteur quantique", "aucun chiffre repris"),
    "Falque": ("réutilisée (Équipe H)", "§4.3 fluides de polaritons", "aucun chiffre repris"),
}
with open(ICI.parent / "references_I.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cle", "auteurs", "annee", "titre", "revue_ou_arXiv", "doi", "arxiv", "statut", "source_de_verification", "date_verification", "origine", "usage", "chiffres_repris"])
    for cle, d in R.items():
        o = ORIGINE.get(cle, ("", "", ""))
        titre = " ".join(d.get("titre", "").replace("<mml:math xmlns:mml=\"http://www.w3.org/1998/Math/MathML\"", "").split())
        w.writerow([cle, d.get("auteurs", ""), d.get("annee", ""), titre[:160], d.get("revue", ""), d.get("doi", "") or "", d.get("arxiv", "") or "",
                    d.get("statut", ""), d.get("source", ""), "2026-11-10", o[0], o[1], o[2]])
print(len(R), "références écrites dans references_I.csv ;", sum(1 for k in R if ORIGINE.get(k, ("",))[0].startswith("nouvelle")), "nouvelles")
