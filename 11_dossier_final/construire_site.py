"""Construit le dossier docs/ (site statique, compatible GitHub Pages) à partir des livrables.

Usage, depuis la racine C204 :
    .venv/bin/python 11_dossier_final/construire_site.py [URL_DU_DEPOT]

- copie le simulateur et la visionneuse (fichiers HTML autonomes) ;
- copie quelques figures ;
- écrit docs/index.html, page d'accueil qui renvoie aux rapports du dépôt.
"""
from pathlib import Path
import html
import shutil
import sys

RACINE = Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
DEPOT = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")

PAGES = [
    ("06_modele_3D/simulateur.html", "simulateur.html"),
    ("06_modele_3D/visionneuse.html", "visionneuse.html"),
]
FIGURES = [
    ("06_modele_3D/rendus/11_comparaison_DOC-004.png", "comparaison_document_modele.png"),
    ("06_modele_3D/rendus/05_eclate.png", "vue_eclatee.png"),
    ("05_simulations/S01_hawking/figures/S01_fig4_carte_contraintes.png", "carte_contraintes.png"),
    ("10_machine_optimisee/figures/figure_de_merite.png", "figure_de_merite.png"),
    ("10_machine_optimisee/modele_R1/rendus/R1_02_interieur.png", "palier_R1_interieur.png"),
]
RAPPORTS = [
    ("11_dossier_final/DOSSIER_SCIENTIFIQUE_C204.md", "Synthèse du programme", "Les treize livrables, les dix questions, les limites"),
    ("10_machine_optimisee/GUIDE_CONSTRUCTION.md", "Guide de construction", "Réplique inerte, version d'initiation, palier R1 complet"),
    ("01_archive/INVENTAIRE.md", "Inventaire des documents", "Les 22 pièces, leur provenance, leur attribution"),
    ("01_archive/HISTORIQUE.md", "Historique", "Chronologie 2000-2001 et diffusion ultérieure"),
    ("02_reconstruction/DOSSIER_TECHNIQUE.md", "Dossier technique", "L'objet tel que décrit, plans, dimensions"),
    ("03_physique_theorique/RAPPORT_B.md", "Physique théorique", "Kerr, Tipler, micro-trous noirs, causalité"),
    ("04_ingenierie/RAPPORT_C.md", "Ingénierie", "Sous-système par sous-système : constructible ou non"),
    ("05_simulations/RAPPORT_D.md", "Simulations", "Neuf simulations reproductibles"),
    ("07_experiences/RAPPORT_F.md", "Expériences", "Douze protocoles sans danger"),
    ("08_red_team/RAPPORT_RED_TEAM_2.md", "Critique de notre propre travail", "Validation contradictoire et corrections"),
    ("09_recherche_contemporaine/RAPPORT_H.md", "Recherche contemporaine", "Littérature 2001-2026, bibliographie vérifiée"),
    ("10_machine_optimisee/RAPPORT_I.md", "Machine optimisée", "Trois paliers de machine cohérente"),
]
VERDICT = [
    ("Un objet, pas une machine", "Les documents montrent l'extérieur d'un coffre à deux logements circulaires. Rien ne documente l'intérieur."),
    ("Exclue par la physique connue", "Écarts de 10 à 30 ordres de grandeur, recalculés par cinq équipes."),
    ("Des chiffres empruntés à de la vraie physique", "Puissance, taille et masse annoncées sont celles d'un trou noir primordial d'environ 10¹² kg — incompatibles avec une unité de 227 kg."),
    ("Périphérie constructible, cœur impossible", "Horloges, calculateurs à vote, gravimètre : oui. Micro-trous noirs, confinement, évent à rayons X : non."),
    ("Jamais vers le passé", "Vers le futur, l'effet est réel mais infime : environ 0,5 milliardième de seconde par heure pour la version constructible."),
]

CSS = """
:root{--fond:#fbfaf7;--carte:#ffffff;--texte:#1d1c1a;--discret:#5f5b55;--trait:#dedad2;--accent:#0b5c8a;--accent2:#b3541e}
@media (prefers-color-scheme:dark){:root{--fond:#15171a;--carte:#1d2024;--texte:#eceae6;--discret:#a39f98;--trait:#32363c;--accent:#6fb6e0;--accent2:#e59a66}}
*{box-sizing:border-box}
body{margin:0;background:var(--fond);color:var(--texte);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:1040px;margin:0 auto;padding:40px 16px 72px}
h1{font-size:clamp(1.7rem,4.5vw,2.6rem);line-height:1.15;margin:0 0 12px;text-wrap:balance}
h2{font-size:1.25rem;margin:48px 0 16px}
p.chapeau{color:var(--discret);max-width:68ch;margin:0 0 28px}
a{color:var(--accent)}
.avert{border-left:4px solid var(--accent2);background:var(--carte);padding:12px 16px;margin:0 0 32px;max-width:76ch}
.grille{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.carte{background:var(--carte);border:1px solid var(--trait);border-radius:10px;padding:18px;display:block;text-decoration:none;color:inherit}
a.carte:hover,a.carte:focus-visible{border-color:var(--accent);outline:none}
.carte strong{display:block;font-size:1.05rem;margin-bottom:4px;color:var(--accent)}
.carte span{color:var(--discret);font-size:.95rem}
.principal strong{font-size:1.2rem}
ol.verdict{padding-left:1.3em;max-width:76ch}
ol.verdict li{margin-bottom:10px}
figure{margin:0}
figure img{width:100%;height:auto;border:1px solid var(--trait);border-radius:10px;background:#fff}
figcaption{color:var(--discret);font-size:.9rem;margin-top:6px}
footer{margin-top:56px;color:var(--discret);font-size:.9rem;border-top:1px solid var(--trait);padding-top:16px}
"""


