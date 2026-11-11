#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-08 — Déviation de la lumière : gravitationnelle (indétectable ici) contre gradient d'indice
(visible à l'œil nu). Explication alternative plausible d'une photo de « faisceau courbé ».

Calcule :
  1. α = 4GM/(c²b) pour le Soleil, la Terre, des masses de 227 kg à 1e13 kg, et la masse qu'il
     faudrait pour une courbure visible ;
  2. l'indice effectif gravitationnel n = 1 + 2GM/(rc²), comparé à l'air et à un gradient thermique ;
  3. la limite de détection angulaire (bruit de photons) et le temps d'intégration correspondant ;
  4. le tracé de rayons dans une solution sucrée stratifiée (profil de diffusion en erf) ;
  5. l'angle critique d'un mirage thermique.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import erf

from constantes import (G, c, h_planck, GM_terre, R_terre, M_soleil, R_soleil, C204, sauver, fig_chemin, sci)

L, D = [], {}
rad2as = 180 / math.pi * 3600
L.append("EXP-08 — DÉVIATION DE LA LUMIÈRE : GRAVITATION CONTRE GRADIENT D'INDICE")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. déviation gravitationnelle
def alpha(M, b):
    return 4 * G * M / (c**2 * b)

L.append("1. Déviation gravitationnelle (champ faible) : α = 4GM/(c²b)")
D["gravitationnelle"] = []
m_lo, m_hi = C204["masse_TN_kg"]            # 3,9–5,1e12 kg par singularité (valeur retenue, erratum E2)
CAS = [("Soleil, rayon rasant", M_soleil, R_soleil), ("Terre, rayon rasant", GM_terre / G, R_terre),
       ("unité de 227 kg, b = 0,1 m", 227.0, 0.1),
       ("une singularité de 3,9e12 kg, b = 1 m", m_lo, 1.0), ("une singularité de 5,1e12 kg, b = 1 m", m_hi, 1.0),
       ("la paire (7,8e12 kg), b = 1 m", 2 * m_lo, 1.0), ("la paire (1,02e13 kg), b = 1 m", 2 * m_hi, 1.0),
       ("la paire (1,02e13 kg), b = 1 cm", 2 * m_hi, 0.01),
       ("masse donnant « 2 g à 1 m » (2,9e11 kg), b = 1 m", 2 * 9.80665 / G, 1.0),
       ("ancienne fourchette v1 : 1e11 kg, b = 1 m", 1e11, 1.0), ("ancienne fourchette v1 : 1e12 kg, b = 1 m", 1e12, 1.0)]
for nom, M, b in CAS:
    a = alpha(M, b)
    D["gravitationnelle"].append({"cas": nom, "M": M, "b": b, "alpha_rad": a})
    L.append(f"   {nom:<48} α = {sci(a)} rad = {sci(a*rad2as)}″ ; déplacement à 10 m : {sci(a*10)} m")
L.append("   (Soleil : 1,75″, valeur d'Einstein vérifiée en 1919 puis à ~1e-4 près par VLBI ; Shapiro et al. 2004)")
for ang_deg in (0.1, 1.0, 10.0):
    M_need = math.radians(ang_deg) * c**2 * 1.0 / (4 * G)
    L.append(f"   pour dévier de {ang_deg:>4}° à b = 1 m il faudrait M = {sci(M_need)} kg = {M_need/(GM_terre/G):.2g} masse terrestre "
             f"(rayon de Schwarzschild {2*G*M_need/c**2*1000:.2g} mm)")
D["masse_pour_1_degre_kg"] = math.radians(1.0) * c**2 / (4 * G)
L.append("")

# ---------------------------------------------------------------- 2. indice effectif
n_air = 2.7e-4
dn_dT = -n_air / 293.0
L.append("2. Comparaison en termes d'indice de réfraction effectif")
M_ref = 2 * m_hi                             # la paire, borne haute : cas le plus favorable à l'affirmation
L.append(f"   gravitation : n - 1 = 2GM/(rc²) = {sci(2*G*M_ref/c**2)} à 1 m de la paire de singularités (1,02e13 kg)")
L.append(f"   air ambiant : n - 1 ≈ {n_air:.1e} ; dn/dT ≈ -(n-1)/T = {sci(dn_dT)} K⁻¹")
D["indice"] = {"grav_paire_1m": 2 * G * M_ref / c**2, "dn_dT_air": dn_dT}
for gradT in (1.0, 20.0, 100.0, 1000.0):
    courb = abs(dn_dT) * gradT           # rad par mètre de trajet
    L.append(f"   gradient thermique transverse de {gradT:>6.0f} K/m : courbure {sci(courb)} rad/m "
             f"= {courb/alpha(M_ref,1.0):.1e} × la déviation TOTALE par la paire (1,02e13 kg) à 1 m")
L.append("   Une unité revendiquée « à 38–49 °C » dans un habitacle à ~20 °C crée des gradients de 10²–10³ K/m près")
L.append("   de ses parois : l'effet thermique dépasse l'effet gravitationnel de la paire de 9 à 10 ordres de grandeur.")
L.append("")

# ---------------------------------------------------------------- 3. limite de détection
lam, P_laser, w0 = 633e-9, 1e-3, 1e-3
N_ph = P_laser / (h_planck * c / lam)
div = lam / (math.pi * w0)
dtheta = div / math.sqrt(N_ph)          # rad/√Hz, ordre de grandeur (détecteur à quadrants idéal)
L.append("3. Limite de détection angulaire d'un laser de classe 2 (1 mW, 633 nm, col w0 = 1 mm)")
L.append(f"   flux de photons {sci(N_ph)} /s ; divergence λ/(πw0) = {sci(div)} rad")
L.append(f"   bruit de photons sur la direction : ≈ divergence/√N = {sci(dtheta)} rad/√Hz (borne idéale)")
D["detection"] = {"bruit_rad_rtHz": dtheta, "temps_s": {}}
for M in (m_lo, m_hi, 2 * m_hi, 1e12):
    t = (3 * dtheta / alpha(M, 1.0))**2
    D["detection"]["temps_s"][f"{M:.2e}"] = t
    L.append(f"   temps d'intégration pour voir α({M:.2e} kg, 1 m) à 3σ : {sci(t)} s = {t/86400:.3g} jours "
             f"(avec modulation parfaite de la masse et zéro dérive — irréaliste)")
L.append("   En pratique la stabilité de pointé (µrad), la turbulence de l'air (~µrad sur 1 m) et les dérives")
L.append("   mécaniques fixent le plancher 7 à 8 ordres de grandeur au-dessus de α ≈ 1–3e-14 rad : INDÉTECTABLE.")
L.append("")

# ---------------------------------------------------------------- 4. solution sucrée stratifiée
n_eau, n_sirop = 1.333, 1.45          # eau ; sirop de saccharose ~65 % en masse
D_diff = 5.0e-10                      # m²/s, saccharose dans l'eau (ordre de grandeur, dilué)
y0 = 0.05                             # hauteur de l'interface initiale (m)

def n_profil(y, t):
    s = 2 * math.sqrt(D_diff * t)
    return n_eau + 0.5 * (n_sirop - n_eau) * (1 - erf((y - y0) / s))

def dn_dy(y, t):
    s = 2 * math.sqrt(D_diff * t)
    return -(n_sirop - n_eau) / (s * math.sqrt(math.pi)) * np.exp(-((y - y0) / s)**2)

def rayon(y_in, pente_in, t, Lcuve=0.40):
    """Équation des rayons (approx. paraxiale exacte en n) : d/dx (n dy/ds) = dn/dy ; ici y'' ≈ (1+y'²)·n'/n."""
    def f(x, u):
        y, yp = u
        return [yp, (1 + yp**2) * dn_dy(y, t) / n_profil(y, t)]
    sol = solve_ivp(f, [0, Lcuve], [y_in, pente_in], max_step=1e-3, rtol=1e-8)
    return sol.t, sol.y[0]

theta_max = math.acos(n_eau / n_sirop)      # invariant de Snell n·cos θ = cste pour un rayon initialement horizontal
L.append("4. Cuve d'eau sucrée stratifiée (sirop n ≈ 1,45 sous eau n = 1,333 ; diffusion D ≈ 5e-10 m²/s)")
L.append(f"   déviation maximale d'un rayon entré horizontalement dans l'eau : arccos(n_eau/n_sirop) = {math.degrees(theta_max):.1f}°")
D["sucre"] = []
D["theta_max_deg"] = math.degrees(theta_max)
for jours in (0.25, 1.0, 3.0, 7.0):
    t = jours * 86400
    s = 2 * math.sqrt(D_diff * t)
    gmax = (n_sirop - n_eau) / (s * math.sqrt(math.pi))
    Rc = (n_eau + n_sirop) / 2 / gmax
    x, y = rayon(y0 + 0.2 * s, 0.0, t, Lcuve=0.10)
    chute = y[0] - y[-1]
    angle = math.degrees(math.atan(abs((y[-1] - y[-2]) / (x[-1] - x[-2]))))
    D["sucre"].append({"jours": jours, "epaisseur_mm": s * 1000, "gradient_max_par_m": gmax, "rayon_courbure_m": Rc,
                       "chute_mm_sur_10cm": chute * 1000, "angle_deg_apres_10cm": angle})
    L.append(f"   après {jours:>4} j : épaisseur 2√(Dt) = {s*1000:5.1f} mm ; dn/dy max = {gmax:5.1f} m⁻¹ ; rayon de courbure minimal "
             f"{Rc*100:5.1f} cm ; après 10 cm de trajet : descente {chute*1000:5.1f} mm, inclinaison {angle:4.1f}°")
courb_sucre = D["sucre"][1]["gradient_max_par_m"] / 1.39
L.append(f"   Courbure du rayon dans la couche (1 jour) : ~{courb_sucre:.1f} rad/m, à comparer aux {sci(alpha(M_ref,1.0))} rad AU TOTAL")
L.append(f"   produits par la paire (1,02e13 kg) à 1 m : rapport ~{courb_sucre*0.1/alpha(M_ref,1.0):.0e} sur 10 cm de trajet.")
L.append("   Un rayon injecté légèrement vers le haut depuis le sirop décrit une arche et retombe (« mirage en cuve »).")
L.append("")

# ---------------------------------------------------------------- 5. mirage
L.append("5. Mirage thermique (air chaud sous air froid) : angle rasant critique θ_c ≈ √(2·Δn/n), Δn = |dn/dT|·ΔT")
D["mirage"] = []
for dT in (5.0, 20.0, 40.0):
    th = math.sqrt(2 * abs(dn_dT) * dT)
    D["mirage"].append({"dT": dT, "theta_c_rad": th})
    L.append(f"   ΔT = {dT:>4.0f} K : θ_c = {th*1e3:.1f} mrad = {math.degrees(th):.2f}°")
L.append("")
# ---------------------------------------------------------------- 6. confrontation à la photo C204-DOC-012
# Lecture visuelle (Équipe F, confiance FAIBLE) de la copie agrandie 01_archive/ameliores/alt_laser_fetch_x5.png :
# trait rouge rectiligne sur ~2/3 de sa longueur, puis courbé d'environ 45–65° sur le dernier tiers, interrompu dans l'air ;
# échelle supposée sur la largeur d'une main (~0,1 m) : rayon de courbure de l'ordre de 0,1 m [HYP]. Projection 2D d'une
# scène 3D : ces valeurs ne sont que des ordres de grandeur.
angle_photo = math.radians(55.0)
Rc_photo = 0.10
g_requis = c**2 / (2 * Rc_photo)                    # courbure d'un rayon dans un champ transverse g : 1/R = 2g/c²
R_2g = c**2 / (2 * 2 * 9.80665)
dn_max_air = 2.7e-4                                  # tout l'écart d'indice entre l'air et le vide
dev_max_vide_air = math.sqrt(2 * dn_max_air)
dn_30K = abs(dn_dT) * 30.0
dev_max_30K = math.sqrt(2 * dn_30K)
gradient_requis = 1.0 / Rc_photo                     # dn/dy ≈ n/R
L.append("6. Confrontation à la photographie dite « du laser » (C204-DOC-012, 252×206 px ; lecture visuelle, confiance faible)")
L.append(f"   courbure apparente : ≈ 45–65° sur le dernier tiers du trait ; rayon de courbure ~{Rc_photo*100:.0f} cm [HYP d'échelle]")
L.append(f"   • gravitation : un rayon de courbure R exige un champ transverse g = c²/(2R) = {sci(g_requis)} m/s² = {g_requis/9.80665:.1e} g ;")
L.append(f"     avec les « 2 g » revendiqués, R = c²/(2·2g) = {sci(R_2g)} m ({R_2g/9.4607e15:.2f} année-lumière) : écart de {g_requis/(2*9.80665):.0e}.")
L.append(f"   • réfraction dans l'AIR : la déviation totale d'un rayon rasant est bornée par √(2Δn) ; même entre le vide et l'air")
L.append(f"     (Δn = 2,7e-4) : {math.degrees(dev_max_vide_air):.2f}° ; pour un écart thermique de 30 K : {math.degrees(dev_max_30K):.2f}°.")
L.append(f"     Courber un rayon à R = {Rc_photo*100:.0f} cm demande dn/dy ≈ {gradient_requis:.0f} m⁻¹ : accessible dans un liquide stratifié")
L.append(f"     ({D['sucre'][0]['gradient_max_par_m']:.0f} m⁻¹ dans la cuve sucrée après 6 h), IMPOSSIBLE dans l'air (≲ 1e-3 m⁻¹).")
L.append("   → ni la gravité ni la réfraction dans l'air n'expliquent une courbure de ~50° sur ~10 cm. Si la scène est bien")
L.append("     dans l'air (légende : faisceau rendu visible par de la fumée), il reste des explications ordinaires d'une autre")
L.append("     nature : guide de lumière souple à émission latérale, pose longue avec source mobile, retouche [HYP ; aucune")
L.append("     n'est démontrable sur une image de 252 px — cf. Équipe A, incohérence I-11].")
D["doc012"] = {"angle_deg": 55.0, "Rc_m": Rc_photo, "g_requis_m_s2": g_requis, "g_requis_en_g": g_requis / 9.80665,
               "R_pour_2g_m": R_2g, "deviation_max_vide_air_deg": math.degrees(dev_max_vide_air),
               "deviation_max_30K_deg": math.degrees(dev_max_30K), "gradient_requis_par_m": gradient_requis}
L.append("")
L.append("Conclusion : un gradient d'indice courbe visiblement un faisceau dans un LIQUIDE stratifié (expérience N1), pas")
L.append("dans l'air. La déviation gravitationnelle par les masses retenues (3,9e12 à 1,0e13 kg) à 1 m vaut 1,2e-14 à 3,0e-14 rad :")
L.append("ni l'œil ni un appareil photo ne peuvent la voir. Une courbure photographiable n'est donc JAMAIS gravitationnelle ici.")

sauver("calc08_deviation_lumiere", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2))
ax = axes[0]
t = 86400.0
s = 2 * math.sqrt(D_diff * t)
yy = np.linspace(0, 0.10, 300)
fond = ax.pcolormesh(np.linspace(0, 0.40, 2) * 100, yy * 100, np.tile(n_profil(yy, t), (2, 1)).T, cmap="YlOrBr",
                     shading="auto", alpha=0.85)
