#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe I — i06 : figures (calculs illustratifs, pas des mesures).

  figures/figure_de_merite.png   déplacement temporel net par heure, échelle logarithmique, par palier,
                                 comparé aux « 10 ans par heure » revendiqués ;
  figures/R1_scenarios.png       déplacement de l'unité R1 par scénario (ns/h, avec signe) ;
  figures/proximite.png          grille de proximité (quatre axes + indice) ;
  figures/R1_detectabilite.png   rapport signal/bruit par type d'horloge (aller-retour de 48 h).

Méthode graphique : forme choisie avant la couleur ; couleur = identité du palier (palette catégorielle
validée par scripts/validate_palette.js de la compétence « dataviz ») ; sens du déplacement porté par la FORME
du marqueur (jamais par la couleur seule) ; étiquettes directes en encre neutre ; un seul axe par graphique.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from i00_commun import RES, FIG, PALETTE, ENCRE, ENCRE2, SURFACE, GRILLE, DEPL_REVENDIQUE_S_PAR_H

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRILLE, "axes.labelcolor": ENCRE2,
                     "xtick.color": ENCRE2, "ytick.color": ENCRE2, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "savefig.facecolor": SURFACE})

r1 = json.loads((RES / "i01_deplacement.json").read_text(encoding="utf-8"))
r5 = json.loads((RES / "i05_palier3.json").read_text(encoding="utf-8"))
r7 = json.loads((RES / "i07_proximite.json").read_text(encoding="utf-8"))
S = r1["scenarios"]
NOTE = ("Calcul illustratif (scripts i01, i05). Paliers R1 et R2 : effet du TRAJET, identique pour un lest de même masse ; la machine le calcule ou le mesure, "
        "elle n'en est pas la cause. Aucune valeur ne correspond à un déplacement vers le passé.")


def pw(v):
    """Écriture française d'une valeur en s/h."""
    import math
    e = int(math.floor(math.log10(abs(v))))
    m = abs(v) / 10**e
    sup = str(e).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return ("%.1f" % m).replace(".", ",") + "×10" + sup + " s/h"


