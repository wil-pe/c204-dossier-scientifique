#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe G (red team) — Programme C204
01_physique_c204.py : re-dérivation INDÉPENDANTE des ordres de grandeur et test de cohérence
des paramètres revendiqués pour l'unité « C204 » (corpus attribué à John Titor, 2000-2001).

Tout est calculé en SI. Les hypothèses sont explicites dans chaque section.
Sortie : texte sur stdout + resultats_physique.json (même dossier).

Coefficients d'émission de Hawking (trou noir de Schwarzschild, non chargé, sans rotation) :
  P = alpha * hbar c^6 / (G^2 M^2)
  - corps noir « naïf », photons seuls, aire de l'horizon : alpha = 1/(15360 pi) = 2,072e-5
    (c'est la formule utilisée par le dossier de base de l'institut) ;
  - Page (1976, Phys. Rev. D 13, 198), calcul avec facteurs de corps gris, M >> 1e14 kg
    (particules sans masse seulement) : alpha = 2,011e-4 avec 4 espèces de neutrinos à
    2 composantes (81,4 % neutrinos, 16,7 % photons, 1,9 % gravitons) ;
  - Page (1976), 5e11 kg << M << 1e14 kg (e+ e- ultra-relativistes en plus) : alpha = 3,6e-4
    (45 % e+-, 45 % neutrinos, 9 % photons, 1 % gravitons).
  On convertit ici à 3 saveurs de neutrinos (6 espèces à 2 composantes), ce qui redonne le
  coefficient de MacGibbon & Webber (1990, Phys. Rev. D 41, 3052) dM/dt = -5,34e25 f(M)/M^2 g/s.
  [Valeurs numériques de Page/MacGibbon citées de mémoire, recoupées entre elles ci-dessous.]
