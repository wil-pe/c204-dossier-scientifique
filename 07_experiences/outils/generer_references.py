#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe F — génère REFERENCES.md à partir du journal de vérification Crossref
(verification_refs/crossref_resultats.json) et d'une liste manuelle de sources hors Crossref.

Une référence est marquée « vérifiée (Crossref) » si l'API a renvoyé une notice dont le premier
auteur et l'année correspondent à ce qui était attendu ; les champs bibliographiques imprimés
sont ceux de Crossref (pas ceux de notre mémoire).

Usage : python -I generer_references.py
"""
import json
import os
import re
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.join(ICI, "..")

GROUPES = [
    ("EXP-01 — Dilatation du temps, horloges", [
        "PoundRebka1960", "HafeleKeating1972a", "HafeleKeating1972b", "Briatore1977", "Vessot1980", "VanBaak2007",
        "Chou2010", "Grotti2018", "McGrew2018", "Delva2018", "Herrmann2018", "Takamoto2020", "Bothwell2022",
        "Zheng2022", "Allan1966", "Knappe2004", "Lutwak2009"]),
    ("EXP-02 — Transfert de temps", [
        "AllanWeiss1980", "Mills1991", "Levine2002", "Ashby2003", "Lipinski2011", "OPERA2012doi", "Novick2015",
        "Lisdat2016"]),
    ("EXP-03 — Mesure de G et test nul électromagnétique", [
        "Cavendish1798", "Tolman1931", "Gundlach2000", "Hathaway2003", "Tajmar2004", "Kapner2007",
        "Schlamminger2008", "Adelberger2009", "Quinn2013", "Rosi2014", "Fuzfa2016", "Rothleitner2017", "Li2018",
        "Lee2020", "Westphal2021", "CODATA2018", "CODATA2022"]),
    ("EXP-04 — Gravimétrie", [
        "Niebauer1995", "Peters1999", "Goodkind1999", "Jekeli2006", "Middlemiss2016", "Menoret2018", "Staacks2018",
        "Stray2022"]),
    ("EXP-05 — Effet Casimir et énergie négative", [
        "Lamoreaux1997", "MohideenRoy1998", "Larraza1998", "Chan2001", "Bressi2002", "Lamoreaux2005", "Jaffe2005",
        "Decca2007", "Munday2009", "Denardo2009", "Klimchitskaya2009", "Sushkov2011", "Wilson2011", "Garrett2018",
        "MTY1988", "FordRoman1995", "FordRoman1996", "Tipler1974", "Tipler1977", "Hawking1992"]),
    ("EXP-06 — Gravité analogue", [
        "Watson1964", "Unruh1981", "Bohr1993", "SchutzholdUnruh2002", "Visser2002", "BushAristoff2003",
        "Volovik2005", "Rousseaux2008", "Philbin2008", "Belgiorno2010", "Weinfurtner2011", "Jannes2011",
        "Barcelo2011", "Euve2016", "Steinhauer2016", "Torres2017", "Bhagat2018", "Duchesne2019", "Drori2019",
        "MunozdeNova2019", "Torres2020", "Cromb2020", "Euve2020", "Kolobov2021", "Svancara2024"]),
    ("EXP-07 — Pièges et lévitation", [
        "Wuerker1959", "Gibbons1975", "Paul1990", "WinterOrtjohann1991", "Rueckner1995", "BerryGeim1997",
        "Simon1997", "SimonGeim2000", "Thompson2002", "Vinitsky2015", "LibbrechtBlack2018"]),
    ("EXP-08 — Déviation de la lumière", ["Dyson1920", "Ambrosini1997", "Bertotti2003", "Shapiro2004"]),
    ("EXP-09 — Sagnac et Lense-Thirring", [
        "Sagnac1913", "MichelsonGale1925", "Post1967", "ValiShorthill1976", "Mashhoon1984", "CiufoliniPavlis2004",
        "Everitt2011", "Bosi2011", "Schreiber2011", "SchreiberWells2013", "Lefevre2014", "Ciufolini2016",
        "VenkatramanKrishnan2020"]),
    ("EXP-10 — Optique quantique et causalité", [
        "ScullyDruhl1982", "Greenberger1983", "Deutsch1991", "Kim2000", "Walborn2002", "Peres2004", "Jacques2007",
        "HillmerKwiat2007", "Brun2009", "Lloyd2011", "Oreshkov2012", "Chiribella2013", "Ma2013", "Ringbauer2014",
        "Procopio2015", "Ma2016", "Rubino2017", "Goswami2018"]),
    ("EXP-11 — Rayonnement", ["Hawking1974", "Hawking1975", "Page1976", "MacGibbonWebber1990"]),
    ("EXP-12 — Banc d'essai, redondance, analyse en aveugle", [
        "LyonsVanderkulk1962", "Pease1980", "Lamport1982", "KleinRoodman2005", "MacCounPerlmutter2015"]),
]

NOTES = {  # précisions sur ce qui a été relu au-delà de la notice
    "VanBaak2007": "Lettre décrivant « Project GREAT » ; chiffres (5400 ft, 2 jours, ≈ 22 ns prédits, ≈ 23 ns observés) relus sur la page du projet.",
    "Bothwell2022": "Résumé relu (arXiv:2109.12238) : incertitude 7,6e-21.",
    "Torres2017": "Résumé arXiv:1612.06180 relu : 3,70 Hz, 6,25 cm d'eau, amplification maximale 20 % (prépublication).",
    "Jannes2011": "Résumé arXiv:1010.1701 relu : horizon de trou blanc démontré par l'angle du cône de Mach.",
    "Weinfurtner2011": "Résumé arXiv:1008.1911 relu.",
    "MunozdeNova2019": "Résumé arXiv:1809.00913 relu.",
    "Sagnac1913": "Notice trouvée : article de 1914 au Journal de Physique ; les notes aux Comptes Rendus de 1913 figurent plus bas (hors Crossref).",
    "OPERA2012doi": "Résultat corrigé, compatible avec c.",
    "Bhagat2018": "Mécanisme contesté par Duchesne et al. 2019 (ci-dessous).",
    "Ciufolini2016": "Budget d'incertitude discuté dans la littérature (commentaire et réponse publiés dans la même revue).",
    "Lisdat2016": "Lecture complémentaire, non citée dans les fiches.",
    "Kapner2007": "Lecture complémentaire, non citée dans les fiches.",
    "Adelberger2009": "Lecture complémentaire, non citée dans les fiches.",
    "Visser2002": "Lecture complémentaire, non citée dans les fiches.",
    "Euve2020": "Lecture complémentaire, non citée dans les fiches.",
    "Simon1997": "Lecture complémentaire, non citée dans les fiches.",
    "Greenberger1983": "Lecture complémentaire, non citée dans les fiches.",
    "Peres2004": "Lecture complémentaire (non-signalisation et relativité), non citée dans les fiches.",
    "Brun2009": "Lecture complémentaire, non citée dans les fiches.",
    "CODATA2022": "Lecture complémentaire ; les scripts utilisent les valeurs CODATA 2018.",
    "Tipler1974": "Contexte théorique (Équipe B) ; cité pour situer la question de l'énergie exotique.",
    "Tipler1977": "Contexte théorique (Équipe B).",
    "Hawking1992": "Contexte théorique (Équipe B).",
    "Gibbons1975": "Contexte théorique (Équipe B).",
}

HORS_CROSSREF = """
## Sources hors Crossref

