# -*- coding: utf-8 -*-
"""Tests du calcul du décalage relativiste. Les valeurs attendues recoupent le script i01 du dossier
(10_machine_optimisee/calculs/i01_deplacement_temporel.py) et trois résultats publiés ou connus."""
import csv
import inspect
import json
import math
import os
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(ICI))
import decalage_relativiste as D  # noqa: E402

# Écarts relatifs y calculés par i01 (latitude 45°, référence au niveau 0) : valeurs copiées de i01_deplacement.json
Y_I01 = {
    "S01": 1.0905938964665548e-13, "S02": 2.180844651117114e-13, "S03": 3.270752425316024e-13,
    "S04": -1.090937199748032e-13, "S05": -1.392459247559734e-13, "S06": 1.247368306608298e-13,
    "S07": -7.254547047571844e-15, "S08": -3.688583982450218e-13, "S09": 2.809453073963407e-13,
    "S10": -9.786713408260976e-14, "S11": 1.7327751696483259e-12,
}
JSON_I01 = os.path.join(os.path.dirname(os.path.dirname(ICI)), "calculs", "resultats", "i01_deplacement.json")


class TestScenarios(unittest.TestCase):
    def test_scenarios_du_rapport_en_ns_par_heure(self):
        for cle, (_lib, alt, v, cap, attendu) in D.SCENARIOS.items():
            y = D.taux_cap(D.LATITUDE_SCENARIOS, alt, v, cap)
            self.assertAlmostEqual(y * 3600e9, attendu, delta=6e-5, msg=cle)

    def test_valeurs_exactes_du_script_i01(self):
        for cle, y_ref in Y_I01.items():
            _lib, alt, v, cap, _ = D.SCENARIOS[cle]
            y = D.taux_cap(D.LATITUDE_SCENARIOS, alt, v, cap)
            self.assertAlmostEqual(y / y_ref, 1.0, delta=1e-9, msg=cle)

    @unittest.skipUnless(os.path.exists(JSON_I01), "résultats du script i01 absents (dépôt logiciel seul)")
    def test_recoupement_direct_avec_i01(self):
        with open(JSON_I01, encoding="utf-8") as f:
            ref = json.load(f)["scenarios"]
        for cle, (_lib, alt, v, cap, _) in D.SCENARIOS.items():
            y = D.taux_cap(D.LATITUDE_SCENARIOS, alt, v, cap)
            self.assertAlmostEqual(y, ref[cle]["y"], delta=1e-22, msg=cle)

    def test_parking_ecart_nul(self):
        self.assertEqual(D.taux(45.0, 0.0)[2], 0.0)


class TestControlesPhysiques(unittest.TestCase):
    def test_gps_38_6_microsecondes_par_jour(self):
        y = D.taux_orbite(20184e3, latitude_ref_deg=0.0)[2]
        self.assertAlmostEqual(y * 86400e6, 38.6, delta=0.05)

    def test_station_spatiale(self):
        y = D.taux_orbite(420e3, latitude_ref_deg=45.0)[2]
        self.assertAlmostEqual(y * 86400e6, -24.44, delta=0.05)          # l'horloge en orbite basse RETARDE

    def test_project_great_22_ns(self):
        y = D.taux(45.0, 1340.0)[2]
        self.assertAlmostEqual(y * 42 * 3600e9, 22.1, delta=0.05)        # 22 ns prédits, ≈ 23 observés (Van Baak)

    def test_hafele_keating_modele_simplifie(self):
        est = D.taux(34.0, 9000.0, +230.0, 0.0)[2] * 41.2 * 3600e9
        ouest = D.taux(34.0, 9000.0, -230.0, 0.0)[2] * 48.6 * 3600e9
        self.assertAlmostEqual(est, -44.7, delta=0.2)                    # observé : −59 ± 10 ns
        self.assertAlmostEqual(ouest, 292.6, delta=0.2)                  # observé : +273 ± 7 ns
        self.assertLess(est, 0)
        self.assertGreater(ouest, 0)

    def test_sagnac_par_kilometre(self):
        self.assertAlmostEqual(D.sagnac_ps_par_km(45.0), 3.655, delta=0.001)

    def test_asymetrie_est_ouest(self):
        v = 130 / 3.6
        y_e, y_o, y_n = (D.taux_cap(45.0, 0.0, v, cap) for cap in (90.0, 270.0, 0.0))
        self.assertLess(y_e, 0)          # vers l'est : l'objet vieillit moins
        self.assertGreater(y_o, 0)       # vers l'ouest : il vieillit plus
        self.assertAlmostEqual((y_e + y_o) / (2 * y_n), 1.0, delta=1e-9)   # la moyenne est le terme en v²/2c²

    def test_decalage_gravitationnel_par_metre(self):
        y = D.taux(45.0, 1.0)[2]
        self.assertAlmostEqual(y, 1.09e-16, delta=0.01e-16)

    def test_aucun_parametre_de_masse(self):
        """Le décalage est celui du trajet : la masse de l'objet n'intervient nulle part (un lest subit le même)."""
        for f in (D.taux, D.taux_cap, D.integrer):
            self.assertFalse(any("mass" in p.lower() for p in inspect.signature(f).parameters))


