#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Génère les deux traces d'exemple (Python standard). Usage : python generer_exemples.py"""
import csv
import os

ICI = os.path.dirname(os.path.abspath(__file__))
EN_TETE = ["t_s", "latitude_deg", "altitude_m", "vitesse_m_s", "cap_deg"]


def ecrire(nom, points):
    with open(os.path.join(ICI, nom), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(EN_TETE)
        for p in points:
            w.writerow([f"{p[0]:.0f}", f"{p[1]:.4f}", f"{p[2]:.1f}", f"{p[3]:.3f}", f"{p[4]:.1f}"])


# 1. une heure d'autoroute plein est, à plat, à 45° de latitude, un point par minute
ecrire("trace_route_est_1h.csv", [(60 * i, 45.0, 200.0, 130 / 3.6, 90.0) for i in range(61)])

# 2. séjour en altitude : montée de 2 h (de 200 m à 1 200 m, 50 km/h, cap au nord), 44 h sur place, descente de 2 h
pts, pas = [], 300
for i in range(0, 48 * 3600 // pas + 1):
    t = i * pas
    if t <= 7200:
        pts.append((t, 45.0, 200.0 + 1000.0 * t / 7200, 50 / 3.6, 0.0))
    elif t < 46 * 3600:
        pts.append((t, 45.0, 1200.0, 0.0, 0.0))
    else:
        pts.append((t, 45.0, 1200.0 - 1000.0 * (t - 46 * 3600) / 7200, 50 / 3.6, 180.0))
ecrire("trace_montee_1000m.csv", pts)
print("exemples écrits :", sorted(f for f in os.listdir(ICI) if f.endswith(".csv")))