def lien_rapport(chemin: str) -> str:
    return f"{DEPOT}/blob/main/{chemin}" if DEPOT else f"../{chemin}"


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "figures").mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    presentes = []
    for src, dst in PAGES:
        s = RACINE / src
        if s.exists():
            shutil.copyfile(s, DOCS / dst)
            presentes.append(dst)
        else:
            print("absent, non copié :", src)
    for src, dst in FIGURES:
        s = RACINE / src
        if s.exists():
            shutil.copyfile(s, DOCS / "figures" / dst)
        else:
            print("absent, non copié :", src)

    e = html.escape
    cartes_pages = []
    if "simulateur.html" in presentes:
        cartes_pages.append('<a class="carte principal" href="simulateur.html"><strong>Simulateur 3D</strong>'
                            '<span>Vue éclatée, « si elle fonctionnait », ce que dit la physique, version constructible</span></a>')
    if "visionneuse.html" in presentes:
        cartes_pages.append('<a class="carte principal" href="visionneuse.html"><strong>Visionneuse du modèle</strong>'
                            '<span>Chaque pièce avec sa source et son niveau de preuve</span></a>')
    guide = RACINE / "10_machine_optimisee/GUIDE_CONSTRUCTION.md"
    if guide.exists():
        cartes_pages.append(f'<a class="carte principal" href="{e(lien_rapport("10_machine_optimisee/GUIDE_CONSTRUCTION.md"))}">'
                            '<strong>Guide de construction</strong><span>Ce qui peut réellement être construit, et comment</span></a>')
    cartes_rapports = "\n".join(
        f'<a class="carte" href="{e(lien_rapport(c))}"><strong>{e(t)}</strong><span>{e(d)}</span></a>'
        for c, t, d in RAPPORTS if (RACINE / c).exists())
    verdict = "\n".join(f"<li><strong>{e(t)}.</strong> {e(d)}</li>" for t, d in VERDICT)
    page = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Programme C204</title>
<meta name="description" content="Étude scientifique critique de la « machine temporelle C204 » attribuée à John Titor.">
<style>{CSS}</style></head><body><main>
<h1>La «&nbsp;machine temporelle C204&nbsp;» à l'épreuve de la physique</h1>
<p class="chapeau">Étude critique des documents attribués à « John Titor » (2000-2001) : reconstitution de l'objet décrit,
analyse physique, simulations, et conception de ce que l'on pourrait réellement construire.</p>
<p class="avert">Rien de ce qu'affirment les documents d'origine n'est tenu pour vrai. Les vues « si elle fonctionnait »
reconstituent un récit ; elles ne correspondent à aucun phénomène observé. Aucune expérience n'a été réalisée.</p>
<div class="grille">
{chr(10).join(cartes_pages)}
</div>
<h2>Le verdict en cinq points</h2>
<ol class="verdict">
{verdict}
</ol>
<h2>En images</h2>
<div class="grille">
<figure><img src="figures/comparaison_document_modele.png" alt="Page de manuel d'origine à gauche, modèle 3D reconstitué à droite" loading="lazy"><figcaption>La page de manuel et le modèle reconstitué, vus du même point</figcaption></figure>
<figure><img src="figures/carte_contraintes.png" alt="Carte de contraintes : aucune masse ne satisfait toutes les affirmations" loading="lazy"><figcaption>Aucune masse ne satisfait à la fois toutes les affirmations du récit</figcaption></figure>
<figure><img src="figures/palier_R1_interieur.png" alt="Composants internes de la version constructible" loading="lazy"><figcaption>La version constructible, dans le même coffre</figcaption></figure>
</div>
<h2>Les rapports</h2>
<div class="grille">
{cartes_rapports}
</div>
<footer>Simulations illustratives. Références vérifiées en ligne sur leurs métadonnées et leurs résumés.
{f'<br>Dépôt : <a href="{e(DEPOT)}">{e(DEPOT)}</a>' if DEPOT else ''}</footer>
</main></body></html>
"""
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    print("docs/index.html écrit ;", len(presentes), "page(s) copiée(s) ; dépôt :", DEPOT or "(liens relatifs)")


if __name__ == "__main__":
    main()
