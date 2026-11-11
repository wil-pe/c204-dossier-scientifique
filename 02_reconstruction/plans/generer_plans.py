#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Programme C204 — Équipe A — plans 2D reconstitués de l'unité « telle que décrite ».

Lit ../dimensions.json et produit, en SVG et en PNG :
  plan_01_vue_dessus          (coffre ouvert, d'après C204-DOC-007)
  plan_02_vue_face            (couvercle fermé)
  plan_03_vue_cote            (profil, couvercle fermé et ouvert)
  plan_04_couvercle_ouvert    (vue de face, couvercle levé, d'après les photos DOC-001/002/003)
  plan_05_implantation_interne_hypotheses (deux variantes, entièrement hypothétiques)

Code couleur imposé par le dossier de base :
  noir, trait plein      = [DOC]  documenté (lisible sur un document source)
  bleu, tirets           = [DÉD]  déduit
  rouge, pointillés      = [HYP]  hypothétique

AVERTISSEMENT : reconstitution documentaire. Ces plans décrivent des images et des textes
attribués à « John Titor » ; ils ne démontrent ni l'existence ni le fonctionnement de la machine.
L'échelle absolue repose sur des étalons supposés : L = 0,85 m, intervalle central 0,74–1,05 m, plage 0,65–1,25 m.

Usage : python generer_plans.py      (aucun argument ; écrit dans le dossier du script)
"""
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle

ICI = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ICI, "..", "dimensions.json"), encoding="utf-8") as f:
    DIM = json.load(f)
C = {c["id"]: c for c in DIM["cotes"]}
L = C["L"]["valeur"]
P = C["P"]["valeur"]
H = C["H_corps"]["valeur"]
E = C["e_couv"]["valeur"]
D_LOG = C["D_log"]["valeur"]

DOC = dict(edgecolor="black", linestyle="-", linewidth=1.3)
DED = dict(edgecolor="#1f4fbf", linestyle="--", linewidth=1.2)
HYP = dict(edgecolor="#c0182b", linestyle=":", linewidth=1.4)
STYLE = {"DOC": DOC, "DÉD": DED, "HYP": HYP}
COUL = {"DOC": "black", "DÉD": "#1f4fbf", "HYP": "#c0182b"}

AVERT = ("Reconstitution documentaire (Équipe A, v1.1) — ne prouve ni l'existence ni le fonctionnement de la machine. "
         "Échelle absolue : étalons supposés, L entre 0,65 et 1,25 m.")


def pm(idc, unite="m", nd=2):
    c = C[idc]
    v = c["valeur"]
    u = c.get("incertitude")
    # Correction post-validation n° 8 : L n'a pas d'incertitude statistique ; on affiche la plage.
    if idc == "L" and c.get("intervalle_plausible"):
        a, b = c["intervalle_plausible"]
        return f"{v:.{nd}f} {unite} (plage {a:.2f}–{b:.2f} {unite})"
    if u is None:
        return f"{v:.{nd}f} {unite}"
    return f"{v:.{nd}f} ± {u:.{nd}f} {unite}"


def rect(ax, x, y, w, h, etq="DOC", fc="none", hatch=None, z=2, **kw):
    st = dict(STYLE[etq])
    st.update(kw)
    r = Rectangle((x, y), w, h, facecolor=fc, hatch=hatch, zorder=z, **st)
    ax.add_patch(r)
    return r


def cercle(ax, x, y, r, etq="DOC", fc="none", z=3, **kw):
    st = dict(STYLE[etq])
    st.update(kw)
    c = Circle((x, y), r, facecolor=fc, zorder=z, **st)
    ax.add_patch(c)
    return c


def bande_danger(ax, x, y, w, h, etq="DOC", n=4):
    """Bande de danger à chevrons obliques (noir sur fond clair)."""
    rect(ax, x, y, w, h, etq, fc="#fff3a0", z=2)
    pas = h / n
    for i in range(n):
        y0 = y + i * pas
        poly = Polygon([(x, y0), (x + w, y0 + pas * 0.5), (x + w, y0 + pas), (x, y0 + pas * 0.5)],
                       closed=True, facecolor="black", edgecolor="none", zorder=3, alpha=0.85)
        ax.add_patch(poly)


def cote(ax, p0, p1, texte, decal=0.0, etq="DÉD", ha="center", va="bottom", rot=0):
    c = COUL[etq]
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<->", mutation_scale=9, color=c, linewidth=0.9, zorder=6))
    xm, ym = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    if rot == 90:
        ax.text(xm - decal, ym, texte, color=c, fontsize=7.5, ha="right", va="center", rotation=90, zorder=7)
    else:
        ax.text(xm, ym + decal, texte, color=c, fontsize=7.5, ha=ha, va=va, zorder=7)


def repere(ax, xy, cible, num, texte=None, etq="DOC"):
    c = COUL[etq]
    ax.annotate("", xy=cible, xytext=xy, arrowprops=dict(arrowstyle="-|>", color=c, lw=0.8), zorder=8)
    ax.add_patch(Circle(xy, 0.022 * L / 0.85, facecolor="white", edgecolor=c, linewidth=0.9, zorder=9))
    ax.text(xy[0], xy[1], str(num), ha="center", va="center", fontsize=7, color=c, zorder=10)
    if texte:
        ax.text(xy[0] + 0.03, xy[1], texte, ha="left", va="center", fontsize=6.8, color=c, zorder=10)


def legende(ax, x, y):
    dy = 0.028 * L / 0.85
    items = [("DOC", "[DOC] documenté (lisible sur un document source)"),
             ("DÉD", "[DÉD] déduit de plusieurs éléments documentés"),
             ("HYP", "[HYP] hypothétique (supposition de l'équipe)")]
    for i, (e, t) in enumerate(items):
        yy = y - i * dy
        st = STYLE[e]
        ax.plot([x, x + 0.06], [yy, yy], color=st["edgecolor"], linestyle=st["linestyle"], linewidth=1.6)
        ax.text(x + 0.07, yy, t, fontsize=7, va="center", color=st["edgecolor"])


def finir(fig, ax, titre, nom, xlim, ylim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(titre, fontsize=10.5, loc="left")
    fig.text(0.01, 0.012, AVERT, fontsize=6.5, color="#444444")
    fig.savefig(os.path.join(ICI, nom + ".svg"), format="svg", bbox_inches="tight")
    fig.savefig(os.path.join(ICI, nom + ".png"), format="png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print("écrit :", nom + ".svg /.png")


# Fractions lues sur C204-DOC-007 (copie OP3.jpg, corps x 48→404 px, y 190→298 px)
ZX = dict(comp_g=(0.022, 0.138), bande1=(0.138, 0.230), trame1=(0.236, 0.303), logement=(0.303, 0.461),
          trame2=(0.461, 0.537), bande2=(0.537, 0.629), trame3=(0.635, 0.697), col_cmd=(0.708, 0.784),
          pan_urg=(0.792, 0.876), comp_d=(0.890, 0.989))
X_LOG = 0.382
Y_LOG = (0.24, 0.59)   # depuis le bord charnière, en fraction de P (profils de pixels sur OP3.jpg ; rapport R10)
CHARN = ((0.194, 0.272), (0.728, 0.806))


def corps_dessus(ax, y0):
    """Dessine le dessus du corps (pont) ; y0 = ordonnée du bord avant ; la charnière est en y0+P."""
    rect(ax, 0, y0, L, P, "DOC", fc="#f4f4f4", linewidth=2.0)
    m = 0.03 * P

    def zone(cle, etq="DOC", fc="#dddddd", hatch=None):
        a, b = ZX[cle]
        return rect(ax, a * L, y0 + m, (b - a) * L, P - 2 * m, etq, fc=fc, hatch=hatch)

    zone("comp_g", hatch="....")
    a, b = ZX["bande1"]
    bande_danger(ax, a * L, y0 + m, (b - a) * L, P - 2 * m)
    zone("trame1", hatch="xxxx")
    zone("logement", fc="#c9c9c9")
    zone("trame2", hatch="xxxx")
    a, b = ZX["bande2"]
    bande_danger(ax, a * L, y0 + m, (b - a) * L, P - 2 * m)
    zone("trame3", hatch="xxxx")
    zone("col_cmd", fc="white")
    zone("pan_urg", fc="#eeeeee", hatch="..")
    zone("comp_d", fc="#f7f7f7", hatch="..")
    # logements circulaires (repères 1 et 2)
    for fy in Y_LOG:
        cercle(ax, X_LOG * L, y0 + P - fy * P, D_LOG / 2, "DOC", fc="black")
    a, b = ZX["logement"]
    ax.plot([a * L, b * L], [y0 + P - 0.41 * P] * 2, color="black", linewidth=0.8, zorder=4)
    # colonne de commande : écran (4), bouton rond (5)
    a, b = ZX["col_cmd"]
    rect(ax, (a + 0.008) * L, y0 + P - 0.14 * P, (b - a - 0.016) * L, 0.085 * P, "DOC", fc="#333333")
    cercle(ax, (a + b) / 2 * L, y0 + P - 0.74 * P, 0.017 * L, "DOC", fc="white")
    rect(ax, (a + 0.01) * L, y0 + P - 0.66 * P, (b - a - 0.02) * L, 0.10 * P, "DOC", hatch="////")
    rect(ax, (a + 0.01) * L, y0 + P - 0.92 * P, (b - a - 0.02) * L, 0.10 * P, "DOC", hatch="////")
    # panneau d'urgence : voyants / touches (8), interrupteur (6)
    a, b = ZX["pan_urg"]
    for i in range(9):
        for j in range(2 if i < 4 else 1):
            ax.plot([(a + 0.022 + 0.022 * j) * L], [y0 + P - (0.10 + 0.06 * i) * P], marker="s", markersize=2.2,
                    color="black", zorder=5)
    rect(ax, (a + 0.012) * L, y0 + P - 0.93 * P, (b - a - 0.024) * L, 0.20 * P, "DOC", fc="#bbbbbb")


def plan_dessus():
    fig, ax = plt.subplots(figsize=(11, 8.2))
    y_corps = 0.0
    y_couv = P + 0.012
    # couvercle rabattu à plat (comme sur DOC-007)
    rect(ax, 0, y_couv, L, P, "DOC", fc="#fafafa", linewidth=2.0)
    m = 0.06 * P
    rect(ax, 0.03 * L, y_couv + m, 0.94 * L, P - 2 * m, "DOC", fc="#f0f0f0", hatch="..", linewidth=0.8)
    for cle in ("bande1", "bande2"):
        a, b = ZX[cle]
        bande_danger(ax, a * L, y_couv + 0.01 * P, (b - a) * L, 0.98 * P)
    rect(ax, 0.711 * L, y_couv + 0.11 * P, (0.868 - 0.711) * L, 0.77 * P, "DOC", fc="#777777")
    for a, b in CHARN:
        rect(ax, a * L, P - 0.002, (b - a) * L, 0.016, "DOC", fc="black")
    corps_dessus(ax, y_corps)
    # télécommande (repère 3) et câble
    tl, th = C["tele_l"]["valeur"], C["tele_h"]["valeur"]
    tx, ty = 0.045 * L, -0.15 - th
    rect(ax, tx, ty, tl, th, "DOC", fc="white")
    rect(ax, tx + 0.1 * tl, ty + 0.62 * th, 0.6 * tl, 0.25 * th, "DOC", fc="#cccccc")
    ax.plot([tx + tl, 1.035 * L, 1.035 * L, L], [ty + 0.12 * th, ty + 0.12 * th, 0.02, 0.02], color="black",
            linewidth=1.3, zorder=3)
    ax.text(0.5 * L, ty + 0.12 * th - 0.012, "câble de liaison [DOC]", fontsize=6.5, ha="center", va="top")
    # repères d'origine (numérotation de DOC-007)
    xg, xd = -0.13, L + 0.17
    repere(ax, (xg, P - Y_LOG[0] * P), (X_LOG * L - D_LOG / 2, P - Y_LOG[0] * P), 1)
    ax.text(xg - 0.03, P - Y_LOG[0] * P, "MAIN SINGULARITY", ha="right", va="center", fontsize=6.8)
    repere(ax, (xg, P - Y_LOG[1] * P), (X_LOG * L - D_LOG / 2, P - Y_LOG[1] * P), 2)
    ax.text(xg - 0.03, P - Y_LOG[1] * P, "STEERING SINGULARITY", ha="right", va="center", fontsize=6.8)
    repere(ax, (xg, ty + th / 2), (tx, ty + th / 2), 3)
    ax.text(xg - 0.03, ty + th / 2, "REMOTE CONTROL UNIT", ha="right", va="center", fontsize=6.8)

    def brise(num, texte, yl, xv, cible):
        """Repère à ligne brisée venant du bas, comme sur le document d'origine."""
        x0 = 0.60 * L
        ax.plot([x0, xv, xv], [yl, yl, cible[1] if cible[0] != xv else yl], color="black", linewidth=0.8, zorder=8)
        ax.annotate("", xy=cible, xytext=(xv, cible[1] if cible[0] != xv else yl),
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=0.8), zorder=8)
        ax.add_patch(Circle((x0, yl), 0.022 * L / 0.85, facecolor="white", edgecolor="black", linewidth=0.9, zorder=9))
        ax.text(x0, yl, str(num), ha="center", va="center", fontsize=7, zorder=10)
        ax.text(x0 - 0.03, yl, texte, ha="right", va="center", fontsize=6.8)

    brise(4, "EMERGENCY VIEW SCREEN", -0.06, 0.666 * L, (0.714 * L, P - 0.10 * P))
    brise(5, "EMERGENCY DISCONNECT", -0.095, 0.746 * L, (0.746 * L, 0.0))
    brise(6, "MAIN UNIT ON/OFF SWITCH", -0.13, 0.834 * L, (0.834 * L, 0.0))
    repere(ax, (xd, y_couv + 0.5 * P), (0.868 * L, y_couv + 0.5 * P), 7, "UNIT CONTROL INSTRUCTIONS")
    repere(ax, (xd, P - 0.15 * P), (0.876 * L, P - 0.15 * P), 8, "EMERGENCY CONTROLS")
    repere(ax, (xd, P - 0.65 * P), (0.94 * L, P - 0.65 * P), 9, "REMOTE STORAGE UNIT")
    # cotes
    cote(ax, (0, 2 * P + 0.05), (L, 2 * P + 0.05), "L = " + pm("L") + "  [DÉD sur étalons HYP, confiance faible]", decal=0.006)
    cote(ax, (L + 0.085, 0), (L + 0.085, P), "P = " + pm("P") + " [DÉD, via L]", decal=0.008, rot=90)
    cote(ax, (0, -0.02), (X_LOG * L, -0.02), f"{X_LOG:.3f} L [DOC]", decal=-0.028, etq="DOC")
    ax.text(0.5 * L, 2 * P + 0.022, f"logements circulaires : Ø = 0,094 L [DOC]  →  ≈ {D_LOG*1000:.0f} mm [DÉD, via L] ; "
            "entraxe 0,107 L [DOC]", fontsize=6.8, ha="center", color=COUL["DÉD"])
    ax.text(-0.01, P + 0.006, "charnières (2) [DOC] →", fontsize=6.5, ha="right", va="center")
    legende(ax, -0.42, 2 * P + 0.19)
    ax.text(-0.42, -0.36,
            "Proportions et zones : lecture directe de C204-DOC-007 (meilleure copie : OP3.jpg, 460×600 px).\n"
            "L/P = 3,27 à 3,30 [DOC]. Les deux logements sont l'un derrière l'autre (dans le sens de la profondeur), au tiers gauche.\n"
            "Écart connu : sur les photographies, les bandes de danger sont plus étroites et placées plus à gauche (voir INCOHERENCES.md).",
            fontsize=6.8, va="top")
    finir(fig, ax, "C204 — Plan 1 : vue de dessus, coffre ouvert, couvercle rabattu (d'après C204-DOC-007)",
          "plan_01_vue_dessus", (-0.45, L + 0.52), (-0.46, 2 * P + 0.22))


def plan_face():
    fig, ax = plt.subplots(figsize=(11, 5.6))
    rect(ax, 0, 0, L, H, "DÉD", fc="#3a3a3a", linewidth=1.8)
    rect(ax, 0, H, L, E, "DÉD", fc="#4a4a4a", linewidth=1.8)
    ax.plot([0, L], [H, H], color="white", linewidth=0.8, zorder=4)
    # fermoirs : au moins deux, positions incertaines (0,32–0,51 L et 0,64–0,85 L selon la photo)
    for fx in (0.41, 0.75):
        rect(ax, fx * L - 0.012, H - 0.03, 0.024, 0.05, "DÉD", fc="#bbbbbb", z=5)
    ax.text(0.58 * L, H + E + 0.012, "fermoirs en face avant : au moins 2 [DOC photo] ; positions à ±0,1 L [DÉD]", fontsize=6.8,
            ha="center", color=COUL["DÉD"])
    # poignée d'extrémité et coins / patins
    rect(ax, -0.012, 0.35 * H, 0.012, 0.3 * H, "HYP", fc="#dddddd")
    rect(ax, L, 0.35 * H, 0.012, 0.3 * H, "HYP", fc="#dddddd")
    for x0 in (0.0, L - 0.07):
        rect(ax, x0, -0.012, 0.07, 0.012, "HYP", fc="#999999")
    ax.text(0.035, -0.03, "patins / coins renforcés [HYP, d'après DOC-005]", fontsize=6.5, color=COUL["HYP"], va="top")
    ax.text(-0.02, 0.5 * H, "poignées\n[HYP]", fontsize=6.5, color=COUL["HYP"], ha="right", va="center")
    # sortie du cordon spiralé, côté droit
    xs = [L + 0.012 + 0.008 * i for i in range(14)]
    ys = [0.55 * H + (0.012 if i % 2 else -0.012) - 0.012 * i for i in range(14)]
    ax.plot(xs, ys, color="black", linewidth=1.2, zorder=5)
    ax.text(L + 0.14, 0.2 * H, "cordon spiralé vers la\ntélécommande [DOC]", fontsize=6.8, va="center")
    cote(ax, (0, -0.075), (L, -0.075), "L = " + pm("L") + " [DÉD sur étalons HYP]", decal=0.006)
    cote(ax, (-0.09, 0), (-0.09, H), "H corps = " + pm("H_corps") + " [DÉD, via L]", decal=0.006, rot=90)
    cote(ax, (-0.16, 0), (-0.16, H + E), "H fermé = " + pm("H_ferme", nd=3) + " [DÉD] (E : 0,242)", decal=0.006, rot=90)
    legende(ax, 0.0, H + E + 0.11)
    ax.text(0.0, -0.12, "Aucune vue de face cotée n'existe dans les documents : hauteur déduite des photographies (H/P = 0,85 ± 0,20).\n"
            "Couleur extérieure sombre (noir ou vert foncé) [DOC photo]. Marquages extérieurs éventuels : inconnus.", fontsize=6.8, va="top")
    finir(fig, ax, "C204 — Plan 2 : vue de face, couvercle fermé (reconstitution)", "plan_02_vue_face",
          (-0.3, L + 0.4), (-0.2, H + E + 0.14))


def plan_cote():
    import math
    fig, ax = plt.subplots(figsize=(8.5, 6.6))
    # Y de gauche (avant) à droite (charnière)
    rect(ax, 0, 0, P, H, "DÉD", fc="#3a3a3a", linewidth=1.8)
    rect(ax, 0, H, P, E, "DÉD", fc="none", linewidth=1.2)
    ax.text(P / 2, H + E / 2, "couvercle fermé", fontsize=6.8, ha="center", va="center", color=COUL["DÉD"])
    # couvercle ouvert : rotation autour de la charnière (P, H)
    for ang, etq, txt in ((105, "DÉD", "ouvert ≈ 105° (DOC-004)"), (125, "HYP", "incliné vers l'arrière ≈ 125°\n(photos du camion ?)")):
        a = math.radians(ang)
        ux, uy = -math.cos(a), math.sin(a)          # direction du panneau depuis la charnière
        nx, ny = -uy, ux                              # normale (épaisseur)
        pts = [(P, H), (P + ux * P, H + uy * P), (P + ux * P + nx * E, H + uy * P + ny * E), (P + nx * E, H + ny * E)]
        st = dict(STYLE[etq])
        ax.add_patch(Polygon(pts, closed=True, facecolor="none", zorder=4, **st))
        ax.text(P + ux * P + 0.02, H + uy * P, txt, fontsize=6.8, color=COUL[etq], va="center")
    cercle(ax, P, H, 0.008, "DOC", fc="black")
    ax.text(P + 0.012, H - 0.015, "charnière sur le grand côté arrière [DOC]", fontsize=6.8, va="top")
    # logements (profil) : positions en profondeur lues sur DOC-007
    for fy in Y_LOG:
        yy = P - fy * P
        rect(ax, yy - D_LOG / 2, H - 0.01, D_LOG, 0.02, "DOC", fc="black", z=5)
        cercle(ax, yy, H - 0.03 - D_LOG * 0.9, D_LOG * 0.9, "HYP")
    ax.text(P * 0.02, H * 0.25, "carters sphériques sous les deux\nouvertures : forme et diamètre [HYP]\n(DOC-008 : « singularity drive housing »)",
            fontsize=6.5, color=COUL["HYP"], va="center", zorder=9,
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.8, pad=1.5))
    rect(ax, 0.02, -0.012, 0.05, 0.012, "HYP", fc="#999999")
    rect(ax, P - 0.07, -0.012, 0.05, 0.012, "HYP", fc="#999999")
    rect(ax, -0.012, H - 0.03, 0.012, 0.05, "DÉD", fc="#bbbbbb")
    ax.text(-0.02, H - 0.005, "fermoir\n[DÉD]", fontsize=6.5, ha="right", va="center", color=COUL["DÉD"])
    cote(ax, (0, -0.06), (P, -0.06), "P = " + pm("P") + " [DÉD, via L]", decal=0.006)
    cote(ax, (-0.1, 0), (-0.1, H), "H = " + pm("H_corps") + " [DÉD, via L]", decal=0.006, rot=90)
    cote(ax, (P + 0.03, H), (P + 0.03, H + E), "e = " + pm("e_couv", nd=3) + "\n(Équipe E : 0,033 m)", decal=0.0, ha="left", va="center")
    ax.text(-0.17, -0.1, "face avant (fermoirs) à gauche ; charnière à droite.\nL'angle d'ouverture réel du couvercle sur les photos n'est pas mesurable avec certitude.",
            fontsize=6.8, va="top")
    legende(ax, -0.17, H + P + 0.12)
    finir(fig, ax, "C204 — Plan 3 : vue de côté (profil), couvercle fermé et ouvert (reconstitution)", "plan_03_vue_cote",
          (-0.22, P + 0.42), (-0.17, H + P + 0.15))


