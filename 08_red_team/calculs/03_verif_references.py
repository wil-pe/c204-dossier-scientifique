#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G — vérification en ligne (API Crossref) des références citées dans le rapport red team.
Aucune donnée personnelle n'est transmise : seule la requête DOI est envoyée, avec un User-Agent générique.
Résultat : ../verif_en_ligne/references_crossref.json  (données téléchargées = non fiables, lues comme du texte).
"""
import json, urllib.request, urllib.parse, time

DOIS = {
 "Kerr 1963 (PRL 11, 237)": "10.1103/PhysRevLett.11.237",
 "Tipler 1974 (PRD 9, 2203)": "10.1103/PhysRevD.9.2203",
 "Tipler 1976 (PRL 37, 879)": "10.1103/PhysRevLett.37.879",
 "Carter 1968 (Phys. Rev. 174, 1559)": "10.1103/PhysRev.174.1559",
 "Hawking 1971 (MNRAS 152, 75)": "10.1093/mnras/152.1.75",
 "Hawking 1974 (Nature 248, 30)": "10.1038/248030a0",
 "Hawking 1975 (CMP 43, 199)": "10.1007/BF02345020",
 "Hawking 1992 (PRD 46, 603)": "10.1103/PhysRevD.46.603",
 "Page 1976 (PRD 13, 198)": "10.1103/PhysRevD.13.198",
 "MacGibbon & Webber 1990 (PRD 41, 3052)": "10.1103/PhysRevD.41.3052",
 "Gibbons 1975 (CMP 44, 245)": "10.1007/BF01609829",
 "Poisson & Israel 1990 (PRD 41, 1796)": "10.1103/PhysRevD.41.1796",
 "Hafele & Keating 1972a (Science 177, 166)": "10.1126/science.177.4044.166",
 "Hafele & Keating 1972b (Science 177, 168)": "10.1126/science.177.4044.168",
 "Bailey et al. 1977 (Nature 268, 301)": "10.1038/268301a0",
 "Arkani-Hamed, Dimopoulos, Dvali 1998 (PLB 429, 263)": "10.1016/S0370-2693(98)00466-3",
 "Dimopoulos & Landsberg 2001 (PRL 87, 161602)": "10.1103/PhysRevLett.87.161602",
 "Giddings & Thomas 2002 (PRD 65, 056010)": "10.1103/PhysRevD.65.056010",
 "Busza, Jaffe, Sandweiss, Wilczek 2000 (RMP 72, 1125)": "10.1103/RevModPhys.72.1125",
 "Giddings & Mangano 2008 (PRD 78, 035009)": "10.1103/PhysRevD.78.035009",
 "CMS 2011 (PLB 697, 434)": "10.1016/j.physletb.2011.02.032",
 "Deutsch 1991 (PRD 44, 3197)": "10.1103/PhysRevD.44.3197",
 "Polchinski 1991 (PRL 66, 397)": "10.1103/PhysRevLett.66.397",
 "Majumdar 1947 (Phys. Rev. 72, 390)": "10.1103/PhysRev.72.390",
 "Morris, Thorne, Yurtsever 1988 (PRL 61, 1446)": "10.1103/PhysRevLett.61.1446",
 "Page 1977 (PRD 16, 2402)": "10.1103/PhysRevD.16.2402",
}
out = {}
for lab, doi in DOIS.items():
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "reference-checker/1.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            m = json.loads(r.read().decode("utf-8"))["message"]
        auth = "; ".join((a.get("family", "") + " " + a.get("given", "")).strip() for a in m.get("author", []))[:160]
        year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
        out[lab] = dict(doi=doi, statut="VÉRIFIÉ (Crossref)", titre=(m.get("title") or [""])[0], auteurs=auth,
                        revue=(m.get("container-title") or [""])[0], volume=m.get("volume"), page=m.get("page") or m.get("article-number"), annee=year)
    except Exception as ex:
        out[lab] = dict(doi=doi, statut=f"NON VÉRIFIÉ ({type(ex).__name__}: {ex})")
    r_ = out[lab]
    print(f"{lab:55s} -> {r_['statut']:20s} | {r_.get('annee')} | {r_.get('revue')} {r_.get('volume')} {r_.get('page')} | {r_.get('auteurs','')[:60]} | {r_.get('titre','')[:90]}")
    time.sleep(0.3)
json.dump(out, open(_RACINE + "/08_red_team/verif_en_ligne/references_crossref.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---- seconde passe : nouvelle tentative (avec temporisation) pour les DOI refusés (HTTP 429)
P = _RACINE + "/08_red_team/verif_en_ligne/references_crossref.json"
out = json.load(open(P, encoding="utf-8"))
for lab, doi in DOIS.items():
    if out[lab]["statut"].startswith("VÉRIFIÉ"):
        continue
    for essai in range(4):
        time.sleep(4 + 4*essai)
        try:
            req = urllib.request.Request("https://api.crossref.org/works/" + urllib.parse.quote(doi), headers={"User-Agent": "reference-checker/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                m = json.loads(r.read().decode("utf-8"))["message"]
            auth = "; ".join((a.get("family", "") + " " + a.get("given", "")).strip() for a in m.get("author", []))[:160]
            year = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
            out[lab] = dict(doi=doi, statut="VÉRIFIÉ (Crossref)", titre=(m.get("title") or [""])[0], auteurs=auth,
                            revue=(m.get("container-title") or [""])[0], volume=m.get("volume"), page=m.get("page") or m.get("article-number"), annee=year)
            break
        except Exception as ex:
            out[lab] = dict(doi=doi, statut=f"NON VÉRIFIÉ ({type(ex).__name__}: {ex})")
    r_ = out[lab]
    print(f"[2e passe] {lab:45s} -> {r_['statut']:20s} | {r_.get('annee')} | {r_.get('revue')} {r_.get('volume')} {r_.get('page')} | {r_.get('auteurs','')[:50]} | {r_.get('titre','')[:90]}")
json.dump(out, open(P, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
