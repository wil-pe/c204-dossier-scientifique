#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — génération du simulateur 3D interactif.

    modele_c204.json (Équipe E)                          ┐
    ../10_machine_optimisee/modele_c204_R1.json (Équipe I, lecture seule)  ├─►  simulateur.html
    simulateur_gabarit.html (HTML + CSS + JavaScript)    │
    traductions_en.json (chaînes du modèle en anglais)   ┘

La page est BILINGUE (français / anglais) : les textes d'interface sont dans le gabarit (français dans le HTML,
anglais dans les attributs data-en et dans les couples tx('…', '…') du script) ; les chaînes du modèle (noms de
pièces, fonctions, notes…) restent en français dans les données et leur traduction, lue dans traductions_en.json,
est embarquée à part. Toute chaîne sans traduction est signalée ci-dessous à la génération.

La page produite est un fichier UNIQUE et autonome (données embarquées en JSON ; seule ressource
externe : three.js r128 sur cdnjs, version figée). Quatre modes :
  1. Explorer                    — la C204 telle que décrite (éclatement continu, fiches, niveau de preuve) ;
  2. Si elle fonctionnait        — reconstitution du RÉCIT (frise chronologique), jamais présentée comme réelle ;
  3. Ce que dit la physique      — conséquences réelles des chiffres du récit (formules affichées) ;
  4. C204-R1 (constructible)     — instrument de mesure de l'Équipe I, fonctionnement simulé.

Les coefficients physiques ne sont pas réinventés : ils sont RELUS, à la génération, dans les sorties des
scripts déjà validés (04_ingenierie/calculs/, 03_physique_theorique/verifications/, 10_machine_optimisee/calculs/),
avec repli sur les valeurs publiées par ces équipes si un fichier manque. Les valeurs de contrôle sont
recalculées ici en Python et imprimées ; la page les recalcule en JavaScript avec les mêmes formules.