def plan_couvercle_ouvert():
    fig, ax = plt.subplots(figsize=(11, 6.6))
    hc = P  # couvercle vu de face, supposé vertical : hauteur apparente = P
    # corps
    rect(ax, 0, 0, L, H, "DÉD", fc="#3a3a3a", linewidth=1.8)
    for fx in (0.41, 0.75):
        rect(ax, fx * L - 0.012, H - 0.03, 0.024, 0.05, "DÉD", fc="#bbbbbb", z=5)
    # tranche du pont (dessus du corps vu presque par la tranche)
    rect(ax, 0, H, L, 0.02, "DOC", fc="#888888")
    # couvercle levé : face intérieure, d'après DOC-001 (M3.JPG) — fractions mesurées sur la photo
    y0 = H + 0.02
    rect(ax, 0, y0, L, hc, "DOC", fc="#2b2b33", linewidth=1.8)
    # étiquette jaune + petit boîtier gris, à gauche
    rect(ax, 0.04 * L, y0 + 0.72 * hc, 0.06 * L, 0.10 * hc, "DOC", fc="#f0c020")
    rect(ax, 0.05 * L, y0 + 0.45 * hc, 0.05 * L, 0.22 * hc, "DOC", fc="#9a9aa5")
    # bandes de danger (photo : 0,13–0,19 L et 0,43–0,49 L)
    for a, b in ((0.13, 0.19), (0.43, 0.49)):
        bande_danger(ax, a * L, y0 + 0.02 * hc, (b - a) * L, 0.96 * hc)
    # notice blanche à bandeau rouge + étiquette orange
    rect(ax, 0.26 * L, y0 + 0.42 * hc, 0.10 * L, 0.25 * hc, "DOC", fc="white")
    rect(ax, 0.27 * L, y0 + 0.58 * hc, 0.08 * L, 0.07 * hc, "DOC", fc="#c0182b", linewidth=0.5)
    rect(ax, 0.26 * L, y0 + 0.25 * hc, 0.11 * L, 0.12 * hc, "DOC", fc="#f0a030")
    # placard d'instructions (lignes de texte claires sur fond sombre)
    rect(ax, 0.64 * L, y0 + 0.05 * hc, 0.16 * L, 0.83 * hc, "DOC", fc="#555560")
    for i in range(11):
        ax.plot([0.65 * L, 0.79 * L], [y0 + (0.12 + 0.07 * i) * hc] * 2, color="#d8d8d8", linewidth=1.2, zorder=4)
    rect(ax, 0.83 * L, y0 + 0.05 * hc, 0.15 * L, 0.83 * hc, "DOC", fc="#33333b")
    # voyant rouge (DOC-002) à la jonction couvercle / pont, sous le placard
    cercle(ax, 0.66 * L, y0 - 0.01, 0.012, "DOC", fc="#ff3030")
    ax.text(0.30 * L, H - 0.05, "lueur rouge à la jonction couvercle/pont (DOC-002) :\nvoyant ou reflet ? [image DOC ; nature HYP]", fontsize=6.5,
            ha="center", va="top", color="white", zorder=9)
    ax.annotate("", xy=(0.655 * L, y0 - 0.012), xytext=(0.47 * L, H - 0.06), arrowprops=dict(arrowstyle="-|>", color="white", lw=0.8),
                zorder=9)
    # cordon et télécommande
    xs = [0.80 * L - 0.012 * i for i in range(16)]
    ys = [H * 0.9 - 0.022 * i + (0.012 if i % 2 else -0.012) for i in range(16)]
    ax.plot(xs, ys, color="black", linewidth=1.5, zorder=6)
    tl, th = C["tele_l"]["valeur"], C["tele_h"]["valeur"]
    rect(ax, 0.80 * L - 0.012 * 16 - tl, -0.16, tl, th, "DOC", fc="#e8d44d", z=6)
    ax.text(0.80 * L - 0.012 * 16 - tl / 2, -0.17, "télécommande filaire\n(boîtier jaune/noir, clavier) [DOC]", fontsize=6.8,
            ha="center", va="top")
    # annotations
    ax.text(0.07 * L, y0 + hc + 0.012, "étiquette jaune\n+ boîtier [DOC]", fontsize=6.5, ha="center", va="bottom")
    ax.text(0.31 * L, y0 + hc + 0.012, "notice blanche/rouge\n+ étiquette orange [DOC]", fontsize=6.5, ha="center", va="bottom")
    ax.text(0.72 * L, y0 + hc + 0.012, "placard de texte = « UNIT CONTROL\nINSTRUCTIONS » (repère 7 de DOC-007) [DÉD]", fontsize=6.5,
            ha="center", va="bottom", color=COUL["DÉD"])
    cote(ax, (0, y0 + hc + 0.085), (L, y0 + hc + 0.085), "L = " + pm("L") + " [DÉD sur étalons HYP]", decal=0.006)
    cote(ax, (-0.05, y0), (-0.05, y0 + hc), "≈ P (couvercle supposé vertical) [DÉD]", decal=0.006, rot=90)
    legende(ax, L + 0.05, y0 + hc)
    ax.text(L + 0.05, y0 + hc - 0.12,
            "Positions des marquages : mesurées sur\nDOC-001 (copie M3.JPG, 288×216 px).\n"
            "Elles diffèrent du dessin DOC-007 :\n  bandes à 0,13–0,19 L et 0,43–0,49 L (photo)\n  contre 0,14–0,23 L et 0,54–0,63 L (dessin) ;\n"
            "  placard à 0,64–0,80 L (photo)\n  contre 0,71–0,87 L (dessin).\nTexte des étiquettes : illisible à cette résolution.",
            fontsize=6.8, va="top")
    finir(fig, ax, "C204 — Plan 4 : vue de face, couvercle ouvert (d'après les photographies DOC-001/002/003)",
          "plan_04_couvercle_ouvert", (-0.2, L + 0.6), (-0.28, H + P + 0.2))


