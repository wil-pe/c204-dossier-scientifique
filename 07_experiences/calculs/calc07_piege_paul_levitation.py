#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-07 — Confinement d'objets chargés : piège de Paul basse fréquence pour grains chargés,
selle tournante (analogue mécanique sans haute tension) et lévitation diamagnétique.

Calcule :
  1. le diagramme de stabilité de l'équation de Mathieu  x'' + (a - 2q cos 2ξ) x = 0
     par la matrice de monodromie (théorie de Floquet), avec et sans amortissement ;
  2. les paramètres d'un piège annulaire à 50 Hz pour des grains (spores de lycopode) ;
  3. les prescriptions de sécurité chiffrées (limitation de courant, charge et énergie stockées) ;
  4. la condition de lévitation diamagnétique  B·dB/dz = µ0·ρ·g/|χ| ;
  5. ce qu'exigerait le « logement » d'un trou noir chargé de 1e12 kg (affirmation NON tenue pour vraie).

Convention (piège annulaire 3D, r0² = 2 z0²) : q_z = 4QV/(m r0² Ω²), a_z = -8QU/(m r0² Ω²).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from constantes import (G, c, eps0, mu0, g0, e_ch, m_e, C204, CHARGE_TENABLE_E, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-07 — PIÈGE DE PAUL, SELLE TOURNANTE, LÉVITATION DIAMAGNÉTIQUE")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. stabilité de Mathieu
def monodromie(a, q, b=0.0, n=400):
    """Matrice de monodromie sur une période π de  x'' + 2b x' + (a - 2q cos 2ξ) x = 0 (RK4)."""
    def f(xi, y):
        return np.array([y[1], -2 * b * y[1] - (a - 2 * q * math.cos(2 * xi)) * y[0]])
    M = np.zeros((2, 2))
    hpas = math.pi / n
    for j, y0 in enumerate(((1.0, 0.0), (0.0, 1.0))):
        y = np.array(y0)
        xi = 0.0
        for _ in range(n):
            k1 = f(xi, y)
            k2 = f(xi + hpas / 2, y + hpas / 2 * k1)
            k3 = f(xi + hpas / 2, y + hpas / 2 * k2)
            k4 = f(xi + hpas, y + hpas * k3)
            y = y + hpas / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            xi += hpas
        M[:, j] = y
    return M

def stable(a, q, b=0.0, n=400):
    vp = np.linalg.eigvals(monodromie(a, q, b, n))
    return np.max(np.abs(vp)) <= 1.0 + 1e-6

# limite de stabilité pour a = 0 : balayage croissant (première sortie de la zone stable), puis dichotomie
def q_limite(b=0.0, q_fin=40.0, pas=0.02):
    q = 0.5
    while q < q_fin and stable(0.0, q, b, n=200):
        q += pas
    if q >= q_fin:
        return float("nan")
    lo, hi = q - pas, q
    for _ in range(25):
        mid = 0.5 * (lo + hi)
        if stable(0.0, mid, b):
            lo = mid
        else:
            hi = mid
    return lo

q0 = q_limite(0.0)
L.append("1. Équation de Mathieu  x'' + 2b·x' + (a - 2q·cos 2ξ)·x = 0, ξ = Ωt/2")
L.append(f"   limite de stabilité à a = 0, sans amortissement : q_max = {q0:.4f} (valeur tabulée : 0,908)")
D["q_max"] = {"b=0": q0}
for b in (0.2, 0.5, 1.0, 2.0, 2.3):
    qb = q_limite(b)
    D["q_max"][f"b={b}"] = qb
    L.append(f"   avec amortissement b = {b:<3} (b = 1/(Ω·τ), frottement de Stokes dans l'air) : q_max = {qb:.3f}")
L.append("   → dans l'air, le frottement élargit fortement la zone stable : c'est ce qui rend la démonstration facile.")
L.append("")

# ---------------------------------------------------------------- 2. piège à 50 Hz pour grains
f_res = 50.0
Om = 2 * math.pi * f_res
r0 = 0.005
V = 2000.0
a_grain, rho_grain = 15e-6, 500.0                 # spore de lycopode (Ø ≈ 30 µm, creuse)
m_grain = 4 / 3 * math.pi * a_grain**3 * rho_grain
eta_air = 1.8e-5
tau = m_grain / (6 * math.pi * eta_air * a_grain)
b_amort = 1.0 / (Om * tau)
L.append("2. Piège annulaire à 50 Hz pour grains chargés (ordres de grandeur pour un TP encadré)")
L.append(f"   anneau r0 = {r0*1000:.0f} mm, amplitude V = {V:.0f} V, Ω = 2π·{f_res:.0f} Hz")
L.append(f"   grain : rayon {a_grain*1e6:.0f} µm, masse {sci(m_grain)} kg ; temps de relaxation de Stokes τ = {tau*1e3:.2f} ms → b = 1/(Ωτ) = {b_amort:.2f}")
L.append("   Dans l'air, la force pondéromotrice moyenne est réduite du facteur 1/(1+b²) (micromouvement amorti et déphasé) :")
L.append(f"   ici 1/(1+b²) = {1/(1+b_amort**2):.2f} ; l'affaissement sous le poids vaut alors g·(1+b²)/ω_sec² (approximation q ≲ 0,4).")
L.append(f"   {'Q/m (C/kg)':>12} | {'charges e':>10} | {'q_z':>6} | {'stable (vide)':>13} | {'stable (air)':>12} | {'affaissement vide':>17} | {'affaissement air':>16} | {'E pour compenser g':>18}")
D["piege"] = []
for Qm in (2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 3e-3):
    q = 4 * Qm * V / (r0**2 * Om**2)
    st0 = stable(0.0, q, 0.0)
    st1 = stable(0.0, q, b_amort)
    if q < 0.9:
        w_sec = q * Om / (2 * math.sqrt(2))
        aff0 = g0 / w_sec**2
        aff1 = aff0 * (1 + b_amort**2)
        t0, t1 = f"{aff0*1000:.1f} mm", f"{aff1*1000:.1f} mm"
    else:
        aff0 = aff1 = float("nan")
        t0, t1 = "—", "(hors approx.)"
    E_comp = g0 / Qm
    D["piege"].append({"Q_sur_m": Qm, "q": q, "stable_vide": bool(st0), "stable_air": bool(st1),
                       "affaissement_vide_m": aff0, "affaissement_air_m": aff1, "E_compensation_V_m": E_comp})
    L.append(f"   {Qm:>12.0e} | {Qm*m_grain/e_ch:>10.0f} | {q:>6.3f} | {'oui' if st0 else 'non':>13} | {'oui' if st1 else 'non':>12} | "
             f"{t0:>17} | {t1:>16} | {E_comp:>12.2e} V/m")
L.append(f"   L'affaissement dépasse vite r0 = {r0*1000:.0f} mm : en pratique on compense le poids par un champ continu vertical")
L.append("   E = g/(Q/m) (10⁴–10⁵ V/m, soit quelques centaines de volts sur 1 cm) ou l'on travaille à q plus élevé,")
L.append("   ce que l'amortissement de l'air autorise (zone stable élargie).")
L.append("")

# ---------------------------------------------------------------- 3. sécurité chiffrée
L.append("3. Sécurité haute tension — dimensionnement À COURANT LIMITÉ (prescriptions, pas un plan de montage)")
V_crete = 3000.0
I_max = 0.5e-3
R_min = V_crete / I_max
C_elec = 10e-12
Q_stock = C_elec * V_crete
E_stock = 0.5 * C_elec * V_crete**2
L.append(f"   tension crête visée ≤ {V_crete:.0f} V ; courant de court-circuit admis ≤ {I_max*1e3:.1f} mA (seuil de perception en alternatif)")
L.append(f"   → résistance série totale ≥ V/I = {R_min/1e6:.0f} MΩ, répartie sur ≥ 2 résistances haute tension en série (tolérance à une panne)")
L.append(f"   capacité des électrodes ~{C_elec*1e12:.0f} pF : charge stockée {Q_stock*1e9:.0f} nC, énergie {E_stock*1e6:.0f} µJ")
L.append("   repères de sécurité usuels (famille CEI 61010, à vérifier dans l'édition en vigueur) : parties accessibles")
L.append("   limitées à ~0,5 mA efficace en régime normal, charge < 45 µC, énergie stockée < 350 mJ.")
L.append(f"   → marges : charge ×{45e-6/Q_stock:.0f}, énergie ×{0.35/E_stock:.0f} sous les repères.")
L.append("   INTERDIT hors laboratoire : transformateur d'enseigne au néon, four à micro-ondes, bobine d'allumage ou")
L.append("   toute source capable de débiter > 1 mA sous haute tension. Niveau N1 : PAS de haute tension — utiliser")
L.append("   la selle tournante et la lévitation diamagnétique ; le piège électrique relève d'un TP encadré (N2) avec")
L.append("   alimentation de TP certifiée à courant limité, capot isolant et interverrouillage.")
D["securite"] = {"R_min_ohm": R_min, "Q_stock_C": Q_stock, "E_stock_J": E_stock}
L.append("")

# ---------------------------------------------------------------- 3bis. selle tournante
# Potentiel U = (m g/(2 R_c))(x² - y²) tournant à Ω. Dans le repère tournant :
#   x'' - 2Ω y' - Ω² x = -ω0² x ;  y'' + 2Ω x' - Ω² y = +ω0² y,  ω0² = g/R_c
#   → λ⁴ + 2Ω²λ² + Ω⁴ - ω0⁴ = 0 → λ² = -Ω² ± ω0² : stable si Ω > ω0 (équivalent « q = ω0²/(2Ω²) < 1/2 »).
Rc = 0.30                                    # rayon de courbure de la selle (m)
w0 = math.sqrt(g0 / Rc)
L.append("3bis. Selle tournante (analogue mécanique, sans haute tension) — point matériel sur z = (x² - y²)/(2R_c)")
L.append(f"   rayon de courbure R_c = {Rc*100:.0f} cm → ω0 = √(g/R_c) = {w0:.2f} rad/s")
L.append(f"   repère tournant : λ² = -Ω² ± ω0² → l'origine est stable si Ω > ω0, soit > {w0/(2*math.pi)*60:.0f} tr/min")
L.append("   (paramètre équivalent q = ω0²/(2Ω²) < 1/2 ; pour une bille qui ROULE, le seuil est modifié par le moment")
L.append("    d'inertie et le frottement finit par l'éjecter lentement : Thompson, Harmon & Ball 2002 ; à mesurer.)")
D["selle"] = {"omega0": w0, "seuil_tr_min": w0 / (2 * math.pi) * 60}
L.append("")

# ---------------------------------------------------------------- 4. lévitation diamagnétique
L.append("4. Lévitation diamagnétique : condition  B·dB/dz = µ0·ρ·g/|χ|")
MAT = [("graphite pyrolytique (χ⊥ ≈ -4,5e-4)", -4.5e-4, 2200.0), ("bismuth (χ ≈ -1,66e-4)", -1.66e-4, 9780.0),
       ("eau / tissus vivants (χ ≈ -9,05e-6)", -9.05e-6, 1000.0)]
D["diamagnetisme"] = []
for nom, chi, ro in MAT:
    BgradB = mu0 * ro * g0 / abs(chi)
    D["diamagnetisme"].append({"materiau": nom, "B_gradB_T2_m": BgradB})
    L.append(f"   {nom:<40} B·dB/dz ≥ {BgradB:7.0f} T²/m")
L.append("   aimants NdFeB en damier, près de la surface : B ≈ 0,4 T et dB/dz ≈ 150–300 T/m → 60–120 T²/m :")
L.append("   suffisant pour le graphite pyrolytique (N1, ~20 €), pas pour l'eau (≈ 1400 T²/m : aimant de Bitter de ~16 T,")
L.append("   expérience de la grenouille, Berry & Geim 1997).")
L.append("   Théorème d'Earnshaw : pas d'équilibre stable statique pour des charges ou des aimants permanents seuls ;")
L.append("   les trois échappatoires réelles sont le champ oscillant (Paul), le diamagnétisme et la rétroaction.")
L.append("")

# ---------------------------------------------------------------- 5. « logement d'une singularité chargée »
# Masse : 4,4e12 kg (valeur centrale retenue, 3,9–5,1e12 kg par singularité, erratum E2).
# Le rapport Q/m extrémal, √(4πε0G), ne dépend pas de la masse : champ de sustentation et tension de piège inchangés.
L.append("5. Lien C204 : que demanderait le confinement d'un trou noir chargé ? (affirmation NON tenue pour vraie)")
M = C204["masse_TN_centrale_kg"]
Qmax = M * math.sqrt(4 * math.pi * eps0 * G)
Qm_tn = Qmax / M
E_sust = g0 / Qm_tn
r0_tn = 0.10
V_paul = 0.4 * r0_tn**2 * Om**2 / (4 * Qm_tn)
L.append(f"   trou noir de {M:.1e} kg (valeur retenue ; ancienne valeur 1e12 kg → 86 C), charge extrémale "
         f"Q_max = M·√(4πε0G) = {Qmax:.0f} C → Q/m = {sci(Qm_tn)} C/kg (indépendant de M)")
L.append(f"   (électron : {e_ch/m_e:.2e} C/kg ; grain de poussière piégé : ~1e-4 C/kg → {1e-4/Qm_tn:.0e} fois plus « léger par charge »)")
L.append(f"   champ électrique pour porter son poids (Mg = {M*g0:.1e} N) : E = g/(Q/m) = {sci(E_sust)} V/m")
L.append("   (rigidité diélectrique de l'air 3e6 V/m ; émission de champ des métaux ~1e9–1e10 V/m)")
L.append(f"   piège de Paul à 50 Hz, r0 = 10 cm, q = 0,4 : V = q·r0²·Ω²/(4·Q/m) = {sci(V_paul)} V")
B_levit = M * g0 / (Qmax * 1.0)
L.append(f"   force magnétique Q·v·B : nulle au repos ; même à v = 1 m/s il faudrait B = Mg/(Qv) = {sci(B_levit)} T")
D["c204"] = {"M_kg": M, "Q_max_C": Qmax, "Q_sur_m": Qm_tn, "E_sustentation_V_m": E_sust, "V_paul_V": V_paul,
             "B_levitation_T": B_levit, "charge_tenable": []}
L.append("   Charge réellement tenable par un micro-trou noir (erratum E14 : ≈ 6 e en valeur quadratique moyenne ; borne ≈ 137 e) :")
for n_e in CHARGE_TENABLE_E:
    Q = n_e * e_ch
    for Mx in C204["masse_TN_kg"]:
        E_t = Mx * g0 / Q
        D["c204"]["charge_tenable"].append({"n_e": n_e, "M_kg": Mx, "Q_sur_m": Q / Mx, "E_sustentation_V_m": E_t})
        L.append(f"     {n_e:>5.0f} e, M = {Mx:.1e} kg : Q/m = {sci(Q/Mx)} C/kg ; champ de sustentation {sci(E_t)} V/m")
L.append("   → le confinement électromagnétique est hors de portée de 5 à 12 ordres de grandeur dans le cas extrémal")
L.append("     (le plus favorable, lui-même intenable), et de plus de 20 ordres de grandeur avec la charge tenable ;")
L.append("     piéger une poussière de 1e-11 kg ne démontre rien sur le « logement magnétique d'une singularité ».")

sauver("calc07_piege_paul_levitation", D, L)

# ---------------------------------------------------------------- figure : diagramme de stabilité + trajectoire
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.3))
ax = axes[0]
qs = np.linspace(0.0, 1.6, 81)
as_ = np.linspace(-0.8, 0.4, 61)
for b, cmap, alpha in ((0.0, "Blues", 0.9), (0.5, "Oranges", 0.45)):
    Z = np.array([[1.0 if stable(a, q, b) else np.nan for q in qs] for a in as_])
    ax.pcolormesh(qs, as_, Z, cmap=cmap, vmin=0, vmax=1.6, alpha=alpha, shading="auto")
