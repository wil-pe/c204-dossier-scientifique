#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red Team n° 2 — Tâche 6. L'estimation L = 0,85 ± 0,20 m de l'Équipe A est-elle statistiquement défendable ?
On reprend les cinq « méthodes » de 02_reconstruction/dimensions.json et on teste trois façons de les combiner.
Chaque méthode est représentée par une loi triangulaire (min, mode, max) = (borne basse, valeur, borne haute).
Graine 20261110."""
import json, os
import numpy as np
rng = np.random.default_rng(20261110)
N = 400000
M = {"M1 sangle (k HYP)": (0.56, 0.74, 1.03), "M2a ruban 2 pouces": (0.67, 0.77, 0.91), "M2b ruban 3 pouces": (1.00, 1.15, 1.36),
     "M3 télécommande (dessin)": (0.71, 0.92, 1.12), "M4 cordon": (0.64, 0.86, 1.07)}
tri = {k: rng.triangular(*v, N) for k, v in M.items()}
def resume(x, nom):
    q = np.quantile(x, [0.025, 0.16, 0.5, 0.84, 0.975])
    print(f"{nom:<64} médiane {q[2]:.2f} ; 68 % [{q[1]:.2f} ; {q[3]:.2f}] ; 95 % [{q[0]:.2f} ; {q[4]:.2f}] ; P(L ≥ 1,20) = {np.mean(x >= 1.20):.3f}")
    return {"mediane": float(q[2]), "ic68": [float(q[1]), float(q[3])], "ic95": [float(q[0]), float(q[4])], "P_L_sup_1.20": float(np.mean(x >= 1.20))}
out = {}
vals = [v[1] for v in M.values()]
print("valeurs centrales :", vals, "médiane", np.median(vals), "moyenne", round(float(np.mean(vals)), 3), "écart-type (n−1)", round(float(np.std(vals, ddof=1)), 3), "demi-étendue", (max(vals) - min(vals)) / 2)
# (a) lecture de A : cinq méthodes équipondérées (mélange) — compte DEUX fois la même mesure de ruban
out["a_cinq_methodes"] = resume(np.concatenate(list(tri.values())), "(a) mélange des 5 « méthodes » (lecture de A)")
# (b) ruban compté UNE fois (2 ou 3 pouces, 50/50) : 4 méthodes
ruban = np.where(rng.random(N) < 0.5, tri["M2a ruban 2 pouces"], tri["M2b ruban 3 pouces"])
out["b_quatre_methodes"] = resume(np.concatenate([tri["M1 sangle (k HYP)"], ruban, tri["M3 télécommande (dessin)"], tri["M4 cordon"]]), "(b) ruban compté une fois (2 ou 3 pouces à 50/50)")
# (c) sans M3 (rapport pris sur le DESSIN DOC-007, dont on sait qu'il n'est pas un relevé de l'objet : I-03, S7c)
out["c_sans_dessin"] = resume(np.concatenate([tri["M1 sangle (k HYP)"], ruban, tri["M4 cordon"]]), "(c) idem sans M3 (étalon lu sur le dessin, non sur l'objet)")
# (d) moyenne des 4 méthodes tirées indépendamment (suppose à tort des erreurs indépendantes et sans biais commun)
out["d_moyenne_independante"] = resume((tri["M1 sangle (k HYP)"] + ruban + tri["M3 télécommande (dessin)"] + tri["M4 cordon"]) / 4, "(d) moyenne de 4 tirages indépendants (optimiste)")
# sensibilité : volume et masse volumique
for L in (0.60, 0.70, 0.85, 1.05, 1.20):
    P = L / 3.30; H = 0.85 * P + 0.25 * P
    print(f"   L = {L:.2f} m : P = {P:.3f} m ; H fermée = {H:.3f} m ; V = {L*P*H*1000:.0f} L ; ρ(227 kg) = {227/(L*P*H):.0f} kg/m³")
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "journaux", "longueur_L.json"), "w"), indent=1)
