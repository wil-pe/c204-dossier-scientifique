"""Construit le dossier docs/ (site statique servi par GitHub Pages) à partir des livrables.

Usage, depuis la racine du projet :
    .venv/bin/python 11_dossier_final/construire_visuels.py          # bannière, captures, documents
    .venv/bin/python 11_dossier_final/construire_site.py [URL_DU_DEPOT]

- copie le simulateur et la visionneuse (fichiers HTML autonomes) ;
- copie quelques figures ;
- écrit docs/index.html, la page d'exploration du dossier.
"""
from pathlib import Path
import html
import re
import shutil
import sys

RACINE = Path(__file__).resolve().parent.parent
DOCS = RACINE / "docs"
DEPOT = (sys.argv[1] if len(sys.argv) > 1 else "").rstrip("/")
_m = re.match(r"https://github\.com/([^/]+)/([^/]+)$", DEPOT)
SITE = f"https://{_m.group(1)}.github.io/{_m.group(2)}/" if _m else ""

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
MODES = [
    ("explorer", "mode_explorer.png", "Explorer la machine",
     "Ouvrez le coffre, faites glisser le curseur de vue éclatée, cliquez une pièce pour savoir d'où elle vient.",
     "La C204 en vue éclatée, chaque sous-ensemble étiqueté"),
    ("recit", "mode_recit.png", "Si elle fonctionnait",
     "Le récit mis en images, étape par étape : montée en puissance, « champ », lumière courbée, noir complet.",
     "Un pick-up schématique entouré des anneaux du schéma d'origine"),
    ("physique", "mode_physique.png", "Ce que dit la physique",
     "Bougez deux curseurs et lisez la masse, la pesanteur, la dose et la température réellement impliquées.",
     "La même scène avec les zones de dose létale et les résultats chiffrés"),
    ("r1", "mode_r1.png", "La version constructible",
     "Quatre horloges, trois calculateurs qui votent, un compteur de muons. Injectez une panne pour voir.",
     "Le coffre du palier R1 avec ses composants réels"),
]
CHIFFRES = [
    ("227 kg", "la masse annoncée de l'unité"),
    ("4 à 5 Gt", "la masse de chaque « singularité » qu'exigent les 300 à 500 MW annoncés : des milliards de tonnes"),
    ("≈ 1 ms", "le temps pour recevoir une dose létale à un mètre, d'après ces mêmes chiffres"),
    ("87 660", "le facteur de « dix ans par heure ». Les électrons du LEP, au CERN, l'atteignaient presque : 89 000"),
    ("0,5 ns/h", "ce que gagne réellement la version constructible à 130 km/h vers l'est. Un sac de sable ferait pareil"),
    ("58", "erreurs trouvées par notre Red Team dans notre propre travail, corrigées et journalisées"),
]
DOCUMENTS = [
    ("doc003_photo_vehicule.jpg", "L'unité photographiée dans un véhicule", "Photo de 2001"),
    ("doc004_unite_ouverte.jpg", "L'unité ouverte et sa télécommande", "Page de manuel"),
    ("doc007_vue_de_dessus.jpg", "Vue de dessus : « main » et « steering singularity »", "Page de manuel"),
    ("doc008_composants.jpg", "Les douze « composants de base »", "Page de manuel"),
    ("doc009_champ.jpg", "Le « champ sinusoïde de Tipler »", "Page de manuel"),
    ("doc005_ecorche.jpg", "L'écorché à 35 repères, sans légende", "Origine inconnue"),
]
CONSTRUCTIONS = [
    ("A", "Réplique inerte", "Le coffre tel que documenté, en maquette de présentation.", "140 à 240 €", "15 à 25 h"),
    ("B", "C204-R1 Lite", "Version d'initiation : références de temps comparées, trois calculateurs à vote, compteur de muons.", "350 à 730 €", "40 à 80 h"),
    ("C", "C204-R1 complet", "Quatre horloges atomiques miniatures, gyromètre à fibre optique, dans le même coffre.", "≈ 49 k€", "300 à 600 h"),
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

CSS = """
:root{--fond:#fbfaf7;--carte:#ffffff;--texte:#1d1c1a;--discret:#5f5b55;--trait:#dedad2;--accent:#0b5c8a;--chaud:#b3541e;--nuit:#0e1116;--nuit-texte:#f0eee9;--nuit-discret:#a0a6b0;--nuit-accent:#6fb6e0;--nuit-chaud:#e59a66}
@media (prefers-color-scheme:dark){:root{--fond:#15171a;--carte:#1d2024;--texte:#eceae6;--discret:#a39f98;--trait:#32363c;--accent:#6fb6e0;--chaud:#e59a66}}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{margin:0;overflow-x:hidden;background:var(--fond);color:var(--texte);font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--accent)}
img{max-width:100%;height:auto;display:block}
.hero{background:var(--nuit);color:var(--nuit-texte);overflow:hidden}
.hero-in{max-width:1180px;margin:0 auto;padding:56px 16px 0;display:grid;gap:8px 40px;grid-template-columns:minmax(0,1fr);align-items:center}
@media (min-width:920px){.hero-in{grid-template-columns:minmax(0,5fr) minmax(0,6fr);padding-top:72px}}
.surtitre{overflow-wrap:anywhere;margin:0 0 14px;color:var(--nuit-accent);font-weight:700;font-size:.82rem;letter-spacing:.09em;text-transform:uppercase}
.hero h1{font-size:clamp(2rem,5.2vw,3.3rem);line-height:1.08;margin:0 0 18px;letter-spacing:-.015em;text-wrap:balance}
.hero h1 em{font-style:normal;color:var(--nuit-chaud)}
.hero .chapeau{color:var(--nuit-discret);font-size:1.08rem;max-width:56ch;margin:0 0 26px}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 40px}
.bouton{display:inline-block;padding:12px 20px;border-radius:8px;border:1px solid #3a4250;color:var(--nuit-texte);text-decoration:none;font-weight:600}
.bouton:hover,.bouton:focus-visible{border-color:var(--nuit-accent);outline:none}
.bouton.plein{background:var(--nuit-accent);border-color:var(--nuit-accent);color:#08131c}
.bouton.plein:hover,.bouton.plein:focus-visible{background:#8cc6ea}
.hero-img{align-self:end;border-radius:12px 12px 0 0;border:1px solid #262c36;border-bottom:0}
main{max-width:1180px;margin:0 auto;padding:8px 16px 72px}
h2{font-size:1.5rem;line-height:1.2;margin:64px 0 6px;letter-spacing:-.01em}
.sous-titre{color:var(--discret);margin:0 0 22px;max-width:70ch}
.avert{border-left:4px solid var(--chaud);background:var(--carte);padding:12px 16px;margin:32px 0 0;max-width:86ch}
.grille{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.grille.deux{grid-template-columns:minmax(0,1fr)}
@media (min-width:720px){.grille.deux{grid-template-columns:repeat(2,minmax(0,1fr))}}
.carte{background:var(--carte);border:1px solid var(--trait);border-radius:12px;display:block;text-decoration:none;color:inherit;overflow:hidden}
a.carte:hover,a.carte:focus-visible{border-color:var(--accent);outline:none}
.carte .corps{padding:16px 18px 18px}
.carte strong{display:block;font-size:1.08rem;margin-bottom:4px;color:var(--accent)}
.carte span{color:var(--discret);font-size:.95rem}
.carte img.capture{aspect-ratio:860/632;width:100%;object-fit:cover;border-bottom:1px solid var(--trait)}
.numero{display:inline-block;font-size:.8rem;font-weight:700;color:var(--chaud);letter-spacing:.06em;margin-bottom:2px}
.chiffres{display:grid;gap:14px;grid-template-columns:minmax(0,1fr)}
@media (min-width:520px){.chiffres{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (min-width:860px){.chiffres{grid-template-columns:repeat(3,minmax(0,1fr))}}
.chiffre{background:var(--carte);border:1px solid var(--trait);border-radius:12px;padding:18px}
.chiffre b{display:block;font-size:2rem;line-height:1.1;color:var(--chaud);font-variant-numeric:tabular-nums;margin-bottom:8px}
.chiffre span{color:var(--discret);font-size:.95rem}
.galerie{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(170px,1fr))}
.galerie figure{margin:0;background:var(--carte);border:1px solid var(--trait);border-radius:12px;overflow:hidden}
.galerie img{width:100%;aspect-ratio:1/1;object-fit:contain;background:#fff;border-bottom:1px solid var(--trait)}
.galerie figcaption{padding:10px 12px 12px;font-size:.9rem}
.galerie figcaption small{display:block;color:var(--discret)}
.prix{display:flex;gap:14px;margin-top:10px;font-size:.92rem;color:var(--texte);font-variant-numeric:tabular-nums}
.prix b{color:var(--chaud)}
.methode{columns:2 320px;column-gap:40px;max-width:1000px}
.methode p{margin:0 0 12px;break-inside:avoid}
figure.pleine{margin:0}
figure.pleine img{border:1px solid var(--trait);border-radius:12px;background:#fff}
figcaption{color:var(--discret);font-size:.9rem;margin-top:6px}
footer{margin-top:64px;color:var(--discret);font-size:.9rem;border-top:1px solid var(--trait);padding-top:16px}
"""


def e(texte: str) -> str:
    """Échappe pour le HTML et pose des espaces insécables dans les guillemets français."""
    texte = re.sub(r"(\d) (\d{3})\b", "\\1\u202f\\2", texte)          # espace fine insécable dans les nombres
    return html.escape(texte).replace("« ", "«&nbsp;").replace(" »", "&nbsp;»").replace(" :", "&nbsp;:").replace(" ;", "&nbsp;;").replace(" ?", "&nbsp;?")


def lien_rapport(chemin: str) -> str:
    return f"{DEPOT}/blob/main/{chemin}" if DEPOT else f"../{chemin}"


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "figures").mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")
    for src, dst in PAGES:
        s = RACINE / src
        if s.exists():
            shutil.copyfile(s, DOCS / dst)
        else:
            print("absent, non copié :", src)
    for src, dst in FIGURES:
        s = RACINE / src
        if s.exists():
            shutil.copyfile(s, DOCS / "figures" / dst)
        else:
            print("absent, non copié :", src)
    manquants = [f for f in ["banniere.png", "hero_scene.jpg"] + [m[1] for m in MODES] if not (DOCS / "figures" / f).exists()]
    if manquants:
        print("visuels manquants (lancer construire_visuels.py) :", manquants)

    cartes_modes = "\n".join(
        f'<a class="carte" href="simulateur.html#mode={cle}"><img class="capture" src="figures/{img.replace(".png", "_vue.png")}" alt="{e(alt)}" loading="lazy" width="860" height="632">'
        f'<div class="corps"><span class="numero">MODE {i}</span><strong>{e(titre)}</strong><span>{e(texte)}</span></div></a>'
        for i, (cle, img, titre, texte, alt) in enumerate(MODES, 1))
    chiffres = "\n".join(f'<div class="chiffre"><b>{e(v)}</b><span>{e(t)}</span></div>' for v, t in CHIFFRES)
    galerie = "\n".join(
        f'<figure><img src="figures/documents/{f}" alt="{e(t)}" loading="lazy"><figcaption>{e(t)}<small>{e(s)}</small></figcaption></figure>'
        for f, t, s in DOCUMENTS if (DOCS / "figures" / "documents" / f).exists())
    constructions = "\n".join(
        f'<div class="carte"><div class="corps"><span class="numero">CONSTRUCTION {l}</span><strong>{e(t)}</strong><span>{e(d)}</span>'
        f'<div class="prix"><span><b>{e(prix)}</b></span><span>{e(duree)}</span></div></div></div>'
        for l, t, d, prix, duree in CONSTRUCTIONS)
    cartes_rapports = "\n".join(
        f'<a class="carte" href="{html.escape(lien_rapport(c))}"><div class="corps"><strong>{e(t)}</strong><span>{e(d)}</span></div></a>'
        for c, t, d in RAPPORTS if (RACINE / c).exists())
    guide = html.escape(lien_rapport("10_machine_optimisee/GUIDE_CONSTRUCTION.md"))
    inventaire = html.escape(lien_rapport("01_archive/INVENTAIRE.md"))
    titre = "C204 — la « machine temporelle » de John Titor, démontée par la physique"
    description = ("Simulateur 3D jouable, reconstitution des documents de 2000-2001, calculs, simulations et guide de "
                   "construction : une étude critique de la machine C204 attribuée à John Titor.")
    og = ""
    if SITE:
        og = (f'<meta property="og:type" content="website"><meta property="og:url" content="{SITE}">'
              f'<meta property="og:title" content="{html.escape(titre)}"><meta property="og:description" content="{html.escape(description)}">'
              f'<meta property="og:image" content="{SITE}figures/banniere.png"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="640">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}figures/banniere.png">'
              f'<link rel="canonical" href="{SITE}">')
    bouton_depot = f'<a class="bouton" href="{html.escape(DEPOT)}">Voir le dépôt GitHub</a>' if DEPOT else ""
    page = f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titre)}</title>
