#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i03 : que mettre à la place des deux « singularités » au palier 1 ? Choix chiffré.

Six candidats sûrs ou presque (pas de source radioactive, pas de laser > classe 2), notés sur six critères
explicites, puis calcul des performances réelles des deux candidats retenus :

  LOGEMENT PRINCIPAL  → télescope à muons cosmiques (dilatation du temps d'un facteur ~10–40, observée
                         directement, sur des particules naturelles ; cône d'acceptance à travers le logement) ;
  LOGEMENT DE DIRECTION → gyromètre Sagnac à fibre (deux ondes contrarotatives : décalage temporel réel dû à
                         la rotation ; donne le cap, qui fixe le SIGNE du déplacement cinématique de l'unité).

Les candidats écartés sont chiffrés eux aussi (tension d'un piège de Paul, entraînement des référentiels
d'un rotor en lévitation, dimensionnement d'une cellule à vortex), pour que le choix soit vérifiable.

Sorties : resultats/i03_demonstrateurs.json / .txt, ../choix_demonstrateurs.csv
"""
import math

import numpy as np

from i00_commun import (G, c, g0, OMEGA_TERRE, R_TERRE, tau_mu, m_mu_MeV, RACINE, ecrire_csv, ecrire_json, ecrire_txt, geometrie_coffre, L_NOMINAL)

# ---------------------------------------------------------------------------------------------
# 1. Grille de choix (notes 0–5 ; poids explicites ; justification en une ligne)
# ---------------------------------------------------------------------------------------------
CRITERES = [  # (clé, libellé, poids)
    ("archi", "Fidélité à l'architecture (logement, bobine, régulateur, capteur, fluide)", 2),
    ("physique", "Lien réel avec le temps ou la rotation relativistes", 3),
    ("fonction", "Utilité pour la fonction de la machine (mesurer / prédire le déplacement temporel)", 3),
    ("securite", "Sécurité au palier 1 (tension, rayonnement, laser, énergie cinétique)", 3),
    ("integration", "Intégration (Ø ≈ 81 mm, véhicule en mouvement, batterie)", 2),
    ("maturite", "Maturité et disponibilité (commerce ou laboratoire courant)", 1),
]
CANDIDATS = {
    "A. Piège de Paul à grain chargé (air)": dict(archi=5, physique=2, fonction=1, securite=1, integration=3, maturite=3,
        note="charge confinée par un champ oscillant : très fidèle au « logement » ; mais 0,5 à 3 kV alternatifs → exclu du palier 1, renvoyé au palier 2 (horloge à ion piégé)"),
    "B. Gyromètre Sagnac à fibre (ondes contrarotatives)": dict(archi=4, physique=4, fonction=5, securite=5, integration=5, maturite=5,
        note="bobine réelle (de fibre) ; décalage temporel réel entre deux ondes ; donne le cap donc le signe du déplacement cinématique"),
    "C. Cellule à vortex de vidange (analogue de Kerr)": dict(archi=4, physique=3, fonction=1, securite=4, integration=1, maturite=3,
        note="analogue mathématique d'un horizon en rotation pour des ondes de surface ; eau libre inutilisable en roulant ; qualitatif à cette taille → palier 2"),
    "D. Rotor en lévitation magnétique asservie": dict(archi=5, physique=1, fonction=1, securite=3, integration=4, maturite=4,
        note="bobines + régulateur + capteur + objet en rotation : l'image même de DOC-008 ; mais son effet relativiste réel est de 10⁻²⁴ rad/s"),
    "E. Lévitation diamagnétique passive (graphite)": dict(archi=2, physique=0, fonction=0, securite=5, integration=5, maturite=5,
        note="confinement magnétique réel et stable, sans rapport avec le temps"),
    "F. Télescope à muons cosmiques (2 scintillateurs)": dict(archi=3, physique=5, fonction=4, securite=5, integration=5, maturite=4,
        note="seule mesure embarquée d'une dilatation du temps d'un facteur ≫ 1 ; fonctionne en roulant ; cône d'acceptance = « évent » inversé"),
}


def facteur_geometrique(a, d, n=200000, graine=1):
    """Facteur géométrique (cm²·sr) de deux carrés a × a (cm) coaxiaux distants de d (cm), flux en cos²θ normalisé
    sur l'intensité verticale : G = ∫∫ cos²θ · cosθ dA dΩ restreint aux trajectoires traversant les deux tuiles.
    Monte-Carlo : points uniformes sur les deux tuiles ; dΩ = dA₂·cosθ/r²."""
    rng = np.random.default_rng(graine)
    p1 = rng.uniform(-a / 2, a / 2, (n, 2))
    p2 = rng.uniform(-a / 2, a / 2, (n, 2))
    dx = p2 - p1
    r2 = (dx**2).sum(axis=1) + d**2
    cos = d / np.sqrt(r2)
    # élément : dA1 · cosθ (projection) · dΩ (= dA2 cosθ / r²) · cos²θ (loi angulaire)
    integrande = cos * (cos / r2) * cos**2
    return float(a**2 * a**2 * integrande.mean()), float(np.degrees(np.arctan(a * math.sqrt(2) / d)))


def main():
    L = ["i03 — CHOIX ET PERFORMANCES DES DÉMONSTRATEURS DES DEUX LOGEMENTS (palier 1)", "=" * 100]
    res = {}
    # ---- 1. grille
    ptot = sum(p for _k, _l, p in CRITERES)
    scores = {}
    lignes = []
    for nom, d in CANDIDATS.items():
        s = sum(d[k] * p for k, _l, p in CRITERES) / (5 * ptot) * 100
        scores[nom] = s
        lignes.append([nom] + [d[k] for k, _l, _p in CRITERES] + [f"{s:.0f}", d["note"]])
    ordre = sorted(scores, key=scores.get, reverse=True)
    L.append("Grille (notes 0–5 ; poids : " + ", ".join(f"{k}={p}" for k, _l, p in CRITERES) + ")")
    for nom in ordre:
        d = CANDIDATS[nom]
        L.append("  %-52s %s → %3.0f / 100" % (nom, " ".join(str(d[k]) for k, _l, _p in CRITERES), scores[nom]))
    L.append("  Retenus : « %s » (logement de direction) et « %s » (logement principal)." % (ordre[0], ordre[1]))
    # Sensibilité : le classement des deux premiers résiste-t-il à ±1 sur chaque poids ?
    stable = True
    for i in range(len(CRITERES)):
        for dp in (-1, +1):
            poids = [p + (dp if j == i else 0) for j, (_k, _l, p) in enumerate(CRITERES)]
            if min(poids) < 0:
                continue
            sc = {n: sum(d[k] * w for (k, _l, _p), w in zip(CRITERES, poids)) for n, d in CANDIDATS.items()}
            if set(sorted(sc, key=sc.get, reverse=True)[:2]) != set(ordre[:2]):
                stable = False
    L.append("  Sensibilité : les deux premiers restent les mêmes pour toute variation de ±1 d'un poids : %s." % ("oui" if stable else "NON"))
    res["grille"] = dict(scores=scores, ordre=ordre, stable_pm1=stable)
    ecrire_csv(RACINE / "choix_demonstrateurs.csv", ["candidat"] + [f"{l} (poids {p})" for _k, l, p in CRITERES] + ["score_sur_100", "justification"],
               sorted(lignes, key=lambda r: -float(r[-2])))

    # ---- 2. télescope à muons
    geo = geometrie_coffre(L_NOMINAL, "E")
    a_cm = 5.0
    L.append("")
    L.append("TÉLESCOPE À MUONS (logement principal ; tuiles %.0f × %.0f cm ; ouverture du logement Ø %.0f mm)" % (a_cm, a_cm, geo["d_logement"] * 1000))
    I_V = 70.0     # m⁻² s⁻¹ sr⁻¹ : intensité verticale des muons > 1 GeV/c au niveau de la mer (valeur usuelle du PDG — de mémoire, à relire dans Navas et al. 2024)
    res["muons"] = {"intensite_verticale_m2_s_sr": I_V, "statut_intensite": "valeur usuelle citée de mémoire (PDG), à relire", "geometries": {}}
    for d_cm in (5.0, 10.0, 15.0):
        Gf, demi_angle = facteur_geometrique(a_cm, d_cm)
        taux = I_V * Gf * 1e-4          # coïncidences par seconde
        res["muons"]["geometries"][f"d={d_cm:.0f}cm"] = dict(G_cm2_sr=Gf, demi_angle_max_deg=demi_angle, taux_Hz=taux, par_heure=taux * 3600,
                                                               par_48h=taux * 172800, incertitude_stat_1h_pct=100 / math.sqrt(taux * 3600))
        L.append("  écartement %4.0f cm : G = %5.2f cm²·sr ; demi-angle max %4.1f° ; %.3f Hz = %4.0f coïncidences/h (±%.1f %% en 1 h)"
                 % (d_cm, Gf, demi_angle, taux, taux * 3600, 100 / math.sqrt(taux * 3600)))
    # Dilatation : longueur de désintégration et rapport altitude / plaine
    ctau = c * tau_mu
    L.append("  Longueur de désintégration sans dilatation : c·τ = %.1f m (τ = %.4f µs)." % (ctau, tau_mu * 1e6))
    res["muons"]["c_tau_m"] = ctau
    tab = []
    for E_GeV in (1.0, 2.0, 4.0, 10.0):
        gam = E_GeV * 1000 / m_mu_MeV
        beta = math.sqrt(1 - 1 / gam**2)
        Ld = gam * beta * ctau
        tab.append(dict(E_GeV=E_GeV, gamma=gam, longueur_km=Ld / 1000, survie_15km=math.exp(-15000 / Ld), survie_15km_sans_dilatation=math.exp(-15000 / ctau)))
        L.append("  muon de %4.0f GeV : γ = %5.1f ; longueur de désintégration %6.1f km ; survie sur 15 km : %.3f (sans dilatation : %.1e)"
                 % (E_GeV, gam, Ld / 1000, math.exp(-15000 / Ld), math.exp(-15000 / ctau)))
    res["muons"]["table_energie"] = tab
    for dh in (1000.0, 2000.0, 3000.0):
        r_sans = math.exp(dh / ctau)
        res["muons"][f"rapport_sans_dilatation_dh={dh:.0f}"] = r_sans
        L.append("  Dénivelé %4.0f m : SANS dilatation, le taux en altitude devrait valoir ≥ %.1f fois le taux en plaine." % (dh, r_sans))
    # Borne inférieure sur γ déduite d'un rapport mesuré R (hypothèse : aucune production entre les deux niveaux ; les pertes d'énergie
    # dans l'air RÉDUISENT encore le flux en plaine, donc la borne est prudente) : γ ≥ Δh / (cτ ln R)
    L.append("  Si l'on mesure un rapport R entre +2 000 m et la plaine, le facteur de dilatation effectif vaut au moins Δh/(c·τ·ln R) :")
    bornes = {}
    for R in (1.3, 1.5, 2.0, 3.0):
        gmin = 2000.0 / (ctau * math.log(R))
        bornes[str(R)] = gmin
        L.append("     R = %.1f → γ_eff ≥ %.1f" % (R, gmin))
    res["muons"]["borne_gamma_selon_R_2000m"] = bornes
    L.append("  Repère publié (résumé vérifié) : Frisch & Smith 1963, mont Washington → niveau de la mer : facteur de dilatation 8,8 ± 0,8")
    L.append("  pour des muons de 0,9950 à 0,9954 c (attendu 8,4 ± 2).")
    # Statistique : séparer « R = 1,5 » de « R ≥ 21 » ou de « R = 1 »
    taux10 = res["muons"]["geometries"]["d=10cm"]["taux_Hz"]
    for T_h in (1, 6, 24):
        N0 = taux10 * T_h * 3600
        N1 = 1.5 * N0
        sig = (N1 - N0) / math.sqrt(N1 + N0)
        res["muons"][f"signif_R1.5_vs_R1_{T_h}h"] = sig
        L.append("  %2d h à chaque altitude (écartement 10 cm) : %5.0f et %5.0f coups ; un rapport de 1,5 se distingue de 1 à %.1f σ"
                 % (T_h, N0, N1, sig))

    # ---- 3. gyromètre Sagnac
    L.append("")
    L.append("GYROMÈTRE SAGNAC À FIBRE (logement de direction)")
    Lf, D, lam = 500.0, 0.070, 1.55e-6
    lat = math.radians(45.0)
    k_s = 2 * math.pi * Lf * D / (lam * c)             # rad par (rad/s)
    for nom, Om in (("rotation terrestre, composante verticale à 45°", OMEGA_TERRE * math.sin(lat)),
                    ("rotation terrestre complète (axe de la bobine parallèle à l'axe du monde)", OMEGA_TERRE),
                    ("virage du véhicule à 10 °/s", math.radians(10.0))):
        dphi = k_s * Om
        dt = dphi * lam / (2 * math.pi * c)
        res.setdefault("sagnac", {})[nom] = dict(Omega_rad_s=Om, dephasage_rad=dphi, decalage_temporel_s=dt)
        L.append("  %-72s Δφ = %.2e rad ; Δt = %.2e s entre les deux ondes" % (nom, dphi, dt))
    res["sagnac"]["facteur_d_echelle_s"] = k_s
    L.append("  Facteur d'échelle 2πLD/(λc) = %.3f s (bobine %.0f m, Ø %.0f mm, λ = %.2f µm)." % (k_s, Lf, D * 1000, lam * 1e6))
    # bruit de grenaille : δφ ≈ 1/√(N photons) ; 10 µW détectés à 1550 nm
    P_det = 10e-6
    n_ph = P_det / (6.626e-34 * c / lam)
    dphi_shot = 1 / math.sqrt(n_ph)                     # rad/√Hz
    arw = dphi_shot / k_s                               # rad/s/√Hz
    arw_deg_rth = math.degrees(arw) * 60                # °/√h
    res["sagnac"]["limite_grenaille"] = dict(P_detectee_W=P_det, dphi_rad_rtHz=dphi_shot, marche_aleatoire_deg_rth=arw_deg_rth,
                                             temps_pour_voir_rotation_terrestre_3sigma_s=(3 * arw / (OMEGA_TERRE * math.sin(lat)))**2)
    L.append("  Limite de grenaille (10 µW détectés) : %.1e rad/√Hz, soit une marche aléatoire angulaire de %.4f °/√h ;"
             % (dphi_shot, arw_deg_rth))
    L.append("  la composante verticale de la rotation terrestre (%.1f °/h) sort à 3 σ en %.2f ms (limite théorique ; un montage"
             % (math.degrees(OMEGA_TERRE * math.sin(lat)) * 3600, res["sagnac"]["limite_grenaille"]["temps_pour_voir_rotation_terrestre_3sigma_s"] * 1e3))
    L.append("  didactique réel est 10 à 100 fois moins bon : dérives thermiques de la bobine, rétrodiffusion).")
    # Rôle « direction » : le cap fixe le signe du déplacement cinématique (voir i01)
    v = 130 / 3.6
    y_est = -(2 * OMEGA_TERRE * R_TERRE * math.cos(lat) * v + v**2) / (2 * c**2)
    y_ouest = -(-2 * OMEGA_TERRE * R_TERRE * math.cos(lat) * v + v**2) / (2 * c**2)
    res["sagnac"]["role_direction"] = dict(y_est=y_est, y_ouest=y_ouest, D_est_ns_h=-y_est * 3600e9, D_ouest_ns_h=-y_ouest * 3600e9)
    L.append("  Rôle de « direction » : à 130 km/h, cap à l'est → D = %+.2f ns/h (vers le futur) ; cap à l'ouest → D = %+.2f ns/h."
             % (-y_est * 3600e9, -y_ouest * 3600e9))
    # exactitude de cap requise pour prédire le terme cinématique à 1 % : d(cos)/cos ≈ ... erreur de cap δ (rad) près de l'est : 1 − cos δ
    L.append("  Exactitude de cap nécessaire pour prédire ce terme à 1 %% près : ±%.0f° autour de l'est (cos δ ≥ 0,99) — très en deçà des"
             % math.degrees(math.acos(0.99)))
    L.append("  performances d'un gyromètre à fibre, et à la portée d'un simple récepteur GNSS : le gyromètre est ici un DÉMONSTRATEUR, pas une nécessité.")

    # ---- 4. candidats écartés, chiffrés
    L.append("")
    L.append("CANDIDATS ÉCARTÉS — chiffres")
    # 4a. Piège de Paul à grain : q/m d'un grain de 30 µm chargé par frottement ; paramètre de stabilité q_z = 4 (q/m) V / (r0² Ω²) (géométrie anneau, ordre de grandeur)
    rho, rg = 1000.0, 15e-6
    m = rho * 4 / 3 * math.pi * rg**3
    q = 1e5 * 1.602e-19          # 10⁵ charges élémentaires [HYP : charge typique d'un grain de pollen / lycopode]
    qm = q / m
    f = 50.0
    Om = 2 * math.pi * f
    V_pour_q04 = {r0: 0.4 * r0**2 * Om**2 / (4 * qm) for r0 in (5e-3, 10e-3)}
    # champ de sustentation contre la pesanteur : E = g m / q
    E_sust = g0 / qm
    res["piege_de_Paul"] = dict(q_sur_m_C_kg=qm, tension_crete_V_r0_5mm=V_pour_q04[5e-3], tension_crete_V_r0_10mm=V_pour_q04[10e-3],
                                champ_sustentation_V_m=E_sust, limite_TBTS_V_alternatif=50,
                                hypotheses="grain 30 µm, 1e5 e [HYP, charge élevée], anneau r0 = 5 ou 10 mm, 50 Hz, q_z = 0,4 ; ordre de grandeur ; "
                                           "limite de très basse tension de sécurité (50 V alternatif) citée de mémoire, à relire dans la norme")
    L.append("  Piège de Paul (grain de 30 µm, 10⁵ e, 50 Hz, q_z = 0,4) : q/m = %.1e C/kg ; tension ≈ %.0f V crête (anneau de 5 mm) à %.0f V crête"
             % (qm, V_pour_q04[5e-3], V_pour_q04[10e-3]))
    L.append("    (anneau de 10 mm), davantage si le grain est moins chargé ; champ de compensation de la pesanteur ≈ %.0f kV/m." % (E_sust / 1000))
    L.append("    Plusieurs centaines de volts alternatifs, au-dessus de la très basse tension de sécurité (50 V) → écarté du palier 1 ;")
    L.append("    il revient au palier 2 sous sa forme utile : le piège de Paul d'une horloge optique à ion unique.")
    # 4b. rotor en lévitation : sphère d'acier Ø 50 mm à 1000 tr/s
    R, rho_a, fr = 0.025, 7850.0, 1000.0
    M = rho_a * 4 / 3 * math.pi * R**3
    J = 0.4 * M * R**2 * 2 * math.pi * fr
    Om_LT = 2 * G * J / (c**2 * 0.1**3)
    v_per = 2 * math.pi * fr * R
    E_c = 0.5 * 0.4 * M * R**2 * (2 * math.pi * fr)**2
    res["rotor"] = dict(masse_kg=M, J_kg_m2_s=J, Omega_LT_a_10cm_rad_s=Om_LT, vitesse_peripherique_m_s=v_per, energie_cinetique_J=E_c)
    L.append("  Rotor en lévitation (sphère d'acier Ø 50 mm, %.2f kg, 1 000 tr/s) : J = %.2f kg·m²/s ; entraînement des référentiels à 10 cm :"
             % (M, J))
    L.append("    Ω = 2GJ/(c²r³) = %.1e rad/s (les meilleurs gyromètres : ~10⁻¹³ rad/s) ; vitesse périphérique %.0f m/s, énergie cinétique %.0f J"
             % (Om_LT, v_per, E_c))
    L.append("    → un vrai « objet en rotation dans un logement magnétique » ne produit aucun effet relativiste mesurable, et impose un carter de sécurité.")
    # 4c. cellule à vortex de Ø 70 mm
    h = 0.008
    cw = math.sqrt(g0 * h)
    Q = 1.0e-3 / 60            # 1 L/min
    Dd = Q / (2 * math.pi * h)
    r_h = Dd / cw
    r_e = 0.015
    C = math.sqrt((cw * r_e)**2 - Dd**2)
    T_H = 1.0546e-34 * cw / (2 * math.pi * 1.380649e-23 * r_h)
    res["cellule_vortex"] = dict(profondeur_m=h, celerite_m_s=cw, debit_L_min=1.0, r_horizon_mm=r_h * 1000, r_ergo_mm=r_e * 1000,
                                 circulation_m2_s=C, rotation_a_r_ergo_tr_s=C / (2 * math.pi * r_e**2), temperature_Hawking_analogue_K=T_H)
    L.append("  Cellule à vortex Ø 70 mm (eau, h = 8 mm, 1 L/min) : célérité √(gh) = %.2f m/s ; horizon analogue à r = %.1f mm (dans l'orifice) ;"
             % (cw, r_h * 1000))
    L.append("    ergorégion de 15 mm pour une circulation de %.1e m²/s (%.1f tr/s à ce rayon) ; température de Hawking analogue %.0e K."
             % (C, C / (2 * math.pi * r_e**2), T_H))
    L.append("    Longueurs d'onde disponibles (1–3 cm) à la frontière gravité/capillarité (17 mm) : démonstration qualitative seulement, véhicule à l'arrêt.")
    ecrire_json("i03_demonstrateurs.json", res)
    ecrire_txt("i03_demonstrateurs.txt", L)


if __name__ == "__main__":
    main()
