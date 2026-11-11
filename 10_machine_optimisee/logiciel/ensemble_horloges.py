#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ensemble de quatre horloges : comparaison deux à deux, détection et exclusion d'une horloge aberrante
(Python + numpy).

Pourquoi quatre horloges ? On ne mesure jamais une horloge seule, seulement des ÉCARTS entre horloges. Avec deux
horloges on sait qu'elles divergent, pas laquelle ; avec trois on identifie la fautive ; la quatrième permet de
continuer à voter après l'exclusion. C'est l'architecture « quatre horloges » du récit d'origine, et celle des
satellites de navigation.

Ce module SIMULE des horloges (bruit blanc de fréquence, écart de fréquence, dérive, saut de fréquence) pour
mettre au point le traitement avant de brancher du matériel. Il ne mesure rien et ne dit rien de la relativité :
le décalage relativiste d'un trajet (≈ 10⁻¹³) est très en dessous du bruit des horloges simulées ici (10⁻¹⁰ à 1 s).

Usage : python ensemble_horloges.py        (démonstration reproductible)
"""
import numpy as np

__all__ = ["simuler_horloges", "ecarts_deux_a_deux", "scores_aberration", "detecter_aberrante", "echelle_ensemble", "ecart_type_allan"]


def simuler_horloges(n=4, duree_s=86400.0, pas_s=10.0, bruit_blanc_1s=3e-10, ecart_frequence=None, derive_par_s=None,
                     aberrante=None, saut_frequence=0.0, t_saut_s=None, graine=0):
    """Simule l'écart de temps x_i(t) (secondes) de n horloges par rapport à un temps idéal.

    bruit_blanc_1s : écart-type d'Allan à 1 s du bruit blanc de fréquence (σ_y(τ) = bruit/√τ) ; scalaire ou liste.
    ecart_frequence, derive_par_s : écart de fréquence initial et dérive de fréquence de chaque horloge.
    aberrante, saut_frequence, t_saut_s : l'horloge `aberrante` subit un saut de fréquence à l'instant t_saut_s.
    Renvoie (t, x) avec x de forme (n, m)."""
    rng = np.random.default_rng(graine)
    m = int(round(duree_s / pas_s)) + 1
    t = np.arange(m) * pas_s
    bruit = np.broadcast_to(np.asarray(bruit_blanc_1s, float), (n,))
    y0 = np.zeros(n) if ecart_frequence is None else np.asarray(ecart_frequence, float)
    d = np.zeros(n) if derive_par_s is None else np.asarray(derive_par_s, float)
    x = np.zeros((n, m))
    for i in range(n):
        # fréquence moyenne sur chaque pas : bruit blanc d'écart-type bruit/√pas
        y = rng.normal(0.0, bruit[i] / np.sqrt(pas_s), m - 1) + y0[i] + d[i] * t[:-1]
        if aberrante == i and saut_frequence:
            ts = duree_s / 2 if t_saut_s is None else t_saut_s
            y = y + np.where(t[:-1] >= ts, saut_frequence, 0.0)
        x[i, 1:] = np.cumsum(y) * pas_s
    return t, x


def ecarts_deux_a_deux(x):
    """Les n(n−1)/2 écarts mesurables x_i − x_j (c'est tout ce qu'un comparateur de phase fournit)."""
    n = x.shape[0]
    return {(i, j): x[i] - x[j] for i in range(n) for j in range(i + 1, n)}


def _pente(t, v):
    tc = t - t.mean()
    return float((tc * (v - v.mean())).sum() / (tc**2).sum())


def _pente_et_incertitude(t, v):
    """Pente de v(t) et son écart-type, estimé sur les données (bruit blanc de fréquence supposé)."""
    pas, duree = float(t[1] - t[0]), float(t[-1] - t[0])
    acc = np.diff(v) / pas                                             # fréquences moyennes sur un pas
    sigma0 = 1.4826 * float(np.median(np.abs(acc - np.median(acc))))   # écart-type robuste (insensible à un saut)
    return _pente(t, v), np.sqrt(6.0 / 5.0) * sigma0 * np.sqrt(pas / duree)


def scores_aberration(t, ecarts, n, fenetre_s=None, etalonnage_s=None):
    """Pour chaque horloge, médiane des écarts de fréquence NORMALISÉS avec chacune des autres (fenêtre finale).

    Pour chaque paire, l'écart de fréquence est la pente de x_i − x_j sur la fenêtre ; son incertitude est
    estimée sur les données elles-mêmes (dispersion robuste des accroissements, hypothèse de bruit blanc de
    fréquence : écart-type de la pente = √(6/5)·σ_y(τ₀)·√(τ₀/T)). Le rapport z = |pente| / incertitude dit de
    combien d'écarts-types la paire diverge.
    Si `etalonnage_s` est donné, on retranche à chaque pente celle mesurée pendant les `etalonnage_s` premières
    secondes : on détecte alors un CHANGEMENT de fréquence, et non l'écart de fréquence permanent que toute paire
    d'horloges réelles présente.
    Une horloge aberrante a ses TROIS rapports grands (médiane grande) ; une horloge saine n'en a qu'un, celui
    avec l'aberrante (médiane petite). Renvoie (scores z par horloge, écarts de fréquence par paire)."""
    sel = slice(None) if fenetre_s is None else (t >= t[-1] - fenetre_s)
    cal = None if etalonnage_s is None else (t <= t[0] + etalonnage_s)
    pentes, z = {}, {}
    for paire, v in ecarts.items():
        p, sp = _pente_et_incertitude(t[sel], v[sel])
        if cal is not None:
            p0, sp0 = _pente_et_incertitude(t[cal], v[cal])
            p, sp = p - p0, float(np.hypot(sp, sp0))
        pentes[paire] = p
        z[paire] = abs(p) / sp if sp > 0 else np.inf
    scores = np.array([float(np.median([zz for (a, b), zz in z.items() if i in (a, b)])) for i in range(n)])
    return scores, pentes


