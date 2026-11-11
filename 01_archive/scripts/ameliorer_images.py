"""Amélioration de lisibilité des documents C204 (copies de travail — les originaux ne sont jamais modifiés).
Usage : .venv/bin/python -I 01_archive/scripts/ameliorer_images.py <dossier_originaux> <dossier_sortie>
Traitements : agrandissement Lanczos x4, débruitage léger, CLAHE (contraste local), masque flou.
ATTENTION : l'agrandissement n'ajoute AUCUNE information ; il facilite seulement la lecture."""
import sys, os, cv2, numpy as np
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in sorted(os.listdir(src)):
    p = os.path.join(src, f)
    img = cv2.imdecode(np.fromfile(p, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None: continue
    h, w = img.shape[:2]
    k = 4 if max(h, w) < 700 else 2
    up = cv2.resize(img, (w*k, h*k), interpolation=cv2.INTER_LANCZOS4)
    up = cv2.fastNlMeansDenoisingColored(up, None, 4, 4, 7, 21)
    lab = cv2.cvtColor(up, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l)
    enh = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    blur = cv2.GaussianBlur(enh, (0, 0), 2.0)
    enh = cv2.addWeighted(enh, 1.6, blur, -0.6, 0)
    out = os.path.join(dst, os.path.splitext(f)[0] + f"__x{k}_ameliore.png")
    cv2.imencode(".png", enh)[1].tofile(out)
    print(f"{f}: {w}x{h} -> {w*k}x{h*k}")
