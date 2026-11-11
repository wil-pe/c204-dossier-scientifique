#!/usr/bin/env python3
"""Vérification bibliographique de l'Équipe H (programme C204).

Usage : python -I verifier_biblio.py <dossier 09_recherche_contemporaine> [fichier_candidats] [nom_sortie.json]

Pour chaque référence candidate, interroge l'API arXiv (identifiant ou recherche) ou l'API Crossref (DOI ou
recherche bibliographique) et compare le titre et les auteurs renvoyés avec ce que le rédacteur attendait.
Les réponses brutes sont rangées dans donnees_brutes/cache/ (données non fiables : jamais exécutées).
Chaque requête est consignée dans donnees_brutes/journal_requetes.jsonl.
Aucune donnée personnelle n'est transmise (agent utilisateur générique, pas d'adresse électronique).
"""
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
import xml.etree.ElementTree as ET

BASE = pathlib.Path(sys.argv[1])
CAND = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else BASE / "outils" / "candidats.txt"
RAW = BASE / "donnees_brutes"
CACHE = RAW / "cache"
CACHE.mkdir(parents=True, exist_ok=True)
LOG = RAW / "journal_requetes.jsonl"
OUT = RAW / (sys.argv[3] if len(sys.argv) > 3 else "resultats_verification.json")
UA = "C204-biblio-check/1.0 (verification bibliographique automatisee)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARX = "{http://arxiv.org/schemas/atom}"
PAUSE_ARXIV = 3.2
PAUSE_CROSSREF = 1.0


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.lower())


def log(entry):
    entry["horodatage"] = datetime.datetime.now().isoformat(timespec="seconds")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def fetch(url, pause, service):
    """Renvoie (code_http, corps). Utilise un cache disque pour ne pas répéter les requêtes réussies."""
    h = hashlib.sha256(url.encode()).hexdigest()[:24]
    cf = CACHE / (h + ".txt")
    if cf.exists():
        return "200", cf.read_text(encoding="utf-8")
    for essai in (1, 2, 3):
        p = subprocess.run(
            ["curl", "-sS", "-L", "-m", "90", "-A", UA, "-w", "\n%{http_code}", url],
            capture_output=True,
        )
        out = p.stdout.decode("utf-8", "replace")
        body, _, code = out.rpartition("\n")
        code = code.strip()
        log({"service": service, "url": url, "http": code, "essai": essai, "octets": len(body),
             "erreur_curl": p.stderr.decode("utf-8", "replace").strip()[:200]})
        time.sleep(pause)
        if code == "200":
            cf.write_text(body, encoding="utf-8")
            return code, body
        if code in ("404", "400"):
            return code, body
        time.sleep(pause * 2 * essai)
    return code, body


def parse_arxiv(body):
    res = []
    try:
        root = ET.fromstring(body)
    except ET.ParseError:
        return res
    for e in root.findall(ATOM + "entry"):
        idurl = (e.findtext(ATOM + "id") or "").strip()
        m = re.search(r"arxiv\.org/abs/(.+?)(v\d+)?$", idurl)
        if not m:
            continue
        title = re.sub(r"\s+", " ", (e.findtext(ATOM + "title") or "").strip())
        authors = [re.sub(r"\s+", " ", (a.findtext(ATOM + "name") or "").strip()) for a in e.findall(ATOM + "author")]
        res.append({
            "arxiv": m.group(1),
            "titre": title,
            "auteurs": authors,
            "annee": (e.findtext(ATOM + "published") or "")[:4],
            "revue_arxiv": re.sub(r"\s+", " ", (e.findtext(ARX + "journal_ref") or "").strip()),
            "doi": (e.findtext(ARX + "doi") or "").strip(),
            "url": "https://arxiv.org/abs/" + m.group(1),
        })
    return res


