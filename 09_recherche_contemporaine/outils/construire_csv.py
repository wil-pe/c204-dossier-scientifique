#!/usr/bin/env python3
"""Construit bibliographie_verifiee.csv à partir des résultats des passes de vérification (Équipe H, C204).

Usage : python -I construire_csv.py <dossier 09_recherche_contemporaine>

- fusionne donnees_brutes/resultats_passe{1,2,3}.json ;
- écarte les notices non retenues (mauvais identifiant, résultat de recherche hors sujet) ;
- pour les notices arXiv sans DOI ni référence de revue, cherche la version publiée par titre exact dans Crossref ;
- ajoute les pages web institutionnelles consultées et les références restées « non vérifiées » ;
- écrit le CSV et un résumé chiffré (donnees_brutes/bilan_csv.json).
"""
import csv
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import sys
import time
import unicodedata
import urllib.parse

BASE = pathlib.Path(sys.argv[1])
RAW = BASE / "donnees_brutes"
CACHE = RAW / "cache"
LOG = RAW / "journal_requetes.jsonl"
UA = "C204-biblio-check/1.0 (verification bibliographique automatisee)"
AUJ = datetime.date.today().isoformat()

THEMES = {
    "1": "1 Micro-trous noirs, LHC, trous noirs primordiaux",
    "2": "2 Rayonnement de Hawking, analogues, information",
    "3": "3 Géométrie de Kerr : observations et mathématiques",
    "4": "4 Trous de ver traversables",
    "5": "5 Métriques de distorsion (warp)",
    "6": "6 Courbes temporelles fermées et causalité",
    "7": "7 Gravité quantique et expériences de table",
    "8": "8 Métrologie du temps",
    "9": "9 Gravimétrie de précision",
    "10": "10 Énergie négative et effet Casimir",
    "11": "11 Cristaux temporels et faux amis du « temps »",
    "12": "12 IBM 5100, an 2038, redondance des calculateurs",
}

# Notices écartées : (clé) -> motif (consigné dans le journal, pas dans le CSV)
ECARTEES = {
    "LHAASOPBH": "résultat de recherche arXiv sans rapport direct avec la limite LHAASO voulue (remplacé par PBH2505)",
    "GW250114": "la recherche par titre a renvoyé une analyse tierce ; remplacée par l'article LVK (GW250114LVK)",
    "GW231123": "la recherche par titre a renvoyé une analyse tierce ; remplacée par l'article LVK (GW231123LVK)",
    "GWTC4": "article « population » ; remplacé par l'article de catalogue (GWTC4cat)",
    "Bose1707": "requête exploratoire sans résultat",
    "TiplerSin": "requête de contrôle terminologique (zéro résultat attendu) — voir journal",
    "EHTM87pers": "non retrouvée par l'API arXiv ; référence abandonnée",
    "KN80": "DOI de mémoire erroné (HTTP 404) ; remplacé par KN80b trouvé par recherche Crossref",
    "CHR09": "identifiant arXiv de mémoire erroné (0907.1280 est un autre article) ; remplacé par CHR09b",
    "Katz78": "requête exploratoire sans résultat pertinent",
    "KerrCTC": "résultat de recherche non retenu (prépublication isolée, non utilisée dans le rapport)",
    "Lu26doi": "doublon de Lu26 (même article, vérifié par arXiv et par DOI)",
}

# Phase 7 : le champ DOI de ces notices arXiv ne désigne pas l'article lui-même (contrôle auteurs + titre).
DOI_ARXIV_ERRONES = {
    "FH06": "le DOI de la notice arXiv (10.1002/andp.200510172) désigne un autre article du même numéro ; DOI correct vérifié par Crossref",
    "FSW93": "le DOI de la notice arXiv (10.1103/PhysRevLett.75.1872) désigne l'erratum de 1995 ; DOI de l'article de 1993 vérifié par Crossref",
}
NOTES_MANUELLES = {
    "AL17": "le DOI de la notice arXiv est celui de l'ouvrage collectif (Springer, 2017) dont ce texte est un chapitre",
}

