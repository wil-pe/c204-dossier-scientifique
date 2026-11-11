# -*- coding: utf-8 -*-
"""S07 — Besoins en énergie négative : trou de ver de Morris-Thorne (gorge de 1 m), bulle
d'Alcubierre (rayon de quelques mètres), comparés à la densité d'énergie Casimir ; lois d'échelle.

SIMULATION ILLUSTRATIVE : on évalue le tenseur énergie-impulsion qu'EXIGERAIENT ces géométries si
on les posait a priori (« ingénierie métrique à rebours »). Aucune source connue ne fournit une
telle matière ; l'effet Casimir est réel mais fournit des densités négatives infimes et un bilan
global positif. Ni un trou de ver ni une bulle de distorsion ne sont, seuls, des machines à
remonter le temps. Ce n'est pas une preuve expérimentale.

Exécution :  .venv/bin/python 05_simulations/S07_energie_negative/s07_energie_negative.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402
from matplotlib.colors import SymLogNorm  # noqa: E402

cc.configurer_matplotlib()
np.seterr(divide="ignore", invalid="ignore", over="ignore")
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S07_energie_negative")
col = cc.COULEURS
G, C, HBAR = cc.G, cc.C, cc.HBAR
K_E = C**4 / (8 * np.pi * G)        # c⁴/(8πG) = 4,82e42 N : « raideur » de l'espace-temps

# ---------------------------------------------------------------------------
# 1. Trou de ver de Morris-Thorne :  ds² = −e^{2Φ} c²dt² + dr²/(1 − b/r) + r² dΩ²
# ---------------------------------------------------------------------------
# Équations d'Einstein (Morris & Thorne 1988), repère orthonormé statique :
#   ρc² = K_E b'/r² ;  τ = K_E [b/r³ − 2(1 − b/r)Φ'/r] (tension radiale) ;
#   p = (r/2)[(ρc² − τ)Φ' − τ'] − τ (pression latérale).
# Condition d'évasement à la gorge : τ0 > ρ0c²  (matière « exotique », violation de la condition
# d'énergie nulle).


def mt_modele_ellis(r, b0):
    """Φ = 0, b = b0²/r (forces de marée nulles). Retourne (ρc², τ, p) en J/m³ = Pa."""
    x = K_E * b0**2 / r**4
    return -x, x, x


def mt_modele_b_constant(r, b0):
    """Φ = 0, b = b0 : densité NULLE partout mais tension τ = K_E b0/r³ (exotique quand même)."""
    return 0.0 * r, K_E * b0 / r**3, K_E * b0 / (2 * r**3)


def mt_modele_benin(r, b0, a0):
    """« Absurdement bénin » (Morris & Thorne) : b = b0[1 − (r − b0)/a0]², Φ = 0 pour b0 ≤ r ≤ b0 + a0,
    espace plat au-delà : la matière exotique est confinée dans une coquille d'épaisseur a0."""
    u = np.clip(1 - (r - b0) / a0, 0, None)
    b = b0 * u**2
    db = -2 * b0 * u / a0
    rho = K_E * db / r**2
    tau = K_E * b / r**3
    dtau = K_E * (db / r**3 - 3 * b / r**4)
    p = (r / 2) * (-dtau) - tau
    return rho, tau, p


def mt_masse_exotique(b0):
    """∫ρ 4πr² dr (volume coordonnée, de la gorge à l'infini, un seul côté) = −b0 c²/(2G) [kg]."""
    return -b0 * C**2 / (2 * G)


def mt_tension_gorge(b0):
    return K_E / b0**2


print("S07 — tests de validation")
# 1.1 Vérification formelle des équations de Morris-Thorne (sympy), composantes mixtes G^μ_ν
t_, r_, th_, ph_ = sp.symbols("t r theta phi", positive=True)
b0s, a0s = sp.symbols("b0 a0", positive=True)


def einstein_mixte(g, coords):
    n = 4
    ginv = g.inv()
    Gam = [[[sum(ginv[i, l] * (sp.diff(g[l, j], coords[k]) + sp.diff(g[l, k], coords[j]) - sp.diff(g[j, k], coords[l]))
                 for l in range(n)) / 2 for k in range(n)] for j in range(n)] for i in range(n)]
    Ric = sp.zeros(n, n)
    for j in range(n):
        for k in range(j, n):
            e = sum(sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k]) for i in range(n))
            e += sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for i in range(n) for l in range(n))
            Ric[j, k] = Ric[k, j] = sp.simplify(e)
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    Ein = Ric - g * Rs / 2
    return (ginv * Ein).applyfunc(sp.simplify)