def crossref_record(msg):
    auteurs = []
    for a in msg.get("author", []) or []:
        nom = (a.get("given", "") + " " + a.get("family", "")).strip() or a.get("name", "")
        if nom:
            auteurs.append(nom)
    annee = ""
    for k in ("published-print", "published-online", "issued", "published"):
        dp = (msg.get(k) or {}).get("date-parts") or [[None]]
        if dp and dp[0] and dp[0][0]:
            annee = str(dp[0][0])
            break
    cont = (msg.get("container-title") or [""])
    ref = cont[0] if cont else ""
    if msg.get("volume"):
        ref += " " + str(msg["volume"])
    pg = msg.get("article-number") or msg.get("page")
    if pg:
        ref += ", " + str(pg)
    titre = re.sub(r"<[^>]+>", "", (msg.get("title") or [""])[0] if msg.get("title") else "")
    return {
        "titre": re.sub(r"\s+", " ", titre).strip(),
        "auteurs": auteurs,
        "annee": annee,
        "revue": ref.strip(),
        "doi": msg.get("DOI", ""),
        "type": msg.get("type", ""),
    }


def concorde(rec, fragment, auteur):
    ok_t = norm(fragment) in norm(rec.get("titre", ""))
    if not auteur:
        return ok_t, ok_t, True
    ok_a = any(norm(auteur) in norm(a) for a in rec.get("auteurs", []))
    return (ok_t and ok_a), ok_t, ok_a


def lire_candidats():
    cands = []
    for line in CAND.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|")
        while len(parts) < 6:
            parts.append("")
        cands.append(dict(zip(("cle", "theme", "type", "ident", "fragment", "auteur"), parts[:6])))
    return cands


