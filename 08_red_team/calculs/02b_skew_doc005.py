#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G — 02b_skew_doc005.py : mesure robuste (Theil-Sen) de l'inclinaison de chaque ligne de texte de DOC-005
(en-tête Courier « RESTRICTED / FILE: TMIM-200S/4005 » et titre sans empattement « MAJOR SYSTEMS DESCRIPTION /
ARMY MODEL GE / C204 ») et des rangées de pastilles de repère. But : tester si titre, en-tête et dessin partagent
la même orientation (même passe d'impression) ou non (collage / surimpression).
Limite : copie JPEG 1023 px ; incertitude estimée par bootstrap.
"""
import numpy as np, cv2
from scipy.stats import theilslopes
P = _RACINE + "/01_archive/originaux/MT7014__johntitor_schematic.jpg"
g = cv2.imread(P, cv2.IMREAD_GRAYSCALE)
rng = np.random.default_rng(0)

def ligne(nom, x0, y0, x1, y1, thr=150):
    sub = g[y0:y1, x0:x1]
    bw = (sub < thr).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(bw, 8)
    pts = np.array([(x0 + st[i, 0] + st[i, 2]/2, y0 + st[i, 1] + st[i, 3]) for i in range(1, n) if st[i, 3] >= 6 and st[i, 4] >= 10])
    if len(pts) < 5:
        print(f"{nom:42s}: trop peu de lettres ({len(pts)})"); return None
    # retire les signes à jambage / ponctuation : garde les bas à ±1,5 px de la médiane locale après un premier ajustement
    s, i0, _, _ = theilslopes(pts[:, 1], pts[:, 0]); r = pts[:, 1] - (i0 + s*pts[:, 0]); pts = pts[np.abs(r - np.median(r)) < 1.6]
    s, i0, lo, hi = theilslopes(pts[:, 1], pts[:, 0], 0.95)
    boot = []
    for _ in range(400):
        k = rng.integers(0, len(pts), len(pts)); 
        if len(np.unique(pts[k, 0])) > 3: boot.append(theilslopes(pts[k, 1], pts[k, 0])[0])
    a = np.degrees(np.arctan(s)); sd = np.degrees(np.std(boot))
    print(f"{nom:42s}: pente = {a:+.2f}° ± {sd:.2f}° (IC95 Theil-Sen {np.degrees(np.arctan(lo)):+.2f}..{np.degrees(np.arctan(hi)):+.2f}) ; {len(pts)} lettres ; étendue {pts[:,0].max()-pts[:,0].min():.0f} px")
    return a, sd

res = {}
res["entete_l1"] = ligne("en-tête ligne 1 « RESTRICTED »", 62, 92, 160, 108)
res["entete_l2"] = ligne("en-tête ligne 2 « FILE: TMIM-200S/4005 »", 62, 108, 232, 124)
res["titre_l1"]  = ligne("titre ligne 1 « MAJOR SYSTEMS DESCRIPTION »", 385, 82, 645, 106)
res["titre_l2"]  = ligne("titre ligne 2 « ARMY MODEL GE / C204 »", 415, 103, 615, 124)

circ = cv2.HoughCircles(cv2.GaussianBlur(g, (3, 3), 0), cv2.HOUGH_GRADIENT, dp=1, minDist=18, param1=120, param2=13, minRadius=5, maxRadius=9)[0]
for nom, (ya, yb) in {"pastilles rangée haute 1": (170, 192), "pastilles rangée haute 2": (215, 238),
                      "pastilles rangée basse 1": (645, 668), "pastilles rangée basse 2": (690, 712)}.items():
    sel = circ[(circ[:, 1] > ya) & (circ[:, 1] < yb)]
    if len(sel) >= 5:
        s, i0, lo, hi = theilslopes(sel[:, 1], sel[:, 0], 0.95)
        print(f"{nom:42s}: pente = {np.degrees(np.arctan(s)):+.2f}° (IC95 {np.degrees(np.arctan(lo)):+.2f}..{np.degrees(np.arctan(hi)):+.2f}) ; {len(sel)} pastilles ; étendue {sel[:,0].max()-sel[:,0].min():.0f} px")
# interligne et hauteur de capitale (cohérence d'échelle)
print("\nDécalage attendu sur 240 px pour 0,5° :", round(240*np.tan(np.radians(0.5)), 2), "px")