NON_VERIFIEES_MANUELLES = [
    {"cle": "Friedl83", "theme": "12", "auteurs": "P. J. Friedl", "titre": "SCAMP: The Missing Link in the PC's Past?",
     "annee": "1983", "revue": "PC Magazine (novembre 1983) — de mémoire", "doi": "", "arxiv": "",
     "url": "https://api.crossref.org/works?rows=5&query.bibliographic=Friedl%20SCAMP%3A%20The%20Missing%20Link%20in%20the%20PC%27s%20Past%20PC%20Magazine%201983",
     "source": "recherche Crossref sans résultat (magazine sans DOI)", "statut": "non vérifiée",
     "note": "Citée de mémoire ; Wikipédia (IBM 5100) cite PC Magazine, nov. 1983, sans auteur. Non utilisée comme preuve."},
]

PAGES_WEB = [
    ("WebCERN-ESPP26", "1", "CERN", "The CERN Council decided to update the European Strategy for Particle Physics", "2026",
     "https://home.cern/the-cern-council-decided-to-update-the-european-strategy-for-particle-physics/",
     "page lue (WebFetch) : décision du 22 mai 2026, FCC-ee option préférée, décision visée d'ici 2028"),
    ("WebCERN-Calendrier24", "1", "CERN (M. Lamont)", "Updated schedule for CERN's accelerators", "2024",
     "https://home.cern/updated-schedule-cerns-accelerators",
     "page lue (WebFetch + curl HTTP 200) : LS3 du LHC début juillet 2026 ; HL-LHC (Run 4) vers juin 2030"),
    ("WebCERN-LEP", "1", "CERN", "The Large Electron-Positron Collider", "s.d.",
     "https://home.cern/science/accelerators/large-electron-positron-collider", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebCERN-Chrono", "1", "CERN / CERN Courier", "Chronologie du LHC (premier faisceau 10 sept. 2008 ; incident 19 sept. 2008 ; collisions à 7 TeV le 30 mars 2010)", "s.d.",
     "https://timeline.web.cern.ch/timeline-header/87",
     "repérée par recherche web (WebSearch, domaines cern) ; pages non ouvertes individuellement"),
    ("WebBIPM-Res5", "8", "BIPM / CGPM", "Resolution 5 of the 27th CGPM (2022) — On the future redefinition of the second", "2022",
     "https://www.bipm.org/en/cgpm-2022/resolution-5", "page lue (WebFetch + curl HTTP 200) : propositions attendues en 2026, adoption visée en 2030"),
    ("WebBIPM-Res4", "8", "BIPM / CGPM", "Resolution 4 of the 27th CGPM (2022)", "2022",
     "https://www.bipm.org/en/cgpm-2022/resolution-4", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebNIST-CSAC", "8", "NIST", "Chip-Scale Clocks", "s.d.",
     "https://www.nist.gov/noac/technology/time-and-frequency/chip-scale-clocks", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebLIGO-2025", "3", "LIGO Laboratory (Caltech)", "Ten Years Later, LIGO is a Black-Hole Hunting Machine", "2025",
     "https://www.ligo.caltech.edu/news/ligo20250910", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebSandia-Z", "1", "Sandia National Laboratories", "Z Pulsed Power Facility", "s.d.",
     "https://www.sandia.gov/z-machine/", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebGPB", "3", "Stanford University", "Gravity Probe B: Testing Einstein's Universe", "s.d.",
     "https://einstein.stanford.edu/", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebPOSIX-time_t", "12", "The Open Group / IEEE", "<sys/types.h> — POSIX.1-2024 (Issue 8)", "2024",
     "https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/sys_types.h.html",
     "page lue (WebFetch + curl HTTP 200) : time_t entier d'au moins 64 bits"),
    ("WebLWN-2038", "12", "LWN.net", "Approaching the kernel year-2038 end game", "2019",
     "https://lwn.net/Articles/776435/", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("Webglibc-2038", "12", "glibc wiki", "Y2038ProofnessDesign", "s.d.",
     "https://sourceware.org/glibc/wiki/Y2038ProofnessDesign", "existence vérifiée (curl HTTP 200, titre de page)"),
    ("WebDebian13", "12", "Debian", "Release notes for Debian 13 (trixie) — What's new", "2025",
     "https://www.debian.org/releases/trixie/release-notes/whats-new.html",
     "page lue (WebFetch) : time_t 64 bits sur toutes les architectures sauf i386"),
    ("WebWP-2038", "12", "Wikipédia (en)", "Year 2038 problem", "consultée 2026-11-10",
     "https://en.wikipedia.org/wiki/Year_2038_problem", "page lue (WebFetch) ; source tertiaire"),
    ("WebWP-5100", "12", "Wikipédia (en)", "IBM 5100", "consultée 2026-11-10",
     "https://en.wikipedia.org/wiki/IBM_5100", "page lue (WebFetch) ; source tertiaire"),
    ("WebWP-PALM", "12", "Wikipédia (en)", "IBM PALM processor", "consultée 2026-11-10",
     "https://en.wikipedia.org/wiki/IBM_PALM_processor", "existence vérifiée (curl HTTP 200, titre de page) ; source tertiaire"),
    ("WebBitsavers-5100", "12", "IBM (numérisation bitsavers, miroir)", "IBM 5100 Maintenance Information Manual, SY31-0405-3 (oct. 1979)", "1979",
     "https://kuiper.mirrorservice.org/sites/www.bitsavers.org/pdf/ibm/5100/SY31-0405-3_IBM_5100_Maintenance_Information_Manual_Oct1979.pdf",
     "repérée par recherche web (WebSearch) ; PDF non ouvert ; l'URL bitsavers devinée de mémoire renvoyait HTTP 404"),
    ("WebLSAG-CDS", "1", "CERN Document Server", "Review of the Safety of LHC Collisions (notice CDS 1111112)", "2008",
     "https://cds.cern.ch/record/1111112", "HTTP 200 mais page anti-robot ; le rapport lui-même est vérifié par arXiv:0806.3414 et DOI"),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def log(entry):
    entry["horodatage"] = datetime.datetime.now().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch(url):
    h = hashlib.sha256(url.encode()).hexdigest()[:24]
    cf = CACHE / (h + ".txt")
    if cf.exists():
        return "200", cf.read_text(encoding="utf-8")
    p = subprocess.run(["curl", "-sS", "-L", "-m", "90", "-A", UA, "-w", "\n%{http_code}", url], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    body, _, code = out.rpartition("\n")
    code = code.strip()
    log({"service": "Crossref", "url": url, "http": code, "essai": 1, "octets": len(body), "objet": "recherche de la version publiée par titre"})
    time.sleep(1.0)
    if code == "200":
        cf.write_text(body, encoding="utf-8")
    return code, body


def version_publiee(titre, auteur):
    """Cherche dans Crossref un article de revue dont le titre normalisé est identique. Renvoie (revue, année, doi) ou None."""
    q = titre + " " + auteur
    url = "https://api.crossref.org/works?rows=5&query.bibliographic=" + urllib.parse.quote(q)
    code, body = fetch(url)
    if code != "200":
        return None
    try:
        items = json.loads(body)["message"]["items"]
    except (ValueError, KeyError):
        return None
    for m in items:
        if m.get("type") != "journal-article":
            continue
        t = re.sub(r"<[^>]+>", "", (m.get("title") or [""])[0])
        if norm(t) != norm(re.sub(r"\$[^$]*\$", "", titre)) and norm(t) != norm(titre):
            continue
        fams = [norm(a.get("family", "")) for a in m.get("author", []) or []]
        if auteur and fams and not any(norm(auteur.split()[-1]) in f or f in norm(auteur) for f in fams if f):
            continue
        cont = (m.get("container-title") or [""])[0]
        ref = cont + (" " + str(m["volume"]) if m.get("volume") else "")
        pg = m.get("article-number") or m.get("page")
        if pg:
            ref += ", " + str(pg)
        an = ""
        for k in ("published-print", "published-online", "issued"):
            dp = (m.get(k) or {}).get("date-parts") or [[None]]
            if dp and dp[0] and dp[0][0]:
                an = str(dp[0][0])
                break
        return ref.strip(), an, m.get("DOI", ""), url
    return None


def auteurs_courts(lst):
    lst = [a for a in lst if a and a.strip(" :") and a.strip() != "Collaboration"]
    if len(lst) <= 3:
        return "; ".join(lst)
    return "; ".join(lst[:3]) + " et al."


def main():
    res = {}
    for n in (1, 2, 3, 5):
        res.update(json.loads((RAW / f"resultats_passe{n}.json").read_text(encoding="utf-8")))
    pub = {}
    for n_pub in (4, 6):  # passes « versions publiées » : DOI vérifiés un à un (clé + "__pub")
        p4 = RAW / f"resultats_passe{n_pub}.json"
        if p4.exists():
            for k, r in json.loads(p4.read_text(encoding="utf-8")).items():
                if r["statut"] == "vérifiée" and k.endswith("__pub"):
                    pub[k[:-5]] = r
    lignes, bilan = [], {"vérifiée": 0, "non vérifiée": 0, "titres_corrigés": [], "écartées": ECARTEES,
                         "versions_publiées_trouvées_par_titre": 0, "pages_web": len(PAGES_WEB)}
    for cle, r in res.items():
        if cle in ECARTEES:
            continue
        if r["statut"] == "non vérifiée":
            continue  # traitées à la main ci-dessous
        note = []
        if r["statut"] == "à revoir":
            # identifiant correct, auteur concordant, mais titre attendu de mémoire différent du titre exact
            note.append("titre attendu de mémoire inexact : titre exact repris de l'API (auteur et sujet concordants, contrôle manuel)")
            bilan["titres_corrigés"].append(cle)
        revue = r.get("revue") or r.get("revue_arxiv") or ""
        annee = r.get("annee_revue") or r.get("annee") or ""
        doi = r.get("doi", "")
        url = r.get("url_requete") or r.get("url", "")  # URL réellement interrogée (API), pas le lien doi.org
        source = r.get("source_verif", "")
        if r.get("type") in ("arxiv", "search"):
            url = "https://export.arxiv.org/api/query?id_list=" + r.get("arxiv", "")
            if cle in pub:
                revue, annee, doi = pub[cle]["revue"], pub[cle]["annee"], pub[cle]["doi"]
                source += " + Crossref (DOI de la version publiée)"
                if norm(pub[cle]["titre"]) != norm(r["titre"]):
                    note.append("titre de la version publiée : " + pub[cle]["titre"])
                bilan["versions_publiées_par_doi_passe4"] = bilan.get("versions_publiées_par_doi_passe4", 0) + 1
                if cle in DOI_ARXIV_ERRONES:
                    note.append(DOI_ARXIV_ERRONES[cle])
            elif not revue and not doi:
                au = (r.get("auteurs") or [""])[0]
                vp = version_publiee(r["titre"], au if "ollaboration" not in au else "")
                # garde-fou : une « version publiée » antérieure de plus d'un an au dépôt arXiv est un homonyme
                if vp and vp[1].isdigit() and r.get("annee", "").isdigit() and int(vp[1]) < int(r["annee"]) - 1:
                    bilan.setdefault("homonymes_rejetés", []).append(f"{cle} : {vp[0]} ({vp[1]}), DOI {vp[2]}")
                    vp = None
                if vp:
                    revue, annee, doi, _ = vp
                    source += " + Crossref (titre exact)"
                    bilan["versions_publiées_trouvées_par_titre"] += 1
                else:
                    revue = "prépublication arXiv (pas de version publiée retrouvée par titre exact)"
            elif doi:
                source += " + Crossref (DOI)"
            if r.get("titre_crossref") and norm(r["titre_crossref"]) != norm(r["titre"]) and r.get("double_verif") is False:
                note.append("titre de la version publiée : " + r["titre_crossref"])
            if r.get("annee") and annee and r["annee"] != annee:
                note.append("dépôt arXiv en " + r["annee"])
        # phase 7 : titre de la version publiée dans une colonne dédiée, dès qu'il diffère du titre de la notice arXiv
        titre_pub = ""
        cand = pub[cle]["titre"] if cle in pub else r.get("titre_crossref", "")
        if r.get("type") in ("arxiv", "search") and cand and norm(cand) != norm(re.sub(r"\$[^$]*\$", "", r.get("titre", ""))) and norm(cand) != norm(r.get("titre", "")):
            titre_pub = cand
        note = [x for x in note if not x.startswith("titre de la version publiée")]
        if cle in NOTES_MANUELLES:
            note.append(NOTES_MANUELLES[cle])
            titre_pub = ""
        lignes.append({
            "cle": cle, "theme": THEMES.get(r["theme"], r["theme"]), "auteurs": auteurs_courts(r.get("auteurs", [])),
            "titre": r.get("titre", ""), "titre_version_publiee": titre_pub, "annee": annee, "revue": revue, "doi": doi, "arxiv": r.get("arxiv", ""),
            "url_consultee": url, "source_verification": source, "statut": "vérifiée", "date_verification": AUJ,
            "note": " ; ".join(note),
        })
        bilan["vérifiée"] += 1
    for nv in NON_VERIFIEES_MANUELLES:
        lignes.append({"cle": nv["cle"], "theme": THEMES[nv["theme"]], "auteurs": nv["auteurs"], "titre": nv["titre"],
                       "titre_version_publiee": "",
                       "annee": nv["annee"], "revue": nv["revue"], "doi": nv["doi"], "arxiv": nv["arxiv"],
                       "url_consultee": nv["url"], "source_verification": nv["source"], "statut": nv["statut"],
                       "date_verification": AUJ, "note": nv["note"]})
        bilan["non vérifiée"] += 1
    for cle, th, aut, titre, an, url, note in PAGES_WEB:
        lignes.append({"cle": cle, "theme": THEMES[th], "auteurs": aut, "titre": titre, "titre_version_publiee": "", "annee": an,
                       "revue": "page web (source institutionnelle ou tertiaire, hors bibliographie scientifique)",
                       "doi": "", "arxiv": "", "url_consultee": url, "source_verification": "consultation directe",
                       "statut": "page web consultée" if "repérée" not in note else "page web repérée (non ouverte)",
                       "date_verification": AUJ, "note": note})
    lignes.sort(key=lambda l: (int(l["theme"].split()[0]), l["statut"] != "vérifiée", l["annee"], l["cle"]))
    champs = ["cle", "theme", "auteurs", "titre", "titre_version_publiee", "annee", "revue", "doi", "arxiv", "url_consultee",
              "source_verification", "statut", "date_verification", "note"]
    with (BASE / "bibliographie_verifiee.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        w.writerows(lignes)
    par_theme = {}
    for l in lignes:
        if l["statut"] == "vérifiée":
            par_theme[l["theme"]] = par_theme.get(l["theme"], 0) + 1
    bilan["par_theme"] = par_theme
    bilan["sans_version_publiee"] = [l["cle"] for l in lignes if l["revue"].startswith("prépublication")]
    (RAW / "bilan_csv.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in bilan.items() if k != "écartées"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
