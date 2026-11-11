# -*- coding: utf-8 -*-
"""S05 — Configuration « C204 » en champ faible : deux masses ponctuelles en rotation.

Potentiel newtonien, accélération, marées entre 0,1 et 4 m, champ gravitomagnétique
(gravito-électromagnétisme linéarisé), entraînement des référentiels, facteur de dilatation
temporelle, rayonnement gravitationnel (formule du quadrupôle) et temps de coalescence (Peters).
Comparaison aux « 1,5–2 g » et aux « 10 ans par heure » (dt/dτ ≈ 87 660) revendiqués.

SIMULATION ILLUSTRATIVE : calcul en champ faible et vitesses lentes, valable à plus de quelques
rayons gravitationnels des masses (soit partout à l'échelle du mètre : r_g ≤ 1e-14 m ici).
Ce n'est pas une preuve expérimentale ; aucune des masses supposées n'est attestée.

Exécution :  .venv/bin/python 05_simulations/S05_champ_faible_c204/s05_champ_faible_c204.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402
from matplotlib.colors import LogNorm  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore")
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S05_champ_faible_c204")
col = cc.COULEURS
G, C, G0 = cc.G, cc.C, cc.G0
REV = cc.REVENDICATIONS

# ---------------------------------------------------------------------------
# 1. Hypothèses [HYP] : masse M de CHAQUE singularité et séparation d
# ---------------------------------------------------------------------------
M_2G_1M = G0 * 1.0**2 / G                    # 2 masses M donnant 2 g à 1 m : 2GM/r² = 2 g0
HYPOTHESES_M = {
    "A : 113 kg (demi-unité de 227 kg)": REV["masse_unite_kg"] / 2,
    "B : 1e9 kg (durée de vie ~30 ans)": 1e9,
    "C : 1,5e11 kg (2 g à 1 m pour la paire)": M_2G_1M,
    "D : 1e12 kg (300–500 MW, photons)": 1e12,
    "E : 4,4e12 kg (300–500 MW, toutes espèces)": 4.4e12,
}
D_REF = 0.30                                  # séparation de référence des cartes [m] ([HYP] de l'Équipe D : échelle du coffre)
D_DOC = 0.098                                 # entraxe des deux logements d'après DOC-007 [DÉD, Équipe A : 98 ± 25 mm, soit ≈ 0,10 m]
SEPARATIONS = (D_DOC, D_REF)                  # correction n° 44 (Red Team, phase 7) : le cas documentaire figure à côté du cas [HYP]
TAILLE_CORPS = 1.0                            # étendue radiale d'un occupant assis [m] ([HYP])


def positions(d, phase=0.0):
    """Positions des deux masses (plan z = 0), séparées de d, à la phase orbitale donnée."""
    return np.array([[0.5 * d * np.cos(phase), 0.5 * d * np.sin(phase), 0.0],
                     [-0.5 * d * np.cos(phase), -0.5 * d * np.sin(phase), 0.0]])


def potentiel(P, M, d, phase=0.0):
    """Φ(P) = −Σ GM/|P − r_i|  [J/kg] ; P de forme (..., 3)."""
    return sum(-G * M / np.linalg.norm(P - s, axis=-1) for s in positions(d, phase))


def acceleration(P, M, d, phase=0.0):
    """g(P) = −∇Φ = −Σ GM (P − r_i)/|P − r_i|³  [m/s²]."""
    g = np.zeros_like(P, dtype=float)
    for s in positions(d, phase):
        dr = P - s
        g += -G * M * dr / np.linalg.norm(dr, axis=-1, keepdims=True)**3
    return g


def tenseur_maree(P, M, d, phase=0.0):
    """T_ij = −∂_i∂_jΦ = Σ GM (3 n_i n_j − δ_ij)/r³  [s⁻²] en un point P (3,)."""
    T = np.zeros((3, 3))
    for s in positions(d, phase):
        dr = P - s
        r = np.linalg.norm(dr)
        n = dr / r
        T += G * M * (3 * np.outer(n, n) - np.eye(3)) / r**3
    return T


def omega_kepler(M, d):
    """Vitesse angulaire orbitale képlérienne de deux masses égales M séparées de d."""
    return np.sqrt(2 * G * M / d**3)


def champ_gm_masses_mobiles(P, M, d, Omega, phase=0.0):
    """Champ gravitomagnétique B_g(P) [m/s²] de deux masses en orbite circulaire (quasi statique).

    Convention de Mashhoon : A = (2G/c) Σ m v/|r − r_i| ; B_g = ∇×A = (2G/c) Σ m v_i × (P − r_i)/|P − r_i|³.
    La précession d'un gyroscope au repos (entraînement) vaut Ω_LT = B_g/c, au signe de convention près."""
    B = np.zeros_like(P, dtype=float)
    for s, signe in zip(positions(d, phase), (+1, -1)):
        v = signe * 0.5 * d * Omega * np.array([-np.sin(phase), np.cos(phase), 0.0])
        dr = P - s
        B += (2 * G / C) * M * np.cross(v, dr) / np.linalg.norm(dr, axis=-1, keepdims=True)**3
    return B