for y_in, pente in ((0.075, -0.05), (0.068, -0.03), (0.062, 0.0), (0.056, 0.0), (0.052, 0.04), (0.045, 0.08)):
    x, y = rayon(y_in, pente, t)
    ok = (y > 0) & (y < 0.10)
    ax.plot(x[ok] * 100, y[ok] * 100, color="#b5179e", lw=1.6)
fig.colorbar(fond, ax=ax, label="indice de réfraction n(y)")
ax.set_xlim(0, 40)
ax.set_xlabel("distance dans la cuve (cm)")
ax.set_ylabel("hauteur (cm) — échelle verticale dilatée ×2,5")
ax.set_title("Rayons laser dans une solution sucrée stratifiée (1 jour de diffusion)\n"
             "tracé de rayons illustratif — la lumière se courbe vers l'indice fort", fontsize=9.5)

ax = axes[1]
noms = ["gravitation, 227 kg\n(b = 0,1 m)", "gravitation, une singularité\n4,4e12 kg (b = 1 m)",
        "gravitation, la paire\n1,0e13 kg (b = 1 m)",
        "Terre (rasant)", "bruit de photons\n1 mW, 1 s", "air : 1 K/m sur 1 m", "Soleil (rasant)",
        "air chaud : 100 K/m\nsur 1 m", "air : borne absolue\n(vide → air)", "eau sucrée stratifiée\n(déviation maximale)",
        "courbure apparente\nsur DOC-012 (≈ 55°)"]
