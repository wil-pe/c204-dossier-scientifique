# -*- coding: utf-8 -*-
"""Tests du voteur à trois voies."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import voteur as V  # noqa: E402


class TestVoteMajoritaire(unittest.TestCase):
    def test_unanime(self):
        self.assertEqual(V.vote_majoritaire(1, 1, 1), (1, V.UNANIME, None))

    def test_une_voie_fautive_a_chaque_position(self):
        self.assertEqual(V.vote_majoritaire(0, 1, 1), (1, V.MAJORITE, 0))
        self.assertEqual(V.vote_majoritaire(1, 0, 1), (1, V.MAJORITE, 1))
        self.assertEqual(V.vote_majoritaire(1, 1, 0), (1, V.MAJORITE, 2))

    def test_desaccord_total(self):
        self.assertEqual(V.vote_majoritaire("a", "b", "c"), (None, V.DESACCORD, None))

    def test_voie_absente(self):
        self.assertEqual(V.vote_majoritaire(1, None, 1), (1, V.DEGRADE, 1))
        self.assertEqual(V.vote_majoritaire(1, None, 0), (None, V.DESACCORD, 1))
        self.assertEqual(V.vote_majoritaire(None, None, 1), (None, V.INDISPONIBLE, None))


class TestVoteMedian(unittest.TestCase):
    def test_unanime_dans_la_tolerance(self):
        v, etat, f = V.vote_median(1.000, 1.001, 0.999, tolerance=0.01)
        self.assertEqual((v, etat, f), (1.000, V.UNANIME, None))

    def test_voie_aberrante_identifiee(self):
        for position in range(3):
            voies = [0.5013, 0.5012, 0.5014]
            voies[position] = 42.0
            v, etat, f = V.vote_median(*voies, tolerance=0.001)
            self.assertEqual((etat, f), (V.MAJORITE, position))
            self.assertTrue(0.5012 <= v <= 0.5014)

    def test_la_mediane_est_bornee_par_deux_voies_saines(self):
        rnd = random.Random(204)
        for _ in range(2000):
            a, b = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            c = rnd.choice([rnd.uniform(-1e9, 1e9), float("inf"), -float("inf")])
            v, _etat, _f = V.vote_median(a, b, c, tolerance=10.0)
            if v is not None:
                self.assertTrue(min(a, b) <= v <= max(a, b))

    def test_nan_traite_comme_absent(self):
        v, etat, f = V.vote_median(1.0, float("nan"), 1.0, tolerance=0.1)
        self.assertEqual((v, etat, f), (1.0, V.DEGRADE, 1))

    def test_deux_voies_en_desaccord(self):
        self.assertEqual(V.vote_median(1.0, None, 2.0, tolerance=0.1), (None, V.DESACCORD, 1))

    def test_trois_voies_en_desaccord(self):
        self.assertEqual(V.vote_median(1.0, 2.0, 3.0, tolerance=0.1), (None, V.DESACCORD, None))

    def test_tolerance_negative(self):
        with self.assertRaises(ValueError):
            V.vote_median(1, 1, 1, tolerance=-1)


class TestVoteurAMemoire(unittest.TestCase):
    def test_exclusion_apres_trois_fautes_consecutives(self):
        v = V.Voteur(tolerance=0.001, seuil_exclusion=3)
        for _ in range(2):
            self.assertEqual(v.voter(1.0, 1.0, 5.0)[1:], (V.MAJORITE, 2))
        self.assertEqual(v.exclues, set())
        v.voter(1.0, 1.0, 5.0)
        self.assertEqual(v.exclues, {2})
        self.assertEqual(v.voter(1.0, 1.0, 5.0), (1.0, V.DEGRADE, 2))
        self.assertFalse(v.etat_sur)

    def test_une_faute_isolee_n_exclut_pas(self):
        v = V.Voteur(tolerance=0.001, seuil_exclusion=3)
        v.voter(1.0, 9.0, 1.0)
        v.voter(1.0, 1.0, 1.0)
        v.voter(1.0, 9.0, 1.0)
        v.voter(1.0, 9.0, 1.0)
        self.assertEqual(v.exclues, set())
        self.assertEqual(v.fautes_totales, [0, 3, 0])

    def test_etat_sur_si_les_deux_voies_restantes_divergent(self):
        v = V.Voteur(tolerance=0.001, seuil_exclusion=1)
        v.voter(1.0, 1.0, 5.0)
        valeur, etat, _ = v.voter(1.0, 2.0, 5.0)
        self.assertIsNone(valeur)
        self.assertEqual(etat, V.DESACCORD)
        self.assertTrue(v.etat_sur)
        v.rearmer()
        self.assertFalse(v.etat_sur)
        self.assertEqual(v.voter(1.0, 1.0, 1.0), (1.0, V.UNANIME, None))


class TestBorda(unittest.TestCase):
    def test_une_voie_fautive_renverse_deux_voies_saines(self):
        scores = V.decompte_borda([list("ABCD"), list("ABCD"), list("BCDA")])
        self.assertEqual((scores["A"], scores["B"]), (6, 7))
        self.assertEqual(max(scores, key=scores.get), "B")
        # le vote majoritaire, lui, donne raison aux deux voies saines
        self.assertEqual(V.vote_majoritaire("A", "A", "B"), ("A", V.MAJORITE, 2))


if __name__ == "__main__":
    unittest.main()
