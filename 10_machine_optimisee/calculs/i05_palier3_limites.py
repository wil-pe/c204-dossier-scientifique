#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i05 : palier 3 (C204-R3) — ce que la physique connue n'interdit pas, chiffré.

(a) Déplacement vers le FUTUR par dilatation : vitesse (anneau de stockage, vaisseau) et gravité (astre compact,
    orbite autour d'un trou noir de Kerr) ; « rendement » temps gagné par joule ; valeur de Γ atteignable.
(b) Trou noir comme source d'énergie ou de poussée (Crane & Westmoreland 2009) : ce qui subsiste de l'idée du corpus.
(c) Trou de ver traversable : matière exotique nécessaire, bornes quantiques, conversion en machine temporelle.
Aucune de ces voies ne mène vers le passé avec la physique établie ; (c) le ferait SI de l'énergie négative
macroscopique existait, ce que les inégalités quantiques et la condition d'énergie nulle moyennée excluent.

Formules : relativité restreinte ; Schwarzschild ; orbites circulaires de Kerr (Bardeen, Press & Teukolsky 1972) ;
puissances de Hawking reprises de l'Équipe B (RAPPORT_B §4.1, calcul complet à facteurs de corps gris).

Sorties : resultats/i05_palier3.json / .txt, ../palier3_dilatation.csv
"""
import math

import mpmath as mp

from i00_commun import (G, c, g0, hbar, AN, M_SOLEIL, GM_TERRE, R_TERRE, tau_mu, m_mu_MeV, m_p_MeV, m_e_MeV, eV,
                        GAMMA_REVENDIQUE, MASSE_UNITE, RACINE, ecrire_csv, ecrire_json, ecrire_txt)

E_MONDE_AN = 6.2e20     # J : consommation mondiale d'énergie primaire (≈ 620 EJ, valeur de l'Équipe C, Energy Institute 2024)
MT_TNT = 4.184e15       # J par mégatonne


def kerr_isco(a):
    """Rayon de la dernière orbite circulaire stable prograde (unités GM/c²), a = J c/(G M²) (BPT 1972)."""
    a = mp.mpf(a)
    z1 = 1 + mp.cbrt(1 - a**2) * (mp.cbrt(1 + a) + mp.cbrt(1 - a))
    z2 = mp.sqrt(3 * a**2 + z1**2)
    return 3 + z2 - mp.sqrt((3 - z1) * (3 + z1 + 2 * z2))


def kerr_ut(r, a):
    """dt/dτ sur une orbite circulaire équatoriale prograde de rayon r (unités GM/c²)."""
    return (1 + a / r**mp.mpf(1.5)) / mp.sqrt(1 - 3 / r + 2 * a / r**mp.mpf(1.5))


def kerr_E(r, a):
    """Énergie spécifique (par unité de mc²) de la même orbite."""
    return (1 - 2 / r + a / r**mp.mpf(1.5)) / mp.sqrt(1 - 3 / r + 2 * a / r**mp.mpf(1.5))


def main():
    mp.mp.dps = 60
    L = ["i05 — PALIER 3 : LIMITES THÉORIQUES", "=" * 100]
    res = {}
    mc2 = MASSE_UNITE * c**2

    # ------------------------------------------------------------------ (a1) vitesse
    L.append("(a1) DILATATION PAR LA VITESSE — γ = dt/dτ ; déplacement vers le futur D = (γ − 1) heure par heure de temps propre")
    L.append("     Énergie cinétique (γ − 1)·m·c² ; pour l'unité de 227 kg, m·c² = %.3e J." % mc2)
    cas = []

    def ajoute(nom, gam, nature, statut, note=""):
        D = float((gam - 1) * 3600)
        E = float((gam - 1)) * mc2
        cas.append(dict(nom=nom, gamma=float(gam), D_s_par_h=D, E_227kg_J=E, nature=nature, statut=statut, note=note))
        L.append("  %-58s γ = %-12.6g D = %-10.3e s/h ; pour 227 kg : %.2e J (%s)" % (nom, float(gam), D, E, statut))

    v_iss = math.sqrt(GM_TERRE / (R_TERRE + 420e3))
    ajoute("Station spatiale (7,66 km/s ; cinématique seule)", 1 + v_iss**2 / (2 * c**2), "objet habité", "Démontré")
    g_mu = math.sqrt(1 + (3094.0 / m_mu_MeV)**2)
    ajoute("Muons en anneau de stockage, p = 3,094 GeV/c (CERN 1977 ; BNL ; Fermilab)", g_mu, "particules", "Démontré",
           "durée de vie au laboratoire %.2f µs contre %.3f µs au repos" % (g_mu * tau_mu * 1e6, tau_mu * 1e6))
    ajoute("Protons du LHC à 6,8 TeV", 6.8e6 / m_p_MeV, "particules", "Démontré")
    ajoute("Électrons du LEP à 45,6 GeV (≈ le facteur revendiqué)", 45.6e3 / m_e_MeV, "particules", "Démontré")
    ajoute("Électrons du LEP à 104,5 GeV", 104.5e3 / m_e_MeV, "particules", "Démontré")
    for beta in (0.1, 0.5, 0.9, 0.99):
        ajoute("Vaisseau à %.2f c" % beta, 1 / math.sqrt(1 - beta**2), "objet macroscopique", "Théoriquement possible")
    ajoute("« 10 ans par heure » (Γ revendiqué)", GAMMA_REVENDIQUE, "objet macroscopique", "Théoriquement possible (vers le futur seulement)")
    res["a1_vitesse"] = cas
    # anneau à muons : rayon, champ, accélération propre
    p_SI = 3.094e9 * eV / c
    B_ring = 1.4513
    R_ring = p_SI / (eV * B_ring)
    a_propre = g_mu**2 * c**2 * (1 - 1 / g_mu**2) / R_ring
    res["anneau_muons"] = dict(gamma=g_mu, tau_labo_us=g_mu * tau_mu * 1e6, rayon_m=R_ring, B_T=B_ring, acceleration_propre_g=a_propre / g0,
                               note="γ, durée de vie dilatée et rayon recalculés à partir de p = 3,094 GeV/c et B = 1,4513 T (valeurs usuelles de l'expérience, de mémoire)")
    L.append("  Anneau à muons : γ = %.2f ; vie dilatée %.1f µs ; rayon p/(eB) = %.2f m pour B = %.4f T ; accélération propre γ²v²/R = %.1e g."
             % (g_mu, g_mu * tau_mu * 1e6, R_ring, B_ring, a_propre / g0))
    # rendement
    rend = 3600.0 / mc2
    rend_mu = tau_mu / (m_mu_MeV * 1e6 * eV)
    res["rendement"] = dict(formule="Δt_gagné / E_cinétique = τ / (m c²), indépendant de γ", unite_227kg_1h_s_par_J=rend, muon_s_par_J=rend_mu)
    L.append("  RENDEMENT : temps gagné (γ − 1)·τ divisé par l'énergie (γ − 1)·m·c² = τ/(m·c²), INDÉPENDANT de γ.")
    L.append("     unité de 227 kg, croisière d'une heure : %.2e s par joule ; un muon pendant sa vie propre : %.1e s par joule." % (rend, rend_mu))
    for gain_txt, gain in (("1 seconde par heure", 1.0), ("1 heure par heure (γ = 2)", 3600.0), ("1 jour par heure (γ = 25)", 86400.0),
                           ("10 ans par heure (γ = 87 661)", 10 * AN)):
        E = gain / rend
        res["rendement"][gain_txt] = dict(E_J=E, Mt_TNT=E / MT_TNT, annees_energie_mondiale=E / E_MONDE_AN)
        L.append("     gagner %-30s coûte %.2e J = %.2e Mt de TNT = %.2e année(s) d'énergie primaire mondiale" % (gain_txt, E, E / MT_TNT, E / E_MONDE_AN))
    # accélération constante, fusée à photons, anneau habité
    for a_g in (1.0, 2.0):
        tau = c / (a_g * g0) * math.acosh(GAMMA_REVENDIQUE)
        res[f"temps_propre_pour_gamma_revendique_a_{a_g:.0f}g_ans"] = tau / AN
        L.append("  À %.0f g constants, atteindre Γ = 87 660 demande %.2f ans de temps propre." % (a_g, tau / AN))
    Rm = GAMMA_REVENDIQUE * (1 + math.sqrt(1 - 1 / GAMMA_REVENDIQUE**2))
    res["rapport_de_masse_fusee_photonique"] = dict(aller=Rm, aller_et_arret=Rm**2)
    L.append("  Fusée à photons idéale : rapport de masse γ(1 + β) = %.3e pour atteindre Γ, %.1e pour s'arrêter ensuite." % (Rm, Rm**2))
    for gam in (g_mu, GAMMA_REVENDIQUE):
        R1g = gam**2 * c**2 / g0
        res[f"rayon_anneau_habite_1g_gamma_{gam:.0f}_al"] = R1g / (c * AN)
        L.append("  Anneau de stockage « habitable » (accélération propre 1 g) à γ = %.0f : rayon γ²c²/g = %.2e m = %.2e années-lumière."
                 % (gam, R1g, R1g / (c * AN)))

    # ------------------------------------------------------------------ (a2) gravité
    L.append("")
    L.append("(a2) DILATATION PAR LA GRAVITÉ — Γ = dt_loin/dτ")
    grav = []

    def ajoute_g(nom, Gam, statut, cout=None, note=""):
        D = float((Gam - 1) * 3600)
        grav.append(dict(nom=nom, Gamma=float(Gam), D_s_par_h=D, statut=statut, cout_retour_fraction_mc2=cout, note=note))
        L.append("  %-64s Γ − 1 = %-11.4e D = %-10.3e s/h%s" % (nom, float(Gam - 1), D, ("" if cout is None else " ; retour : %.3f m·c²" % cout)))

    ajoute_g("Centre de la Terre contre surface (densité uniforme : ½·g·R/c²)", 1 + 0.5 * g0 * R_TERRE / c**2, "Démontré (principe)")
    ajoute_g("Surface du Soleil contre l'infini", 1 / math.sqrt(1 - 2 * G * M_SOLEIL / (6.957e8 * c**2)), "Démontré")
    ajoute_g("Surface d'une naine blanche (0,6 M☉ ; 8 900 km) [valeurs typiques]", 1 / math.sqrt(1 - 2 * G * 0.6 * M_SOLEIL / (8.9e6 * c**2)), "Démontré (spectroscopie)")
    rs_ns = 2 * G * 1.4 * M_SOLEIL / c**2
    G_ns = 1 / math.sqrt(1 - rs_ns / 12e3)
    ajoute_g("Surface d'une étoile à neutrons (1,4 M☉ ; 12 km) [valeurs typiques]", G_ns, "Théoriquement possible", 1 - 1 / G_ns,
             "pesanteur locale ~10¹¹ g : aucun équipage")
    # orbites de Kerr
    for a in (0.0, 0.5, 0.9, 0.99, 0.998, 0.9999):
        r = kerr_isco(a)
        ut = kerr_ut(r, mp.mpf(a))
        E = kerr_E(r, mp.mpf(a))
        ajoute_g("Dernière orbite stable, trou noir de Kerr a/M = %g (r = %.3f GM/c²)" % (a, float(r)), ut,
                 "Théoriquement possible" + (" (limite de Thorne des trous noirs accrétants)" if a == 0.998 else ""), float(1 - E),
                 "chute libre : aucune pesanteur ressentie ; énergie de liaison %.1f %% de m·c²" % (float(1 - E) * 100))
    # spin nécessaire pour Γ = 87 660 à l'ISCO
    f = lambda le: kerr_ut(kerr_isco(1 - mp.mpf(10)**le), 1 - mp.mpf(10)**le) - GAMMA_REVENDIQUE
    le = mp.findroot(f, -14)
    eps = mp.mpf(10)**le
    res["spin_pour_gamma_revendique_a_l_ISCO"] = dict(un_moins_a=float(eps), log10=float(le))
    L.append("  Pour que la dernière orbite stable donne Γ = 87 660, il faut 1 − a/M = %.2e (limite astrophysique admise : 1 − a/M ≈ 2×10⁻³)."
             % float(eps))
    # statique au-dessus d'un horizon
    x = 1 / (GAMMA_REVENDIQUE**2 - 1)
    for nom, M in (("Sgr A* (4,3×10⁶ M☉)", 4.3e6 * M_SOLEIL), ("trou noir de 10 M☉", 10 * M_SOLEIL)):
        rs = 2 * G * M / c**2
        a_p = c**2 / (2 * rs) * GAMMA_REVENDIQUE / (1 + x)**2
        res.setdefault("statique_gamma_revendique", {})[nom] = dict(r_s_m=rs, altitude_au_dessus_horizon_m=rs * x, acceleration_propre_g=a_p / g0)
        L.append("  Observateur immobile à Γ = 87 660 au-dessus de %s : à %.2e m de l'horizon (r_s = %.2e m) ; poussée requise %.1e g."
                 % (nom, rs * x, rs, a_p / g0))
    # marée à l'ISCO (ordre de grandeur newtonien 2GM·ℓ/r³, ℓ = 2 m, a = 0,998)
    r_isco = float(kerr_isco(0.998))
    for nom, M in (("Sgr A* (4,3×10⁶ M☉)", 4.3e6 * M_SOLEIL), ("trou noir de 10 M☉", 10 * M_SOLEIL)):
        rg = G * M / c**2
        maree = 2 * G * M * 2.0 / (r_isco * rg)**3
        res.setdefault("maree_ISCO_a0.998", {})[nom] = dict(r_g_m=rg, maree_sur_2m_g=maree / g0, periode_orbitale_s=2 * math.pi * (r_isco**1.5 + 0.998) * rg / c)
        L.append("  Marée sur 2 m à cette orbite (a/M = 0,998, ordre de grandeur newtonien) autour de %s : %.1e g ; période orbitale %.1e s."
                 % (nom, maree / g0, 2 * math.pi * (r_isco**1.5 + 0.998) * rg / c))
    # rendement comparé gravité / vitesse à Γ égal (a = 0,998)
    ut998 = float(kerr_ut(kerr_isco(0.998), mp.mpf(0.998)))
    E998 = float(kerr_E(kerr_isco(0.998), mp.mpf(0.998)))
    ratio = (ut998 - 1) / (1 - E998)
    res["rendement_gravite_vs_vitesse_a0.998"] = dict(Gamma=ut998, energie_liaison=1 - E998, avantage=ratio, cout_retour_227kg_J=(1 - E998) * mc2)
    L.append("  À Γ = %.1f : la voie orbitale coûte %.3f m·c² (%.1e J pour 227 kg, pour remonter du puits) contre %.2f m·c² par la vitesse :"
             % (ut998, 1 - E998, (1 - E998) * mc2, ut998 - 1))
    L.append("  avantage d'un facteur %.0f — à condition de disposer d'un trou noir supermassif en rotation rapide à portée (Sgr A* : ~26 000 années-lumière)." % ratio)
    res["a2_gravite"] = grav

    # ------------------------------------------------------------------ (b) trou noir moteur
    L.append("")
    L.append("(b) TROU NOIR COMME SOURCE D'ÉNERGIE OU DE POUSSÉE (puissances : Équipe B, §4.1)")
    TN = [  # masse kg, puissance W, durée de vie, r_s m (Équipe B, tableau §4.1)
        (1e9, 6.1e16, "15 ans", 1.5e-18),
        (1e12, 7.7e9, "1,2×10¹¹ ans", 1.5e-15),
        (4e12, 4.8e8, "7,9×10¹² ans", 5.9e-15),
    ]
    res["b_trou_noir"] = {}
    for M, P, vie, rs in TN:
        F = P / c
        d = dict(puissance_W=P, duree_de_vie=vie, r_s_m=rs, poussee_max_N=F, acceleration_propre_m_s2=F / M, energie_de_fabrication_J=M * c**2,
                 annees_energie_mondiale=M * c**2 / E_MONDE_AN, debit_d_entretien_kg_s=P / c**2, poids_N=M * g0)
        res["b_trou_noir"][f"M={M:.0e}kg"] = d
        L.append("  M = %.0e kg : P = %.1e W (%s) ; poussée maximale P/c = %.1e N ; accélération de l'ensemble ≤ %.1e m/s² ;"
                 % (M, P, vie, F, F / M))
        L.append("      fabrication ≥ M·c² = %.1e J (%.1e années d'énergie mondiale) ; entretien : %.2e kg/s à faire avaler à un objet de %.0e m."
                 % (M * c**2, M * c**2 / E_MONDE_AN, P / c**2, rs))
    # facteur de Lorentz final d'un vaisseau à trou noir : rapidité = η ln R (η : fraction de l'énergie rayonnée convertie en impulsion dirigée)
    L.append("  Facteur de Lorentz final d'un vaisseau consommant tout son trou noir : γ = cosh(η·ln R), R = masse initiale / masse finale,")
    L.append("  η = fraction de l'énergie rayonnée convertie en impulsion dirigée (≤ 0,44 : seuls γ et e± sont absorbables ; neutrinos perdus).")
    tabv = {}
    for eta in (1.0, 0.44, 0.1):
        ligne = []
        for R in (11.0, 101.0, 1001.0):
            gam = math.cosh(eta * math.log(R))
            tabv[f"eta={eta},R={R:.0f}"] = gam
            ligne.append("R = %4.0f → γ = %-7.4g" % (R, gam))
        L.append("      η = %.2f : %s" % (eta, " ; ".join(ligne)))
    R_need = math.exp(math.acosh(GAMMA_REVENDIQUE))
    tabv["R_pour_gamma_revendique_eta1"] = R_need
    tabv["R_pour_gamma_revendique_eta0.44"] = math.exp(math.acosh(GAMMA_REVENDIQUE) / 0.44)
    L.append("      Γ = 87 660 exigerait R = %.2e (η = 1) ou %.1e (η = 0,44)." % (R_need, tabv["R_pour_gamma_revendique_eta0.44"]))
    res["b_trou_noir"]["gamma_final"] = tabv
    L.append("  Ce qui subsiste de l'idée du corpus : un trou noir de 10⁹–10¹² kg rayonnerait bien de 10¹⁰ à 10¹⁷ W (jamais observé) ;")
    L.append("  Crane & Westmoreland (2009) jugent le vaisseau « à la limite du possible » ; la fabrication par concentration de lumière est")
    L.append("  exclue par Álvarez-Domínguez et al. (2024). Rien de cela ne tient dans 227 kg, ni ne déplace quoi que ce soit dans le temps,")
    L.append("  sinon vers le futur, par la vitesse acquise.")

    # ------------------------------------------------------------------ (c) trou de ver
    L.append("")
    L.append("(c) TROU DE VER TRAVERSABLE (Morris & Thorne 1988 ; Morris, Thorne & Yurtsever 1988)")
    res["c_trou_de_ver"] = {}
    for nom, b in (("coffre seul (diagonale 0,93 m)", 0.47), ("véhicule (rayon 2,5 m)", 2.5), ("zone de 11 m (cote de DOC-014)", 11.0)):
        Mex = -b * c**2 / (2 * G)
        tens = c**4 / (8 * math.pi * G * b**2)
        tau0 = (3 * hbar / (32 * math.pi**2 * c**3 * tens))**0.25
        d_cas = (math.pi**2 * hbar * c / (720 * tens))**0.25
        res["c_trou_de_ver"][nom] = dict(rayon_gorge_m=b, masse_exotique_kg=Mex, masse_exotique_Jupiter=Mex / 1.898e27, tension_Pa=tens,
                                         duree_max_inegalite_quantique_s=tau0, ecartement_Casimir_equivalent_m=d_cas)
        L.append("  Gorge de %.2f m (%s) : masse exotique ≈ %.2e kg (%.2f masse de Jupiter, négative) ; tension %.1e Pa ;"
                 % (b, nom, Mex, Mex / 1.898e27, tens))
        L.append("      une telle densité d'énergie négative n'est permise que pendant %.0e s (inégalité de Ford-Roman) ; plaques de Casimir"
                 % tau0)
        L.append("      équivalentes écartées de %.0e m (longueur de Planck : 1,6×10⁻³⁵ m ; noyau : 10⁻¹⁵ m)." % d_cas)
    # conversion en machine temporelle : décalage accumulé = T (1 − 1/γ) ≤ T
    L.append("  Conversion en machine temporelle : une bouche déplacée à γ pendant la durée extérieure T prend un retard T·(1 − 1/γ) ≤ T.")
    for gam in (2.0, 10.0, GAMMA_REVENDIQUE):
        T36 = 36.0 / (1 - 1 / gam)
        res["c_trou_de_ver"][f"duree_pour_36_ans_gamma_{gam:g}"] = T36
        L.append("      décalage de 36 ans (2036 → 2000) avec γ = %-7g : il faut %.1f ans de mouvement relatif." % (gam, T36))
    L.append("      Conséquence générale : on ne remonte jamais avant la date de mise en service de la machine. Un départ de 2036 vers 1975")
    L.append("      supposerait un trou de ver déjà ouvert en 1975. Et la formation de l'horizon chronologique fait diverger le tenseur")
    L.append("      énergie-impulsion du vide (Kim & Thorne 1991 ; Hawking 1992 ; Kay, Radzikowski & Wald 1997).")
    L.append("  Les seuls trous de ver traversables cohérents avec la théorie quantique (Gao, Jafferis & Wall 2017 ; Maldacena, Milekhin &")
    L.append("  Popov 2018/2023) sont plus LONGS à traverser que le trajet extérieur : ils ne permettent aucune machine temporelle.")

    ecrire_csv(RACINE / "palier3_dilatation.csv",
               ["voie", "cas", "facteur_dt_sur_dtau", "deplacement_vers_le_futur_s_par_h", "energie_pour_227kg_J_ou_cout_retour_fraction_mc2", "nature", "statut_physique", "note"],
               [["vitesse", d["nom"], f"{d['gamma']:.10g}", f"{d['D_s_par_h']:.4e}", f"{d['E_227kg_J']:.3e} J", d["nature"], d["statut"], d["note"]] for d in cas] +
               [["gravité", d["nom"], f"{d['Gamma']:.10g}", f"{d['D_s_par_h']:.4e}", "" if d["cout_retour_fraction_mc2"] is None else f"{d['cout_retour_fraction_mc2']:.4f} m·c²",
                 "astre / orbite", d["statut"], d["note"]] for d in grav])
    ecrire_json("i05_palier3.json", res)
    ecrire_txt("i05_palier3.txt", L)


if __name__ == "__main__":
    main()