def champ_gm_dipole(P, J):
    """B_g dipolaire d'un moment cinétique J :  B_g = (G/c) [3 (J·n) n − J]/r³ ; Ω_LT = B_g/c."""
    r = np.linalg.norm(P, axis=-1, keepdims=True)
    n = P / r
    return (G / C) * (3 * np.sum(J * n, axis=-1, keepdims=True) * n - J) / r**3


def puissance_og_quadrupole(M, d, Omega):
    """Deux masses égales en rotation circulaire : P = (32/5)(G/c⁵) μ² d⁴ Ω⁶, μ = M/2."""
    return (32 / 5) * (G / C**5) * (M / 2)**2 * d**4 * Omega**6


def puissance_og_numerique(M, d, Omega, n=4096):
    """P = (G/5c⁵) ⟨d³Q_ij/dt³ · d³Q_ij/dt³⟩, quadrupôle sans trace, dérivées par FFT (test indépendant)."""
    t = np.linspace(0, 2 * np.pi / Omega, n, endpoint=False)
    Q = np.zeros((n, 3, 3))
    for signe in (+1, -1):
        x = signe * 0.5 * d * np.stack([np.cos(Omega * t), np.sin(Omega * t), 0 * t], axis=1)
        Q += M * (np.einsum("ni,nj->nij", x, x) - np.eye(3) * np.sum(x**2, axis=1)[:, None, None] / 3)
    w = 2 * np.pi * np.fft.fftfreq(n, d=t[1] - t[0])
    Q3 = np.real(np.fft.ifft((1j * w[:, None, None])**3 * np.fft.fft(Q, axis=0), axis=0))
    return (G / (5 * C**5)) * np.mean(np.sum(Q3**2, axis=(1, 2)))


def peters_puissance(m1, m2, a):
    return (32 / 5) * G**4 * m1**2 * m2**2 * (m1 + m2) / (C**5 * a**5)


def peters_temps_coalescence(m1, m2, a0):
    return (5 / 256) * C**5 * a0**4 / (G**3 * m1 * m2 * (m1 + m2))


