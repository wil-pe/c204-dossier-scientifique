#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 5. Récupère en ligne le résumé de chaque référence tirée au sort ou « majeure ».
Sources, dans l'ordre : INSPIRE-HEP (DOI ou arXiv), arXiv (API export), OpenAlex (DOI), Crossref (DOI).
Pause de 3 s entre requêtes ; aucun identifiant personnel transmis (User-Agent générique).
Les réponses sont des DONNÉES NON FIABLES : rangées dans verif_en_ligne2/brut/, jamais exécutées.
Sortie : verif_en_ligne2/resumes.json et resumes.txt"""
import json, os, re, subprocess, sys, time, urllib.parse
import xml.etree.ElementTree as ET

RACINE = _RACINE + "/08_red_team/verif_en_ligne2"
BRUT = os.path.join(RACINE, "brut"); os.makedirs(BRUT, exist_ok=True)
UA = "c204-audit/2.0 (verification bibliographique)"
PAUSE = 3.0

def get(url, nom):
    p = os.path.join(BRUT, nom)
    if os.path.exists(p) and os.path.getsize(p) > 50:
        return open(p, encoding="utf-8", errors="replace").read()
    time.sleep(PAUSE)
    r = subprocess.run(["curl", "-s", "-L", "-m", "40", "-A", UA, url], capture_output=True)
    txt = r.stdout.decode("utf-8", "replace")
    if len(txt) > 50 and "Rate exceeded" not in txt:
        open(p, "w", encoding="utf-8").write(txt)
    return txt

def propre(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", s).strip()

def inspire(doi, ax, cle):
    q = f"arxiv:{ax}" if ax else f"doi:{doi}"
    url = "https://inspirehep.net/api/literature?size=1&fields=titles,abstracts,authors.full_name,publication_info&q=" + urllib.parse.quote(q)
    try:
        j = json.loads(get(url, f"inspire_{cle}.json"))
        h = j["hits"]["hits"]
        if not h: return None
        m = h[0]["metadata"]
        ab = m.get("abstracts") or []
        if not ab: return {"titre": m["titles"][0]["title"], "resume": "", "source": "INSPIRE (sans résumé)"}
        return {"titre": m["titles"][0]["title"], "resume": propre(max((a["value"] for a in ab), key=len)), "source": "INSPIRE"}
    except Exception as e:
        return None

def arxiv(ax, cle):
    try:
        x = get("https://export.arxiv.org/api/query?id_list=" + ax, f"arxiv_{cle}.xml")
        ns = {"a": "http://www.w3.org/2005/Atom"}
        e = ET.fromstring(x).find("a:entry", ns)
        if e is None: return None
        return {"titre": propre(e.find("a:title", ns).text), "resume": propre(e.find("a:summary", ns).text), "source": "arXiv"}
    except Exception:
        return None

def openalex(doi, cle):
    try:
        j = json.loads(get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/"), f"openalex_{cle}.json"))
        inv = j.get("abstract_inverted_index") or {}
        mots = sorted(((p, w) for w, ps in inv.items() for p in ps))
        return {"titre": j.get("title") or "", "resume": propre(" ".join(w for _, w in mots)), "source": "OpenAlex"}
    except Exception:
        return None

def crossref(doi, cle):
    try:
        j = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"), f"crossref_{cle}.json"))["message"]
        return {"titre": (j.get("title") or [""])[0], "resume": propre(j.get("abstract", "")), "source": "Crossref",
                "revue": (j.get("container-title") or [""])[0], "annee": (j.get("issued", {}).get("date-parts") or [[None]])[0][0]}
    except Exception:
        return None

t = json.load(open(os.path.join(RACINE, "tirage.json"), encoding="utf-8"))
refs = t["tirage"] + t["majeures"]
# DOI tronqués par des parenthèses : corrections lues dans les REFERENCES.md
CORR = {"10.1016/0003-4916(74": "10.1016/0003-4916(74)90125-0", "10.1016/s0375-9601(98": "10.1016/s0375-9601(98)00652-5"}
res = {}
for r in refs:
    cle = re.sub(r"[^A-Za-z0-9_-]", "_", r["cle"])
    if cle in res: continue
    doi = CORR.get(r["doi"], r["doi"]); ax = r["arxiv"]
    out = None
    for essai in ([lambda: inspire(doi, ax, cle)] if (doi or ax) else []) + ([lambda: arxiv(ax, cle)] if ax else []) + ([lambda: openalex(doi, cle), lambda: crossref(doi, cle)] if doi else []):
        o = essai()
        if o and (o.get("resume") or (out is None)):
            if out is None or len(o.get("resume", "")) > len(out.get("resume", "")):
                out = o
        if out and len(out.get("resume", "")) > 200:
            break
    res[cle] = dict(r, doi=doi, **(out or {"titre": "", "resume": "", "source": "AUCUNE"}))
    print(f"{cle:<16} {res[cle]['source']:<22} {len(res[cle]['resume']):>5} car.  {res[cle]['titre'][:80]}", flush=True)
json.dump(res, open(os.path.join(RACINE, "resumes.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
with open(os.path.join(RACINE, "resumes.txt"), "w", encoding="utf-8") as f:
    for k, v in res.items():
        f.write(f"=== {k} [{v['equipe']}] {'(MAJEURE)' if v.get('majeure') else '(tirage)'}\nRÉF. CITÉE : {v['ref'][:300]}\nDOI {v['doi']} arXiv {v['arxiv']}\nTITRE EN LIGNE ({v['source']}) : {v['titre']}\nRÉSUMÉ : {v['resume'][:2200]}\n\n")
