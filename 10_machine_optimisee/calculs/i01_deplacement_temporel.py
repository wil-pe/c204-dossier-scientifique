#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i01 : décalage relativiste subi par TOUT OBJET sur un trajet donné, et détectabilité par horloge.

CORRECTION POST-VALIDATION (Red Team n° 2, I-1) : la grandeur calculée ici est une propriété du TRAJET (altitude,
vitesse, cap), pas de la machine. Un lest de même masse posé dans le véhicule subit exactement le même décalage.
Le palier R1 n'en est pas la cause : il le CALCULE (R1-A) ou le MESURE (R1-B). Les clés internes « D_futur… »
sont conservées pour la compatibilité des scripts ; les libellés publiés parlent de « décalage relativiste du trajet ».

Physique (relativité générale, champ faible, vitesses lentes ; Ashby 2003 pour le formalisme GPS) :
dans le repère géocentrique non tournant,

    dτ/dt = 1 − GM/(r c²) − v_I²/(2 c²)            (v_I : vitesse inertielle)

Pour une unité à l'altitude h, de vitesse sol (v_E vers l'est, v_N vers le nord), à la latitude φ, comparée
à une référence FIXE au sol (altitude h0, même latitude) :

    y = (dτ_unité − dτ_réf)/dt = [GM/r0 − GM/r]/c² − [ (Ω r cosφ + v_E)² + v_N² − (Ω r0 cosφ)² ] / (2c²)

  y > 0 : l'horloge embarquée AVANCE (l'unité vieillit plus que la référence) ;
  y < 0 : l'horloge embarquée RETARDE : c'est le seul « déplacement vers le futur » réel.
On note D = −y × 3600 s le déplacement net vers le futur par heure (positif = vers le futur de la référence).
Dans aucun cas l'ordre des événements n'est inversé : aucun scénario ne mène vers le passé.

