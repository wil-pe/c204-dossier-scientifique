#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Voteur à trois voies : vote majoritaire (valeurs discrètes) et vote médian (valeurs continues), avec
détection de la voie fautive (Python standard, aucune dépendance).

C'est la redondance modulaire triple classique (Lyons & Vanderkulk 1962) : trois calculateurs font le même
calcul, le voteur retient la valeur majoritaire ou médiane et signale la voie qui s'écarte. Limites à connaître :
  - trois voies tolèrent UNE panne franche ; elles ne tolèrent pas une panne « byzantine » (une voie qui ment
    différemment à chacun) : il en faudrait quatre (Lamport, Shostak & Pease 1982) ;
  - une panne de mode commun (même bogue dans les trois logiciels, même alimentation) passe au travers : d'où
    trois calculateurs d'architectures différentes dans le projet.
Le « protocole de Borda » cité par le récit d'origine n'est pas un mécanisme de tolérance aux pannes : la fonction
`decompte_borda` montre qu'une seule voie fautive peut y renverser deux voies saines.

Usage : python voteur.py        (démonstration)
"""
import math
from statistics import median

UNANIME = "unanime"
MAJORITE = "majorité"
DESACCORD = "désaccord total"
DEGRADE = "dégradé (deux voies)"
INDISPONIBLE = "indisponible"

__all__ = ["vote_majoritaire", "vote_median", "Voteur", "decompte_borda", "UNANIME", "MAJORITE", "DESACCORD", "DEGRADE", "INDISPONIBLE"]


def _valide(v):
    return v is not None and not (isinstance(v, float) and math.isnan(v))


def vote_majoritaire(a, b, c):
    """Vote 2-parmi-3 sur des valeurs discrètes. None = voie absente.

    Renvoie (valeur, état, voie_fautive) ; voie_fautive vaut 0, 1, 2 ou None. En cas de désaccord total ou de
    voie unique, la valeur vaut None : le système doit alors se mettre en état sûr."""
    v = [a, b, c]
    ok = [i for i in range(3) if _valide(v[i])]
    if len(ok) == 3:
        if v[0] == v[1] == v[2]:
            return v[0], UNANIME, None
        for i, j, k in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            if v[i] == v[j]:
                return v[i], MAJORITE, k
        return None, DESACCORD, None
    if len(ok) == 2:
        i, j = ok
        absent = ({0, 1, 2} - {i, j}).pop()
        if v[i] == v[j]:
            return v[i], DEGRADE, absent
        return None, DESACCORD, absent
    return None, INDISPONIBLE, None


def vote_median(a, b, c, tolerance):
    """Vote médian sur des valeurs continues ; une voie est dite fautive si elle s'écarte de la médiane de plus
    de `tolerance` alors que les deux autres s'accordent entre elles.

    Renvoie (valeur, état, voie_fautive). La médiane de trois valeurs est toujours bornée par deux voies saines,
    quelle que soit la valeur fournie par la troisième : c'est ce qui la rend sûre."""
    if tolerance < 0:
        raise ValueError("tolérance négative")
    v = [a, b, c]
    ok = [i for i in range(3) if _valide(v[i])]
    if len(ok) == 3:
        m = median(v)
        hors = [i for i in range(3) if abs(v[i] - m) > tolerance]
        if not hors:
            return m, UNANIME, None
        if len(hors) == 1:
            return m, MAJORITE, hors[0]
        return None, DESACCORD, None
    if len(ok) == 2:
        i, j = ok
        absent = ({0, 1, 2} - {i, j}).pop()
        if abs(v[i] - v[j]) <= tolerance:
            return 0.5 * (v[i] + v[j]), DEGRADE, absent
        return None, DESACCORD, absent
    return None, INDISPONIBLE, None


class Voteur:
    """Voteur médian à mémoire : une voie fautive `seuil_exclusion` fois de suite est exclue jusqu'à réarmement.

    Après exclusion, le voteur fonctionne en mode dégradé (comparaison des deux voies restantes) ; si elles
    divergent, la sortie vaut None et `etat_sur` passe à True : le système doit s'arrêter proprement."""

    def __init__(self, tolerance, seuil_exclusion=3):
        self.tolerance = float(tolerance)
        self.seuil = int(seuil_exclusion)
        self.fautes_consecutives = [0, 0, 0]
        self.fautes_totales = [0, 0, 0]
        self.exclues = set()
        self.etat_sur = False
        self.cycles = 0

    def voter(self, a, b, c):
        v = [a, b, c]
        for i in self.exclues:
            v[i] = None
        valeur, etat, fautive = vote_median(v[0], v[1], v[2], self.tolerance)
        self.cycles += 1
        for i in range(3):
            if i in self.exclues:
                continue
            if etat == MAJORITE and fautive == i:
                self.fautes_consecutives[i] += 1
                self.fautes_totales[i] += 1
                if self.fautes_consecutives[i] >= self.seuil:
                    self.exclues.add(i)
            else:
                self.fautes_consecutives[i] = 0
        if valeur is None:
            self.etat_sur = True
        return valeur, etat, fautive

    def rearmer(self, voie=None):
        """Réintègre une voie (ou toutes) après réparation, et lève l'état sûr."""
        for i in ([voie] if voie is not None else [0, 1, 2]):
            self.exclues.discard(i)
            self.fautes_consecutives[i] = 0
        self.etat_sur = False


def decompte_borda(classements):
    """Décompte de Borda : chaque votant classe les options de la préférée à la moins bonne ; une option reçoit
    (n − 1 − rang) points. Renvoie le dictionnaire des scores.

    Fourni pour montrer pourquoi ce n'est PAS un voteur de sûreté : avec quatre options, deux votants sains qui
    classent A > B > C > D donnent A = 6 et B = 4 ; un seul votant fautif qui classe B > C > D > A porte B à 7 :
    l'option que deux voies saines préfèrent est battue (6 contre 7)."""
    scores = {}
    for classement in classements:
        n = len(classement)
        for rang, option in enumerate(classement):
            scores[option] = scores.get(option, 0) + (n - 1 - rang)
    return scores


def _demo():
    print("Vote majoritaire :", vote_majoritaire("MARCHE", "MARCHE", "ARRET"))
    print("Vote médian      :", vote_median(0.5013, 0.5012, 7.3, tolerance=0.001))
    v = Voteur(tolerance=0.001, seuil_exclusion=3)
    for k in range(5):
        print(f"  cycle {k + 1} :", v.voter(0.5013, 0.5013, 0.9), "| voies exclues :", sorted(v.exclues))
    print("  les deux voies restantes divergent :", v.voter(0.5013, 0.6, 0.9), "| état sûr :", v.etat_sur)
    s = decompte_borda([list("ABCD"), list("ABCD"), list("BCDA")])
    print("Borda (2 voies saines A>B>C>D, 1 fautive B>C>D>A) :", s, "→ gagnant :", max(s, key=s.get), "(les voies saines voulaient A)")


if __name__ == "__main__":
    _demo()