"""
import json, math
import numpy as np

# ----------------------------------------------------------------------------- constantes (CODATA 2018)
G     = 6.67430e-11        # m^3 kg^-1 s^-2
c     = 2.99792458e8       # m/s
hbar  = 1.054571817e-34    # J s
kB    = 1.380649e-23       # J/K
eps0  = 8.8541878128e-12   # F/m
e     = 1.602176634e-19    # C
me    = 9.1093837015e-31   # kg
sigma = 5.670374419e-8     # W m^-2 K^-4
g0    = 9.80665            # m/s^2
MeV   = 1.602176634e-13    # J
yr    = 365.25*86400.0     # s (année julienne)
lb    = 0.45359237         # kg
ft    = 0.3048             # m
M_sun = 1.98847e30
M_jup = 1.89813e27
M_earth = 5.9722e24
L_sun = 3.828e26           # W
r_e_classique = e**2/(4*math.pi*eps0*me*c**2)   # 2,818e-15 m
r_proton = 0.8414e-15      # rayon de charge du proton (CODATA 2018), m
E_schwinger = me**2*c**3/(e*hbar)               # 1,32e18 V/m

R = {}   # résultats exportés

def titre(s):
    print("\n" + "="*100 + "\n" + s + "\n" + "="*100)

# ----------------------------------------------------------------------------- A. vérification du §6 du dossier
titre("A. Vérification indépendante des coefficients du §6 du DOSSIER DE BASE")
rs_coef = 2*G/c**2
T_coef  = hbar*c**3/(8*math.pi*G*kB)
K       = hbar*c**6/G**2                       # W kg^2
a_bb    = 1/(15360*math.pi)                    # corps noir, photons seuls
P_coef  = a_bb*K
t_coef  = 5120*math.pi*G**2/(hbar*c**4)
Q_coef  = math.sqrt(4*math.pi*eps0*G)
print(f"r_s/M            = {rs_coef:.4e} m/kg        (dossier : 1,485e-27)")
print(f"T_H * M          = {T_coef:.4e} K kg        (dossier : 1,227e23)")
print(f"P * M^2 (photons, corps noir) = {P_coef:.4e} W kg^2 (dossier : 3,56e32)")
print(f"t_evap / M^3 (photons, corps noir) = {t_coef:.4e} s/kg^3 (dossier : 8,41e-17)")
print(f"Q_max / M        = {Q_coef:.4e} C/kg        (dossier : 8,62e-11)")
print(f"E(227 kg) = {227*c**2:.3e} J = {227*c**2/4.184e18:.2f} Gt TNT (dossier : 2,0e19 J ; 4,9 Gt)")
print(f"500 lb = {500*lb:.1f} kg ; 10 ans/h -> dt/dtau = {10*yr/3600:.0f} (dossier : 87 660)")
print(f"100-120 °F = {(100-32)/1.8:.1f}-{(120-32)/1.8:.1f} °C ; 10-12 ft = {10*ft:.2f}-{12*ft:.2f} m ; 4 ft = {4*ft:.2f} m")
for r in (1.0, 3.0):
    print(f"M pour 2 g à r = {r:.0f} m : {2*g0*r**2/G:.2e} kg (dossier : 2,9e11 / 2,6e12)")
R["A"] = dict(rs_coef=rs_coef, T_coef=T_coef, P_coef_bb=P_coef, t_coef_bb=t_coef, Q_coef=Q_coef)

# ----------------------------------------------------------------------------- B. Hawking : masse <-> puissance
titre("B. Masse compatible avec « 300-500 MW » selon trois modèles d'émission")
# Page 1976 (4 espèces de neutrinos à 2 composantes)
a_page_massless_4nu = 2.011e-4
frac = dict(nu=0.814, gamma=0.167, grav=0.019)
a_gamma = a_page_massless_4nu*frac["gamma"]            # 3,36e-5
a_nu3   = a_page_massless_4nu*frac["nu"]*6/4           # 3 saveurs
a_grav  = a_page_massless_4nu*frac["grav"]
a_epm   = 0.45*3.6e-4                                   # e+ e- ultra-relativistes (Page 1976)
a_massless = a_gamma + a_nu3 + a_grav                   # ~2,83e-4
a_full  = a_massless + a_epm                            # ~4,45e-4 (domaine 5e11 kg << M << 1e14 kg)
print(f"alpha corps noir photons seuls : {a_bb:.3e}")
print(f"alpha photons (Page, corps gris) : {a_gamma:.3e}  -> x{a_gamma/a_bb:.2f} par rapport au corps noir naïf")
print(f"alpha sans masse (gamma + 3 nu + graviton) : {a_massless:.3e}")
print(f"   recoupement MacGibbon-Webber : {a_massless*K/c**2*1e9:.3e} g^3/s (valeur publiée 5,34e25)")
print(f"alpha total avec e+- : {a_full:.3e}   (f(M) = {a_full/a_massless:.3f} ; MacGibbon : ~1,57)")
fr = {k: v/a_full for k, v in dict(gamma=a_gamma, nu=a_nu3, grav=a_grav, epm=a_epm).items()}
print("   fractions de puissance : " + ", ".join(f"{k} {100*v:.1f} %" for k, v in fr.items()))
a_dep = a_gamma + a_epm     # part déposable localement (photons + e+-), neutrinos et gravitons s'échappent

rows = []
for P in (300e6, 400e6, 500e6):
    for nom, a in (("corps noir photons seuls (dossier)", a_bb),
                   ("Page complet : gamma+3nu+grav+e± = puissance totale", a_full),
                   ("Page, part gamma+e± seulement = 300-500 MW", a_dep)):
        M = math.sqrt(a*K/P)
        rs = rs_coef*M
        kT = kB*T_coef/M/MeV
        rows.append((P/1e6, nom, M, rs*1e15, kT))
        print(f"P = {P/1e6:.0f} MW | {nom:55s} | M = {M:.2e} kg | r_s = {rs*1e15:.2f} fm | kT = {kT:.1f} MeV")
R["B_masse_pour_puissance"] = [dict(P_MW=a_, modele=b_, M_kg=c_, rs_fm=d_, kT_MeV=e_) for a_, b_, c_, d_, e_ in rows]
print(f"\nrayon classique de l'électron = {r_e_classique*1e15:.3f} fm ; rayon de charge du proton = {r_proton*1e15:.3f} fm")
print("   (l'électron n'a pas de taille mesurée : ponctuel jusqu'à < 1e-18 m ; le « rayon classique » est une convention)")
M_re = r_e_classique/rs_coef
print(f"Trou noir de rayon r_s = r_e classique : M = {M_re:.2e} kg -> P(corps noir photons) = {a_bb*K/M_re**2/1e6:.0f} MW ; "
      f"P(Page total) = {a_full*K/M_re**2/1e6:.0f} MW")
print("   -> « taille d'un électron ↔ masse d'une grosse montagne » n'est cohérent qu'avec le rayon CLASSIQUE (2,8 fm).")
for k_ in (0.1, 0.01):
    M_ = k_*M_re
    print(f"   « bien plus petites » (masse x{k_}) : M = {M_:.1e} kg -> P(photons corps noir) = {a_bb*K/M_**2:.2e} W, "
          f"P(Page total, sous-estimé car autres espèces) >= {a_full*K/M_**2:.2e} W")
R["B_M_rayon_electron"] = M_re

# durées de vie
print("\nDurées de vie (t = M^3 / (3 alpha hbar c^4 / G^2)) :")
Kt = hbar*c**4/G**2
for M in (100.0, 227.0, 1e9, 1e11, 2.9e11, 1e12, 4e12):
    t_bb = M**3/(3*a_bb*Kt)
    t_full = M**3/(3*a_full*Kt)     # borne haute pour M < 5e11 kg (davantage d'espèces émises)
    print(f"M = {M:9.3g} kg : t(corps noir photons) = {t_bb:.2e} s = {t_bb/yr:.2e} a ; "
          f"t(gamma+nu+e±) = {t_full:.2e} s = {t_full/yr:.2e} a ; P_bb = {a_bb*K/M**2:.2e} W")
R["B_duree_vie_1e12_kg_ans"] = dict(corps_noir_photons=(1e12**3/(3*a_bb*Kt))/yr, page_complet=(1e12**3/(3*a_full*Kt))/yr)
# repère : masse s'évaporant en 13,8 Ga avec f = 1,9 (MacGibbon) -> ~5e11 kg
M_star = (3*1.9*a_massless*Kt*13.8e9*yr)**(1/3)
print(f"Repère : masse initiale s'évaporant en 13,8 Ga (f = 1,9) = {M_star:.2e} kg (valeur publiée ~5e11 kg)")

# « rayons X » : quelle masse / quelle puissance ?
print("\nSi le rayonnement est réellement dans le domaine X (kT = 1-100 keV) :")
for kT_keV in (1, 10, 100):
    M = kB*T_coef/(kT_keV*1e-3*MeV)
    print(f"  kT = {kT_keV:3d} keV -> M = {M:.2e} kg, r_s = {rs_coef*M:.2e} m, P(gamma+nu+grav) = {a_massless*K/M**2:.2e} W")
print("  -> un trou noir qui émet des rayons X rayonne des watts à des dizaines de MW seulement si M ~1e14-1e16 kg ;")
print("     « 300-500 MW » ET « rayons X » sont incompatibles (300-500 MW => kT ~ 2-13 MeV, pic photon ~ 5 kT).")

# ----------------------------------------------------------------------------- C. pesanteur ressentie et marées
titre("C. « 1,5 à 2 g ressentis » : masse requise, gradient de marée, dilatation gravitationnelle")
for gg in (1.5, 2.0):
    for r in (0.5, 1.0, 1.5, 2.0, 3.0):
        M = gg*g0*r**2/G
        grad = 2*G*M/r**3/g0        # en g par mètre
        print(f"{gg:.1f} g à r = {r:.1f} m : M_total = {M:.2e} kg ; gradient = {grad:.1f} g/m ; "
              f"g à r-0,3 m = {G*M/(r-0.3)**2/g0 if r>0.3 else float('nan'):.1f} g, à r+0,3 m = {G*M/(r+0.3)**2/g0:.2f} g")
M2 = 2e12   # deux trous noirs de 1e12 kg (valeur du dossier)
print(f"\nAvec 2 x 1e12 kg (valeur dossier) : g(1 m) = {G*M2/1**2/g0:.1f} g ; g(1,5 m) = {G*M2/1.5**2/g0:.1f} g ; "
      f"rayon où g = 2 g : {math.sqrt(G*M2/(2*g0)):.2f} m ; où g = 1,5 g : {math.sqrt(G*M2/(1.5*g0)):.2f} m")
M2p = 2*4.4e12
print(f"Avec 2 x 4,4e12 kg (Page complet, 400 MW) : g(1 m) = {G*M2p/g0:.0f} g ; rayon où g = 2 g : {math.sqrt(G*M2p/(2*g0)):.2f} m")
print(f"Avec 227 kg (masse revendiquée de l'unité) : g(1 m) = {G*227/g0:.2e} g")
# dilatation gravitationnelle à 1 m
for M in (2.9e11, 2e12, 8.8e12):
    phi = G*M/(1.0*c**2)
    print(f"Potentiel GM/(r c^2) à 1 m pour M = {M:.1e} kg : {phi:.2e} -> décalage accumulé en 6,1 h : {phi*6.1*3600:.2e} s")
gamma_req = 10*yr/3600
eps = 1/gamma_req**2   # 1 - r_s/r = 1/gamma^2
print(f"Facteur requis par « 10 ans/heure » : {gamma_req:.0f} -> en Schwarzschild il faut r/r_s - 1 = {eps:.2e} "
      f"(observateur statique collé à l'horizon), et la dilatation ne donne JAMAIS un déplacement vers le passé.")
print(f"Écart entre effet disponible à 1 m (≈{G*2e12/c**2:.1e}) et effet requis (≈{gamma_req:.1e}) : "
      f"{gamma_req/(G*2e12/c**2):.1e} (≈ 10^{math.log10(gamma_req/(G*2e12/c**2)):.0f})")
R["C"] = dict(M_2g_1m=2*g0/G, grad_g_par_m_a_1m_pour_2g=4.0, gamma_requis=gamma_req, potentiel_1m_2e12=G*2e12/c**2)

# ----------------------------------------------------------------------------- D. échelle des effets de Kerr
titre("D. Échelle réelle des structures de Kerr (ergosphère, anneau, CTC) vs « 3-4 m » revendiqués")
for M in (227.0, 2.9e11, 1e12, 4.4e12):
    rg = G*M/c**2
    print(f"M = {M:8.3g} kg : GM/c^2 = {rg:.2e} m ; ergosphère équatoriale (a=M) r = 2GM/c^2 = {2*rg:.2e} m ; "
          f"rayon max de l'anneau a_max = GM/c^2 = {rg:.2e} m ; rapport à 3,35 m : {3.35/(2*rg):.1e}")
for Rg, lab in ((3.35, "ergosphère de 3,35 m (11 ft)"), (1.0, "anneau de 1 m de rayon (a = GM/c^2, Kerr extrême)")):
    M = Rg*c**2/(2*G) if "ergo" in lab else Rg*c**2/G
    print(f"Pour une {lab} : M = {M:.2e} kg = {M/M_jup:.2f} M_Jupiter = {M/M_earth:.0f} M_Terre")
# moment cinétique max et moment magnétique
for M in (1e12,):
    Jmax = G*M**2/c
    print(f"J_max(1e12 kg) = {Jmax:.2e} J s = {Jmax/hbar:.2e} hbar ; fréquence de rotation de l'horizon (extrême) "
          f"Omega = c^3/(2GM) = {c**3/(2*G*M):.2e} rad/s")
R["D"] = dict(M_ergosphere_3p35m_kg=3.35*c**2/(2*G), M_anneau_1m_kg=1.0*c**2/G)

# ----------------------------------------------------------------------------- E. poids, confinement, charge
titre("E. Poids, confinement magnétique/électrique, charge maximale réellement soutenable")
for M in (2.9e11/2, 1e12, 4.4e12):
    W = M*g0
    Qext = Q_coef*M
    rs = rs_coef*M
    E_h = Qext/(4*math.pi*eps0*(rs/2)**2)       # RN extrême : r+ = GM/c^2 = rs/2
    V_h = Qext/(4*math.pi*eps0*(rs/2))
    print(f"M = {M:.2e} kg : poids = {W:.2e} N (= {W/g0/1e3:.2e} tonnes-force) ; Q_extrême = {Qext:.1f} C ; "
          f"E à l'horizon (extrême) = {E_h:.2e} V/m = {E_h/E_schwinger:.1e} x champ de Schwinger ; potentiel = {V_h:.2e} V")
    print(f"     champ électrique externe pour léviter avec Q_extrême : E = Mg/Q = {W/Qext:.2e} V/m")
print(f"Champ critique de Schwinger = {E_schwinger:.3e} V/m")
M_sch = c**4/(math.sqrt(4*math.pi*eps0)*G**1.5*E_schwinger)
print(f"Masse au-dessus de laquelle un trou noir extrême a E_horizon < E_Schwinger : {M_sch:.2e} kg = {M_sch/M_sun:.1e} M_soleil")
Zmax = 170
Q_real = Zmax*e
M = 1e12
print(f"Charge soutenable réaliste d'un trou noir de rayon ~fm (comme un noyau supercritique) : |Z| <~ {Zmax} -> Q = {Q_real:.2e} C")
print(f"  champ électrique requis pour porter 1e12 kg avec cette charge : {M*g0/Q_real:.2e} V/m "
      f"({M*g0/Q_real/E_schwinger:.1e} x Schwinger)")
mu = Q_real*G*M/c          # moment magnétique max (g=2) : mu = Q J/M, J = G M^2/c
print(f"  moment magnétique max (Kerr-Newman, g=2) : mu = Q G M / c = {mu:.2e} A m^2 -> gradient requis dB/dz = Mg/mu = {M*g0/mu:.2e} T/m")
mu_ext = Q_coef*M*G*M/c
print(f"  même avec Q extrême (86 C, impossible) : mu = {mu_ext:.2e} A m^2 -> dB/dz = {M*g0/mu_ext:.2e} T/m "
      f"(aimants actuels : ~1e2-1e3 T/m ; record de champ continu ~45 T)")
# injection d'électrons
for dM in (1.0, 1e9):
    N = dM/me
    print(f"« Injecter des électrons pour modifier la masse » : +{dM:.0e} kg = {N:.2e} électrons = {N*e:.2e} C "
          f"(charge extrême de 1e12 kg : {Q_coef*1e12:.0f} C)")
print(f"  énergie pour amener UN électron sur un trou noir de 1e12 kg déjà chargé à 1 C : "
      f"{e*1.0/(4*math.pi*eps0*rs_coef*1e12)/MeV:.2e} MeV")
payload = 800.0
print(f"Charge utile typique d'un pick-up 4x4 des années 1980 : ~{payload:.0f} kg ; rapport poids des singularités / charge utile : {2e12/payload:.1e}")
R["E"] = dict(poids_1e12_N=1e12*g0, M_schwinger_kg=M_sch, dBdz_T_par_m=M*g0/mu, E_levitation_V_par_m=M*g0/Q_real)

# attraction sur l'environnement et détectabilité gravimétrique
print("\nAttraction exercée sur l'environnement par 2e12 kg (permanente : un trou noir ne s'éteint pas) :")
for r in (3.0, 10.0, 30.0, 100.0, 1e3, 1e5, 1e6):
    a = G*2e12/r**2
    print(f"  r = {r:9.0f} m : a = {a:.2e} m/s^2 = {a/g0:.2e} g = {a/1e-5:.2e} mGal")
print("  (gravimètre de terrain : ~0,01 mGal ; gravimètre supraconducteur : ~1e-3 µGal = 1e-11 m/s^2)")
print(f"  distance où le signal vaut 1 µGal (1e-8 m/s^2) : {math.sqrt(G*2e12/1e-8)/1e3:.0f} km")

# ----------------------------------------------------------------------------- F. dose
titre("F. Dose pour l'opérateur à 1 m pendant 6,1 h (61 ans à 10 ans/h)")
mu_en_tissu = 0.0016      # m^2/kg : coefficient massique d'absorption d'énergie de l'eau, ~0,015-0,02 cm^2/g entre 10 et 50 MeV (ordre de grandeur, tables NIST XCOM — non re-téléchargées ici)
t_trip = 61/10*3600.0
for Ptot, lab in ((400e6, "400 MW = puissance totale (Page)"), (400e6/fr["gamma"]*1.0, "cas où 400 MW = photons seuls")):
    Pg = Ptot*fr["gamma"]; Pe = Ptot*fr["epm"]; Pnu = Ptot*fr["nu"]
    flux = Pg/(4*math.pi*1.0**2)
    D = flux*mu_en_tissu
    print(f"{lab} : P_gamma = {Pg/1e6:.0f} MW, P_e± = {Pe/1e6:.0f} MW, P_nu = {Pnu/1e6:.0f} MW")
    print(f"   flux gamma à 1 m = {flux:.2e} W/m^2 ; débit de dose (sans blindage, gamma primaires seuls) = {D:.2e} Gy/s ; "
          f"dose létale (5 Gy) en {5/D*1e3:.2f} ms ; dose en 6,1 h = {D*t_trip:.1e} Gy")
    att = D*t_trip/1e-3
    print(f"   atténuation requise pour ramener à 1 mSv par trajet : {att:.1e} = {math.log(att):.0f} longueurs d'atténuation")
Pg = 400e6*fr["gamma"]
D1 = Pg/(4*math.pi)*mu_en_tissu
mfp_Pb = 1/(0.062*11.35)   # cm, ~20 MeV dans le plomb (mu/rho ~ 0,06 cm^2/g, ordre de grandeur)
n_mfp = math.log(D1*t_trip/1e-3)
ep = n_mfp*mfp_Pb
print(f"Blindage plomb : libre parcours ~{mfp_Pb:.1f} cm à ~20 MeV -> >= {ep:.0f} cm (hors facteur d'accumulation des gerbes, "
      f"qui impose plutôt 45-60 cm) ; sphère de plomb de rayon {ep:.0f} cm : {4/3*math.pi*(ep/100)**3*11350/1e3:.1f} t ; de rayon 50 cm : {4/3*math.pi*0.5**3*11350/1e3:.1f} t")
print("Faisceau « évacué vers l'arrière » (direction non blindée), atténuation dans l'air ~ 460 m à 20 MeV :")
for d in (10, 100, 1000):
    Dd = D1/d**2*math.exp(-d/460.0)
    print(f"   à {d:5d} m : {Dd:.2e} Gy/s = {Dd*3600:.2e} Gy/h")
print("Hors trajet aussi : la source ne peut pas être éteinte ; sans blindage intégral elle irradie en permanence.")
R["F"] = dict(debit_dose_Gy_s=D1, dose_trajet_Gy=D1*t_trip, epaisseur_plomb_cm_min=ep)

# ----------------------------------------------------------------------------- G. bilan thermique
titre("G. Bilan thermique : puissance déposée dans un coffre de ~0,13 m^3 vs « 38-49 °C »")
for Ptot in (300e6, 500e6):
    Pdep = Ptot*(fr["gamma"]+fr["epm"])
    A = 2*(1.2*0.36+1.2*0.30+0.36*0.30)     # surface du coffre H1 du dossier
    Teq = (Pdep/(sigma*A))**0.25
    mdot = Pdep/(2.257e6 + 4186*80)          # eau 20°C -> vapeur
    print(f"P_tot = {Ptot/1e6:.0f} MW : P déposée (gamma+e±, neutrinos exclus) = {Pdep/1e6:.0f} MW ; surface coffre = {A:.2f} m^2 ; "
          f"T d'équilibre radiatif = {Teq:.0f} K ; eau à vaporiser = {mdot:.0f} kg/s = {mdot*t_trip/1e3:.0f} t en 6,1 h")
    print(f"     temps pour porter 227 kg d'acier à la fusion (ΔT = 1500 K, c = 500 J/kg/K) : {227*500*1500/Pdep:.2f} s")
Pcab = 5e3
print(f"À titre de comparaison, maintenir un habitacle à ~45 °C par 25 °C extérieur correspond à quelques kW (~{Pcab/1e3:.0f} kW) : "
      f"rapport {400e6*(fr['gamma']+fr['epm'])/Pcab:.0e}")
print(f"Même si « 300-500 MW » désignait la seule part photonique à blindage parfait et refroidissement idéal, "
      f"le coffre devrait évacuer ~{400e6/1e6:.0f} MW : densité ~{400e6/0.13:.1e} W/m^3 (cœur de réacteur REP : ~1e8 W/m^3).")
R["G"] = dict(T_equilibre_K_300MW=((300e6*(fr['gamma']+fr['epm']))/(sigma*A))**0.25)

# ----------------------------------------------------------------------------- H. énergie de création
titre("H. Énergie de création (« E = mc² peut se résoudre pour la masse »)")
E_world = 6.0e20     # J/an, énergie primaire mondiale ~ 600 EJ/an (ordre de grandeur 2020)
E_lhc_beam = 362e6   # J, énergie stockée par faisceau du LHC au nominal (7 TeV)
E_z = 2e6            # J, rayons X de la Z machine (Sandia, fin des années 1990 ; ordre de grandeur)
m_planck = math.sqrt(hbar*c/G)
for M, lab in ((227.0, "227 kg (toute l'unité)"), (2*2.9e11/2, "2,9e11 kg (2 g à 1 m)"), (2e12, "2 x 1e12 kg"), (8.8e12, "2 x 4,4e12 kg")):
    E = M*c**2
    print(f"{lab:26s}: E = {E:.2e} J = {E/E_world:.2e} années d'énergie primaire mondiale = {E/L_sun:.2e} s de luminosité solaire "
          f"= {E/E_lhc_beam:.1e} faisceaux LHC = {E/E_z:.1e} tirs de Z")
print(f"Masse de Planck = {m_planck:.3e} kg = {m_planck*c**2/1.602e-10:.2e} GeV ; énergie d'une collision LHC = 1,4e4 GeV "
      f"-> rapport {m_planck*c**2/1.602e-10/1.4e4:.1e}")
M_tev = 5e3*1.602e-10/c**2
print(f"Trou noir « TeV » hypothétique (dimensions supplémentaires) : M ~ 5 TeV = {M_tev:.1e} kg ; rapport à 1e12 kg : {1e12/M_tev:.1e} ; "
      f"durée de vie ~1e-26 s (ordre de grandeur publié), aucune pesanteur mesurable.")
R["H"] = dict(E_2e12kg_J=2e12*c**2, annees_energie_mondiale=2e12*c**2/E_world, s_luminosite_solaire=2e12*c**2/L_sun)

# ----------------------------------------------------------------------------- I. deux trous noirs proches
titre("I. Deux trous noirs voisins : force mutuelle, orbite, coalescence gravitationnelle")
for M in (1.45e11, 1e12):
    for d in (0.15, 0.30):
        F = G*M*M/d**2
        w = math.sqrt(G*2*M/d**3)
        t_gw = (5/256)*c**5*d**4/(G**3*M*M*2*M)
        print(f"M = {M:.2e} kg, d = {d:.2f} m : F = {F:.2e} N ; si orbite mutuelle : f = {w/2/math.pi:.1f} Hz, v = {w*d/2:.1f} m/s ; "
              f"coalescence par ondes gravitationnelles : {t_gw:.1e} s ({t_gw/yr:.1e} a)")
print("-> la coalescence par rayonnement gravitationnel n'est PAS un problème (objection faible) ;")
print("   le problème est la tenue statique (logements fixes des dessins) : ~1e14-1e15 N entre deux objets de taille fm,")
print("   ou bien une orbite mutuelle à ~10 Hz que les dessins ne montrent pas, et de toute façon le poids (section E).")
print("   Remarque honnête : deux trous noirs chargés extrêmes de même signe sont en équilibre statique (Majumdar-Papapetrou),")
print("   mais alors T_Hawking = 0 (pas de 300-500 MW) et la charge extrême est instantanément neutralisée (section E).")

# ----------------------------------------------------------------------------- J. position de la Terre
titre("J. « Verrou de gravité » : chemin parcouru par la Terre pendant le saut")
dt = 61*yr; tau = 6.1*3600
for v, lab in ((29.78e3, "orbite terrestre (réf. Soleil)"), (230e3, "Soleil autour de la Galaxie"), (370e3, "Soleil / fond cosmologique")):
    L = v*dt
    print(f"{lab:32s}: v = {v/1e3:.0f} km/s -> {L:.2e} m en 61 ans ; rapporté aux 6,1 h propres : {L/tau:.2e} m/s = {L/tau/c:.1f} c")
print("-> « rester collé à la Terre » sur 61 ans en 6,1 h de temps propre n'a de sens que si l'on suit la ligne d'univers")
print("   de la Terre à rebours ; aucune géométrie connue (Kerr, Tipler) ne fournit de courbe fermée de genre temps de ce type.")

# ----------------------------------------------------------------------------- K. conservation, divers
titre("K. Divers : divergence, suspension, air, creusement du sol")
print(f"Divergence : unité « sûre à ~1 % par 60 ans » vs 2,5 % annoncés pour 61 ans (2036->1975) : rapport {2.5/(61/60):.2f}")
print(f"Masse de l'unité 227 kg vs trois adultes de 80 kg = 240 kg : aucune suspension renforcée nécessaire.")
V_cab = 3.0; n = 1
co2 = 0.020*6.1*n/V_cab*100
print(f"Air : 1 personne, {V_cab:.0f} m^3, 6,1 h : CO2 ~ {co2:.1f} % (seuil dangereux ~4 %) ; O2 consommé ~{0.025*6.1:.2f} m^3 -> oxygène d'appoint plausible.")
print(f"Sol : « 1 pied cube sur 6 pieds carrés » = {1/6*12:.0f} pouces d'épaisseur moyenne, mais le texte dit « un pouce ou à peu près » (facteur 2).")

# ----------------------------------------------------------------------------- L. chiffres du « steelman »
titre("L. Version la plus défendable (steelman) : deux trous de Kerr-Newman quasi extrêmes de 1,45e11 kg")
Ms = 1.45e11; Mt = 2*Ms
print(f"g à 1 m = {G*Mt/g0:.2f} g ; g à 3,7 m = {G*Mt/3.7**2/g0:.2f} g ; distance où le signal vaut 1 µGal : {math.sqrt(G*Mt/1e-8)/1e3:.0f} km")
print(f"poids par trou = {Ms*g0:.2e} N ; charge extrême = {Q_coef*Ms:.1f} C ; horizon extrême GM/c^2 = {G*Ms/c**2*1e15:.2f} fm ; r_s = {rs_coef*Ms*1e15:.2f} fm")
print(f"énergie de fabrication = {Mt*c**2:.2e} J = {Mt*c**2/E_world:.1e} années d'énergie primaire mondiale")
Rz = 3.0
print(f"énergie négative d'ordre -R c^2/G pour une région de R = {Rz:.0f} m : -{Rz*c**2/G:.1e} kg (= {Rz*c**2/G/M_jup:.1f} M_Jupiter)")
R["L_steelman"] = dict(dist_1microGal_km=math.sqrt(G*Mt/1e-8)/1e3, poids_par_trou_N=Ms*g0, Q_ext_C=Q_coef*Ms, masse_negative_kg=Rz*c**2/G)

with open(__file__.replace("01_physique_c204.py", "resultats_physique.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, indent=1, ensure_ascii=False, default=float)
print("\n-> resultats_physique.json écrit.")
