#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — vérification en ligne des références NOUVELLES (non présentes chez B, C, F, H).
Interroge Crossref (par DOI ou par requête bibliographique) et arXiv (par identifiant).
Aucune donnée personnelle transmise (agent utilisateur générique). Les réponses brutes sont rangées dans
brut/ : données non fiables, jamais exécutées ; ce script ne fait que les lire comme du JSON / du texte.
Usage : python -I verifier_refs.py
"""
import json, re, subprocess, time, urllib.parse
from pathlib import Path

ICI = Path(__file__).resolve().parent
BRUT = ICI / "brut"
BRUT.mkdir(exist_ok=True)
UA = "ref-checker/1.0 (generic research client)"

# cle, type, identifiant ou requête, premier auteur attendu, année attendue
CIBLES = [
    ("RossiHall41", "doi", "10.1103/PhysRev.59.223", "Rossi", 1941),
    ("FrischSmith63", "doi", "10.1119/1.1969508", "Frisch", 1963),
    ("CosmicWatch18", "arxiv", "1801.03029", "Axani", 2018),
    ("PDG24", "doi", "10.1103/PhysRevD.110.030001", "Navas", 2024),
    ("Bailey77", "doi", "10.1038/268301a0", "Bailey", 1977),
    ("Bennett06", "doi", "10.1103/PhysRevD.73.072003", "Bennett", 2006),
    ("Aguillard23", "doi", "10.1103/PhysRevLett.131.161802", "Aguillard", 2023),
    ("Botermann14", "doi", "10.1103/PhysRevLett.113.120405", "Botermann", 2014),
    ("Koller17", "doi", "10.1103/PhysRevLett.118.073601", "Koller", 2017),
    ("BPT72", "doi", "10.1086/151796", "Bardeen", 1972),
    ("CW09", "arxiv", "0908.1803", "Crane", 2009),
    ("Roslund24", "arxiv", "2308.12457", "Roslund", 2023),
    ("Grotti18", "arxiv", "1705.04089", "Grotti", 2017),
    ("Torres17", "arxiv", "1612.06180", "Torres", 2016),
    ("Svancara24", "arxiv", "2308.10773", "", 2023),
    ("Lloyd11a", "arxiv", "1005.2219", "Lloyd", 2010),
    ("Ringbauer14", "arxiv", "1501.05014", "Ringbauer", 2015),
    ("Procopio15", "arxiv", "1412.4006", "Procopio", 2014),
    ("MM20", "arxiv", "2008.06618", "Maldacena", 2020),
    ("MMP18", "arxiv", "1807.04726", "Maldacena", 2018),
    ("Kugel24", "arxiv", "2405.02389", "", 2024),
    ("VKD03", "arxiv", "gr-qc/0301003", "Visser", 2003),
    ("Janvier22", "arxiv", "2201.03345", "Janvier", 2022),
    ("Templier22", "arxiv", "2209.13209", "Templier", 2022),
    ("ASMY23", "arxiv", "2207.07666", "Arvidsson", 2022),
    ("Huang26", "arxiv", "2501.16335", "Huang", 2025),
    ("Takamoto20", "doi", "10.1038/s41566-020-0619-8", "Takamoto", 2020),
    ("Menoret18", "doi", "10.1038/s41598-018-30608-1", "noret", 2018),
    ("Stray22", "doi", "10.1038/s41586-021-04315-3", "Stray", 2022),
    ("Chou10", "doi", "10.1126/science.1192720", "Chou", 2010),
    ("HK72b", "doi", "10.1126/science.177.4044.168", "Hafele", 1972),
    ("Wu19", "arxiv", "1904.09084", "Wu", 2019),
    ("Bidel20", "arxiv", "1910.06666", "Bidel", 2019),
    ("QCTRL26", "arxiv", "2608.25563", "Everitt", 2026),
    ("Bothwell22", "arxiv", "2109.12238", "Bothwell", 2021),
    ("Lu26", "arxiv", "2512.07346", "Arnold", 2025),
    ("Marshall25", "arxiv", "2504.13071", "Marshall", 2025),
    ("Goswami18", "arxiv", "1803.04302", "Goswami", 2018),
    ("Falque", "arxiv", "2311.01392", "Falque", 2023),
]

def curl(url, dest):
    if dest.exists() and dest.stat().st_size > 200:
        return dest.read_text(encoding="utf-8", errors="replace")
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    txt = r.stdout.decode("utf-8", errors="replace")
    dest.write_text(txt, encoding="utf-8")
    time.sleep(1.0)
    return txt

def crossref(doi):
    txt = curl("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"), BRUT / ("crossref_" + re.sub(r"[^A-Za-z0-9]+", "_", doi) + ".json"))
    try:
        m = json.loads(txt)["message"]
    except Exception:
        return None
    auteurs = "; ".join((a.get("given", "") + " " + a.get("family", a.get("name", ""))).strip() for a in m.get("author", [])[:4])
    if len(m.get("author", [])) > 4:
        auteurs += " et al."
    annee = None
    for k in ("published-print", "published-online", "issued", "published"):
        if k in m and m[k].get("date-parts") and m[k]["date-parts"][0] and m[k]["date-parts"][0][0]:
            annee = m[k]["date-parts"][0][0]; break
    revue = (m.get("container-title") or [""])[0]
    ref = "%s %s, %s" % (revue, m.get("volume", ""), m.get("page", m.get("article-number", "")))
    resume = re.sub(r"<[^>]+>", " ", m.get("abstract", ""))
    return dict(auteurs=auteurs, titre=(m.get("title") or [""])[0], annee=annee, revue=ref.strip(), doi=m.get("DOI", doi), resume=" ".join(resume.split()))

def arxiv(ident):
    txt = curl("http://export.arxiv.org/api/query?id_list=" + ident, BRUT / ("arxiv_" + ident.replace("/", "_") + ".xml"))
    e = re.search(r"<entry>(.*?)</entry>", txt, re.S)
    if not e:
        return None
    e = e.group(1)
    g = lambda tag: (re.search(r"<%s[^>]*>(.*?)</%s>" % (tag, tag), e, re.S) or [None, ""])[1]
    noms = re.findall(r"<name>(.*?)</name>", e)
    auteurs = "; ".join(noms[:4]) + (" et al." if len(noms) > 4 else "")
    doi = g("arxiv:doi"); jr = g("arxiv:journal_ref")
    return dict(auteurs=auteurs, titre=" ".join(g("title").split()), annee=int(g("published")[:4]) if g("published") else None,
                revue=jr or "prépublication arXiv", doi=doi, arxiv=ident, resume=" ".join(g("summary").split()))

def main():
    res = {}
    for cle, typ, ident, auteur, annee in CIBLES:
        d = crossref(ident) if typ == "doi" else arxiv(ident)
        if d is None or not d.get("titre"):
            res[cle] = dict(statut="ÉCHEC (pas de notice)", identifiant=ident); print(cle, "ÉCHEC"); continue
        ok_auteur = (auteur.lower() in d["auteurs"].lower()) if auteur else True
        d["statut"] = "vérifiée" if ok_auteur else "DISCORDANCE auteur"
        d["source"] = "API Crossref (DOI)" if typ == "doi" else "API arXiv (identifiant)"
        d["identifiant"] = ident
        res[cle] = d
        print("%-14s %-18s %s | %s | %s | %s" % (cle, d["statut"], d["auteurs"][:50], d["annee"], d["titre"][:80], d["revue"][:50]))
    (ICI / "resultats_verification.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

if __name__ == "__main__":
    main()