def figure_de_merite():
    vL = {d["nom"]: d for d in r5["a1_vitesse"]}
    gL = {d["nom"]: d for d in r5["a2_gravite"]}
    kerr = [d for d in r5["a2_gravite"] if "a/M = 0.998" in d["nom"]][0]
    ns = [d for d in r5["a2_gravite"] if "étoile à neutrons" in d["nom"]][0]
    gam_bh = r5["b_trou_noir"]["gamma_final"]["eta=0.44,R=1001"]
    # (libellé, valeur absolue s/h, sens, groupe) ; sens : "futur", "plus" (l'unité vieillit plus), "resolution", "revendique"
    rows = [
        ("C204 revendiquée : « 10 ans par heure » (attribué à la machine)", DEPL_REVENDIQUE_S_PAR_H, "revendique", "revendique"),
        ("C204 telle que décrite : effet PROPRE de ses 227 kg, à 1 m", r1["potentiel_propre_227kg_1m"]["s_par_h"], "futur", "original"),
        ("Variante « deux trous noirs de 4,4×10¹² kg » : effet propre à 1 m", r1["potentiel_2x4.4e12kg_1m"]["s_par_h"], "futur", "original"),
        ("Trajet (R1) — séjour à +1 000 m d'altitude", abs(S["S01"]["D_futur_s_par_h"]), "plus", "R1"),
        ("Trajet (R1) — mine à −1 000 m", S["S04"]["D_futur_s_par_h"], "futur", "R1"),
        ("Trajet (R1) — route, 130 km/h vers l'est", S["S05"]["D_futur_s_par_h"], "futur", "R1"),
        ("Trajet (R1) — train, 320 km/h vers l'est", S["S08"]["D_futur_s_par_h"], "futur", "R1"),
        ("Trajet (R1) — avion de ligne vers l'ouest", abs(S["S11"]["D_futur_s_par_h"]), "plus", "R1"),
        ("Trajet — orbite basse (hors gabarit du véhicule)", S["S20"]["D_futur_s_par_h"], "futur", "R1"),
        ("Trajet (R2) — remorque, 130 km/h vers l'est : même valeur", S["S05"]["D_futur_s_par_h"], "futur", "R2"),
        ("R2 — plus petit décalage MESURABLE (horloges à 10⁻¹⁸)", 3.6e-15, "resolution", "R2"),
        ("R3 — surface d'une étoile à neutrons (aucun équipage)", ns["D_s_par_h"], "futur", "R3"),
        (("R3 — vaisseau à trou noir de 10⁹ kg (γ = %.1f)" % gam_bh).replace(".", ","), (gam_bh - 1) * 3600, "futur", "R3"),
        ("R3 — orbite autour d'un trou noir de Kerr a/M = 0,998", kerr["D_s_par_h"], "futur", "R3"),
        ("R3 — muons en anneau de stockage (particules, γ = 29,3) : réalisé", [d for d in r5["a1_vitesse"] if d["nom"].startswith("Muons")][0]["D_s_par_h"], "futur", "R3"),
        ("R3 — protons du LHC (particules, γ = 7 247) : réalisé", [d for d in r5["a1_vitesse"] if d["nom"].startswith("Protons")][0]["D_s_par_h"], "futur", "R3"),
        ("R3 — électrons du LEP à 45,6 GeV (particules) : réalisé", [d for d in r5["a1_vitesse"] if "45,6" in d["nom"]][0]["D_s_par_h"], "futur", "R3"),
    ]
    n = len(rows)
    fig, ax = plt.subplots(figsize=(13.2, 8.9))
    fig.subplots_adjust(left=0.415, right=0.965, top=0.835, bottom=0.215)
    ax.set_xscale("log")
    ax.set_xlim(1e-23, 1e13)
    ax.set_ylim(n - 0.4, -0.6)
    ax.set_yticks(range(n))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9.6, color=ENCRE)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRILLE, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.axvline(DEPL_REVENDIQUE_S_PAR_H, color=ENCRE2, lw=1.0, ls=(0, (4, 3)), zorder=1)
    mk = {"futur": dict(marker="o", filled=True), "plus": dict(marker="o", filled=False), "resolution": dict(marker="D", filled=False),
          "revendique": dict(marker="s", filled=True)}
    for i, (lab, v, sens, grp) in enumerate(rows):
        col = PALETTE[grp]
        ax.plot([1e-23, v], [i, i], color=col, lw=1.4, alpha=0.55, zorder=2, solid_capstyle="round")
        m = mk[sens]
        ax.plot([v], [i], marker=m["marker"], ms=9.5, mfc=col if m["filled"] else SURFACE, mec=col, mew=2.0, zorder=3, ls="none")
        if v < 1e2 or sens == "revendique":
            ax.text(v * 3.2, i, pw(v), va="center", ha="left", fontsize=9.2, color=ENCRE)
        else:   # à droite du graphique : étiquette à gauche du marqueur, sur fond de surface pour masquer la tige
            ax.text(v / 3.4, i, pw(v), va="center", ha="right", fontsize=9.2, color=ENCRE, zorder=5,
                    bbox=dict(facecolor=SURFACE, edgecolor="none", pad=1.2))
    # séparateurs de groupes
    for y in (0.5, 2.5, 8.5, 10.5):
        ax.axhline(y, color=GRILLE, lw=0.8)
    ax.set_xlabel("Décalage relativiste par heure de trajet, en valeur absolue (secondes par heure, échelle logarithmique)")
    fig.text(0.02, 0.962, "Décalage relativiste subi par tout objet sur ce trajet, par heure", fontsize=14.5, fontweight="bold", color=ENCRE)
    fig.text(0.02, 0.93, "Écart d'horloge entre un objet qui suit le trajet indiqué et une référence restée au sol. La machine n'en est PAS la cause : "
                         "un lest de même masse\nsubit exactement le même décalage. R1-A le calcule, R1-B et R2 le mesurent. Seules les deux lignes orange "
                         "sont un effet propre de l'appareil.\nLes 29 ordres de grandeur jusqu'à la valeur revendiquée ne sont franchis que par des particules en "
                         "accélérateur ; rien ne va vers le passé.", fontsize=9.6, color=ENCRE2, va="top", linespacing=1.35)
    hg = [Line2D([], [], marker="s", ls="none", ms=9, mfc=PALETTE[k], mec=PALETTE[k], label=l) for k, l in
          (("revendique", "revendiqué (non démontré)"), ("original", "effet propre de l'appareil décrit"), ("R1", "trajets accessibles au palier R1 (effet du trajet)"),
           ("R2", "palier R2 (même trajet ; résolution de mesure)"), ("R3", "palier R3 (trajectoires théoriques ou particules)"))]
    hs = [Line2D([], [], marker="o", ls="none", ms=9, mfc=ENCRE2, mec=ENCRE2, label="l'objet vieillit MOINS que la référence"),
          Line2D([], [], marker="o", ls="none", ms=9, mfc=SURFACE, mec=ENCRE2, mew=2, label="l'objet vieillit PLUS que la référence"),
          Line2D([], [], marker="D", ls="none", ms=8, mfc=SURFACE, mec=ENCRE2, mew=2, label="résolution de mesure (ce n'est pas un décalage subi)")]
    l1 = fig.legend(handles=hg, loc="lower left", bbox_to_anchor=(0.02, 0.092), ncol=3, frameon=False, fontsize=9.2, handletextpad=0.3, columnspacing=1.4)
    fig.legend(handles=hs, loc="lower left", bbox_to_anchor=(0.02, 0.052), ncol=3, frameon=False, fontsize=9.2, handletextpad=0.3, columnspacing=1.4)
    fig.add_artist(l1)
    fig.text(0.02, 0.012, NOTE.replace("la machine le calcule", "\nla machine le calcule"), fontsize=8.4, color=ENCRE2, style="italic", linespacing=1.3)
    fig.savefig(FIG / "figure_de_merite.png", dpi=150)
    plt.close(fig)
    return rows


