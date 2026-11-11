#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-10 — Expériences d'optique quantique liées à la causalité : gomme quantique à choix retardé,
simulation de courbes temporelles fermées par post-sélection (P-CTC), interrupteur quantique.

Ce script ne « simule » aucun voyage dans le temps. Il montre, à partir du formalisme standard :
  1. que la distribution MARGINALE du photon signal est rigoureusement indépendante de la base
     de mesure choisie (même tardivement) sur le photon témoin : aucun signal vers le passé ;
     les franges n'apparaissent que dans les coïncidences triées APRÈS COUP ;
  2. la visibilité attendue d'une gomme « de table » (pointeur laser, fil, polariseurs) ;
  3. la probabilité de réussite de la post-sélection dans un circuit P-CTC à un qubit,
     P = |Tr U|²/4 : elle s'annule exactement pour le circuit « paradoxal » ;
  4. le principe de l'interrupteur quantique : distinguer [A,B] = 0 de {A,B} = 0 en un seul usage
     de chaque porte ;
  5. un budget de comptage (coïncidences, accidentelles) pour un montage N3.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import sauver, fig_chemin, sci

L, D = [], {}
L.append("EXP-10 — OPTIQUE QUANTIQUE ET CAUSALITÉ : CE QUE LES EXPÉRIENCES MONTRENT VRAIMENT")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. gomme quantique à photons intriqués
# État : |ψ> = Σ_x A(x) [ e^{+iφ(x)/2} |x>|H> + e^{-iφ(x)/2} |x>|V> ] / √2
# (le chemin 1/2 du photon signal est « marqué » par la polarisation H/V du photon témoin)
x = np.linspace(-6e-3, 6e-3, 1201)                 # position du détecteur signal (m)
lam, d_fentes, a_fente, Dist = 702e-9, 0.2e-3, 0.05e-3, 1.0
phi = 2 * np.pi * d_fentes * x / (lam * Dist)
enveloppe = np.sinc(a_fente * x / (lam * Dist))**2
A = np.sqrt(enveloppe / enveloppe.sum())
amp_H = A * np.exp(+1j * phi / 2) / math.sqrt(2)   # amplitude jointe <x, H|ψ>
amp_V = A * np.exp(-1j * phi / 2) / math.sqrt(2)

def jointes(base):
    """Probabilités jointes P(x, résultat du témoin) pour une base de mesure du témoin."""
    if base == "HV":            # garde l'information de chemin
        return {"H": np.abs(amp_H)**2, "V": np.abs(amp_V)**2}
    if base == "DA":            # efface l'information de chemin
        return {"D": np.abs((amp_H + amp_V) / math.sqrt(2))**2, "A": np.abs((amp_H - amp_V) / math.sqrt(2))**2}
    raise ValueError(base)

P_HV, P_DA = jointes("HV"), jointes("DA")
marg_HV = P_HV["H"] + P_HV["V"]
marg_DA = P_DA["D"] + P_DA["A"]
ecart = float(np.max(np.abs(marg_HV - marg_DA)))

def visibilite(p):
    """Visibilité des franges après division par l'enveloppe de diffraction, sur ±2,5 mm (> 1 interfrange)."""
    centre = np.abs(x) < 2.5e-3
    q = p[centre] / (A[centre]**2)
    return float((q.max() - q.min()) / (q.max() + q.min()))

L.append("1. Gomme quantique à paires de photons (schéma de type Walborn et al. 2002 / Kim et al. 2000)")
L.append("   état : (|chemin 1>|H> + |chemin 2>|V>)/√2 ; le témoin est mesuré en base H/V (chemin connu) ou D/A (chemin effacé)")
L.append(f"   écart maximal entre les distributions marginales du signal selon la base du témoin : {ecart:.1e}")
L.append("   → identiques à la précision machine : le choix (même retardé) fait sur le témoin NE CHANGE RIEN à ce que")
L.append("     l'on voit sur le détecteur signal seul. Aucune information ne remonte le temps.")
L.append(f"   visibilité des franges : signal seul {visibilite(marg_HV):.3f} ; coïncidences |H> {visibilite(P_HV['H']):.3f} ; "
         f"coïncidences |D> {visibilite(P_DA['D']):.3f} ; coïncidences |A> {visibilite(P_DA['A']):.3f}")
L.append("   les sous-ensembles D et A portent des franges et des anti-franges complémentaires dont la somme est plate ;")
L.append("   on ne peut les séparer qu'en recevant, par un canal classique ordinaire, le résultat obtenu sur le témoin.")
D["gomme"] = {"ecart_marginales": ecart, "V_signal_seul": visibilite(marg_HV), "V_coinc_D": visibilite(P_DA["D"]),
              "V_coinc_A": visibilite(P_DA["A"]), "V_coinc_H": visibilite(P_HV["H"])}

