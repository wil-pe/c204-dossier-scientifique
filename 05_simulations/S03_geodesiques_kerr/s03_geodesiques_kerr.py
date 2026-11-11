# -*- coding: utf-8 -*-
"""S03 — Géodésiques dans l'espace-temps de Kerr : orbites équatoriales et quasi polaires,
traversée des horizons et passage par l'anneau vers l'extension r < 0, temps propre et temps
coordonnée.

SIMULATION ILLUSTRATIVE : intégration numérique de géodésiques d'une solution exacte (Kerr
éternel, maximalement étendu). L'extension r < 0 se situe derrière l'horizon de Cauchy r = r-,
réputé instable ; rien n'indique qu'elle existe pour un trou noir réel, et rien ici ne constitue
une preuve expérimentale.

Deux intégrateurs indépendants :
  (A) équation des géodésiques du second ordre en coordonnées de Boyer-Lindquist (BL), où E, L_z,
      la norme et la constante de Carter ne sont PAS imposées : leur conservation est un test ;
  (B) équations séparées du second ordre en temps de Mino λ (dτ = Σ dλ), régulières à travers les
      horizons et le disque r = 0 ; angles et temps « entrants » de Kerr (réguliers à l'horizon).

Unités : G = c = 1, M = 1 (longueurs en GM/c², temps en GM/c³).
Exécution :  .venv/bin/python 05_simulations/S03_geodesiques_kerr/s03_geodesiques_kerr.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp, quad, cumulative_trapezoid
from scipy.optimize import fsolve, brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore")
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S03_geodesiques_kerr")
col = cc.COULEURS
M = 1.0

# ---------------------------------------------------------------------------
# 1. Métrique de Kerr et dérivées (générées par calcul formel pour éviter toute erreur de recopie)
# ---------------------------------------------------------------------------
_r, _th, _a = sp.symbols("r theta a", real=True)
_S = _r**2 + _a**2 * sp.cos(_th)**2
_D = _r**2 - 2 * _r + _a**2
_comps = [-(1 - 2 * _r / _S),                                                   # g_tt
          -2 * _a * _r * sp.sin(_th)**2 / _S,                                   # g_tφ
          sp.sin(_th)**2 * ((_r**2 + _a**2)**2 - _D * _a**2 * sp.sin(_th)**2) / _S,  # g_φφ
          _S / _D,                                                              # g_rr
          _S]                                                                   # g_θθ
_f_metrique = sp.lambdify((_r, _th, _a), _comps + [sp.diff(c, _r) for c in _comps] + [sp.diff(c, _th) for c in _comps],
                          "numpy", cse=True)


def metrique(r, th, a):
    return _f_metrique(r, th, a)[:5]


def second_membre_bl(tau, y, a):
    """Équation des géodésiques  d/dτ(g_νβ u^β) = ½ ∂_ν g_αβ u^α u^β  en coordonnées BL.

    État y = (t, r, θ, φ, u^t, u^r, u^θ, u^φ) ; paramètre affine τ (temps propre si μ = 1)."""
    t, r, th, ph, ut, ur, uh, up = y
    (gtt, gtp, gpp, grr, ghh, gtt_r, gtp_r, gpp_r, grr_r, ghh_r,
     gtt_h, gtp_h, gpp_h, grr_h, ghh_h) = _f_metrique(r, th, a)
    dgtt = ur * gtt_r + uh * gtt_h
    dgtp = ur * gtp_r + uh * gtp_h
    dgpp = ur * gpp_r + uh * gpp_h
    dgrr = ur * grr_r + uh * grr_h
    dghh = ur * ghh_r + uh * ghh_h
    T_t = dgtt * ut + dgtp * up
    T_p = dgtp * ut + dgpp * up
    q_r = gtt_r * ut**2 + 2 * gtp_r * ut * up + gpp_r * up**2 + grr_r * ur**2 + ghh_r * uh**2
    q_h = gtt_h * ut**2 + 2 * gtp_h * ut * up + gpp_h * up**2 + grr_h * ur**2 + ghh_h * uh**2
    T_r = dgrr * ur - 0.5 * q_r
    T_h = dghh * uh - 0.5 * q_h
    det = gtt * gpp - gtp**2
    return [ut, ur, uh, up,
            -(gpp * T_t - gtp * T_p) / det,
            -T_r / grr,
            -T_h / ghh,
            -(-gtp * T_t + gtt * T_p) / det]


def constantes_du_mouvement(y, a):
    """(E, L_z, norme g_μν u^μ u^ν, constante de Carter Q) le long d'une solution y(τ)."""
    t, r, th, ph, ut, ur, uh, up = y
    gtt, gtp, gpp, grr, ghh = metrique(r, th, a)
    E = -(gtt * ut + gtp * up)
    L = gtp * ut + gpp * up
    norme = gtt * ut**2 + 2 * gtp * ut * up + gpp * up**2 + grr * ur**2 + ghh * uh**2
    mu2 = -norme
    Qc = (ghh * uh)**2 + np.cos(th)**2 * (a**2 * (mu2 - E**2) + L**2 / np.sin(th)**2)
    return E, L, norme, Qc


def R_radial(r, E, L, Qc, a, mu2=1.0):
    P = (r**2 + a**2) * E - a * L
    return P**2 - (r**2 - 2 * r + a**2) * (mu2 * r**2 + (L - a * E)**2 + Qc)


def dR_radial(r, E, L, Qc, a, mu2=1.0):
    P = (r**2 + a**2) * E - a * L
    K = (L - a * E)**2 + Qc
    D = r**2 - 2 * r + a**2
    return 4 * r * E * P - (2 * r - 2) * (mu2 * r**2 + K) - D * 2 * mu2 * r


def Theta_polaire(th, E, L, Qc, a, mu2=1.0):
    c2 = np.cos(th)**2
    terme_L = L**2 / np.sin(th)**2 if L != 0 else 0.0
    return Qc - c2 * (a**2 * (mu2 - E**2) + terme_L)


def dTheta_polaire(th, E, L, Qc, a, mu2=1.0):
    terme_L = 2 * L**2 * np.cos(th) / np.sin(th)**3 if L != 0 else 0.0
    return 2 * np.sin(th) * np.cos(th) * a**2 * (mu2 - E**2) + terme_L