Usage : python generer_simulateur.py
"""
import json
import math
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
CHAMPS = ("id", "nom", "ensemble", "repere", "source", "classement", "existence", "fonction_revendiquee", "fonction_reelle", "systeme",
          "primitive", "position", "quaternion", "liaison", "eclate", "couleur", "opacite", "couche", "masque", "fantome", "notes", "appui")

# Légendes d'origine (dossier de base §3 ; DOC-008 n°7 : erratum E13 de l'Équipe A, confiance faible)
LEGENDES = {
    "DOC-007": {
        "1": ["MAIN SINGULARITY", "Singularité principale"], "2": ["STEERING SINGULARITY", "Singularité de direction"],
        "3": ["REMOTE CONTROL UNIT", "Télécommande"], "4": ["EMERGENCY VIEW SCREEN", "Écran de visualisation de secours"],
        "5": ["EMERGENCY DISCONNECT", "Coupure d'urgence"], "6": ["MAIN UNIT ON/OFF SWITCH", "Interrupteur général marche/arrêt"],
        "7": ["UNIT CONTROL INSTRUCTIONS", "Instructions de commande de l'unité"], "8": ["EMERGENCY CONTROLS", "Commandes d'urgence"],
        "9": ["REMOTE STORAGE UNIT", "Rangement de la télécommande"]},
    "DOC-008": {
        "1": ["Singularity drive housing", "Carter d'entraînement de singularité"], "2": ["Singularity magnetic field coil", "Bobine de champ magnétique"],
        "3": ["Magnetic field generator / regulator", "Générateur / régulateur de champ magnétique"],
        "4": ["Electron mass injector manifold", "Collecteur d'injection de masse d'électrons"], "5": ["Electron regulator", "Régulateur d'électrons"],
        "6": ["Electron generator", "Générateur d'électrons"],
        "7": ["Singularity sensor booster (ou « status sensor » : lecture de l'Équipe A, confiance faible)", "Amplificateur (ou capteur d'état) de singularité",
              "Singularity sensor booster (or “status sensor”: Team A's reading, low confidence)"],
        "8": ["Singularity cooling housing", "Enveloppe de refroidissement"], "9": ["Singularity cooling pump", "Pompe de refroidissement"],
        "10": ["Singularity cooling supply", "Réserve de fluide de refroidissement"], "11": ["Gravity sensor unit", "Unité de capteurs de gravité"],
        "12": ["Battery supply", "Alimentation par batterie"]},
    "texte": {
        "5": ["Main clocks (4 cesium units)", "Horloges principales (4 au césium)"], "6": ["Main computer units (3)", "Calculateurs principaux (3)"]},
}


def lire(chemin):
    try:
        return Path(chemin).read_text(encoding="utf-8")
    except OSError:
        return None


def coefficients_physiques():
    """Coefficients relus dans les sorties des scripts validés (repli : valeurs publiées par les équipes B et C)."""
    ph = {
        "alpha_M12": 4.4664102375e-4, "f_gamma": 0.0753146696, "f_e": 0.3664375417, "f_nu": 0.5496563126, "f_grav": 0.0085914761,
        "alpha_UV": 4.2148e-3, "muen_cm2_g": 1.441e-2, "E_photon_MeV": 15, "DL50_Gy": [2.5, 5.0], "EPS": 0.9, "T_AMB": 298.15,
        "coffre_C": [0.85, 0.26, 0.285], "charge_utile_kg": [700.0, 1500.0], "sources": {},
    }
    src = ph["sources"]
    t = lire(RACINE / "04_ingenierie/calculs/resultats/c01_hawking.json")
    if t:
        s = json.loads(t)["synthese"]
        ph["alpha_M12"] = s["alpha_M_1e12kg"]
        fr = s["fractions_M_1e12kg"]
        ph.update(f_gamma=fr["photons"], f_e=fr["electrons_positrons"], f_nu=fr["neutrinos"], f_grav=fr["gravitons"])
        src["alpha_M12"] = ["relu dans 04_ingenierie/calculs/resultats/c01_hawking.json (intégration des facteurs de corps gris, comparée à Page 1976)",
                            "read from 04_ingenierie/calculs/resultats/c01_hawking.json (integration of the grey-body factors, compared with Page 1976)"]
    else:
        src["alpha_M12"] = ["valeur publiée par l'Équipe C (fichier c01_hawking.json introuvable à la génération)",
                            "value published by Team C (file c01_hawking.json not found when the page was generated)"]
    t = lire(RACINE / "03_physique_theorique/verifications/sorties/02_hawking_corps_gris.txt")
    m = re.search(r"tout le Modèle standard\)\s*:\s*([0-9.eE+-]+)", t) if t else None
    if m:
        ph["alpha_UV"] = float(m.group(1))
        src["alpha_UV"] = ["relu dans 03_physique_theorique/verifications/sorties/02_hawking_corps_gris.txt",
                           "read from 03_physique_theorique/verifications/sorties/02_hawking_corps_gris.txt"]
    else:
        src["alpha_UV"] = ["valeur publiée par l'Équipe B (sortie introuvable à la génération)",
                           "value published by Team B (output file not found when the page was generated)"]
    t = lire(RACINE / "04_ingenierie/calculs/c05_refroidissement_rayonnement.py")
    if t:
        m = re.search(r"MUEN_EAU\s*=\s*\{([^}]*)\}", t)
        if m:
            table = {int(k): float(v) for k, v in re.findall(r"(\d+)\s*:\s*([0-9.eE+-]+)", m.group(1))}
            if 15 in table:
                ph["muen_cm2_g"] = table[15]
        for cle, motif in (("EPS", r"^EPS\s*=\s*([0-9.]+)"), ("T_AMB", r"^T_AMB\s*=\s*([0-9.]+)")):
            m = re.search(motif, t, re.M)
            if m:
                ph[cle] = float(m.group(1))
        m = re.search(r"^DL50\s*=\s*\(([0-9.]+),\s*([0-9.]+)\)", t, re.M)
        if m:
            ph["DL50_Gy"] = [float(m.group(1)), float(m.group(2))]
        src["dose"] = ["μ_en/ρ de l'eau à 15 MeV (NIST), ε, T₀ et DL50 relus dans 04_ingenierie/calculs/c05_refroidissement_rayonnement.py",
                       "μ_en/ρ of water at 15 MeV (NIST), ε, T₀ and LD50 read from 04_ingenierie/calculs/c05_refroidissement_rayonnement.py"]
    t = lire(RACINE / "04_ingenierie/calculs/c00_constantes.py")
    m = re.search(r"_GEOM\s*=\s*dict\(L=([0-9.]+),\s*P=([0-9.]+),\s*H_ferme=([0-9.]+)", t) if t else None
    if m:
        ph["coffre_C"] = [float(m.group(i)) for i in (1, 2, 3)]
        src["coffre_C"] = ["géométrie figée de l'Équipe C (c00_constantes.py), d'après l'Équipe A",
                           "geometry frozen by Team C (c00_constantes.py), after Team A"]
    t = lire(RACINE / "04_ingenierie/calculs/c09_structure_vehicule.py")
    m = re.search(r"^CHARGE_UTILE\s*=\s*\(([0-9.]+),\s*([0-9.]+)\)", t, re.M) if t else None
    if m:
        ph["charge_utile_kg"] = [float(m.group(1)), float(m.group(2))]
        src["charge_utile_kg"] = ["04_ingenierie/calculs/c09_structure_vehicule.py ([HYP] : pick-up 4×4 des années 1980)",
                                  "04_ingenierie/calculs/c09_structure_vehicule.py ([HYP]: 1980s 4×4 pickup truck)"]
    return ph


def parametres_R1():
    """Paramètres du palier R1 (Équipe I) : relus dans ses scripts quand c'est possible."""
    r1 = {"I_V": 70.0, "tuile_cm": 5.0, "ecart_cm": 10.0, "fibre_m": 500.0, "bobine_m": 0.070, "lambda_m": 1.55e-6, "csac_a": 3e-10, "lat_deg": 45.0,
          "GM_TERRE": 3.986004418e14, "R_TERRE": 6.371e6, "OMEGA_TERRE": 7.2921150e-5, "sources": {}}
    t = lire(RACINE / "10_machine_optimisee/calculs/i03_demonstrateurs_logements.py")
    if t:
        m = re.search(r"I_V\s*=\s*([0-9.]+)", t)
        if m:
            r1["I_V"] = float(m.group(1))
        m = re.search(r"Lf,\s*D,\s*lam\s*=\s*([0-9.]+),\s*([0-9.]+),\s*([0-9.eE+-]+)", t)
        if m:
            r1.update(fibre_m=float(m.group(1)), bobine_m=float(m.group(2)), lambda_m=float(m.group(3)))
        r1["sources"]["i03"] = "relu dans 10_machine_optimisee/calculs/i03_demonstrateurs_logements.py"
    t = lire(RACINE / "10_machine_optimisee/calculs/i00_commun.py")
    if t:
        for cle in ("GM_TERRE", "R_TERRE", "OMEGA_TERRE"):
            m = re.search(rf"^{cle}\s*=\s*([0-9.eE+-]+)", t, re.M)
            if m:
                r1[cle] = float(m.group(1))
        r1["sources"]["i00"] = "relu dans 10_machine_optimisee/calculs/i00_commun.py"
    r1["trajets"] = [   # id, libellé, altitude (m), vitesse vers l'est (m/s), cap affiché (degrés), scénario de i01
        {"id": "route", "nom": "Route vers l'est à 130 km/h", "nom_en": "Road, eastbound at 130 km/h", "h": 0, "vE": 130 / 3.6, "cap": 90, "ref": "S05"},
        {"id": "train", "nom": "Train à 320 km/h vers l'est", "nom_en": "Train, eastbound at 320 km/h", "h": 0, "vE": 320 / 3.6, "cap": 90, "ref": "S08"},
        {"id": "mine", "nom": "Mine à −1 000 m (immobile)", "nom_en": "Mine at −1,000 m (stationary)", "h": -1000, "vE": 0, "cap": 0, "ref": "S04"},
        {"id": "altitude", "nom": "Altitude +1 000 m (immobile)", "nom_en": "Altitude +1,000 m (stationary)", "h": 1000, "vE": 0, "cap": 0, "ref": "S01"},
        {"id": "avion", "nom": "Avion vers l'ouest (10,7 km, 250 m/s)", "nom_en": "Aircraft, westbound (10.7 km, 250 m/s)", "h": 10700, "vE": -250, "cap": 270, "ref": "S11"},
    ]
    return r1


