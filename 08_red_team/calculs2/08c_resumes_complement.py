#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 5 (complément). Références « majeures » des équipes B, C, D, F (hors tirage) :
résumés récupérés par INSPIRE-HEP / OpenAlex / Crossref. Plus : contrôle de la recherche en texte intégral
« Tipler sinusoid » sur INSPIRE (affirmation de l'Équipe H, §3.4). Sortie : verif_en_ligne2/resumes_complement.json"""
import json, os, re, subprocess, time, urllib.parse
V = _RACINE + "/08_red_team/verif_en_ligne2"; BRUT = os.path.join(V, "brut")
UA = "c204-audit/2.0 (verification bibliographique)"
def get(url, nom):
    p = os.path.join(BRUT, nom)
    if os.path.exists(p) and os.path.getsize(p) > 50:
        return open(p, encoding="utf-8", errors="replace").read()
    time.sleep(3.0)
    t = subprocess.run(["curl", "-s", "-L", "-m", "40", "-A", UA, url], capture_output=True).stdout.decode("utf-8", "replace")
    if len(t) > 50: open(p, "w", encoding="utf-8").write(t)
    return t
def propre(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()
REFS = [  # (clé, équipe, DOI, ce que le rapport lui fait dire)
 ("Hahn2019", "B,C", "10.1038/s41586-019-1293-1", "record de champ magnétique continu 45,5 T"),
 ("LeahyUnruh1979", "B", "10.1103/PhysRevD.19.3509", "anisotropie modérée de l'émission de Hawking d'un trou de Kerr, jamais un cône"),
 ("PressTeukolsky1972", "B", "10.1038/238211a0", "superradiance : gains maximaux ~0,3 % (scalaire), 4,4 % (EM), 138 % (gravitationnel)"),
 ("TeukolskyPress1974", "B", "10.1086/153180", "idem (gains de superradiance)"),
 ("ChambersHiscockTaylor1997", "B,H", "10.1103/PhysRevLett.78.3249", "un trou en rotation perd son moment cinétique plus vite que sa masse"),
 ("Andreasson2008", "B", "10.1016/j.jde.2008.05.010", "2GM/(Rc²) ≤ 8/9 pour toute matière vérifiant p_r + 2p_t ≤ ρc²"),
 ("Aeppli2024", "B,H", "10.1103/PhysRevLett.133.023401", "horloge à réseau Sr à 8,1e-19"),
 ("Peters1964", "B,D", "10.1103/PhysRev.136.B1224", "formules de puissance OG et de temps de coalescence"),
 ("PoissonIsrael1990", "B,H,G", "10.1103/PhysRevD.41.1796", "inflation de masse à l'horizon de Cauchy"),
 ("Carr2010", "D,B", "10.1103/PhysRevD.81.104019", "f(M→0) = 15,35 ; τ(1e7 kg) = 407 s ; M* = 5,1e14 g (valeurs utilisées comme repères par D)"),
 ("MacGibbon1991", "D,H", "10.1103/PhysRevD.44.376", "paramétrisation f(M), α = 5,34e25 g³/s"),
 ("Middlemiss2016", "C", "10.1038/nature17397", "gravimètre MEMS 40 µGal/√Hz"),
 ("Torres2017", "F,H", "10.1038/nphys4151", "superradiance d'un vortex en cuve : 14 ± 8 %"),
 ("LyonsVanderkulk1962", "C,F,H", "10.1147/rd.62.0200", "redondance modulaire triple à vote majoritaire (1962)"),
 ("MudawarBowers1999", "C", "10.1016/S0017-9310(98)00241-5", "flux critique record 276 MW/m²"),
 ("Yao2017_hors", "ctrl", "10.1103/PhysRevLett.118.030401", "(contrôle négatif de la chaîne : cristaux temporels)"),
 ("Unruh1976", "C", "10.1103/PhysRevD.14.3251", "section efficace de Dirac à basse énergie = 1/8 de celle du scalaire"),
 ("Page1976b", "B,C,H", "10.1103/PhysRevD.14.3260", "le moment cinétique est émis plusieurs fois plus vite que l'énergie"),
 ("FordRoman1995", "B", "10.1103/PhysRevD.51.4277", "inégalité quantique, échantillonnage lorentzien : ρ ≥ −3ħ/(32π²c³τ⁴)"),
 ("Gott1991", "B,H", "10.1103/PhysRevLett.66.1126", "deux cordes cosmiques en mouvement relativiste ⇒ CTC"),
]
out = {}
for cle, eq, doi, usage in REFS:
    res = None
    try:
        j = json.loads(get("https://inspirehep.net/api/literature?size=1&fields=titles,abstracts&q=" + urllib.parse.quote("doi:" + doi), f"c_inspire_{cle}.json"))
        h = j["hits"]["hits"]
        if h:
            m = h[0]["metadata"]; ab = m.get("abstracts") or []
            res = {"titre": m["titles"][0]["title"], "resume": propre(max((a["value"] for a in ab), key=len)) if ab else "", "source": "INSPIRE"}
    except Exception: pass
    if not res or not res["resume"]:
        try:
            j = json.loads(get("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi, safe="/"), f"c_openalex_{cle}.json"))
            inv = j.get("abstract_inverted_index") or {}
            mots = sorted(((p, w) for w, ps in inv.items() for p in ps))
            r2 = {"titre": j.get("title") or "", "resume": propre(" ".join(w for _, w in mots)), "source": "OpenAlex"}
            if r2["resume"] or not res: res = r2
        except Exception: pass
    if not res or not res["resume"]:
        try:
            j = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"), f"c_crossref_{cle}.json"))["message"]
            r3 = {"titre": (j.get("title") or [""])[0], "resume": propre(j.get("abstract", "")), "source": "Crossref"}
            if r3["resume"] or not res or not res.get("titre"): res = r3
        except Exception: pass
    out[cle] = dict(equipe=eq, doi=doi, usage=usage, **(res or {"titre": "", "resume": "", "source": "AUCUNE"}))
    print(f"### {cle} [{eq}] {out[cle]['source']} | {out[cle]['titre'][:100]}\n   USAGE : {usage}\n   {out[cle]['resume'][:1100]}\n", flush=True)
# recherche en texte intégral sur INSPIRE
for q in ('fulltext:"Tipler sinusoid"', 'fulltext:"off-set Tipler"', 'fulltext:"negative time event horizon"'):
    try:
        j = json.loads(get("https://inspirehep.net/api/literature?size=5&fields=titles,arxiv_eprints,earliest_date&q=" + urllib.parse.quote(q), "c_fulltext_" + re.sub(r"\W+", "_", q) + ".json"))
        hits = j["hits"]
        print("RECHERCHE", q, "→", hits["total"], [(h["metadata"]["titles"][0]["title"][:70], (h["metadata"].get("arxiv_eprints") or [{}])[0].get("value"), h["metadata"].get("earliest_date")) for h in hits["hits"]])
        out["recherche " + q] = {"total": hits["total"]}
    except Exception as e:
        print("RECHERCHE", q, "échec", e)
json.dump(out, open(os.path.join(V, "resumes_complement.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