def conditions_initiales(E, L, Qc, r0, th0, a, signe_r=-1, signe_th=+1, mu2=1.0):
    """4-vitesse initiale déduite des intégrales premières (E, L_z, Q)."""
    S = r0**2 + a**2 * np.cos(th0)**2
    D = r0**2 - 2 * r0 + a**2
    P = (r0**2 + a**2) * E - a * L
    Rv = max(R_radial(r0, E, L, Qc, a, mu2), 0.0)
    Tv = max(Theta_polaire(th0, E, L, Qc, a, mu2), 0.0)
    ut = (a * (L - a * E * np.sin(th0)**2) + (r0**2 + a**2) * P / D) / S
    up = ((L / np.sin(th0)**2 if L != 0 else 0.0) - a * E + a * P / D) / S
    return [0.0, r0, th0, 0.0, ut, signe_r * np.sqrt(Rv) / S, signe_th * np.sqrt(Tv) / S, up]


def integrer_bl(y0, a, tau_max, evenements=None, rtol=1e-11, atol=1e-13, n=4000):
    sol = solve_ivp(second_membre_bl, (0, tau_max), y0, args=(a,), method="DOP853", rtol=rtol, atol=atol,
                    events=evenements, dense_output=True)
    tau = np.linspace(0, sol.t[-1], n)
    return tau, sol.sol(tau), sol


# Orbites circulaires équatoriales (Bardeen, Press & Teukolsky 1972), sens prograde
def orbite_circulaire(r, a):
    d = np.sqrt(r**1.5 - 3 * np.sqrt(r) + 2 * a)
    E = (r**1.5 - 2 * np.sqrt(r) + a) / (r**0.75 * d)
    L = (r**2 - 2 * a * np.sqrt(r) + a**2) / (r**0.75 * d)
    Om = 1.0 / (r**1.5 + a)
    return E, L, Om


def r_isco(a):
    z1 = 1 + (1 - a**2)**(1 / 3) * ((1 + a)**(1 / 3) + (1 - a)**(1 / 3))
    z2 = np.sqrt(3 * a**2 + z1**2)
    return 3 + z2 - np.sqrt((3 - z1) * (3 + z1 + 2 * z2))


def horizons(a):
    return 1 + np.sqrt(1 - a**2), 1 - np.sqrt(1 - a**2)


def derive_relative(x):
    x = np.asarray(x)
    ref = max(abs(x[0]), 1e-12)
    return float(np.max(np.abs(x - x[0])) / ref)


# ---------------------------------------------------------------------------
# 2. Partie A — orbites liées (extérieur de l'horizon), intégrateur BL
# ---------------------------------------------------------------------------
print("S03 — partie A : orbites en coordonnées de Boyer-Lindquist")
A_KERR = 0.9
RP, RM = horizons(A_KERR)
orbites = {}

# A1/A2 : orbites équatoriales excentriques prograde et rétrograde (périastre 4 M / 8 M, apoastre 12 M)
for nom, r_p, r_a, sens in (("équatoriale prograde", 4.0, 12.0, +1), ("équatoriale rétrograde", 8.0, 12.0, -1)):
    E0, L0 = fsolve(lambda v: [R_radial(r_p, v[0], v[1], 0.0, A_KERR), R_radial(r_a, v[0], v[1], 0.0, A_KERR)],
                    [0.95, sens * 3.5], xtol=1e-13)
    y0 = conditions_initiales(E0, L0, 0.0, r_a, np.pi / 2, A_KERR)
    y0[5] = 0.0   # départ à l'apoastre : u^r = 0
    tau, y, sol = integrer_bl(y0, A_KERR, 1500.0)
    E, L, norme, Qc = constantes_du_mouvement(y, A_KERR)
    orbites[nom] = {"tau": tau, "y": y, "E": E0, "L": L0, "Q": 0.0,
                    "derives": {"E": derive_relative(E), "L": derive_relative(L),
                                "norme": float(np.max(np.abs(norme + 1))), "Q_abs": float(np.max(np.abs(Qc)))}}
    val.verifier(f"Conservation de E ({nom}), dérive relative", derive_relative(E), 0.0, tol_abs=1e-8)
    val.verifier(f"Conservation de L_z ({nom}), dérive relative", derive_relative(L), 0.0, tol_abs=1e-8)
    val.verifier(f"Conservation de g(u,u) = −1 ({nom})", np.max(np.abs(norme + 1)), 0.0, tol_abs=1e-8)
    val.verifier(f"Constante de Carter Q = 0 conservée ({nom})", np.max(np.abs(Qc)), 0.0, tol_abs=1e-8)

# A3 : orbite quasi polaire (L_z petit) entre 6 M et 10 M
L_pol = 0.15
E0, Q0 = fsolve(lambda v: [R_radial(6.0, v[0], L_pol, v[1], A_KERR), R_radial(10.0, v[0], L_pol, v[1], A_KERR)],
                [0.94, 12.0], xtol=1e-13)
y0 = conditions_initiales(E0, L_pol, Q0, 10.0, np.pi / 2, A_KERR)
y0[5] = 0.0
tau, y, sol = integrer_bl(y0, A_KERR, 2500.0, n=8000)
E, L, norme, Qc = constantes_du_mouvement(y, A_KERR)
orbites["quasi polaire"] = {"tau": tau, "y": y, "E": E0, "L": L_pol, "Q": Q0,
                            "derives": {"E": derive_relative(E), "L": derive_relative(L),
                                        "norme": float(np.max(np.abs(norme + 1))), "Q": derive_relative(Qc)}}
val.verifier("Conservation de E (quasi polaire)", derive_relative(E), 0.0, tol_abs=1e-8)
val.verifier("Conservation de L_z (quasi polaire)", derive_relative(L), 0.0, tol_abs=1e-7)
val.verifier("Conservation de la constante de Carter (quasi polaire), dérive relative", derive_relative(Qc), 0.0, tol_abs=1e-8)
theta_min_pol = float(np.degrees(np.min(y[2])))