def detecter_aberrante(t, x, fenetre_s=3600.0, seuil=5.0, etalonnage_s=None):
    """Indice de l'horloge aberrante, ou None. Ne se sert que des écarts deux à deux.

    Règle : l'horloge de score maximal est déclarée aberrante si ce score (en écarts-types) dépasse `seuil`.
    Avec du matériel réel, donner `etalonnage_s` (période initiale réputée saine) pour ne pas confondre un écart
    de fréquence permanent avec une panne. Le seuil de 5 donne un taux de fausse alarme négligeable pour du bruit
    blanc de fréquence ; en présence de scintillation ou de dérive, l'étalonner sur une période saine.
    Renvoie (indice ou None, scores)."""
    n = x.shape[0]
    if n < 3:
        raise ValueError("il faut au moins trois horloges pour identifier la fautive")
    scores, _ = scores_aberration(t, ecarts_deux_a_deux(x), n, fenetre_s, etalonnage_s)
    k = int(np.argmax(scores))
    if scores[k] > seuil:
        return k, scores
    return None, scores


def echelle_ensemble(x, exclues=()):
    """Temps d'ensemble : moyenne des horloges non exclues (en simulation, on peut le comparer au temps idéal)."""
    garde = [i for i in range(x.shape[0]) if i not in set(exclues)]
    if not garde:
        raise ValueError("toutes les horloges sont exclues")
    return x[garde].mean(axis=0)


def ecart_type_allan(x, pas_s, m=1):
    """Écart-type d'Allan (estimateur à recouvrement) d'une série d'écarts de temps x, pour τ = m·pas."""
    x = np.asarray(x, float)
    if len(x) < 2 * m + 2:
        raise ValueError("série trop courte")
    d2 = x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]
    tau = m * pas_s
    return float(np.sqrt((d2**2).mean() / (2 * tau**2)))


def _demo():
    np.set_printoptions(precision=2, suppress=False)
    t, x = simuler_horloges(aberrante=2, saut_frequence=2e-10, graine=1)
    k, scores = detecter_aberrante(t, x)
    print("Quatre horloges simulées (bruit blanc 3e-10 à 1 s), saut de fréquence de 2e-10 sur l'horloge n° 3 à mi-parcours")
    print("  scores (écart de fréquence médian, en écarts-types, dernière heure) :", " ".join(f"{s:.1f}" for s in scores))
    print("  horloge déclarée aberrante : n°", None if k is None else k + 1)
    fin = slice(-360, None)
    e_tout = np.ptp(echelle_ensemble(x)[fin])
    e_sans = np.ptp(echelle_ensemble(x, exclues=[] if k is None else [k])[fin])
    print(f"  excursion du temps d'ensemble sur la dernière heure : {e_tout * 1e9:.0f} ns avec les quatre, {e_sans * 1e9:.0f} ns après exclusion")
    t, x = simuler_horloges(graine=1)
    print("  sans horloge aberrante → détection :", detecter_aberrante(t, x)[0])
    print(f"  écart-type d'Allan simulé à 100 s : {ecart_type_allan(x[0], 10.0, 10):.2e} (attendu 3e-10/√100 = 3,0e-11)")
    print("Rappel : le décalage relativiste d'un trajet terrestre (≈ 1e-13) est invisible à ce niveau de bruit.")


if __name__ == "__main__":
    _demo()
