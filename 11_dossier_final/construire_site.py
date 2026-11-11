"""Construit le dossier docs/ (site statique servi par GitHub Pages) à partir des livrables.

Usage, depuis la racine du projet :
    .venv/bin/python 11_dossier_final/construire_visuels.py          # bannière, captures, documents
    .venv/bin/python 11_dossier_final/construire_site.py [URL_DU_DEPOT]

- copie le simulateur et la visionneuse (fichiers HTML autonomes) ;
- copie quelques figures ;
- écrit la page d'exploration en deux langues : docs/index.html (français) et docs/en/index.html (anglais),
  reliées par un sélecteur de langue en haut de page.
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
MODES = ["explorer", "recit", "physique", "r1"]
DOCS_IMAGES = ["doc003_photo_vehicule.jpg", "doc004_unite_ouverte.jpg", "doc007_vue_de_dessus.jpg",
               "doc008_composants.jpg", "doc009_champ.jpg", "doc005_ecorche.jpg"]
RAPPORTS = ["11_dossier_final/DOSSIER_SCIENTIFIQUE_C204.md", "10_machine_optimisee/GUIDE_CONSTRUCTION.md",
            "01_archive/INVENTAIRE.md", "01_archive/HISTORIQUE.md", "02_reconstruction/DOSSIER_TECHNIQUE.md",
            "03_physique_theorique/RAPPORT_B.md", "04_ingenierie/RAPPORT_C.md", "05_simulations/RAPPORT_D.md",
            "07_experiences/RAPPORT_F.md", "08_red_team/RAPPORT_RED_TEAM_2.md",
            "09_recherche_contemporaine/RAPPORT_H.md", "10_machine_optimisee/RAPPORT_I.md"]

T = {
    "fr": {
        "titre": "C204 — la « machine temporelle » de John Titor, démontée par la physique",
        "description": "Simulateur 3D jouable, reconstitution des documents de 2000-2001, calculs, simulations et guide de construction : une étude critique de la machine C204 attribuée à John Titor.",
        "surtitre": "Étude critique · simulateur 3D · dossier ouvert",
        "h1": "La « machine temporelle » de John Titor, <em>démontée par la physique</em>",
        "chapeau": "En novembre 2000, un inconnu se disant venu de 2036 publie sur des forums les photos et le manuel de sa machine, la C204. Nous avons pris ces documents au sérieux, juste le temps de les démonter : reconstitution en 3D, calculs, simulations, et ce que l'on pourrait vraiment construire.",
        "bouton_sim": "Lancer le simulateur 3D", "bouton_depot": "Voir le dépôt GitHub",
        "alt_hero": "Vue 3D : un pick-up schématique portant l'unité, entouré des anneaux et du cône dessinés dans le manuel d'origine",
        "avert": "Rien de ce qu'affirment les documents d'origine n'est tenu pour vrai. Les vues « si elle fonctionnait » mettent un récit en images ; elles ne correspondent à aucun phénomène observé. Aucune expérience n'a été réalisée : tout ici est reconstitution, calcul et simulation.",
        "h_modes": "Quatre façons d'explorer",
        "s_modes": "Le simulateur tourne dans le navigateur, sans rien installer. Chaque carte ouvre directement le mode correspondant.",
        "mode": "MODE",
        "modes": [
            ("Explorer la machine", "Ouvrez le coffre, faites glisser le curseur de vue éclatée, cliquez une pièce pour savoir d'où elle vient.", "La C204 en vue éclatée, chaque sous-ensemble étiqueté"),
            ("Si elle fonctionnait", "Le récit mis en images, étape par étape : montée en puissance, « champ », lumière courbée, noir complet.", "Un pick-up schématique entouré des anneaux du schéma d'origine"),
            ("Ce que dit la physique", "Bougez deux curseurs et lisez la masse, la pesanteur, la dose et la température réellement impliquées.", "La même scène avec les zones de dose létale et les résultats chiffrés"),
            ("La version constructible", "Quatre horloges, trois calculateurs qui votent, un compteur de muons. Injectez une panne pour voir.", "Le coffre du palier R1 avec ses composants réels"),
        ],
        "h_chiffres": "Les chiffres qui fâchent",
        "s_chiffres": "Les nombres du récit, pris au pied de la lettre et passés au calcul. Chaque valeur est recalculée par un script du dépôt.",
        "chiffres": [
            ("227 kg", "la masse annoncée de l'unité"),
            ("4 à 5 Gt", "la masse de chaque « singularité » qu'exigent les 300 à 500 MW annoncés : des milliards de tonnes"),
            ("≈ 1 ms", "le temps pour recevoir une dose létale à un mètre, d'après ces mêmes chiffres"),
            ("87 660", "le facteur de « dix ans par heure ». Les électrons du LEP, au CERN, l'atteignaient presque : 89 000"),
            ("0,5 ns/h", "ce que gagne réellement la version constructible à 130 km/h vers l'est. Un sac de sable ferait pareil"),
            ("58", "erreurs trouvées par notre Red Team dans notre propre travail, corrigées et journalisées"),
        ],
        "h_docs": "Les pièces du dossier",
        "s_docs": "Six des vingt-deux documents inventoriés. Ce sont des images anonymes diffusées sur des forums en 2000-2001, reproduites ici pour les analyser. Leur provenance et leurs empreintes sont dans <a href=\"{inventaire}\">l'inventaire</a>.",
        "docs": [
            ("L'unité photographiée dans un véhicule", "Photo de 2001"),
            ("L'unité ouverte et sa télécommande", "Page de manuel"),
            ("Vue de dessus : « main » et « steering singularity »", "Page de manuel"),
            ("Les douze « composants de base »", "Page de manuel"),
            ("Le « champ sinusoïde de Tipler »", "Page de manuel"),
            ("L'écorché à 35 repères, sans légende", "Origine inconnue"),
        ],
        "h_modele": "Du document au modèle",
        "s_modele": "Chaque pièce du modèle 3D porte son niveau de preuve : lue sur un document, déduite, ou supposée. Rien n'est documenté sous la platine supérieure ; l'intérieur est donc une hypothèse, et le modèle le dit.",
        "alt_modele": "À gauche la page de manuel d'origine, à droite le modèle 3D vu du même point",
        "leg_modele": "La page de manuel et le modèle reconstitué, vus du même point.",
        "lien_visionneuse": "Ouvrir la visionneuse pièce par pièce",
        "h_construire": "Ce qu'on peut vraiment construire",
        "s_construire": "Pas une machine à voyager dans le temps : un instrument de mesure dans le même coffre. Coûts et durées sont des estimations sans devis, et rien n'a été construit par nous. <a href=\"{guide}\">Lire le guide de construction</a>",
        "construction": "CONSTRUCTION",
        "constructions": [
            ("Réplique inerte", "Le coffre tel que documenté, en maquette de présentation.", "140 à 240 €", "15 à 25 h"),
            ("C204-R1 Lite", "Version d'initiation : références de temps comparées, trois calculateurs à vote, compteur de muons.", "350 à 730 €", "40 à 80 h"),
            ("C204-R1 complet", "Quatre horloges atomiques miniatures, gyromètre à fibre optique, dans le même coffre.", "≈ 49 k€", "300 à 600 h"),
        ],
        "h_rapports": "Tout le dossier",
        "s_rapports": "Douze rapports, leurs scripts et leurs données. Tout se relance depuis le dépôt.",
        "rapports": [
            ("Synthèse du programme", "Les treize livrables, les dix questions, les limites"),
            ("Guide de construction", "Réplique inerte, version d'initiation, palier R1 complet"),
            ("Inventaire des documents", "Les 22 pièces, leur provenance, leur attribution"),
            ("Historique", "Chronologie 2000-2001 et diffusion ultérieure"),
            ("Dossier technique", "L'objet tel que décrit, plans, dimensions"),
            ("Physique théorique", "Kerr, Tipler, micro-trous noirs, causalité"),
            ("Ingénierie", "Sous-système par sous-système : constructible ou non"),
            ("Simulations", "Neuf simulations reproductibles"),
            ("Expériences", "Douze protocoles sans danger"),
            ("Critique de notre propre travail", "Validation contradictoire et corrections"),
            ("Recherche contemporaine", "Littérature 2001-2026, bibliographie vérifiée"),
            ("Machine optimisée", "Trois paliers de machine cohérente"),
        ],
        "h_methode": "Méthode et limites",
        "methode": [
            ("Comment c'est fait.", "Huit équipes d'agents d'IA spécialisées, pilotées avec Claude Code : archives, physique théorique, ingénierie, simulation, modèle 3D, expériences, littérature récente, machine optimisée. Une neuvième, la Red Team, n'avait qu'une mission : démolir le travail des autres."),
            ("Ce que la Red Team a trouvé.", "58 erreurs ou conclusions trop fortes dans notre propre dossier, toutes corrigées. Chaque rapport se termine par son journal de corrections."),
            ("Ce qui est vérifié.", "Les calculs se relancent à l'identique. 446 références ont été contrôlées en ligne, sur leurs métadonnées et leurs résumés, pas sur leur texte intégral."),
            ("Ce qui ne l'est pas.", "Aucune expérience n'a été réalisée et rien n'a été construit. Les simulations sont illustratives. L'échelle du coffre repose sur des étalons supposés."),
            ("Ce qu'on ne sait pas.", "Qui était l'auteur, d'où vient l'écorché à 35 repères, et comment la photo du « laser courbé » a été faite."),
            ("Ce qu'on ne prétend pas.", "Des passionnés ont épluché ces images dès 2003. Ce dossier fait le tour complet, de l'archive jusqu'au simulateur, et montre ses sources."),
        ],
        "pied": "Programme C204 — étude critique.", "depot": "Dépôt GitHub", "simulateur": "Simulateur", "visionneuse": "Visionneuse",
        "nav_langue": "Langue",
    },
    "en": {
        "titre": "C204 — John Titor's “time machine”, taken apart by physics",
        "description": "A playable 3D simulator, a reconstruction of the 2000–2001 documents, calculations, simulations and a build guide: a critical study of the C204 machine attributed to John Titor.",
        "surtitre": "Critical study · 3D simulator · open dossier",
        "h1": "John Titor's “time machine”, <em>taken apart by physics</em>",
        "chapeau": "In November 2000 an anonymous poster claiming to come from 2036 published photos and manual pages of his machine, the C204. We took those documents at face value, just long enough to take them apart: a 3D reconstruction, calculations, simulations, and what could actually be built.",
        "bouton_sim": "Launch the 3D simulator", "bouton_depot": "View the GitHub repository",
        "alt_hero": "3D view: a schematic pickup truck carrying the unit, surrounded by the rings and cone drawn in the original manual",
        "avert": "Nothing claimed in the original documents is taken as true. The “if it worked” views put a story into pictures; they do not correspond to any observed phenomenon. No experiment was run: everything here is reconstruction, calculation and simulation.",
        "h_modes": "Four ways to explore",
        "s_modes": "The simulator runs in the browser, nothing to install. Each card opens the matching mode directly.",
        "mode": "MODE",
        "modes": [
            ("Explore the machine", "Open the case, drag the exploded-view slider, click a part to see where it comes from.", "The C204 in exploded view, each sub-assembly labelled"),
            ("If it worked", "The story in pictures, step by step: power-up, “field”, bent light, total darkness.", "A schematic pickup truck surrounded by the rings of the original diagram"),
            ("What physics says", "Move two sliders and read the mass, gravity, dose and temperature those figures really imply.", "The same scene with lethal-dose zones and computed results"),
            ("The buildable version", "Four clocks, three voting computers, a muon counter. Inject a fault and watch.", "The R1 case with its real components"),
        ],
        "h_chiffres": "The numbers that don't add up",
        "s_chiffres": "The story's own figures, taken literally and run through the calculations. Every value is recomputed by a script in the repository.",
        "chiffres": [
            ("500 lb", "the stated mass of the unit (227 kg)"),
            ("4–5 Gt", "the mass of each “singularity” required by the stated 300–500 MW: billions of tonnes"),
            ("≈ 1 ms", "the time to receive a lethal dose at one metre, according to those same figures"),
            ("87,660", "the factor behind “ten years per hour”. LEP's electrons at CERN nearly reached it: 89,000"),
            ("0.5 ns/h", "what the buildable version really gains at 130 km/h heading east. A sandbag would do the same"),
            ("58", "errors our red team found in our own work, all fixed and logged"),
        ],
        "h_docs": "The exhibits",
        "s_docs": "Six of the twenty-two inventoried documents. These are anonymous images circulated on forums in 2000–2001, reproduced here for analysis. Their provenance and hashes are in <a href=\"{inventaire}\">the inventory</a> (in French).",
        "docs": [
            ("The unit photographed in a vehicle", "2001 photo"),
            ("The unit open, with its remote control", "Manual page"),
            ("Top view: “main” and “steering singularity”", "Manual page"),
            ("The twelve “basic components”", "Manual page"),
            ("The “Tipler sinusoid field”", "Manual page"),
            ("The 35-callout cutaway, no legend", "Origin unknown"),
        ],
        "h_modele": "From document to model",
        "s_modele": "Every part of the 3D model carries its level of evidence: read on a document, deduced, or assumed. Nothing is documented below the top plate, so the interior is a hypothesis, and the model says so.",
        "alt_modele": "Left, the original manual page; right, the 3D model seen from the same viewpoint",
        "leg_modele": "The manual page and the reconstructed model, seen from the same viewpoint.",
        "lien_visionneuse": "Open the part-by-part viewer (in French)",
        "h_construire": "What can actually be built",
        "s_construire": "Not a time machine: a measuring instrument in the same case. Costs and durations are estimates without quotes, and we have built none of it. <a href=\"{guide}\">Read the build guide</a> (in French)",
        "construction": "BUILD",
        "constructions": [
            ("Inert replica", "The case as documented, as a display model.", "€140–240", "15–25 h"),
            ("C204-R1 Lite", "Entry-level version: time references compared, three voting computers, a muon counter.", "€350–730", "40–80 h"),
            ("Full C204-R1", "Four chip-scale atomic clocks and a fibre-optic gyroscope, in the same case.", "≈ €49k", "300–600 h"),
        ],
        "h_rapports": "The full dossier",
        "s_rapports": "Twelve reports with their scripts and data. The reports are in French; a summary in English is linked first. Everything can be re-run from the repository.",
        "rapports": [
            ("Programme synthesis", "The thirteen deliverables, the ten questions, the limits"),
            ("Build guide", "Inert replica, entry-level version, full R1"),
            ("Document inventory", "The 22 exhibits, their provenance and attribution"),
            ("History", "Timeline of 2000–2001 and later circulation"),
            ("Technical file", "The object as described, drawings, dimensions"),
            ("Theoretical physics", "Kerr, Tipler, micro black holes, causality"),
            ("Engineering", "Subsystem by subsystem: buildable or not"),
            ("Simulations", "Nine reproducible simulations"),
            ("Experiments", "Twelve safe protocols"),
            ("Criticism of our own work", "Adversarial validation and corrections"),
            ("Contemporary research", "Literature 2001–2026, verified bibliography"),
            ("Optimised machine", "Three tiers of a coherent machine"),
        ],
        "h_methode": "Method and limits",
        "methode": [
            ("How it was made.", "Eight specialised AI agent teams, driven with Claude Code: archives, theoretical physics, engineering, simulation, 3D model, experiments, recent literature, optimised machine. A ninth, the red team, had one job: tear the others' work apart."),
            ("What the red team found.", "58 errors or overstated conclusions in our own dossier, all fixed. Each report ends with its correction log."),
            ("What is verified.", "The calculations re-run identically. 446 references were checked online, from their metadata and abstracts, not their full text."),
            ("What is not.", "No experiment was run and nothing was built. The simulations are illustrative. The scale of the case rests on assumed reference objects."),
            ("What we do not know.", "Who the author was, where the 35-callout cutaway comes from, and how the “bent laser” photo was made."),
            ("What we do not claim.", "Enthusiasts were already poring over these images in 2003. This dossier covers the whole path, from the archive to the simulator, and shows its sources."),
        ],
        "pied": "C204 programme — a critical study.", "depot": "GitHub repository", "simulateur": "Simulator", "visionneuse": "Viewer (in French)",
        "nav_langue": "Language",
    },
}

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
.langues{max-width:1180px;margin:0 auto;padding:14px 16px 0;display:flex;justify-content:flex-end;gap:6px}
.langues a{padding:6px 12px;border-radius:999px;border:1px solid #3a4250;color:var(--nuit-discret);text-decoration:none;font-size:.86rem;font-weight:600}
.langues a:hover,.langues a:focus-visible{border-color:var(--nuit-accent);color:var(--nuit-texte);outline:none}
.langues a[aria-current="page"]{background:var(--nuit-texte);border-color:var(--nuit-texte);color:var(--nuit)}
.hero-in{max-width:1180px;margin:0 auto;padding:32px 16px 0;display:grid;gap:8px 40px;grid-template-columns:minmax(0,1fr);align-items:center}
@media (min-width:920px){.hero-in{grid-template-columns:minmax(0,5fr) minmax(0,6fr);padding-top:44px}}
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
.etiquette-langue{font-size:.78rem;color:var(--discret);border:1px solid var(--trait);border-radius:999px;padding:1px 8px;margin-left:6px;white-space:nowrap}
footer{margin-top:64px;color:var(--discret);font-size:.9rem;border-top:1px solid var(--trait);padding-top:16px}
"""