# ------------------------------------------------------------------------------------------------
# Valeurs de contrôle recalculées en Python (mêmes formules que la page)
# ------------------------------------------------------------------------------------------------
G, c, hbar, sigma, g0 = 6.67430e-11, 299792458.0, 1.054571817e-34, 5.670374419e-8, 9.80665


def taux_trajet(r1, h, vE, vN=0.0):
    phi = math.radians(r1["lat_deg"])
    r0, r = r1["R_TERRE"], r1["R_TERRE"] + h
    grav = (r1["GM_TERRE"] / r0 - r1["GM_TERRE"] / r) / c**2
    cin = -((r1["OMEGA_TERRE"] * r * math.cos(phi) + vE)**2 + vN**2 - (r1["OMEGA_TERRE"] * r0 * math.cos(phi))**2) / (2 * c**2)
    return grav + cin


def facteur_geometrique(a, d, n=400):
    """G = ∫∫ (a−|u|)(a−|v|)·d⁴/(u²+v²+d²)³ du dv sur [−a, a]² (cm²·sr) : deux tuiles carrées coaxiales, flux en cos²θ."""
    s, pas = 0.0, 2 * a / n
    for i in range(n):
        u = -a + (i + 0.5) * pas
        for j in range(n):
            v = -a + (j + 0.5) * pas
            s += (a - abs(u)) * (a - abs(v)) * d**4 / (u * u + v * v + d * d)**3
    return s * pas * pas