# --- Tests de validation contre des résultats analytiques ---------------------------------
# V2 : avance du périastre en Schwarzschild (a = 0), formule exacte par quadrature
p_s, e_s = 50.0, 0.3
rp_s, ra_s = p_s / (1 + e_s), p_s / (1 - e_s)
E_s = np.sqrt(((p_s - 2)**2 - 4 * e_s**2) / (p_s * (p_s - 3 - e_s**2)))
L_s = p_s / np.sqrt(p_s - 3 - e_s**2)
val.verifier("Schwarzschild : R(r_p) = 0 avec (E, L) analytiques", R_radial(rp_s, E_s, L_s, 0.0, 0.0), 0.0, tol_abs=1e-9)
y0 = conditions_initiales(E_s, L_s, 0.0, ra_s, np.pi / 2, 0.0)
y0[5] = 0.0
ev_apo = lambda tau, y, a: y[5]          # u^r = 0, sens décroissant → passage à l'apoastre
ev_apo.direction = -1
sol = solve_ivp(second_membre_bl, (0, 20000.0), y0, args=(0.0,), method="DOP853", rtol=1e-12, atol=1e-14, events=ev_apo)
phi_apo = sol.y_events[0][:, 3]
avance_num = float(np.mean(np.diff(np.concatenate([[0.0], phi_apo]))[1:4]) - 2 * np.pi)
avance_exacte = quad(lambda chi: (1 - (2 / p_s) * (3 + e_s * np.cos(chi)))**-0.5, 0, 2 * np.pi, epsabs=1e-13)[0] - 2 * np.pi
val.verifier("Schwarzschild : avance du périastre par orbite (p = 50 M, e = 0,3) ↔ quadrature exacte",
             avance_num, avance_exacte, tol_rel=1e-7)
val.verifier("… et ↔ formule d'Einstein au premier ordre 6πM/p", avance_num, 6 * np.pi / p_s, tol_rel=0.12,
             commentaire="écart attendu d'ordre M/p (terme du second ordre)")

# V3 : orbite circulaire prograde r = 8 M (a = 0,9) : r constant et Ω = 1/(r^{3/2} + a)
Ec, Lc, Omc = orbite_circulaire(8.0, A_KERR)
y0 = conditions_initiales(Ec, Lc, 0.0, 8.0, np.pi / 2, A_KERR)
y0[5] = 0.0
tau, y, sol = integrer_bl(y0, A_KERR, 800.0)
val.verifier("Orbite circulaire r = 8 M : dérive de r", np.max(np.abs(y[1] - 8.0)), 0.0, tol_abs=1e-7)
val.verifier("Orbite circulaire : dφ/dt = 1/(r^{3/2} + a) (Bardeen et al. 1972)", (y[3][-1] - y[3][0]) / (y[0][-1] - y[0][0]), Omc, tol_rel=1e-9)

# V4 : ISCO — R, R' et R'' s'annulent
for a_, attendu in ((0.0, 6.0), (0.9, 2.320883), (1.0 - 1e-9, 1.0)):
    val.verifier(f"r_ISCO(a = {a_:.3g})", r_isco(a_), attendu, tol_abs=2e-3 if a_ > 0.99 else 1e-5)
ri = r_isco(A_KERR)
Ei, Li, _ = orbite_circulaire(ri, A_KERR)
h = 1e-4
d2R = (R_radial(ri + h, Ei, Li, 0, A_KERR) - 2 * R_radial(ri, Ei, Li, 0, A_KERR) + R_radial(ri - h, Ei, Li, 0, A_KERR)) / h**2
val.verifier("ISCO (a = 0,9) : R = 0", R_radial(ri, Ei, Li, 0, A_KERR), 0.0, tol_abs=1e-10)
val.verifier("ISCO (a = 0,9) : R' = 0", dR_radial(ri, Ei, Li, 0, A_KERR), 0.0, tol_abs=1e-9)
val.verifier("ISCO (a = 0,9) : R'' = 0 (stabilité marginale)", d2R, 0.0, tol_abs=1e-4)

# V5 : chute radiale en Schwarzschild depuis le repos à l'infini : τ(10M → 3M) analytique
y0 = conditions_initiales(1.0, 0.0, 0.0, 10.0, np.pi / 2, 0.0)
ev_r3 = lambda tau, y, a: y[1] - 3.0
ev_r3.terminal = True
sol = solve_ivp(second_membre_bl, (0, 200.0), y0, args=(0.0,), method="DOP853", rtol=1e-12, atol=1e-14, events=ev_r3)
val.verifier("Schwarzschild : temps propre de chute 10M → 3M = (2/3)(r0^{3/2} − r1^{3/2})/√(2M)",
             sol.t_events[0][0], (2 / 3) * (10**1.5 - 3**1.5) / np.sqrt(2), tol_rel=1e-9)

# V6 : précession nodale de Lense-Thirring d'une orbite sphérique inclinée lointaine (r = 500 M).
#      (Une orbite exactement polaire, L_z = 0, passe par θ = 0 où les coordonnées BL sont
#      singulières : l'intégrateur du second ordre y renvoie NaN — divergence de coordonnées
#      documentée dans le README ; on prend donc une inclinaison de ~60°.)
r_lt, L_lt = 500.0, 11.0
E0, Q0 = fsolve(lambda v: [R_radial(r_lt, v[0], L_lt, v[1], A_KERR), dR_radial(r_lt, v[0], L_lt, v[1], A_KERR)], [0.999, r_lt - L_lt**2], xtol=1e-13)
y0 = conditions_initiales(E0, L_lt, Q0, r_lt, np.pi / 2, A_KERR, signe_th=-1)
y0[5] = 0.0
ev_eq = lambda tau, y, a: y[2] - np.pi / 2     # passages à l'équateur (nœud ascendant : θ décroissant)
ev_eq.direction = -1
sol = solve_ivp(second_membre_bl, (0, 6.5 * 2 * np.pi * r_lt**1.5), y0[:2] + [y0[2] - 1e-9] + y0[3:], args=(A_KERR,),
                method="DOP853", rtol=1e-12, atol=1e-14, events=ev_eq)
