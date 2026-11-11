# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 7 : trois calculateurs à vote (« Borda ») — comparaison à la redondance
modulaire triple (TMR), fiabilité de la chaîne complète, et démonstration qu'un décompte de Borda n'est pas
un voteur tolérant aux fautes.

Sorties : resultats/c08_calculateurs.json
"""
import itertools
import numpy as np
import c00_constantes as K

res = {}
T = 6.0   # h

# ------------------------------------------------------------------ fiabilité simplex / TMR / 2oo4
fiab = {}
for lam in (1e-3, 1e-4, 1e-5):          # taux de défaillance par heure [HYP]
    R = np.exp(-lam * T)
    R_tmr = 3 * R**2 - 2 * R**3          # voteur parfait, majorité 2 sur 3
    fiab[f"lambda = {lam:g} /h"] = dict(
        R_simplex=R, defaillance_simplex=1 - R, R_TMR=R_tmr, defaillance_TMR=1 - R_tmr,
        gain=(1 - R) / (1 - R_tmr), MTTF_simplex_h=1 / lam, MTTF_TMR_h=5 / (6 * lam))
res["fiabilite_6h"] = fiab
res["TMR_utile_si_R_superieur_a"] = 0.5

# ------------------------------------------------------------------ chaîne complète : éléments non redondés
# D'après DOC-008 : 1 batterie, 1 pompe, 1 générateur d'électrons, 1 unité de capteurs de gravité ;
# 2 générateurs/régulateurs de champ (un par singularité, donc en série, pas en redondance) ;
# 3 calculateurs (2 sur 3), 4 horloges (2 sur 4 supposé).
lam = 1e-4
R1 = np.exp(-lam * T)
from math import comb
R_tmr = 3 * R1**2 - 2 * R1**3
R_2oo4 = sum(comb(4, k) * R1**k * (1 - R1) ** (4 - k) for k in (2, 3, 4))
serie = dict(batterie=R1, pompe=R1, generateur_electrons=R1, unite_capteurs_gravite=R1,
             regulateur_champ_1=R1, regulateur_champ_2=R1)
R_serie = float(np.prod(list(serie.values())))
R_sys = R_serie * R_tmr * R_2oo4
res["chaine_complete_lambda_1e-4"] = dict(
    defaillance_elements_non_redondes=1 - R_serie, defaillance_calculateurs_TMR=1 - R_tmr,
    defaillance_horloges_2sur4=1 - R_2oo4, defaillance_systeme=1 - R_sys,
    part_des_calculateurs_dans_le_risque=(1 - R_tmr) / (1 - R_sys))

# ------------------------------------------------------------------ Borda contre majorité
def borda(classements):
    cands = sorted(classements[0])
    n = len(cands)
    score = {c: 0 for c in cands}
    for cl in classements:
        for rang, c in enumerate(cl):
            score[c] += n - 1 - rang
    return score


# 2 calculateurs sains classent A > B > C > D ; 1 calculateur fautif (ou malveillant) classe B > C > D > A
sains = ["A", "B", "C", "D"]
fautif = ["B", "C", "D", "A"]
sc = borda([sains, sains, fautif])
res["borda_exemple"] = dict(classement_des_2_sains="A>B>C>D", classement_du_fautif="B>C>D>A", scores=sc,
                            gagnant_borda=max(sc, key=sc.get), gagnant_majorite="A")
# recherche exhaustive : dans combien de cas (2 sains d'accord, 1 fautif arbitraire) Borda écarte-t-il le choix des sains ?
stats = {}
for n in (3, 4, 5):
    cands = [chr(65 + i) for i in range(n)]
    perdu = egalite = total = 0
    for perm in itertools.permutations(cands):
        s = borda([cands, cands, list(perm)])
        best = max(s.values())
        gagnants = [c for c, v in s.items() if v == best]
        total += 1
        if "A" not in gagnants:
            perdu += 1
        elif len(gagnants) > 1:
            egalite += 1
    stats[f"{n} options"] = dict(classements_fautifs_possibles=total, choix_sain_renverse=perdu, ex_aequo=egalite)
res["borda_statistiques"] = stats
# voteur médian sur valeurs numériques : une valeur aberrante est toujours masquée
vals = [9.80665, 9.80664, 1e6]
res["voteur_median_exemple"] = dict(entrees=vals, sortie=float(np.median(vals)))
res["byzantin"] = "Sans messages signés, tolérer f fautes arbitraires exige n >= 3f + 1 calculateurs (Lamport, Shostak, Pease 1982) : 3 ne suffisent pas pour f = 1."

K.sauver_json("c08_calculateurs.json", res)
for k_, v in fiab.items():
    print(k_, {a: f"{b:.4g}" for a, b in v.items()})
print("Chaîne complète :", {a: f"{b:.4g}" for a, b in res["chaine_complete_lambda_1e-4"].items()})
print("Borda :", res["borda_exemple"])
print("Borda stats :", stats)
print("Médian :", res["voteur_median_exemple"])