def plan_interne():
    fig, axes = plt.subplots(2, 1, figsize=(11, 9.4))
    # ---------- Variante A : schéma DOC-008 replié dans l'enveloppe DOC-007 ----------
    ax = axes[0]
    rect(ax, 0, 0, L, P, "DOC", fc="#fbfbfb", linewidth=2.0)

    def num(x, y, t, etq="HYP", fs=8):
        ax.text(x, y, t, fontsize=fs, ha="center", va="center", color=COUL[etq], zorder=9, fontweight="bold",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8))

    R = min(0.20 * P, D_LOG * 0.9)
    for fy in Y_LOG:
        yy = P - fy * P
        cercle(ax, X_LOG * L, yy, D_LOG / 2, "DOC", fc="#222222")
        cercle(ax, X_LOG * L, yy, R, "HYP")
        cercle(ax, X_LOG * L, yy, R * 1.25, "HYP", linewidth=0.8)
    num(X_LOG * L + R * 1.25 + 0.022, P - Y_LOG[0] * P, "1·2·7·8")
    num(X_LOG * L + R * 1.25 + 0.022, P - Y_LOG[1] * P, "1·2·7·8")
    rect(ax, (X_LOG - 0.03) * L, P - 0.45 * P, 0.06 * L, 0.08 * P, "HYP", fc="#ffd9d9")
    num(X_LOG * L, P - 0.41 * P, "4", fs=7)
    rect(ax, 0.03 * L, 0.08 * P, 0.10 * L, 0.84 * P, "HYP", fc="#e6eefc")
    cercle(ax, 0.055 * L, 0.62 * P, 0.022 * L, "HYP")
    cercle(ax, 0.105 * L, 0.62 * P, 0.022 * L, "HYP")
    num(0.08 * L, 0.80 * P, "10")
    rect(ax, 0.05 * L, 0.14 * P, 0.06 * L, 0.2 * P, "HYP", fc="#cfdcf7")
    num(0.08 * L, 0.24 * P, "9")
    rect(ax, 0.14 * L, 0.04 * P, 0.09 * L, 0.92 * P, "HYP", fc="#dddddd", linewidth=0.9)
    num(0.185 * L, 0.5 * P, "12")
    rect(ax, 0.24 * L, 0.06 * P, 0.055 * L, 0.3 * P, "HYP", fc="#ffeccc")
    rect(ax, 0.24 * L, 0.64 * P, 0.055 * L, 0.3 * P, "HYP", fc="#ffeccc")
    num(0.2675 * L, 0.21 * P, "3")
    num(0.2675 * L, 0.79 * P, "3")
    rect(ax, 0.50 * L, 0.1 * P, 0.13 * L, 0.52 * P, "HYP", fc="#eeeeee")
    num(0.565 * L, 0.36 * P, "6")
    rect(ax, 0.50 * L, 0.68 * P, 0.07 * L, 0.24 * P, "HYP", fc="#e8e8e8")
    num(0.535 * L, 0.80 * P, "5")
    rect(ax, 0.64 * L, 0.55 * P, 0.06 * L, 0.38 * P, "HYP", fc="#e2f5e2")
    num(0.67 * L, 0.74 * P, "11")
    rect(ax, 0.71 * L, 0.04 * P, 0.17 * L, 0.92 * P, "DOC", fc="white")
    ax.text(0.795 * L, 0.72 * P, "panneau de commande\n[DOC, DOC-007]", fontsize=6.4, ha="center", va="center")
    rect(ax, 0.72 * L, 0.08 * P, 0.15 * L, 0.34 * P, "HYP", fc="#f3e6ff")
    num(0.795 * L, 0.25 * P, "H·C")
    rect(ax, 0.89 * L, 0.04 * P, 0.10 * L, 0.92 * P, "DOC", fc="#f7f7f7", hatch="..")
    ax.text(0.94 * L, 0.5 * P, "logement\ntélécommande\n[DOC]", fontsize=6.0, ha="center", va="center",
            bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8))
    ax.text(0.5 * L, -0.012,
            "Numéros = repères de DOC-008 :  1 carter de singularité (×2) · 2 bobine de champ magnétique · 3 générateur/régulateur de champ (×2) · "
            "4 collecteur d'injection d'électrons\n5 régulateur d'électrons · 6 générateur d'électrons · 7 capteur d'état · "
            "8 enveloppe de refroidissement · 9 pompe · 10 réservoirs de refroidissement (×2) · 11 capteurs de gravité · 12 batterie\n"
            "H·C = 4 horloges au césium et 3 calculateurs (cités par le texte seulement, absents de DOC-008).   "
            "Seuls l'enveloppe, les deux ouvertures circulaires, le panneau de commande et le logement de télécommande sont [DOC] ; "
            "tout le reste est [HYP].", fontsize=6.3, ha="center", va="top")
    ax.set_title("Variante A — composants de C204-DOC-008 (« BASIC COMPONENTS ») replacés dans l'enveloppe de C204-DOC-007 (vue de dessus)",
                 fontsize=9, loc="left")
    ax.set_xlim(-0.05, L + 0.05)
    ax.set_ylim(-0.11, P + 0.03)
    ax.set_aspect("equal")
    ax.axis("off")
    # ---------- Variante B : lecture de l'écorché DOC-005 ----------
    ax = axes[1]
    rect(ax, 0, 0, L, P, "HYP", fc="#fbfbfb", linewidth=2.0)
    rect(ax, 0.01 * L, 0.05 * P, 0.14 * L, 0.9 * P, "HYP", fc="#eeeeee")
    cercle(ax, 0.10 * L, 0.38 * P, 0.14 * P, "HYP")
    ax.text(0.08 * L, 0.80 * P, "18–19, 1–2 :\ngrand cylindre,\ndisques empilés", fontsize=6.0, ha="center", va="center", color=COUL["HYP"])
    rect(ax, 0.16 * L, 0.55 * P, 0.07 * L, 0.4 * P, "HYP", hatch="----")
    ax.text(0.195 * L, 0.42 * P, "3 : plaques\nempilées", fontsize=6.0, ha="center", va="center", color=COUL["HYP"])
    for (fx, fy) in ((0.27, 0.72), (0.52, 0.76), (0.31, 0.2), (0.60, 0.2)):
        rect(ax, (fx - 0.045) * L, fy * P - 0.16 * P, 0.09 * L, 0.32 * P, "HYP", fc="#f1f1f1")
        for k in range(12):
            import math
            a = 2 * math.pi * k / 12
            ax.plot([fx * L, fx * L + 0.04 * L * math.cos(a)], [fy * P, fy * P + 0.14 * P * math.sin(a)], color=COUL["HYP"],
                    linewidth=0.6, zorder=4)
    ax.text(0.42 * L, P + 0.012, "5, 13, 23–24, 31–32 : quatre blocs à ailettes radiales", fontsize=6.2, ha="center", color=COUL["HYP"])
    rect(ax, 0.36 * L, 0.36 * P, 0.12 * L, 0.22 * P, "HYP", fc="#dddddd")
    cercle(ax, 0.455 * L, 0.42 * P, 0.15 * P, "HYP")
    ax.text(0.455 * L, 0.10 * P, "26–27 : ensemble central\nà couronnes (allure de\nmachine tournante)", fontsize=6.0, ha="center", va="center",
            color=COUL["HYP"], bbox=dict(facecolor="white", edgecolor="none", alpha=0.85, pad=0.8))
    rect(ax, 0.52 * L, 0.34 * P, 0.12 * L, 0.2 * P, "HYP", fc="#dddddd")
    cercle(ax, 0.60 * L, 0.80 * P, 0.11 * P, "HYP")
    cercle(ax, 0.655 * L, 0.70 * P, 0.09 * P, "HYP")
    ax.text(0.63 * L, P + 0.012, "14 : cylindres", fontsize=6.2, ha="center", color=COUL["HYP"])
    rect(ax, 0.72 * L, 0.25 * P, 0.26 * L, 0.7 * P, "HYP", fc="white")
    cercle(ax, 0.80 * L, 0.5 * P, 0.03 * P * 2, "HYP")
    rect(ax, 0.88 * L, 0.42 * P, 0.04 * L, 0.14 * P, "HYP")
    ax.text(0.85 * L, 0.78 * P, "15–17, 35 : panneau supérieur droit\n(bouton sphérique, interrupteur)", fontsize=6.0, ha="center",
            va="center", color=COUL["HYP"])
    ax.text(0.5 * L, -0.02, "Aucun des 35 repères de DOC-005 n'a de légende : toutes les désignations ci-dessus décrivent des formes, pas des fonctions.",
            fontsize=6.6, ha="center", va="top")
    ax.set_title("Variante B — lecture de l'écorché C204-DOC-005 (35 repères sans légende) : entièrement [HYP]", fontsize=9, loc="left")
    ax.set_xlim(-0.05, L + 0.05)
    ax.set_ylim(-0.06, P + 0.04)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.text(0.01, 0.012, AVERT + "  Les deux variantes sont incompatibles entre elles (voir INCOHERENCES.md, I-01).", fontsize=6.5,
             color="#444444")
    fig.suptitle("C204 — Plan 5 : implantation interne — deux hypothèses concurrentes", fontsize=10.5, x=0.01, ha="left")
    fig.savefig(os.path.join(ICI, "plan_05_implantation_interne_hypotheses.svg"), format="svg", bbox_inches="tight")
    fig.savefig(os.path.join(ICI, "plan_05_implantation_interne_hypotheses.png"), format="png", dpi=170, bbox_inches="tight")
    plt.close(fig)
    print("écrit : plan_05_implantation_interne_hypotheses.svg /.png")


if __name__ == "__main__":
    plan_dessus()
    plan_face()
    plan_cote()
    plan_couvercle_ouvert()
    plan_interne()