def main():
    cands = lire_candidats()
    resultats = {}
    # --- 1. arXiv par identifiant, par lots ---
    arx = [c for c in cands if c["type"] == "arxiv"]
    par_id = {}
    for i in range(0, len(arx), 20):
        lot = arx[i:i + 20]
        url = ("https://export.arxiv.org/api/query?id_list="
               + ",".join(urllib.parse.quote(c["ident"], safe="/.") for c in lot) + "&max_results=40")
        code, body = fetch(url, PAUSE_ARXIV, "arXiv")
        if code == "200":
            for r in parse_arxiv(body):
                par_id[r["arxiv"]] = r
        print(f"arXiv lot {i // 20 + 1} : HTTP {code}, cumul {len(par_id)} notices", flush=True)
    for c in arx:
        r = par_id.get(c["ident"])
        if not r:
            resultats[c["cle"]] = {**c, "statut": "non vérifiée", "note": "identifiant arXiv absent de la réponse de l'API"}
            continue
        ok, ok_t, ok_a = concorde(r, c["fragment"], c["auteur"])
        resultats[c["cle"]] = {**c, **r, "statut": "vérifiée" if ok else "à revoir",
                               "note": "" if ok else f"discordance (titre {'ok' if ok_t else 'NON'}, auteur {'ok' if ok_a else 'NON'})",
                               "source_verif": "API arXiv (id_list)"}
    # --- 2. arXiv par recherche ---
    for c in [c for c in cands if c["type"] == "search"]:
        url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(c["ident"])
               + "&max_results=8&sortBy=relevance")
        code, body = fetch(url, PAUSE_ARXIV, "arXiv")
        recs = parse_arxiv(body) if code == "200" else []
        choisi = None
        for r in recs:
            if concorde(r, c["fragment"], c["auteur"])[0]:
                choisi = r
                break
        if choisi:
            resultats[c["cle"]] = {**c, **choisi, "statut": "vérifiée", "note": "trouvée par recherche API arXiv",
                                   "source_verif": "API arXiv (search_query)", "url_requete": url}
        else:
            resultats[c["cle"]] = {**c, "statut": "non vérifiée",
                                   "note": "recherche arXiv sans résultat concordant ; candidats : "
                                           + " / ".join(r["titre"][:80] for r in recs[:5]),
                                   "url_requete": url}
        print(f"recherche {c['cle']} : {resultats[c['cle']]['statut']}", flush=True)
    # --- 3. Crossref par DOI ---
    for c in [c for c in cands if c["type"] == "doi"]:
        url = "https://api.crossref.org/works/" + urllib.parse.quote(c["ident"], safe="/")
        code, body = fetch(url, PAUSE_CROSSREF, "Crossref")
        if code != "200":
            resultats[c["cle"]] = {**c, "statut": "non vérifiée", "note": f"Crossref HTTP {code}", "doi": c["ident"]}
            continue
        try:
            r = crossref_record(json.loads(body)["message"])
        except (ValueError, KeyError):
            resultats[c["cle"]] = {**c, "statut": "non vérifiée", "note": "réponse Crossref illisible", "doi": c["ident"]}
            continue
        ok, ok_t, ok_a = concorde(r, c["fragment"], c["auteur"])
        resultats[c["cle"]] = {**c, **r, "url": "https://doi.org/" + c["ident"], "url_requete": url,
                               "statut": "vérifiée" if ok else "à revoir",
                               "note": "" if ok else f"discordance (titre {'ok' if ok_t else 'NON'}, auteur {'ok' if ok_a else 'NON'})",
                               "source_verif": "API Crossref (DOI)"}
    print("Crossref DOI terminé", flush=True)
    # --- 4. Crossref recherche bibliographique ---
    for c in [c for c in cands if c["type"] == "biblio"]:
        url = ("https://api.crossref.org/works?rows=5&query.bibliographic=" + urllib.parse.quote(c["ident"]))
        code, body = fetch(url, PAUSE_CROSSREF, "Crossref")
        choisi, recs = None, []
        if code == "200":
            try:
                recs = [crossref_record(m) for m in json.loads(body)["message"]["items"]]
            except (ValueError, KeyError):
                recs = []
        for r in recs:
            if concorde(r, c["fragment"], c["auteur"])[0]:
                choisi = r
                break
        if choisi:
            resultats[c["cle"]] = {**c, **choisi, "url": "https://doi.org/" + choisi["doi"], "url_requete": url,
                                   "statut": "vérifiée", "note": "trouvée par recherche Crossref",
                                   "source_verif": "API Crossref (query.bibliographic)"}
        else:
            resultats[c["cle"]] = {**c, "statut": "non vérifiée", "url_requete": url,
                                   "note": "recherche Crossref sans résultat concordant ; candidats : "
                                           + " / ".join(r["titre"][:80] for r in recs[:5])}
    # --- 5. Enrichissement : revue via Crossref pour les notices arXiv munies d'un DOI ---
    for cle, r in resultats.items():
        if r.get("type") in ("arxiv", "search") and r.get("doi") and r.get("statut") in ("vérifiée", "à revoir"):
            url = "https://api.crossref.org/works/" + urllib.parse.quote(r["doi"], safe="/")
            code, body = fetch(url, PAUSE_CROSSREF, "Crossref")
            if code == "200":
                try:
                    cr = crossref_record(json.loads(body)["message"])
                    r["revue"] = cr["revue"]
                    r["annee_revue"] = cr["annee"]
                    r["titre_crossref"] = cr["titre"]
                    r["double_verif"] = norm(cr["titre"])[:25] == norm(r["titre"])[:25]
                except (ValueError, KeyError):
                    pass
    OUT.write_text(json.dumps(resultats, ensure_ascii=False, indent=1), encoding="utf-8")
    n = {}
    for r in resultats.values():
        n[r["statut"]] = n.get(r["statut"], 0) + 1
    print("BILAN :", n)
    for cle, r in resultats.items():
        if r["statut"] != "vérifiée":
            print(f"  {cle} [{r['type']} {r['ident'][:50]}] {r['statut']} — {r.get('note', '')} — titre reçu : {r.get('titre', '')[:110]} — auteurs : {', '.join(r.get('auteurs', [])[:3])}")


if __name__ == "__main__":
    main()