def figure_scenarios():
    ids = sorted(["S11", "S03", "S02", "S09", "S06", "S01", "S07", "S10", "S04", "S05", "S08"], key=lambda i: -S[i]["D_futur_ns_par_h"])
    vals = [S[i]["D_futur_ns_par_h"] for i in ids]
    labs = [S[i]["libelle"] for i in ids]
    BLEU, ORANGE = "#2a78d6", "#eb6834"      # paire divergente (pôles froid / chaud), zéro neutre
    fig, ax = plt.subplots(figsize=(11.6, 5.9))
    fig.subplots_adjust(left=0.40, right=0.95, top=0.82, bottom=0.17)
    for i, (v, l) in enumerate(zip(vals, labs)):
        ax.barh(i, v, height=0.56, color=BLEU if v > 0 else ORANGE, zorder=3, edgecolor=SURFACE, linewidth=2)
        txt = ("%+.2f" % v).replace(".", ",").replace("-", "−") + " ns/h"
        ax.text(v + (0.12 if v > 0 else -0.12), i, txt, va="center", ha="left" if v > 0 else "right", fontsize=9.2, color=ENCRE)
    ax.axvline(0, color=ENCRE2, lw=1.0, zorder=4)
    ax.set_yticks(range(len(ids)))
    ax.set_yticklabels(labs, fontsize=9.4, color=ENCRE)
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-7.6, 2.6)
    ax.xaxis.grid(True, color=GRILLE, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Décalage relativiste du trajet D (nanosecondes par heure) — référence fixe au sol, latitude 45°")
    fig.text(0.02, 0.94, "Décalage relativiste subi par tout objet selon le trajet (trajets accessibles au palier R1)", fontsize=13.5, fontweight="bold", color=ENCRE)
    fig.text(0.02, 0.895, "Propriété du trajet, non de la machine : un lest de même masse a la même valeur. À gauche du zéro l'objet vieillit plus que la\n"
                          "référence (altitude, cap à l'ouest) ; à droite il vieillit moins. Jamais vers le passé. Le cap compte davantage que la vitesse.", fontsize=9.6, color=ENCRE2, va="top")
    h = [Line2D([], [], marker="s", ls="none", ms=9, mfc=BLEU, mec=BLEU, label="D > 0 : l'objet vieillit moins que la référence"),
         Line2D([], [], marker="s", ls="none", ms=9, mfc=ORANGE, mec=ORANGE, label="D < 0 : l'objet vieillit plus que la référence")]
    fig.legend(handles=h, loc="lower left", bbox_to_anchor=(0.02, 0.045), ncol=2, frameon=False, fontsize=9.2)
    fig.text(0.02, 0.012, "Calcul illustratif (script i01) ; contrôles : GPS +38,6 µs/jour, Hafele-Keating, « Project GREAT ».", fontsize=8.4, color=ENCRE2, style="italic")
    fig.savefig(FIG / "R1_scenarios.png", dpi=150)
    plt.close(fig)


def figure_proximite():
    ordre = [("O", "C204 d'origine", "original"), ("R1", "C204-R1", "R1"), ("R2", "C204-R2", "R2"), ("R3", "C204-R3", "R3")]
    axes_ = [("A", "A · Architecture\nconservée"), ("F", "F · Fonctions\nréellement remplies"), ("C", "C · Cohérence\nphysique"), ("D", "D · Constructibilité"),
             ("indice", "Indice de proximité\n(moyenne géométrique)"), ("indice_strict", "Indice strict\n(maillon le plus faible)")]
    fig, axs = plt.subplots(1, 6, figsize=(13.4, 4.5), sharey=True)
    fig.subplots_adjust(left=0.105, right=0.985, top=0.70, bottom=0.12, wspace=0.16)
    for ax, (k, titre) in zip(axs, axes_):
        for i, (c_, lab, col) in enumerate(ordre):
            v = r7[c_][k]
            ax.barh(i, v, height=0.6, color=PALETTE[col], zorder=3, edgecolor=SURFACE, linewidth=2)
            ax.text(v + 3, i, "%.0f" % v, va="center", ha="left", fontsize=9.6, color=ENCRE)
        ax.set_xlim(0, 118)
        ax.set_ylim(3.6, -0.6)
        ax.set_xticks([0, 50, 100])
        ax.xaxis.grid(True, color=GRILLE, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_title(titre, fontsize=9.8, color=ENCRE, loc="left", pad=8)
        for s in ("top", "right", "left"):
            ax.spines[s].set_visible(False)
        ax.tick_params(axis="y", length=0)
    axs[0].set_yticks(range(4))
    axs[0].set_yticklabels([o[1] for o in ordre], fontsize=10, color=ENCRE)
    fig.text(0.02, 0.94, "Proximité à la C204 — NOTES SUBJECTIVES de l'Équipe I : quatre axes sur 100, et deux indices", fontsize=14, fontweight="bold", color=ENCRE)
    fig.text(0.02, 0.885, "Ces chiffres résument des choix de notation, pas une mesure : à ne pas citer sans cette réserve. La machine d'origine garde son architecture mais échoue sur la physique.",
             fontsize=9.6, color=ENCRE2)
    fig.text(0.02, 0.02, "Notes subjectives ; règles : script i07 et grille_proximite_detail.csv. Indice strict = indice × (TRL minimal / 9) × cohérence minimale. "
                         "Le décalage relativiste noté dans F est celui du trajet, pas de la machine.", fontsize=8.4, color=ENCRE2, style="italic")
    fig.savefig(FIG / "proximite.png", dpi=150)
    plt.close(fig)


def figure_detectabilite():
    det = r1["detectabilite_48h"]
    noms = list(det.keys())
    court = ["CSAC au césium (dans le coffre)", "Rubidium miniature nu (dans le coffre)", "Rubidium en enceinte étanche\nthermostatée [à démontrer]",
             "Césium à jet, tube standard\n(hors coffre)", "Césium à jet, haute performance\n(hors coffre)", "Horloge optique à iode de 35 L\n(hors coffre)"]
    v = [det[n]["SB"]["1000"] for n in noms]
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    fig.subplots_adjust(left=0.33, right=0.95, top=0.80, bottom=0.17)
    ax.set_xscale("log")
    for i, x in enumerate(v):
        ax.plot([1e-4, x], [i, i], color=PALETTE["R1"], lw=1.6, alpha=0.6, zorder=2)
        ax.plot([x], [i], "o", ms=10, mfc=PALETTE["R1"] if x >= 3 else SURFACE, mec=PALETTE["R1"], mew=2, zorder=3)
        if 0.4 < x < 3:
            ax.text(x / 1.5, i - 0.28, ("%.3g" % x).replace(".", ","), va="center", ha="right", fontsize=9.4, color=ENCRE)
        else:
            ax.text(x * 1.5, i, ("%.3g" % x).replace(".", ","), va="center", fontsize=9.4, color=ENCRE)
    ax.axvline(3, color=ENCRE2, lw=1.0, ls=(0, (4, 3)))
    ax.text(3.3, len(v) - 0.45, "seuil de détection : 3 σ", fontsize=8.8, color=ENCRE2, va="bottom")
    ax.set_yticks(range(len(v)))
    ax.set_yticklabels(court, fontsize=9.4, color=ENCRE)
    ax.set_ylim(len(v) - 0.4, -0.6)
    ax.set_xlim(1e-4, 300)
    ax.tick_params(axis="y", length=0)
    ax.xaxis.grid(True, color=GRILLE, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_xlabel("Rapport signal / bruit — séjour de 48 h à +1 000 m (signal : 18,8 ns), échelle logarithmique")
    fig.text(0.02, 0.93, "C204-R1 : quelle horloge mesure réellement le déplacement temporel de l'unité ?", fontsize=13.5, fontweight="bold", color=ENCRE)
    fig.text(0.02, 0.875, "Aucune horloge qui entre dans le coffre n'y parvient ; il faut un étalon à jet de césium ou une horloge optique compacte, hors du coffre.",
             fontsize=9.6, color=ENCRE2)
    h = [Line2D([], [], marker="o", ls="none", ms=9, mfc=PALETTE["R1"], mec=PALETTE["R1"], label="détecte (≥ 3 σ)"),
         Line2D([], [], marker="o", ls="none", ms=9, mfc=SURFACE, mec=PALETTE["R1"], mew=2, label="ne détecte pas")]
    fig.legend(handles=h, loc="lower left", bbox_to_anchor=(0.02, 0.045), ncol=2, frameon=False, fontsize=9.2)
    fig.text(0.02, 0.012, "Calcul illustratif (script i01) ; paramètres de bruit : Équipe F (calc01), fiches vérifiées par l'Équipe C, résumé de Roslund et al. 2024.", fontsize=8.4, color=ENCRE2, style="italic")
    fig.savefig(FIG / "R1_detectabilite.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    rows = figure_de_merite()
    figure_scenarios()
    figure_proximite()
    figure_detectabilite()
    # table de données de la figure de mérite (vue tabulaire exigée par la méthode graphique)
    import csv
    with open(FIG.parent / "figure_de_merite_donnees.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["cas", "decalage_relativiste_absolu_s_par_h", "sens", "palier", "cause_du_decalage"])
        cause = {"revendique": "attribué à la machine par le corpus (non démontré)", "original": "effet propre de l'appareil (sa masse)",
                 "R1": "le trajet : tout objet le subit, la machine n'en est pas la cause", "R2": "le trajet : tout objet le subit, la machine n'en est pas la cause",
                 "R3": "la trajectoire ou l'accélérateur (palier théorique)"}
        for lab, v, sens, grp in rows:
            w.writerow([lab, "%.4e" % v, {"futur": "l'objet vieillit moins que la référence", "plus": "l'objet vieillit plus que la référence",
                                           "resolution": "résolution de mesure, pas un décalage subi", "revendique": "revendiqué, non démontré"}[sens], grp,
                        "sans objet (résolution d'instrument)" if sens == "resolution" else cause[grp]])
    print("figures écrites :", sorted(p.name for p in FIG.glob("*.png")))