# ---------------------------------------------------------------------------
# 2. Tests de validation
# ---------------------------------------------------------------------------
print("S05 — tests de validation")
rng = np.random.default_rng(204)
Mt, dt_ = 1e12, D_REF
# V1 : g = −∇Φ (différences centrées)
Pts = rng.uniform(-3, 3, (200, 3))
Pts = Pts[np.linalg.norm(Pts, axis=1) > 0.5]
h = 1e-5
g_num = np.stack([-(potentiel(Pts + h * e, Mt, dt_) - potentiel(Pts - h * e, Mt, dt_)) / (2 * h) for e in np.eye(3)], axis=1)
g_ana = acceleration(Pts, Mt, dt_)
val.verifier("g analytique ↔ −∇Φ numérique (erreur relative max.)", np.max(np.linalg.norm(g_num - g_ana, axis=1) / np.linalg.norm(g_ana, axis=1)), 0.0, tol_abs=1e-7)
# V2 : équation de Laplace : trace du tenseur de marée nulle hors des sources
tr = max(abs(np.trace(tenseur_maree(p, Mt, dt_))) / np.linalg.norm(tenseur_maree(p, Mt, dt_)) for p in Pts[:50])
val.verifier("Trace du tenseur de marée (ΔΦ = 0 hors sources), relative", tr, 0.0, tol_abs=1e-12)
# V3 : champ lointain sur l'axe : g → (2GM/r²)(1 + 3d²/(4r²))
r_l = 30.0
g_axe = np.linalg.norm(acceleration(np.array([[r_l, 0, 0]]), Mt, dt_))
val.verifier("Champ lointain sur l'axe : monopôle + correction quadrupolaire", g_axe, 2 * G * Mt / r_l**2 * (1 + 3 * dt_**2 / (4 * r_l**2)), tol_rel=1e-8)
# V4 : formule du quadrupôle : analytique ↔ numérique (FFT)
Om = omega_kepler(Mt, dt_)
val.verifier("Puissance OG : formule fermée ↔ ⟨Q⃛ij Q⃛ij⟩ numérique", puissance_og_numerique(Mt, dt_, Om), puissance_og_quadrupole(Mt, dt_, Om), tol_rel=1e-9)
# V5 : identité avec la formule de Peters (orbite képlérienne)
val.verifier("Puissance OG : quadrupôle (Ω képlérien) ↔ Peters (1964)", puissance_og_quadrupole(Mt, dt_, Om), peters_puissance(Mt, Mt, dt_), tol_rel=1e-12)
# V6 : temps de coalescence de Peters ↔ intégration numérique de da/dt = −(64/5) G³ m1 m2 (m1+m2)/(c⁵ a³)
k_p = (64 / 5) * G**3 * Mt * Mt * (2 * Mt) / C**5
t_p = peters_temps_coalescence(Mt, Mt, dt_)
sol = solve_ivp(lambda t, a: [-k_p / a[0]**3], (0, 0.999999 * t_p), [dt_], rtol=1e-11, atol=0, method="DOP853")
val.verifier("Peters : a(t) numérique à 0,999999 t_c ↔ a0 (1 − t/t_c)^(1/4)", sol.y[0, -1], dt_ * (1 - 0.999999)**0.25, tol_rel=1e-5)
# V7 : repère Terre-Soleil ≈ 196 W
P_ts = peters_puissance(cc.M_SOLEIL, cc.M_TERRE, 1.495978707e11)
val.verifier("Repère : puissance OG du système Terre-Soleil ≈ 196 W", P_ts, 196.0, tol_rel=0.03)
# V8 : repère Gravity Probe B : entraînement ≈ 39 mas/an (orbite polaire à 642 km, moyenne ⟨Ω⟩ = GJ/(2c²r³))
J_terre, r_gpb = 5.86e33, 6.371e6 + 6.42e5
gpb = G * J_terre / (2 * C**2 * r_gpb**3) * cc.ANNEE * (180 / np.pi) * 3600e3
val.verifier("Repère : effet Lense-Thirring de Gravity Probe B ≈ 39 mas/an", gpb, 39.2, tol_rel=0.06)
# V9 : repère GPS : +38,5 µs/jour (gravitation + vitesse) avec le même développement en champ faible
GM_T, R_T, r_gps = 3.986004e14, 6.371e6, 2.6560e7
gps = ((GM_T / C**2) * (1 / R_T - 1 / r_gps) - (GM_T / r_gps) / (2 * C**2)) * cc.JOUR * 1e6
val.verifier("Repère : avance des horloges GPS ≈ +38,5 µs/jour", gps, 38.5, tol_rel=0.02)
# V10 : champ gravitomagnétique des deux masses en orbite, moyenné sur une orbite ↔ dipôle de J_orb (loin)
P_far = np.array([[0.0, 0.0, 50 * dt_], [50 * dt_, 0.0, 0.0], [20 * dt_, 0.0, 30 * dt_]])
phases = np.linspace(0, 2 * np.pi, 720, endpoint=False)
B_moy = np.mean([champ_gm_masses_mobiles(P_far, Mt, dt_, Om, ph) for ph in phases], axis=0)
J_orb = np.array([0, 0, Mt * dt_**2 * Om / 2])
B_dip = champ_gm_dipole(P_far, J_orb)
val.verifier("B_g moyen de la paire en orbite ↔ dipôle de J_orb (r = 50 d), erreur relative", np.max(np.linalg.norm(B_moy - B_dip, axis=1) / np.linalg.norm(B_dip, axis=1)), 0.0, tol_abs=2e-3)

