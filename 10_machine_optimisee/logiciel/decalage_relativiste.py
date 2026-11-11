#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Décalage relativiste subi par TOUT OBJET le long d'un trajet (Python standard, aucune dépendance).

Ce module est le logiciel de référence du calculateur du projet « C204-R1 ». Il ne décrit AUCUN voyage dans le
temps : il calcule l'écart de marche, de l'ordre de la nanoseconde par heure, entre une horloge qui suit un
trajet (altitude, vitesse, cap) et une horloge identique restée au sol. Cet écart est une propriété du TRAJET :
un lest de même masse, ou le véhicule vide, le subit à l'identique. L'appareil n'en est pas la cause.

Physique (relativité générale, champ faible, vitesses lentes ; formalisme usuel du GPS) — dans le repère
géocentrique non tournant, dτ/dt = 1 − GM/(r c²) − v_I²/(2 c²). Pour un objet à l'altitude h, de vitesse sol
(v_est, v_nord), à la latitude φ, comparé à une référence fixe à l'altitude h_ref sur la même équipotentielle :

    y = [GM/r_ref − GM/r]/c² − [(Ω r cos φ + v_est)² + v_nord² − (Ω r_ref cos φ)²]/(2 c²)

    y > 0 : l'horloge transportée AVANCE (l'objet vieillit un peu PLUS que la référence) ;
    y < 0 : elle RETARDE (l'objet vieillit un peu MOINS).
Dans les deux cas rien ne va vers le passé : seul le rythme relatif de deux horloges change.

Le terme croisé −Ω r cos φ · v_est / c² (effet Sagnac d'une horloge transportée) fait dépendre le signe du CAP :
vers l'est l'horloge retarde, vers l'ouest elle avance (Hafele & Keating 1972).

Limites du modèle : Terre sphérique (g exact à ~0,3 % près), vitesse verticale négligée, séjour souterrain
approché, latitude de la référence prise égale à celle du point courant (horloges au repos sur le géoïde
supposées battre au même rythme). Exactitude visée : ~1 % du décalage, bien au-delà de ce qu'un montage
d'amateur peut mesurer.

Usage :
    python decalage_relativiste.py --scenarios
    python decalage_relativiste.py --trace exemples/trace_montee_1000m.csv
    python decalage_relativiste.py --trace ma_trace.csv --alt-ref 250
Format de trace (CSV à en-tête) : t_s, latitude_deg, altitude_m, vitesse_m_s, cap_deg   (cap : 0 = nord, 90 = est).
"""
import argparse
import csv
import math
import sys

C = 299_792_458.0            # m/s (exact)
GM_TERRE = 3.986004418e14    # m³/s²
R_TERRE = 6.371e6            # m (rayon moyen)
OMEGA_TERRE = 7.2921150e-5   # rad/s

__all__ = ["taux", "taux_cap", "taux_orbite", "integrer", "lire_trace_csv", "trace_constante", "SCENARIOS", "sagnac_ps_par_km"]


def taux(latitude_deg, altitude_m, v_est=0.0, v_nord=0.0, altitude_ref_m=0.0):
    """Écart relatif de marche y (sans dimension) d'un objet par rapport à une référence fixe au sol.

    Renvoie le triplet (y_gravitation, y_cinematique, y_total). Aucun paramètre de masse : la masse de l'objet
    n'intervient pas (un lest subit le même décalage que l'appareil)."""
    phi = math.radians(latitude_deg)
    r_ref = R_TERRE + altitude_ref_m
    r = R_TERRE + altitude_m
    y_grav = (GM_TERRE / r_ref - GM_TERRE / r) / C**2
    v2 = (OMEGA_TERRE * r * math.cos(phi) + v_est) ** 2 + v_nord ** 2
    v2_ref = (OMEGA_TERRE * r_ref * math.cos(phi)) ** 2
    y_cin = -(v2 - v2_ref) / (2 * C**2)
    return y_grav, y_cin, y_grav + y_cin


def taux_cap(latitude_deg, altitude_m, vitesse_m_s=0.0, cap_deg=0.0, altitude_ref_m=0.0):
    """Même calcul avec la vitesse sol et le cap (0° = nord, 90° = est). Renvoie y_total."""
    cap = math.radians(cap_deg)
    return taux(latitude_deg, altitude_m, vitesse_m_s * math.sin(cap), vitesse_m_s * math.cos(cap), altitude_ref_m)[2]


def taux_orbite(altitude_m, latitude_ref_deg=45.0):
    """Orbite circulaire comparée à une référence au sol. Renvoie (y_gravitation, y_cinematique, y_total)."""
    r = R_TERRE + altitude_m
    v = math.sqrt(GM_TERRE / r)
    y_grav = (GM_TERRE / R_TERRE - GM_TERRE / r) / C**2
    y_cin = -(v**2 - (OMEGA_TERRE * R_TERRE * math.cos(math.radians(latitude_ref_deg))) ** 2) / (2 * C**2)
    return y_grav, y_cin, y_grav + y_cin


def sagnac_ps_par_km(latitude_deg):
    """Retard (picosecondes) pris par une horloge par kilomètre parcouru vers l'est, indépendamment de la vitesse."""
    return OMEGA_TERRE * R_TERRE * math.cos(math.radians(latitude_deg)) * 1000.0 / C**2 * 1e12


def integrer(trace, altitude_ref_m=None):
    """Intègre le décalage le long d'une trace.

    trace : suite de points (t_s, latitude_deg, altitude_m, vitesse_m_s, cap_deg), t croissant.
    altitude_ref_m : altitude de la référence restée au sol (par défaut : celle du premier point).
    Renvoie un dictionnaire : durée, écart cumulé (s et ns ; positif = l'horloge transportée avance, l'objet a
    vieilli PLUS que la référence), taux moyen, extrêmes, et la liste des (t, y, cumul)."""
    points = [tuple(float(v) for v in p) for p in trace]
    if len(points) < 2:
        raise ValueError("il faut au moins deux points")
    if any(points[i + 1][0] <= points[i][0] for i in range(len(points) - 1)):
        raise ValueError("les instants doivent être strictement croissants")
    h_ref = points[0][2] if altitude_ref_m is None else float(altitude_ref_m)
    ys = [taux_cap(lat, alt, v, cap, h_ref) for (_t, lat, alt, v, cap) in points]
    cumul, detail = 0.0, [(points[0][0], ys[0], 0.0)]
    for i in range(1, len(points)):
        dt = points[i][0] - points[i - 1][0]
        cumul += 0.5 * (ys[i] + ys[i - 1]) * dt          # méthode des trapèzes
        detail.append((points[i][0], ys[i], cumul))
    duree = points[-1][0] - points[0][0]
    return {
        "duree_s": duree,
        "ecart_cumule_s": cumul,
        "ecart_cumule_ns": cumul * 1e9,
        "taux_moyen": cumul / duree,
        "taux_moyen_ns_par_h": cumul / duree * 3600e9,
        "taux_min": min(ys),
        "taux_max": max(ys),
        "altitude_ref_m": h_ref,
        "sens": ("l'objet a vieilli un peu PLUS que la référence" if cumul > 0 else
                 "l'objet a vieilli un peu MOINS que la référence" if cumul < 0 else "aucun écart"),
        "detail": detail,
    }


def lire_trace_csv(chemin):
    """Lit une trace CSV à en-tête : t_s, latitude_deg, altitude_m, vitesse_m_s, cap_deg."""
    colonnes = ("t_s", "latitude_deg", "altitude_m", "vitesse_m_s", "cap_deg")
    with open(chemin, newline="", encoding="utf-8") as f:
        lecteur = csv.DictReader(f)
        manquantes = [c for c in colonnes if c not in (lecteur.fieldnames or [])]
        if manquantes:
            raise ValueError("colonnes manquantes : " + ", ".join(manquantes))
        return [tuple(float(ligne[c]) for c in colonnes) for ligne in lecteur]


def trace_constante(duree_s, latitude_deg, altitude_m, vitesse_m_s=0.0, cap_deg=0.0, pas_s=60.0):
    """Trace synthétique à état constant (pour les essais)."""
    n = max(1, int(round(duree_s / pas_s)))
    return [(i * duree_s / n, latitude_deg, altitude_m, vitesse_m_s, cap_deg) for i in range(n + 1)]


# Scénarios du rapport (latitude 45°, référence au niveau 0) : identifiant → (libellé, altitude, vitesse, cap,
# avance attendue de l'horloge transportée en ns par heure, valeurs du script i01 du dossier).
SCENARIOS = {
    "S00": ("Parking, à côté de la référence", 0.0, 0.0, 0.0, 0.0000),
    "S01": ("Séjour statique à +1 000 m", 1000.0, 0.0, 0.0, +0.3926),
    "S02": ("Séjour statique à +2 000 m", 2000.0, 0.0, 0.0, +0.7851),
    "S03": ("Séjour statique à +3 000 m", 3000.0, 0.0, 0.0, +1.1775),
    "S04": ("Séjour statique à −1 000 m (mine)", -1000.0, 0.0, 0.0, -0.3927),
    "S05": ("Route, 130 km/h plein est", 0.0, 130 / 3.6, 90.0, -0.5013),
    "S06": ("Route, 130 km/h plein ouest", 0.0, 130 / 3.6, 270.0, +0.4491),
    "S07": ("Route, 130 km/h vers le nord", 0.0, 130 / 3.6, 0.0, -0.0261),
    "S08": ("Train, 320 km/h plein est", 0.0, 320 / 3.6, 90.0, -1.3279),
    "S09": ("Train, 320 km/h plein ouest", 0.0, 320 / 3.6, 270.0, +1.0114),
    "S10": ("Avion, 10,7 km, 250 m/s plein est", 10700.0, 250.0, 90.0, -0.3523),
    "S11": ("Avion, 10,7 km, 250 m/s plein ouest", 10700.0, 250.0, 270.0, +6.2380),
}
LATITUDE_SCENARIOS = 45.0


def _fr(x, n=4):
    return (f"{x:+.{n}f}").replace(".", ",").replace("-", "−")


def afficher_scenarios(sortie=sys.stdout):
    print("Décalage relativiste subi par tout objet sur le trajet (latitude 45°, référence fixe au sol)", file=sortie)
    print("avance > 0 : l'objet vieillit un peu plus que la référence ; avance < 0 : un peu moins. Jamais vers le passé.", file=sortie)
    print(f"{'id':4} {'trajet':40} {'avance de l’horloge (ns/h)':>28} {'sur 48 h (ns)':>15}", file=sortie)
    for cle, (lib, alt, v, cap, _att) in SCENARIOS.items():
        y = taux_cap(LATITUDE_SCENARIOS, alt, v, cap)
        print(f"{cle:4} {lib:40} {_fr(y * 3600e9):>28} {_fr(y * 172800e9, 1):>15}", file=sortie)
    print("Un lest de même masse posé dans le véhicule subit exactement les mêmes valeurs : l'appareil n'en est pas la cause.", file=sortie)


def main(argv=None):
    p = argparse.ArgumentParser(description="Décalage relativiste subi par tout objet le long d'un trajet (ns par heure).")
    p.add_argument("--scenarios", action="store_true", help="affiche les scénarios de référence du rapport")
    p.add_argument("--trace", help="fichier CSV : t_s, latitude_deg, altitude_m, vitesse_m_s, cap_deg")
    p.add_argument("--alt-ref", type=float, default=None, help="altitude de la référence restée au sol (m) ; défaut : premier point")
    a = p.parse_args(argv)
    if not a.scenarios and not a.trace:
        a.scenarios = True
    if a.scenarios:
        afficher_scenarios()
    if a.trace:
        r = integrer(lire_trace_csv(a.trace), a.alt_ref)
        print(f"Trace : {a.trace}")
        print(f"  durée                : {r['duree_s'] / 3600:.2f} h".replace(".", ","))
        print(f"  référence au sol     : altitude {r['altitude_ref_m']:.0f} m")
        print(f"  écart cumulé         : {_fr(r['ecart_cumule_ns'], 3)} ns ({r['sens']})")
        print(f"  taux moyen           : {_fr(r['taux_moyen_ns_par_h'])} ns/h")
        print(f"  taux extrêmes        : {_fr(r['taux_min'] * 3600e9)} à {_fr(r['taux_max'] * 3600e9)} ns/h")
        print("  Rappel : ce décalage est celui du trajet ; un lest de même masse aurait la même valeur.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