def e(texte: str, lang: str) -> str:
    """Échappe pour le HTML ; en français, pose les espaces insécables de la typographie."""
    if lang == "fr":
        texte = re.sub(r"(\d) (\d{3})\b", "\\1\u202f\\2", texte)          # espace fine insécable dans les nombres
        return (html.escape(texte, quote=False).replace("« ", "«&nbsp;").replace(" »", "&nbsp;»")
                .replace(" :", "&nbsp;:").replace(" ;", "&nbsp;;").replace(" ?", "&nbsp;?"))
    return html.escape(texte, quote=False)


def lien_rapport(chemin: str, lang: str) -> str:
    return f"{DEPOT}/blob/main/{chemin}" if DEPOT else ("../" if lang == "fr" else "../../") + chemin


def page(lang: str) -> str:
    t = T[lang]
    base = "" if lang == "fr" else "../"                     # préfixe vers la racine du site
    sim = f"{base}simulateur.html"
    frag_lang = "" if lang == "fr" else "&lang=en"
    suffixe_img = "_en" if lang == "en" and all((DOCS / "figures" / f"mode_{m}_vue_en.png").exists() for m in MODES) else ""
    url_fr, url_en = (f"{SITE}", f"{SITE}en/") if SITE else ("../" if lang == "en" else "./", "en/" if lang == "fr" else "./")
    rel_fr, rel_en = ("./", "en/") if lang == "fr" else ("../", "./")

    cartes_modes = "\n".join(
        f'<a class="carte" href="{sim}#mode={cle}{frag_lang}"><img class="capture" src="{base}figures/mode_{cle}_vue{suffixe_img}.png" alt="{html.escape(alt)}" loading="lazy" width="860" height="632">'
        f'<div class="corps"><span class="numero">{t["mode"]} {i}</span><strong>{e(titre, lang)}</strong><span>{e(texte, lang)}</span></div></a>'
        for i, (cle, (titre, texte, alt)) in enumerate(zip(MODES, t["modes"]), 1))
    chiffres = "\n".join(f'<div class="chiffre"><b>{e(v, lang)}</b><span>{e(x, lang)}</span></div>' for v, x in t["chiffres"])
    galerie = "\n".join(
        f'<figure><img src="{base}figures/documents/{f}" alt="{html.escape(titre)}" loading="lazy"><figcaption>{e(titre, lang)}<small>{e(sous, lang)}</small></figcaption></figure>'
        for f, (titre, sous) in zip(DOCS_IMAGES, t["docs"]) if (DOCS / "figures" / "documents" / f).exists())
    constructions = "\n".join(
        f'<div class="carte"><div class="corps"><span class="numero">{t["construction"]} {lettre}</span><strong>{e(titre, lang)}</strong><span>{e(texte, lang)}</span>'
        f'<div class="prix"><span><b>{e(prix, lang)}</b></span><span>{e(duree, lang)}</span></div></div></div>'
        for lettre, (titre, texte, prix, duree) in zip("ABC", t["constructions"]))
    rapports = []
    if lang == "en" and (RACINE / "11_dossier_final/SUMMARY_EN.md").exists():
        rapports.append(f'<a class="carte" href="{html.escape(lien_rapport("11_dossier_final/SUMMARY_EN.md", lang))}"><div class="corps"><strong>Summary in English</strong><span>The verdict, the ten questions, the limits</span></div></a>')
    for chemin, (titre, texte) in zip(RAPPORTS, t["rapports"]):
        if (RACINE / chemin).exists():
            marque = ' <span class="etiquette-langue">in French</span>' if lang == "en" else ""
            rapports.append(f'<a class="carte" href="{html.escape(lien_rapport(chemin, lang))}"><div class="corps"><strong>{e(titre, lang)}{marque}</strong><span>{e(texte, lang)}</span></div></a>')
    methode = "\n".join(f"<p><strong>{e(a, lang)}</strong> {e(b, lang)}</p>" for a, b in t["methode"])
    guide = html.escape(lien_rapport("10_machine_optimisee/GUIDE_CONSTRUCTION.md", lang))
    inventaire = html.escape(lien_rapport("01_archive/INVENTAIRE.md", lang))
    og = ""
    if SITE:
        url = url_fr if lang == "fr" else url_en
        og = (f'<meta property="og:type" content="website"><meta property="og:url" content="{url}">'
              f'<meta property="og:title" content="{html.escape(t["titre"])}"><meta property="og:description" content="{html.escape(t["description"])}">'
              f'<meta property="og:locale" content="{"fr_FR" if lang == "fr" else "en_GB"}">'
              f'<meta property="og:image" content="{SITE}figures/banniere.png"><meta property="og:image:width" content="1280"><meta property="og:image:height" content="640">'
              f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}figures/banniere.png">'
              f'<link rel="canonical" href="{url}"><link rel="alternate" hreflang="fr" href="{url_fr}"><link rel="alternate" hreflang="en" href="{url_en}"><link rel="alternate" hreflang="x-default" href="{url_en}">')
    bouton_depot = f'<a class="bouton" href="{html.escape(DEPOT)}">{t["bouton_depot"]}</a>' if DEPOT else ""
    cur_fr = ' aria-current="page"' if lang == "fr" else ""
    cur_en = ' aria-current="page"' if lang == "en" else ""
    h1 = t["h1"].replace("« ", "«&nbsp;").replace(" »", "&nbsp;»")
    pied_depot = f'<a href="{html.escape(DEPOT)}">{t["depot"]}</a> · ' if DEPOT else ""
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(t["titre"])}</title>
<meta name="description" content="{html.escape(t["description"])}">
{og}
<style>{CSS}</style></head><body>
<header class="hero">
<nav class="langues" aria-label="{t["nav_langue"]}"><a href="{rel_fr}" lang="fr" hreflang="fr"{cur_fr}>Français</a><a href="{rel_en}" lang="en" hreflang="en"{cur_en}>English</a></nav>
<div class="hero-in">
<div>
<p class="surtitre">{e(t["surtitre"], lang)}</p>
<h1>{h1}</h1>
<p class="chapeau">{e(t["chapeau"], lang)}</p>
<p class="actions"><a class="bouton plein" href="{sim}#mode=recit{frag_lang}">{t["bouton_sim"]}</a>{bouton_depot}</p>
</div>
<img class="hero-img" src="{base}figures/hero_scene.jpg" width="1400" height="1022" alt="{html.escape(t["alt_hero"])}">
</div></header>
<main>
<p class="avert">{e(t["avert"], lang)}</p>