# ---------------------------------------------------------------------------
# 3. Tableau par hypothèse de masse
# ---------------------------------------------------------------------------
tableau = {}
for nom, M in HYPOTHESES_M.items():
    ligne = {"M_kg": M, "r_g_m": G * M / C**2}
    for r in (0.1, 0.5, 1.0, 2.0, 3.0, 4.0):
        P = np.array([[0.0, r, 0.0]])            # sur la médiatrice de la paire
        ligne[f"g_a_{r}m_en_g0"] = float(np.linalg.norm(acceleration(P, M, D_REF)) / G0)
        ligne[f"dilatation_dt_dtau_moins_1_a_{r}m"] = float(-potentiel(P, M, D_REF)[0] / C**2)
    for r in (1.0, 2.0, 3.0):                    # marée tête-pieds sur TAILLE_CORPS
        g1 = np.linalg.norm(acceleration(np.array([[0.0, r - TAILLE_CORPS / 2, 0.0]]), M, D_REF))
        g2 = np.linalg.norm(acceleration(np.array([[0.0, r + TAILLE_CORPS / 2, 0.0]]), M, D_REF))
        ligne[f"maree_sur_{TAILLE_CORPS}m_centre_{r}m_en_g0"] = float(abs(g1 - g2) / G0)
        ligne[f"gradient_radial_a_{r}m_s-2"] = float(tenseur_maree(np.array([0.0, r, 0.0]), M, D_REF)[1, 1])
    ligne["distance_pour_2g_m"] = float(np.sqrt(2 * G * M / (2 * G0)))
    ligne["distance_pour_1p5g_m"] = float(np.sqrt(2 * G * M / (1.5 * G0)))
    ligne["epaisseur_coquille_1p5_a_2g_m"] = ligne["distance_pour_1p5g_m"] - ligne["distance_pour_2g_m"]
    ligne["decalage_temporel_cumule_6h_a_1m_s"] = ligne["dilatation_dt_dtau_moins_1_a_1.0m"] * 6 * cc.HEURE
    for d in SEPARATIONS:
        Om_k = omega_kepler(M, d)
        J_spin_max = G * M**2 / C
        J_orb_k = M * d**2 * Om_k / 2
        ligne[f"d={d}m"] = {
            "Omega_kepler_rad_s": Om_k, "periode_s": 2 * np.pi / Om_k, "vitesse_orbitale_m_s": Om_k * d / 2,
            "J_orbital_kg_m2_s": J_orb_k, "J_spin_max_par_masse_kg_m2_s": J_spin_max,
            "omega_LT_pole_1m_orbital_rad_s": 2 * G * J_orb_k / (C**2 * 1.0**3),
            "omega_LT_pole_1m_spins_max_rad_s": 2 * G * (2 * J_spin_max) / (C**2 * 1.0**3),
            "P_OG_W": puissance_og_quadrupole(M, d, Om_k),
            "temps_coalescence_s": peters_temps_coalescence(M, M, d),
            "temps_coalescence_ans": peters_temps_coalescence(M, M, d) / cc.ANNEE,
            "force_mutuelle_N": G * M**2 / d**2,
        }
    tableau[nom] = ligne