| Source | Usage | Statut de vérification |
|---|---|---|
| T. Van Baak, « Project GREAT: General Relativity Einstein/Essen Anniversary Test », page web leapsecond.com/great2005/ (créée le 24/09/2005) | EXP-01 | **relue en ligne le 10/11/2026** (HTTP ; le site refuse HTTPS) |
| J. H. Hubbell & S. M. Seltzer, *Tables of X-Ray Mass Attenuation Coefficients and Mass Energy-Absorption Coefficients*, NIST Standard Reference Database 126 (NISTIR 5632), physics.nist.gov/PhysRefData/XrayMassCoef/ | EXP-11 | **relue en ligne le 10/11/2026** (eau, air, plomb à 0,1 ; 1 ; 10 ; 15 ; 20 MeV) |
| Résumés arXiv 1612.06180, 1010.1701, 2109.12238, 1008.1911, 1809.00913 (API export.arxiv.org) | EXP-01, EXP-06 | **relus en ligne le 10/11/2026** |
| H. B. G. Casimir, « On the attraction between two perfectly conducting plates », *Proc. K. Ned. Akad. Wet.* **51**, 793 (1948) | EXP-05 | non vérifiée en ligne (référence classique absente de Crossref) |
| G. Sagnac, notes aux *Comptes Rendus de l'Académie des Sciences* **157**, 708 et 1410 (1913) | EXP-09 | non vérifiée en ligne (l'article de 1914 au *Journal de Physique* l'est, voir plus haut) |
| J. Lense & H. Thirring, *Physikalische Zeitschrift* **19**, 156 (1918) | EXP-09 | non vérifiée en ligne directement ; traduction commentée vérifiée (Mashhoon, Hehl & Theiss 1984) |
| S. Earnshaw, « On the nature of the molecular forces which regulate the constitution of the luminiferous ether », *Trans. Camb. Phil. Soc.* **7**, 97 (1842) | EXP-07 | non vérifiée en ligne |
| W. J. Riley, *Handbook of Frequency Stability Analysis*, NIST Special Publication 1065 (2008) | EXP-01 | non vérifiée en ligne |
| IEEE Std 1588 (Precision Time Protocol) ; RFC 5905 (Network Time Protocol version 4) | EXP-02 | non vérifiées en ligne (normes) |
| Norme CEI/IEC 61010-1 (sécurité des appareils de mesure et de laboratoire) : limites de courant, charge et énergie accessibles | EXP-03, EXP-07 | non vérifiée en ligne — **valeurs à relire dans l'édition en vigueur avant tout montage** |
| UNSCEAR, rapport 2008 (sources et effets des rayonnements ionisants) ; CIPR, Publication 103 (2007) | EXP-11 | non vérifiées en ligne |