<section aria-labelledby="t-modes">
<h2 id="t-modes">{e(t["h_modes"], lang)}</h2>
<p class="sous-titre">{e(t["s_modes"], lang)}</p>
<div class="grille deux">
{cartes_modes}
</div>
</section>

<section aria-labelledby="t-chiffres">
<h2 id="t-chiffres">{e(t["h_chiffres"], lang)}</h2>
<p class="sous-titre">{e(t["s_chiffres"], lang)}</p>
<div class="chiffres">
{chiffres}
</div>
</section>

<section aria-labelledby="t-docs">
<h2 id="t-docs">{e(t["h_docs"], lang)}</h2>
<p class="sous-titre">{t["s_docs"].format(inventaire=inventaire)}</p>
<div class="galerie">
{galerie}
</div>
</section>

<section aria-labelledby="t-modele">
<h2 id="t-modele">{e(t["h_modele"], lang)}</h2>
<p class="sous-titre">{e(t["s_modele"], lang)}</p>
<figure class="pleine"><img src="{base}figures/comparaison_document_modele.png" alt="{html.escape(t["alt_modele"])}" loading="lazy"><figcaption>{e(t["leg_modele"], lang)} <a href="{base}visionneuse.html">{t["lien_visionneuse"]}</a></figcaption></figure>
</section>

