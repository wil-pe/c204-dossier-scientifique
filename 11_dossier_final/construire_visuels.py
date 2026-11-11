"""Fabrique les visuels du site et du README : bannière, captures des quatre modes, documents d'origine.

Usage, depuis la racine du projet :
    .venv/bin/python 11_dossier_final/construire_visuels.py

La bannière (1280×640) sert d'image d'en-tête du README, d'image de partage (Open Graph) du site,
et peut être téléversée comme « Social preview » dans les réglages du dépôt GitHub.
Polices : celles du système (macOS) si elles existent, sinon la police par défaut de Pillow.

Le fond de la bannière est une capture du simulateur sans ses étiquettes, obtenue ainsi :
  1. copier 06_modele_3D/simulateur.html en ajoutant dans <head> :
         <style>#etiquettes,#traits{display:none!important}</style>
  2. Chrome sans tête :
         chrome --headless=new --use-angle=swiftshader --enable-unsafe-swiftshader --hide-scrollbars \
                --window-size=1280,800 --force-device-scale-factor=2 --virtual-time-budget=9000 \
                --screenshot=scene.png "file://…/copie.html#mode=recit&theme=dark&t=0.43"
  3. ranger l'image dans 11_dossier_final/visuels_source/scene_recit_sombre_sans_etiquettes.png
"""
from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RACINE = Path(__file__).resolve().parent.parent
FIG = RACINE / "docs" / "figures"
RENDUS = RACINE / "06_modele_3D" / "rendus"
ORIG = RACINE / "01_archive" / "originaux"
SOURCE_SCENE = Path(__file__).resolve().parent / "visuels_source" / "scene_recit_sombre_sans_etiquettes.png"

MODES = {
    "mode_explorer.png": "simulateur_1280_1_explorer_eclate100.png",
    "mode_recit.png": "simulateur_1280_2_recit_champ.png",
    "mode_physique.png": "simulateur_1280_3_physique_A.png",
    "mode_r1.png": "simulateur_1280_4_r1_panne.png",
}
DOCUMENTS = {
    "doc004_unite_ouverte.jpg": "MT7013__c204unit_johntitor.jpg",
    "doc007_vue_de_dessus.jpg": "MT7016__timetravel_0_1.jpg",
    "doc008_composants.jpg": "MT7017__c204_unit_instructions.jpeg",
    "doc009_champ.jpg": "MT7018__singularities1.jpg",
    "doc005_ecorche.jpg": "MT7014__johntitor_schematic.jpg",
    "doc003_photo_vehicule.jpg": "MT7012__JT3.jpg",
}
FOND = (14, 17, 22)
BLANC = (240, 238, 233)
DISCRET = (160, 166, 176)
ACCENT = (111, 182, 224)
ORANGE = (229, 154, 102)


def police(taille: int, gras: bool = False):
    candidates = [("/System/Library/Fonts/HelveticaNeue.ttc", 1 if gras else 0),
                  ("/System/Library/Fonts/Helvetica.ttc", 1 if gras else 0),
                  ("/System/Library/Fonts/Supplemental/Arial Bold.ttf" if gras else "/System/Library/Fonts/Supplemental/Arial.ttf", 0)]
    for chemin, index in candidates:
        try:
            return ImageFont.truetype(chemin, taille, index=index)
        except OSError:
            continue
    return ImageFont.load_default()


def banniere() -> None:
    L, H = 1280, 640
    img = Image.new("RGB", (L, H), FOND)
    # Scène 3D du mode « récit » (thème sombre), capturée SANS étiquettes à 2560×1600 (voir l'en-tête du fichier),
    # recadrée sur la vue 3D et fondue dans le fond à gauche.
    src = Image.open(SOURCE_SCENE).convert("RGB")
    vue = src.crop((60, 290, 1720, 1475))                    # zone 3D, sans barres, pastilles ni légende
    echelle = H / vue.height
    vue = vue.resize((int(vue.width * echelle), H), Image.LANCZOS)
    x0 = L - vue.width + 100                                 # la marge droite de la scène est vide : on la laisse déborder
    masque = Image.new("L", vue.size, 255)
    d = ImageDraw.Draw(masque)
    fondu = 300
    for x in range(fondu):
        d.line([(x, 0), (x, H)], fill=int(255 * (x / fondu) ** 1.6))
    img.paste(vue, (x0, 0), masque)
    # Voile sombre sous le texte pour la lisibilité
    voile = Image.new("L", (L, H), 0)
    dv = ImageDraw.Draw(voile)
    for x in range(700):
        dv.line([(x, 0), (x, H)], fill=int(200 * (1 - x / 700) ** 1.2))
    img.paste(Image.new("RGB", (L, H), FOND), (0, 0), voile)

    d = ImageDraw.Draw(img)
    x = 64
    d.text((x, 54), "ÉTUDE CRITIQUE  ·  SIMULATEUR 3D  ·  DOSSIER OUVERT", font=police(19, True), fill=ACCENT)
    d.text((x - 6, 78), "C204", font=police(168, True), fill=BLANC)
    d.text((x, 298), "La « machine temporelle »", font=police(34), fill=BLANC)
    d.text((x, 340), "de John Titor,", font=police(34), fill=BLANC)
    largeur_debut = d.textlength("de John Titor, ", font=police(34))
    d.text((x + largeur_debut, 340), "démontée", font=police(34, True), fill=BLANC)
    d.text((x, 382), "par la physique.", font=police(34, True), fill=BLANC)
    # Trois chiffres
    y = 458
    for valeur, legende in (("227 kg", "annoncés"), ("5 milliards de t", "exigés par ses propres chiffres"), ("0,5 ns/h", "ce qu'on sait vraiment construire")):
        d.text((x, y), valeur, font=police(26, True), fill=ORANGE)
        largeur = d.textlength(valeur, font=police(26, True))
        d.text((x + largeur + 12, y + 5), legende, font=police(20), fill=DISCRET)
        y += 38
    d.text((x, H - 46), "wil-pe.github.io/c204-dossier-scientifique", font=police(18), fill=DISCRET)
    img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=40))
    img.save(FIG / "banniere.png", optimize=True)
    print("bannière :", (FIG / "banniere.png").stat().st_size // 1024, "ko")


def scene_hero() -> None:
    """Scène 3D seule (sans texte), pour l'en-tête de la page d'exploration."""
    src = Image.open(SOURCE_SCENE).convert("RGB")
    vue = src.crop((200, 330, 1720, 1440))
    vue = vue.resize((1400, int(vue.height * 1400 / vue.width)), Image.LANCZOS)
    vue.save(FIG / "hero_scene.jpg", quality=86, optimize=True, progressive=True)
    print("scène d'en-tête :", (FIG / "hero_scene.jpg").stat().st_size // 1024, "ko", vue.size)


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "documents").mkdir(exist_ok=True)
    banniere()
    scene_hero()
    for dst, src in MODES.items():
        shutil.copyfile(RENDUS / src, FIG / dst)
        # version recadrée sur la vue 3D seule, pour les cartes de la page d'exploration
        Image.open(RENDUS / src).convert("RGB").crop((0, 108, 860, 740)).save(FIG / dst.replace(".png", "_vue.png"), optimize=True)
    for dst, src in DOCUMENTS.items():
        shutil.copyfile(ORIG / src, FIG / "documents" / dst)
    print(len(MODES), "captures et", len(DOCUMENTS), "documents copiés dans docs/figures/")


if __name__ == "__main__":
    main()