phi_noeuds = sol.y_events[0][:, 3]
prec_num = float(np.mean(np.diff(phi_noeuds)) - 2 * np.pi)
prec_lt = 4 * np.pi * A_KERR / r_lt**1.5
inclinaison_lt = float(np.degrees(np.arccos(L_lt / np.sqrt(L_lt**2 + Q0))))
val.verifier(f"Précession nodale par orbite (r = 500 M, i ≈ {inclinaison_lt:.0f}°) ↔ Lense-Thirring 4πa(M/r)^(3/2)",
             prec_num, prec_lt, tol_rel=0.03, commentaire="champ faible : corrections relatives d'ordre M/r et a²/r^(1/2)")

# ---------------------------------------------------------------------------
# 3. Partie B — temps de Mino : traversée des horizons et de l'anneau (r < 0)
# ---------------------------------------------------------------------------
print("S03 — partie B : temps de Mino, traversée des horizons et passage vers r < 0")


def second_membre_mino(lam, y, E, L, Qc, a, mu2):
    """État y = (r, r', θ, θ', φ̃, t̃, τ) ; ' = d/dλ ; dτ = Σ dλ.

    r'' = ½ dR/dr ;  θ'' = ½ dΘ/dθ  (réguliers partout, y compris en Δ = 0 et en r ≤ 0).
    φ̃ et t̃ sont l'angle et le temps « entrants » (Kerr-Schild) : dφ̃ = dφ + (a/Δ) dr,
    dt̃ = dt + (2Mr/Δ) dr, réguliers à travers les horizons futurs pour un mouvement entrant."""
    r, vr, th, vth, _, _, _ = y
    D = r**2 - 2 * r + a**2
    P = (r**2 + a**2) * E - a * L
    K = (L - a * E)**2 + Qc
    # W = (P + r')/Δ, écrit sous une forme régulière en Δ = 0 quand P − r' ne s'annule pas
    W = (mu2 * r**2 + K) / (P - vr) if abs(P - vr) > abs(D) else (P + vr) / D
    s2 = np.sin(th)**2
    dphi = a * W - a * E + (L / s2 if L != 0 else 0.0)
    dt = a * (L - a * E * s2) + P + 2 * r * W
    return [vr, 0.5 * dR_radial(r, E, L, Qc, a, mu2), vth, 0.5 * dTheta_polaire(th, E, L, Qc, a, mu2),
            dphi, dt, r**2 + a**2 * np.cos(th)**2]


def integrer_mino(E, L, Qc, r0, th0, a, lam_max=60.0, mu2=1.0, r_sortie=-25.0):
    R0 = R_radial(r0, E, L, Qc, a, mu2)
    T0 = Theta_polaire(th0, E, L, Qc, a, mu2)
    y0 = [r0, -np.sqrt(max(R0, 0.0)), th0, np.sqrt(max(T0, 0.0)), 0.0, 0.0, 0.0]
    rp, rm = horizons(a)

    def ev_sortie(lam, y, *args):       # fuite vers r → −∞
        return y[0] - r_sortie
    ev_sortie.terminal = True

    def ev_singularite(lam, y, *args):  # voisinage de l'anneau Σ = 0
        return y[0]**2 + a**2 * np.cos(y[2])**2 - 1e-5
    ev_singularite.terminal = True

    def ev_retour(lam, y, *args):       # retour vers l'horizon interne par l'intérieur (mouvement sortant)
        return (y[0] - (rm - 1e-3)) if y[1] > 0 else -1.0
    ev_retour.terminal = True
    ev_retour.direction = 1

    def ev_fuite_ext(lam, y, *args):    # ressort vers l'extérieur (ne se produit pas pour les cas étudiés)
        return y[0] - (r0 + 1.0)
    ev_fuite_ext.terminal = True

    sol = solve_ivp(second_membre_mino, (0, lam_max), y0, args=(E, L, Qc, a, mu2), method="DOP853", rtol=1e-12, atol=1e-14,
                    events=[ev_sortie, ev_singularite, ev_retour, ev_fuite_ext], dense_output=True, max_step=0.02)
    fin = ["fuite vers r → −∞ (autre région asymptotique)", "atteint la singularité annulaire",
           "rebond en r < 0 puis retour vers l'horizon interne (sortie vers un autre feuillet)", "ressort", "durée max."]
    cause = next((fin[i] for i in range(4) if len(sol.t_events[i])), fin[4])
    lam = np.linspace(0, sol.t[-1], 6000)
    y = sol.sol(lam)
    inv_r = y[1]**2 - R_radial(y[0], E, L, Qc, a, mu2)
    inv_th = y[3]**2 - Theta_polaire(y[2], E, L, Qc, a, mu2)
    echelle = max(R0, 1.0)
    return {"lam": lam, "y": y, "cause": cause, "inv_r": float(np.max(np.abs(inv_r)) / echelle),
            "inv_th": float(np.max(np.abs(inv_th)) / max(abs(Qc), 1.0)), "E": E, "L": L, "Q": Qc, "a": a,
            "r_min": float(np.min(y[0])), "tau_total": float(y[6][-1])}


a_B = 0.9
rpB, rmB = horizons(a_B)
E_seuil_axe = np.sqrt(1 + 1 / a_B)        # sur l'axe : traversée complète ssi E² > 1 + M/a
passages = {}
# Sur l'axe (θ = 0, L = 0) : Q = −a²(E² − 1) pour que Θ ≡ 0
for nom, E_ in (("axe, E = 1,2 (rebond en r < 0)", 1.2), ("axe, E = 1,6 (traversée complète)", 1.6)):
    passages[nom] = integrer_mino(E_, 0.0, -a_B**2 * (E_**2 - 1), 10.0, 0.0, a_B)
