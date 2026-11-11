# Programme C204 — Errata du rapport n° 1 de la Red Team

Établi par la direction le 10 novembre 2026 d'après l'auto-correction de la Red Team (second passage,
`CORRECTIONS_A_APPLIQUER.md`, section 8). Le fichier `RAPPORT_RED_TEAM_1.md` est conservé tel que rendu, parce qu'il
constitue le rapport *indépendant* du premier passage ; **les valeurs ci-dessous prévalent**. Aucune de ces
corrections ne modifie une objection ni son classement (fatale / sévère / mineure).

| Lieu dans le rapport n° 1 | Texte d'origine | Valeur corrigée | Raison |
|---|---|---|---|
| l. 68 (objection F1) | « un trou noir de 100 kg vit 8×10⁻¹¹ s » | **≈ 4×10⁻¹³ s** | Aux petites masses, toutes les espèces du Modèle standard sont émises : le facteur par rapport à « photons seuls » est ≈ 212, et non 21 |
| l. 293 (§5, D3) | « 100 kg : 4×10⁻¹² s » | **≈ 4×10⁻¹³ s** | Même raison ; Équipes B et C concordantes |
| l. 133 (objection F7) | « Mc² pour 2×10¹² kg : 1,8×10²⁹ J » | **7–9×10²⁹ J** (30 à 40 min de luminosité solaire) | La masse retenue était celle de la formule « photons seuls » ; avec 2 × 3,9–5,1×10¹² kg l'énergie est plus élevée |
| l. 113 (objection F5) | « ≥ 36 cm de plomb (2 à 6 t) » | **40–60 cm, 6–15 t** | 36 cm est une borne en faisceau étroit ; le faisceau large demande davantage |
| l. 79 (objection F2) | charge « ≲ 170 e » | borne ≈ 137–170 e ; **valeur typique ≈ 6 e** | Valeur quadratique moyenne de Page (1977) |
| §4.3 et §3 (steelman) | séparation des singularités 0,15–0,30 m | **≈ 0,09–0,10 m** d'après DOC-007 (entraxe ≈ 0,107 à 0,115 L selon la mesure, L = 0,85 m) | La séparation d'origine n'était pas documentaire |
| §2, S7 (e) | mention « not to scale » de DOC-009 : confiance faible | **confiance moyenne à élevée** | Confirmée sur les meilleures copies par l'Équipe A |

Rappel des fourchettes désormais retenues par l'ensemble du programme :

- masse d'une singularité correspondant à 300–500 MW : **3,9–5,1×10¹² kg** (toutes espèces) ;
- énergie de fabrication : **2,6×10²⁸ J** (deux singularités donnant ensemble 2 g à 1 m) à **7–9×10²⁹ J** (deux singularités de 300–500 MW) ;
- débit de dose des photons primaires d'une singularité de 400 MW : **≈ 3,5×10³ Gy/s à 1 m, ≈ 3,8×10² Gy/s à 3 m** (borne basse, sans cascade) ;
- temps de coalescence de deux singularités de 10¹² kg : ≈ 1 à 2×10²³ ans à 0,09–0,10 m, ≈ 2×10²⁵ ans à 0,30 m (l'objection de la coalescence reste retirée).
