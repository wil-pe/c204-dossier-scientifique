# -*- coding: utf-8 -*-
"""C204 — Équipe C. Génère le schéma fonctionnel de l'architecture REVENDIQUÉE (../schema_fonctionnel.svg),
colorié selon la faisabilité établie par les calculs c01 à c10. Schéma d'analyse, pas un plan de construction.
"""
import os
from xml.sax.saxutils import escape
import c00_constantes as K

C2 = K.charger_json("c02_confinement.json")
C5 = K.charger_json("c05_refroidissement.json")
C6 = K.charger_json("c06_alimentation.json")
C7 = K.charger_json("c07_capteurs_horloges.json")

W, Hh = 1600, 1175
COUL = {"vert": ("#e3f4e4", "#2e7d32"), "orange": ("#fff0d6", "#c77700"), "rouge": ("#fde0e0", "#c62828"),
        "gris": ("#f2f2f2", "#666666")}
out = []


def boite(x, y, w, h, titre, lignes, classe, repere="", tirets=False):
    fond, trait = COUL[classe]
    dash = ' stroke-dasharray="8 5"' if tirets else ""
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fond}" stroke="{trait}" '
               f'stroke-width="2.2"{dash}/>')
    out.append(f'<text x="{x + 10}" y="{y + 21}" class="t">{escape(titre)}</text>')
    if repere:
        out.append(f'<text x="{x + w - 8}" y="{y + h - 8}" class="r" text-anchor="end">{escape(repere)}</text>')
    for i, li in enumerate(lignes):
        out.append(f'<text x="{x + 10}" y="{y + 41 + 16 * i}" class="l">{escape(li)}</text>')