# Hors axe : orbite « vorticale » (Q < 0), spirale autour de l'axe et traverse le disque
E_v, L_v = 1.6, 0.05
Q_v = -0.9 * a_B**2 * (E_v**2 - 1)
_thg = np.linspace(1e-3, np.pi / 2 - 1e-3, 40001)
_Tg = np.array([Theta_polaire(t_, E_v, L_v, Q_v, a_B) for t_ in _thg])
_chg = np.where(np.diff(np.sign(_Tg)) != 0)[0]          # bornes de l'intervalle permis Θ ≥ 0
th_bornes = [brentq(lambda th: Theta_polaire(th, E_v, L_v, Q_v, a_B), _thg[i], _thg[i + 1]) for i in _chg[:2]]
passages["vorticale, E = 1,6, L = 0,05 (traverse le disque)"] = integrer_mino(E_v, L_v, Q_v, 10.0, 0.5 * sum(th_bornes), a_B)
# Équatoriale (Q = 0) : traverse r+ et r- puis atteint la singularité annulaire
passages["équatoriale, E = 1, L = 0,5 (atteint l'anneau)"] = integrer_mino(1.0, 0.5, 0.0, 10.0, np.pi / 2, a_B)

for nom, p in passages.items():
    val.verifier(f"Invariant radial r'² − R(r) = 0 ({nom})", p["inv_r"], 0.0, tol_abs=1e-8)
    val.verifier(f"Invariant polaire θ'² − Θ(θ) = 0 ({nom})", p["inv_th"], 0.0, tol_abs=1e-8)
    print(f"    {nom} : fin = {p['cause']} ; r_min = {p['r_min']:.3f} M ; τ = {p['tau_total']:.3f} M")

val.verifier("Seuil de traversée sur l'axe : E² = 1 + M/a (a = 0,9) → E_seuil", E_seuil_axe, np.sqrt(1 + 1 / 0.9), tol_abs=1e-12)
val.verifier_vrai("Axe, E = 1,2 < E_seuil : rebond en r < 0 (comme prédit)", "rebond" in passages["axe, E = 1,2 (rebond en r < 0)"]["cause"])
val.verifier_vrai("Axe, E = 1,6 > E_seuil : traversée vers r → −∞ (comme prédit)", "fuite" in passages["axe, E = 1,6 (traversée complète)"]["cause"])
val.verifier_vrai("Équatoriale Q = 0 : atteint la singularité annulaire", "singularité" in passages["équatoriale, E = 1, L = 0,5 (atteint l'anneau)"]["cause"])
# Point de rebroussement sur l'axe (analytique) : (r² + a²)(E² − 1) + 2Mr = 0
E_ = 1.2
r_reb = (-1 + np.sqrt(1 - a_B**2 * (E_**2 - 1)**2)) / (E_**2 - 1)
val.verifier("Axe, E = 1,2 : rayon de rebond ↔ racine analytique", passages["axe, E = 1,2 (rebond en r < 0)"]["r_min"], r_reb, tol_rel=1e-6)
# Temps propre sur l'axe de r = 10 à r = 0 ↔ quadrature directe τ = ∫ (r²+a²) dr / sqrt(R)
p_axe = passages["axe, E = 1,6 (traversée complète)"]
i0 = np.argmin(np.abs(p_axe["y"][0]))
tau_num = np.interp(0.0, p_axe["y"][0][::-1], p_axe["y"][6][::-1])
tau_quad = quad(lambda r: (r**2 + a_B**2) / np.sqrt(R_radial(r, 1.6, 0.0, -a_B**2 * (1.6**2 - 1), a_B)), 0.0, 10.0, epsabs=1e-12)[0]
val.verifier("Axe, E = 1,6 : temps propre 10M → disque (r = 0) ↔ quadrature", tau_num, tau_quad, tol_rel=1e-7)

# Recoupement A ↔ B : même géodésique (vorticale) intégrée par les deux méthodes hors de l'horizon
p_v = passages["vorticale, E = 1,6, L = 0,05 (traverse le disque)"]
y0 = conditions_initiales(E_v, L_v, Q_v, 10.0, 0.5 * sum(th_bornes), a_B, signe_r=-1, signe_th=+1)
ev_h = lambda tau, y, a: y[1] - 2.2
ev_h.terminal = True
solA = solve_ivp(second_membre_bl, (0, 100.0), y0, args=(a_B,), method="DOP853", rtol=1e-12, atol=1e-14, events=ev_h)
tauA, thA = solA.t_events[0][0], solA.y_events[0][0][2]
iB = np.where(p_v["y"][0] > 2.2)[0][-1]
tauB = np.interp(2.2, p_v["y"][0][:iB + 2][::-1], p_v["y"][6][:iB + 2][::-1])
thB = np.interp(2.2, p_v["y"][0][:iB + 2][::-1], p_v["y"][2][:iB + 2][::-1])
val.verifier("Recoupement des deux intégrateurs : τ(r = 2,2 M) (BL second ordre ↔ Mino)", tauB, tauA, tol_rel=1e-5)
val.verifier("Recoupement des deux intégrateurs : θ(r = 2,2 M)", thB, thA, tol_abs=1e-5)

# ---------------------------------------------------------------------------
# 4. Partie C — temps propre et temps coordonnée
# ---------------------------------------------------------------------------
p_eq = passages["équatoriale, E = 1, L = 0,5 (atteint l'anneau)"]
lam, yq = p_eq["lam"], p_eq["y"]
r_q, tau_q, ttilde_q = yq[0], yq[6], yq[5]
ext = r_q > rpB + 1e-4
Dq = r_q**2 - 2 * r_q + a_B**2
Pq = (r_q**2 + a_B**2) * 1.0 - a_B * 0.5
dt_bl = a_B * (0.5 - a_B * 1.0) + (r_q**2 + a_B**2) * Pq / Dq
t_bl = cumulative_trapezoid(np.where(ext, dt_bl, 0.0), lam, initial=0.0)
t_bl[~ext] = np.nan
tau_horizon = float(np.interp(rpB, r_q[::-1], tau_q[::-1]))
tau_horizon_int = float(np.interp(rmB, r_q[::-1], tau_q[::-1]))
tau_anneau = float(tau_q[-1])


def ut_circulaire(r, a):
    return (1 + a / r**1.5) / np.sqrt(1 - 3 / r + 2 * a / r**1.5)