# tirage Monte-Carlo pour la figure et test statistique
rng = np.random.default_rng(10)
N = 200_000
def tirage(P):
    cles = list(P)
    flat = np.concatenate([P[k] for k in cles])
    idx = rng.choice(flat.size, size=N, p=flat / flat.sum())
    return {k: np.bincount(idx[(idx // x.size) == i] % x.size, minlength=x.size) for i, k in enumerate(cles)}
T_HV, T_DA = tirage(P_HV), tirage(P_DA)
binning = 20
def regroupe(v):
    return v[: (v.size // binning) * binning].reshape(-1, binning).sum(axis=1)
s1, s2 = regroupe(T_HV["H"] + T_HV["V"]), regroupe(T_DA["D"] + T_DA["A"])
ok = (s1 + s2) > 20
chi2 = float(np.sum((s1[ok] - s2[ok])**2 / (s1[ok] + s2[ok])))
ndl = int(ok.sum() - 1)
L.append(f"   Monte-Carlo ILLUSTRATIF ({N} paires par configuration) : χ² entre les deux histogrammes du signal seul = "
         f"{chi2:.1f} pour {ndl} degrés de liberté (compatibles, comme attendu)")
D["gomme"]["chi2"] = chi2
D["gomme"]["ndl"] = ndl
L.append("")

# ---------------------------------------------------------------- 2. gomme de table (optique classique)
L.append("2. Gomme « de table » N1 (pointeur laser, fil fin, films polarisants) — explicable par l'optique ondulatoire")
L.append("   marqueurs de chemin : polariseurs d'axes θ1, θ2 de part et d'autre du fil → visibilité V = |cos(θ1 - θ2)|")
for dth in (0, 30, 45, 60, 90):
    L.append(f"     θ1 - θ2 = {dth:>2}° : V = {abs(math.cos(math.radians(dth))):.2f}")
L.append("   analyseur (« gomme ») à l'angle β derrière des marqueurs croisés : I(x) ∝ ½·[1 + sin(2β)·cos φ(x)]")
for beta in (0, 22.5, 45, -45, 90):
    L.append(f"     β = {beta:>5}° : V = {abs(math.sin(math.radians(2*beta))):.2f}" + ("  (anti-franges)" if beta < 0 else ""))
eps = 0.01
V_res = 2 * math.sqrt(eps) / (1 + eps)
L.append(f"   polariseurs imparfaits (fuite d'intensité ε = {eps:g}) : visibilité résiduelle « marqueurs croisés » ≈ 2√ε/(1+ε) = {V_res:.2f}")
L.append("   Avec un laser (état cohérent), il n'y a rien de spécifiquement quantique : c'est une analogie classique.")
D["gomme_table"] = {"V_residuelle": V_res}
L.append("")

# ---------------------------------------------------------------- 3. P-CTC : post-sélection
# Circuit à un qubit : le qubit sort de la « courbe », subit U, y rentre. Dans le modèle P-CTC (Lloyd et al. 2011),
# l'amplitude de réussite de la post-sélection (projection sur l'état de Bell initial) vaut <Φ|(U⊗1)|Φ> = Tr(U)/2.
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)
I2 = np.eye(2, dtype=complex)
bell = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
def p_postselection(U):
    amp = bell.conj() @ (np.kron(U, I2) @ bell)
    return float(abs(amp)**2)
L.append("3. « Courbe temporelle fermée » simulée par téléportation post-sélectionnée (modèle P-CTC, Lloyd et al. 2011)")
L.append("   un qubit sort de la boucle, subit U(θ) = exp(-iθ·σx/2) (θ = π : il « s'inverse lui-même », circuit paradoxal), y rentre")
L.append("   probabilité que la post-sélection réussisse : P = |Tr U|²/4 = cos²(θ/2)")
D["pctc"] = []
thetas = np.linspace(0, math.pi, 7)
for th in thetas:
    U = math.cos(th / 2) * I2 - 1j * math.sin(th / 2) * X
    p = p_postselection(U)
    D["pctc"].append({"theta_deg": math.degrees(th), "P": p})
    L.append(f"     θ = {math.degrees(th):5.1f}° : P = {p:.3f}")
L.append("   → le cas paradoxal (θ = 180°) a une probabilité exactement nulle : on ne « résout » pas le paradoxe, on")
L.append("     JETTE les essais incohérents. Tous les photons vont vers le futur ; la « boucle » est une probabilité")
L.append("     conditionnelle. Une téléportation ordinaire sans post-sélection exige un message classique (≤ c).")
L.append("     (Calcul de principe ; ce n'est pas une reproduction des données de l'expérience.)")
L.append("")

# ---------------------------------------------------------------- 4. interrupteur quantique
def interrupteur(Aop, Bop, psi):
    """Contrôle en |+> ; ordre A puis B si contrôle 0, B puis A si contrôle 1 ; mesure du contrôle en base ±."""
    plus = (Bop @ Aop + Aop @ Bop) @ psi / 2
    moins = (Bop @ Aop - Aop @ Bop) @ psi / 2
    return float(np.vdot(plus, plus).real), float(np.vdot(moins, moins).real)
psi = np.array([0.6, 0.8j], dtype=complex)
L.append("4. Interrupteur quantique (ordre causal « indéfini » : superposition de A∘B et B∘A pilotée par un qubit)")
D["interrupteur"] = []
for nom, Aop, Bop in (("A = X, B = X (commutent)", X, X), ("A = X, B = Z (anticommutent)", X, Z),
                      ("A = Z, B = Z (commutent)", Z, Z), ("A = Z, B = X (anticommutent)", Z, X)):
    pp, pm = interrupteur(Aop, Bop, psi)
    D["interrupteur"].append({"cas": nom, "P_plus": pp, "P_moins": pm})
    L.append(f"     {nom:<30} P(contrôle = +) = {pp:.2f} ; P(contrôle = -) = {pm:.2f}")
L.append("   → un seul usage de chaque porte suffit à décider « commutent ou anticommutent », ce qu'aucun circuit à ordre")
L.append("     fixe ne fait avec un seul usage de chacune (Chiribella et al. 2013 ; réalisé par Procopio et al. 2015).")
L.append("   Mise en garde : dans ces montages, le photon traverse des composants fixes d'un interféromètre, dans un")
L.append("   espace-temps ordinaire à structure causale parfaitement définie. « Ordre indéfini » qualifie l'ordre des")
L.append("   OPÉRATIONS sur le système, pas l'ordre temporel d'événements ; aucun signal ne précède sa cause.")
L.append("")

# ---------------------------------------------------------------- 5. budget de comptage (N3)
R_s, R_i, eta, tau_c = 2.0e5, 2.0e5, 0.15, 1.0e-9      # simples/s, efficacité d'annonce, fenêtre de coïncidence
R_c = eta * R_s
R_acc = R_s * R_i * tau_c
frac_fente = 0.02                                       # fraction du profil vue par une fente de balayage
par_point = R_c * frac_fente
t_point = 10.0
Npt = par_point * t_point
L.append("5. Budget de comptage indicatif pour une gomme à paires de photons (N3)")
L.append(f"   simples {R_s:.0e} /s par voie, efficacité d'annonce {eta:.0%} → coïncidences vraies {R_c:.0f} /s ; "
         f"accidentelles R1·R2·τ = {R_acc:.0f} /s (fenêtre {tau_c*1e9:.0f} ns) → {R_acc/R_c:.1%}")
L.append(f"   fente de balayage ({frac_fente:.0%} du profil) : {par_point:.0f} coïncidences/s par position ; en {t_point:.0f} s : "
         f"{Npt:.0f} coups → incertitude statistique {1/math.sqrt(Npt):.1%} par point")
L.append(f"   60 positions × 2 bases × {t_point:.0f} s ≈ {60*2*t_point/60:.0f} min d'acquisition (hors alignement : plusieurs jours).")
D["budget"] = {"R_c": R_c, "R_acc": R_acc, "coups_par_point": Npt}

sauver("calc10_optique_quantique_causalite", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8))
xb = x[: (x.size // binning) * binning].reshape(-1, binning).mean(axis=1) * 1e3
ax = axes[0]
ax.step(xb, s1, where="mid", color="#33658a", lw=1.4, label="témoin mesuré en H/V")
ax.step(xb, s2, where="mid", color="#f26419", lw=1.0, label="témoin mesuré en D/A")
ax.set_title("Détecteur signal SEUL : aucune frange,\nquelle que soit la base du témoin", fontsize=10)
ax.set_xlabel("position x (mm)")
ax.set_ylabel("coups")
ax.legend(fontsize=8)
ax.grid(alpha=0.25)
ax = axes[1]
ax.step(xb, regroupe(T_DA["D"]), where="mid", color="#2e8b57", lw=1.3, label="coïncidences avec |D> (franges)")
ax.step(xb, regroupe(T_DA["A"]), where="mid", color="#d1495b", lw=1.3, label="coïncidences avec |A> (anti-franges)")
ax.step(xb, regroupe(T_HV["H"]), where="mid", color="gray", lw=1.0, label="coïncidences avec |H> (pas de franges)")
ax.set_title("Tri APRÈS COUP par le résultat du témoin :\nfranges et anti-franges complémentaires", fontsize=10)
ax.set_xlabel("position x (mm)")
ax.legend(fontsize=7.5)
ax.grid(alpha=0.25)
ax = axes[2]
th = np.linspace(0, 180, 181)
ax.plot(th, np.cos(np.radians(th) / 2)**2, color="#33658a", lw=2)
ax.set_xlabel("angle θ de l'opération U(θ) dans la boucle (°)")
ax.set_ylabel("probabilité de réussite de la post-sélection")
ax.set_title("P-CTC à un qubit : P = cos²(θ/2)\nle cas paradoxal (180°) est simplement rejeté", fontsize=10)
ax.grid(alpha=0.25)
fig.suptitle("EXP-10 — simulation illustrative du formalisme standard (pas une mesure, pas un voyage dans le temps)", fontsize=10)
fig.tight_layout()
fig.savefig(fig_chemin("calc10_gomme_quantique.png"), dpi=150)
print("figure :", fig_chemin("calc10_gomme_quantique.png"))
