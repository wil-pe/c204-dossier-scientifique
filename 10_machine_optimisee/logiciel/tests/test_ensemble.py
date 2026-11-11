# -*- coding: utf-8 -*-
"""Tests de l'ensemble de quatre horloges simulées (numpy requis)."""
import os
import sys
import unittest

try:
    import numpy as np
except ImportError:                                   # le reste du logiciel n'a pas besoin de numpy
    raise unittest.SkipTest("numpy absent : tests de l'ensemble d'horloges ignorés")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ensemble_horloges as E  # noqa: E402


class TestSimulation(unittest.TestCase):
    def test_reproductible(self):
        _, x1 = E.simuler_horloges(duree_s=3600, graine=7)
        _, x2 = E.simuler_horloges(duree_s=3600, graine=7)
        self.assertTrue(np.array_equal(x1, x2))

    def test_ecart_type_d_allan_du_bruit_blanc_de_frequence(self):
        _, x = E.simuler_horloges(n=1, duree_s=200000, pas_s=10.0, bruit_blanc_1s=3e-10, graine=3)
        for m, tol in ((1, 0.05), (10, 0.10), (100, 0.25)):
            attendu = 3e-10 / np.sqrt(10.0 * m)
            self.assertAlmostEqual(E.ecart_type_allan(x[0], 10.0, m) / attendu, 1.0, delta=tol)

    def test_six_ecarts_pour_quatre_horloges(self):
        _, x = E.simuler_horloges(duree_s=600, graine=1)
        ec = E.ecarts_deux_a_deux(x)
        self.assertEqual(len(ec), 6)
        self.assertTrue(np.allclose(ec[(0, 1)] + ec[(1, 2)], ec[(0, 2)]))      # fermeture des écarts


class TestDetection(unittest.TestCase):
    def test_chaque_horloge_aberrante_est_identifiee(self):
        for graine in range(8):
            for fautive in range(4):
                t, x = E.simuler_horloges(duree_s=14400, aberrante=fautive, saut_frequence=2e-10, graine=graine)
                trouvee, scores = E.detecter_aberrante(t, x)
                self.assertEqual(trouvee, fautive, msg=f"graine {graine}")
                self.assertGreater(scores[fautive], 15.0)

    def test_pas_de_fausse_alarme_sur_des_horloges_saines(self):
        for graine in range(60):
            t, x = E.simuler_horloges(duree_s=14400, graine=graine)
            trouvee, scores = E.detecter_aberrante(t, x)
            self.assertIsNone(trouvee, msg=f"graine {graine}, scores {scores}")

    def test_un_ecart_de_frequence_permanent_n_est_pas_une_panne(self):
        # des horloges réelles ont toutes un écart de fréquence permanent : avec une période d'étalonnage, on ne
        # détecte que les CHANGEMENTS
        ecarts = [0.0, 1e-10, -1e-10, 2e-10]
        for graine in range(20):
            t, x = E.simuler_horloges(duree_s=14400, ecart_frequence=ecarts, graine=graine)
            self.assertIsNotNone(E.detecter_aberrante(t, x)[0])                       # sans étalonnage : fausse alarme
            self.assertIsNone(E.detecter_aberrante(t, x, etalonnage_s=3600)[0])       # avec : rien à signaler
            t, x = E.simuler_horloges(duree_s=14400, ecart_frequence=ecarts, aberrante=1, saut_frequence=2e-10, graine=graine)
            self.assertEqual(E.detecter_aberrante(t, x, etalonnage_s=3600)[0], 1)

    def test_derive_forte_d_une_horloge(self):
        t, x = E.simuler_horloges(duree_s=14400, derive_par_s=[0.0, 5e-14, 0.0, 0.0], graine=2)
        self.assertEqual(E.detecter_aberrante(t, x)[0], 1)

    def test_trois_horloges_minimum(self):
        t, x = E.simuler_horloges(n=2, duree_s=600, graine=1)
        with self.assertRaises(ValueError):
            E.detecter_aberrante(t, x)


class TestEnsemble(unittest.TestCase):
    def test_l_exclusion_ameliore_le_temps_d_ensemble(self):
        t, x = E.simuler_horloges(duree_s=14400, aberrante=0, saut_frequence=2e-10, graine=4)
        fautive, _ = E.detecter_aberrante(t, x)
        fin = t >= t[-1] - 3600
        avec = np.ptp(E.echelle_ensemble(x)[fin])
        sans = np.ptp(E.echelle_ensemble(x, exclues=[fautive])[fin])
        self.assertLess(sans, avec / 3)

    def test_la_moyenne_de_quatre_horloges_saines_est_deux_fois_moins_bruitee(self):
        _, x = E.simuler_horloges(duree_s=200000, graine=9)
        seule = E.ecart_type_allan(x[0], 10.0, 10)
        ensemble = E.ecart_type_allan(E.echelle_ensemble(x), 10.0, 10)
        self.assertAlmostEqual(seule / ensemble, 2.0, delta=0.3)              # √4

    def test_tout_exclure_est_une_erreur(self):
        _, x = E.simuler_horloges(duree_s=600, graine=1)
        with self.assertRaises(ValueError):
            E.echelle_ensemble(x, exclues=[0, 1, 2, 3])

    def test_le_decalage_relativiste_est_sous_le_bruit(self):
        """Rappel chiffré : 10⁻¹³ (1 000 m de dénivelé) contre le bruit d'une horloge miniature moyenné sur 48 h."""
        bruit_48h = 3e-10 / np.sqrt(48 * 3600.0)
        self.assertGreater(bruit_48h / 1.09e-13, 5.0)


if __name__ == "__main__":
    unittest.main()