def controles(ph, r1):
    K = hbar * c**6 / G**2
    PM2 = ph["alpha_M12"] * K
    M300, M500, M400 = (math.sqrt(PM2 / P) for P in (300e6, 500e6, 400e6))
    muen = ph["muen_cm2_g"] * 0.1
    L, P_, H = ph["coffre_C"]
    out = {
        "P·M² (W·kg²)": PM2, "M(300 MW) kg": M300, "M(500 MW) kg": M500,
        "g à 1 m, 2 singularités de 500 MW (g)": G * 2 * M500 / g0, "g à 1 m, 2 singularités de 300 MW (g)": G * 2 * M300 / g0,
        "dose photons 1 singularité 400 MW à 1 m (Gy/s)": ph["f_gamma"] * 400e6 / (4 * math.pi) * muen,
        "dose photons 1 singularité 400 MW à 3 m (Gy/s)": ph["f_gamma"] * 400e6 / (4 * math.pi * 9) * muen,
        "surface du coffre (m²)": 2 * (L * P_ + L * H + P_ * H),
        "Γ−1 à 0,5 m (2 × 300 MW)": G * 2 * M300 / (0.5 * c**2), "Γ−1 à 4 m (2 × 500 MW)": G * 2 * M500 / (4 * c**2),
        "durée de vie 113,5 kg (s)": G**2 * 113.5**3 / (3 * ph["alpha_UV"] * hbar * c**4),
        "énergie de 227 kg (J)": 227.0 * c**2,
        "muons par heure": r1["I_V"] * facteur_geometrique(r1["tuile_cm"], r1["ecart_cm"]) * 1e-4 * 3600,
        "Sagnac 2πLD/(λc) (s)": 2 * math.pi * r1["fibre_m"] * r1["bobine_m"] / (r1["lambda_m"] * c),
    }
    for t in r1["trajets"]:
        out[f"trajet {t['id']} (ns/h, avance de l'horloge embarquée)"] = taux_trajet(r1, t["h"], t["vE"]) * 3600e9
    return out


# ------------------------------------------------------------------------------------------------
# Traduction anglaise des chaînes du modèle
# ------------------------------------------------------------------------------------------------
CHAMPS_TRADUITS = ("nom", "repere", "source", "existence", "appui", "fonction_revendiquee", "fonction_reelle", "notes")


def _norm(s):
    return s.replace(" ", " ").replace(" ", " ")


def table_anglaise(donnees):
    """Renvoie ({chaîne française: chaîne anglaise}, [chaînes sans traduction]) pour tout ce que la page affiche du modèle."""
    t = json.loads((ICI / "traductions_en.json").read_text(encoding="utf-8"))
    exact = {_norm(k): v for k, v in t["exact"].items()}
    regles = [(re.compile(m), r) for m, r in t["regles"]]
    chaines = []
    pieces = list(donnees["A"]["pieces"]) + list((donnees.get("R1") or {}).get("internes") or []) + list((donnees.get("R1") or {}).get("enveloppe") or [])
    for p in pieces:
        chaines += [p[c] for c in CHAMPS_TRADUITS if p.get(c)]
    for c in donnees["classements"].values():
        chaines += [c[k] for k in ("libelle", "definition") if c.get(k)]
    en, manquantes = {}, []
    for s in dict.fromkeys(chaines):
        n = _norm(s)
        if n in exact:
            en[s] = exact[n]
            continue
        for motif, rempl in regles:
            if motif.fullmatch(n):
                en[s] = motif.sub(rempl, n)
                break
        else:
            manquantes.append(s)
    return {k: v for k, v in en.items() if v != k}, manquantes