FACTEUR = cc.REVENDICATIONS["taux_temporel"]          # 87 660
# Observateur statique en Schwarzschild : dt/dτ = (1 − r_s/r)^(-1/2)
eps_statique = 1.0 / FACTEUR**2                        # = 1 − r_s/r
# Orbite circulaire prograde en Kerr quasi extrémal : dt/dτ maximal à l'ISCO
dilatation = {
    "facteur_revendique": FACTEUR,
    "observateur_statique_schwarzschild_1_moins_rs_sur_r": eps_statique,
    "altitude_au_dessus_horizon_pour_M_1e12kg_m": eps_statique * 2 * cc.G * 1e12 / cc.C**2,
    "acceleration_propre_requise_M_1e12kg_m_s2": cc.C**4 / (4 * cc.G * 1e12) * FACTEUR,
    "ut_ISCO_schwarzschild": float(ut_circulaire(6.0, 0.0)),
    "ut_ISCO_a_0p9": float(ut_circulaire(r_isco(0.9), 0.9)),
    "ut_ISCO_a_0p998": float(ut_circulaire(r_isco(0.998), 0.998)),
}
# spin nécessaire pour que dt/dτ à l'ISCO atteigne 87 660 (si tant est que cela ait un sens)
try:
    a_req = brentq(lambda la: np.log(ut_circulaire(r_isco(1 - 10**la), 1 - 10**la)) - np.log(FACTEUR), -14.5, -2)
    dilatation["un_moins_a_requis_pour_ut_ISCO_87660_ordre_de_grandeur"] = 10**a_req  # proche de la limite de la double précision
except Exception as exc:  # noqa: BLE001
    dilatation["un_moins_a_requis_pour_ut_ISCO_87660_ordre_de_grandeur"] = f"non atteint en double précision ({exc})"
val.verifier("dt/dτ à l'ISCO de Schwarzschild = √2", dilatation["ut_ISCO_schwarzschild"], np.sqrt(2), tol_rel=1e-12)

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------


def cercle(ax, rayon, **kw):
    ph = np.linspace(0, 2 * np.pi, 361)
    ax.plot(rayon * np.cos(ph), rayon * np.sin(ph), **kw)