symb = {}
for nom, b_expr in (("Ellis b = b0²/r", b0s**2 / r_), ("bénin b = b0(1 − (r − b0)/a0)²", b0s * (1 - (r_ - b0s) / a0s)**2)):
    g = sp.diag(-1, 1 / (1 - b_expr / r_), r_**2, r_**2 * sp.sin(th_)**2)
    Gm = einstein_mixte(g, (t_, r_, th_, ph_))
    rho_f = sp.diff(b_expr, r_) / r_**2                   # 8πρ
    tau_f = b_expr / r_**3                                # 8πτ  (Φ = 0)
    p_f = (r_ / 2) * (-sp.diff(tau_f, r_)) - tau_f        # 8πp
    res = [sp.simplify(-Gm[0, 0] - rho_f), sp.simplify(-Gm[1, 1] - tau_f), sp.simplify(Gm[2, 2] - p_f), sp.simplify(Gm[3, 3] - p_f)]
    symb[nom] = all(e == 0 for e in res)
    val.verifier_vrai(f"Morris-Thorne ({nom}) : G^t_t = −8πρ, G^r_r = −8πτ, G^θ_θ = G^φ_φ = 8πp (calcul formel)", symb[nom])

# 1.2 Intégrales numériques ↔ formules fermées (gorge b0 = 1 m)
B0 = 1.0
m_num = quad(lambda r: mt_modele_ellis(r, B0)[0] / C**2 * 4 * np.pi * r**2, B0, np.inf)[0]
val.verifier("MT (Ellis) : masse exotique ∫ρ dV numérique ↔ −b0c²/(2G)", m_num, mt_masse_exotique(B0), tol_rel=1e-8)
A0 = 0.1
m_ben = quad(lambda r: mt_modele_benin(r, B0, A0)[0] / C**2 * 4 * np.pi * r**2, B0, B0 + A0)[0]
val.verifier("MT (bénin, a0 = 0,1 m) : même masse exotique −b0c²/(2G), indépendante de a0", m_ben, mt_masse_exotique(B0), tol_rel=1e-8)
val.verifier("MT : tension à la gorge pour b0 = 10 m ≈ 5e40 Pa (5e41 dyn/cm², Morris & Thorne 1988)", mt_tension_gorge(10.0), 5e40, tol_rel=0.05)
vkd = quad(lambda r: (mt_modele_ellis(r, B0)[0] - mt_modele_ellis(r, B0)[1]) * 4 * np.pi * r**2, B0, np.inf)[0]
val.verifier("MT (Ellis) : ∫(ρc² − τ) dV = −(c⁴/G) b0 (quantificateur de Visser-Kar-Dadhich, un côté)", vkd, -C**4 / G * B0, tol_rel=1e-8)

# ---------------------------------------------------------------------------
# 2. Bulle d'Alcubierre :  ds² = −c²dt² + (dx − v f(r_s) dt)² + dy² + dz²
# ---------------------------------------------------------------------------


def alc_f(r, R, sigma):
    return (np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))) / (2 * np.tanh(sigma * R))


def alc_df(r, R, sigma):
    return sigma * (1 / np.cosh(sigma * (r + R))**2 - 1 / np.cosh(sigma * (r - R))**2) / (2 * np.tanh(sigma * R))


def alc_densite(x, rho_c, R, sigma, v):
    """Densité d'énergie mesurée par les observateurs eulériens [J/m³] :
    ρ_E = −(c²v²/(32πG)) (ρ_c²/r_s²) f'(r_s)²   (toujours ≤ 0)."""
    rs = np.hypot(x, rho_c)
    return -(C**2 * v**2 / (32 * np.pi * G)) * (rho_c**2 / rs**2) * alc_df(rs, R, sigma)**2


def alc_energie(R, sigma, v):
    """E = ∫ρ_E d³x = −(c²v²/(12G)) ∫₀^∞ r² f'² dr  [J]."""
    integ = quad(lambda r: r**2 * alc_df(r, R, sigma)**2, 0, R + 40 / sigma, points=[R], limit=400)[0]
    return -(C**2 * v**2 / (12 * G)) * integ


