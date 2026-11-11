#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — contrôle d'interférences du modèle (boîtes englobantes alignées sur les axes).

Vérifie, pour chaque variante du coffre, que les composants internes ne se chevauchent pas entre eux,
ne traversent ni la platine ni le fond ni les parois, et ne pénètrent pas dans le bac de rangement.
Le test est conservatif pour les sphères, tores et cylindres (boîte englobante) : les couples
volontairement emboîtés (carter / enveloppe / bobines / calottes / raccords d'un même ensemble, collecteur
traversant le régulateur 5, comme sur DOC-008) sont ignorés.

Usage : python mesures/verifier_interferences.py [modele.json]      (code de retour 1 si interférence)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from construire_modele import maillage_piece   # noqa: E402

TOL = 5e-4   # m


def main(chemin=None):
    chemin = Path(chemin) if chemin else Path(__file__).resolve().parents[1] / "modele_c204.json"
    modele = json.loads(chemin.read_text(encoding="utf-8"))
    nb = 0
    for cle in ("A", "A2"):
        v = modele["variantes"][cle]
        k = v["cotes_cles"]
        c = modele["cotes"]
        e, ef = c["e_rebord"]["valeur"], c["e_fond"]["valeur"]
        zpi = k["z_platine"] - c["e_platine"]["valeur"]
        boites = {}
        for p in v["pieces"]:
            if p["couche"] == "interne" or p["nom"].startswith("Rangement 9"):
                m = maillage_piece(p, v, "ferme")
                boites[p["id"]] = (p, m.bounds)
        internes = [(p, b) for p, b in boites.values() if p["couche"] == "interne"]
        bac = [(p, b) for p, b in boites.values() if p["nom"].startswith("Rangement 9")]
        # 1) contre l'enveloppe intérieure
        for p, b in internes:
            lim = [(e, k["L"] - e), (e, k["P"] - e), (ef, zpi)]
            for ax, (lo, hi) in enumerate(lim):
                dans_logement = ax == 2 and p["ensemble"].startswith("Ensemble singularité")   # le sommet affleure dans le fût
                if b[0][ax] < lo - TOL or (b[1][ax] > hi + TOL and not dans_logement):
                    nb += 1
                    print(f"[{cle}] HORS ENVELOPPE axe {'XYZ'[ax]} : {p['nom']}  ({b[0][ax]:.4f} … {b[1][ax]:.4f}, limites {lo:.4f} … {hi:.4f})")

        def chevauche(b1, b2):
            return all(b1[0][i] < b2[1][i] - TOL and b2[0][i] < b1[1][i] - TOL for i in range(3))

        # 2) entre composants d'ensembles différents
        for i in range(len(internes)):
            for j in range(i + 1, len(internes)):
                (p1, b1), (p2, b2) = internes[i], internes[j]
                if p1["ensemble"] == p2["ensemble"]:
                    continue
                noms = p1["nom"] + " | " + p2["nom"]
                noyau = all(q["ensemble"].startswith("Ensemble singularité") or q["ensemble"].startswith("Injection") or q["ensemble"].startswith("Générateurs / régulateurs")
                            for q in (p1, p2))
                if noyau and ("Collecteur" in noms or "Régulateur d'électrons" in noms or "Calotte" in noms or "Bobine" in noms or "Enveloppe" in noms):
                    continue      # emboîtements du noyau, repris de DOC-008 (boîtes englobantes de sphères et de tores)
                if chevauche(b1, b2):
                    nb += 1
                    print(f"[{cle}] CHEVAUCHEMENT : {p1['nom']}  ×  {p2['nom']}")
        # 3) contre le bac de rangement
        for p, b in internes:
            for q, bq in bac:
                if chevauche(b, bq):
                    nb += 1
                    print(f"[{cle}] DANS LE RANGEMENT 9 : {p['nom']}  ×  {q['nom']}")
    print(f"{chemin.name} : L = {modele['cotes']['L']['valeur']} m — {nb} interférence(s)")
    return nb


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else None) else 0)