## Affirmations données sans référence vérifiée (à traiter comme [HYP] ou à sourcer)

- Performances chiffrées des horloges commerciales (rubidium, césium à jet, CSAC, maser), coefficients d'environnement
  d'un rubidium : valeurs de type « fiche technique », de mémoire.
- Performances typiques des méthodes de transfert de temps ; sensibilité d'un tube Geiger (≈ 175 coups/min par µSv/h) ;
  bruit des accéléromètres et gyromètres MEMS ; résolution des gravimètres commerciaux.
- Énergie stockée dans les grands aimants (IRM, 45 T, LHC, ITER).
- Précision de la navigation par corrélation de cartes de gravité (« centaine de mètres au kilomètre »).
- Domaines de distance et précisions des expériences de Casimir ; valeur « 14 ± 8 % » de la version publiée de Torres et al. 2017.
- Susceptibilités magnétiques et coefficient de diffusion du saccharose : valeurs usuelles de tables, non revérifiées.
- Valeurs reprises du programme après validation contradictoire, non re-dérivées par l'Équipe F : fraction photons du
  rayonnement de Hawking (7,5 %) et énergie des photons (12–16 MeV) ; charge tenable d'un micro-trou noir (≈ 6 e,
  borne 137 e) ; masse 3,9–5,1e12 kg par singularité ; dimensions révisées du coffre (L = 0,85 m). Sources : dossier
  de base v1.2 (errata E2, E12, E14), Équipes B, C, A, Red Team n° 2. Le débit de dose et l'entraînement orbital qui
  en découlent ont, eux, été recalculés par nos scripts.
