#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red Team n° 2 — recalcul INDÉPENDANT des coefficients de puissance de Hawking (facteurs de corps gris).
Aucun code des équipes B ou C n'est importé. Unités G = c = hbar = k_B = 1, M = 1 (r_s = 2), T_H = 1/(8 pi).
Équation radiale : d²psi/dr*² + (w² - V) psi = 0, intégrée en r de l'horizon vers l'infini.
  spins 0, 1, 2 : V = f [ l(l+1)/r² + 2(1 - s²)/r³ ]             (Regge-Wheeler), l >= s, dégénérescence 2l+1
  spin 1/2     : V = W² + dW/dr*, W = kappa sqrt(f)/r  =>  V = kappa² f/r² - kappa sqrt(f)(r-3)/r³ (re-dérivé ici),
                 kappa = 1, 2, ..., dégénérescence 2 kappa par état d'hélicité.
Transmission : psi -> exp(-i w r*) à l'horizon ; à grande distance |A_in|² = (|psi|² + |psi'|²/w² + 2)/4 ; Gamma = 1/|A_in|².
Puissance par degré de liberté : P = (1/2pi) Int w Sum g Gamma / (exp(8 pi w) -/+ 1) dw   [en hbar c^6/(G² M²)].
Sortie : journaux/corps_gris_independant.json"""
import json, math, os, time
import numpy as np
from scipy.integrate import solve_ivp, simpson

def V(r, s, lk):
    f = 1.0 - 2.0 / r
    if s == 0.5:
        return lk * lk * f / r**2 - lk * math.sqrt(f) * (r - 3.0) / r**3
    return f * (lk * (lk + 1) / r**2 + 2.0 * (1 - s * s) / r**3)

def transmission(w, s, lk):
    d = 1e-7
    r0 = 2.0 * (1.0 + d)
    rs0 = r0 + 2.0 * math.log(r0 / 2.0 - 1.0)
    psi0 = complex(math.cos(w * rs0), -math.sin(w * rs0))
    y0 = [psi0, -1j * w * psi0]
    L2 = (lk * lk) if s == 0.5 else (lk * (lk + 1) + 1)
    rmax = 60.0 + 40.0 * math.sqrt(L2) / w            # V/w² < ~6e-4 (erreur relative sur Gamma du même ordre)
    def rhs(r, y):
        f = 1.0 - 2.0 / r
        return [y[1] / f, -(w * w - V(r, s, lk)) * y[0] / f]
    sol = solve_ivp(rhs, (r0, rmax), y0, method="DOP853", rtol=1e-9, atol=1e-13)
    psi, dpsi = sol.y[0, -1], sol.y[1, -1]
    S = abs(psi) ** 2 + abs(dpsi) ** 2 / (w * w)      # = 2(|A_in|² + |A_out|²) ; et |A_in|² - |A_out|² = 1
    return 4.0 / (S + 2.0)

def puissance(s, xs):
    T = 1.0 / (8.0 * math.pi)
    integ = []
    for x in xs:
        w = x * T
        tot = 0.0
        lk = 1 if s == 0.5 else int(s)
        while True:
            g = (2 * lk) if s == 0.5 else (2 * lk + 1)
            G = transmission(w, s, lk)
            tot += g * G
            if (g * G < 1e-7 * max(tot, 1e-300) and lk > (1 if s == 0.5 else s) + 1) or lk > 30:
                break
            lk += 1
        stat = (math.exp(x) + 1.0) if s == 0.5 else (math.exp(x) - 1.0)
        integ.append(w * tot / stat)
    integ = np.array(integ)
    return simpson(integ, x=xs * T) / (2.0 * math.pi), xs[np.argmax(integ)]

if __name__ == "__main__":
    xs = np.linspace(0.05, 32.0, 257)      # x = hbar w / k T
    res = {}
    for s in (0, 0.5, 1, 2):
        t0 = time.time()
        P, xpic = puissance(s, xs)
        res[str(s)] = {"P_par_ddl": P, "pic_puissance_E_sur_kT": float(xpic)}
        print(f"spin {s}: P/ddl = {P:.4e} hbar c^6/(G²M²) ; pic de puissance à E/kT ≈ {xpic:.2f}   [{time.time()-t0:.0f} s]")
    ref_B = {"0": 7.439e-5, "0.5": 4.092e-5, "1": 1.682e-5, "2": 1.918e-6}
    page76 = {"0.5": 0.814 * 2.011e-4 / 4, "1": 0.167 * 2.011e-4 / 2, "2": 0.019 * 2.011e-4 / 2}
    for k in res:
        res[k]["equipe_B"] = ref_B[k]
        res[k]["ecart_vs_B_pct"] = 100 * (res[k]["P_par_ddl"] / ref_B[k] - 1)
        if k in page76:
            res[k]["Page1976_par_ddl"] = page76[k]
            res[k]["ecart_vs_Page_pct"] = 100 * (res[k]["P_par_ddl"] / page76[k] - 1)
        print(k, {a: (round(b, 3) if abs(b) > 1e-3 else float(f"{b:.4e}")) for a, b in res[k].items()})
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "journaux", "corps_gris_independant.json")
    json.dump(res, open(out, "w"), indent=1)