ax.plot([], [], color="#2b6cb0", lw=6, label="stable, sans amortissement (b = 0)")
ax.plot([], [], color="#f6ad55", lw=6, label="stable, air (b = 0,5)")
ax.axhline(0, color="k", lw=0.6)
ax.axvline(0.908, color="k", ls=":", lw=1)
ax.text(0.92, 0.3, "q = 0,908", fontsize=8)
ax.set_xlabel("q")
ax.set_ylabel("a")
ax.set_title("Première zone de stabilité de Mathieu (un axe)\ncalcul numérique illustratif (Floquet)", fontsize=10)
ax.legend(fontsize=8, loc="lower left")

ax = axes[1]
def traj(q, b, n_per=40):
    sol = solve_ivp(lambda xi, y: [y[1], -2 * b * y[1] - (-2 * q * math.cos(2 * xi)) * y[0]],
                    [0, n_per * math.pi], [1.0, 0.0], max_step=0.02, rtol=1e-8)
    return sol.t / math.pi, sol.y[0]
for q, b, col, lab in ((0.3, 0.0, "#33658a", "q = 0,3 ; b = 0 : confiné (mouvement séculaire + micromouvement)"),
                       (0.3, 0.1, "#2e8b57", "q = 0,3 ; b = 0,1 : confiné et amorti"),
                       (1.0, 0.0, "#d1495b", "q = 1,0 ; b = 0 : instable (éjecté)")):
    t, x = traj(q, b, 24 if q > 0.9 else 40)
    hors = np.where(np.abs(x) > 6)[0]
    if hors.size:                       # trajectoire instable : on arrête le tracé à la sortie du cadre
        t, x = t[: hors[0] + 1], x[: hors[0] + 1]
    ax.plot(t, np.clip(x, -6, 6), color=col, lw=1.3, label=lab)
ax.set_ylim(-6, 6)
ax.set_xlabel("temps (périodes du champ)")
ax.set_ylabel("position (unités arbitraires)")
ax.set_title("Trajectoires dans un piège de Paul (a = 0)\nsimulation illustrative", fontsize=10)
ax.legend(fontsize=7.5, loc="upper left")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc07_mathieu.png"), dpi=150)
print("figure :", fig_chemin("calc07_mathieu.png"))