def reduire(p):
    return {k: p[k] for k in CHAMPS if k in p}


def main():
    modele = json.loads((ICI / "modele_c204.json").read_text(encoding="utf-8"))
    A = modele["variantes"]["A"]
    donnees = {
        "genere_le": modele["meta"]["genere_le"],
        "avertissement": modele["meta"]["avertissement"],
        "classements": dict(modele["meta"]["classements"]),
        "systemes": dict(modele["meta"]["systemes"]),
        "echelle": {"L": modele["cotes"]["L"]["valeur"], "incertitude": modele["cotes"]["L"]["incertitude"]},
        "A": {"pieces": [reduire(p) for p in A["pieces"]], "etats": A["etats"], "articulations": A["articulations"], "cotes_cles": A["cotes_cles"],
              "bilan_classement": A["bilan_classement"], "bilan_couches": A["bilan_couches"], "bilan_volumique": A["bilan_volumique"]},
        "legendes": LEGENDES,
        "phys": coefficients_physiques(),
        "r1p": parametres_R1(),
    }
    # --- modèle R1 de l'Équipe I (lecture seule) : on n'embarque que ses 34 composants si l'enveloppe est bien la nôtre
    t = lire(RACINE / "10_machine_optimisee/modele_c204_R1.json")
    if t:
        mr = json.loads(t)
        R = mr["variantes"]["R1A"]
        parA = {p["id"]: p for p in A["pieces"]}
        cles = ("nom", "primitive", "position", "quaternion", "eclate", "couche", "liaison", "classement")
        reprises = [p for p in R["pieces"] if p["id"].startswith("E-")]
        identiques = all(p["id"][2:] in parA and all(json.dumps(p[k], sort_keys=True) == json.dumps(parA[p["id"][2:]][k], sort_keys=True) for k in cles)
                         for p in reprises)
        donnees["classements"].update({k: v for k, v in mr["meta"]["classements"].items() if k not in donnees["classements"]})
        donnees["R1"] = {"nom": R["nom"], "avertissement": mr["meta"]["avertissement"], "systemes": mr["meta"]["systemes"], "etats": R["etats"],
                         "articulations": R["articulations"], "bilan_volumique": R.get("bilan_volumique"),
                         "internes": [reduire(p) for p in R["pieces"] if not p["id"].startswith("E-")]}
        if identiques:
            donnees["R1"]["reprises"] = [p["id"][2:] for p in reprises]
        else:
            donnees["R1"]["enveloppe"] = [reduire(p) for p in reprises]
        print(f"modèle R1 : {len(donnees['R1']['internes'])} composants de l'Équipe I ; enveloppe {'identique à la nôtre (non dupliquée)' if identiques else 'DIFFÉRENTE : embarquée telle quelle'}")
    else:
        donnees["R1"] = None
        print("ATTENTION : 10_machine_optimisee/modele_c204_R1.json introuvable — le mode 4 affichera un message")

    donnees["en"], manquantes = table_anglaise(donnees)
    print(f"traduction anglaise : {len(donnees['en'])} chaînes du modèle traduites" + ("" if not manquantes else f" ; ATTENTION, {len(manquantes)} SANS TRADUCTION (elles resteront en français dans la page) :"))
    for s in manquantes:
        print("   - " + s)

    ctl = controles(donnees["phys"], donnees["r1p"])
    print("valeurs de contrôle (Python, mêmes formules que la page) :")
    for k, v in ctl.items():
        print(f"   {k:58s} {v:.4g}")
    donnees["controles_python"] = {k: float(f"{v:.6g}") for k, v in ctl.items()}

    gabarit = (ICI / "simulateur_gabarit.html").read_text(encoding="utf-8")
    brut = json.dumps(donnees, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    ech = ("%.2f m ± %.2f m" % (donnees["echelle"]["L"], donnees["echelle"]["incertitude"])).replace(".", ",")
    assert gabarit.count("__DONNEES__") == 1
    html = gabarit.replace("__DONNEES__", brut).replace("__ECHELLE__", ech).replace("__DATE__", donnees["genere_le"])
    (ICI / "simulateur.html").write_text(html, encoding="utf-8")
    print("écrit : simulateur.html (%.0f ko)" % (len(html.encode("utf-8")) / 1024))


if __name__ == "__main__":
    main()
