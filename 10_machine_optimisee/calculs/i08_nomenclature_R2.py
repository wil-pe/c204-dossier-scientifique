#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i08 : nomenclature chiffrée du palier 2 (C204-R2, laboratoire de recherche) et bilans.

Toutes les masses, puissances et coûts sont des ESTIMATIONS d'ordre de grandeur (2026), sauf mention
« vérifié » (fiche relue par l'Équipe C ou chiffre lu dans le résumé d'un article vérifié par API).
Le palier 2 n'est pas contraint par le coffre : c'est une installation de laboratoire dont une partie
(horloges, gravimètre) est transportable en remorque.

Sorties : ../nomenclature_R2.csv, resultats/i08_bilans_R2.json / .txt
"""
from i00_commun import RACINE, ecrire_csv, ecrire_json, ecrire_txt

# id, module, désignation, élément C204 correspondant, quantité, masse unitaire kg, puissance unitaire W, coût unitaire k€, TRL, performance clé, source / statut
N = [
    ("R2-01", "M1 horloges", "Horloge optique à ion unique (piège de Paul, lasers, peigne de fréquences), en baie transportable", "singularité principale + logement + refroidissement", 1, 400, 1500, 1500, 5,
     "incertitude 10⁻¹⁸ à 10⁻¹⁹ ; instabilité 3,5 à 4,8×10⁻¹⁶/√τ", "performances : résumés vérifiés (Marshall 2025, Arnold 2026) ; masse, puissance, coût : estimation"),
    ("R2-02", "M1 horloges", "Seconde horloge optique identique, sur plateforme à hauteur réglable (0 à 1 m, ±1 mm)", "singularité de direction", 1, 450, 1500, 1500, 5,
     "Δf/f = 1,09×10⁻¹⁶ par mètre de surélévation", "estimation"),
    ("R2-03", "M1 horloges", "Lien optique fibré stabilisé (local et vers un laboratoire distant)", "—", 1, 20, 100, 80, 7, "transfert de fréquence < 10⁻¹⁸", "estimation"),
    ("R2-04", "M1 horloges", "Horloge optique compacte à iode de 35 L (oscillateur volant, horloge de transport)", "4 horloges au césium", 1, 40, 150, 300, 7,
     "erreur de temps < 300 ps par jour en mer ; 35 L", "résumé vérifié (Roslund 2024) ; masse, puissance, coût : estimation"),
    ("R2-05", "M1 horloges", "Ensemble de 4 horloges miniatures au césium + comparateur (repris du palier 1)", "4 horloges au césium", 1, 3, 16, 28, 9, "secours et datation", "voir nomenclature_R1.csv"),
    ("R2-06", "M2 gravité", "Gravimètre absolu à atomes froids", "capteurs de gravité VGL", 1, 140, 500, 500, 8, "stabilité à long terme < 1 µGal",
     "masse < 140 kg et 500 W : vérifié C ; stabilité : résumé vérifié (Ménoret 2018) ; coût : estimation"),
    ("R2-07", "M2 gravité", "Gradiomètre différentiel à atomes froids", "capteurs de gravité VGL", 1, 150, 500, 700, 6, "gradient vertical : 20 E statistique ; 0,1 E à long terme",
     "résumés vérifiés (Stray 2022 ; Janvier 2022) ; masse, puissance, coût : estimation"),
    ("R2-08", "M2 gravité", "Gravimètre relatif de classe microgal (repris du palier 1)", "capteurs de gravité VGL", 1, 5.5, 5.2, 100, 9, "écart-type < 5 µGal", "vérifié C ; coût : estimation"),
    ("R2-09", "M2 gravité", "Nivellement de précision, GNSS géodésique, station météorologique", "—", 1, 15, 20, 40, 9, "dénivelés à ±1 cm", "estimation"),
    ("R2-10", "M3 Kerr analogue", "Cuve 3 m × 1,5 m × 0,5 m à fond percé de deux orifices, structure, 280 L d'eau", "deux singularités « dans un champ de Kerr » (DOC-009)", 1, 600, 0, 25, 4,
     "h = 6,25 cm ; ondes longues à 0,78 m/s", "conception Équipe I ; estimation"),
    ("R2-11", "M3 Kerr analogue", "Recirculation : 2 pompes régulées (0 à 1 L/s), débitmètres, tranquillisation, 2 réservoirs", "pompe et réservoirs", 1, 80, 600, 15, 6,
     "circulation ~1,5×10⁻² m²/s par vortex", "estimation"),
    ("R2-12", "M3 Kerr analogue", "Batteur à houle et plage absorbante", "—", 1, 30, 100, 10, 8, "ondes planes de 0,5 à 5 Hz", "estimation"),
    ("R2-13", "M3 Kerr analogue", "Profilométrie optique de la surface (caméra rapide, mire, éclairage à diodes)", "capteur de singularité", 1, 20, 200, 60, 7,
     "hauteur de surface à ~10 µm", "estimation"),
    ("R2-14", "M4 causalité quantique", "Banc photonique : source de paires de photons, optique de polarisation, 4 détecteurs de photons uniques, coïncidences", "—", 1, 60, 150, 120, 6,
     "~10⁴ paires/s ; P-CTC, D-CTC simulées, interrupteur quantique", "estimation ; laser de pompe de classe 3B : cadre de laboratoire obligatoire"),
    ("R2-15", "M4 causalité quantique", "Accès à un processeur quantique en nuage", "—", 1, 0, 0, 20, 7, "circuits à post-sélection sur quelques qubits", "résumé vérifié (Huang 2026) pour le principe ; coût annuel : estimation"),
    ("R2-16", "communs", "Hodoscope à muons à 4 plans (taux selon l'altitude, durée de vie du muon)", "« évent à rayons X »", 1, 20, 20, 8, 9, "τ = 2,2 µs ; facteur de dilatation", "estimation"),
    ("R2-17", "communs", "Centrale inertielle à gyromètres à fibre de classe navigation", "singularité de direction (R1)", 1, 5, 20, 60, 9, "cap à ~0,1°", "estimation"),
    ("R2-18", "communs", "3 calculateurs à vote, acquisition en aveugle (clé scellée), stockage", "3 calculateurs à vote", 1, 30, 300, 20, 9, "protocole de l'expérience EXP-12", "estimation"),
    ("R2-19", "communs", "Remorque ou abri climatisé (±0,5 K), onduleur 10 kVA, isolation vibratoire", "coffre + batterie", 1, 1500, 3000, 120, 9, "transport de M1 et M2", "estimation"),
    ("R2-20", "communs", "Sécurité : interverrouillages laser et haute tension, arrêt d'urgence, enceintes", "arrêt d'urgence", 1, 20, 20, 15, 9, "état sûr réel", "estimation"),
]


def main():
    lignes = [[i, m, d, o, q, mu, q * mu, pu, q * pu, cu, q * cu, t, perf, src] for (i, m, d, o, q, mu, pu, cu, t, perf, src) in N]
    ecrire_csv(RACINE / "nomenclature_R2.csv",
               ["id", "module", "designation", "element_C204_correspondant", "quantite", "masse_unitaire_kg_estimation", "masse_totale_kg", "puissance_unitaire_W_estimation",
                "puissance_totale_W", "cout_unitaire_kEUR_estimation", "cout_total_kEUR", "TRL", "performance_cle", "source_et_statut"], lignes)
    L = ["i08 — NOMENCLATURE ET BILANS DU PALIER 2 (estimations)", "=" * 90]
    res = {}
    for mod in sorted({n[1] for n in N}):
        m = sum(n[4] * n[5] for n in N if n[1] == mod)
        p = sum(n[4] * n[6] for n in N if n[1] == mod)
        c_ = sum(n[4] * n[7] for n in N if n[1] == mod)
        res[mod] = dict(masse_kg=m, puissance_W=p, cout_kEUR=c_, TRL_min=min(n[8] for n in N if n[1] == mod))
        L.append("  %-24s %7.0f kg  %6.0f W  %6.0f k€   TRL minimal %d" % (mod, m, p, c_, res[mod]["TRL_min"]))
    M = sum(v["masse_kg"] for v in res.values())
    P = sum(v["puissance_W"] for v in res.values())
    C = sum(v["cout_kEUR"] for v in res.values())
    transportable = sum(n[4] * n[5] for n in N if n[1] in ("M1 horloges", "M2 gravité")) + 1500 + 5 + 30 + 20
    res["total"] = dict(masse_kg=M, puissance_W=P, cout_kEUR=C, masse_partie_transportable_kg=transportable, rapport_masse_a_227kg=M / 227.0)
    L.append("  %-24s %7.0f kg  %6.0f W  %6.0f k€" % ("TOTAL", M, P, C))
    L.append("  Partie transportable (M1, M2, communs en remorque) : ≈ %.0f kg. Rapport à la masse revendiquée de la C204 : ×%.0f." % (transportable, M / 227.0))
    # thermique : la quasi-totalité de la puissance électrique finit en chaleur dans l'abri
    L.append("  Thermique : ≈ %.1f kW à évacuer par la climatisation de l'abri (stabilité requise ±0,5 K pour les cavités optiques)." % (P / 1000))
    L.append("  Énergie : %.0f kWh par jour ; hors de portée d'une batterie embarquée de 227 kg (≈ 30 kWh) au-delà de quelques heures." % (P * 24 / 1000))
    res["total"]["energie_kWh_par_jour"] = P * 24 / 1000
    ecrire_json("i08_bilans_R2.json", res)
    ecrire_txt("i08_bilans_R2.txt", L)


if __name__ == "__main__":
    main()
