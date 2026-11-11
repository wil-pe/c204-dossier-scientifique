#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G (red team) — Programme C204
02_analyse_images.py : examen critique élémentaire des documents graphiques (lecture seule des originaux).

  1. Structure JPEG : marqueurs, tables de quantification -> qualité estimée, sous-échantillonnage chromatique.
  2. Analyse des niveaux d'erreur (ELA) : recompression à Q=90, différence amplifiée, statistiques par zones.
  3. Bruit local (résidu passe-haut) par blocs sur les photos.
  4. DOC-005 : inclinaison (skew) comparée du titre, de l'en-tête et du bord de numérisation.
  5. DOC-007 vs photos : proportions (rapport L/P du coffre, position des bandes de danger et du panneau de texte).
  6. Agrandissements de contrôle (DOC-009 : texte interne, repères 5/6 ; DOC-006 : dates).

LIMITES (à répéter dans le rapport) : les fichiers sont des copies de copies (forum de 2023), recompressées, de
239 à 1023 px de large. L'ELA et l'analyse de bruit ne peuvent PAS, sur un tel matériau, prouver ni exclure une
retouche de l'original de 2000 : elles ne détectent que des hétérogénéités postérieures à la dernière compression
globale. Un résultat « homogène » n'innocente rien ; un résultat « hétérogène » aux bords contrastés est attendu.
"""
import os, io, json, struct
import numpy as np
from PIL import Image, ImageChops
import cv2

ORIG = _RACINE + "/01_archive/originaux"
OUT  = _RACINE + "/08_red_team/figures"
os.makedirs(OUT, exist_ok=True)
FILES = sorted(f for f in os.listdir(ORIG) if f.lower().endswith((".jpg", ".jpeg", ".png")))
R = {}

def titre(s): print("\n" + "="*96 + "\n" + s + "\n" + "="*96)

# ----------------------------------------------------------------------------- 1. structure JPEG
titre("1. Structure des fichiers")
STD_LUM = np.array([16,11,10,16,24,40,51,61,12,12,14,19,26,58,60,55,14,13,16,24,40,57,69,56,14,17,22,29,51,87,80,62,
                    18,22,37,56,68,109,103,77,24,35,55,64,81,104,113,92,49,64,78,87,103,121,120,101,72,92,95,98,112,100,103,99], float)
def qualite_ijg(qt):
    """Estime la qualité IJG à partir de la table de luminance (moyenne du rapport à la table standard)."""
    q = np.array(qt, float)
    s = 100*np.mean(q)/np.mean(STD_LUM)          # facteur d'échelle approx.
    return (200 - s)/2 if s <= 100 else 5000/s

def marqueurs(path):
    b = open(path, "rb").read(); out = []; i = 2
    while i < len(b)-4 and b[i] == 0xFF:
        m = b[i+1]; L = struct.unpack(">H", b[i+2:i+4])[0]
        seg = b[i+4:i+2+L]
        nom = {0xE0:"APP0", 0xE1:"APP1", 0xE2:"APP2", 0xED:"APP13", 0xEE:"APP14", 0xFE:"COM", 0xDB:"DQT", 0xC0:"SOF0(baseline)",
               0xC2:"SOF2(progressif)", 0xC4:"DHT", 0xDA:"SOS", 0xDD:"DRI"}.get(m, hex(m))
        ident = seg[:12].split(b"\x00")[0].decode("latin1", "replace") if nom.startswith(("APP", "COM")) else ""
        out.append(nom + (f"[{ident}]" if ident else ""))
        if m == 0xDA: break
        i += 2 + L
    return out

for f in FILES:
    p = os.path.join(ORIG, f); im = Image.open(p)
    info = dict(taille=im.size, mode=im.mode, format=im.format, octets=os.path.getsize(p))
    if im.format == "JPEG":
        qt = im.quantization
        info["qualite_estimee"] = round(float(qualite_ijg(qt[0])), 1)
        info["n_tables"] = len(qt)
        info["marqueurs"] = marqueurs(p)
        info["sous_echantillonnage"] = {(1,1):"4:4:4", (2,1):"4:2:2", (2,2):"4:2:0"}.get(
            tuple(getattr(im, "layer", [(0,1,1,0)])[0][1:3]), str(getattr(im, "layer", "")))
        info["exif"] = bool(im.getexif())
        info["bpp"] = round(8*info["octets"]/(im.size[0]*im.size[1]), 2)
    else:
        info["palette"] = im.mode == "P"; info["info"] = {k: str(v)[:60] for k, v in im.info.items()}
    R[f] = info
    print(f"{f:44s} {info['taille']} {info['mode']:4s} {info['octets']:6d} o | " +
          (f"Q≈{info['qualite_estimee']} | {info['sous_echantillonnage']} | {info['bpp']} bit/px | EXIF={info['exif']} | {' '.join(info['marqueurs'][:6])}"
           if im.format == "JPEG" else f"PNG palette={info['palette']} {info['info']}"))

# ----------------------------------------------------------------------------- 2. ELA
titre("2. Analyse des niveaux d'erreur (ELA, recompression Q=90)")
def ela(path, q=90):
    im = Image.open(path).convert("RGB")
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=q); buf.seek(0)
    d = np.asarray(ImageChops.difference(im, Image.open(buf).convert("RGB")), float).max(axis=2)
    return np.asarray(im), d

def blocs(a, n=16):
    h, w = a.shape[:2]; H, W = h//n, w//n
    return a[:H*n, :W*n].reshape(H, n, W, n).swapaxes(1, 2).reshape(H, W, -1)

photos = [f for f in FILES if "JT" in f]
for f in [x for x in FILES if x.lower().endswith((".jpg", ".jpeg"))]:
    rgb, d = ela(os.path.join(ORIG, f))
    b = blocs(d).mean(axis=2)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(float)
    grad = blocs(np.hypot(cv2.Sobel(gray, cv2.CV_64F, 1, 0), cv2.Sobel(gray, cv2.CV_64F, 0, 1))).mean(axis=2)
    rho = float(np.corrcoef(b.ravel(), grad.ravel())[0, 1])
    z = (b - np.median(b))/(1.4826*np.median(np.abs(b - np.median(b))) + 1e-9)
    # blocs « anormaux » : ELA très supérieure à ce que prédit le contraste local (régression linéaire)
    A = np.vstack([grad.ravel(), np.ones(grad.size)]).T
    coef, *_ = np.linalg.lstsq(A, b.ravel(), rcond=None)
    res = b.ravel() - A @ coef
    zr = (res - np.median(res))/(1.4826*np.median(np.abs(res - np.median(res))) + 1e-9)
    n_out = int((zr > 6).sum())
    R[f]["ela"] = dict(moyenne=float(d.mean()), max=float(d.max()), corr_ELA_contraste=rho, blocs_residu_z_sup_6=n_out, n_blocs=int(b.size))
    print(f"{f:44s} ELA moy={d.mean():5.2f} max={d.max():4.0f} | corrélation ELA/contraste local = {rho:+.2f} | "
          f"blocs 16 px à résidu > 6 sigma : {n_out}/{b.size}")
    vis = np.clip(d*12, 0, 255).astype(np.uint8)
    k = max(1, 900//rgb.shape[1])
    pan = np.hstack([cv2.resize(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), None, fx=k, fy=k, interpolation=cv2.INTER_NEAREST),
                     cv2.resize(cv2.applyColorMap(vis, cv2.COLORMAP_INFERNO), None, fx=k, fy=k, interpolation=cv2.INTER_NEAREST)])
    cv2.imwrite(os.path.join(OUT, "ELA_" + os.path.splitext(f)[0] + ".png"), pan)

# ----------------------------------------------------------------------------- 3. bruit local des photos
titre("3. Bruit local (résidu médian 3x3) sur les photos : zones « étiquettes/bandes » vs reste")
for f in photos:
    bgr = cv2.imread(os.path.join(ORIG, f)); gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(float)
    resid = gray - cv2.medianBlur(gray.astype(np.uint8), 3).astype(float)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    jaune = ((hsv[..., 0] > 18) & (hsv[..., 0] < 40) & (hsv[..., 1] > 60) & (hsv[..., 2] > 110))
    frac = float(jaune.mean())
    s_j = float(resid[jaune].std()) if jaune.sum() > 30 else float("nan")
    s_r = float(resid[~jaune].std())
    # netteté : largeur des transitions des bandes (gradient max) comparée au reste
    g = np.hypot(cv2.Sobel(gray, cv2.CV_64F, 1, 0), cv2.Sobel(gray, cv2.CV_64F, 0, 1))
    dil = cv2.dilate(jaune.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    p99_j = float(np.percentile(g[dil], 99)) if dil.sum() > 30 else float("nan")
    p99_r = float(np.percentile(g[~dil], 99))
    R[f]["bruit"] = dict(fraction_jaune=frac, sigma_resid_jaune=s_j, sigma_resid_reste=s_r, grad99_jaune=p99_j, grad99_reste=p99_r)
    print(f"{f:28s} pixels jaunes {100*frac:4.1f} % | sigma résidu : jaune {s_j:.2f} / reste {s_r:.2f} | "
          f"gradient p99 : bandes {p99_j:.0f} / reste {p99_r:.0f}")
    # centres des bandes jaunes (profil en colonnes dans la moitié haute)
    prof = jaune[: gray.shape[0]*2//3].sum(axis=0).astype(float)
    prof = np.convolve(prof, np.ones(5)/5, mode="same")
    thr = 0.35*prof.max(); seg = []; inside = False
    for x, v in enumerate(prof):
        if v > thr and not inside: x0 = x; inside = True
        if (v <= thr or x == len(prof)-1) and inside:
            inside = False
            if x - x0 >= 4: seg.append((x0, x, float(np.average(np.arange(x0, x), weights=prof[x0:x]))))
    R[f]["bandes_jaunes_x"] = seg
    print("      segments de bandes jaunes (x0, x1, centre) en px :", [(a, b, round(c_, 1)) for a, b, c_ in seg])

# ----------------------------------------------------------------------------- 4. DOC-005 : inclinaisons
titre("4. DOC-005 (écorché) : inclinaison du titre, de l'en-tête et du bord de page")
f5 = [f for f in FILES if "7014" in f][0]
g5 = cv2.imread(os.path.join(ORIG, f5), cv2.IMREAD_GRAYSCALE)
def angle_lignes_texte(roi, nom):
    """Angle de la ligne de base : régression sur le BAS des composantes connexes (lettres) de chaque ligne."""
    x0, y0, x1, y1 = roi; sub = g5[y0:y1, x0:x1]
    _, bw = cv2.threshold(sub, 140, 255, cv2.THRESH_BINARY_INV)
    n, lab, st, cen = cv2.connectedComponentsWithStats(bw, 8)
    comps = [(st[i, 0] + st[i, 2]/2, st[i, 1] + st[i, 3], st[i, 3]) for i in range(1, n) if 5 <= st[i, 3] <= 30 and st[i, 4] > 8]
    if len(comps) < 6: return None
    comps = np.array(comps)
    # sépare les lignes par k-moyennes 1D sur y (2 lignes)
    ys = comps[:, 1]; med = np.median(ys); res = []
    for sel in (ys <= med, ys > med):
        c_ = comps[sel]
        if len(c_) < 5: continue
        # garde les lettres sans jambage : bas proche de la médiane de la ligne
        for _ in range(3):
            pfit = np.polyfit(c_[:, 0], c_[:, 1], 1); r_ = c_[:, 1] - np.polyval(pfit, c_[:, 0])
            c_ = c_[np.abs(r_) < max(1.0, 1.5*np.std(r_))]
        res.append((np.degrees(np.arctan(pfit[0])), len(c_), float(np.std(c_[:, 1] - np.polyval(pfit, c_[:, 0])))))
    for a, n_, s_ in res: print(f"   {nom:34s}: pente = {a:+.2f}°  ({n_} lettres, résidu {s_:.2f} px)")
    return [r_[0] for r_ in res]
aT = angle_lignes_texte((380, 80, 650, 125), "titre (Arial gras, 2 lignes)")
aH = angle_lignes_texte((60, 90, 240, 125), "en-tête RESTRICTED / FILE (Courier)")
# bord de numérisation : bande sombre en haut de l'image
top = g5[:40, 100:900]; ys_edge = []
for x in range(0, top.shape[1], 8):
    col = top[:, x].astype(float); idx = np.where(col < 128)[0]
    if len(idx): ys_edge.append((x, idx.max()))
if len(ys_edge) > 10:
    e = np.array(ys_edge); pe = np.polyfit(e[:, 0], e[:, 1], 1)
    print(f"   bord sombre supérieur de la numérisation : pente = {np.degrees(np.arctan(pe[0])):+.2f}°")
    aB = float(np.degrees(np.arctan(pe[0])))
else:
    aB = None; print("   bord supérieur : non mesurable")
# pastilles de repère : alignement des rangées (rangée basse 19..35 et rangée haute)
circ = cv2.HoughCircles(cv2.GaussianBlur(g5, (3, 3), 0), cv2.HOUGH_GRADIENT, dp=1, minDist=18, param1=120, param2=13, minRadius=5, maxRadius=9)
if circ is not None:
    cc = circ[0]; bas = cc[(cc[:, 1] > 640) & (cc[:, 1] < 720)];
    for nom, sel in (("rangée de repères du bas (y≈700)", cc[(cc[:, 1] > 690) & (cc[:, 1] < 712)]),
                     ("rangée de repères du bas (y≈655)", cc[(cc[:, 1] > 645) & (cc[:, 1] < 668)]),
                     ("rangée de repères du haut (y≈180)", cc[(cc[:, 1] > 170) & (cc[:, 1] < 192)]),
                     ("rangée de repères du haut (y≈225)", cc[(cc[:, 1] > 215) & (cc[:, 1] < 238)])):
        if len(sel) >= 4:
            pc = np.polyfit(sel[:, 0], sel[:, 1], 1)
            print(f"   {nom:34s}: pente = {np.degrees(np.arctan(pc[0])):+.2f}°  ({len(sel)} pastilles)")
            R.setdefault("DOC005_skew", {})[nom] = float(np.degrees(np.arctan(pc[0])))
R.setdefault("DOC005_skew", {}).update(titre=aT, entete=aH, bord=aB)

# ----------------------------------------------------------------------------- 5. proportions DOC-007 vs photos
titre("5. Proportions : DOC-007 (vue de dessus) et photos")
f7 = [f for f in FILES if "7016" in f][0]
g7 = cv2.imread(os.path.join(ORIG, f7), cv2.IMREAD_GRAYSCALE)
_, bw7 = cv2.threshold(g7, 110, 255, cv2.THRESH_BINARY_INV)
# le coffre = deux grands rectangles arrondis ; on isole par contours externes hors cadre
cnts, _ = cv2.findContours(bw7, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
rects = sorted([cv2.boundingRect(c_) for c_ in cnts if 0.6*g7.shape[1] < cv2.boundingRect(c_)[2] < 0.9*g7.shape[1]
                and 60 < cv2.boundingRect(c_)[3] < 0.5*g7.shape[0]], key=lambda r_: r_[1])
print("   rectangles candidats (x, y, l, h) :", rects[:6])
if rects:
    for r_ in rects[:4]:
        print(f"      L/P = {r_[2]/r_[3]:.2f}")
# puits circulaires noirs (singularités) : composantes sombres compactes
n, lab, st, cen = cv2.connectedComponentsWithStats((g7 < 60).astype(np.uint8), 8)
disks = [(cen[i][0], cen[i][1], st[i, 2], st[i, 3], st[i, 4]) for i in range(1, n)
         if 22 <= st[i, 2] <= 50 and 0.8 < st[i, 2]/st[i, 3] < 1.25 and st[i, 4] > 0.6*st[i, 2]*st[i, 3]]
print("   disques noirs (cx, cy, l, h, aire) :", [tuple(round(float(v), 1) for v in d_) for d_ in disks])
R["DOC007"] = dict(rects=rects[:6], disques=[[float(v) for v in d_] for d_ in disks])
# bandes hachurées du DOC-007 : profil de transitions noir/blanc par colonne dans la zone du couvercle
if rects:
    x, y, w, h = rects[0]
    sub = (g7[y+8:y+h-8, x+5:x+w-5] < 110).astype(np.uint8)
    trans = np.abs(np.diff(sub, axis=0)).sum(axis=0).astype(float)
    trans = np.convolve(trans, np.ones(5)/5, mode="same"); thr = 0.5*trans.max(); seg = []; inside = False
    for xx, v in enumerate(trans):
        if v > thr and not inside: xa = xx; inside = True
        if (v <= thr or xx == len(trans)-1) and inside:
            inside = False
            if xx - xa >= 8: seg.append((xa, xx))
    print("   zones à forte alternance (bandes hachurées / panneau de texte) dans le premier rectangle, en fraction de L :",
          [(round(a/w, 3), round(b/w, 3)) for a, b in seg])
    R["DOC007"]["zones_alternance_frac"] = [(a/w, b/w) for a, b in seg]

# ----------------------------------------------------------------------------- 6. agrandissements de contrôle
titre("6. Agrandissements de contrôle écrits dans figures/")
def crop_zoom(fname_key, box, k, out):
    f = [x for x in FILES if fname_key in x][0]
    im = Image.open(os.path.join(ORIG, f)).convert("L").crop(box)
    im = im.resize((im.size[0]*k, im.size[1]*k), Image.LANCZOS)
    im.save(os.path.join(OUT, out)); print("   ", out, im.size)
crop_zoom("7018", (80, 75, 215, 110), 8, "zoom_DOC009_texte_interne.png")
crop_zoom("7018", (0, 50, 110, 260), 6, "zoom_DOC009_gauche_reperes.png")
crop_zoom("7018", (190, 110, 260, 180), 8, "zoom_DOC009_repere_droit.png")
crop_zoom("7018", (40, 300, 318, 369), 6, "zoom_DOC009_legende.png")
crop_zoom("7015", (220, 470, 477, 540), 6, "zoom_DOC006_dates.png")
crop_zoom("7014", (40, 70, 700, 135), 3, "zoom_DOC005_entete_titre.png")
crop_zoom("7012", (170, 30, 472, 160), 5, "zoom_JT3_couvercle.png")
crop_zoom("7012", (330, 150, 472, 300), 6, "zoom_JT3_telecommande.png")

json.dump(R, open(os.path.join(os.path.dirname(__file__), "resultats_images.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False, default=str)
print("\n-> resultats_images.json écrit.")