def alc_energie_paroi_mince(R, sigma, v):
    return -(C**2 * v**2 / (12 * G)) * R**2 * sigma / 3


def alc_energie_pfenning_ford(R, Delta, v):
    """Paroi linéaire par morceaux d'épaisseur Δ : E = −(c²v²/(12G)) (R²/Δ + Δ/12) (Pfenning & Ford 1997)."""
    return -(C**2 * v**2 / (12 * G)) * (R**2 / Delta + Delta / 12)


# 2.1 Vérification formelle : G^{tt} = −¼[(∂_yF)² + (∂_zF)²] pour un décalage F(t,x,y,z) quelconque
ts, xs, ys, zs = sp.symbols("t x y z", real=True)
Ff = sp.Function("F")(ts, xs, ys, zs)
g_alc = sp.Matrix([[-1 + Ff**2, -Ff, 0, 0], [-Ff, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
coords = (ts, xs, ys, zs)
ginv = g_alc.inv().applyfunc(sp.simplify)
Gam = [[[sum(ginv[i, l] * (sp.diff(g_alc[l, j], coords[k]) + sp.diff(g_alc[l, k], coords[j]) - sp.diff(g_alc[j, k], coords[l]))
             for l in range(4)) / 2 for k in range(4)] for j in range(4)] for i in range(4)]
Ric = sp.zeros(4, 4)
for j in range(4):
    for k in range(j, 4):
        e = sum(sp.diff(Gam[i][j][k], coords[i]) - sp.diff(Gam[i][j][i], coords[k]) for i in range(4))
        e += sum(Gam[i][i][l] * Gam[l][j][k] - Gam[i][k][l] * Gam[l][j][i] for i in range(4) for l in range(4))
        Ric[j, k] = Ric[k, j] = sp.expand(e)
Rs = sp.expand(sum(ginv[i, j] * Ric[i, j] for i in range(4) for j in range(4)))
Gup_tt = sp.expand(sum(ginv[0, i] * ginv[0, j] * (Ric[i, j] - g_alc[i, j] * Rs / 2) for i in range(4) for j in range(4)))
residu_alc = sp.simplify(Gup_tt + (sp.diff(Ff, ys)**2 + sp.diff(Ff, zs)**2) / 4)
symb["Alcubierre G^tt"] = bool(residu_alc == 0)
val.verifier_vrai("Alcubierre : G^{tt} ≡ −¼[(∂_yF)² + (∂_zF)²] pour tout décalage F (calcul formel) → ρ_E ≤ 0", symb["Alcubierre G^tt"])

# 2.2 Intégrales
R_B, SIG_B, V_B = 3.0, 8.0, C
E_rad = alc_energie(R_B, SIG_B, V_B)
# intégration 3D indépendante en coordonnées cylindriques (x, ρ_c) : d³x = 2π ρ_c dρ_c dx
xg = np.linspace(-6, 6, 2401)
rg = np.linspace(0, 6, 1201)
XG, RG = np.meshgrid(xg, rg)
dens = alc_densite(XG, RG, R_B, SIG_B, V_B)
dens[~np.isfinite(dens)] = 0.0
E_3d = np.trapezoid(np.trapezoid(dens * 2 * np.pi * RG, xg, axis=1), rg)
val.verifier("Alcubierre : énergie par intégrale radiale ↔ intégration 2D cylindrique indépendante", E_3d, E_rad, tol_rel=2e-3)
val.verifier("Alcubierre : limite de paroi mince E → −(c²v²/12G) R²σ/3 (σR = 24)", E_rad, alc_energie_paroi_mince(R_B, SIG_B, V_B), tol_rel=5e-3)
Delta_t = 0.25
E_pl_num = -(C**2 * V_B**2 / (12 * G)) * quad(lambda r: r**2 / Delta_t**2, R_B - Delta_t / 2, R_B + Delta_t / 2)[0]
val.verifier("Alcubierre : profil linéaire par morceaux ↔ formule de Pfenning & Ford (1997)", E_pl_num, alc_energie_pfenning_ford(R_B, Delta_t, V_B), tol_rel=1e-10)
# Repère de la littérature : R = 100 m, paroi Δ ~ 100 L_Planck, v = c. Pfenning & Ford (1997) concluent à une épaisseur de
# paroi de « quelques centaines de longueurs de Planck » (résumé vérifié sur arXiv gr-qc/9702026) ; le chiffre de
# −6,2e62 kg est cité DE MÉMOIRE et ne figure pas dans le résumé : REPÈRE NON VÉRIFIÉ.
# Correction n° 41 (Red Team, phase 7) : cette comparaison est retirée du décompte de validation (ramenée à ±0,3 décade
# après un premier échec à 5 %, elle ne pouvait plus échouer). La formule elle-même reste vérifiée par le test précédent.
E_pf_100 = alc_energie_pfenning_ford(100.0, 100 * cc.L_PLANCK, C) / C**2
val.consigner("repère non vérifié", "Pfenning & Ford : R = 100 m, Δ = 100 L_P, v = c → masse équivalente [kg]", E_pf_100, -6.2e62,
              commentaire="valeur de référence citée de mémoire, absente du résumé en ligne ; écart obtenu 12 % (0,05 décade)",
              constat=abs(np.log10(-E_pf_100) - np.log10(6.2e62)) < 0.3)

# ---------------------------------------------------------------------------
# 3. Effet Casimir (plaques parfaitement conductrices, T = 0)
# ---------------------------------------------------------------------------


def casimir_densite(d):
    """u = −π²ħc/(720 d⁴) [J/m³] entre deux plaques idéales distantes de d."""
    return -np.pi**2 * HBAR * C / (720 * d**4)


def casimir_pression(d):
    return -np.pi**2 * HBAR * C / (240 * d**4)


val.verifier("Casimir : pression à d = 1 µm ≈ −1,3 mPa", casimir_pression(1e-6), -1.3e-3, tol_rel=0.01)
val.verifier("Casimir : u = P/3·… relation u = P/3 (plaques idéales)", casimir_densite(1e-7) / casimir_pression(1e-7), 1 / 3, tol_rel=1e-12)

D_REALISABLE = 100e-9         # ordre de grandeur des plus petites séparations mesurées avec précision (~0,1 µm)
D_OPTIMISTE = 10e-9           # hypothèse optimiste [HYP] (idéalisation de conducteur parfait déjà invalide)
FRACTION_VIDE = 0.5           # empilement plaques/cavités moitié-moitié [HYP]
RHO_PLAQUES = 2700.0          # aluminium [kg/m³]

casimir = {}
for nom, d in (("1 µm", 1e-6), ("100 nm (réalisable)", D_REALISABLE), ("10 nm (optimiste [HYP])", D_OPTIMISTE), ("1 nm (idéalisation invalide)", 1e-9)):
    u = casimir_densite(d)
    casimir[nom] = {"d_m": d, "densite_J_m3": u, "densite_equivalente_kg_m3": u / C**2, "pression_Pa": casimir_pression(d),
                    "energie_negative_par_m3_d_empilement_J": u * FRACTION_VIDE,
                    "energie_de_masse_des_plaques_par_m3_J": RHO_PLAQUES * (1 - FRACTION_VIDE) * C**2,
                    "rapport_negatif_sur_positif": abs(u * FRACTION_VIDE) / (RHO_PLAQUES * (1 - FRACTION_VIDE) * C**2)}

# ---------------------------------------------------------------------------
# 4. Bilan chiffré
# ---------------------------------------------------------------------------
mt = {
    "gorge_b0_m": B0,
    "tension_a_la_gorge_Pa": mt_tension_gorge(B0),
    "densite_energie_gorge_modele_Ellis_J_m3": float(mt_modele_ellis(B0, B0)[0]),
    "densite_massique_gorge_kg_m3": float(mt_modele_ellis(B0, B0)[0] / C**2),
    "masse_exotique_kg": mt_masse_exotique(B0),
    "masse_exotique_masses_de_Jupiter": mt_masse_exotique(B0) / cc.M_JUPITER,
    "masse_exotique_masses_terrestres": mt_masse_exotique(B0) / cc.M_TERRE,
    "energie_exotique_J": mt_masse_exotique(B0) * C**2,
    "integrale_VKD_un_cote_J": vkd,
    "separation_casimir_pour_atteindre_la_densite_de_gorge_m": float((np.pi**2 * HBAR * C / (720 * K_E / B0**2))**0.25),
    "rapport_densite_requise_sur_casimir_100nm": float(K_E / B0**2 / abs(casimir_densite(D_REALISABLE))),
    "note_VKD": "Visser, Kar & Dadhich (2003) : la quantité intégrée de matière exotique peut en principe être rendue arbitrairement "
                "petite pour des géométries très particulières ; la violation locale à la gorge (τ0 > ρ0c²) reste obligatoire.",
}
alc = {
    "rayon_R_m": R_B, "sigma_m-1": SIG_B, "epaisseur_paroi_approx_m": 2 / SIG_B, "vitesse": "c",
    "energie_J": E_rad, "masse_equivalente_kg": E_rad / C**2, "masse_equivalente_masses_de_Jupiter": E_rad / C**2 / cc.M_JUPITER,
    "densite_min_J_m3": float(np.nanmin(dens)),
    "energie_v_0p1c_J": alc_energie(R_B, SIG_B, 0.1 * C),
    "paroi_inegalites_quantiques_Delta_m": 100 * cc.L_PLANCK,
    "energie_paroi_inegalites_quantiques_J": alc_energie_pfenning_ford(R_B, 100 * cc.L_PLANCK, C),
    "masse_paroi_inegalites_quantiques_kg": alc_energie_pfenning_ford(R_B, 100 * cc.L_PLANCK, C) / C**2,
    "masse_univers_observable_ordre_de_grandeur_kg": 1.5e53,
    "repere_Pfenning_Ford_R100m_kg": E_pf_100,
}
volume_ref = 4 / 3 * np.pi * R_B**3
comparaison = {
    "energie_casimir_disponible_dans_sphere_R3m_100nm_J": casimir_densite(D_REALISABLE) * FRACTION_VIDE * volume_ref,
    "rapport_MT_sur_casimir_sphere_1m": float(abs(mt_masse_exotique(B0) * C**2) / abs(casimir_densite(D_REALISABLE) * FRACTION_VIDE * 4 / 3 * np.pi * B0**3)),
    "rapport_Alcubierre_sur_casimir_sphere_3m": float(abs(E_rad) / abs(casimir_densite(D_REALISABLE) * FRACTION_VIDE * volume_ref)),
    "lois_d_echelle": {"MT_masse_exotique": "∝ b0", "MT_densite_et_tension_a_la_gorge": "∝ b0⁻²", "MT_gap_Casimir_equivalent": "∝ b0^(1/2)",
                       "Alcubierre_energie": "∝ v² R² σ ≈ 2 v² R²/Δ", "Casimir_densite": "∝ d⁻⁴"},
}

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
# --- Figure 1 : Morris-Thorne --------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(17, 5.7))
r = np.linspace(B0, 4.0, 1500)
ax = axes[0]
rho_e, tau_e, p_e = mt_modele_ellis(r, B0)
ax.semilogy(r, -rho_e, color=col["rouge"], lw=2, label="Ellis : −ρc² (densité NÉGATIVE)")
ax.semilogy(r, tau_e, color=col["bleu"], lw=2, ls="--", label="Ellis : tension radiale τ (= p latérale)")
rho_c, tau_c, p_c = mt_modele_b_constant(r, B0)
ax.semilogy(r, tau_c, color=col["vert"], lw=2, ls="-.", label="b = b₀ : τ (densité nulle !)")
rb = np.linspace(B0, B0 + 0.5, 600)
rho_b, tau_b, p_b = mt_modele_benin(rb, B0, 0.5)
ax.semilogy(rb, -rho_b, color=col["orange"], lw=2, label="« bénin » (a₀ = 0,5 m) : −ρc²")
ax.semilogy(rb, np.maximum(tau_b, 1e30), color=col["violet"], lw=2, ls=":", label="« bénin » : τ")
ax.set_ylim(1e39, 1e44)
ax.set_xlabel("coordonnée radiale r [m]")
ax.set_ylabel("densité d'énergie / tension [J/m³ = Pa]")
ax.set_title(f"(a) Matière requise, gorge b₀ = 1 m\nτ(gorge) = c⁴/(8πG b₀²) = {cc.sci(mt_tension_gorge(B0))} Pa", fontsize=10)
ax.legend(fontsize=7.8, loc="upper right")
ax = axes[1]
rr = np.linspace(B0, 5, 400)
z_emb = B0 * np.arccosh(rr / B0)
for s_ in (1, -1):
    ax.plot(rr, s_ * z_emb, color="k", lw=2)
    ax.plot(-rr, s_ * z_emb, color="k", lw=2)
ax.annotate("", xy=(B0, 0), xytext=(-B0, 0), arrowprops=dict(arrowstyle="<->", color=col["rouge"], lw=1.5))
ax.text(0, 0.12, "gorge : 2b₀ = 2 m", color=col["rouge"], ha="center", fontsize=9)
ax.text(0, 2.0, "univers « du haut »", ha="center", fontsize=9)
ax.text(0, -2.2, "univers « du bas »", ha="center", fontsize=9)
ax.set_aspect("equal")
ax.set_xlabel("r [m]")
ax.set_ylabel("z [m] (hauteur de plongement)")
ax.set_title("(b) Diagramme de plongement (modèle d'Ellis) : z = b₀ arccosh(r/b₀)", fontsize=10)
ax = axes[2]
b0s_ = np.logspace(-3, 3, 100)
ax.loglog(b0s_, -mt_masse_exotique(b0s_), color=col["rouge"], lw=2, label="|masse exotique| = b₀c²/(2G)  [kg]")
ax.loglog(b0s_, mt_tension_gorge(b0s_), color=col["bleu"], lw=2, ls="--", label="tension à la gorge c⁴/(8πG b₀²)  [Pa]")
for y, nom in ((cc.M_TERRE, "masse de la Terre"), (cc.M_JUPITER, "masse de Jupiter"), (cc.M_SOLEIL, "masse du Soleil")):
    ax.axhline(y, color=col["gris"], ls=":", lw=1)
    ax.text(1.2e-3, y * 1.5, nom, color=col["gris"], fontsize=8)
ax.plot(B0, -mt_masse_exotique(B0), "o", color=col["rouge"])
ax.annotate(f"b₀ = 1 m : {cc.sci(-mt_masse_exotique(B0), 2)} kg\n(≈ {-mt['masse_exotique_masses_de_Jupiter']:.2f} masse de Jupiter, NÉGATIVE)".replace(".", ","),
            (B0, -mt_masse_exotique(B0)), textcoords="offset points", xytext=(-175, 75), fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("rayon de gorge b₀ [m]")
ax.set_ylabel("kg  ou  Pa")
ax.set_ylim(1e22, 1e52)
ax.set_title("(c) Lois d'échelle : masse ∝ b₀, tension ∝ b₀⁻²", fontsize=10)
ax.legend(fontsize=8.3, loc="upper right")
cc.titre(fig, "S07 — Trou de ver traversable de Morris-Thorne à gorge de 1 m : matière exotique requise")
cc.sauver_figure(fig, FIG / "S07_fig1_morris_thorne.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : Alcubierre -------------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.7))
ax = axes[0]
XX = np.concatenate([XG[::-1][:-1], XG])            # symétrisation ρ_c → ±ρ_c pour l'affichage
RR_ = np.concatenate([-RG[::-1][:-1], RG])
DD = np.concatenate([dens[::-1][:-1], dens])
pc = ax.pcolormesh(XX, RR_, DD, cmap="RdBu", norm=SymLogNorm(linthresh=1e38, vmin=-abs(np.nanmin(dens)), vmax=abs(np.nanmin(dens))), shading="auto")
ax.add_patch(plt.Circle((0, 0), R_B, fill=False, color="k", ls="--", lw=1))
ax.annotate("", xy=(5.5, 0), xytext=(3.8, 0), arrowprops=dict(arrowstyle="->", lw=1.5))
ax.text(4.0, 0.25, "v", fontsize=11)
ax.set_aspect("equal")
ax.set_xlabel("x − x_s(t) [m] (direction du mouvement)")
ax.set_ylabel("distance transverse [m]")
ax.set_title(f"(a) Densité d'énergie eulérienne (R = 3 m, σ = 8 m⁻¹, v = c)\nmin = {cc.sci(float(np.nanmin(dens)), 2)} J/m³ ; partout ≤ 0", fontsize=10)
ax.grid(False)
fig.colorbar(pc, ax=ax, fraction=0.046, pad=0.03, label="ρ_E [J/m³] (échelle symlog)")
ax = axes[1]
rr = np.linspace(0, 6, 1000)
for sg, c in ((2.0, col["bleu"]), (8.0, col["rouge"]), (30.0, col["vert"])):
    ax.plot(rr, alc_f(rr, R_B, sg), color=c, lw=2, label=f"σ = {sg:g} m⁻¹ (paroi ≈ {2 / sg:.2g} m)".replace(".", ","))
ax.axvline(R_B, color="k", ls=":", lw=1)
ax.set_xlabel("$r_s$ [m]")
ax.set_ylabel("fonction de forme f($r_s$)")
ax.set_title("(b) Fonction de forme : f = 1 dans la bulle, 0 dehors", fontsize=10)
ax.legend(fontsize=8.5)
ax = axes[2]
Dl = np.logspace(np.log10(100 * cc.L_PLANCK), 0.3, 300)
for vv, c in ((0.1 * C, col["bleu"]), (C, col["rouge"]), (10 * C, col["violet"])):
    ax.loglog(Dl, -alc_energie_pfenning_ford(R_B, Dl, vv) / C**2, color=c, lw=2, label=f"v = {vv / C:g} c".replace(".", ","))
ax.axhline(cc.M_JUPITER, color=col["gris"], ls=":", lw=1)
ax.text(1e-30, cc.M_JUPITER * 3, "masse de Jupiter", color=col["gris"], fontsize=8.5)
ax.axhline(cc.M_SOLEIL, color=col["gris"], ls=":", lw=1)
ax.text(1e-30, cc.M_SOLEIL * 3, "masse du Soleil", color=col["gris"], fontsize=8.5)
ax.axhline(1.5e53, color=col["orange"], ls="--", lw=1.2)
ax.text(1e-30, 1.5e53 * 3, "masse de l'Univers observable (~10⁵³ kg)", color=col["orange"], fontsize=8.5)
ax.axvline(100 * cc.L_PLANCK, color="k", ls=":", lw=1)
ax.text(100 * cc.L_PLANCK * 2, 1e35, "Δ = 100 L_Planck\n(borne des inégalités quantiques,\nPfenning & Ford 1997)", fontsize=8)
ax.plot(2 / SIG_B, -E_rad / C**2, "o", color="k")
ax.annotate(f"paroi de 0,25 m :\n{cc.sci(-E_rad / C**2, 2)} kg", (2 / SIG_B, -E_rad / C**2), textcoords="offset points", xytext=(-95, 20), fontsize=8.5,
            arrowprops=dict(arrowstyle="->", lw=0.8))
ax.set_xlabel("épaisseur de paroi Δ [m]")
ax.set_ylabel("|énergie négative| / c²  [kg]")
ax.set_title("(c) |E| = (c²v²/12G)(R²/Δ + Δ/12), R = 3 m", fontsize=10)
ax.legend(fontsize=8.5, loc="upper right")
cc.titre(fig, "S07 — Bulle d'Alcubierre de 3 m de rayon : densité d'énergie négative requise et énergie totale")
cc.sauver_figure(fig, FIG / "S07_fig2_alcubierre.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : comparaison Casimir ------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
d = np.logspace(-18.5, -5, 300)
ax1.loglog(d, -casimir_densite(d), color=col["bleu"], lw=2, label="Casimir : |u| = π²ħc/(720 d⁴)")
ax1.axvspan(D_REALISABLE, 1e-5, color=col["vert"], alpha=0.2, label="séparations mesurées en laboratoire (≳ 0,1 µm)")
ax1.axvspan(d[0], 1e-9, color=col["gris"], alpha=0.15, label="d < 1 nm : idéalisation de conducteur parfait invalide")
for y, nom, c, fy in ((K_E / B0**2, "Morris-Thorne, gorge 1 m : 4,8×10⁴² J/m³", col["rouge"], 2e-4),
                      (abs(np.nanmin(dens)), f"Alcubierre (R = 3 m, v = c) : {cc.sci(abs(float(np.nanmin(dens))), 2)} J/m³", col["violet"], 30.0)):
    ax1.axhline(y, color=c, ls="--", lw=1.5)
    ax1.text(3e-13, y * fy, nom, color=c, fontsize=8.5)
ax1.set_ylim(1e-9, 1e52)
ax1.plot(D_REALISABLE, -casimir_densite(D_REALISABLE), "o", color="k")
ax1.annotate(f"d = 100 nm : {cc.sci(-casimir_densite(D_REALISABLE), 2)} J/m³", (D_REALISABLE, -casimir_densite(D_REALISABLE)),
             textcoords="offset points", xytext=(-140, 22), fontsize=8.5, arrowprops=dict(arrowstyle="->", lw=0.8))
ax1.plot(mt["separation_casimir_pour_atteindre_la_densite_de_gorge_m"], K_E / B0**2, "o", color=col["rouge"])
ax1.annotate(f"d = {cc.sci(mt['separation_casimir_pour_atteindre_la_densite_de_gorge_m'], 2)} m\n(≈ 1/{cc.R_PROTON / mt['separation_casimir_pour_atteindre_la_densite_de_gorge_m']:.0f} du rayon du proton)",
             (mt["separation_casimir_pour_atteindre_la_densite_de_gorge_m"], K_E / B0**2), textcoords="offset points", xytext=(14, -62), fontsize=8.5, color=col["rouge"])
ax1.set_xlabel("séparation des plaques d [m]")
ax1.set_ylabel("|densité d'énergie négative| [J/m³]")
ax1.set_title("(a) Densité d'énergie Casimir et densités requises", fontsize=10)
ax1.legend(fontsize=8, loc="lower left")

L = np.logspace(-3, 3, 100)
ax2.loglog(L, -mt_masse_exotique(L) * C**2, color=col["rouge"], lw=2, label="Morris-Thorne : |M|c² = b₀c⁴/(2G)")
ax2.loglog(L, -alc_energie_pfenning_ford(L, L / 10, C), color=col["violet"], lw=2, label="Alcubierre, v = c, paroi Δ = R/10")
ax2.loglog(L, -alc_energie_pfenning_ford(L, 100 * cc.L_PLANCK, C), color=col["violet"], lw=2, ls=":", label="Alcubierre, v = c, paroi Δ = 100 L_Planck")
ax2.loglog(L, -casimir_densite(D_REALISABLE) * FRACTION_VIDE * 4 / 3 * np.pi * L**3, color=col["bleu"], lw=2, ls="--",
           label="Casimir disponible : sphère de rayon L remplie de cavités de 100 nm")
ax2.loglog(L, -casimir_densite(D_OPTIMISTE) * FRACTION_VIDE * 4 / 3 * np.pi * L**3, color=col["ciel"], lw=2, ls="--", label="idem, cavités de 10 nm [HYP optimiste]")
ax2.axvline(1.0, color="k", ls=":", lw=1)
ecart = np.log10(comparaison["rapport_MT_sur_casimir_sphere_1m"])
ax2.annotate("", xy=(1.0, -mt_masse_exotique(1.0) * C**2), xytext=(1.0, -casimir_densite(D_REALISABLE) * FRACTION_VIDE * 4 / 3 * np.pi),
             arrowprops=dict(arrowstyle="<->", color="k", lw=1.5))
ax2.text(1.3, 1e22, f"écart à L = 1 m :\n≈ {ecart:.0f} ordres de grandeur", fontsize=9.5, weight="bold")
ax2.set_xlabel("taille caractéristique L = b₀ ou R [m]")
ax2.set_ylabel("|énergie négative| [J]")
ax2.set_title("(b) Énergie négative requise et « disponible » en fonction de la taille", fontsize=10)
ax2.legend(fontsize=7.8, loc="upper left")
cc.titre(fig, "S07 — Énergie négative : besoins (Morris-Thorne, Alcubierre) comparés à l'effet Casimir")
cc.sauver_figure(fig, FIG / "S07_fig3_comparaison_casimir.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Résultats
# ---------------------------------------------------------------------------
resultats = {
    "simulation": "S07_energie_negative",
    "avertissement": cc.MENTION,
    "constante_c4_sur_8piG_N": K_E,
    "morris_thorne": mt,
    "alcubierre": alc,
    "casimir": casimir,
    "comparaison": comparaison,
    "verification_symbolique": symb,
    "validation": val.bilan(),
}
cc.ecrire_json(RES / "S07_resultats.json", resultats)
val.imprimer_bilan()
print("S07 terminé.")