# --- Figure 1 : orbites équatoriales + conservation -----------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.8))
for ax, nom, c in zip(axes[:2], ("équatoriale prograde", "équatoriale rétrograde"), (col["bleu"], col["rouge"])):
    o = orbites[nom]
    r_, ph_ = o["y"][1], o["y"][3]
    rho = np.sqrt(r_**2 + A_KERR**2)
    ax.plot(rho * np.cos(ph_), rho * np.sin(ph_), color=c, lw=1.0)
    ax.fill(np.sqrt(RP**2 + A_KERR**2) * np.cos(np.linspace(0, 2 * np.pi, 200)), np.sqrt(RP**2 + A_KERR**2) * np.sin(np.linspace(0, 2 * np.pi, 200)), color="k")
    cercle(ax, np.sqrt(4 + A_KERR**2), color=col["vert"], ls="--", lw=1.2, label="ergosurface (r = 2M)")
    cercle(ax, np.sqrt(r_isco(A_KERR)**2 + A_KERR**2) if "pro" in nom else np.sqrt(8.717**2 + A_KERR**2), color=col["gris"], ls=":", lw=1.2,
           label="ISCO " + ("prograde (2,32 M)" if "pro" in nom else "rétrograde (8,72 M)"))
    n_orb = (ph_[-1] - ph_[0]) / (2 * np.pi)
    ax.set_title(f"Orbite {nom}\nE = {o['E']:.5f}, $L_z$ = {o['L']:.4f} M ; r ∈ [{r_.min():.2f}, {r_.max():.2f}] M".replace(".", ","), fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlabel("x / M")
    ax.set_ylabel("y / M")
    ax.legend(fontsize=8, loc="upper right")
ax = axes[2]
for nom, c in (("équatoriale prograde", col["bleu"]), ("équatoriale rétrograde", col["rouge"]), ("quasi polaire", col["vert"])):
    o = orbites[nom]
    E, L, norme, Qc = constantes_du_mouvement(o["y"], A_KERR)
    ax.semilogy(o["tau"], np.abs(E - E[0]) / abs(E[0]) + 1e-17, color=c, lw=1.2, label=f"{nom} : |ΔE/E|")
    ax.semilogy(o["tau"], np.abs(norme + 1) + 1e-17, color=c, lw=1.2, ls="--", label=f"{nom} : |g(u,u) + 1|")
    if nom == "quasi polaire":
        ax.semilogy(o["tau"], np.abs(Qc - Qc[0]) / abs(Qc[0]) + 1e-17, color=c, lw=1.2, ls=":", label=f"{nom} : |ΔQ/Q| (Carter)")
ax.axhline(1e-8, color="k", lw=0.8, ls="-.")
ax.text(1750, 1.5e-8, "seuil de validation 10⁻⁸", fontsize=8)
ax.set_ylim(1e-17, 1e-6)
ax.set_xlabel("temps propre τ [GM/c³]")
ax.set_ylabel("erreur sur les intégrales premières")
ax.set_title("Test : conservation de E, de la norme et de la constante de Carter", fontsize=10)
ax.legend(fontsize=7.5, loc="upper left", ncol=1)
cc.titre(fig, "S03 — Géodésiques équatoriales autour d'un trou noir de Kerr (a = 0,9 M) et test de conservation")
cc.sauver_figure(fig, FIG / "S03_fig1_orbites_equatoriales.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : orbite quasi polaire --------------------------------------------------------
o = orbites["quasi polaire"]
t_, r_, th_, ph_ = o["y"][:4]
rho = np.sqrt(r_**2 + A_KERR**2) * np.sin(th_)
x_, y_, z_ = rho * np.cos(ph_), rho * np.sin(ph_), r_ * np.cos(th_)
fig = plt.figure(figsize=(15.5, 6.2))
ax = fig.add_subplot(1, 2, 1, projection="3d")
ax.plot(x_, y_, z_, color=col["vert"], lw=0.7)
u, v = np.meshgrid(np.linspace(0, 2 * np.pi, 40), np.linspace(0, np.pi, 20))
ax.plot_surface(np.sqrt(RP**2 + A_KERR**2) * np.cos(u) * np.sin(v), np.sqrt(RP**2 + A_KERR**2) * np.sin(u) * np.sin(v), RP * np.cos(v), color="k")
ax.plot([0, 0], [0, 0], [-11, 11], color=col["gris"], ls="--", lw=1)
ax.set_xlabel("x / M")
ax.set_ylabel("y / M")
ax.set_zlabel("z / M")
ax.set_box_aspect((1, 1, 1))
ax.set_title(f"Orbite quasi polaire (r ∈ [6, 10] M, $θ_{{min}}$ = {theta_min_pol:.1f}°)\nle plan orbital est entraîné autour de l'axe de rotation".replace(".", ","), fontsize=10)
ax2 = fig.add_subplot(1, 2, 2)
# longitude du nœud ascendant à chaque passage à l'équateur (sens montant)
idx = np.where((th_[:-1] > np.pi / 2) & (th_[1:] <= np.pi / 2))[0]
ax2.plot(o["tau"][idx], np.degrees(ph_[idx] - ph_[idx][0]) - 360.0 * np.arange(len(idx)), "o-", color=col["vert"], ms=3, lw=1,
         label="longitude du nœud (calcul numérique)")
pente = np.polyfit(o["tau"][idx], np.degrees(ph_[idx] - ph_[idx][0]) - 360.0 * np.arange(len(idx)), 1)[0]
ax2.set_xlabel("temps propre τ [GM/c³]")
ax2.set_ylabel("dérive de la longitude du nœud [degrés]")
ax2.set_title(f"Précession nodale (entraînement des référentiels) : {pente * 1000:.2f}° par 1000 GM/c³".replace(".", ","), fontsize=10)
ax2.legend(fontsize=8.5)
cc.titre(fig, "S03 — Orbite quasi polaire dans Kerr (a = 0,9 M) : précession de Lense-Thirring du plan orbital")
cc.sauver_figure(fig, FIG / "S03_fig2_orbite_polaire.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : passage par l'anneau ---------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(17, 6.4))
ax = axes[0]
th_c = np.linspace(0, np.pi, 361)
for signe in (1, -1):
    ax.plot(signe * np.sqrt(rpB**2 + a_B**2) * np.sin(th_c), rpB * np.cos(th_c), color=col["ciel"], lw=1.5, label="horizon externe $r_+$" if signe > 0 else None)
    ax.plot(signe * np.sqrt(rmB**2 + a_B**2) * np.sin(th_c), rmB * np.cos(th_c), color=col["bleu"], lw=1.5, ls="--", label="horizon interne $r_-$" if signe > 0 else None)
ax.plot([-a_B, a_B], [0, 0], "o", color=col["rouge"], ms=7, label="singularité annulaire (vue en coupe)")
ax.plot([-a_B, a_B], [0, 0], color=col["rouge"], lw=1, ls=":")
couleurs_p = [col["orange"], col["vert"], col["violet"], col["noir"]]
decalages = [-0.06, 0.06, 0.0, 0.0]
for (nom, p), c, dx in zip(passages.items(), couleurs_p, decalages):
    r_, th_, ph_ = p["y"][0], p["y"][2], p["y"][4]
    rho = np.sqrt(r_**2 + a_B**2) * np.sin(th_)
    if "équatoriale" in nom:
        rho = rho * np.sign(np.cos(ph_ + np.arctan2(a_B, r_)) + 1e-12) * 0 + rho   # projection méridienne : ρ ≥ 0
    z = r_ * np.cos(th_)
    pos = r_ >= 0
    ax.plot(np.where(pos, rho + dx, np.nan), np.where(pos, z, np.nan), color=c, lw=1.8, label=nom)
    ax.plot(np.where(~pos, rho + dx, np.nan), np.where(~pos, z, np.nan), color=c, lw=1.8, ls=(0, (1, 1)))
ax.plot([], [], color="k", lw=1.8, ls=(0, (1, 1)), label="pointillé : feuillet r < 0 (autre région asymptotique)")
ax.set_xlim(-3.2, 3.2)
ax.set_ylim(-6.5, 6.5)
ax.set_xlabel("ρ / M (coordonnée de Kerr-Schild)")
ax.set_ylabel("z / M = r cos θ / M")
ax.set_title("(a) Plan méridien : trajectoires à travers le disque de l'anneau", fontsize=10)
ax.legend(fontsize=7, loc="lower left")

ax = axes[1]
for (nom, p), c in zip(passages.items(), couleurs_p):
    ax.plot(p["y"][6], p["y"][0], color=c, lw=1.8, label=f"{nom}\n→ {p['cause']}")
ax.axhline(rpB, color=col["ciel"], lw=1.2)
ax.axhline(rmB, color=col["bleu"], lw=1.2, ls="--")
ax.axhline(0, color=col["rouge"], lw=1.2, ls=":")
ax.text(0.2, rpB + 0.15, "$r_+$", color=col["bleu"], fontsize=9)
ax.text(0.2, rmB + 0.15, "$r_-$", color=col["bleu"], fontsize=9)
ax.text(0.2, -0.75, "disque r = 0", color=col["rouge"], fontsize=9)
ax.set_ylim(-12, 10.5)
ax.set_xlim(0, 22)
ax.set_xlabel("temps propre τ [GM/c³]")
ax.set_ylabel("coordonnée radiale r / M")
ax.set_title("(b) r(τ) : tout se joue en un temps propre fini (~10 GM/c³)", fontsize=10)
ax.legend(fontsize=6.8, loc="lower left")

ax = axes[2]
r_ax = np.linspace(-8, 8, 2001)
for E_, c in ((1.0, col["gris"]), (1.2, col["orange"]), (E_seuil_axe, col["bleu"]), (1.6, col["vert"])):
    Rax = (r_ax**2 + a_B**2) * ((r_ax**2 + a_B**2) * (E_**2 - 1) + 2 * r_ax)
    ax.plot(r_ax, Rax / (r_ax**2 + a_B**2)**2, color=c, lw=1.8, label=f"E = {E_:.3f}".replace(".", ","))
ax.axhline(0, color="k", lw=0.8)
ax.axvline(0, color=col["rouge"], lw=1, ls=":")
ax.axhspan(-1, 0, color=col["rouge"], alpha=0.08)
ax.text(-7.6, -0.42, "région interdite : $(dr/d\\tau)^2$ < 0", fontsize=8.5, color=col["rouge"])
ax.set_ylim(-0.6, 2.2)
ax.set_xlabel("r / M sur l'axe de rotation (θ = 0)")
ax.set_ylabel(r"$(dr/d\tau)^2 = R(r)/\Sigma^2$")
ax.set_title(f"(c) Sur l'axe : côté r < 0 la gravité est répulsive ;\ntraversée complète seulement si E² > 1 + M/a (E > {E_seuil_axe:.3f})".replace(".", ","), fontsize=10)
ax.legend(fontsize=8, loc="upper center")
cc.titre(fig, "S03 — Kerr maximalement étendu (a = 0,9 M) : géodésiques traversant les horizons puis le disque de l'anneau vers r < 0")
cc.sauver_figure(fig, FIG / "S03_fig3_passage_anneau.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 4 : temps propre et temps coordonnée ---------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.6))
ax = axes[0]
ax.plot(tau_q, r_q, color="k", lw=2)
ax.axhline(rpB, color=col["ciel"], lw=1.2)
ax.axhline(rmB, color=col["bleu"], lw=1.2, ls="--")
ax.text(0.3, rpB + 0.15, "$r_+$", color=col["bleu"])
ax.text(0.3, rmB + 0.15, "$r_-$", color=col["bleu"])
ax.set_xlabel("temps propre τ [GM/c³]")
ax.set_ylabel("r / M")
ax.set_title(f"(a) Chute équatoriale (E = 1, $L_z$ = 0,5 M) : horizon en τ = {tau_horizon:.2f},\nanneau en τ = {tau_anneau:.2f} GM/c³ (temps propre FINI)".replace(".", ","), fontsize=10)
ax = axes[1]
ax.plot(tau_q, t_bl, color=col["rouge"], lw=2, label="temps de Boyer-Lindquist t (observateur lointain)")
ax.plot(tau_q, ttilde_q, color=col["bleu"], lw=2, ls="--", label="temps « entrant » de Kerr-Schild t̃ (régulier)")
ax.plot(tau_q, tau_q, color=col["gris"], lw=1, ls=":", label="t = τ")
ax.axvline(tau_horizon, color=col["ciel"], lw=1.2)
ax.text(tau_horizon + 0.1, 5, "traversée de $r_+$", rotation=90, color=col["bleu"], fontsize=8.5)
ax.set_ylim(0, 60)
ax.set_xlabel("temps propre τ [GM/c³]")
ax.set_ylabel("temps coordonnée [GM/c³]")
ax.set_title("(b) t → ∞ à l'horizon : divergence de COORDONNÉES,\nnon un voyage dans le temps", fontsize=10)
ax.legend(fontsize=8, loc="upper left")
ax = axes[2]
for a_, c in ((0.0, col["bleu"]), (0.9, col["vert"]), (0.998, col["rouge"])):
    rr = np.logspace(np.log10(r_isco(a_)), 2, 400)
    ax.loglog(rr, ut_circulaire(rr, a_) - 1, color=c, lw=2, label=f"a = {a_} M ; ISCO : dt/dτ = {ut_circulaire(r_isco(a_), a_):.2f}".replace(".", ","))
    ax.plot(r_isco(a_), ut_circulaire(r_isco(a_), a_) - 1, "o", color=c)
ax.axhline(FACTEUR, color="k", ls="--", lw=1.5)
ax.text(1.3, FACTEUR * 0.35, "revendication « 10 ans/heure » : dt/dτ ≈ 87 660", fontsize=8.5)
ax.set_ylim(1e-3, 1e6)
ax.set_xlabel("rayon de l'orbite circulaire r / M")
ax.set_ylabel("dt/dτ − 1")
ax.set_title("(c) Dilatation sur orbite circulaire stable (toujours vers le FUTUR)", fontsize=10)
ax.legend(fontsize=8, loc="center right")
cc.titre(fig, "S03 — Temps propre et temps coordonnée dans Kerr (a = 0,9 M)")
cc.sauver_figure(fig, FIG / "S03_fig4_temps_propre_coordonnee.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S03_geodesiques_kerr",
    "avertissement": cc.MENTION,
    "unites": "G = c = 1, M = 1 ; 1 GM/c³ = 2,48e-24 s pour M = 1e12 kg",
    "GM_sur_c3_pour_1e12_kg_s": cc.G * 1e12 / cc.C**3,
    "parametres": {"a": A_KERR, "r_plus": RP, "r_moins": RM, "r_isco_prograde": r_isco(A_KERR)},
    "orbites_liees": {k: {"E": v["E"], "L_z": v["L"], "Q_carter": v["Q"], "derives": v["derives"]} for k, v in orbites.items()},
    "theta_min_orbite_quasi_polaire_deg": theta_min_pol,
    "avance_periastre_schwarzschild_p50_e0p3_rad": {"numerique": avance_num, "quadrature_exacte": avance_exacte, "premier_ordre_6piM_sur_p": 6 * np.pi / p_s},
    "precession_nodale_r500_rad_par_orbite": {"numerique": prec_num, "lense_thirring": prec_lt},
    "passages_par_l_anneau": {k: {"E": v["E"], "L_z": v["L"], "Q_carter": v["Q"], "issue": v["cause"], "r_min_M": v["r_min"],
                                  "temps_propre_total_M": v["tau_total"], "invariant_radial": v["inv_r"], "invariant_polaire": v["inv_th"]}
                              for k, v in passages.items()},
    "seuil_energie_traversee_axe": E_seuil_axe,
    "chute_equatoriale": {"tau_horizon_externe_M": tau_horizon, "tau_horizon_interne_M": tau_horizon_int, "tau_anneau_M": tau_anneau,
                          "tau_anneau_secondes_pour_1e12_kg": tau_anneau * cc.G * 1e12 / cc.C**3},
    "dilatation_temporelle": dilatation,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S03_resultats.json", resultats)
val.imprimer_bilan()
print("S03 terminé.")
