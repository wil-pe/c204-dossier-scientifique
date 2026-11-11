# -*- coding: utf-8 -*-
"""S06 — Confinement électromagnétique d'un objet chargé massif (micro-trou noir chargé hypothétique).

Pièges de Penning et de Paul avec pesanteur, stabilité (équations de Mathieu, analyse de Floquet),
champs requis en fonction du rapport Q/M jusqu'à la charge extrémale, trajectoires illustratives.

SIMULATION ILLUSTRATIVE : dynamique classique d'une charge ponctuelle dans des champs idéaux.
Les pièges de Penning et de Paul sont des techniques réelles pour des ions (Q/M ~ 10⁵–10⁸ C/kg) ;
leur extrapolation à Q/M ≤ 8,6×10⁻¹¹ C/kg est purement formelle. Ce n'est pas une preuve
expérimentale.

Exécution :  .venv/bin/python 05_simulations/S06_confinement_em/s06_confinement_em.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import mathieu_a, mathieu_b

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore", over="ignore")
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S06_confinement_em")
col = cc.COULEURS
G, C, G0 = cc.G, cc.C, cc.G0

# ---------------------------------------------------------------------------
# 1. Charge et rapports Q/M
# ---------------------------------------------------------------------------
QM_EXTREMAL = np.sqrt(4 * np.pi * cc.EPS0 * G)             # (Q/M) d'un trou noir extrémal [C/kg]
QM_ELECTRON = cc.E_CHARGE / cc.M_ELECTRON
QM_PROTON = cc.E_CHARGE / cc.M_PROTON
E_CLAQUAGE_AIR = 3e6          # V/m, ordre de grandeur usuel (air sec, pression normale)
E_LIMITE_VIDE = 1e9           # V/m, ordre de grandeur de l'émission de champ sur électrodes [HYP]
B_LABO_CONTINU = 45.0         # T, ordre de grandeur du record en champ continu
B_MAGNETAR = 1e11             # T, ordre de grandeur des magnétars
Q_SCHWINGER = cc.E_SCHWINGER * cc.LAMBDA_COMPTON_E_REDUITE**2 / cc.K_COULOMB   # charge ~ e/α ≈ 137 e : BORNE SUPÉRIEURE d'ordre de grandeur
# Correction n° 43 (Red Team, phase 7) : la charge TYPIQUE d'un micro-trou noir est bien plus faible que cette borne —
# valeur quadratique moyenne ≈ 6,14 e quand GMμ/ħc → 0 (Page 1977, Phys. Rev. D 16, 2402 ; résumé vérifié par la Red Team,
# non relu par nous). On traite donc les deux cas.
Q_TYPIQUE = 6.14 * cc.E_CHARGE


def champ_levitation(qm):
    """Champ électrique vertical compensant le poids : E = g0 / (Q/M) [V/m]."""
    return G0 / qm


def penning_requis(qm, d0=0.05, f=0.1):
    """Piège de Penning d'axe vertical. Affaissement sous la pesanteur ≤ f·d0 → ω_z² ≥ g/(f d0).
    Retourne (V0 [V], B_min [T]) : V0 = ω_z² d0²/(Q/M) ; B_min = sqrt(2) ω_z/(Q/M)."""
    wz2 = G0 / (f * d0)
    return wz2 * d0**2 / qm, np.sqrt(2 * wz2) / qm


def paul_requis(qm, r0=0.05, f=0.1, q=0.4):
    """Piège de Paul (a = 0). Pseudo-potentiel : ω_sec = qΩ/(2√2) ; affaissement g/ω_sec² ≤ f·r0.
    Retourne (V [V], Ω [rad/s]) : V = q r0² Ω²/(4 Q/M)."""
    w_sec2 = G0 / (f * r0)
    Omega = np.sqrt(w_sec2) * 2 * np.sqrt(2) / q
    return q * r0**2 * Omega**2 / (4 * qm), Omega


print("S06 — tests de validation")
val.verifier("(Q/M) extrémal = sqrt(4πε₀G) (dossier : 8,62e-11 C/kg)", QM_EXTREMAL, 8.62e-11, tol_rel=1e-3)
val.verifier("Charge critique de Schwinger à l'échelle de Compton ≈ e/α (137 e)", Q_SCHWINGER / cc.E_CHARGE, 137.036, tol_rel=1e-3)
# Équilibre de Majumdar-Papapetrou : deux masses extrémales de même signe → force nulle
M_t = 1e12
F_grav = G * M_t**2 / 0.3**2
F_coul = cc.K_COULOMB * (QM_EXTREMAL * M_t)**2 / 0.3**2
val.verifier("Deux masses extrémales de même signe : Coulomb = gravitation (Majumdar-Papapetrou)", F_coul / F_grav, 1.0, tol_rel=1e-12)

# ---------------------------------------------------------------------------
# 2. Piège de Penning avec pesanteur (unités réduites : temps 1/ω_z, longueur d0)
# ---------------------------------------------------------------------------
# Potentiel quadrupolaire Φ = (V0/2d0²)(z² − ρ²/2), champ B uniforme selon z, accélération a.
#   x'' = x/2 + β y' + γ_x ;  y'' = y/2 − β x' + γ_y ;  z'' = −z + γ_z
# β = ω_c/ω_z ; γ = a/(ω_z² d0). Stabilité radiale : β² > 2.


def penning_rhs(t, s, beta, gam):
    x, y, z, vx, vy, vz = s
    return [vx, vy, vz, 0.5 * x + beta * vy + gam[0], 0.5 * y - beta * vx + gam[1], -z + gam[2]]


def penning_energie(s, gam):
    x, y, z, vx, vy, vz = s
    return 0.5 * (vx**2 + vy**2 + vz**2) + 0.5 * (z**2 - 0.5 * (x**2 + y**2)) - gam[0] * x - gam[1] * y - gam[2] * z


def integrer_penning(beta, gam, s0, t_max, n=40000):
    sol = solve_ivp(penning_rhs, (0, t_max), s0, args=(beta, gam), method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
    t = np.linspace(0, t_max, n)
    return t, sol.sol(t)


def frequence_dominante(t, sig, fmin=0.0, fmax=np.inf):
    """Pulsation du pic dominant du spectre (FFT avec fenêtre de Hann + interpolation parabolique)."""
    sig = sig - np.mean(sig)
    spec = np.abs(np.fft.rfft(sig * np.hanning(len(sig))))
    w = 2 * np.pi * np.fft.rfftfreq(len(sig), d=t[1] - t[0])
    masque = (w > fmin) & (w < fmax)
    i = np.argmax(np.where(masque, spec, 0))
    a_, b_, c_ = np.log(spec[i - 1]), np.log(spec[i]), np.log(spec[i + 1])
    return w[i] + 0.5 * (a_ - c_) / (a_ - 2 * b_ + c_) * (w[1] - w[0])


beta = 3.0
gam_axial = np.array([0.0, 0.0, -0.1])           # pesanteur selon −z, affaissement attendu : 0,1 d0
w_plus = 0.5 * (beta + np.sqrt(beta**2 - 2))
w_moins = 0.5 * (beta - np.sqrt(beta**2 - 2))
# Durée d'intégration = nombre ENTIER de périodes axiales (64) : les moyennes temporelles ne sont
# alors pas biaisées et le pic axial tombe sur un canal de la FFT. (Première version : T = 400/ω_z,
# moyennes sur un nombre non entier de périodes → 3 tests en échec marginal, biais de 2e-4 à 5e-3
# dus à la méthode de mesure et non à la dynamique ; corrigé ici, voir README.)
T_PEN = 64 * 2 * np.pi
t, s = integrer_penning(beta, gam_axial, [0.15, 0.0, 0.0, 0.0, 0.1, 0.0], T_PEN)
En = penning_energie(s, gam_axial)
TOL_SPECTRE = 0.05 * 2 * np.pi / T_PEN        # précision de l'estimateur spectral : ~5 % du pas de fréquence
val.verifier("Penning : conservation de l'énergie (dérive relative)", np.max(np.abs(En - En[0])) / abs(En[0]), 0.0, tol_abs=1e-8)
val.verifier("Penning : position d'équilibre axiale z_eq = γ_z (affaissement g/ω_z²)", np.mean(s[2][:-1]), gam_axial[2], tol_rel=1e-3)
val.verifier("Penning : pulsation axiale = ω_z", frequence_dominante(t, s[2], 0.5, 1.5), 1.0, tol_abs=TOL_SPECTRE)
val.verifier("Penning : pulsation cyclotron modifiée ω₊", frequence_dominante(t, s[0], 1.5, 5.0), w_plus, tol_abs=TOL_SPECTRE)
val.verifier("Penning : pulsation magnétron ω₋", frequence_dominante(t, s[0], 0.05, 1.0), w_moins, tol_abs=TOL_SPECTRE)
val.verifier("Théorème d'invariance : ω₊² + ω₋² + ω_z² = ω_c² (Brown & Gabrielse 1986)", w_plus**2 + w_moins**2 + 1.0, beta**2, tol_rel=1e-12)
# Accélération latérale (freinage du véhicule) : centre de l'orbite déplacé en x_eq = −2γ_x
gam_lat = np.array([0.08, 0.0, -0.1])
t2, s2 = integrer_penning(beta, gam_lat, [0.15, 0.0, 0.0, 0.0, 0.1, 0.0], T_PEN)
m_mag = t2 < 11 * 2 * np.pi / w_moins          # moyenne sur 11 périodes magnétron entières
val.verifier("Penning : centre de l'orbite sous accélération latérale x_eq = −2γ_x", np.mean(s2[0][m_mag]), -2 * gam_lat[0], tol_rel=0.02)
# Cas instable β² < 2 : croissance exponentielle de taux Im(ω) = sqrt(2 − β²)/2
beta_i = 1.2
t3, s3 = integrer_penning(beta_i, gam_axial, [0.01, 0.0, 0.0, 0.0, 0.0, 0.0], 30.0)
rho3 = np.hypot(s3[0], s3[1])
taux_num = np.polyfit(t3[t3 > 15], np.log(rho3[t3 > 15]), 1)[0]
val.verifier("Penning instable (β = 1,2) : taux de croissance = sqrt(2 − β²)/2", taux_num, np.sqrt(2 - beta_i**2) / 2, tol_rel=1e-3)

# ---------------------------------------------------------------------------
# 3. Piège de Paul : équation de Mathieu u'' + (a − 2q cos 2ξ) u = 0, analyse de Floquet
# ---------------------------------------------------------------------------


def trace_monodromie(a, q, n=400):
    """Trace de la matrice de monodromie sur une période π (RK4 vectorisé). Stable ⇔ |trace| < 2."""
    a = np.asarray(a, float)
    q = np.asarray(q, float)
    h = np.pi / n
    y = np.stack([np.ones_like(a + q), np.zeros_like(a + q), np.zeros_like(a + q), np.ones_like(a + q)])  # (u1, u1', u2, u2')

    def f(xi, y):
        k = -(a - 2 * q * np.cos(2 * xi))
        return np.stack([y[1], k * y[0], y[3], k * y[2]])

    xi = 0.0
    for _ in range(n):
        k1 = f(xi, y)
        k2 = f(xi + h / 2, y + h / 2 * k1)
        k3 = f(xi + h / 2, y + h / 2 * k2)
        k4 = f(xi + h, y + h * k3)
        y = y + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xi += h
    return y[0] + y[3]


# Validation : frontières de la première zone de stabilité ↔ valeurs caractéristiques a0(q), b1(q)
q_max_num = brentq(lambda q: trace_monodromie(0.0, q, 2000) + 2.0, 0.5, 1.2, xtol=1e-10)
q_max_ref = brentq(lambda q: mathieu_b(1, q), 0.5, 1.2, xtol=1e-12)
val.verifier("Mathieu : q_max à a = 0 (Floquet numérique) ↔ zéro de b₁(q) (scipy) ≈ 0,908", q_max_num, q_max_ref, tol_rel=1e-6)
val.verifier("Mathieu : q_max ≈ 0,908046 (valeur tabulée)", q_max_num, 0.908046, tol_rel=1e-5)
for q_t in (0.3, 0.6):
    a_bas = brentq(lambda a: trace_monodromie(a, q_t, 2000) - 2.0, -0.6, 0.0, xtol=1e-11)
    val.verifier(f"Mathieu : frontière inférieure a₀(q = {q_t}) (Floquet ↔ scipy.special.mathieu_a)", a_bas, mathieu_a(0, q_t), tol_abs=1e-7)
    a_haut = brentq(lambda a: trace_monodromie(a, q_t, 2000) + 2.0, 0.0, 1.0, xtol=1e-11)
    val.verifier(f"Mathieu : frontière supérieure b₁(q = {q_t}) (Floquet ↔ scipy.special.mathieu_b)", a_haut, mathieu_b(1, q_t), tol_abs=1e-7)


def paul_rhs(xi, s, a, q, gam):
    """z'' + (a − 2q cos 2ξ) z = −γ ; γ = 4g/(Ω² r0) (pesanteur réduite)."""
    return [s[1], -(a - 2 * q * np.cos(2 * xi)) * s[0] - gam]


q_st, gam_p = 0.3, 0.004
beta_floquet = np.arccos(trace_monodromie(0.0, q_st, 2000) / 2) / np.pi      # exposant caractéristique β
sol = solve_ivp(paul_rhs, (0, 600.0), [0.05, 0.0], args=(0.0, q_st, gam_p), method="DOP853", rtol=1e-11, atol=1e-13, dense_output=True)
xi_p = np.linspace(0, 600.0, 60000)
z_p = sol.sol(xi_p)[0]
w_sec_num = frequence_dominante(xi_p, z_p, 0.05, 0.6)
val.verifier("Paul : pulsation séculaire numérique ↔ exposant de Floquet β (en unités de ξ)", w_sec_num, beta_floquet, tol_rel=1e-3)
val.verifier("Paul : β ↔ approximation de Dehmelt q/√2 (q = 0,3)", beta_floquet, q_st / np.sqrt(2), tol_rel=0.05,
             commentaire="approximation valable pour q ≲ 0,4")
val.verifier("Paul : affaissement moyen sous pesanteur ↔ pseudo-potentiel −γ/β²", np.mean(z_p), -gam_p / beta_floquet**2, tol_rel=0.05)
sol_i = solve_ivp(paul_rhs, (0, 40.0), [0.05, 0.0], args=(0.0, 0.95, gam_p), method="DOP853", rtol=1e-10, atol=1e-12, dense_output=True)
xi_i = np.linspace(0, 40.0, 4000)
z_i = sol_i.sol(xi_i)[0]

# ---------------------------------------------------------------------------
# 4. Champs requis en fonction de Q/M et de la masse
# ---------------------------------------------------------------------------
qm = np.logspace(-30, 12, 500)
V_pen, B_pen = penning_requis(qm)
V_paul, Om_paul = paul_requis(qm)
M_hyp = {"113 kg (demi-unité)": cc.REVENDICATIONS["masse_unite_kg"] / 2, "1e9 kg": 1e9, "1,5e11 kg": G0 / G, "1e12 kg": 1e12, "4,4e12 kg": 4.4e12}
bilan_masses = {}
for nom, M in M_hyp.items():
    Q_ext = QM_EXTREMAL * M
    Q_air = E_CLAQUAGE_AIR * 1.0**2 / cc.K_COULOMB           # charge max. telle que E(1 m) < claquage de l'air
    r_schw = np.sqrt(cc.K_COULOMB * Q_ext / cc.E_SCHWINGER)  # rayon où E dépasse le champ de Schwinger (charge extrémale)
    lignes = {}
    for cle, Q in (("charge_extremale", Q_ext), ("charge_limitee_claquage_air_a_1m", min(Q_air, Q_ext)),
                   ("charge_borne_superieure_schwinger_137e", min(Q_SCHWINGER, Q_ext)), ("charge_typique_6e_page_1977", min(Q_TYPIQUE, Q_ext))):
        qm_ = Q / M
        Vp, Bp = penning_requis(qm_)
        Vq, Oq = paul_requis(qm_)
        lignes[cle] = {"Q_C": Q, "Q_en_e": Q / cc.E_CHARGE, "Q_sur_M_C_kg": qm_, "E_levitation_V_m": champ_levitation(qm_),
                       "E_levitation_sur_E_Schwinger": champ_levitation(qm_) / cc.E_SCHWINGER,
                       "Penning_V0_V": Vp, "Penning_B_min_T": Bp, "Paul_V_V": Vq, "Paul_Omega_rad_s": Oq,
                       "champ_propre_a_1m_V_m": cc.K_COULOMB * Q / 1.0**2}
    bilan_masses[nom] = {"M_kg": M, "poids_N": M * G0, "poids_en_tonnes_force": M * G0 / (1000 * G0),
                         "rayon_champ_superieur_Schwinger_charge_extremale_m": r_schw,
                         "rayon_claquage_air_charge_extremale_m": np.sqrt(cc.K_COULOMB * Q_ext / E_CLAQUAGE_AIR),
                         "moment_magnetique_max_A_m2": Q_ext * G * M / C,              # μ = Q a c, a = GM/c² (g = 2)
                         "gradient_B_pour_levitation_dipolaire_T_m": M * G0 / (Q_ext * G * M / C),
                         **lignes}

charge_utile_camion_N = 1.0e4      # ordre de grandeur de la charge utile d'un pick-up (~1 t) [HYP]
reaction = {
    "principe": "le piège transmet au véhicule l'intégralité du poids M·g (troisième loi de Newton) : léviter une masse ne l'allège pas",
    "poids_1e12_kg_N": 1e12 * G0,
    "rapport_au_poids_supportable_par_un_pick_up": 1e12 * G0 / charge_utile_camion_N,
    "pression_sur_0p1_m2_Pa": 1e12 * G0 / 0.1,
}

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
# --- Figure 1 : champs requis vs Q/M ---------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 6.2))
ax1.loglog(qm, champ_levitation(qm), color="k", lw=2, label="champ de lévitation E = g₀/(Q/M)")
for y, nom, c in ((E_CLAQUAGE_AIR, "claquage de l'air (~3×10⁶ V/m)", col["orange"]), (E_LIMITE_VIDE, "émission de champ sous vide (~10⁹ V/m) [HYP]", col["vert"]),
                  (cc.E_SCHWINGER, "champ critique de Schwinger (1,3×10¹⁸ V/m)", col["rouge"])):
    ax1.axhline(y, color=c, ls="--", lw=1.4)
    ax1.text(2e-30, y * 2.5, nom, color=c, fontsize=8.5)
reps = (("électron", QM_ELECTRON, col["bleu"]), ("proton", QM_PROTON, col["ciel"]),
        ("trou noir extrémal\n(toute masse)", QM_EXTREMAL, col["rouge"]),
        ("10¹² kg, Q ≤ 137 e (borne) ;\ntypique ≈ 6 e : 22 fois plus haut", Q_SCHWINGER / 1e12, col["violet"]),
        ("113 kg, Q ≤ 137 e (borne)", Q_SCHWINGER / (cc.REVENDICATIONS["masse_unite_kg"] / 2), col["orange"]))
for nom, x, c in reps:
    ax1.plot(x, champ_levitation(x), "o", color=c, ms=7)
    ax1.annotate(nom, (x, champ_levitation(x)), textcoords="offset points", xytext=(8, 6), fontsize=8.5, color=c)
ax1.axvspan(qm[0], QM_EXTREMAL, color=col["gris"], alpha=0.12)
ax1.text(1e-22, 3e-9, "domaine accessible à un trou noir :\nQ/M ≤ 8,6×10⁻¹¹ C/kg", fontsize=8.5, color=col["gris"])
ax1.set_ylim(1e-13, 1e35)
ax1.set_xlabel("rapport charge/masse Q/M [C/kg]")
ax1.set_ylabel("champ électrique de lévitation [V/m]")
ax1.set_title("(a) Compenser le poids par un champ électrique", fontsize=10)
ax1.legend(fontsize=8.5, loc="upper right")

ax2.loglog(qm, B_pen, color=col["bleu"], lw=2, label="Penning : champ magnétique minimal $B_{min}$ [T]")
ax2.loglog(qm, V_pen, color=col["vert"], lw=2, label="Penning : tension $V_0$ [V]")
ax2.loglog(qm, V_paul, color=col["rouge"], lw=2, ls="--", label="Paul (q = 0,4) : amplitude RF V [V]")
ax2.axhline(B_LABO_CONTINU, color=col["bleu"], ls=":", lw=1.3)
ax2.text(2e-30, B_LABO_CONTINU * 2.5, "champ continu de laboratoire (~45 T)", color=col["bleu"], fontsize=8.5)
ax2.axhline(B_MAGNETAR, color=col["violet"], ls=":", lw=1.3)
ax2.text(2e-30, B_MAGNETAR * 2.5, "magnétar (~10¹¹ T)", color=col["violet"], fontsize=8.5)
ax2.axvline(QM_EXTREMAL, color=col["rouge"], lw=1.3)
Vp_e, Bp_e = penning_requis(QM_EXTREMAL)
ax2.plot(QM_EXTREMAL, Bp_e, "o", color=col["bleu"])
ax2.annotate(f"extrémal :\n$B_{{min}}$ = {cc.sci(Bp_e, 2)} T\n$V_0$ = {cc.sci(Vp_e, 2)} V", (QM_EXTREMAL, Bp_e), textcoords="offset points", xytext=(10, 5), fontsize=8.5)
ax2.set_xlabel("rapport charge/masse Q/M [C/kg]")
ax2.set_ylabel("champ magnétique [T] ou tension [V]")
ax2.set_title("(b) Pièges dimensionnés pour un affaissement ≤ 10 % ($d_0$ = $r_0$ = 5 cm)", fontsize=10)
ax2.legend(fontsize=8.5, loc="upper right")
cc.titre(fig, "S06 — Champs requis pour faire léviter et piéger un objet chargé en fonction de Q/M, jusqu'à la charge extrémale")
cc.sauver_figure(fig, FIG / "S06_fig1_champs_requis.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : Penning --------------------------------------------------------------------------
fig, axes = plt.subplots(1, 4, figsize=(18.5, 5.2))
ax = axes[0]
m = t < 120
ax.plot(s[0][m], s[1][m], color=col["bleu"], lw=0.7, label="pesanteur axiale seule")
ax.plot(s2[0][m], s2[1][m], color=col["orange"], lw=0.7, label="+ accélération latérale (γₓ = 0,08)")
ax.plot(0, 0, "+", color="k", ms=10)
ax.plot(-2 * gam_lat[0], 0, "x", color=col["rouge"], ms=8)
ax.set_aspect("equal")
ax.set_xlabel("x / d₀")
ax.set_ylabel("y / d₀")
ax.set_title("(a) Plan radial, β = ω_c/ω_z = 3 (stable)", fontsize=9.5)
ax.legend(fontsize=7.5, loc="upper right")
ax = axes[1]
ax.plot(t[t < 60], s[2][t < 60], color=col["vert"], lw=1.2)
ax.axhline(gam_axial[2], color="k", ls="--", lw=1)
ax.text(1, gam_axial[2] + 0.012, "équilibre déplacé : z = −g/ω_z²", fontsize=8.5)
ax.set_xlabel("temps [1/ω_z]")
ax.set_ylabel("z / d₀")
ax.set_title("(b) Mouvement axial avec pesanteur", fontsize=9.5)
ax = axes[2]
spec = np.abs(np.fft.rfft((s[0] - s[0].mean()) * np.hanning(len(t))))
wax = 2 * np.pi * np.fft.rfftfreq(len(t), d=t[1] - t[0])
ax.semilogy(wax, spec / spec.max(), color=col["bleu"], lw=1, label="spectre de x(t)")
specz = np.abs(np.fft.rfft((s[2] - s[2].mean()) * np.hanning(len(t))))
ax.semilogy(wax, specz / specz.max(), color=col["vert"], lw=1, label="spectre de z(t)")
for w_, nom in ((w_moins, "ω₋"), (1.0, "ω_z"), (w_plus, "ω₊")):
    ax.axvline(w_, color=col["rouge"], ls=":", lw=1)
    ax.text(w_ + 0.03, 0.3, nom, color=col["rouge"], fontsize=9)
ax.set_xlim(0, 4)
ax.set_ylim(1e-8, 2)
ax.set_xlabel("pulsation [ω_z]")
ax.set_ylabel("amplitude spectrale normalisée")
ax.set_title("(c) Les trois modes propres (traits : théorie)", fontsize=9.5)
ax.legend(fontsize=7.5, loc="lower right")
ax = axes[3]
ax.semilogy(t3, rho3, color=col["rouge"], lw=1.5, label="β = 1,2 < √2 : instable")
ax.semilogy(t3, 0.004 * np.exp(np.sqrt(2 - beta_i**2) / 2 * t3), color="k", ls="--", lw=1, label="taux théorique sqrt(2 − β²)/2")
ax.set_xlabel("temps [1/ω_z]")
ax.set_ylabel("ρ / d₀")
ax.set_title("(d) Champ B trop faible : fuite radiale", fontsize=9.5)
ax.legend(fontsize=7.5)
cc.titre(fig, "S06 — Piège de Penning avec pesanteur (unités réduites) : trajectoires, modes propres et instabilité")
cc.sauver_figure(fig, FIG / "S06_fig2_penning.png", rect=(0, 0.04, 1, 0.9))

# --- Figure 3 : Mathieu / Paul ---------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.8))
qg = np.linspace(0, 1.5, 451)
ag = np.linspace(-0.8, 0.5, 391)
QG, AG = np.meshgrid(qg, ag)
tr_z = trace_monodromie(AG, QG, 300)
tr_r = trace_monodromie(-AG / 2, -QG / 2, 300)
stable_z = np.abs(tr_z) < 2
stable_r = np.abs(tr_r) < 2
zone = stable_z.astype(int) + 2 * stable_r.astype(int)
cmap = plt.matplotlib.colors.ListedColormap(["#ffffff", "#a6cee3", "#fdbf6f", "#33a02c"])
ax = axes[0]
ax.pcolormesh(QG, AG, zone, cmap=cmap, vmin=-0.5, vmax=3.5, shading="auto")
qq = np.linspace(1e-4, 1.5, 300)
ax.plot(qq, mathieu_a(0, qq), color="k", lw=1.3, ls="--", label="a₀(q), b₁(q) (scipy.special)")
ax.plot(qq, mathieu_b(1, qq), color="k", lw=1.3, ls="--")
ax.plot(q_max_num, 0, "o", color=col["rouge"])
ax.annotate(f"$q_{{max}}$ = {q_max_num:.4f}".replace(".", ","), (q_max_num, 0), textcoords="offset points", xytext=(8, 8), fontsize=9, color=col["rouge"])
ax.set_xlim(0, 1.5)
ax.set_ylim(-0.8, 0.5)
ax.set_xlabel("$q_z = 4QV/(M r_0^2 \\Omega^2)$")
ax.set_ylabel("$a_z = -8QU/(M r_0^2 \\Omega^2)$")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc="#33a02c", label="stable en z ET en r (piégeage 3D)"), Patch(fc="#a6cee3", label="stable en z seulement"),
                   Patch(fc="#fdbf6f", label="stable en r seulement"), plt.Line2D([], [], color="k", ls="--", label="a₀(q), b₁(q) (scipy.special)")],
          fontsize=7.8, loc="lower left")
ax.set_title("(a) Diagramme de stabilité (analyse de Floquet numérique)", fontsize=10)
ax.grid(False)
ax = axes[1]
m = xi_p < 150
ax.plot(xi_p[m], z_p[m], color=col["bleu"], lw=0.9, label=f"q = {q_st} (stable) + pesanteur".replace(".", ","))
ax.axhline(-gam_p / beta_floquet**2, color="k", ls="--", lw=1)
ax.text(2, -gam_p / beta_floquet**2 - 0.02, "affaissement moyen −γ/β² (pseudo-potentiel)", fontsize=8.5, va="top")
ax.set_xlabel("ξ = Ωt/2")
ax.set_ylabel("z / r₀")
ax.set_title("(b) Trajectoire stable : mouvement séculaire + micromouvement", fontsize=10)
ax.legend(fontsize=8.5, loc="upper right")
ax = axes[2]
ax.semilogy(xi_i, np.abs(z_i) + 1e-6, color=col["rouge"], lw=1.2, label="q = 0,95 > $q_{max}$ : instable")
ax.axhline(1.0, color="k", ls="--", lw=1)
ax.text(1, 1.3, "électrode (z = r₀)", fontsize=8.5)
ax.set_xlabel("ξ = Ωt/2")
ax.set_ylabel("|z| / r₀")
ax.set_title("(c) Hors de la zone de stabilité : éjection exponentielle", fontsize=10)
ax.legend(fontsize=8.5, loc="lower right")
cc.titre(fig, "S06 — Piège de Paul avec pesanteur : stabilité de Mathieu et trajectoires illustratives")
cc.sauver_figure(fig, FIG / "S06_fig3_paul_mathieu.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 4 : limites de charge vs masse ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.8))
Ms = np.logspace(1, 14, 300)
Q_ext_s = QM_EXTREMAL * Ms
Q_air_s = np.minimum(E_CLAQUAGE_AIR / cc.K_COULOMB, Q_ext_s)
Q_sch_s = np.minimum(Q_SCHWINGER, Q_ext_s)
Q_typ_s = np.minimum(Q_TYPIQUE, Q_ext_s)
ax1.loglog(Ms, Q_ext_s, color=col["rouge"], lw=2, label="charge extrémale $Q = M\\sqrt{4\\pi\\varepsilon_0 G}$")
ax1.loglog(Ms, Q_air_s, color=col["orange"], lw=2, ls="--", label="charge telle que E(1 m) < claquage de l'air")
ax1.loglog(Ms, Q_sch_s, color=col["violet"], lw=2, ls=":", label="borne supérieure ≈ 137 e (champ < Schwinger à l'échelle de Compton)")
ax1.loglog(Ms, Q_typ_s, color=col["bleu"], lw=2, ls="-.", label="charge typique ≈ 6 e (valeur quadratique moyenne, Page 1977)")
ax1.axhline(cc.E_CHARGE, color=col["gris"], lw=1)
ax1.text(20, cc.E_CHARGE * 2, "charge élémentaire e", color=col["gris"], fontsize=8.5)
ax1.set_xlabel("masse M [kg]")
ax1.set_ylabel("charge [C]")
ax1.set_title("(a) Charge qu'un micro-trou noir pourrait porter", fontsize=10)
ax1.legend(fontsize=8.3, loc="upper left")
ax2.loglog(Ms, champ_levitation(Q_ext_s / Ms), color=col["rouge"], lw=2, label="avec la charge extrémale")
ax2.loglog(Ms, champ_levitation(Q_air_s / Ms), color=col["orange"], lw=2, ls="--", label="avec la charge limitée par l'air")
ax2.loglog(Ms, champ_levitation(Q_sch_s / Ms), color=col["violet"], lw=2, ls=":", label="avec Q ≈ 137 e (borne supérieure)")
ax2.loglog(Ms, champ_levitation(Q_typ_s / Ms), color=col["bleu"], lw=2, ls="-.", label="avec Q ≈ 6 e (typique)")
ax2.axhline(cc.E_SCHWINGER, color="k", ls="--", lw=1.2)
ax2.text(20, cc.E_SCHWINGER * 3, "champ de Schwinger", fontsize=8.5)
ax2.axhline(E_LIMITE_VIDE, color=col["vert"], ls="--", lw=1.2)
ax2.text(20, E_LIMITE_VIDE * 3, "~10⁹ V/m (limite pratique sous vide) [HYP]", color=col["vert"], fontsize=8.5)
for Mv in (cc.REVENDICATIONS["masse_unite_kg"] / 2, 1e12):
    ax2.axvline(Mv, color=col["bleu"], ls=":", lw=1)
ax2.set_xlabel("masse M [kg]")
ax2.set_ylabel("champ électrique de lévitation requis [V/m]")
ax2.set_title("(b) Champ de lévitation correspondant", fontsize=10)
ax2.legend(fontsize=8.3, loc="center right")
cc.titre(fig, "S06 — Charge soutenable par un micro-trou noir et champ de lévitation requis, en fonction de la masse")
cc.sauver_figure(fig, FIG / "S06_fig4_limites_de_charge.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S06_confinement_em",
    "avertissement": cc.MENTION,
    "Q_sur_M": {"extremal_C_kg": QM_EXTREMAL, "electron_C_kg": QM_ELECTRON, "proton_C_kg": QM_PROTON,
                "rapport_proton_sur_extremal": QM_PROTON / QM_EXTREMAL},
    "champ_levitation_charge_extremale_V_m": champ_levitation(QM_EXTREMAL),
    "charge_critique_schwinger_C": Q_SCHWINGER, "charge_critique_schwinger_en_e": Q_SCHWINGER / cc.E_CHARGE,
    "charge_typique_C": Q_TYPIQUE, "charge_typique_en_e": Q_TYPIQUE / cc.E_CHARGE,
    "note_charge": "≈ 137 e est une borne supérieure d'ordre de grandeur ; la valeur typique est ≈ 6 e (valeur quadratique moyenne, Page 1977)",
    "champ_schwinger_V_m": cc.E_SCHWINGER,
    "penning_extremal_d0_5cm_affaissement_10pct": {"V0_V": Vp_e, "B_min_T": Bp_e, "B_min_sur_magnetar": Bp_e / B_MAGNETAR},
    "paul_extremal_r0_5cm_q0p4": {"V_V": paul_requis(QM_EXTREMAL)[0], "Omega_rad_s": paul_requis(QM_EXTREMAL)[1]},
    "penning_adimensionnel": {"beta": beta, "omega_plus": w_plus, "omega_moins": w_moins, "condition_stabilite": "β² = (ω_c/ω_z)² > 2"},
    "mathieu": {"q_max_a0": q_max_num, "beta_floquet_q0p3": beta_floquet, "approximation_dehmelt_q0p3": q_st / np.sqrt(2)},
    "bilan_par_masse": bilan_masses,
    "reaction_sur_le_vehicule": reaction,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S06_resultats.json", resultats)
val.imprimer_bilan()
print("S06 terminé.")