class TestIntegration(unittest.TestCase):
    def test_une_heure_vers_l_est(self):
        r = D.integrer(D.trace_constante(3600, 45.0, 0.0, 130 / 3.6, 90.0))
        self.assertAlmostEqual(r["ecart_cumule_ns"], -0.5013, delta=1e-4)
        self.assertIn("MOINS", r["sens"])

    def test_aller_retour_est_puis_ouest(self):
        aller = D.trace_constante(3600, 45.0, 0.0, 130 / 3.6, 90.0)
        retour = [(t + 3600 + 1e-6, la, al, v, 270.0) for (t, la, al, v, _c) in D.trace_constante(3600, 45.0, 0.0, 130 / 3.6, 90.0)]
        r = D.integrer(aller + retour)
        self.assertAlmostEqual(r["ecart_cumule_ns"], -0.5013 + 0.4491, delta=2e-4)   # il ne reste que 2 × v²/2c²

    def test_sejour_de_48_h_a_1000_m(self):
        r = D.integrer(D.trace_constante(48 * 3600, 45.0, 1000.0), altitude_ref_m=0.0)
        self.assertAlmostEqual(r["ecart_cumule_ns"], 18.84, delta=0.01)
        self.assertIn("PLUS", r["sens"])

    def test_reference_a_la_meme_altitude(self):
        r = D.integrer(D.trace_constante(3600, 45.0, 1000.0))          # référence = premier point
        self.assertEqual(r["ecart_cumule_s"], 0.0)

    def test_trapezes_sur_une_rampe(self):
        # montée linéaire de 0 à 1 000 m en une heure : l'écart vaut la moitié de celui d'une heure à 1 000 m (à 0,1 % près)
        pts = [(i * 60.0, 45.0, 1000.0 * i / 60, 0.0, 0.0) for i in range(61)]
        r = D.integrer(pts)
        self.assertAlmostEqual(r["ecart_cumule_ns"], 0.3926 / 2, delta=3e-4)

    def test_erreurs(self):
        with self.assertRaises(ValueError):
            D.integrer([(0, 45, 0, 0, 0)])
        with self.assertRaises(ValueError):
            D.integrer([(0, 45, 0, 0, 0), (0, 45, 0, 0, 0)])

    def test_lecture_csv(self):
        with tempfile.TemporaryDirectory() as d:
            chemin = os.path.join(d, "trace.csv")
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["t_s", "latitude_deg", "altitude_m", "vitesse_m_s", "cap_deg"])
                for p in D.trace_constante(3600, 45.0, 0.0, 320 / 3.6, 90.0, pas_s=600):
                    w.writerow(p)
            r = D.integrer(D.lire_trace_csv(chemin))
            self.assertAlmostEqual(r["taux_moyen_ns_par_h"], -1.3279, delta=1e-4)
            with open(chemin, "w", encoding="utf-8") as f:
                f.write("t_s,latitude_deg\n0,45\n")
            with self.assertRaises(ValueError):
                D.lire_trace_csv(chemin)

    def test_exemples_fournis(self):
        ex = os.path.join(os.path.dirname(ICI), "exemples")
        r = D.integrer(D.lire_trace_csv(os.path.join(ex, "trace_route_est_1h.csv")))
        self.assertAlmostEqual(r["ecart_cumule_ns"], -0.5013, delta=1e-3)
        r = D.integrer(D.lire_trace_csv(os.path.join(ex, "trace_montee_1000m.csv")))
        self.assertTrue(17.0 < r["ecart_cumule_ns"] < 18.84)             # 44 h à +1 000 m et deux rampes de 2 h
        self.assertAlmostEqual(r["duree_s"], 48 * 3600, delta=1)


if __name__ == "__main__":
    unittest.main()