Le terme croisé −Ω r cosφ·v_E/c² (effet Sagnac d'une horloge transportée) rend le signe du déplacement
cinématique dépendant du CAP : vers l'est l'horloge retarde, vers l'ouest elle avance (Hafele & Keating 1972).

Sorties : resultats/i01_deplacement.json, resultats/i01_deplacement.txt,
          ../deplacement_scenarios.csv, ../detectabilite_horloges.csv
"""
import math

from i00_commun import (GM_TERRE, R_TERRE, OMEGA_TERRE, c, g0, G, MASSE_UNITE, GAMMA_REVENDIQUE,
                        DEPL_REVENDIQUE_S_PAR_H, RACINE, ecrire_csv, ecrire_json, ecrire_txt, fr)

LAT = 45.0   # latitude de référence des scénarios terrestres (degrés) [HYP]


def taux(h, v_est=0.0, v_nord=0.0, lat=LAT, h0=0.0):
    """Écart relatif de marche y de l'unité par rapport à une référence fixe au sol (altitude h0)."""
    phi = math.radians(lat)
    r0, r = R_TERRE + h0, R_TERRE + h
    grav = (GM_TERRE / r0 - GM_TERRE / r) / c**2
    vI2 = (OMEGA_TERRE * r * math.cos(phi) + v_est)**2 + v_nord**2
    vI02 = (OMEGA_TERRE * r0 * math.cos(phi))**2
    cin = -(vI2 - vI02) / (2 * c**2)
    return grav, cin, grav + cin


def taux_orbite(h, lat_ref=LAT):
    """Orbite circulaire d'altitude h comparée à une référence au sol (latitude lat_ref)."""
    r = R_TERRE + h
    v = math.sqrt(GM_TERRE / r)
    grav = (GM_TERRE / R_TERRE - GM_TERRE / r) / c**2
    cin = -(v**2 - (OMEGA_TERRE * R_TERRE * math.cos(math.radians(lat_ref)))**2) / (2 * c**2)
    return grav, cin, grav + cin, v


SCENARIOS = [
    # id, libellé, h (m), v_est (m/s), v_nord (m/s), accessible au palier, remarque
    ("S00", "Parking, à côté de la référence", 0, 0, 0, "R1", "témoin : écart nul attendu"),
    ("S01", "Séjour statique à +1 000 m (col de montagne)", 1000, 0, 0, "R1", "g·Δh/c²"),
    ("S02", "Séjour statique à +2 000 m", 2000, 0, 0, "R1", ""),
    ("S03", "Séjour statique à +3 000 m (observatoire d'altitude)", 3000, 0, 0, "R1", ""),
    ("S04", "Séjour statique à −1 000 m (mine profonde)", -1000, 0, 0, "R1", "approximation g·Δh (potentiel intérieur non modélisé)"),
    ("S05", "Route, 130 km/h plein est, à plat", 0, 130 / 3.6, 0, "R1", "terme de Sagnac dominant"),
    ("S06", "Route, 130 km/h plein ouest, à plat", 0, -130 / 3.6, 0, "R1", ""),
    ("S07", "Route, 130 km/h nord-sud, à plat", 0, 0, 130 / 3.6, "R1", "seul v²/2c² subsiste"),
    ("S08", "Train à grande vitesse, 320 km/h plein est", 0, 320 / 3.6, 0, "R1", ""),
    ("S09", "Train à grande vitesse, 320 km/h plein ouest", 0, -320 / 3.6, 0, "R1", ""),
    ("S10", "Avion de ligne, 10,7 km, 250 m/s plein est", 10700, 250, 0, "R1", "soute pressurisée"),
    ("S11", "Avion de ligne, 10,7 km, 250 m/s plein ouest", 10700, -250, 0, "R1", ""),
]


def main():
    L = ["i01 — DÉCALAGE RELATIVISTE SUBI PAR TOUT OBJET SUR LE TRAJET (latitude %.0f°)" % LAT, "=" * 100]
    L.append("Grandeur propre au TRAJET : la machine n'en est pas la cause (un lest de même masse a la même valeur).")
    L.append("Convention : y = écart relatif de marche (horloge embarquée − référence au sol).")
    L.append("             D = −y × 3600 s par heure (D > 0 : l'objet vieillit MOINS que la référence ; D < 0 : il vieillit PLUS).")
    L.append("             Jamais vers le passé : seul le rythme relatif de deux horloges change.")
    L.append("")
    L.append("%-4s %-52s %11s %11s %11s %12s %12s" % ("id", "scénario", "gravité", "cinémat.", "y total", "avance ns/h", "D ns/h"))
    lignes_csv, res = [], {"latitude_deg": LAT, "scenarios": {}}
    for sid, lib, h, ve, vn, palier, rem in SCENARIOS:
        gr, ci, y = taux(h, ve, vn)
        ns_h = y * 3600e9
        res["scenarios"][sid] = dict(libelle=lib, h_m=h, v_est=ve, v_nord=vn, y_grav=gr, y_cin=ci, y=y,
                                     avance_horloge_ns_par_h=ns_h, D_futur_ns_par_h=-ns_h, D_futur_s_par_h=-y * 3600,
                                     ecart_48h_ns=y * 172800e9, palier=palier, remarque=rem)
        L.append("%-4s %-52s %+11.3e %+11.3e %+11.3e %+12.4f %+12.4f" % (sid, lib, gr, ci, y, ns_h, -ns_h))
        sens = "l'objet vieillit moins que la référence" if y < 0 else ("aucun" if y == 0 else "l'objet vieillit plus que la référence")
        lignes_csv.append([sid, lib, h, round(ve, 2), round(vn, 2), f"{gr:.4e}", f"{ci:.4e}", f"{y:.4e}", f"{ns_h:+.4f}", f"{-ns_h:+.4f}",
                           f"{-y * 3600:+.3e}", f"{y * 172800e9:+.2f}", sens, palier, "calculé (i01)", rem])

    # Orbites (hors palier 1 : il faudrait satelliser l'unité)
    L.append("")
    for sid, lib, h in (("S20", "Orbite basse 420 km (Station spatiale)", 420e3), ("S21", "Orbite GPS 20 184 km", 20184e3),
                        ("S22", "Orbite géostationnaire 35 786 km", 35786e3)):
        gr, ci, y, v = taux_orbite(h)
        ns_h = y * 3600e9
        res["scenarios"][sid] = dict(libelle=lib, h_m=h, v_orbitale=v, y_grav=gr, y_cin=ci, y=y, avance_horloge_ns_par_h=ns_h,
                                     D_futur_ns_par_h=-ns_h, D_futur_s_par_h=-y * 3600, ecart_par_jour_us=y * 86400e6, palier="hors palier 1")
        L.append("%-4s %-52s %+11.3e %+11.3e %+11.3e %+12.2f %+12.2f   (%.1f µs/jour)" % (sid, lib, gr, ci, y, ns_h, -ns_h, y * 86400e6))
        sens = "l'objet vieillit moins que la référence" if y < 0 else "l'objet vieillit plus que la référence"
        lignes_csv.append([sid, lib, h, "", "", f"{gr:.4e}", f"{ci:.4e}", f"{y:.4e}", f"{ns_h:+.2f}", f"{-ns_h:+.2f}", f"{-y * 3600:+.3e}",
                           f"{y * 172800e9:+.1f}", sens, "hors palier 1 (satellisation)", "calculé (i01)", f"v = {v:.0f} m/s"])
    # Contrôles
    ygps = res["scenarios"]["S21"]["y"]
    # la valeur de référence +38,6 µs/jour (Ashby 2003) est donnée par rapport au géoïde ; notre référence est à 45° de latitude
    gr, ci, yg, v = taux_orbite(20184e3, lat_ref=0.0)
    geoide = (GM_TERRE / R_TERRE) / c**2  # non utilisé : simple rappel d'ordre de grandeur (6,95e-10)
    L.append("")
    L.append("Contrôle 1 — GPS : y = %+.3e, soit %+.1f µs/jour (valeur de référence : +38,6 µs/jour, dont +45,8 gravité et −7,2 vitesse)."
             % (yg, yg * 86400e6))
    res["controle_GPS_us_par_jour"] = yg * 86400e6
    # Hafele-Keating simplifié (mêmes paramètres que l'Équipe F : h = 9 km, 230 m/s, latitude 34°, 41,2 h et 48,6 h)
    hk = {}
    for nom, ve, dur in (("est", 230.0, 41.2), ("ouest", -230.0, 48.6)):
        gr, ci, y = taux(9000.0, ve, 0.0, lat=34.0)
        hk[nom] = dict(grav_ns=gr * dur * 3600e9, cin_ns=ci * dur * 3600e9, total_ns=y * dur * 3600e9)
    L.append("Contrôle 2 — Hafele-Keating (modèle simplifié h = 9 km, 230 m/s, 34°) : est %+.0f ns, ouest %+.0f ns "
             "(observé : −59 ± 10 ns et +273 ± 7 ns, résumé de l'article vérifié)." % (hk["est"]["total_ns"], hk["ouest"]["total_ns"]))
    res["controle_HK"] = hk
    # Project GREAT (Van Baak 2005) : 1 340 m, 42 h → 22 ns prédits (valeurs de l'Équipe F)
    gr, ci, y = taux(1340.0)
    L.append("Contrôle 3 — « Project GREAT » (Δh = 1 340 m, 42 h) : %+.1f ns (prédit ≈ 22 ns, observé ≈ 23 ns selon la page du projet, relue par l'Équipe F)."
             % (y * 42 * 3600e9))
    res["controle_GREAT_ns"] = y * 42 * 3600e9

    # Sagnac d'une horloge transportée : écart par kilomètre parcouru vers l'est
    sag = OMEGA_TERRE * R_TERRE * math.cos(math.radians(LAT)) * 1000.0 / c**2
    L.append("")
    L.append("Effet du CAP (terme de Sagnac d'une horloge transportée, latitude %.0f°) : %.3f ps par kilomètre parcouru vers l'est"
             % (LAT, sag * 1e12))
    L.append("  (retard de l'horloge embarquée ; avance pour un trajet vers l'ouest ; indépendant de la vitesse).")
    L.append("  Vitesse sol au-dessous de laquelle le cap l'emporte sur v²/2c² : v < 2·Ω·R·cosφ = %.0f m/s (%.0f km/h)."
             % (2 * OMEGA_TERRE * R_TERRE * math.cos(math.radians(LAT)), 2 * OMEGA_TERRE * R_TERRE * math.cos(math.radians(LAT)) * 3.6))
    res["sagnac_ps_par_km_est"] = sag * 1e12
    res["vitesse_bascule_m_s"] = 2 * OMEGA_TERRE * R_TERRE * math.cos(math.radians(LAT))

    # Ce que la masse de l'unité elle-même produit (pour mémoire : c'est tout ce que ferait la C204 « telle que décrite »)
    y_self = G * MASSE_UNITE / (1.0 * c**2)
    y_steel = 2 * G * 4.4e12 / (1.0 * c**2)
    L.append("")
    ref_r1 = abs(res["scenarios"]["S05"]["D_futur_s_par_h"])
    L.append("Pour mémoire — potentiel propre de 227 kg à 1 m : GM/(rc²) = %.2e, soit %.2e s par heure (%.1f ordres de grandeur sous le scénario S05 de R1)."
             % (y_self, y_self * 3600, math.log10(ref_r1 / (y_self * 3600))))
    L.append("            — deux masses de 4,4e12 kg (300–500 MW de Hawking) à 1 m : %.2e, soit %.2e s par heure." % (y_steel, y_steel * 3600))
    L.append("            — revendiqué : Γ = %.0f, soit %.3e s par heure." % (GAMMA_REVENDIQUE, DEPL_REVENDIQUE_S_PAR_H))
    res["potentiel_propre_227kg_1m"] = dict(y=y_self, s_par_h=y_self * 3600)
    res["potentiel_2x4.4e12kg_1m"] = dict(y=y_steel, s_par_h=y_steel * 3600)
    res["revendique_s_par_h"] = DEPL_REVENDIQUE_S_PAR_H

    # -----------------------------------------------------------------------------------------
    # Détectabilité : quelle horloge mesure réellement le déplacement ?
    # Modèle (identique à celui de l'Équipe F, calc01) : comparaison avant/après d'une horloge transportée pendant T
    # à une horloge identique restée en bas : bruit ≈ √2·√[(a·√T)² + (plancher·T)²] ; environnement traité à part.
    # -----------------------------------------------------------------------------------------
    HORLOGES = [
        # nom, a (bruit blanc de fréquence à 1 s), plancher de scintillation, effet d'environnement résiduel (relatif),
        # encombrement (mm), masse kg, puissance W, statut des données, entre dans le coffre ?
        ("CSAC au césium (SA.45s)", 3e-10, 5e-12, 5e-11, (41, 36, 12), 0.035, 0.12,
         "a : fiche constructeur vérifiée par l'Équipe C ; plancher et environnement : estimation"),
        ("Rubidium miniature (classe PRS10), nu", 2e-11, 1e-12, 1e-10, (51, 76, 102), 0.6, 14,
         "paramètres de l'Équipe F (calc01) ; environnement : pression, température, champ"),
        ("Rubidium miniature en enceinte étanche thermostatée blindée [à démontrer]", 2e-11, 3e-13, 3e-13, (120, 120, 160), 3.0, 20,
         "hypothèse de conception : gain ×300 sur l'environnement ; plancher : estimation"),
        ("Césium à jet 5071A, tube standard", 2.7e-11, 5e-14, 0.0, (425.5, 523.9, 133.4), 30, 50,
         "dimensions et masse : fiche vérifiée par l'Équipe C ; bruit : paramètres de l'Équipe F"),
        ("Césium à jet 5071A, tube haute performance", 8.5e-12, 1e-14, 0.0, (425.5, 523.9, 133.4), 30, 50,
         "idem ; plancher ≤ 1e-14 vérifié par l'Équipe C"),
        ("Horloge optique à iode, 35 L (Roslund et al. 2024)", None, None, None, (None, None, None), None, None,
         "résumé de l'article : erreur de temps < 300 ps par jour en mer ; volume 35 L"),
    ]
    T48 = 48 * 3600.0
    SIGNAUX = [("S01", 1000), ("S02", 2000), ("S03", 3000)]
    L.append("")
    L.append("DÉTECTABILITÉ (aller-retour de 48 h, une horloge transportée comparée à une horloge identique restée en bas)")
    L.append("%-74s %10s %10s | S/B à +1000 m  +2000 m  +3000 m | Δh min (3σ)" % ("horloge", "bruit ns", "envir. ns"))
    det_csv, det = [], {}
    for nom, a, pl, env, dims, masse, puiss, statut in HORLOGES:
        if a is None:
            bruit = 0.6      # ns : 300 ps/jour × 2 jours (borne du résumé, cumul linéaire prudent)
            envn = 0.0
        else:
            bruit = math.sqrt(2) * math.sqrt((a * math.sqrt(T48))**2 + (pl * T48)**2) * 1e9
            envn = env * T48 * 1e9
        tot = math.hypot(bruit, envn)
        sb = [abs(res["scenarios"][sid]["y"]) * T48 * 1e9 / tot for sid, _ in SIGNAUX]
        dh_min = 3 * tot / (g0 / c**2 * T48 * 1e9)
        det[nom] = dict(bruit_ns=bruit, environnement_ns=envn, total_ns=tot, SB=dict(zip(["1000", "2000", "3000"], sb)),
                        dh_min_3sigma_m=dh_min, dims_mm=dims, masse_kg=masse, puissance_W=puiss, statut=statut)
        L.append("%-74s %10.1f %10.1f | %12.2f %8.2f %8.2f | %8.0f m" % (nom[:74], bruit, envn, sb[0], sb[1], sb[2], dh_min))
        det_csv.append([nom, "" if a is None else f"{a:.1e}", "" if pl is None else f"{pl:.1e}", f"{bruit:.2f}", f"{envn:.2f}", f"{tot:.2f}",
                        f"{sb[0]:.2f}", f"{sb[1]:.2f}", f"{sb[2]:.2f}", f"{dh_min:.0f}",
                        "détecte" if sb[0] >= 3 else ("marginal" if sb[2] >= 3 else "ne détecte pas"), statut])
    res["detectabilite_48h"] = det
    L.append("  Signal : %.1f ns (1 000 m), %.1f ns (2 000 m), %.1f ns (3 000 m) en 48 h."
             % tuple(abs(res["scenarios"][s]["y"]) * T48 * 1e9 for s, _ in SIGNAUX))
    # --- Essai T6 (correction I-3) : à quoi compare-t-on les 3 étalons emportés ?
    a_hp, pl_hp = 8.5e-12, 1e-14
    un = math.hypot(a_hp * math.sqrt(T48), pl_hp * T48) * 1e9             # bruit d'UN étalon haute performance sur 48 h (ns)
    sig = abs(res["scenarios"]["S01"]["y"]) * T48 * 1e9
    b_local = math.sqrt(2) * un / math.sqrt(3)                             # 3 emportés contre 3 restés au sol
    lien = {"GNSS, vue commune sur le code [estimation : 1 ns par comparaison]": 1.0,
            "GNSS, phase de la porteuse avec récepteurs étalonnés [estimation : 0,2 ns par comparaison]": 0.2}
    t6 = {"bruit_un_etalon_48h_ns": un, "signal_1000m_48h_ns": sig,
          "option_a_3_etalons_de_reference_au_sol": dict(bruit_ns=b_local, SB=sig / b_local, cout_supplementaire_kEUR=240, masse_hors_vehicule_kg=90)}
    L.append("")
    L.append("ESSAI T6 — référence des trois étalons emportés (séjour de 48 h à +1 000 m ; signal %.1f ns ; un étalon : %.1f ns)" % (sig, un))
    L.append("  (a) 3 étalons identiques restés au sol (≈ 240 k€, 90 kg, hors véhicule) : bruit %.1f ns → S/B = %.1f" % (b_local, sig / b_local))
    for nom, s_l in lien.items():
        # 3 étalons emportés, raccordés avant et après à une échelle de temps de laboratoire par un lien de bruit s_l (deux comparaisons)
        b = math.hypot(un / math.sqrt(3), math.sqrt(2) * s_l)
        t6["option_b_lien_" + nom] = dict(bruit_lien_par_comparaison_ns=s_l, bruit_total_ns=b, SB=sig / b)
        L.append("  (b) lien de temps %s : bruit %.1f ns → S/B = %.1f" % (nom, b, sig / b))
    L.append("  Le bruit des liens est une ESTIMATION de notre part (ordre de grandeur usuel, non vérifié) ; l'option (b) suppose l'accès")
    L.append("  à une échelle de temps de laboratoire et deux récepteurs étalonnés (≈ 15 k€, estimation).")
    res["essai_T6"] = t6
    L.append("")
    L.append("  Conclusion : aucune horloge miniature (CSAC, rubidium nu) ne mesure le décalage du trajet sur Terre ;")
    L.append("  il faut un étalon à jet de césium (30 kg, 425 × 524 × 133 mm) ou une horloge optique compacte (35 L).")

    ecrire_csv(RACINE / "deplacement_scenarios.csv",
               ["id", "scenario", "altitude_m", "v_est_m_s", "v_nord_m_s", "y_gravitation", "y_cinematique", "y_total",
                "avance_horloge_embarquee_ns_par_h", "decalage_relativiste_du_trajet_D_ns_par_h_(positif_=_l_objet_vieillit_moins)",
                "decalage_relativiste_du_trajet_D_s_par_h", "ecart_cumule_48h_ns", "sens", "trajet_accessible_au_palier", "statut_valeur",
                "remarque", "cause"], [l + ["le trajet (tout objet le subit) ; la machine n'en est pas la cause"] for l in lignes_csv])
    ecrire_csv(RACINE / "detectabilite_horloges.csv",
               ["horloge", "bruit_blanc_frequence_1s", "plancher_scintillation", "bruit_48h_ns", "environnement_48h_ns", "total_48h_ns",
                "SB_1000m", "SB_2000m", "SB_3000m", "denivele_min_3sigma_m", "verdict_palier_1", "statut_des_parametres"], det_csv)
    ecrire_json("i01_deplacement.json", res)
    ecrire_txt("i01_deplacement.txt", L)


if __name__ == "__main__":
    main()