- Angle (≈ 55°) et rayon de courbure (~10 cm) lus sur la photographie C204-DOC-012 : lecture visuelle, confiance faible.
"""


def sans_accents(t):
    return "".join(ch for ch in unicodedata.normalize("NFD", t or "") if unicodedata.category(ch) != "Mn").lower()


def nettoie(titre):
    t = re.sub(r"<[^>]+>", " ", titre or "")
    t = t.replace("&amp;", "&")
    if re.search(r"[\u0400-\u04FF]", t):          # notice bilingue : on garde la partie en caractères latins
        t = t.split(";")[0]
    return " ".join(t.split())


AFFICHAGE_AUTEUR = {"VanBaak2007": "Van Baak", "Cavendish1798": "Cavendish", "OPERA2012doi": "Collaboration OPERA",
                    "VenkatramanKrishnan2020": "Venkatraman Krishnan"}


def choisir(entree):
    att, an = sans_accents(entree["auteur_attendu"]), entree["annee_attendue"]
    # on préfère les notices d'articles de revue (volume et titre de revue renseignés) aux résumés de conférence
    cands = sorted(entree.get("resultats") or [], key=lambda r: (not r.get("volume"), not r.get("revue")))
    for r in cands:
        a = sans_accents(r.get("premier_auteur"))
        if a and (att in a or a in att) and r.get("annee") and abs(int(r["annee"]) - an) <= 1:
            return r, True
    for r in cands:        # auteur absent ou collectif dans la notice (collaboration, article ancien)
        if r.get("annee") and int(r["annee"]) == an and (entree.get("doi_demande") or not r.get("premier_auteur")) \
                and r.get("revue"):
            return r, True
    return None, False


def main():
    with open(os.path.join(RACINE, "verification_refs", "crossref_resultats.json"), encoding="utf-8") as f:
        base = {t["cle"]: t for t in json.load(f)}
    L = ["# Équipe F — Références et statut de vérification", "",
         "Généré par `outils/generer_references.py` à partir du journal `verification_refs/crossref_resultats.json`",
         "(interrogation de l'API publique Crossref le 10 novembre 2026, script `outils/verif_references_crossref.py`).", "",
         "**Règle appliquée** : aucune référence inventée. « Vérifiée (Crossref) » signifie que la notice renvoyée par",
         "Crossref correspond à l'auteur et à l'année attendus ; les champs ci-dessous (revue, volume, pages, titre, DOI)",
         "sont ceux de Crossref. Cela atteste l'**existence et l'identité** de l'article, pas l'exactitude de chaque",
         "chiffre que nous en citons : lorsque nous avons relu un résumé ou une page, c'est indiqué en note ; sinon les",
         "valeurs numériques tirées des articles sont citées de mémoire et signalées comme telles dans les fiches.", ""]
    n_ok = n_tot = 0
    non_verifiees = []
    for titre, cles in GROUPES:
        L += [f"## {titre}", "", "| Référence (notice Crossref) | Statut | Note |", "|---|---|---|"]
        for cle in cles:
            n_tot += 1
            e = base.get(cle)
            r, ok = choisir(e) if e else (None, False)
            if ok:
                n_ok += 1
                nb = r.get("nb_auteurs") or 0
                aut = AFFICHAGE_AUTEUR.get(cle) or r.get("premier_auteur") or "(auteur non renseigné dans la notice)"
                if aut.isupper():
                    aut = aut.title()
                suite = " et al." if nb > 2 else (" et un coauteur" if nb == 2 else "")
                if cle == "OPERA2012doi":
                    suite = ""
                vol = f" **{r['volume']}**" if r.get("volume") else ""
                pages = f", {r['page']}" if r.get("page") else ""
                ref = (f"{aut}{suite} ({r.get('annee')}). {nettoie(r.get('titre'))}. *{nettoie(r.get('revue'))}*"
                       f"{vol}{pages}. doi:{r.get('doi')}")
                L.append(f"| {ref} | vérifiée (Crossref) | {NOTES.get(cle, '')} |")
            else:
                non_verifiees.append(cle)
                L.append(f"| {cle} | **non vérifiée** | notice non retrouvée |")
        L.append("")
    L.append(HORS_CROSSREF.strip())
    L += ["", "## Bilan", "",
          f"- {n_ok} références sur {n_tot} vérifiées par Crossref ; non retrouvées : {', '.join(non_verifiees) or 'aucune'}.",
          "- 3 sources web relues directement (page Project GREAT, tables NIST, 5 résumés arXiv).",
          "- 8 sources classiques, normatives ou institutionnelles citées sans vérification en ligne, signalées comme telles.", ""]
    with open(os.path.join(RACINE, "REFERENCES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"{n_ok}/{n_tot} vérifiées ; non vérifiées : {non_verifiees}")


if __name__ == "__main__":
    main()