FACTEUR = REV["taux_temporel"]
M_D = HYPOTHESES_M["D : 1e12 kg (300–500 MW, photons)"]
dil_1m_D = tableau["D : 1e12 kg (300–500 MW, photons)"]["dilatation_dt_dtau_moins_1_a_1.0m"]
comparaison = {
    "facteur_revendique_dt_dtau": FACTEUR,
    "dilatation_obtenue_a_1m_M_1e12kg": dil_1m_D,
    "ecart_decades_M_1e12kg": float(np.log10(FACTEUR / dil_1m_D)),
    "dilatation_obtenue_a_1m_M_113kg": tableau["A : 113 kg (demi-unité de 227 kg)"]["dilatation_dt_dtau_moins_1_a_1.0m"],
    "ecart_decades_M_113kg": float(np.log10(FACTEUR / tableau["A : 113 kg (demi-unité de 227 kg)"]["dilatation_dt_dtau_moins_1_a_1.0m"])),
    "signe": "la dilatation gravitationnelle ne fait que RALENTIR l'horloge proche (avance vers le futur extérieur) ; "
             "elle ne produit aucun déplacement vers le passé",
    "g_a_1m_M_113kg_en_g0": tableau["A : 113 kg (demi-unité de 227 kg)"]["g_a_1.0m_en_g0"],
    "ecart_decades_pesanteur_M_113kg": float(np.log10(2.0 / tableau["A : 113 kg (demi-unité de 227 kg)"]["g_a_1.0m_en_g0"])),
}
# Modulation du champ vue par un observateur fixe quand la paire tourne (fréquence 2Ω)
modulation = {}
for r in (1.0, 2.0, 3.0):
    gs = [np.linalg.norm(acceleration(np.array([[r, 0.0, 0.0]]), M_2G_1M, D_REF, ph)) for ph in np.linspace(0, np.pi, 181)]
    gs_doc = [np.linalg.norm(acceleration(np.array([[r, 0.0, 0.0]]), M_2G_1M, D_DOC, ph)) for ph in np.linspace(0, np.pi, 181)]
    modulation[f"r={r}m"] = {"variation_relative_crete_a_crete": float((max(gs) - min(gs)) / np.mean(gs)),
                            "approximation_9d2_sur_8r2": 9 * D_REF**2 / (8 * r**2),
                            "variation_relative_crete_a_crete_entraxe_documentaire": float((max(gs_doc) - min(gs_doc)) / np.mean(gs_doc))}
# Sensibilité des champs à 1–3 m au choix de la séparation (0,30 m [HYP] contre 0,098 m documentaire)
sensibilite_d = {}
for r in (1.0, 2.0, 3.0):
    Pm = np.array([[0.0, r, 0.0]])
    sensibilite_d[f"r={r}m"] = {
        "rapport_g_entraxe_documentaire_sur_g_0p30m": float(np.linalg.norm(acceleration(Pm, M_2G_1M, D_DOC)) / np.linalg.norm(acceleration(Pm, M_2G_1M, D_REF))),
        "rapport_dilatation": float(potentiel(Pm, M_2G_1M, D_DOC)[0] / potentiel(Pm, M_2G_1M, D_REF)[0])}
val.verifier("Modulation de |g| à 2 m ↔ estimation quadrupolaire (3/4)(d/r)²·(3/2) = 9d²/(8r²)",
             modulation["r=2.0m"]["variation_relative_crete_a_crete"], 9 * D_REF**2 / (8 * 2.0**2), tol_rel=0.05)

# ---------------------------------------------------------------------------
# 4. Figures
# ---------------------------------------------------------------------------
# --- Figure 1 : carte d'accélération + profils ------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.3), gridspec_kw={"width_ratios": [1, 1.15]})
x = np.linspace(-4, 4, 641)
X, Y = np.meshgrid(x, x)
P = np.stack([X, Y, 0 * X], axis=-1)
gmap = np.linalg.norm(acceleration(P, M_2G_1M, D_REF), axis=-1) / G0
pc = ax1.pcolormesh(X, Y, gmap, norm=LogNorm(vmin=1e-1, vmax=1e3), cmap="viridis", shading="auto")
cs = ax1.contour(X, Y, gmap, levels=[0.2, 0.5, 1.0, 1.5, 2.0, 10.0, 100.0], colors="white", linewidths=[0.7, 0.7, 0.9, 1.6, 1.6, 0.9, 0.7])
ax1.clabel(cs, fmt=lambda v: f"{v:g} g".replace(".", ","), fontsize=7.5)
ax1.plot(positions(D_REF)[:, 0], positions(D_REF)[:, 1], "o", color=col["rouge"], ms=4)
for rr_, ls in ((1.0, "--"), (3.0, "--")):
    ax1.add_patch(plt.Circle((0, 0), rr_, fill=False, color=col["orange"], ls=ls, lw=1.2))