vals = [alpha(227, 0.1), alpha(C204["masse_TN_centrale_kg"], 1), alpha(2 * m_hi, 1), alpha(GM_terre / G, R_terre), dtheta,
        abs(dn_dT) * 1.0, alpha(M_soleil, R_soleil), abs(dn_dT) * 100, dev_max_vide_air, theta_max, angle_photo]
cols = ["#33658a"] * 4 + ["gray", "#d1495b", "#33658a", "#d1495b", "#d1495b", "#d1495b", "k"]
ordre = np.argsort(vals)
ax.barh(range(len(vals)), np.array(vals)[ordre], color=np.array(cols)[ordre])
ax.set_yticks(range(len(vals)))
ax.set_yticklabels(np.array(noms)[ordre], fontsize=7.5)
ax.set_xscale("log")
ax.axvline(3e-4, color="k", ls=":", lw=1)
ax.text(3.6e-4, 0.1, "résolution de l'œil (~1′)", rotation=90, fontsize=8, va="bottom")
ax.set_xlabel("angle de déviation (rad)")
ax.set_title("Déviations comparées : gravitation (bleu) contre gradients d'indice (rouge)\ncalcul illustratif", fontsize=9.5)
ax.grid(True, which="both", axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc08_deviation_lumiere.png"), dpi=150)
print("figure :", fig_chemin("calc08_deviation_lumiere.png"))
