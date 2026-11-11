#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — script 02 : rayonnement de Hawking d'un trou noir de Schwarzschild,
calcul DE PREMIERS PRINCIPES des facteurs de corps gris (spins 0, 1/2, 1, 2),
puis puissance totale par espèces, durée de vie et confrontation aux chiffres
revendiqués (227 kg ; 300-500 MW ; « rayons X »).

Méthode (unités G = c = hbar = k_B = 1, M = 1, horizon r = 2) :
  - équation radiale  d²psi/dr*² + (w² - V) psi = 0,  r* = r + 2 ln(r/2 - 1)
      bosons  s = 0, 1, 2 (Regge-Wheeler) : V = f [ l(l+1)/r² + 2(1 - s²)/r³ ],  f = 1 - 2/r
      fermion s = 1/2 sans masse (Dirac)  : V = k² f/r² - k sqrt(f) (r - 3)/r³,  k = j + 1/2
  - condition purement entrante à l'horizon (psi = exp(-i w r*)), intégration vers l'infini,
    décomposition A_in, A_out ; probabilité de transmission Gamma = 1/|A_in|².
  - puissance par degré de liberté (polarisation ou état d'hélicité) :
      P = (1/2pi) ∫ dw w Σ_modes Gamma / (exp(8 pi w) -+ 1)
    modes : (2l+1) par l pour les bosons (l >= s) ; 2k par k pour les fermions.
  - résultat en unités hbar c^6 / (G² M²).

Valeurs publiées servant de CONTRÔLE (Page 1976, Phys. Rev. D 13, 198) :
  neutrino + antineutrino d'une saveur : 8,18e-5 ; photon (2 pol.) : 3,37e-5 ; graviton (2 pol.) : 3,84e-6.

Modélisation des seuils de masse (approximation, étiquetée [HYP]) : une espèce de masse m
ne reçoit que la partie du spectre sans masse située au-dessus de E = m c². Les quarks et
gluons sont comptés comme partons libres au-dessus d'une énergie effective (~0,3 et 0,6 GeV),
dans l'esprit de MacGibbon & Webber (1990). Cette approximation n'affecte que la zone
1e8-1e11 kg et aucune des conclusions.
"""
import math
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp, simpson, cumulative_trapezoid
from scipy.special import lambertw
from scipy.optimize import brentq

from constantes import *

LMAX = 12


def w_de_rstar(x):
    """Renvoie w = r/2 - 1 en fonction de r* (M = 1) : w + ln w = x/2 - 1."""
    z = 0.5 * x - 1.0
    if z < 30.0:
        return float(lambertw(math.exp(z)).real)
    w = z - math.log(z)
    for _ in range(50):
        g = w + math.log(w) - z
        w_new = w - g / (1.0 + 1.0 / w)
        if abs(w_new - w) < 1e-15 * abs(w):
            w = w_new
            break
        w = w_new
    return w


def potentiel(x, spin, modes):
    w = w_de_rstar(x)
    r = 2.0 * (1.0 + w)
    f = w / (1.0 + w)
    if spin == 0.5:
        k = modes
        return k * k * f / r**2 - k * math.sqrt(f) * (r - 3.0) / r**3
    L = modes * (modes + 1.0)
    return f * (L / r**2 + 2.0 * (1.0 - spin * spin) / r**3)


def transmissions(omega, spin, modes):
    """Gamma pour un tableau de modes (l ou kappa) à la pulsation omega (unités de 1/M)."""
    n = len(modes)
    x0 = -40.0
    x1 = max(150.0, 60.0 * (modes.max() + 1.0) / omega)
    psi0 = np.exp(-1j * omega * x0) * np.ones(n, dtype=complex)
    y0 = np.concatenate([psi0, -1j * omega * psi0])

    def rhs(x, y):
        V = potentiel(x, spin, modes)
        return np.concatenate([y[n:], (V - omega * omega) * y[:n]])

    sol = solve_ivp(rhs, (x0, x1), y0, method="DOP853", rtol=1e-9, atol=1e-13)
    psi, phi = sol.y[:n, -1], sol.y[n:, -1]
    V1 = potentiel(x1, spin, modes)
    k = np.sqrt(omega * omega - V1)
    N = (k * np.abs(psi) ** 2 + np.abs(phi) ** 2 / k) / (2.0 * omega)   # |A_in|² + |A_out|²
    flux = np.imag(np.conj(psi) * phi) / omega                           # doit valoir -1 (conservation du wronskien)
    gamma = 2.0 / (N + 1.0)
    # erreur relative sur N (donc sur Gamma) déduite de la non-conservation numérique du flux
    return gamma, float(np.max(np.abs(flux + 1.0) / (N + 1.0)))


def spectre(spin, omegas):
    """Renvoie dP/dw et dN/dt/dw par degré de liberté (unités M = 1)."""
    signe = +1.0 if spin == 0.5 else -1.0
    dP = np.zeros_like(omegas)
    dN = np.zeros_like(omegas)
    err_flux = 0.0
    for i, om in enumerate(omegas):
        lcrit = math.sqrt(27.0) * om
        if spin == 0.5:
            mmax = int(min(LMAX, math.ceil(1.6 * lcrit + 4)))
            modes = np.arange(1, mmax + 1, dtype=float)
            deg = 2.0 * modes
        else:
            lmin = int(spin)
            mmax = int(min(LMAX, math.ceil(1.6 * lcrit + 3 + lmin)))
            modes = np.arange(lmin, mmax + 1, dtype=float)
            deg = 2.0 * modes + 1.0
        gam, ef = transmissions(om, spin, modes)
        err_flux = max(err_flux, ef)
        s = float(np.sum(deg * gam))
        occ = 1.0 / (math.exp(8.0 * math.pi * om) + signe)
        dN[i] = s * occ / (2.0 * math.pi)
        dP[i] = om * dN[i]
    return dP, dN, err_flux


def pic_parabolique(x, y):
    """Abscisse du maximum affinée par interpolation parabolique sur 3 points."""
    i = int(np.argmax(y))
    if i == 0 or i == len(y) - 1:
        return float(x[i])
    y0, y1, y2 = y[i - 1], y[i], y[i + 1]
    d = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    return float(x[i] + d * (x[i + 1] - x[i]))


def main():
    t0 = time.time()
    print("=" * 78)
    print("SCRIPT 02 — Rayonnement de Hawking : facteurs de corps gris, espèces, durée de vie")
    print("=" * 78)
    # grille en x = w / T = 8 pi M w
    xs = np.linspace(0.05, 32.0, 161)
    omegas = xs / (8.0 * math.pi)
    resultats = {}
    for spin in (0, 0.5, 1, 2):
        dP, dN, ef = spectre(spin, omegas)
        # contribution de [0, w_min] : extrapolation linéaire vers 0
        P = simpson(dP, x=omegas) + 0.5 * dP[0] * omegas[0]
        Ndot = simpson(dN, x=omegas) + 0.5 * dN[0] * omegas[0]
        xp_P = pic_parabolique(xs, dP)
        xp_N = pic_parabolique(xs, dN)
        resultats[spin] = dict(P=P, N=Ndot, dP=dP, dN=dN, x_pic_P=xp_P, x_pic_N=xp_N)
        print(f"spin {spin:>3} : P/ddl = {P:.4e} hbar c^6/(G² M²) ; dN/dt/ddl = {Ndot:.4e} c³/(G M) ;"
              f" pic puissance x = E/kT = {xp_P:.2f} ; pic flux x = {xp_N:.2f} ;"
              f" erreur relative de flux max = {ef:.1e}   [{time.time()-t0:.0f} s]")
        sys.stdout.flush()

    c0, c12, c1, c2 = (resultats[s]["P"] for s in (0, 0.5, 1, 2))
    print()
    print("Contrôle contre Page (1976) :")
    print(f"  neutrino+antineutrino (2 états) : {2*c12:.4e}   (publié 8,18e-5)   écart {100*(2*c12/8.183e-5-1):+.2f} %")
    print(f"  photon (2 polarisations)        : {2*c1:.4e}   (publié 3,37e-5)   écart {100*(2*c1/3.366e-5-1):+.2f} %")
    print(f"  graviton (2 polarisations)      : {2*c2:.4e}   (publié 3,84e-6)   écart {100*(2*c2/3.84e-6-1):+.2f} %")
    print(f"  scalaire (1 ddl)                : {c0:.4e}")
    print(f"  corps noir naïf, photons, aire de l'horizon : {1/(15360*math.pi):.4e}"
          f"  -> le vrai flux de photons vaut {2*c1*15360*math.pi:.3f} fois la formule du dossier")
    print(f"  limite d'optique géométrique par ddl bosonique : {27/(30*4096*math.pi):.4e}")

    # ------------------------------------------------------------------
    # Espèces du Modèle standard : (nom, spin, nombre de ddl, seuil en GeV)
    # ------------------------------------------------------------------
    especes = [
        ("photon", 1, 2, 0.0),
        ("graviton", 2, 2, 0.0),
        ("neutrinos (3 saveurs, nu + anti-nu)", 0.5, 6, 0.0),
        ("electron/positron", 0.5, 4, 0.000511),
        ("muon", 0.5, 4, 0.10566),
        ("tau", 0.5, 4, 1.777),
        ("quarks u,d,s (seuil effectif 0,3 GeV)", 0.5, 36, 0.3),
        ("quark c", 0.5, 12, 1.27),
        ("quark b", 0.5, 12, 4.18),
        ("quark t", 0.5, 12, 172.7),
        ("gluons (seuil effectif 0,6 GeV)", 1, 16, 0.6),
        ("W+-", 1, 6, 80.4),
        ("Z", 1, 3, 91.19),
        ("Higgs", 0, 1, 125.2),
    ]
    # fraction cumulée du spectre de puissance au-dessus de x
    frac = {}
    for s in (0, 0.5, 1, 2):
        dP = resultats[s]["dP"]
        cum = cumulative_trapezoid(dP, omegas, initial=0.0)
        tot = cum[-1]
        frac[s] = (xs.copy(), 1.0 - cum / tot)

    coefP = hbar * c**6 / G**2          # W kg²
    kT_GeV_kg = hbar * c**3 / (8 * math.pi * G) / GeV   # kT [GeV] = kT_GeV_kg / M[kg]

    def alpha_tot(M, detail=False):
        """Coefficient sans dimension : P = alpha * hbar c^6 / (G² M²)."""
        kT = kT_GeV_kg / M
        total = 0.0
        parts = {}
        for nom, s, ndl, seuil in especes:
            x_seuil = seuil / kT
            xg, fr = frac[s]
            fraction = 1.0 if x_seuil <= xg[0] else (0.0 if x_seuil >= xg[-1] else float(np.interp(x_seuil, xg, fr)))
            val = ndl * resultats[s]["P"] * fraction
            parts[nom] = val
            total += val
        return (total, parts) if detail else total

    def puissance(M):
        return alpha_tot(M) * coefP / M**2

    def duree_de_vie(M0):
        """tau = ∫_0^M0 G² M² dM / (alpha(M) hbar c^4), intégration en log M depuis la masse de Planck."""
        lnM = np.linspace(math.log(m_planck), math.log(M0), 4000)
        Ms = np.exp(lnM)
        integrand = np.array([m**3 / alpha_tot(m) for m in Ms])   # M² dM = M³ dlnM
        return simpson(integrand, x=lnM) * G**2 / (hbar * c**4)

    a_ir, parts_ir = alpha_tot(1e20, detail=True)
    a_e = alpha_tot(3e12)
    a_uv = alpha_tot(1.0)
    print()
    print("Coefficient alpha(M) = P G² M² / (hbar c^6) :")
    print(f"  M >> 1e14 kg (photon, graviton, 3 neutrinos)          : {a_ir:.4e}")
    print(f"  M ~ 3e12 kg (+ e±)                                    : {a_e:.4e}")
    print(f"  M << 1e8 kg (tout le Modèle standard)                 : {a_uv:.4e}"
          f"   (rapport au cas « photons corps noir » du dossier : {a_uv*15360*math.pi:.0f})")

    print()
    print("Tableau : masse, température, puissance, durée de vie")
    print(f"{'M (kg)':>10} {'r_s (m)':>10} {'kT':>12} {'P totale (W)':>13} {'P photons (W)':>13} {'frac. nu':>8} {'tau':>22}")
    for M in (100.0, 113.5, 227.0, 1e6, 1e9, 1e10, 1e11, 5e11, 1e12, 2e12, 4e12, 5e12, 1e13, 1e14, 1e15, 1e16):
        a, parts = alpha_tot(M, detail=True)
        P = a * coefP / M**2
        Pg = parts["photon"] * coefP / M**2
        fnu = parts["neutrinos (3 saveurs, nu + anti-nu)"] / a
        tau = duree_de_vie(M)
        kT = kT_GeV_kg / M
        kTs = f"{kT:.3g} GeV" if kT >= 1 else (f"{kT*1e3:.3g} MeV" if kT >= 1e-3 else f"{kT*1e6:.3g} keV")
        taus = f"{tau:.3e} s" if tau < an else f"{tau/an:.3e} ans"
        print(f"{M:>10.3g} {2*G*M/c**2:>10.2e} {kTs:>12} {P:>13.3e} {Pg:>13.3e} {fnu:>8.2f} {taus:>22}")

    print()
    print("Masse correspondant aux puissances revendiquées (300-500 MW) :")
    for Pc in (300e6, 500e6):
        M_tot = brentq(lambda m: puissance(m) - Pc, 1e11, 1e14)
        M_ph = brentq(lambda m: alpha_tot(m, True)[1]["photon"] * coefP / m**2 - Pc, 1e11, 1e14)
        M_cn = math.sqrt(coefP / (15360 * math.pi) / Pc)
        print(f"  P = {Pc/1e6:.0f} MW : puissance TOTALE -> M = {M_tot:.3e} kg (kT = {kT_GeV_kg/M_tot*1e3:.2f} MeV, r_s = {2*G*M_tot/c**2*1e15:.2f} fm,"
              f" tau = {duree_de_vie(M_tot)/an:.2e} ans)")
        print(f"               photons seuls (corps gris) -> M = {M_ph:.3e} kg ; photons corps noir (dossier) -> M = {M_cn:.3e} kg")

    print()
    M_star = brentq(lambda m: duree_de_vie(m) - 13.8e9 * an, 1e10, 1e13)
    print(f"Contrôle : masse dont la durée de vie vaut 13,8 Ga : M* = {M_star:.3e} kg"
          f"  (littérature : ≈ 5,0-5,1e11 kg, MacGibbon, Carr & Page 2008)")

    print()
    print("Masse minimale pour une durée de vie donnée, et puissance correspondante :")
    for nom, tt in (("1 seconde", 1.0), ("1 heure", 3600.0), ("1 an", an), ("36 ans", 36 * an), ("100 ans", 100 * an), ("1e6 ans", 1e6 * an)):
        Mm = brentq(lambda m: duree_de_vie(m) - tt, 1e2, 1e13)
        print(f"  tau = {nom:>9} : M = {Mm:.3e} kg ; P = {puissance(Mm):.3e} W ; kT = {kT_GeV_kg/Mm:.3g} GeV")

    print()
    print("Cas revendiqué : unité de 227 kg")
    for M in (227.0, 113.5):
        tau = duree_de_vie(M)
        print(f"  M = {M} kg : tau = {tau:.3e} s (la lumière parcourt {c*tau*1e3:.3f} mm) ; P initiale = {puissance(M):.3e} W ;"
              f" énergie libérée = {M*c**2:.3e} J = {M*c**2/TNT_tonne/1e9:.2f} Gt TNT")

    print()
    xpic1_P = resultats[1]["x_pic_P"]
    xpic1_N = resultats[1]["x_pic_N"]
    print(f"Pic du spectre de photons : x = E/kT ≈ {xpic1_P:.2f} (puissance), {xpic1_N:.2f} (flux)")
    for M in (8.4e11, 1.09e12, 4e12, 5e12):
        kT = kT_GeV_kg / M * 1e3
        print(f"  M = {M:.2e} kg : kT = {kT:.2f} MeV ; énergie de photon au pic de puissance ≈ {xpic1_P*kT:.1f} MeV (gamma, pas X)")
    print("Trou noir dont le spectre de photons culmine dans les rayons X :")
    for Epic_keV in (1.0, 10.0, 100.0):
        kT_keV = Epic_keV / xpic1_P
        M = kT_GeV_kg / (kT_keV * 1e-6)
        print(f"  pic à {Epic_keV:>5.0f} keV : kT = {kT_keV:.3g} keV ; M = {M:.3e} kg ; puissance totale = {puissance(M):.3e} W ;"
              f" photons = {alpha_tot(M, True)[1]['photon']*coefP/M**2:.3e} W")

    print()
    print(f"Temps de calcul : {time.time()-t0:.0f} s")


if __name__ == "__main__":
    main()
