#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — rendus PNG du modèle (rendu LOGICIEL, sans GPU).

    modele_c204.json  ──►  rendus/*.png

Moteur : rastérisation par tampon de profondeur (z-buffer) écrite en numpy — occultation exacte,
ombrage plat à deux lumières, arêtes tracées par détection de contours dans l'image (identifiant de
pièce et normale), enveloppes translucides par « depth peeling » (3 couches), suréchantillonnage ×2.
matplotlib ne sert qu'à l'habillage (titres, repères, légende, échelle).

Les images sont ILLUSTRATIVES : elles montrent un objet tel qu'il est décrit par des documents non
authentifiés, à l'échelle hypothétique lue dans parametres.json (echelle.L).

Usage : python rendre_vues.py            (ou appelé par construire_modele.py)
"""
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

from construire_modele import maillage_piece, pieces_visibles, couleur_piece, hex_rgb

ICI = Path(__file__).resolve().parent
ARCHIVE = ICI.parent / "01_archive" / "originaux"
SORTIE = ICI / "rendus"
SSAA = 2
import json as _json
_L = _json.loads((ICI / "parametres.json").read_text(encoding="utf-8"))["echelle"]["L"]
ECHELLE_TXT = ("L = %.2f m ± %.2f m" % (_L["valeur"], _L["incertitude"])).replace(".", ",")
AVERT = "Reconstruction documentaire d'un objet DÉCRIT (documents non authentifiés) — rien n'atteste qu'il ait existé ni fonctionné. Échelle hypothétique : " + ECHELLE_TXT + " (estimation de l'Équipe A, confiance faible)."


# ------------------------------------------------------------------------------------------------
# Caméra
# ------------------------------------------------------------------------------------------------
class Camera:
    """Caméra définie par un œil et une base (droite, haut, avant). Orthographique (echelle en px/m)
    ou perspective (focale en px). Coordonnées d'écran en pixels de l'image finale."""

    def __init__(self, oeil, avant, haut, largeur, hauteur, focale=None, echelle=None, centre=None):
        self.oeil = np.asarray(oeil, float)
        f = np.asarray(avant, float)
        self.f = f / np.linalg.norm(f)
        r = np.cross(self.f, np.asarray(haut, float))
        self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)
        self.W, self.H = largeur, hauteur
        self.focale, self.echelle = focale, echelle
        self.cx, self.cy = centre if centre else (largeur / 2, hauteur / 2)

    def vers_camera(self, P):
        d = np.asarray(P, float) - self.oeil
        return d @ self.r, d @ self.u, d @ self.f

    def projeter(self, P):
        """→ (x écran, y écran, q) où q croît quand on se rapproche de l'œil (linéaire à l'écran)."""
        x, y, z = self.vers_camera(P)
        if self.focale:
            z = np.maximum(z, 1e-6)
            return self.cx + self.focale * x / z, self.cy - self.focale * y / z, 1.0 / z
        return self.cx + self.echelle * x, self.cy - self.echelle * y, -z

    def direction_vue(self, P):
        if self.focale:
            d = np.asarray(P, float) - self.oeil
            return d / np.linalg.norm(d, axis=-1, keepdims=True)
        return np.broadcast_to(self.f, np.shape(P))


def direction(azimut_deg, elevation_deg):
    """Direction œil → cible pour un observateur placé à l'azimut donné (0° = devant, +90° = à droite)
    et à l'élévation donnée au-dessus de l'horizon."""
    az, el = math.radians(azimut_deg), math.radians(elevation_deg)
    vers_oeil = np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)])
    return -vers_oeil


def camera_ajustee(points, azimut, elevation, largeur, hauteur, perspective=False, fov=28.0, marge=1.06, haut=None):
    """Caméra cadrant le nuage de points donné."""
    avant = direction(azimut, elevation)
    haut = np.array([0, 0, 1.0]) if haut is None else np.asarray(haut, float)
    if abs(avant @ haut) > 0.999:
        haut = np.array([0, 1.0, 0])
    centre = (points.min(axis=0) + points.max(axis=0)) / 2
    cam = Camera(centre - avant * 10, avant, haut, largeur, hauteur, echelle=1.0)
    x, y, z = cam.vers_camera(points)
    cx, cy = (x.min() + x.max()) / 2, (y.min() + y.max()) / 2
    demi_l, demi_h = (x.max() - x.min()) / 2 * marge, (y.max() - y.min()) / 2 * marge
    centre_vue = cam.oeil + cx * cam.r + cy * cam.u + 10 * cam.f
    if not perspective:
        echelle = min(largeur / (2 * demi_l), hauteur / (2 * demi_h))
        return Camera(centre_vue - avant * 10, avant, haut, largeur, hauteur, echelle=echelle)
    focale = hauteur / 2 / math.tan(math.radians(fov) / 2)
    dist = 2.0
    for _ in range(40):          # recule ou avance jusqu'à cadrer
        c = Camera(centre_vue - avant * dist, avant, haut, largeur, hauteur, focale=focale)
        sx, sy, _q = c.projeter(points)
        k = max((sx.max() - sx.min()) / largeur, (sy.max() - sy.min()) / hauteur) * marge
        if abs(k - 1) < 0.004:
            break
        dist *= k
    c = Camera(centre_vue - avant * dist, avant, haut, largeur, hauteur, focale=focale)
    sx, sy, _q = c.projeter(points)       # recentrage
    c.cx += largeur / 2 - (sx.min() + sx.max()) / 2
    c.cy += hauteur / 2 - (sy.min() + sy.max()) / 2
    return c


# ------------------------------------------------------------------------------------------------
# Scène → triangles
# ------------------------------------------------------------------------------------------------
def triangles_scene(modele, cle, etat, mode="classement", cacher=None, alpha=None):
    """Renvoie (tri (N,3,3), rgb (N,3), a (N,), pid (N,), pieces, centres) pour la variante et l'état."""
    variante = modele["variantes"][cle]
    T, RGB, A, PID, pieces, centres = [], [], [], [], [], {}
    for p in pieces_visibles(variante, etat):
        if cacher and cacher(p):
            continue
        m = maillage_piece(p, variante, etat)
        t = m.vertices[m.faces]
        a = p.get("opacite", 1.0)
        if alpha:
            a2 = alpha(p)
            if a2 is not None:
                a = a2
        T.append(t)
        RGB.append(np.tile(couleur_piece(p, modele, mode), (len(t), 1)))
        A.append(np.full(len(t), a))
        PID.append(np.full(len(t), len(pieces) + 1))
        centres[p["id"]] = (m.bounds[0] + m.bounds[1]) / 2
        pieces.append(p)
    return np.concatenate(T), np.concatenate(RGB), np.concatenate(A), np.concatenate(PID), pieces, centres


# ------------------------------------------------------------------------------------------------
# Rastérisation
# ------------------------------------------------------------------------------------------------
def _rasteriser(sx, sy, q, rgb, pid, nrm, W, H, qbuf, q_plafond=None):
    """Remplit (couleur, qbuf, idbuf, nbuf). Un fragment est retenu s'il est plus proche que qbuf
    et, si q_plafond est fourni, strictement plus loin que q_plafond (depth peeling)."""
    coul = np.zeros((H, W, 3), np.float32)
    idb = np.zeros((H, W), np.int32)
    nb = np.zeros((H, W, 3), np.float32)
    x0, x1, x2 = sx[:, 0], sx[:, 1], sx[:, 2]
    y0, y1, y2 = sy[:, 0], sy[:, 1], sy[:, 2]
    aire = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
    xmin = np.clip(np.floor(sx.min(axis=1)).astype(int), 0, W - 1)
    xmax = np.clip(np.ceil(sx.max(axis=1)).astype(int), 0, W - 1)
    ymin = np.clip(np.floor(sy.min(axis=1)).astype(int), 0, H - 1)
    ymax = np.clip(np.ceil(sy.max(axis=1)).astype(int), 0, H - 1)
    ok = (np.abs(aire) > 1e-9) & (sx.max(axis=1) >= 0) & (sx.min(axis=1) <= W) & (sy.max(axis=1) >= 0) & (sy.min(axis=1) <= H)
    for i in np.nonzero(ok)[0]:
        a, b, c, d = xmin[i], xmax[i], ymin[i], ymax[i]
        px = np.arange(a, b + 1)[None, :] + 0.5
        py = np.arange(c, d + 1)[:, None] + 0.5
        w0 = ((x1[i] - px) * (y2[i] - py) - (x2[i] - px) * (y1[i] - py)) / aire[i]
        w1 = ((x2[i] - px) * (y0[i] - py) - (x0[i] - px) * (y2[i] - py)) / aire[i]
        w2 = 1.0 - w0 - w1
        qq = w0 * q[i, 0] + w1 * q[i, 1] + w2 * q[i, 2]
        sub = qbuf[c:d + 1, a:b + 1]
        m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6) & (qq > sub)
        if q_plafond is not None:
            m &= qq < q_plafond[c:d + 1, a:b + 1]
        if not m.any():
            continue
        sub[m] = qq[m]
        coul[c:d + 1, a:b + 1][m] = rgb[i]
        idb[c:d + 1, a:b + 1][m] = pid[i]
        nb[c:d + 1, a:b + 1][m] = nrm[i]
    return coul, idb, nb


def _aretes(idb, nb, seuil=0.72):
    e = np.zeros(idb.shape, bool)
    for ax in (0, 1):
        d_id = np.diff(idb, axis=ax) != 0
        prod = (nb * np.roll(nb, -1, axis=ax)).sum(axis=2)
        prod = prod[:-1, :] if ax == 0 else prod[:, :-1]
        meme = ~d_id
        pli = meme & (prod < seuil) & ((idb[:-1, :] if ax == 0 else idb[:, :-1]) > 0)
        m = d_id | pli
        if ax == 0:
            e[:-1, :] |= m
        else:
            e[:, :-1] |= m
    return e


def rendre(tri, rgb, alpha, pid, cam, fond=(1.0, 1.0, 1.0), couches=3):
    """Rend la scène ; renvoie une image RGB uint8 (cam.H, cam.W)."""
    W, H = cam.W * SSAA, cam.H * SSAA
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    ln = np.linalg.norm(n, axis=1)
    garde = ln > 1e-14
    tri, rgb, alpha, pid, n = tri[garde], rgb[garde], alpha[garde], pid[garde], n[garde] / ln[garde][:, None]
    cen = tri.mean(axis=1)
    vue = cam.direction_vue(cen)
    face = (n * vue).sum(axis=1) < 0                         # faces tournées vers l'œil
    # éclairage : lumière principale en haut à gauche de l'observateur, lumière d'appoint côté œil
    l1 = -cam.f * 0.55 + cam.u * 0.75 - cam.r * 0.45
    l1 /= np.linalg.norm(l1)
    l2 = -cam.f + cam.r * 0.5 + cam.u * 0.1
    l2 /= np.linalg.norm(l2)
    I = 0.40 + 0.50 * np.clip(n @ l1, 0, 1) + 0.22 * np.clip(n @ l2, 0, 1)
    teinte = np.clip(rgb * I[:, None], 0, 1)
    sx, sy, q = cam.projeter(tri.reshape(-1, 3))
    sx, sy, q = (sx * SSAA).reshape(-1, 3), (sy * SSAA).reshape(-1, 3), q.reshape(-1, 3)

    opaque = face & (alpha >= 0.999)
    qbuf = np.full((H, W), -np.inf)
    coul, idb, nb = _rasteriser(sx[opaque], sy[opaque], q[opaque], teinte[opaque], pid[opaque], n[opaque], W, H, qbuf)
    img = np.where((idb > 0)[..., None], coul, np.array(fond, np.float32))
    ar = ndimage.binary_dilation(_aretes(idb, nb), iterations=1)
    img = img * (1 - 0.78 * ar[..., None])

    trans = face & (alpha < 0.999)
    if trans.any():
        calques = []
        plafond = np.full((H, W), np.inf)
        for _ in range(couches):
            qb = qbuf.copy()
            c, i, nn = _rasteriser(sx[trans], sy[trans], q[trans], teinte[trans], np.arange(1, trans.sum() + 1), n[trans], W, H, qb, plafond)
            touche = i > 0
            if not touche.any():
                break
            a_px = np.zeros((H, W), np.float32)
            a_px[touche] = alpha[trans][i[touche] - 1]
            pid_px = np.zeros((H, W), np.int32)
            pid_px[touche] = pid[trans][i[touche] - 1]
            calques.append((c, a_px, pid_px, nn))
            plafond = np.where(touche, qb - 1e-9 * np.abs(qb) - 1e-12, -np.inf)
        for c, a_px, pid_px, nn in reversed(calques):
            img = img * (1 - a_px[..., None]) + c * a_px[..., None]
            ar_t = _aretes(pid_px, nn)
            img = img * (1 - 0.45 * ar_t[..., None])
    img = img.reshape(cam.H, SSAA, cam.W, SSAA, 3).mean(axis=(1, 3))
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


# ------------------------------------------------------------------------------------------------
# Habillage : titres, repères, légende
# ------------------------------------------------------------------------------------------------
def legende_classement(modele, bilan=None):
    cl = modele["meta"]["classements"]
    out = []
    for k, v in cl.items():
        txt = f"[{k}] {v['libelle']}" + (f" — {bilan[k]} pièce{'s' if bilan[k] > 1 else ''}" if bilan else "")
        out.append(Patch(facecolor=v["couleur"], edgecolor="#333", label=txt))
    return out


def habiller(img, chemin, titre, sous_titre="", reperes=(), cam=None, legende=None, marges=(330, 330, 86, 96), barre=None, note=AVERT):
    """Compose l'image finale. reperes : liste de (texte, point 3D ou (px, py), côté 'g'/'d'/None)."""
    mg, md, mh, mb = marges
    H, W = img.shape[:2]
    Wt, Ht = W + mg + md, H + mh + mb
    fig = plt.figure(figsize=(Wt / 100, Ht / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, Wt)
    ax.set_ylim(Ht, 0)
    ax.axis("off")
    ax.imshow(img, extent=(mg, mg + W, mh + H, mh), zorder=1)
    ax.text(Wt / 2, 30, titre, ha="center", va="center", fontsize=17, fontweight="bold", color="#111")
    if sous_titre:
        ax.text(Wt / 2, 62, sous_titre, ha="center", va="center", fontsize=11, color="#333")
    ax.text(Wt / 2, Ht - 14, note, ha="center", va="center", fontsize=8.6, color="#555", style="italic")
    # repères
    pts = []
    for txt, p, cote in reperes:
        if len(p) == 3:
            x, y, _ = cam.projeter(np.asarray(p, float)[None, :])
            px, py = float(x[0]) + mg, float(y[0]) + mh
        else:
            px, py = p[0] + mg, p[1] + mh
        pts.append([txt, px, py, cote or ("g" if px < mg + W / 2 else "d")])
    for cote in ("g", "d"):
        grp = sorted([p for p in pts if p[3] == cote], key=lambda p: p[2])
        if not grp:
            continue
        y0, y1 = mh + 26, mh + H - 26
        pas = (y1 - y0) / max(len(grp) - 1, 1)
        pas = min(pas, 58)
        ymil = np.mean([p[2] for p in grp])
        debut = float(np.clip(ymil - pas * (len(grp) - 1) / 2, y0, max(y0, y1 - pas * (len(grp) - 1))))
        for k, (txt, px, py, _c) in enumerate(grp):
            ty = debut + k * pas
            tx = mg - 14 if cote == "g" else mg + W + 14
            ax.plot([tx, px], [ty, py], color="#222", lw=0.7, zorder=3)
            ax.plot([px], [py], marker="o", ms=3.4, color="#111", zorder=4)
            ax.text(tx - 5 if cote == "g" else tx + 5, ty, txt, ha="right" if cote == "g" else "left", va="center", fontsize=9.2, color="#111",
                    zorder=4, linespacing=1.15)
    if legende:
        ax.legend(handles=legende, loc="lower center", bbox_to_anchor=(0.5, 26 / Ht), ncol=len(legende), frameon=False, fontsize=9.5,
                  handlelength=1.4, columnspacing=2.2)
    if barre and cam is not None and cam.echelle:
        lg = barre * cam.echelle
        bx, by = mg + 10, mh + H + 16
        ax.plot([bx, bx + lg], [by, by], color="#111", lw=2.2, zorder=5, solid_capstyle="butt")
        for xx in (bx, bx + lg):
            ax.plot([xx, xx], [by - 6, by + 6], color="#111", lw=1.4, zorder=5)
        ax.text(bx + lg + 10, by, f"{barre:.2f} m".replace(".", ",") + " (échelle hypothétique)", ha="left", va="center", fontsize=8.8, color="#111", zorder=5)
    fig.savefig(chemin, dpi=100, facecolor="white")
    plt.close(fig)


def trouver(pieces, centres, fragment):
    """Centre (dans l'état rendu) de la première pièce dont le nom contient le fragment."""
    for p in pieces:
        if fragment in p["nom"]:
            return centres[p["id"]]
    raise KeyError(fragment)


def cl(pieces, fragment):
    for p in pieces:
        if fragment in p["nom"]:
            return f"[{p['classement']}]"
    return ""


# ------------------------------------------------------------------------------------------------
# Vues
# ------------------------------------------------------------------------------------------------
def points_emprise(tri):
    return tri.reshape(-1, 3)


REP_007 = [   # (texte, fragment du nom de pièce, côté)
    ("1 · Singularité principale\n« MAIN SINGULARITY »", "Collerette du logement — singularité principale", "g"),
    ("2 · Singularité de direction\n« STEERING SINGULARITY »", "Collerette du logement — singularité de direction", "g"),
    ("3 · Télécommande\n« REMOTE CONTROL UNIT »", "Télécommande — boîtier", "g"),
    ("4 · Écran de secours\n« EMERGENCY VIEW SCREEN »", "Écran de visualisation de secours (4) — fente", "d"),
    ("5 · Coupure d'urgence\n« EMERGENCY DISCONNECT »", "Organe rond de coupure d'urgence (5)", "d"),
    ("6 · Marche / arrêt général\n« MAIN UNIT ON/OFF SWITCH »", "Interrupteur général (6) — boîtier", "d"),
    ("7 · Instructions de commande\n« UNIT CONTROL INSTRUCTIONS »", "Plaque d'instructions de commande (7)", "d"),
    ("8 · Commandes d'urgence\n« EMERGENCY CONTROLS »", "Panneau 8 — plage blanche des touches", "d"),
    ("9 · Rangement télécommande\n« REMOTE STORAGE UNIT »", "Rangement 9 — fond", "d", "[DOC]\n(profondeur : [HYP])"),
]
REP_008 = [
    ("1 · Carter d'entraînement\nde singularité", "Carter d'entraînement de singularité (1) — principale", "g"),
    ("2 · Bobine de champ magnétique", "Bobine de champ magnétique (2) — principale, spire 6", "g"),
    ("3 · Générateur / régulateur\nde champ magnétique", "Générateur / régulateur de champ magnétique (3) — de direction", "g"),
    ("4 · Collecteur d'injection\nd'électrons", "Collecteur d'injection (4) — de direction, tube 1", "g"),
    ("5 · Régulateur d'électrons", "Régulateur d'électrons (5)", "d"),
    ("6 · Générateur d'électrons", "Générateur d'électrons (6) — boîtier", "d"),
    ("7 · Amplificateur de capteur\nde singularité", "Amplificateur de capteur de singularité (7) — de direction", "g"),
    ("8 · Enveloppe de refroidissement", "Enveloppe de refroidissement (8) — de direction", "d"),
    ("9 · Pompe de refroidissement", "Pompe de refroidissement (9)", "g"),
    ("10 · Réservoirs de fluide\nde refroidissement", "Réservoir de refroidissement (10) n°1 — virole", "g"),
    ("11 · Unité de capteurs\nde gravité", "Capteurs de gravité (11) — socle du module", "d"),
    ("12 · Batterie", "Batterie (12) — élément 1", "g"),
    ("Horloges au césium ×4\n(texte seul)", "Horloge au césium n°2", "d"),
    ("Calculateurs ×3\n(texte seul)", "Calculateur n°3", "d"),
]


def reperes(liste, pieces, centres, avec_classement=True):
    out = []
    for txt, frag, cote, *etiq in liste:
        try:
            p = trouver(pieces, centres, frag)
        except KeyError:
            continue
        out.append((txt + ("  " + (etiq[0] if etiq else cl(pieces, frag)) if avec_classement else ""), p, cote))
    return out


def vue(modele, cle, etat, mode, az, el, taille=(1500, 980), perspective=True, cacher=None, alpha=None, fov=26.0, cam=None, marge=1.06):
    tri, rgb, a, pid, pieces, centres = triangles_scene(modele, cle, etat, mode, cacher, alpha)
    if cam is None:
        cam = camera_ajustee(points_emprise(tri), az, el, taille[0], taille[1], perspective, fov, marge)
    return rendre(tri, rgb, a, pid, cam), cam, pieces, centres


def main(modele=None):
    if modele is None:
        modele = json.loads((ICI / "modele_c204.json").read_text(encoding="utf-8"))
    SORTIE.mkdir(exist_ok=True)
    A = modele["variantes"]["A"]
    leg = legende_classement(modele)
    fantome = lambda p: 0.14 if p.get("fantome") else None
    coque_fantome = lambda p: 0.13 if (p.get("fantome") and p["couche"] == "coque") else None
    sans_platine = lambda p: p["couche"] in ("platine", "mobile")
    faits = []

    # 01 — extérieur fermé
    img, cam, pcs, cen = vue(modele, "A", "ferme", "classement", -32, 28, fov=16)
    rep = [("Couvercle articulé  [DOC]\n(extérieur fermé : aucune image)", trouver(pcs, cen, "Couvercle — dessus") + np.array([0.2, -0.1, 0.02]), "d"),
           ("Corps du coffre  [DOC]\nL/P = 3,27 (DOC-007) ; H/L = 0,246 (DOC-004)", trouver(pcs, cen, "Corps — paroi avant") + np.array([0.25, 0, -0.03]), "d"),
           ("Loquets avant  [DÉD]\n(DOC-004, position incertaine)", trouver(pcs, cen, "Loquet de fermeture avant n°1"), "g"),
           ("Poignée encastrée  [DÉD]\n(DOC-004)", trouver(pcs, cen, "Poignée encastrée d'extrémité gauche"), "g"),
           ("Fond  [HYP]\n(jamais montré)", trouver(pcs, cen, "Corps — fond") + np.array([0.3, -A["cotes_cles"]["P"] / 2, 0]), "d")]
    habiller(img, SORTIE / "01_exterieur_ferme.png", "C204 — variante A : coffre fermé (vue extérieure)",
             "Couleurs = classement des pièces. L'aspect extérieur fermé n'est montré par aucun document : volume déduit du coffre ouvert.", rep, cam, leg)
    faits.append("01_exterieur_ferme.png")

    # 02 / 03 — ouvert, vue 3/4 (aspect, puis classement)
    for num, mode, titre, st in (("02", "aspect", "C204 — variante A : coffre ouvert, aspect d'après les documents",
                                  "Vue 3/4 comparable à DOC-004 ; teintes jaune/noir/orange relevées sur les photos DOC-001 à 003 ; repères de DOC-007."),
                                 ("03", "classement", "C204 — variante A : coffre ouvert, couleurs par classement",
                                  "Tout ce qui est bleu est lisible sur DOC-004/007 ou les photos ; orange = déduit ; rose = hypothétique.")):
        img, cam, pcs, cen = vue(modele, "A", "ouvert", mode, -34, 40)
        habiller(img, SORTIE / f"{num}_ouvert_{mode}.png", titre, st, reperes(REP_007, pcs, cen, mode == "classement"), cam, leg if mode == "classement" else None)
        faits.append(f"{num}_ouvert_{mode}.png")

    # 04 — intérieur : coque translucide, platine masquée
    img, cam, pcs, cen = vue(modele, "A", "ouvert", "classement", -28, 34, cacher=sans_platine, alpha=coque_fantome)
    habiller(img, SORTIE / "04_interieur_composants.png", "C204 — variante A : composants internes (couvercle ouvert, platine retirée, coque translucide)",
             "Repères = légende de DOC-008. Les carters sont placés sous les logements de DOC-007 [DÉD] ; tout autre emplacement est [HYP] (disposition I1).",
             reperes(REP_008, pcs, cen), cam, leg)
    faits.append("04_interieur_composants.png")

    # 05 — éclaté
    img, cam, pcs, cen = vue(modele, "A", "eclate", "classement", -30, 22, taille=(1250, 1500), fov=24)
    rep = [("Couvercle (intérieur : bandes,\nplaque 7, étiquettes)  [DOC]", trouver(pcs, cen, "Couvercle — dessus"), "d"),
           ("Marquages et commandes\nde la platine  [DOC]", trouver(pcs, cen, "Panneau 8 — plage blanche des touches"), "d"),
           ("Platine supérieure (DOC-007)  [DOC]", trouver(pcs, cen, "Platine — zone tramée gauche (a)"), "g"),
           ("Cadre des deux logements  [DOC]", trouver(pcs, cen, "Platine — cadre des deux logements"), "g"),
           ("Ensemble singularité principale\n(carter, enveloppe, bobines)  [DÉD]", trouver(pcs, cen, "Carter d'entraînement de singularité (1) — principale"), "d"),
           ("Ensemble singularité de direction  [DÉD]", trouver(pcs, cen, "Carter d'entraînement de singularité (1) — de direction"), "g"),
           ("Générateur d'électrons (6)  [HYP]", trouver(pcs, cen, "Générateur d'électrons (6) — boîtier"), "d"),
           ("Réservoirs (10) et pompe (9)  [HYP]", trouver(pcs, cen, "Réservoir de refroidissement (10) n°1 — virole"), "g"),
           ("Batterie (12)  [HYP]", trouver(pcs, cen, "Batterie (12) — élément 1"), "g"),
           ("Capteurs de gravité (11), horloges,\ncalculateurs  [HYP]", trouver(pcs, cen, "Capteurs de gravité (11) — socle du module"), "d"),
           ("Corps du coffre  [DOC]", trouver(pcs, cen, "Corps — paroi avant"), "d"),
           ("Télécommande (3)  [DOC]\ncordon : tracé [DÉD]", trouver(pcs, cen, "Télécommande — boîtier"), "g")]
    habiller(img, SORTIE / "05_eclate.png", "C204 — variante A : vue éclatée", "Décalages verticaux de présentation (sans valeur documentaire).", rep, cam, leg)
    faits.append("05_eclate.png")

    # 06 — orthographique de dessus, couvercle rabattu à plat comme sur DOC-007
    img, cam, pcs, cen = vue(modele, "A", "a_plat", "classement", 0, 90, taille=(1500, 1120), perspective=False, marge=1.04)
    habiller(img, SORTIE / "06_ortho_dessus.png", "C204 — variante A : vue orthographique de dessus (couvercle rabattu à plat, comme DOC-007)",
             "Positions en plan = proportions mesurées sur DOC-007 (±0,3 % de L).", reperes(REP_007, pcs, cen), cam, leg, barre=0.20)
    faits.append("06_ortho_dessus.png")

    # 07 — orthographique de face (fermé, enveloppes translucides)
    img, cam, pcs, cen = vue(modele, "A", "ferme", "classement", 0, 0, taille=(1500, 560), perspective=False, alpha=fantome, cacher=lambda p: p["couche"] == "platine" and p["systeme"] == "signalisation")
    habiller(img, SORTIE / "07_ortho_face.png", "C204 — variante A : vue orthographique de face (fermé, enveloppes translucides)",
             "Hauteur du corps d'après DOC-004 ; contenu d'après DOC-008 (tailles relatives) et disposition I1 [HYP].",
             reperes([r for r in REP_008 if r[0][:2] in ("1 ", "3 ", "6 ", "9 ", "10", "11", "12", "Ho", "Ca")], pcs, cen), cam, leg, barre=0.20)
    faits.append("07_ortho_face.png")

    # 08 — orthographique de côté (depuis l'extrémité gauche) : la lecture « élévation » de DOC-008
    noyau = lambda p: (p["ensemble"].startswith("Ensemble singularité") or p["ensemble"].startswith("Générateurs / régulateurs")
                       or p["nom"] in ("Régulateur d'électrons (5)", "Collecteur d'injection (4) — rampe commune"))
    seul_noyau = lambda p: not (noyau(p) or (p.get("fantome") and p["couche"] in ("coque", "couvercle")) or (p["couche"] == "platine" and p["systeme"] == "singularites"))
    img, cam, pcs, cen = vue(modele, "A", "ferme", "classement", -90, 0, taille=(900, 760), perspective=False, alpha=fantome, cacher=seul_noyau)
    img08 = img
    rep8 = [("1 · Carter (singularité\nprincipale, côté charnière)", "Carter d'entraînement de singularité (1) — principale", "g"),
            ("1 · Carter (singularité\nde direction, côté avant)", "Carter d'entraînement de singularité (1) — de direction", "d"),
            ("2 · Bobines", "Bobine de champ magnétique (2) — principale, spire 6", "g"),
            ("8 · Enveloppe de\nrefroidissement", "Enveloppe de refroidissement (8) — de direction", "d"),
            ("7 · Amplificateur\nde capteur", "Amplificateur de capteur de singularité (7) — de direction", "d"),
            ("5 · Régulateur\nd'électrons", "Régulateur d'électrons (5)", "d"),
            ("4 · Collecteur\nd'injection", "Collecteur d'injection (4) — principale, tube 3", "g"),
            ("3 · Générateurs /\nrégulateurs de champ", "Générateur / régulateur de champ magnétique (3) — principale", "g")]
    habiller(img, SORTIE / "08_ortho_cote.png", "C204 — variante A : vue de côté (depuis l'extrémité gauche), noyau seul",
             "Lecture proposée [DÉD] : DOC-008 = élévation vue en bout ; les carters « côte à côte » y sont ceux alignés en profondeur de DOC-007.",
             reperes(rep8, pcs, cen), cam, leg, marges=(300, 300, 86, 96), barre=0.10)
    faits.append("08_ortho_cote.png")

    # 09 — variante B
    img, cam, pcs, cen = vue(modele, "B", "ouvert", "classement", -30, 30, taille=(1500, 900))
    repB = []
    for p in pcs:
        if p["repere"].startswith("DOC-005 n°"):
            repB.append((p["repere"].replace("DOC-005 n°", "") + " · " + p["nom"].split(" (")[0][:44], cen[p["id"]], None))
    habiller(img, SORTIE / "09_variante_B_ecorche.png", "C204 — variante B : écorché DOC-005 (enveloppe et volumes principaux)",
             "Numéros = repères de DOC-005, dont la légende manque : fonctions INCONNUES. Profondeurs supposées (vue unique). Échelle arbitraire.",
             repB, cam, legende_classement(modele, modele["variantes"]["B"]["bilan_classement"]), marges=(380, 380, 86, 96))
    faits.append("09_variante_B_ecorche.png")

    # 10 — comparaison DOC-007 / modèle (vue de dessus, aspect)
    img, cam, pcs, cen = vue(modele, "A", "a_plat", "aspect", 0, 90, taille=(1200, 900), perspective=False, marge=1.04)
    comparer(Image.open(ARCHIVE / "MT7016__timetravel_0_1.jpg").convert("RGB").crop((14, 8, 448, 362)), img, SORTIE / "10_comparaison_DOC-007.png",
             "Comparaison : DOC-007 (à gauche) et modèle, vue de dessus couvercle à plat (à droite)", "DOC-007 — document source (recadré)", "Modèle — aspect (jaune des bandes d'après les photos)")
    faits.append("10_comparaison_DOC-007.png")

    # 11 — comparaison DOC-004 / modèle, avec la caméra ajustée sur DOC-004
    mes = json.loads((ICI / "mesures" / "mesures_proportions.json").read_text(encoding="utf-8"))
    cp = mes["DOC-004"]["camera_perspective_libre"]
    from mesures.mesurer_proportions import _rot
    R = _rot(math.radians(cp["lacet_deg"]), math.radians(cp["tangage_deg"]), math.radians(cp["roulis_deg"]))
    t = np.array(cp["translation"])
    L = A["cotes_cles"]["L"]
    k = 3.0                                              # image d'origine 477×440 → rendu ×3
    cam4 = Camera((-R.T @ t) * L, R.T @ np.array([0, 0, 1.0]), -(R.T @ np.array([0, 1.0, 0])), int(477 * k), int(440 * k), focale=cp["focale_px"] * k)
    tri, rgb, a, pid, pcs, cen = triangles_scene(modele, "A", "ouvert", "aspect", cacher=lambda p: p["couche"] == "mobile")
    img = rendre(tri, rgb, a, pid, cam4)
    comparer(Image.open(ARCHIVE / "MT7013__c204unit_johntitor.jpg").convert("RGB"), img, SORTIE / "11_comparaison_DOC-004.png",
             "Comparaison : DOC-004 (à gauche) et modèle vu par la caméra ajustée sur DOC-004 (à droite)", "DOC-004 — document source",
             "Modèle — même point de vue (caméra ajustée sur 9 coins, résidu 4 px) ; télécommande omise")
    faits.append("11_comparaison_DOC-004.png")

    # 12 — comparaison DOC-005 / variante B
    img, cam, pcs, cen = vue(modele, "B", "ouvert", "aspect", -30, 30, taille=(1200, 800))
    comparer(Image.open(ARCHIVE / "MT7014__johntitor_schematic.jpg").convert("RGB").crop((20, 130, 1000, 700)), img, SORTIE / "12_comparaison_DOC-005.png",
             "Comparaison : DOC-005 (à gauche) et variante B du modèle (à droite)", "DOC-005 — écorché sans légende", "Modèle — enveloppe translucide et volumes génériques [DÉD]")
    faits.append("12_comparaison_DOC-005.png")

    # 14 — comparaison DOC-008 (noyau) / vue de côté du modèle
    comparer(Image.open(ARCHIVE / "MT7017__c204_unit_instructions.jpeg").convert("RGB").crop((60, 150, 310, 350)), img08, SORTIE / "14_comparaison_DOC-008.png",
             "Comparaison : noyau de DOC-008 (à gauche) et modèle vu depuis l'extrémité gauche (à droite)", "DOC-008 — schéma de principe (extrait : repères 1 à 5, 7, 8)",
             "Modèle — entraxe ramené de 1,62 D (DOC-008) à 1,16 D (DOC-007)")
    faits.append("14_comparaison_DOC-008.png")

    # 13 — deux hypothèses de disposition interne, en plan
    imgs = []
    for cle in ("A", "A2"):
        im, cam, pcs, cen = vue(modele, cle, "ferme", "classement", 0, 90, taille=(1300, 430), perspective=False, cacher=lambda p: p["couche"] in ("platine", "couvercle"), alpha=coque_fantome)
        imgs.append(im)
    di = json.loads((ICI / "parametres.json").read_text(encoding="utf-8"))["disposition_interne"]
    fig, axs = plt.subplots(2, 1, figsize=(14, 10.4), dpi=100)
    for ax, im, cle in zip(axs, imgs, (di["retenue"], di["alternative"])):
        ax.imshow(im)
        ax.axis("off")
        ax.set_title(di["dispositions"][cle]["nom"] + ("   (retenue)" if cle == di["retenue"] else "   (alternative)"), fontsize=11.5, loc="left")
    fig.suptitle("C204 — variante A : deux hypothèses de disposition interne (vue en plan, platine et couvercle retirés)", fontsize=14.5, fontweight="bold")
    fig.legend(handles=leg, loc="lower center", ncol=3, frameon=False, fontsize=10, bbox_to_anchor=(0.5, 0.035))
    fig.text(0.5, 0.012, AVERT, ha="center", fontsize=8.6, color="#555", style="italic")
    fig.text(0.5, 0.925, "Seul le noyau (carters sous les logements de DOC-007) est contraint par les documents ; l'emplacement des autres composants est un choix [HYP].",
             ha="center", fontsize=10.5, color="#333")
    fig.subplots_adjust(left=0.02, right=0.98, top=0.88, bottom=0.09, hspace=0.12)
    fig.savefig(SORTIE / "13_dispositions_internes_I1_I2.png", dpi=100, facecolor="white")
    plt.close(fig)
    faits.append("13_dispositions_internes_I1_I2.png")
    for f in faits:
        print("rendu :", f)


def comparer(doc, img, chemin, titre, lg, ld):
    fig, axs = plt.subplots(1, 2, figsize=(16.5, 7.6), dpi=100)
    axs[0].imshow(doc)
    axs[0].set_title(lg, fontsize=11.5)
    axs[1].imshow(img)
    axs[1].set_title(ld, fontsize=11.5)
    for ax in axs:
        ax.axis("off")
    fig.suptitle(titre, fontsize=15, fontweight="bold")
    fig.text(0.5, 0.018, AVERT, ha="center", fontsize=8.6, color="#555", style="italic")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.05, wspace=0.03)
    fig.savefig(chemin, dpi=100, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    main()