def fleche(pts, classe, etiquette=None, pos=None):
    d = " ".join(f"{x},{y}" for x, y in pts)
    out.append(f'<polyline points="{d}" class="f {classe}" marker-end="url(#m-{classe})"/>')
    if etiquette:
        x, y = pos if pos else ((pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2 - 5)
        out.append(f'<text x="{x}" y="{y}" class="e {classe}-t" text-anchor="middle">{escape(etiquette)}</text>')


B_req = C2["penning"]["B_min_extremal_T"]
E_lev = C2["E_sustentation_extremal_V_par_m"]
q_ref = C5["charges_thermiques_W"]["réf. x2 : 2 singularités, 400 MW chacune (dépôt γ + e±)"]
blind = C5["blindage_requis_a_1m"]["1 mSv sur le trajet (limite annuelle du public)"]
aux = C6["auxiliaires_W"]
C9 = K.charger_json("c09_structure.json")
m44 = [x for x in C2["par_masse"] if abs(x["M_kg"] - 4.4e12) < 1][0]
fl = C5["flux_parietal_reference"]
blog = C5["blindage_logeable"]
bproche = C5["blindage_logeable_par_direction"]["profondeur, vers la face la plus proche (DOC-007)"]
p38, p49 = (C5["puissance_coffre_a_T_revendiquee_W"][k_] for k_ in ("38 °C", "49 °C"))
dens = sorted(C5["densite_volumique_coffre_MW_par_L"].values())
auto = sorted(d["autonomie_reservoirs_s"] for d in C5["debits"] if "vaporisée" in d["fluide"])
q5071 = C7["quatre_5071A"]
vmv = C9["verdict_masse_volume"]


def fr(x, n=2):
    """Nombre en notation française, n chiffres significatifs."""
    return f"{x:.{n}g}".replace(".", ",")

# ----------------------------------------------------------------------------- en-tête
out.append(f'<text x="{W/2}" y="34" class="titre" text-anchor="middle">C204 — schéma fonctionnel de '
           f"l'architecture revendiquée et faisabilité de chaque bloc</text>")
out.append(f'<text x="{W/2}" y="58" class="sous" text-anchor="middle">Reconstitution d\'analyse (Équipe C) '
           f"d'après DOC-007, DOC-008 et le texte attribué à « John Titor ». Aucune affirmation de la source "
           f"n'est tenue pour vraie ; ce n'est pas un plan de construction.</text>")

# ----------------------------------------------------------------------------- rangée A : commande-contrôle
out.append('<text x="40" y="92" class="bande">COMMANDE-CONTRÔLE</text>')
boite(40, 102, 235, 128, "Télécommande filaire", ["temps de trajet, écart VGL,", "température de l'unité",
      "→ boîtier à cordon spiralé :", "technologie banale"], "vert", "DOC-007 r.3")
boite(300, 102, 265, 128, "Arrêt d'urgence, marche/arrêt", ["coupure, écran de secours", "(ISO 13850 : réalisable)",
      "MAIS aucun état sûr : couper", "n'éteint ni gravité ni rayonnement"], "vert", "DOC-007 r.4-6, 8")
boite(600, 102, 300, 128, "3 calculateurs + vote « Borda »", ["= redondance modulaire triple (TMR)",
      "voteur majoritaire ou médian : classique", "« protocole de Borda » : inconnu de la",
      "littérature ; non tolérant aux fautes"], "vert", "texte")
boite(935, 102, 265, 128, "4 horloges au césium", [f"2000 : 4 x 30 kg = {q5071['fraction_du_volume_coffre']*100:.0f} % du coffre",
      "aujourd'hui : 4 CSAC = 140 g, 0,5 W", "exactitude 5e-13 : insensibles au",
      "potentiel des singularités (≤ 3e-14)"], "vert", "texte")
boite(1235, 102, 325, 128, "Unité de capteurs de gravité (VGL)", ["réel : 1-5 µGal (5 à 150 kg, 20-45 °C)",
      "bloc de 1 m³ à 2 m : 4 µGal → détectable", "à 0,3 m d'une singularité : 22-330 g,",
      "tenue de position requise ~1e-12 m"], "orange", "DOC-008 r.11")

# ----------------------------------------------------------------------------- rangée B : actionneurs
out.append('<text x="40" y="292" class="bande">ACTIONNEURS</text>')
boite(40, 302, 240, 112, "Générateur d'électrons", ["canon thermo-ionique ou", "photocathode, 100 kV x 1 mA",
      "→ 100 W : réalisable"], "vert", "DOC-008 r.6")
boite(310, 302, 225, 112, "Régulateur d'électrons", ["régulation de courant", "et de tension d'accélération",
      "→ réalisable"], "vert", "DOC-008 r.5")
boite(565, 302, 290, 112, "Collecteur d'injection (« masse »)", ["1 % de masse = 5e40 électrons",
      "= 2e14 ans à 1 A ; charge max atteinte", "pour ΔM/M = 4,9e-22 ; barrière", "jusqu'à 1e27 eV"],
      "rouge", "DOC-008 r.4")
boite(985, 302, 295, 112, "Générateurs/régulateurs de champ x2", ["alimentations d'aimants : réalisables",
      "(45 T continu = 30-33 MW réseau)", "sur batterie : aimant supra", "en mode persistant seulement"],
      "orange", "DOC-008 r.3")
boite(1305, 302, 255, 112, "Bobines de champ x2", ["réel : 20-45 T (continu), 100 T (pulsé)",
      f"requis (charge extrémale) : {B_req:.1e} T", "limite des matériaux : ~570 T",
      "trou noir neutre : aucun couplage"], "rouge", "DOC-008 r.2")

# ----------------------------------------------------------------------------- rangée C : singularités
out.append('<text x="40" y="472" class="bande">CŒUR REVENDIQUÉ</text>')
boite(40, 482, 300, 180, "Capteur de singularité", ["« détecte divers paramètres »", "position : en principe mesurable",
      "(gravité 2e4 à 3e5 g à 1 cm)", "mais environnement : > 1e3 Gy/s,", "champ fort, MW thermiques",
      "→ aucun capteur ne survit"], "orange", "DOC-008 r.7")
boite(400, 482, 340, 180, "Carter + SINGULARITÉ PRINCIPALE", ["300-500 MW ⇒ M = 3,9 à 5,1e12 kg",
      "(r_s = 6 à 7,5 fm ; kT = 2,1 à 2,7 MeV)", "poids 4e13 N ; création 4e29 J",
      "100 kg ⇒ durée de vie 4e-13 s", "charge tenable : quelques e (Page 1977)",
      f"sustentation : E ≥ {E_lev:.1e} V/m", "→ IMPOSSIBLE dans 227 kg"], "rouge", "DOC-007 r.1 / DOC-008 r.1")
boite(800, 482, 340, 180, "Carter + SINGULARITÉ DE DIRECTION", ["mêmes impossibilités",
      f"attraction mutuelle à {fr(K.D_PAIRE*100)} cm :",
      f"≈ {round(m44['attraction_mutuelle_sur_poids'], -2):.0f} fois leur poids,",
      f"période orbitale {fr(m44['periode_orbitale_mutuelle_s']*1e3)} ms",
      "orientation de l'axe : précession", "≤ 4e-9 rad/s à 45 T (51 ans/tour)", "→ IMPOSSIBLE"],
      "rouge", "DOC-007 r.2 / DOC-008 r.1")
boite(1200, 482, 360, 180, "« Cône d'évacuation des rayons X »", ["émission réelle : isotrope",
      "55 % neutrinos, 37 % e±, 7,5 % γ", "γ de 5 à 70 MeV : pas des rayons X",
      "collimater = absorber 93 % (cône 30°)", "dans l'axe : ~1000 Gy/h à 100 m",
      "→ CONTREDIT"], "rouge", "DOC-009 r.5")

# ----------------------------------------------------------------------------- rangée D : refroidissement
out.append('<text x="40" y="742" class="bande">THERMIQUE ET RADIOPROTECTION</text>')
boite(40, 752, 290, 128, "Réservoirs de caloporteur x2", ["2 x 0,25 L à l'échelle du schéma",
      f"vaporisés en {fr(auto[0]*1e3, 2)} à {fr(auto[-1]*1e3, 2)} ms",
      "trajet de 6 h en circuit ouvert :", "1500 à 8300 t d'eau"], "orange", "DOC-008 r.10")
boite(365, 752, 250, 128, "Pompe de refroidissement", [f"charge : {q_ref/1e6:.0f} MW (130 à 1000)",
      "eau ΔT 50 K : 0,6 à 4,8 t/s", "puissance pompe : 1 à 6 MW", "(batterie : ~25 kW)"], "orange", "DOC-008 r.9")
boite(650, 752, 320, 128, "Enveloppes de refroidissement x2", [
      f"flux pariétal (r = {fr(K.R_CARTER*100)} cm) : {fr(fl['flux_W_m2']/1e9)} GW/m²",
      f"= {fl['rapport_au_record_CHF']:.0f} x le flux critique record",
      f"coffre : {fr(dens[0])} à {fr(dens[-1])} MW/L (HFIR : 1,7 MW/L)",
      f"38-49 °C ⇒ en réalité {fr(p38/1e3)} à {fr(p49/1e3)} kW"], "orange", "DOC-008 r.8")
boite(1005, 752, 555, 128, "Blindage (absent des documents — exigé par le calcul)", [
      "sans blindage à 1 m : 3300 Gy/s (γ seuls) ; dose létale en ~1 ms",
      f"pour 1 mSv par trajet : {blind['faisceau_etroit']['15 MeV']['epaisseur_plomb_m']*100:.0f} à "
      f"{blind['epaisseur_plomb_m']*100:.0f} cm de plomb (faisceau étroit à large), "
      f"{blind['faisceau_etroit']['15 MeV']['masse_sphere_plomb_kg']/1e3:.0f} à {blind['masse_sphere_plomb_kg']/1e3:.0f} t",
      f"logeable : {fr(bproche['epaisseur_plomb_m']*100)} à {fr(blog['epaisseur_plomb_m']*100)} cm → reste "
      f"{bproche['debit_dose_residuel_photons_1m_Gy_s']:.0f} à {blog['debit_dose_residuel_photons_1m_Gy_s']:.0f} Gy/s",
      "+ neutrons photonucléaires (seuils 6 à 8 MeV dans Pb, W)"], "rouge", "—", tirets=True)

# ----------------------------------------------------------------------------- rangée E : batterie + légende
out.append('<text x="40" y="952" class="bande">ÉNERGIE</text>')
boite(40, 962, 420, 128, "Batterie", [f"auxiliaires réels : {aux['min']:.0f} à {aux['max']:.0f} W → 1,4 à 5,5 kWh/6 h : OK",
      "pack logeable (4 L) : 1,3 kWh ; pack de 50 kg (30 L) : 7,5 kWh",
      "pompe + aimants : 1 à 30 MW → hors de portée",
      f"création des singularités : {fr(C6['creation_2g_J'])} à {fr(C6['creation_scenario_A_J'], 1)} J".replace("e+", "e")],
      "orange", "DOC-008 r.12")

# légende
lx, ly = 500, 962
out.append(f'<rect x="{lx}" y="{ly}" width="1060" height="178" rx="8" fill="#ffffff" stroke="#999" stroke-width="1"/>')
out.append(f'<text x="{lx + 12}" y="{ly + 22}" class="t">Légende</text>')
leg = [("vert", "constructible aujourd'hui et apte à sa fonction déclarée"),
       ("orange", "constructible, mais loin de l'exigence (≥ 3 ordres de grandeur) ou fonction partielle"),
       ("rouge", "fonction impossible ou contredite par la physique connue (démontré par calcul)")]
for i, (cl, tx) in enumerate(leg):
    fond, trait = COUL[cl]
    out.append(f'<rect x="{lx + 14}" y="{ly + 36 + 26 * i}" width="26" height="16" rx="3" fill="{fond}" '
               f'stroke="{trait}" stroke-width="2"/>')
    out.append(f'<text x="{lx + 50}" y="{ly + 49 + 26 * i}" class="l">{escape(tx)}</text>')
fl = [("data", "données / commandes"), ("elec", "faisceau d'électrons"), ("mag", "courant des bobines / champ"),
      ("fluide", "caloporteur"), ("ray", "rayonnement"), ("pwr", "alimentation électrique")]
for i, (cl, tx) in enumerate(fl):
    x0 = lx + 560 + 250 * (i // 3)
    y0 = ly + 44 + 26 * (i % 3)
    out.append(f'<polyline points="{x0},{y0} {x0 + 46},{y0}" class="f {cl}" marker-end="url(#m-{cl})"/>')
    out.append(f'<text x="{x0 + 58}" y="{y0 + 5}" class="l">{escape(tx)}</text>')
out.append(f'<text x="{lx + 12}" y="{ly + 136}" class="t">Périphériques dimensionnés sans contrainte de place : '
           f"{vmv['masse_configuration_genereuse_kg']:.0f} kg (≤ 227 kg) mais {vmv['volume_configuration_genereuse_L']:.0f} L "
           f"pour {vmv['volume_utile_L']:.0f} L utiles ; seule une version réduite tient "
           f"({vmv['configuration_logeable']['masse_kg']:.0f} kg, Équipe I).</text>")
out.append(f'<text x="{lx + 12}" y="{ly + 162}" class="n">Valeurs : scripts calculs/c01 à c10 (résultats dans '
           f"calculs/resultats/). Coffre : {fr(K.COFFRE_L, 3)} x {fr(K.COFFRE_P, 3)} x {fr(K.COFFRE_H, 3)} m (Équipe A). "
           f"r. = repère du document source. [HYP] = hypothèse de l'Équipe C.</text>")

# ----------------------------------------------------------------------------- flèches
# données (les calculateurs commandent aussi la pompe : liaison non tracée pour la lisibilité)
fleche([(1235, 150), (1200, 150)], "data")                       # capteurs de gravité -> même bus que les horloges
fleche([(935, 166), (900, 166)], "data", "bus", (917, 160))      # horloges + capteurs -> calculateurs
fleche([(275, 150), (300, 150)], "data")                         # télécommande -> arrêt d'urgence
fleche([(565, 166), (600, 166)], "data")                         # arrêt d'urgence -> calculateurs
fleche([(40, 572), (20, 572), (20, 258), (620, 258), (620, 230)], "data", "mesures", (330, 252))
fleche([(700, 230), (700, 280), (422, 280), (422, 302)], "data", "consignes", (560, 294))
fleche([(820, 230), (820, 262), (1130, 262), (1130, 302)], "data", "consignes", (975, 256))
# électrons
fleche([(280, 358), (310, 358)], "elec")
fleche([(535, 358), (565, 358)], "elec")
fleche([(650, 414), (650, 482)], "elec", "e⁻", (664, 440))
fleche([(830, 414), (830, 482)], "elec", "e⁻", (844, 440))
# champ
fleche([(1280, 358), (1305, 358)], "mag")
fleche([(1400, 414), (1400, 456), (1060, 456), (1060, 482)], "mag", "B", (1230, 450))
fleche([(1060, 456), (710, 456), (710, 482)], "mag")
# caloporteur
fleche([(330, 816), (365, 816)], "fluide")
fleche([(615, 816), (650, 816)], "fluide")
fleche([(740, 752), (740, 706), (570, 706), (570, 662)], "fluide")
fleche([(880, 752), (880, 706), (970, 706), (970, 662)], "fluide")
# rayonnement
fleche([(1140, 572), (1200, 572)], "ray", "γ, e±, ν", (1170, 564))
fleche([(1090, 662), (1090, 712), (1280, 712), (1280, 752)], "ray", "4π sr", (1186, 706))
# alimentation
fleche([(250, 962), (250, 915), (1540, 915)], "pwr", "bus d'alimentation → tous les blocs", (900, 908))
out.append('<polyline points="250,915 160,915" class="f pwr"/>')
fleche([(160, 915), (160, 880)], "pwr")
fleche([(490, 915), (490, 880)], "pwr")

style = """
  .titre{font:700 21px Helvetica,Arial,sans-serif;fill:#111}
  .sous{font:13px Helvetica,Arial,sans-serif;fill:#444}
  .bande{font:700 12px Helvetica,Arial,sans-serif;fill:#555;letter-spacing:1.5px}
  .t{font:700 14px Helvetica,Arial,sans-serif;fill:#111}
  .r{font:italic 11px Helvetica,Arial,sans-serif;fill:#555}
  .l{font:12.5px Helvetica,Arial,sans-serif;fill:#222}
  .n{font:italic 11.5px Helvetica,Arial,sans-serif;fill:#555}
  .e{font:italic 11.5px Helvetica,Arial,sans-serif}
  .f{fill:none;stroke-width:2}
  .data{stroke:#1565c0;stroke-dasharray:6 4} .data-t{fill:#1565c0}
  .elec{stroke:#6a1b9a} .elec-t{fill:#6a1b9a}
  .mag{stroke:#c77700} .mag-t{fill:#c77700}
  .fluide{stroke:#00838f} .fluide-t{fill:#00838f}
  .ray{stroke:#c62828;stroke-dasharray:2 3} .ray-t{fill:#c62828}
  .pwr{stroke:#444;stroke-width:1.5} .pwr-t{fill:#444}
"""
marqueurs = "".join(
    f'<marker id="m-{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
    f'<path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
    for n, c in (("data", "#1565c0"), ("elec", "#6a1b9a"), ("mag", "#c77700"), ("fluide", "#00838f"),
                 ("ray", "#c62828"), ("pwr", "#444")))
svg = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" '
       f'width="{W}" height="{Hh}" font-family="Helvetica,Arial,sans-serif">\n'
       f'<title>C204 — schéma fonctionnel de l\'architecture revendiquée (analyse de faisabilité)</title>\n'
       f'<defs>{marqueurs}<style>{style}</style></defs>\n'
       f'<rect width="{W}" height="{Hh}" fill="#fafafa"/>\n' + "\n".join(out) + "\n</svg>\n")
chemin = os.path.join(os.path.dirname(K.ICI), "schema_fonctionnel.svg")
with open(chemin, "w", encoding="utf-8") as f:
    f.write(svg)
print("écrit :", chemin, len(svg), "octets")