<meta name="description" content="{html.escape(description)}">
{og}
<style>{CSS}</style></head><body>
<header class="hero"><div class="hero-in">
<div>
<p class="surtitre">Étude critique · simulateur 3D · dossier ouvert</p>
<h1>La «&nbsp;machine temporelle&nbsp;» de John Titor, <em>démontée par la physique</em></h1>
<p class="chapeau">En novembre 2000, un inconnu se disant venu de 2036 publie sur des forums les photos et le manuel de sa machine, la C204. Nous avons pris ces documents au sérieux, juste le temps de les démonter&nbsp;: reconstitution en 3D, calculs, simulations, et ce que l'on pourrait vraiment construire.</p>
<p class="actions"><a class="bouton plein" href="simulateur.html#mode=recit">Lancer le simulateur 3D</a>{bouton_depot}</p>
</div>
<img class="hero-img" src="figures/hero_scene.jpg" width="1400" height="1022" alt="Vue 3D : un pick-up schématique portant l'unité, entouré des anneaux et du cône dessinés dans le manuel d'origine">
</div></header>
<main>
<p class="avert">Rien de ce qu'affirment les documents d'origine n'est tenu pour vrai. Les vues «&nbsp;si elle fonctionnait&nbsp;» mettent un récit en images&nbsp;; elles ne correspondent à aucun phénomène observé. Aucune expérience n'a été réalisée&nbsp;: tout ici est reconstitution, calcul et simulation.</p>

