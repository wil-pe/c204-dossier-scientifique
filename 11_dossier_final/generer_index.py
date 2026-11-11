"""Génère 11_dossier_final/INDEX_DES_FICHIERS.md et vérifie les liens relatifs de la synthèse.

Usage : .venv/bin/python 11_dossier_final/generer_index.py   (depuis la racine C204)
"""
from pathlib import Path
import re

RACINE = Path(__file__).resolve().parent.parent
ICI = Path(__file__).resolve().parent

DOSSIERS = [
    ("01_archive", "Équipe A — archives : originaux, copies alternatives, inventaire, transcriptions, historique"),
    ("02_reconstruction", "Équipe A — dossier technique, plans 2D, dimensions, incohérences"),
    ("03_physique_theorique", "Équipe B — physique théorique et relativité générale"),
    ("04_ingenierie", "Équipe C — électromagnétisme et ingénierie"),
    ("05_simulations", "Équipe D — simulations numériques"),
    ("06_modele_3D", "Équipe E — modèle 3D paramétrique et visionneuse"),
    ("07_experiences", "Équipe F — expériences réalisables"),
    ("08_red_team", "Équipe G — Red Team, deux passages"),
    ("09_recherche_contemporaine", "Équipe H — littérature 2001-2026"),
    ("10_machine_optimisee", "Équipe I — machine optimisée, trois paliers"),
    ("11_dossier_final", "Direction — synthèse finale"),
    ("docs", "Site statique : page d'accueil, simulateur, visionneuse"),
]
# Présents dans le dossier de travail local, mais non redistribués dans le dépôt en ligne (voir .gitignore)
HORS_DEPOT = {"copies_alternatives", "sources_web"}
# Fichiers d'entrée mis en avant : tout .md, .csv, .json, .svg, .html, .sh au premier niveau de chaque dossier
EXT_ENTREE = {".md", ".csv", ".json", ".svg", ".html", ".sh"}


def taille(n: int) -> str:
    for unite in ("o", "ko", "Mo", "Go"):
        if n < 1024 or unite == "Go":
            return (f"{n:.0f} {unite}" if unite == "o" else f"{n:.1f} {unite}").replace(".", ",")
        n /= 1024
    return str(n)


def titre_md(p: Path) -> str:
    try:
        for ligne in p.read_text(encoding="utf-8", errors="replace").splitlines()[:8]:
            if ligne.startswith("# "):
                return ligne[2:].strip()
    except OSError:
        pass
    return ""


def main() -> None:
    L = ["# Index des livrables du programme C204", "",
         "Généré par `generer_index.py`. Les chemins sont relatifs à la racine du projet. Les décomptes sont ceux du",
         "dossier de travail local ; les sous-dossiers marqués « hors dépôt en ligne » n'y sont pas publiés.", ""]
    total_f = total_o = 0
    L += ["## Vue d'ensemble", "", "| Dossier | Contenu | Fichiers | Taille |", "|---|---|---|---|"]
    stats = {}
    for d, desc in DOSSIERS:
        fichiers = [f for f in (RACINE / d).rglob("*") if f.is_file() and ".venv" not in f.parts]
        n = len(fichiers)
        o = sum(f.stat().st_size for f in fichiers)
        stats[d] = (n, o)
        total_f += n
        total_o += o
        L.append(f"| `{d}/` | {desc} | {n} | {taille(o)} |")
    L += [f"| **Total** | | **{total_f}** | **{taille(total_o)}** |", ""]

    for d, desc in DOSSIERS:
        base = RACINE / d
        L += [f"## `{d}/`", "", desc + ".", ""]
        entrees = sorted(f for f in base.iterdir() if f.is_file() and f.suffix.lower() in EXT_ENTREE)
        if entrees:
            L += ["| Fichier | Taille | Titre ou nature |", "|---|---|---|"]
            for f in entrees:
                nature = titre_md(f) if f.suffix == ".md" else {
                    ".csv": "tableau", ".json": "données", ".svg": "schéma vectoriel",
                    ".html": "page interactive", ".sh": "script de relance"}.get(f.suffix, "")
                L.append(f"| `{d}/{f.name}` | {taille(f.stat().st_size)} | {nature} |")
            L.append("")
        sous = sorted(s for s in base.iterdir() if s.is_dir() and not s.name.startswith("."))
        if sous:
            L += ["| Sous-dossier | Fichiers | Types principaux |", "|---|---|---|"]
            for s in sous:
                fs = [f for f in s.rglob("*") if f.is_file()]
                types = {}
                for f in fs:
                    types[f.suffix.lower() or "(sans)"] = types.get(f.suffix.lower() or "(sans)", 0) + 1
                princ = ", ".join(f"{k} ×{v}" for k, v in sorted(types.items(), key=lambda kv: -kv[1])[:4])
                marque = " — **hors dépôt en ligne**" if s.name in HORS_DEPOT else ""
                L.append(f"| `{d}/{s.name}/`{marque} | {len(fs)} | {princ} |")
            L.append("")

    (ICI / "INDEX_DES_FICHIERS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"INDEX_DES_FICHIERS.md écrit : {total_f} fichiers, {taille(total_o)}")

    # Vérification des liens relatifs de la synthèse et du fichier d'accueil
    manquants = 0
    for doc in (ICI / "DOSSIER_SCIENTIFIQUE_C204.md", RACINE / "README.md"):
        if not doc.exists():
            continue
        texte = doc.read_text(encoding="utf-8")
        cibles = set(re.findall(r"\]\(([^)#]+)\)", texte))
        cibles |= {c for c in re.findall(r"`(\.\./[^`]+)`", texte) if " " not in c}
        for c in sorted(cibles):
            if c.startswith("http"):
                continue
            if not (doc.parent / c).exists():
                manquants += 1
                print(f"LIEN MANQUANT dans {doc.name} : {c}")
        print(f"{doc.name} : {len(cibles)} liens contrôlés")
    print("Liens manquants :", manquants)


if __name__ == "__main__":
    main()
