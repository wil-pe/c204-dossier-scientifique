# -*- coding: utf-8 -*-
"""C204 — Équipe C. Re-dérivation indépendante du rayonnement de Hawking d'un trou noir de Schwarzschild.

Méthode : intégration numérique des équations radiales (Regge-Wheeler pour s = 0, 1, 2 ; potentiels
supersymétriques de Dirac pour s = 1/2 sans masse) pour obtenir les facteurs de corps gris Gamma_l(omega),
puis sommation sur les modes :
    P  = (1/2pi) * somme_l deg_l * int domega  hbar*omega * Gamma / (exp(hbar omega/kT) -/+ 1)
Unités internes : G = c = hbar = 1, M = 1  ->  kT = 1/(8 pi).  P = alpha * hbar c^6 / (G^2 M^2).
Comparaison : Page, Phys. Rev. D 13, 198 (1976), éq. (29)-(30).

Sorties : resultats/c01_hawking.json, c01_spectre_photon.csv, c01_scenarios_puissance.csv, c01_table_masses.csv
"""
import csv
import os
import numpy as np
from scipy.integrate import solve_ivp, trapezoid, cumulative_trapezoid
from scipy.special import wrightomega
import c00_constantes as K

TH = 1.0 / (8 * np.pi)      # température de Hawking en unités M = 1


def r_de_rstar(rs):
    """Inverse de r* = r + 2 ln(r/2 - 1)  (M = 1)."""
    return 2.0 * (1.0 + np.real(wrightomega(rs / 2.0 - 1.0)))


def potentiel(r, spin, l):
    f = 1.0 - 2.0 / r
    if spin in (0, 1, 2):
        return f * (l * (l + 1) / r**2 + 2.0 * (1 - spin**2) / r**3)
    # spin 1/2 : l joue le rôle de kappa = j + 1/2 = 1, 2, 3...
    kap = l
    return kap**2 * f / r**2 + kap * np.sqrt(f) * (3.0 - r) / r**3


def transmission(omega, spin, l):
    """Probabilité de transmission Gamma_l(omega) à travers la barrière."""
    lam = l * (l + 1) if spin in (0, 1, 2) else l * (l - 1)   # coefficient du terme 1/r^2 à l'infini

    def rhs(x, y):
        r = r_de_rstar(x)
        return [y[1], -(omega**2 - potentiel(r, spin, l)) * y[0]]

    x0 = -60.0
    x1 = max(600.0, 150.0 / omega)
    y0 = [np.exp(-1j * omega * x0), -1j * omega * np.exp(-1j * omega * x0)]
    sol = solve_ivp(rhs, (x0, x1), np.array(y0, dtype=complex), method="DOP853", rtol=1e-9, atol=1e-12)
    psi, dpsi = sol.y[0, -1], sol.y[1, -1]
    r = r_de_rstar(x1)
    # base asymptotique corrigée au 1er ordre en 1/(omega r)
    corr = 1j * lam / (2 * omega * r)
    u_out = np.exp(1j * omega * x1) * (1 + corr)
    du_out = np.exp(1j * omega * x1) * (1j * omega * (1 + corr) - corr / r)
    u_in, du_in = np.conj(u_out), np.conj(du_out)
    det = u_in * du_out - u_out * du_in
    a_in = (psi * du_out - dpsi * u_out) / det
    return float(min(1.0, 1.0 / abs(a_in) ** 2))


def spectre(spin, n_l=7, x=None):
    """Retourne x = omega*M, dP/dx et dN/dx (par état d'hélicité), sommés sur les modes."""
    if x is None:
        x = np.concatenate([np.linspace(0.004, 0.1, 25), np.linspace(0.104, 1.1, 250)])
    l_min = {0: 0, 1: 1, 2: 2, 0.5: 1}[spin]
    dP = np.zeros_like(x)
    dN = np.zeros_like(x)
    for l in range(l_min, l_min + n_l):
        deg = (2 * l + 1) if spin in (0, 1, 2) else 2 * l      # 2j+1 = 2*kappa
        gam = np.array([transmission(w, spin, l) for w in x])
        stat = np.exp(x / TH) + (1.0 if spin == 0.5 else -1.0)
        dN += deg * gam / stat / (2 * np.pi)
        dP += deg * gam * x / stat / (2 * np.pi)
    return x, dP, dN


