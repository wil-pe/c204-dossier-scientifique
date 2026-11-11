# -*- coding: utf-8 -*-
"""Constantes physiques communes (SI, CODATA 2018) — Équipe B."""
import math

G = 6.67430e-11           # m^3 kg^-1 s^-2
c = 2.99792458e8          # m/s (exact)
hbar = 1.054571817e-34    # J s
h = 2 * math.pi * hbar
kB = 1.380649e-23         # J/K (exact)
e = 1.602176634e-19       # C (exact)
eps0 = 8.8541878128e-12   # F/m
mu0 = 1.25663706212e-6    # N/A^2
m_e = 9.1093837015e-31    # kg
m_p = 1.67262192369e-27   # kg
alpha = e**2 / (4 * math.pi * eps0 * hbar * c)   # constante de structure fine
sigma_SB = math.pi**2 * kB**4 / (60 * hbar**3 * c**2)

eV = e                    # J
MeV = 1e6 * eV
GeV = 1e9 * eV
an = 365.25 * 86400.0     # année julienne, s
g0 = 9.80665              # m/s^2

M_soleil = 1.98847e30     # kg
M_terre = 5.9722e24       # kg
M_jupiter = 1.89813e27    # kg

# échelles de Planck
m_planck = math.sqrt(hbar * c / G)
l_planck = math.sqrt(hbar * G / c**3)
t_planck = l_planck / c

# longueurs caractéristiques de l'électron
r_e_classique = e**2 / (4 * math.pi * eps0 * m_e * c**2)
lambda_compton_e = h / (m_e * c)
lambda_compton_reduite_e = hbar / (m_e * c)

# champ critique de Schwinger
E_schwinger = m_e**2 * c**3 / (e * hbar)     # V/m
B_schwinger = m_e**2 * c**2 / (e * hbar)     # T

TNT_tonne = 4.184e9       # J


def sci(x, n=3):
    """Écriture scientifique compacte."""
    return f"{x:.{n}e}"
