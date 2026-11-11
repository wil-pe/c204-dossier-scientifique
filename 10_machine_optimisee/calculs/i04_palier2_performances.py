#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i04 : performances calculées du palier 2 (C204-R2, laboratoire de recherche).

Quatre modules, chacun avec ce qu'il MESURE (ou SIMULE) réellement :
  M1  horloges optiques (ions piégés / réseau, transportables) : résolution du déplacement temporel ;
  M2  gravimètre et gradiomètre à atomes froids (« VGL » de classe microgal) ;
  M3  simulateur analogique de Kerr à deux vortex (cuve) — SIMULATION ANALOGIQUE, pas de gravitation ;
  M4  simulateur quantique de courbes temporelles fermées (P-CTC, D-CTC) et interrupteur quantique —
      SIMULATION : circuits causalement ordonnés ; rien ne remonte le temps.

Chiffres d'entrée : résumés d'articles vérifiés par API (verification_refs/resultats_verification.json) ;
les paramètres de conception de la cuve sont des choix de notre part, marqués comme tels.

Sorties : resultats/i04_palier2.json / .txt
"""
import math

import numpy as np

from i00_commun import G, c, g0, hbar, kB, ecrire_json, ecrire_txt

AN = 365.25 * 86400


def main():
    L = ["i04 — PERFORMANCES DU PALIER 2 (C204-R2)", "=" * 100]
    res = {}

    # ------------------------------------------------------------------ M1 horloges optiques
    L.append("M1 — HORLOGES OPTIQUES")
    horloges = [
        # nom, incertitude systématique, instabilité à 1 s (1/√τ), source
        ("Ion unique ²⁷Al⁺ (Marshall et al. 2025)", 5.5e-19, 3.5e-16, "résumé vérifié"),
        ("Ion unique ¹⁷⁶Lu⁺ (Arnold et al. 2026)", 1.2e-19, 4.8e-16, "résumé vérifié (instabilité de la comparaison)"),
        ("Réseau ⁸⁷Sr transportable (Koller et al. 2017)", 7e-17, None, "titre vérifié (7×10⁻¹⁷) ; instabilité non lue"),
        ("Horloge à iode de 35 L (Roslund et al. 2024)", 300e-12 / 86400, None, "résumé vérifié : < 300 ps/jour, soit 3,5×10⁻¹⁵ en valeur relative sur un jour"),
    ]
    res["M1"] = {}
    for nom, u, s1, src in horloges:
        dh = u * c**2 / g0
        d = dict(incertitude=u, denivele_equivalent_m=dh, resolution_s_par_h=u * 3600, source=src)
        if s1:
            d["temps_pour_1e-18_s"] = (s1 / 1e-18)**2
            d["temps_pour_incertitude_s"] = (s1 / u)**2
        res["M1"][nom] = d
        L.append("  %-50s u = %.1e → %.2e m de dénivelé ; résolution %.1e s par heure%s"
                 % (nom, u, dh, u * 3600, ("" if not s1 else " ; 10⁻¹⁸ atteint en %.1f h de moyenne" % ((s1 / 1e-18)**2 / 3600))))
    # ce que voit une horloge à 1e-18 : dénivelés et masses
    y18 = 1e-18
    L.append("  Une comparaison à 10⁻¹⁸ résout : %.1f mm de dénivelé terrestre ; à 10⁻¹⁹ : %.2f mm." % (y18 * c**2 / g0 * 1000, 1e-19 * c**2 / g0 * 1000))
    entraxe = 0.0925
    L.append("  Les deux logements (entraxe %.1f mm) : si l'un est surélevé de 10 mm, Δf/f = %.2e ; de 100 mm : %.2e." %
             (entraxe * 1000, g0 * 0.010 / c**2, g0 * 0.100 / c**2))
    # masse détectable par son potentiel à 1 m
    for y in (1e-18, 1e-19):
        M = y * c**2 * 1.0 / G
        res["M1"][f"masse_detectable_a_1m_pour_y={y:.0e}"] = M
        L.append("  Masse dont le potentiel à 1 m vaut %.0e : %.2e kg (une masse de laboratoire de 1 t donne %.1e : indétectable)."
                 % (y, M, G * 1000 / c**2))
    M_s = 4.4e12
    r_det = G * 2 * M_s / (1e-18 * c**2)
    res["M1"]["distance_detection_2x4.4e12kg_m"] = r_det
    L.append("  Si deux « singularités » de 4,4×10¹² kg existaient, une horloge à 10⁻¹⁸ verrait leur potentiel jusqu'à %.1f km." % (r_det / 1000))
    res["M1"]["signal_scenarios_R1_vs_resolution"] = {"+1000 m": 1.091e-13 / 1e-18, "130 km/h est": 1.392e-13 / 1e-18}
    L.append("  Rapport signal / résolution (10⁻¹⁸) sur les scénarios du palier 1 : ≈ %.0e (dénivelé de 1 000 m), ≈ %.0e (130 km/h vers l'est)."
             % (1.091e-13 / 1e-18, 1.392e-13 / 1e-18))
    L.append("  Limite : une horloge optique est un étalon de FRÉQUENCE à fonctionnement intermittent ; on mesure un taux (par lien fibré")
    L.append("  stabilisé ou par comparaison locale avant/après), pas directement un temps accumulé sur 48 h.")

    # ------------------------------------------------------------------ M2 gravimétrie atomique
    L.append("")
    L.append("M2 — GRAVIMÈTRE ET GRADIOMÈTRE À ATOMES FROIDS")
    dg = 1e-8        # 1 µGal = 1e-8 m/s² : stabilité long terme (Ménoret et al. 2018, résumé vérifié)
    grad_air = 3.086e-6
    res["M2"] = dict(stabilite_m_s2=dg, denivele_equivalent_mm=dg / grad_air * 1000)
    L.append("  Stabilité 10 nm/s² = 1 µGal (Ménoret et al. 2018) ↔ %.1f mm de dénivelé (gradient à l'air libre 308,6 µGal/m)." % (dg / grad_air * 1000))
    for M in (1e3, 1e4, 2.27e2):
        r = math.sqrt(G * M / (3 * dg))
        res["M2"][f"portee_3sigma_masse_{M:.0f}kg_m"] = r
        L.append("  Masse de %6.0f kg détectée à 3 σ (3 µGal) jusqu'à %.2f m." % (M, r))
    # gradiomètre : 20 E statistique (Stray 2022) ; 0,1 E long terme (Janvier 2022) ; gradient d'une masse M à r : 2GM/r³
    for E_res, nom in ((20e-9, "20 E (Stray et al. 2022)"), (0.1e-9, "0,1 E à long terme (Janvier et al. 2022)")):
        r = (2 * G * 1e3 / E_res)**(1 / 3)
        res["M2"][f"portee_gradiometre_1t_{nom}"] = r
        L.append("  Gradiomètre %s : une tonne à %.2f m donne ce gradient (2GM/r³)." % (nom, r))
    # prédiction du décalage d'horloge par nivellement + gravimétrie : dW = g dh ; exactitude
    L.append("  Rôle dans la machine : fournir la prédiction classique ΔW = ∫g·dh du décalage d'horloge. Avec g à 1 µGal (10⁻⁹ g) et Δh à")
    L.append("  1 cm sur 1 000 m (10⁻⁵), la prédiction est limitée par le nivellement, à ~10⁻⁵ en valeur relative, soit ~10⁻¹⁸ sur 10⁻¹³.")
    res["M2"]["limite_prediction_relative"] = 1e-5

    # cotes de la page de champ DOC-014 (5, 6, 8, 11 m) : ce que les instruments réels verraient à ces distances
    L.append("  Aux distances cotées sur DOC-014 (Équipe A) — ce que des instruments réels y distinguent :")
    res["DOC-014"] = {}
    for d_m, nom in ((5.0, "décalage de masse"), (6.0, "distance verticale de sécurité"), (8.0, "distance arrière"), (11.0, "distance avant")):
        y_v = g0 * d_m / c**2
        M3 = 3 * dg * d_m**2 / G
        res["DOC-014"][nom] = dict(distance_m=d_m, decalage_si_denivele=y_v, masse_detectable_3microGal_kg=M3)
        L.append("    %4.0f m (%s) : un dénivelé de cette valeur décale les horloges de %.2e ; une masse n'y est vue par le gravimètre (3 µGal) qu'au-delà de %.0f t."
                 % (d_m, nom, y_v, M3 / 1000))

    # ------------------------------------------------------------------ M3 cuve à deux vortex
    L.append("")
    L.append("M3 — SIMULATEUR ANALOGIQUE DE KERR À DEUX VORTEX (paramètres de conception : choix de notre part)")
    h = 0.0625                  # m : profondeur de Torres et al. 2017 (résumé vérifié)
    cw = math.sqrt(g0 * h)      # ondes longues ; l'expérience de 2017 était en régime dispersif
    Q = 0.5e-3                  # m³/s par orifice [choix]
    Dd = Q / (2 * math.pi * h)
    Cc = 1.5e-2                 # m²/s : circulation par vortex [choix]
    r_h = Dd / cw
    r_e = math.sqrt(Cc**2 + Dd**2) / cw
    Om_h = Cc / r_h**2
    T_H = hbar * cw / (2 * math.pi * kB * r_h)
    d_sep = 0.60                # m : entraxe des deux vortex [choix]
    f_cav = cw / (2 * d_sep)
    Om_orb = 2 * Cc / d_sep**2  # vitesse angulaire d'une paire de vortex libres de même signe
    v_trans = Cc / d_sep        # vitesse de translation d'une paire de signes opposés
    # bande superradiante (critère idéal ω < m Ω_H évalué au rayon de l'ergosurface pour rester dans le régime ondes longues)
    Om_e = Cc / r_e**2
    f_sr = {m: m * Om_e / (2 * math.pi) for m in (1, 2)}
    res["M3"] = dict(profondeur_m=h, celerite_ondes_longues_m_s=cw, debit_par_orifice_L_s=Q * 1e3, D_m2_s=Dd, C_m2_s=Cc,
                     r_horizon_mm=r_h * 1e3, r_ergo_mm=r_e * 1e3, rotation_ergo_rad_s=Om_e, temperature_Hawking_analogue_K=T_H,
                     entraxe_m=d_sep, frequence_cavite_Hz=f_cav, rotation_paire_libre_rad_s=Om_orb, translation_paire_opposee_m_s=v_trans,
                     bande_superradiante_Hz=f_sr, amplification_publiee="jusqu'à 20 % à 3,70 Hz, h = 6,25 cm (résumé arXiv de Torres et al. 2017 ; 14 ± 8 % dans la version publiée selon l'Équipe F)")
    L.append("  Cuve 3 m × 1,5 m, h = %.2f cm : célérité des ondes longues %.2f m/s." % (h * 100, cw))
    L.append("  Par vortex (débit %.1f L/s, circulation %.1e m²/s) : horizon analogue r = %.1f mm ; ergosurface r = %.1f mm ;"
             % (Q * 1e3, Cc, r_h * 1e3, r_e * 1e3))
    L.append("    rotation à l'ergosurface %.1f rad/s ; ondes amplifiables (critère idéal ω < mΩ) : f < %.2f Hz (m = 1), < %.2f Hz (m = 2)."
             % (Om_e, f_sr[1], f_sr[2]))
    L.append("    Température de Hawking analogue : %.1e K (inobservable dans de l'eau à 293 K : seuls les effets STIMULÉS sont mesurables)." % T_H)
    L.append("  Deux vortex distants de %.2f m : premier mode de cavité entre les deux ergorégions ≈ %.2f Hz ; paire libre de même sens :"
             % (d_sep, f_cav))
    L.append("    rotation mutuelle %.3f rad/s ; paire de sens opposés : translation %.1f cm/s (d'où des orifices fixes pour les épingler)."
             % (Om_orb, v_trans * 100))
    L.append("  Repère publié : amplification maximale de 20 % à 3,70 Hz pour h = 6,25 cm, un seul vortex (Torres et al. 2017, résumé).")
    L.append("  À notre connaissance, aucune expérience publiée ne porte sur DEUX vortex de vidange en interaction (question Q9 de l'Équipe H).")

    # ------------------------------------------------------------------ M4 simulation quantique de CTC
    L.append("")
    L.append("M4 — SIMULATEUR QUANTIQUE DE COURBES TEMPORELLES FERMÉES (calcul matriciel exact)")
    I2 = np.eye(2)
    X = np.array([[0, 1], [1, 0]], complex)
    Z = np.array([[1, 0], [0, -1]], complex)
    Y = np.array([[0, -1j], [1j, 0]])
    H = (X + Z) / math.sqrt(2)

    # (a) P-CTC : un qubit traverse la boucle et subit U = exp(−iθX/2) ; probabilité de post-sélection p = |Tr U|²/d²
    res["M4"] = {"P-CTC": {}}
    L.append("  (a) P-CTC (téléportation post-sélectionnée, Lloyd et al. 2011) : le qubit de la boucle subit U(θ) = exp(−iθX/2).")
    for th_deg in (0, 45, 90, 135, 170, 180):
        th = math.radians(th_deg)
        U = math.cos(th / 2) * I2 - 1j * math.sin(th / 2) * X
        p = abs(np.trace(U))**2 / 4
        res["M4"]["P-CTC"][f"theta={th_deg}"] = float(p)
        L.append("      θ = %3d° : fraction d'essais conservés p = |Tr U|²/4 = %.4f%s"
                 % (th_deg, p, "   ← « paradoxe du grand-père » : aucun essai n'est jamais post-sélectionné" if th_deg == 180 else ""))
    # taux utile avec une source de paires de 1e4 coïncidences/s et une post-sélection de Bell à 1/4
    for th_deg in (90, 170):
        p = res["M4"]["P-CTC"][f"theta={th_deg}"]
        L.append("      Source de 10⁴ paires/s : %.0f essais conservés par seconde à θ = %d°." % (1e4 * p, th_deg))

    # (b) D-CTC : point fixe de Deutsch ρ = Tr_CR[U (ρ_in ⊗ ρ) U†]
    def point_fixe(U, rho_in, n=4000):
        rho = I2 / 2          # départ maximalement mélangé + moyenne des itérés : sélectionne le point fixe d'entropie maximale
        acc = np.zeros((2, 2), complex)
        for _ in range(n):
            tot = U @ np.kron(rho_in, rho) @ U.conj().T
            t4 = tot.reshape(2, 2, 2, 2)                 # indices (cr, ctc, cr', ctc')
            rho = np.einsum("abac->bc", t4)              # trace sur CR
            acc += rho
        rho = acc / n
        tot = U @ np.kron(rho_in, rho) @ U.conj().T
        out_cr = np.einsum("abcb->ac", tot.reshape(2, 2, 2, 2))
        return rho, out_cr

    ket = lambda v: np.outer(v, np.conj(v))
    k0, k1 = np.array([1, 0], complex), np.array([0, 1], complex)
    kp, km = (k0 + k1) / math.sqrt(2), (k0 - k1) / math.sqrt(2)
    # grand-père : CNOT (contrôle = qubit de la boucle, cible = CR) puis NON sur la boucle… forme minimale : U = I ⊗ X
    rho, _ = point_fixe(np.kron(I2, X), ket(k0))
    S = -sum(float(l) * math.log2(l) for l in np.linalg.eigvalsh(rho).real if l > 1e-12)
    res["M4"]["D-CTC_grand_pere"] = dict(rho=[[float(abs(x)) for x in r] for r in rho], entropie_bits=S)
    L.append("  (b) D-CTC (Deutsch 1991) — porte NON sur la boucle : point fixe ρ = diag(%.2f, %.2f), entropie %.2f bit : l'état est"
             % (rho[0, 0].real, rho[1, 1].real, S))
    L.append("      maximalement mélangé ; le « paradoxe » est remplacé par une perte totale d'information.")
    # discrimination d'états non orthogonaux (Brun, Harrington & Wilde 2009) : ÉCHANGE puis Hadamard contrôlé (contrôle = sortie CR, cible = boucle)
    SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], complex)
    CH = np.kron(ket(k0), I2) + np.kron(ket(k1), H)       # contrôle = premier qubit (CR), cible = second (boucle)
    U = CH @ SWAP
    res["M4"]["D-CTC_discrimination"] = {}
    L.append("      Circuit ÉCHANGE + Hadamard contrôlé : états d'entrée |0⟩ et |−⟩ (recouvrement |⟨0|−⟩|² = 0,5).")
    for nom, v in (("|0>", k0), ("|->", km)):
        rho, out = point_fixe(U, ket(v))
        p1 = out[1, 1].real
        res["M4"]["D-CTC_discrimination"][nom] = dict(P_sortie_1=float(p1))
        L.append("        entrée %s → probabilité de lire « 1 » en sortie : %.4f" % (nom.replace(">", "⟩"), p1))
    helstrom = 0.5 * (1 - math.sqrt(1 - 0.5))
    res["M4"]["D-CTC_discrimination"]["erreur_minimale_mecanique_quantique_lineaire"] = helstrom
    L.append("      → discrimination parfaite, alors que la mécanique quantique linéaire impose une erreur ≥ %.3f (borne de Helstrom)." % helstrom)
    L.append("      C'est la signature de la NON-LINÉARITÉ du modèle ; l'expérience (Ringbauer et al. 2014) la simule en préparant")
    L.append("      l'état de la boucle qui satisfait la condition de cohérence (de mémoire) : simulation, pas boucle temporelle.")

    # (c) interrupteur quantique : un seul appel de A et de B décide commutation / anticommutation
    L.append("  (c) Interrupteur quantique (Procopio et al. 2015) : contrôle en |+⟩, cible quelconque ; mesure du contrôle dans la base ±.")
    rng = np.random.default_rng(7)
    psi = rng.normal(size=2) + 1j * rng.normal(size=2)
    psi /= np.linalg.norm(psi)
    res["M4"]["interrupteur"] = {}
    for nom, A, B in (("X, X (commutent)", X, X), ("X, Z (anticommutent)", X, Z), ("Y, Z (anticommutent)", Y, Z), ("Z, Z (commutent)", Z, Z),
                      ("X, H (ni l'un ni l'autre)", X, H)):
        plus = 0.5 * (A @ B + B @ A) @ psi
        p_plus = float(np.vdot(plus, plus).real)
        res["M4"]["interrupteur"][nom] = p_plus
        L.append("        A, B = %-28s P(contrôle = +) = %.3f" % (nom, p_plus))
    L.append("      Un seul usage de chaque porte suffit, contre deux pour tout circuit à ordre fixe : avantage de calcul réel,")
    L.append("      mais l'ordre « indéfini » est plongé dans un espace-temps ordinaire : aucune boucle causale.")
    L.append("")
    L.append("Aucun des quatre modules ne transmet d'information vers le passé ; M3 et M4 sont des SIMULATIONS.")
    ecrire_json("i04_palier2.json", res)
    ecrire_txt("i04_palier2.txt", L)


if __name__ == "__main__":
    main()