<section aria-labelledby="t-modes">
<h2 id="t-modes">Quatre façons d'explorer</h2>
<p class="sous-titre">Le simulateur tourne dans le navigateur, sans rien installer. Chaque carte ouvre directement le mode correspondant.</p>
<div class="grille deux">
{cartes_modes}
</div>
</section>

<section aria-labelledby="t-chiffres">
<h2 id="t-chiffres">Les chiffres qui fâchent</h2>
<p class="sous-titre">Les nombres du récit, pris au pied de la lettre et passés au calcul. Chaque valeur est recalculée par un script du dépôt.</p>
<div class="chiffres">
{chiffres}
</div>
</section>

<section aria-labelledby="t-docs">
<h2 id="t-docs">Les pièces du dossier</h2>
<p class="sous-titre">Six des vingt-deux documents inventoriés. Ce sont des images anonymes diffusées sur des forums en 2000-2001, reproduites ici pour les analyser. Leur provenance et leurs empreintes sont dans <a href="{inventaire}">l'inventaire</a>.</p>
<div class="galerie">
{galerie}
</div>
</section>

<section aria-labelledby="t-modele">
<h2 id="t-modele">Du document au modèle</h2>
<p class="sous-titre">Chaque pièce du modèle 3D porte son niveau de preuve&nbsp;: lue sur un document, déduite, ou supposée. Rien n'est documenté sous la platine supérieure&nbsp;; l'intérieur est donc une hypothèse, et le modèle le dit.</p>
<figure class="pleine"><img src="figures/comparaison_document_modele.png" alt="À gauche la page de manuel d'origine, à droite le modèle 3D vu du même point" loading="lazy"><figcaption>La page de manuel et le modèle reconstitué, vus du même point. <a href="visionneuse.html">Ouvrir la visionneuse pièce par pièce</a></figcaption></figure>
</section>