def main():
    res = {}
    spectres = {}
    for spin in (0, 0.5, 1, 2):
        x, dP, dN = spectre(spin)
        alpha = trapezoid(dP, x)          # coefficient de puissance par état d'hélicité
        beta = trapezoid(dN, x)           # taux d'émission en nombre, unités c^3/(G M)
        res[str(spin)] = dict(
            alpha_par_etat=alpha, beta_par_etat=beta,
            pic_flux_kT=float(x[np.argmax(dN)] / TH),
            pic_puissance_kT=float(x[np.argmax(dP)] / TH),
            energie_moyenne_kT=float(alpha / beta / TH))
        spectres[spin] = (x, dP, dN)
        print(f"spin {spin}: alpha/état = {alpha:.4e}  beta/état = {beta:.4e}  "
              f"pic flux = {res[str(spin)]['pic_flux_kT']:.2f} kT  pic puissance = "
              f"{res[str(spin)]['pic_puissance_kT']:.2f} kT  <E> = {res[str(spin)]['energie_moyenne_kT']:.2f} kT")

    a0, a12, a1, a2 = (res[s]["alpha_par_etat"] for s in ("0", "0.5", "1", "2"))
    b12, b1 = res["0.5"]["beta_par_etat"], res["1"]["beta_par_etat"]

    # --- Comparaison à Page (1976) : 4 « sortes » de neutrinos (états), 2 photons, 2 gravitons
    alpha_page_calc = 4 * a12 + 2 * a1 + 2 * a2
    comp = dict(
        alpha_total_calcule=alpha_page_calc, alpha_total_Page=2.011e-4,
        fraction_neutrinos=4 * a12 / alpha_page_calc, fraction_photons=2 * a1 / alpha_page_calc,
        fraction_gravitons=2 * a2 / alpha_page_calc,
        Page=dict(neutrinos=0.814, photons=0.167, gravitons=0.019),
        alpha_avec_electrons_calcule=8 * a12 + 2 * a1 + 2 * a2, alpha_avec_electrons_Page=3.6e-4)
    print("Comparaison Page 1976 :", comp)

    # --- Contenu en particules retenu pour kT ~ 2-15 MeV (M ~ 10^12 kg) :
    # photon (2 états), 3 saveurs de neutrinos x (nu, anti-nu) = 6 états, e+/e- = 4 états, graviton (2 états).
    # Muons négligés (< 10 % de la contribution e+- pour M > 6,8e11 kg d'après Page 1977).
    comp_M12 = dict(photons=2 * a1, neutrinos=6 * a12, electrons_positrons=4 * a12, gravitons=2 * a2)
    alpha_M12 = sum(comp_M12.values())
    frac_M12 = {k_: v / alpha_M12 for k_, v in comp_M12.items()}
    alpha_bb = 1.0 / (15360 * np.pi)       # corps noir de photons, aire 4 pi r_s^2 (formule du dossier §6)
    alpha_sans_masse = 2 * a1 + 6 * a12 + 2 * a2
    # Modèle standard complet (kT >> 173 GeV) : 4 scalaires (Higgs + modes longitudinaux W/Z),
    # 90 états de spin 1/2 (72 quarks + 12 leptons chargés + 6 neutrinos), 24 états de spin 1
    # (16 gluons + 2 photon + 6 W/Z transverses), 2 gravitons.
    alpha_MS = 4 * a0 + 90 * a12 + 24 * a1 + 2 * a2
    res["synthese"] = dict(
        K_hawking_W_kg2=K.K_HAWKING, alpha_corps_noir_photons_dossier=alpha_bb,
        alpha_sans_masse=alpha_sans_masse, alpha_M_1e12kg=alpha_M12, fractions_M_1e12kg=frac_M12,
        alpha_modele_standard_complet=alpha_MS,
        rapport_alpha_M12_sur_dossier=alpha_M12 / alpha_bb, comparaison_Page=comp,
        fraction_deposee_localement=frac_M12["photons"] + frac_M12["electrons_positrons"])
    print(f"alpha(M~1e12 kg) = {alpha_M12:.4e}  (dossier, corps noir photons : {alpha_bb:.4e} ; rapport "
          f"{alpha_M12 / alpha_bb:.1f})")
    print("fractions :", {k_: round(v, 4) for k_, v in frac_M12.items()})
    print(f"alpha(MS complet) = {alpha_MS:.4e}")

    # --- Scénarios d'interprétation de « 300-500 MW »
    lignes = []
    for nom, coef in (("A_total_toutes_particules", alpha_M12),
                      ("B_photons_plus_e±_(déposé)", comp_M12["photons"] + comp_M12["electrons_positrons"]),
                      ("C_photons_seuls_(corps_gris)", comp_M12["photons"]),
                      ("D_dossier_corps_noir_photons", alpha_bb)):
        for P in (300e6, 400e6, 500e6):
            M = np.sqrt(coef * K.K_HAWKING / P)
            kT = K.kB * K.T_HAWKING_KG / M / K.MeV
            P_tot = alpha_M12 * K.K_HAWKING / M**2
            tau = K.G**2 * M**3 / (3 * alpha_M12 * K.hbar * K.c**4)
            lignes.append(dict(
                scenario=nom, P_revendiquee_MW=P / 1e6, M_kg=M, r_s_fm=K.RS_PAR_KG * M * 1e15,
                T_K=K.T_HAWKING_KG / M, kT_MeV=kT, pic_flux_photons_MeV=res["1"]["pic_flux_kT"] * kT,
                pic_flux_e_MeV=res["0.5"]["pic_flux_kT"] * kT,
                P_totale_MW=P_tot / 1e6, P_neutrinos_MW=frac_M12["neutrinos"] * P_tot / 1e6,
                P_e_MW=frac_M12["electrons_positrons"] * P_tot / 1e6,
                P_photons_MW=frac_M12["photons"] * P_tot / 1e6,
                g_a_1m_en_g=K.G * M / K.g0, poids_N=M * K.g0,
                duree_de_vie_ans_borne_sup=tau / K.an, perte_masse_kg_par_s=P_tot / K.c**2))
    with open(os.path.join(K.RES, "c01_scenarios_puissance.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        for li in lignes:
            w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
    res["scenarios"] = lignes
    for li in lignes:
        print(f"{li['scenario']:32s} P={li['P_revendiquee_MW']:.0f} MW  M={li['M_kg']:.3e} kg  "
              f"r_s={li['r_s_fm']:.2f} fm  kT={li['kT_MeV']:.2f} MeV  Ptot={li['P_totale_MW']:.0f} MW  "
              f"g(1m)={li['g_a_1m_en_g']:.1f} g")

    # --- Modèle grossier alpha(M) avec seuils d'espèces [HYP] et table de masses
    def alpha_modele(M):
        kT_GeV = K.kB * K.T_HAWKING_KG / M / K.GeV
        a = 2 * a1 + 6 * a12 + 2 * a2                      # photon, neutrinos, graviton
        seuil = lambda m: kT_GeV > m / 4.0                 # espèce active si kT > m c^2 / 4  [HYP]
        for m_lep in (0.000511, 0.10566, 1.777):
            if seuil(m_lep):
                a += 4 * a12
        if kT_GeV > 0.2:                                   # quarks u, d, s + gluons au-delà de ~Lambda_QCD [HYP]
            a += 3 * 12 * a12 + 16 * a1
        elif seuil(0.1396):                                # pions (3 états scalaires) en dessous
            a += 3 * a0
        for m_q in (1.27, 4.18, 172.7):
            if seuil(m_q):
                a += 12 * a12
        if seuil(80.4):
            a += 6 * a1 + 3 * a0                           # W, Z (transverses + longitudinaux)
        if seuil(125.2):
            a += a0                                        # Higgs
        return a

    def duree_de_vie(M0):
        # tau = int_0^M0 G^2 M^2 / (alpha(M) hbar c^4) dM   (intégration log)
        m = np.logspace(np.log10(M0) - 12, np.log10(M0), 4000)
        integ = K.G**2 * m**2 / (np.array([alpha_modele(mi) for mi in m]) * K.hbar * K.c**4)
        return float(trapezoid(integ * m, np.log(m)))

    table = []
    for M in (1e2, 1e4, 1e6, 1e8, 1e9, 1e10, 1e11, 2.94e11, 1e12, 4.4e12, 1e13, 1e15):
        a = alpha_modele(M)
        P = a * K.K_HAWKING / M**2
        tau = duree_de_vie(M)
        tau_dossier = 5120 * np.pi * K.G**2 * M**3 / (K.hbar * K.c**4)
        table.append(dict(M_kg=M, r_s_m=K.RS_PAR_KG * M, T_K=K.T_HAWKING_KG / M,
                          kT_MeV=K.kB * K.T_HAWKING_KG / M / K.MeV, alpha_modele=a, P_W=P,
                          P_dossier_W=alpha_bb * K.K_HAWKING / M**2,
                          duree_de_vie_s=tau, duree_de_vie_ans=tau / K.an,
                          duree_dossier_s=tau_dossier, rapport_duree_dossier_sur_calcul=tau_dossier / tau,
                          energie_de_masse_J=M * K.c**2, g_a_1m_m_s2=K.G * M, poids_N=M * K.g0))
    with open(os.path.join(K.RES, "c01_table_masses.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader()
        for li in table:
            w.writerow({k_: f"{v:.4g}" for k_, v in li.items()})
    res["table_masses"] = table
    for li in table:
        print(f"M={li['M_kg']:.2e} kg  kT={li['kT_MeV']:.3e} MeV  alpha={li['alpha_modele']:.2e}  "
              f"P={li['P_W']:.2e} W  tau={li['duree_de_vie_s']:.2e} s = {li['duree_de_vie_ans']:.2e} ans "
              f"(dossier/calcul = {li['rapport_duree_dossier_sur_calcul']:.0f})")

    # --- Spectre des photons (forme universelle en E/kT) et fractions de puissance par bande
    x, dP, dN = spectres[1]
    E_kT = x / TH
    cumul = cumulative_trapezoid(dP, x, initial=0.0) / trapezoid(dP, x)
    with open(os.path.join(K.RES, "c01_spectre_photon.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["E_sur_kT", "dP_dx_par_etat(unites hbar c^6/G^2M^2 par unite de GM omega/c^3)",
                    "dN_dx_par_etat", "fraction_cumulee_puissance"])
        for i in range(len(x)):
            w.writerow([f"{E_kT[i]:.4f}", f"{dP[i]:.5e}", f"{dN[i]:.5e}", f"{cumul[i]:.5e}"])
    bandes = {}
    for li in lignes:
        if li["P_revendiquee_MW"] != 400:
            continue
        kT = li["kT_MeV"]
        f_inf = lambda E_MeV: float(np.interp(E_MeV / kT, E_kT, cumul))
        bandes[li["scenario"]] = dict(kT_MeV=kT, fraction_puissance_photons_sous_100keV=f_inf(0.1),
                                      fraction_sous_1MeV=f_inf(1.0), fraction_sous_10MeV=f_inf(10.0),
                                      energie_mediane_puissance_MeV=float(np.interp(0.5, cumul, E_kT) * kT))
    res["bandes_photons_400MW"] = bandes
    print("Bandes photons (400 MW) :", bandes)

    # Masse d'un trou noir qui émettrait réellement des rayons X (kT = 10 keV) et sa puissance
    M_X = K.kB * K.T_HAWKING_KG / (10e3 * K.e)
    P_X = alpha_sans_masse * K.K_HAWKING / M_X**2
    res["trou_noir_X_kT_10keV"] = dict(M_kg=M_X, P_totale_W=P_X, P_photons_W=2 * a1 * K.K_HAWKING / M_X**2)
    print(f"Trou noir « à rayons X » (kT = 10 keV) : M = {M_X:.3e} kg, P_tot = {P_X:.3e} W")

    # Taux d'émission en nombre (pour la décharge) : N_point = beta c^3/(G M)
    res["taux_nombre"] = dict(beta_e_par_etat=b12, beta_photon_par_etat=b1,
                              unite="c^3/(G M) par état d'hélicité")
    K.sauver_json("c01_hawking.json", res)

    # Figure illustrative
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 4.2))
        for spin, lab in ((0.5, "spin 1/2 (ν, e±)"), (1, "spin 1 (photon)"), (2, "spin 2 (graviton)")):
            xs, dPs, _ = spectres[spin]
            ax.plot(xs / TH, dPs / TH, label=lab)
        ax.set_xlabel("E / kT")
        ax.set_ylabel("dP/d(E/kT) par état d'hélicité  [ħc⁶/(G²M²)]")
        ax.set_title("Spectre de puissance de Hawking (Schwarzschild) — calcul illustratif")
        ax.set_xlim(0, 20)
        ax.legend()
        ax.grid(alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(K.RES, "c01_spectre_hawking.png"), dpi=130)
    except Exception as exc:        # la figure est accessoire
        print("Figure non produite :", exc)


if __name__ == "__main__":
    main()
