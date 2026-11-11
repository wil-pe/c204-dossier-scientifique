#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red Team n° 2 — Tâche 4. Contrôles indépendants des démonstrations de l'annexe B1 (Équipe B).
 (1) Extérieur de van Stockum-Tipler pour aR > 1/2 : solution du vide ? raccord C1 ? structure « sinusoïdale en ln r » ?
 (2) Kerr-Newman : g^{tt} < 0 pour r > r+ (cas sous-extrémal) ; cas NON couvert : sur-extrémal (singularité nue).
 (3) Borne « 2 g » : contre-exemple hors hypothèse de staticité (observateur en chute libre) pour situer la portée.
Sortie : journaux/audit_demonstrations_B.txt"""
import math, os, random
import sympy as sp
import mpmath as mp

OUT = []
def dit(s=""):
    print(s); OUT.append(s)

# ---------------------------------------------------------------- (1) Tipler extérieur, aR > 1/2
dit("(1) EXTÉRIEUR DE VAN STOCKUM-TIPLER, aR > 1/2")
t, r, ph, z = sp.symbols("t r phi z", real=True)
Rr, m = sp.symbols("R m", positive=True)                 # m = sqrt(4 a²R² − 1) > 0 ; a²R² = (1 + m²)/4
beta = sp.atan(m)
gam = m * sp.log(r / Rr)
a2R2 = (1 + m**2) / 4
H = sp.exp(-a2R2) * (r / Rr) ** (-2 * a2R2)
L = Rr * r * sp.sin(3 * beta + gam) / (2 * sp.sin(2 * beta) * sp.cos(beta))
M = r * sp.sin(beta + gam) / sp.sin(2 * beta)
F = r * sp.sin(beta - gam) / (Rr * sp.sin(beta))
X = (t, r, ph, z)
g = sp.Matrix([[-F, 0, M, 0], [0, H, 0, 0], [M, 0, L, 0], [0, 0, 0, H]])
# identité F L + M² = r² (contrôlée numériquement à 40 chiffres : la simplification symbolique d'atan(m) est lente)
mp.mp.dps = 40
def num(expr, vals):
    return mp.mpf(sp.N(expr.subs(vals), 40))
pire = 0
for (mv, rv) in ((0.3, 1.7), (1.0, 5.0), (math.sqrt(3), 0.9), (2.5, 40.0)):
    vals = {m: sp.Float(mv, 40), Rr: sp.Float(1, 40), r: sp.Float(rv, 40)}
    pire = max(pire, abs(num(F * L + M**2 - r**2, vals) / num(r**2, vals)))
dit(f"   identité F·L + M² = r² : écart relatif max. sur 4 points = {mp.nstr(pire, 3)}")
# tenseur de Ricci (formel), puis évaluation numérique à 40 chiffres en plusieurs points (m, r)
ginv = g.inv()
def Gamma(i, j, k):
    return sum(ginv[i, l] * (sp.diff(g[l, j], X[k]) + sp.diff(g[l, k], X[j]) - sp.diff(g[j, k], X[l])) for l in range(4)) / 2
Gam = [[[Gamma(i, j, k) for k in range(4)] for j in range(4)] for i in range(4)]
def Ricci(j, k):
    return sum(sp.diff(Gam[i][j][k], X[i]) - sp.diff(Gam[i][j][i], X[k]) + sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for l in range(4)) for i in range(4))
comps = [(0, 0), (0, 2), (2, 2), (1, 1), (3, 3)]
Ric = {jk: Ricci(*jk) for jk in comps}
pire = 0
for (mv, rv) in ((0.3, 1.7), (1.0, 5.0), (math.sqrt(3), 0.9), (2.5, 40.0), (0.2, 300.0)):
    vals = {m: sp.Float(mv, 40), Rr: sp.Float(1, 40), r: sp.Float(rv, 40)}
    for jk, e in Ric.items():
        ech = abs(num(g[jk[0], jk[1]], vals)) / mp.mpf(rv) ** 2 + mp.mpf("1e-40")
        pire = max(pire, abs(num(e, vals)) / ech)
dit(f"   R_μν = 0 (5 composantes non triviales, 5 points (m, r), 40 chiffres) : résidu relatif max. = {mp.nstr(pire, 3)}")
# raccord C1 en r = R avec l'intérieur (H = exp(−a²r²), L = r²(1 − a²r²), M = a r², F = 1)
av = sp.sqrt(a2R2) / Rr
inter = {"H": sp.exp(-av**2 * r**2), "L": r**2 * (1 - av**2 * r**2), "M": av * r**2, "F": sp.Integer(1)}
exter = {"H": H, "L": L, "M": M, "F": F}
pire0 = pire1 = 0
for mv in (0.3, 1.0, 2.5):
    vals = {m: sp.Float(mv, 40), Rr: sp.Float(1, 40), r: sp.Float(1, 40)}
    for k in inter:
        pire0 = max(pire0, abs(num(inter[k] - exter[k], vals)))
        pire1 = max(pire1, abs(num(sp.diff(inter[k], r) - sp.diff(exter[k], r), vals)))
dit(f"   raccord en r = R : saut max. des fonctions = {mp.nstr(pire0, 3)} ; saut max. des dérivées premières = {mp.nstr(pire1, 3)}")
# structure : L/r est une sinusoïde PURE en ln r ; L lui-même est une sinusoïde en ln r multipliée par r (amplitude croissante)
dit("   L/(R r) = sin(3β + m ln(r/R)) / (2 sin 2β cos β) : sinusoïde exacte de la variable ln r, de « période » 2π/m en ln r ;")
dit("   L, M, F eux-mêmes = r × (sinusoïde en ln r) : log-périodiques d'amplitude ∝ r, pas des sinusoïdes de r.")
for aR in (0.51, 0.6, 1.0, 2.0):
    mv = math.sqrt(4 * aR * aR - 1); b = math.atan(mv)
    zs = [math.exp((n * math.pi - 3 * b) / mv) for n in range(1, 5)]
    zs = [x for x in zs if x >= 1 - 1e-12][:3]
    dit(f"   aR = {aR:<4} : m = {mv:.4f} ; zéros de g_φφ à r/R = " + ", ".join(f"{x:.4g}" for x in zs) + f" ; raison e^(π/m) = {math.exp(math.pi/mv):.4g}")
dit("   Verdict (1) : formules exactes (vide, raccord C1, FL + M² = r²). « Sinusoïdal en ln r » est exact pour L/r, M/r, F/r.")

# ---------------------------------------------------------------- (2) Kerr-Newman
dit("\n(2) KERR-NEWMAN : g^{tt} = −N/(ΔΣ), N = (r² + a²)² − Δ a² sin²θ")
random.seed(20261110)
viol = 0; n = 0
for _ in range(200000):
    a_ = random.uniform(0, 1); q_ = random.uniform(0, 1)
    if a_ * a_ + q_ * q_ > 1:
        continue
    rp = 1 + math.sqrt(1 - a_ * a_ - q_ * q_)
    rr = rp * (1 + 10 ** random.uniform(-8, 3)); th = random.uniform(0, math.pi)
    D = rr * rr - 2 * rr + a_ * a_ + q_ * q_
    N = (rr * rr + a_ * a_) ** 2 - D * a_ * a_ * math.sin(th) ** 2
    n += 1; viol += (N <= 0) or (D <= 0)
dit(f"   cas sous-extrémal (a² + Q² ≤ M²) : {n} tirages (r > r+), violations de N > 0, Δ > 0 : {viol}  → démonstration D4 confirmée")
# cas non couvert : sur-extrémal. Pas d'horizon (Δ > 0 partout) ; g_φφ(équateur) = r² + a² + a²(2Mr − Q²)/r².
def gpp_eq(rr, a_, q_): return rr * rr + a_ * a_ + a_ * a_ * (2 * rr - q_ * q_) / (rr * rr)
for (a_, q_) in ((1.2, 0.0), (0.9, 0.6), (5.0, 0.0), (0.2, 1.1)):
    # zone g_φφ < 0 sur l'équateur : balayage en r (unités M)
    rs = [x / 1000 for x in range(-4000, 4001) if x != 0]
    neg = [x for x in rs if gpp_eq(x, a_, q_) < 0]
    disc = 1 - a_ * a_ - q_ * q_
    dit(f"   a = {a_}, Q = {q_} (a² + Q² − M² = {-disc:+.2f}) : horizon ? {'oui' if disc >= 0 else 'NON (singularité nue)'} ; g_φφ < 0 sur l'équateur pour r ∈ [{min(neg):.3f}, {max(neg):.3f}] M")
dit("   Cas NON couvert par D4 : pour a² + Q² > M² il n'y a pas d'horizon ; la zone g_φφ < 0 (|r| ≲ 2M autour de l'anneau, et r > 0 dès que Q ≠ 0)")
dit("   est alors accessible depuis l'infini et tout l'espace-temps viole la chronologie (Carter 1968). D4 suppose donc implicitement un horizon.")
dit("   La conclusion pratique est sauvée par D3(b) : toute CTC doit passer à ≲ 32 GM/c² (~1e-13 m) de l'anneau ; un véhicule ne le peut pas.")

# ---------------------------------------------------------------- (3) Portée de la borne « 2 g »
dit("\n(3) BORNE Γ − 1 ≤ 2 g L / c² (D2)")
c = 299792458.0; g0 = 9.80665
dit(f"   2 g × 3,7 m / c² = {2*g0*3.7/c**2:.3e} (rapport B : 8,1e-16) — exact pour des observateurs SUIVANT UN CHAMP DE KILLING de genre temps.")
dit("   Hypothèses nécessaires : (i) espace-temps stationnaire ; (ii) véhicule immobile dans ce champ ; (iii) |a| ≤ 2 g sur TOUT le chemin statique")
dit("   reliant le véhicule à la zone de référence (N ≈ 1) ; (iv) potentiel négligeable au-delà de L (sinon ajouter GM/(L c²)).")
# contre-exemple hors hypothèse (ii) : chute libre radiale depuis le repos à l'infini, Schwarzschild : a = 0, dt/dτ = 1/(1 − r_s/r)
for x in (1e-1, 1e-3, 1.3e-10):
    dit(f"   hors hypothèse : chute libre (a ressenti = 0) à r/r_s − 1 = {x:.1e} : dt/dτ = {1/(1-1/(1+x)):.3e} — la borne ne contraint pas un observateur non statique.")
dit("   Non couvert : géométries non stationnaires (le dispositif est décrit comme dynamique). Aucune solution connue n'exploite cette faille à masse modeste (D3 : échelle GM/c²).")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "journaux", "audit_demonstrations_B.txt"), "w", encoding="utf-8").write("\n".join(OUT) + "\n")