ax1.text(0.75, 0.75, "1 m", color=col["orange"], fontsize=8.5)
ax1.text(2.17, 2.17, "3 m", color=col["orange"], fontsize=8.5)
ax1.set_aspect("equal")
ax1.set_xlabel("x [m] (axe joignant les deux masses)")
ax1.set_ylabel("y [m]")
ax1.set_title(f"(a) |g|/g₀ pour l'hypothèse C : 2 × {cc.sci(M_2G_1M, 2)} kg, d = {D_REF} m".replace(".", ","), fontsize=10)
ax1.grid(False)
fig.colorbar(pc, ax=ax1, fraction=0.046, pad=0.03, label="|g| / g₀ (échelle log.)")

r = np.logspace(-1, np.log10(4), 300)
for (nom, M), c in zip(HYPOTHESES_M.items(), (col["bleu"], col["ciel"], col["vert"], col["orange"], col["rouge"])):
    gy = np.linalg.norm(acceleration(np.stack([0 * r, r, 0 * r], axis=1), M, D_REF), axis=1) / G0
    ax2.loglog(r, gy, color=c, lw=2, label=nom)
ax2.axhspan(*REV["pesanteur_g"], color=col["jaune"], alpha=0.7, label="revendication : 1,5 à 2 g")
ax2.axvspan(1.0, 3.0, color=col["gris"], alpha=0.15, label="distances 1 à 3 m")
ax2.axvspan(*REV["zone_effet_m"], color=col["violet"], alpha=0.15, label="« champ efficace 10–12 ft »")
ax2.set_xlabel("distance r au centre de la paire, sur la médiatrice [m]")
ax2.set_ylabel("|g| / g₀")
ax2.set_xlim(0.1, 4)
ax2.set_xticks([0.1, 0.2, 0.5, 1, 2, 3, 4])
ax2.set_xticklabels(["0,1", "0,2", "0,5", "1", "2", "3", "4"])
ax2.xaxis.set_minor_formatter(plt.NullFormatter())
ax2.set_ylim(1e-20, 1e4)
ax2.set_title("(b) Profils radiaux pour les cinq hypothèses de masse", fontsize=10)
ax2.legend(fontsize=7.8, loc="lower left", ncol=1)
cc.titre(fig, "S05 — Deux masses ponctuelles séparées de 0,3 m : accélération newtonienne entre 0,1 et 4 m")
cc.sauver_figure(fig, FIG / "S05_fig1_acceleration.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : marées -------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.5, 5.6))
rc = np.linspace(0.6, 4.0, 400)
for (nom, M), c in zip(list(HYPOTHESES_M.items())[2:], (col["vert"], col["orange"], col["rouge"])):
    g_in = np.linalg.norm(acceleration(np.stack([0 * rc, rc - TAILLE_CORPS / 2, 0 * rc], axis=1), M, D_REF), axis=1)
    g_out = np.linalg.norm(acceleration(np.stack([0 * rc, rc + TAILLE_CORPS / 2, 0 * rc], axis=1), M, D_REF), axis=1)
    ax1.semilogy(rc, (g_in - g_out) / G0, color=c, lw=2, label=nom)
ax1.axhline(0.5, color="k", ls="--", lw=1)
ax1.text(2.6, 0.56, "écart max. compatible avec « 1,5 à 2 g » : 0,5 g", fontsize=8.5)
ax1.set_xlabel("distance du centre du corps à la paire [m]")
ax1.set_ylabel(f"différence de pesanteur sur {TAILLE_CORPS:g} m d'étendue radiale [g₀]")
ax1.set_title("(a) Marée « tête-pieds » subie par un occupant ([HYP] : étendue radiale 1 m)", fontsize=10)
ax1.legend(fontsize=8.5)
Ms = np.logspace(10.5, 13, 200)
r2 = np.sqrt(2 * G * Ms / (2 * G0))
r15 = np.sqrt(2 * G * Ms / (1.5 * G0))
ax2.fill_between(Ms, r2, r15, color=col["jaune"], alpha=0.8, label="coquille où 1,5 g ≤ |g| ≤ 2 g")
ax2.plot(Ms, r2, color=col["rouge"], lw=1.5, label="|g| = 2 g")
ax2.plot(Ms, r15, color=col["orange"], lw=1.5, label="|g| = 1,5 g")
ax2.axhspan(1.0, 3.0, color=col["gris"], alpha=0.15, label="distances 1 à 3 m")
ax2.set_xscale("log")
ax2.set_xlabel("masse M de chaque singularité [kg]")
ax2.set_ylabel("distance au centre [m]")
ax2.set_ylim(0, 5)
ax2.set_title("(b) La zone « 1,5–2 g » est une coquille mince : épaisseur = 15,5 % du rayon", fontsize=10)
ax2.legend(fontsize=8.5, loc="upper left")
cc.titre(fig, "S05 — Marées : un champ en 1/r² ne peut pas donner « 1,5 à 2 g » uniformément dans un habitacle")
cc.sauver_figure(fig, FIG / "S05_fig2_marees.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : dilatation temporelle et entraînement ----------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.8))
ax = axes[0]
dil = -potentiel(P, M_D, D_REF) / C**2
pc = ax.pcolormesh(X, Y, dil, norm=LogNorm(vmin=3e-16, vmax=3e-14), cmap="plasma", shading="auto")
cs = ax.contour(X, Y, dil, levels=[5e-16, 1e-15, 2e-15, 5e-15], colors="white", linewidths=0.8)
ax.clabel(cs, fmt=lambda v: cc.sci(v, 1), fontsize=7.5)
ax.set_aspect("equal")
ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.set_title("(a) dt/dτ − 1 = −Φ/c², hypothèse D (2 × 10¹² kg)\n(revendiqué : 8,8×10⁴)", fontsize=10)
ax.grid(False)
fig.colorbar(pc, ax=ax, fraction=0.046, pad=0.03, label="dt/dτ − 1")

ax = axes[1]
xz = np.linspace(-4, 4, 401)
XZ, ZZ = np.meshgrid(xz, xz)
Pxz = np.stack([XZ, 0 * XZ, ZZ], axis=-1)
J_tot = np.array([0, 0, 2 * G * M_D**2 / C + M_D * D_REF**2 * omega_kepler(M_D, D_REF) / 2])
Om_lt = np.linalg.norm(champ_gm_dipole(Pxz, J_tot), axis=-1) / C
Om_lt[np.hypot(XZ, ZZ) < 0.3] = np.nan
pc = ax.pcolormesh(XZ, ZZ, Om_lt, norm=LogNorm(vmin=10**np.floor(np.log10(np.nanmin(Om_lt))), vmax=10**np.ceil(np.log10(np.nanmax(Om_lt)))),
                   cmap="cividis", shading="auto")
Bv = champ_gm_dipole(Pxz, J_tot)
ax.streamplot(XZ, ZZ, Bv[..., 0], Bv[..., 2], color="white", density=0.9, linewidth=0.6, arrowsize=0.7)
ax.set_aspect("equal")
ax.set_xlabel("x [m]")
ax.set_ylabel("z [m] (axe de rotation)")
ax.set_title("(b) Entraînement des référentiels $\\Omega_{LT}$, hypothèse D\n(spins maximaux + orbite képlérienne ; dipôle, r ≫ d)", fontsize=10)
ax.grid(False)
fig.colorbar(pc, ax=ax, fraction=0.046, pad=0.03, label="$\\Omega_{LT}$ [rad/s]")

ax = axes[2]
etiquettes, valeurs, couleurs = [], [], []
for nom, M in HYPOTHESES_M.items():
    etiquettes.append(nom.split(" (")[0])
    valeurs.append(tableau[nom]["dilatation_dt_dtau_moins_1_a_1.0m"])
    couleurs.append(col["bleu"])
etiquettes.append("REVENDIQUÉ\n(10 ans/h)")
valeurs.append(FACTEUR)
couleurs.append(col["rouge"])
ax.barh(range(len(valeurs)), valeurs, color=couleurs)
ax.set_xscale("log")
ax.set_yticks(range(len(valeurs)))
ax.set_yticklabels(etiquettes, fontsize=8.5)
for i, v in enumerate(valeurs):
    ax.text(v * 2, i, cc.sci(v, 2), va="center", fontsize=8.5)
ax.set_xlim(1e-27, 1e9)
ax.set_xlabel("dt/dτ − 1 à 1 m de la paire")
ax.set_title(f"(c) dt/dτ − 1 à 1 m : il manque {comparaison['ecart_decades_M_1e12kg']:.0f} à {comparaison['ecart_decades_M_113kg']:.0f} ordres de grandeur", fontsize=10)
ax.grid(axis="y", visible=False)
cc.titre(fig, "S05 — Champ faible : dilatation temporelle et entraînement des référentiels autour de la paire de masses")
cc.sauver_figure(fig, FIG / "S05_fig3_dilatation_entrainement.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 4 : ondes gravitationnelles ---------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.6))
Ms = np.logspace(1.5, 13.5, 200)
for d, ls in zip(SEPARATIONS, ("--", "-")):
    ax1.loglog(Ms, puissance_og_quadrupole(Ms, d, omega_kepler(Ms, d)), color=col["bleu"], ls=ls, lw=2, label=(f"d = {d:g} m (orbite képlérienne)".replace(".", ",") + (" — entraxe de DOC-007" if d == D_DOC else " [HYP]")))
    ax2.loglog(Ms, peters_temps_coalescence(Ms, Ms, d) / cc.ANNEE, color=col["rouge"], ls=ls, lw=2, label=(f"d = {d:g} m".replace(".", ",") + (" — entraxe de DOC-007" if d == D_DOC else " [HYP]")))
for nom, M in HYPOTHESES_M.items():
    ax1.plot(M, puissance_og_quadrupole(M, D_REF, omega_kepler(M, D_REF)), "o", color="k", ms=5)
    ax1.annotate(nom.split(" :")[0], (M, puissance_og_quadrupole(M, D_REF, omega_kepler(M, D_REF))), textcoords="offset points", xytext=(5, -10), fontsize=8.5)
    ax2.plot(M, peters_temps_coalescence(M, M, D_REF) / cc.ANNEE, "o", color="k", ms=5)
    ax2.annotate(nom.split(" :")[0], (M, peters_temps_coalescence(M, M, D_REF) / cc.ANNEE), textcoords="offset points", xytext=(5, 5), fontsize=8.5)
ax1.axhspan(*REV["puissance_W"], color=col["orange"], alpha=0.5, label="« 300–500 MW » (pour comparaison d'échelle)")
ax1.set_xlabel("masse M de chaque singularité [kg]")
ax1.set_ylabel("puissance rayonnée en ondes gravitationnelles [W]")
ax1.set_title("(a) Formule du quadrupôle : P = (32/5) G⁴M⁵·2 / (c⁵d⁵)", fontsize=10)
ax1.legend(fontsize=8.5, loc="upper left")
ax2.axhline(cc.AGE_UNIVERS / cc.ANNEE, color=col["gris"], ls=":", lw=1.5)
ax2.text(50, cc.AGE_UNIVERS / cc.ANNEE * 3, "âge de l'Univers", color=col["gris"], fontsize=8.5)
ax2.set_xlabel("masse M de chaque singularité [kg]")
ax2.set_ylabel("temps de coalescence de Peters [années]")
ax2.set_title("(b) Temps de coalescence : $t_c = (5/256)\\,c^5 d^4/(2G^3M^3)$", fontsize=10)
ax2.legend(fontsize=8.5)
cc.titre(fig, "S05 — Rayonnement gravitationnel de la paire en rotation et temps de coalescence")
cc.sauver_figure(fig, FIG / "S05_fig4_ondes_gravitationnelles.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 5. Résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S05_champ_faible_c204",
    "avertissement": cc.MENTION,
    "hypotheses": {"masses_kg": HYPOTHESES_M, "separation_reference_m": D_REF, "separation_documentaire_m": D_DOC, "etendue_corps_m": TAILLE_CORPS},
    "masse_par_singularite_pour_2g_a_1m_kg": M_2G_1M,
    "tableau_par_hypothese": tableau,
    "comparaison_revendications": comparaison,
    "modulation_du_champ_par_la_rotation": modulation,
    "separations_m": {"entraxe_documentaire_equipe_A": D_DOC, "incertitude_entraxe_m": 0.025, "hypothese_equipe_D": D_REF},
    "sensibilite_des_champs_a_la_separation": sensibilite_d,
    "epaisseur_relative_coquille_1p5_2g": float(np.sqrt(2 / 1.5) - 1),
    "reperes_validation": {"P_OG_Terre_Soleil_W": P_ts, "GPB_mas_par_an": gpb, "GPS_microsecondes_par_jour": gps},
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S05_resultats.json", resultats)
val.imprimer_bilan()
print("S05 terminé.")
