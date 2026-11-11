#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Archive un fil complet du forum Time Travel Institute (moteur Discourse, API JSON publique).

Usage : python -I telecharger_tti.py <dossier_sortie> <id_fil> [<id_fil> ...]
Produit pour chaque fil : tti_t<ID>_complet.json (tous les messages) et tti_t<ID>.txt (texte lisible :
numéro, date ISO, pseudonyme, texte brut, liens et images cités).
Lecture seule ; aucune authentification ; pause entre requêtes.
"""
import html
import json
import os
import re
import subprocess
import sys
import time

AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
         "(KHTML, like Gecko) Version/17.0 Safari/605.1.15")
BASE = "https://timetravelinstitute.com"


def get(url):
    for i in range(4):
        r = subprocess.run(["curl", "-s", "-L", "-m", "60", "-A", AGENT, "-w", "%{http_code}", url],
                           capture_output=True)
        d = r.stdout
        code = d[-3:].decode("ascii", "replace")
        if code == "200":
            return json.loads(d[:-3].decode("utf-8"))
        time.sleep(5 * (i + 1))
    raise RuntimeError(f"échec {url} (HTTP {code})")


def texte(cooked):
    t = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r" [IMG:\1] ", cooked)
    t = re.sub(r"<a[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"\2 <\1>", t, flags=re.S)
    t = re.sub(r"<br\s*/?>|</p>|</div>|</li>|</blockquote>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(t).strip()


def main():
    sortie = sys.argv[1]
    os.makedirs(sortie, exist_ok=True)
    for tid in sys.argv[2:]:
        d = get(f"{BASE}/t/{tid}.json")
        ids = d["post_stream"]["stream"]
        posts = {p["id"]: p for p in d["post_stream"]["posts"]}
        manquants = [i for i in ids if i not in posts]
        for k in range(0, len(manquants), 20):
            lot = manquants[k:k + 20]
            q = "&".join(f"post_ids[]={i}" for i in lot)
            dd = get(f"{BASE}/t/{tid}/posts.json?{q}")
            for p in dd["post_stream"]["posts"]:
                posts[p["id"]] = p
            time.sleep(1.0)
        ordre = [posts[i] for i in ids if i in posts]
        d["post_stream"]["posts"] = ordre
        with open(os.path.join(sortie, f"tti_t{tid}_complet.json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        with open(os.path.join(sortie, f"tti_t{tid}.txt"), "w", encoding="utf-8") as f:
            f.write(f"# {d.get('title')} — {BASE}/t/{d.get('slug')}/{tid}\n")
            f.write(f"# {len(ordre)} messages sur {len(ids)} ; créé le {d.get('created_at')}\n\n")
            for p in ordre:
                f.write(f"--- #{p['post_number']} | {p['created_at']} | {p['username']} "
                        f"(nom affiché : {p.get('name')})\n{texte(p['cooked'])}\n\n")
        print(tid, d.get("title"), len(ordre), "/", len(ids))
        time.sleep(1.5)


if __name__ == "__main__":
    main()