<section aria-labelledby="t-construire">
<h2 id="t-construire">{e(t["h_construire"], lang)}</h2>
<p class="sous-titre">{t["s_construire"].format(guide=guide)}</p>
<div class="grille">
{constructions}
</div>
</section>

<section aria-labelledby="t-rapports">
<h2 id="t-rapports">{e(t["h_rapports"], lang)}</h2>
<p class="sous-titre">{e(t["s_rapports"], lang)}</p>
<div class="grille">
{chr(10).join(rapports)}
</div>
</section>

<section aria-labelledby="t-methode">
<h2 id="t-methode">{e(t["h_methode"], lang)}</h2>
<div class="methode">
{methode}
</div>
</section>

<footer>{e(t["pied"], lang)} {pied_depot}<a href="{sim}{"#lang=en" if lang == "en" else ""}">{t["simulateur"]}</a> · <a href="{base}visionneuse.html">{t["visionneuse"]}</a></footer>
</main></body></html>
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "figures").mkdir(exist_ok=True)
    (DOCS / "en").mkdir(exist_ok=True)
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
    attendus = ["banniere.png", "hero_scene.jpg"] + [f"mode_{m}_vue.png" for m in MODES]
    manquants = [f for f in attendus if not (DOCS / "figures" / f).exists()]
    if manquants:
        print("visuels manquants (lancer construire_visuels.py) :", manquants)
    (DOCS / "index.html").write_text(page("fr"), encoding="utf-8")
    (DOCS / "en" / "index.html").write_text(page("en"), encoding="utf-8")
    print("docs/index.html et docs/en/index.html écrits ; dépôt :", DEPOT or "(liens relatifs)", "; site :", SITE or "(inconnu)")


if __name__ == "__main__":
    main()