<section aria-labelledby="t-construire">
<h2 id="t-construire">Ce qu'on peut vraiment construire</h2>
<p class="sous-titre">Pas une machine à voyager dans le temps&nbsp;: un instrument de mesure dans le même coffre. Coûts et durées sont des estimations sans devis, et rien n'a été construit par nous. <a href="{guide}">Lire le guide de construction</a></p>
<div class="grille">
{constructions}
</div>
</section>

<section aria-labelledby="t-rapports">
<h2 id="t-rapports">Tout le dossier</h2>
<p class="sous-titre">Douze rapports, leurs scripts et leurs données. Tout se relance depuis le dépôt.</p>
<div class="grille">
{cartes_rapports}
</div>
</section>

<section aria-labelledby="t-methode">
<h2 id="t-methode">Méthode et limites</h2>
<div class="methode">
<p><strong>Comment c'est fait.</strong> Huit équipes d'agents d'IA spécialisées, pilotées avec Claude Code&nbsp;: archives, physique théorique, ingénierie, simulation, modèle 3D, expériences, littérature récente, machine optimisée. Une neuvième, la Red Team, n'avait qu'une mission&nbsp;: démolir le travail des autres.</p>
<p><strong>Ce que la Red Team a trouvé.</strong> 58 erreurs ou conclusions trop fortes dans notre propre dossier, toutes corrigées. Chaque rapport se termine par son journal de corrections.</p>
<p><strong>Ce qui est vérifié.</strong> Les calculs se relancent à l'identique. 446 références ont été contrôlées en ligne, sur leurs métadonnées et leurs résumés, pas sur leur texte intégral.</p>
<p><strong>Ce qui ne l'est pas.</strong> Aucune expérience n'a été réalisée et rien n'a été construit. Les simulations sont illustratives. L'échelle du coffre repose sur des étalons supposés.</p>
<p><strong>Ce qu'on ne sait pas.</strong> Qui était l'auteur, d'où vient l'écorché à 35 repères, et comment la photo du «&nbsp;laser courbé&nbsp;» a été faite.</p>
<p><strong>Ce qu'on ne prétend pas.</strong> Des passionnés ont épluché ces images dès 2003. Ce dossier fait le tour complet, de l'archive jusqu'au simulateur, et montre ses sources.</p>
</div>
</section>

<footer>Programme C204 — étude critique. {f'<a href="{html.escape(DEPOT)}">Dépôt GitHub</a> · ' if DEPOT else ''}<a href="simulateur.html">Simulateur</a> · <a href="visionneuse.html">Visionneuse</a></footer>
</main></body></html>
"""
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    print("docs/index.html écrit ; dépôt :", DEPOT or "(liens relatifs)", "; site :", SITE or "(inconnu)")


if __name__ == "__main__":
    main()
