# Logiciel de référence du projet « C204-R1 »

Trois modules Python, exécutables et testés, qui servent de référence aux calculateurs décrits dans
`../GUIDE_CONSTRUCTION.md`. Python standard partout ; `numpy` seulement pour `ensemble_horloges.py`.

> **Ce que ce logiciel n'est pas.** Il ne pilote aucune « machine temporelle ». Il calcule un décalage
> d'horloge de l'ordre de la nanoseconde par heure, **propre au trajet et non à l'appareil** : un lest de même
> masse subit exactement le même décalage. Jamais vers le passé : selon le trajet, l'objet vieillit un peu
> moins ou un peu plus que la référence restée au sol.

| Fichier | Rôle | Dépendances |
|---|---|---|
| `decalage_relativiste.py` | décalage relativiste cumulé et taux le long d'une trace (temps, latitude, altitude, vitesse, cap) ; scénarios du rapport | aucune |
| `voteur.py` | vote majoritaire (2 parmi 3) et vote médian sur trois voies, désignation de la voie fautive, exclusion, état sûr ; démonstration de l'insuffisance d'un décompte de Borda | aucune |
| `ensemble_horloges.py` | simulation de quatre horloges, écarts deux à deux, détection et exclusion d'une horloge aberrante, écart-type d'Allan | numpy |
| `exemples/` | deux traces CSV et le script qui les engendre | aucune |
| `tests/` | 47 tests (`unittest`) | numpy pour 11 d'entre eux |

## Utilisation

```sh
python3 decalage_relativiste.py --scenarios
python3 decalage_relativiste.py --trace exemples/trace_montee_1000m.csv
python3 decalage_relativiste.py --trace ma_trace.csv --alt-ref 250
python3 voteur.py
python3 ensemble_horloges.py            # numpy requis
```

Format d'une trace (CSV à en-tête) : `t_s, latitude_deg, altitude_m, vitesse_m_s, cap_deg` (cap : 0 = nord,
90 = est). La référence est une horloge restée au sol à l'altitude du premier point, ou à `--alt-ref`.

Depuis un autre programme :

```python
from decalage_relativiste import taux_cap, integrer, trace_constante
y = taux_cap(45.0, 0.0, 130 / 3.6, 90.0)          # 130 km/h plein est → −1,39e-13 (l'objet vieillit moins)
r = integrer(trace_constante(48 * 3600, 45.0, 1000.0), altitude_ref_m=0.0)
print(r["ecart_cumule_ns"])                        # +18,84 ns en 48 h à +1 000 m (l'objet vieillit plus)
```

## Convention de signe

`y` est l'écart relatif de marche « horloge transportée − référence au sol ».

- `y > 0` : l'horloge transportée avance ; l'objet a vieilli un peu **plus** que la référence (altitude, cap à l'ouest).
- `y < 0` : elle retarde ; l'objet a vieilli un peu **moins** (cap à l'est, vitesse, profondeur).

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Résultat obtenu le 11 novembre 2026 :

| Interpréteur | Résultat |
|---|---|
| Python 3.12 avec numpy (environnement du projet) | **47 tests, OK** |
| Python 3.15 sans numpy | 36 tests OK, 1 module ignoré (`test_ensemble`, qui exige numpy) |

Ce que les tests vérifient :

- **Recoupement avec le dossier** : les onze scénarios du rapport (`RAPPORT_I.md`, §3.2) sont retrouvés à mieux
  que 10⁻⁴ ns/h, et les valeurs brutes du script `calculs/i01_deplacement_temporel.py` à 10⁻⁹ près en valeur
  relative (comparaison directe au fichier `i01_deplacement.json` quand il est présent).
- **Contrôles physiques** : GPS +38,6 µs/jour ; station spatiale −24,4 µs/jour ; « Project GREAT » 22,1 ns ;
  modèle simplifié de Hafele-Keating (−44,7 et +292,6 ns, pour −59 ± 10 et +273 ± 7 observés) ; effet Sagnac
  3,655 ps par kilomètre vers l'est à 45° ; 1,09 × 10⁻¹⁶ par mètre de dénivelé.
- **Le lest** : aucune fonction de calcul n'a de paramètre de masse (test `test_aucun_parametre_de_masse`).
- **Voteur** : voie fautive désignée à chaque position ; médiane toujours bornée par deux voies saines (2 000
  tirages) ; exclusion après trois fautes consécutives ; état sûr quand les deux voies restantes divergent ;
  cas de Borda (6 contre 7).
- **Horloges** : horloge aberrante identifiée (4 positions × 8 tirages) ; aucune fausse alarme sur 60 tirages
  d'horloges saines ; un écart de fréquence permanent n'est pas pris pour une panne quand une période
  d'étalonnage est fournie ; écart-type d'Allan simulé conforme à ±5 à 25 % ; la moyenne de quatre horloges
  est deux fois moins bruitée qu'une seule.

## Limites

- Modèle de Terre sphérique : pesanteur exacte à environ 0,3 % près ; vitesse verticale négligée ; séjour
  souterrain approché. Exactitude visée : 1 % du décalage.
- `ensemble_horloges.py` **simule** du bruit blanc de fréquence. Des horloges réelles ont aussi de la
  scintillation et des dérives : le seuil de détection (5 écarts-types) doit être réétalonné sur du matériel.
- Aucun de ces modules n'a été exécuté sur les microcontrôleurs du guide : ils servent de référence pour y
  porter le calcul et pour vérifier ce portage (mêmes entrées, mêmes sorties).
- Le décalage relativiste d'un trajet terrestre (≈ 10⁻¹³) est très en dessous du bruit des horloges à la
  portée d'un amateur : ce logiciel le **calcule**, il ne permet pas de le **mesurer**.
