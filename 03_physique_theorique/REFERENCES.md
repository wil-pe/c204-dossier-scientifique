# Références — Équipe B (physique théorique)

Règle appliquée : aucune référence inventée. Chaque entrée a été confrontée à une source en ligne les
10–11 novembre 2026 :

- **Crossref** : API `https://api.crossref.org/works?query.bibliographic=…` — 227 requêtes ; script
  `verifications/00_verif_references_crossref.py` ; réponses brutes dans `verifications/sorties/refs_crossref/` ;
  résumé dans `verifications/sorties/refs_crossref_resume.txt`.
- **arXiv** : API `https://export.arxiv.org/api/query` — 16 requêtes ; résumé dans
  `verifications/sorties/refs_arxiv_resume.txt`.
- **INSPIRE-HEP** : API `https://inspirehep.net/api/literature` — 6 requêtes (résumés relus lors des corrections
  post-validation, et recherche en texte intégral) ; résumé dans `verifications/sorties/refs_inspire_resume.txt`.

Statuts :

- **V-CR** : vérifiée en ligne (Crossref) — auteurs, titre, année, revue, volume et pages (ou numéro d'article) concordent.
- **V-AX** : vérifiée en ligne (arXiv).
- **V-IN** : vérifiée en ligne (INSPIRE-HEP).
- **V-ind** : existence de l'ouvrage confirmée indirectement (recension ou réédition indexée), contenu non consulté.
- **NV** : non vérifiée en ligne — citée de mémoire ; à confirmer avant toute reprise dans le dossier final.

« Vérifiée » porte sur l'**existence et les métadonnées** de la référence. Le contenu des articles n'a pas été
relu intégralement : lorsque nous attribuons un résultat précis à un article, c'est d'après notre connaissance de
la littérature, sauf pour les résumés effectivement consultés sur arXiv ou INSPIRE (signalés par †).

Recherche de l'expression exacte « Tipler sinusoid » : **0 résultat** dans les métadonnées d'arXiv
(`all:"Tipler sinusoid"`, titres et résumés) ; **1 résultat** en texte intégral sur INSPIRE
(`fulltext:"Tipler sinusoid"`) : arXiv:1008.3244 (2010), postérieur au récit.

---

## 1. Kerr, Kerr-Newman, structure interne

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| R. P. Kerr (1963). Gravitational field of a spinning mass as an example of algebraically special metrics. *Phys. Rev. Lett.* 11, 237–238 | 10.1103/PhysRevLett.11.237 | V-CR | §2, §13 |
| E. T. Newman, E. Couch, K. Chinnapared, A. Exton, A. Prakash, R. Torrence (1965). Metric of a rotating, charged mass. *J. Math. Phys.* 6, 918–919 | 10.1063/1.1704351 | V-CR | §2 |
| R. H. Boyer, R. W. Lindquist (1967). Maximal analytic extension of the Kerr metric. *J. Math. Phys.* 8, 265–281 | 10.1063/1.1705193 | V-CR | §2.4 |
| B. Carter (1968). Global structure of the Kerr family of gravitational fields. *Phys. Rev.* 174, 1559–1571 | 10.1103/PhysRev.174.1559 † | V-CR | §2.2–2.4, D4 |
| W. Israel (1967). Event horizons in static vacuum space-times. *Phys. Rev.* 164, 1776–1779 | 10.1103/PhysRev.164.1776 | V-CR | §2.2 |
| B. Carter (1971). Axisymmetric black hole has only two degrees of freedom. *Phys. Rev. Lett.* 26, 331–333 | 10.1103/PhysRevLett.26.331 | V-CR | §2.2 |
| D. C. Robinson (1975). Uniqueness of the Kerr black hole. *Phys. Rev. Lett.* 34, 905–906 | 10.1103/PhysRevLett.34.905 | V-CR | §2.2 |
| R. Penrose (1965). Gravitational collapse and space-time singularities. *Phys. Rev. Lett.* 14, 57–59 | 10.1103/PhysRevLett.14.57 | V-CR | contexte |
| R. Penrose (1969). Gravitational collapse: the role of general relativity. *Riv. Nuovo Cimento* (n° spécial) 1, 252 ; réimpr. *Gen. Relativ. Gravit.* 34, 1141–1165 (2002) | 10.1023/A:1016578408204 (réimpression) | V-CR (réimpression) | énergie de rotation |
| R. Penrose, R. M. Floyd (1971). Extraction of rotational energy from a black hole. *Nature Phys. Sci.* 229, 177–179 | 10.1038/physci229177a0 | V-CR | §2.2 |
| D. Christodoulou (1970). Reversible and irreversible transformations in black-hole physics. *Phys. Rev. Lett.* 25, 1596–1597 | 10.1103/PhysRevLett.25.1596 | V-CR | §2.2 |
| D. Christodoulou, R. Ruffini (1971). Reversible transformations of a charged black hole. *Phys. Rev. D* 4, 3552–3555 | 10.1103/PhysRevD.4.3552 | V-CR | §4.5, D7 |
| J. M. Bardeen, W. H. Press, S. A. Teukolsky (1972). Rotating black holes: locally nonrotating frames, energy extraction, and scalar synchrotron radiation. *Astrophys. J.* 178, 347 | 10.1086/151796 | V-CR | ergosphère |
| M. Simpson, R. Penrose (1973). Internal instability in a Reissner-Nordström black hole. *Int. J. Theor. Phys.* 7, 183–197 | 10.1007/BF00792069 | V-CR | §2.4 |
| E. Poisson, W. Israel (1989). Inner-horizon instability and mass inflation in black holes. *Phys. Rev. Lett.* 63, 1663–1666 | 10.1103/PhysRevLett.63.1663 | V-CR | §2.4 |
| E. Poisson, W. Israel (1990). Internal structure of black holes. *Phys. Rev. D* 41, 1796–1809 | 10.1103/PhysRevD.41.1796 | V-CR | §2.4 |
| A. Ori (1991). Inner structure of a charged black hole: an exact mass-inflation solution. *Phys. Rev. Lett.* 67, 789–792 | 10.1103/PhysRevLett.67.789 | V-CR | §2.4 |
| A. Ori (1992). Structure of the singularity inside a realistic rotating black hole. *Phys. Rev. Lett.* 68, 2117–2120 | 10.1103/PhysRevLett.68.2117 | V-CR | §2.4 |
| A. Ori (1999). Oscillatory null singularity inside realistic spinning black holes. *Phys. Rev. Lett.* 83, 5423–5426 | 10.1103/PhysRevLett.83.5423 | V-CR | complément |
| M. Dafermos (2005). The interior of charged black holes and the problem of uniqueness in general relativity. *Commun. Pure Appl. Math.* 58, 445–504 | 10.1002/cpa.20071 | V-CR | §2.4 |
| M. Dafermos, J. Luk (2025). The interior of dynamical vacuum black holes I: The C⁰-stability of the Kerr Cauchy horizon. *Ann. of Math.* 202, 309–630 | 10.4007/annals.2025.202.2.1 ; arXiv:1710.01722 | V-CR, V-AX | §2.4, §12 |
| D. Marolf, A. Ori (2012). Outgoing gravitational shock wave at the inner horizon: the late-time limit of black hole interiors. *Phys. Rev. D* 86, 124026 | 10.1103/PhysRevD.86.124026 | V-CR | complément |
| N. D. Birrell, P. C. W. Davies (1978). On falling through a black hole into another universe. *Nature* 272, 35–37 | 10.1038/272035a0 | V-CR | §2.4 |
| W. A. Hiscock (1977). Stress-energy tensor near a charged, rotating, evaporating black hole. *Phys. Rev. D* 15, 3054–3057 | 10.1103/PhysRevD.15.3054 | V-CR | complément |
| N. Zilberman, A. Levi, A. Ori (2020). Quantum fluxes at the inner horizon of a spherical charged black hole. *Phys. Rev. Lett.* 124, 171302 | 10.1103/PhysRevLett.124.171302 | V-CR | §2.4 |
| N. Zilberman, M. Casals, A. Ori, A. C. Ottewill (2022). Quantum fluxes at the inner horizon of a spinning black hole. *Phys. Rev. Lett.* 129, 261102 | 10.1103/PhysRevLett.129.261102 | V-CR | §2.4 |
| S. Hollands, R. M. Wald, J. Zahn (2020). Quantum instability of the Cauchy horizon in Reissner–Nordström–deSitter spacetime. *Class. Quantum Grav.* 37, 115009 | 10.1088/1361-6382/ab8052 | V-CR | §2.4 |
| M. Visser (2007). The Kerr spacetime: a brief introduction | arXiv:0706.0622 | V-AX | introduction |

## 2. Van Stockum, Tipler, systèmes à deux trous noirs

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| W. J. van Stockum (1937). The gravitational field of a distribution of particles rotating about an axis of symmetry. *Proc. R. Soc. Edinburgh* 57, 135–154 (Crossref date la mise en ligne de 1938) | 10.1017/S0370164600013699 | V-CR | §3.1 |
| C. Lanczos (1924). Über eine stationäre Kosmologie im Sinne der Einsteinschen Gravitationstheorie. *Z. Phys.* 21, 73–110 | 10.1007/BF01328251 | V-CR | antécédent |
| T. Lewis (1932). Some special solutions of the equations of axially symmetric gravitational fields. *Proc. R. Soc. A* 136, 176–192 | 10.1098/rspa.1932.0073 | V-CR | extérieurs |
| F. J. Tipler (1974). Rotating cylinders and the possibility of global causality violation. *Phys. Rev. D* 9, 2203–2206 | 10.1103/PhysRevD.9.2203 † | V-CR | §3, D10 (« a closed timelike line to connect any two events ») |
| J. Prezens (2010). The double Kerr solution as a possible mechanism for controlled global causality violation (prépublication) | arXiv:1008.3244 | V-IN (INSPIRE) | §3.3 : seule occurrence en texte intégral de « Tipler sinusoid », postérieure au récit ; contenu non évalué |
| F. J. Tipler (1976). Causality violation in asymptotically flat space-times. *Phys. Rev. Lett.* 37, 879–882 | 10.1103/PhysRevLett.37.879 | V-CR | §3.4 |
| F. J. Tipler (1977). Singularities and causality violation. *Ann. Phys.* 108, 1–36 | 10.1016/0003-4916(77)90348-7 | V-CR | §3.4 |
| W. B. Bonnor (1980). The rigidly rotating relativistic dust cylinder. *J. Phys. A* 13, 2121–2132 | 10.1088/0305-4470/13/6/033 | V-CR | complément |
| S. D. Majumdar (1947). A class of exact solutions of Einstein's field equations. *Phys. Rev.* 72, 390–398 | 10.1103/PhysRev.72.390 | V-CR | §3.5 |
| A. Papapetrou (1947). A static solution of the equations of the gravitational field for an arbitrary charge-distribution. *Proc. R. Irish Acad. A* 51, 191 | — | **NV** | §3.5 |
| J. B. Hartle, S. W. Hawking (1972). Solutions of the Einstein-Maxwell equations with many black holes. *Commun. Math. Phys.* 26, 87–101 | 10.1007/BF01645696 | V-CR | §3.5 |
| R. Bach, H. Weyl (1922). Neue Lösungen der Einsteinschen Gravitationsgleichungen. *Math. Z.* 13, 134–145 | 10.1007/BF01485284 | V-CR | §3.5 |
| D. Kramer, G. Neugebauer (1980). The superposition of two Kerr solutions. *Phys. Lett. A* 75, 259–261 | 10.1016/0375-9601(80)90556-3 | V-CR | §3.5 |
| W. Dietz, C. Hoenselaers (1985). Two mass solutions of Einstein's vacuum equations: the double Kerr solution. *Ann. Phys.* 165, 319–383 | 10.1016/0003-4916(85)90301-X | V-CR | §3.5 |
| V. S. Manko, E. Ruiz (2019). Metric for two arbitrary Kerr sources. *Phys. Lett. B* 794, 36–40 | 10.1016/j.physletb.2019.05.027 | V-CR | §3.5 |
| G. Neugebauer, J. Hennig (2009). Non-existence of stationary two-black-hole configurations. *Gen. Relativ. Gravit.* 41, 2113–2130 | 10.1007/s10714-009-0840-8 | V-CR | §3.5, Q2 |
| J. Hennig, G. Neugebauer (2011). Non-existence of stationary two-black-hole configurations: the degenerate case. *Gen. Relativ. Gravit.* 43, 3139–3162 | 10.1007/s10714-011-1228-0 | V-CR | §3.5 |
| W. Kinnersley, M. Walker (1970). Uniformly accelerating charged mass in general relativity. *Phys. Rev. D* 2, 1359–1370 | 10.1103/PhysRevD.2.1359 | V-CR | §3.5 |
| R. Wald (1972). Gravitational spin interaction. *Phys. Rev. D* 6, 406–413 | 10.1103/PhysRevD.6.406 | V-CR | §3.5 |
| P. C. Peters (1964). Gravitational radiation and the motion of two point masses. *Phys. Rev.* 136, B1224–B1232 | 10.1103/PhysRev.136.B1224 | V-CR | §3.5 |
| W. Israel (1966). Singular hypersurfaces and thin shells in general relativity. *Nuovo Cimento B* 44, 1–14 | 10.1007/BF02710419 | V-CR | D5 |

## 3. Rayonnement de Hawking, micro-trous noirs, charge, superradiance

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| S. Hawking (1971). Gravitationally collapsed objects of very low mass. *Mon. Not. R. Astron. Soc.* 152, 75–78 | 10.1093/mnras/152.1.75 | V-CR | §4, §10 |
| S. W. Hawking (1974). Black hole explosions? *Nature* 248, 30–31 | 10.1038/248030a0 | V-CR | §4.1 |
| S. W. Hawking (1975). Particle creation by black holes. *Commun. Math. Phys.* 43, 199–220 | 10.1007/BF02345020 | V-CR | §4.1 |
| J. D. Bekenstein (1973). Black holes and entropy. *Phys. Rev. D* 7, 2333–2346 | 10.1103/PhysRevD.7.2333 | V-CR | contexte |
| D. N. Page (1976). Particle emission rates from a black hole: massless particles from an uncharged, nonrotating hole. *Phys. Rev. D* 13, 198–206 | 10.1103/PhysRevD.13.198 † | V-CR | §4.1 (valeurs de contrôle) |
| D. N. Page (1976). Particle emission rates from a black hole. II. Massless particles from a rotating hole. *Phys. Rev. D* 14, 3260–3273 | 10.1103/PhysRevD.14.3260 † | V-CR | §4.6 : le moment cinétique est émis plusieurs fois plus vite que l'énergie ; puissance accrue par la rotation |
| D. N. Page (1977). Particle emission rates from a black hole. III. Charged leptons from a nonrotating hole. *Phys. Rev. D* 16, 2402–2411 | 10.1103/PhysRevD.16.2402 † | V-CR | §4.5, D7 : charge quadratique moyenne 6,14 e |
| W. G. Unruh (1976). Absorption cross section of small black holes. *Phys. Rev. D* 14, 3251–3259 | 10.1103/PhysRevD.14.3251 | V-CR | script 08 |
| J. H. MacGibbon, B. R. Webber (1990). Quark- and gluon-jet emission from primordial black holes: the instantaneous spectra. *Phys. Rev. D* 41, 3052–3079 | 10.1103/PhysRevD.41.3052 | V-CR | §4.1, D8 |
| J. H. MacGibbon (1991). Quark- and gluon-jet emission from primordial black holes. II. The emission over the black-hole lifetime. *Phys. Rev. D* 44, 376–392 | 10.1103/PhysRevD.44.376 | V-CR | D8 |
| J. H. MacGibbon, B. J. Carr, D. N. Page (2008). Do evaporating black holes form photospheres? *Phys. Rev. D* 78, 064043 | 10.1103/PhysRevD.78.064043 | V-CR | contrôle M* |
| B. J. Carr, K. Kohri, Y. Sendouda, J. Yokoyama (2010). New cosmological constraints on primordial black holes. *Phys. Rev. D* 81, 104019 | 10.1103/PhysRevD.81.104019 | V-CR | contexte |
| D. A. Leahy, W. G. Unruh (1979). Angular dependence of neutrino emission from rotating black holes. *Phys. Rev. D* 19, 3509–3515 | 10.1103/PhysRevD.19.3509 | V-CR | §4.2 : asymétrie d'émission des neutrinos uniquement ; l'absence de collimation est une déduction de notre part |
| C. M. Chambers, W. A. Hiscock, B. Taylor (1997). Spinning down a black hole with scalar fields. *Phys. Rev. Lett.* 78, 3249–3251 | 10.1103/PhysRevLett.78.3249 † | V-CR | §4.6, citée comme **exception** : émission scalaire, état final a/M ≈ 0,555 (mal employée dans la version 1) |
| W. T. Zaumen (1974). Upper bound on the electric charge of a black hole. *Nature* 247, 530–531 | 10.1038/247530a0 | V-CR | §4.5 |
| B. Carter (1974). Charge and particle conservation in black-hole decay. *Phys. Rev. Lett.* 33, 558–561 | 10.1103/PhysRevLett.33.558 | V-CR | §4.5 |
| G. W. Gibbons (1975). Vacuum polarization and the spontaneous loss of charge by black holes. *Commun. Math. Phys.* 44, 245–264 | 10.1007/BF01609829 | V-CR | §4.5 |
| T. Damour, R. Ruffini (1975). Quantum electrodynamical effects in Kerr-Newmann geometries. *Phys. Rev. Lett.* 35, 463–466 | 10.1103/PhysRevLett.35.463 | V-CR | §4.5 |
| W. A. Hiscock, L. D. Weems (1990). Evolution of charged evaporating black holes. *Phys. Rev. D* 41, 1142–1151 | 10.1103/PhysRevD.41.1142 | V-CR | complément |
| J. Schwinger (1951). On gauge invariance and vacuum polarization. *Phys. Rev.* 82, 664–679 | 10.1103/PhysRev.82.664 | V-CR | §4.5, §8 |
| W. H. Press, S. A. Teukolsky (1972). Floating orbits, superradiant scattering and the black-hole bomb. *Nature* 238, 211–212 | 10.1038/238211a0 | V-CR | §4.6 |
| S. A. Teukolsky, W. H. Press (1974). Perturbations of a rotating black hole. III. *Astrophys. J.* 193, 443 | 10.1086/153180 | V-CR | §4.6 |
| W. G. Unruh (1974). Second quantization in the Kerr metric. *Phys. Rev. D* 10, 3194–3205 | 10.1103/PhysRevD.10.3194 | V-CR | complément |
| J. D. Bekenstein, M. Schiffer (1998). The many faces of superradiance. *Phys. Rev. D* 58, 064014 | 10.1103/PhysRevD.58.064014 | V-CR | complément |
| R. Brito, V. Cardoso, P. Pani (2020). *Superradiance*, 2ᵉ éd., Lect. Notes Phys. 971 | 10.1007/978-3-030-46622-0 ; arXiv:1501.06570 | V-CR, V-AX | revue |
| N. Arkani-Hamed, S. Dimopoulos, G. Dvali (1998). The hierarchy problem and new dimensions at a millimeter. *Phys. Lett. B* 429, 263–272 | 10.1016/S0370-2693(98)00466-3 | V-CR | §4.7 |
| S. Dimopoulos, G. Landsberg (2001). Black holes at the Large Hadron Collider. *Phys. Rev. Lett.* 87, 161602 | 10.1103/PhysRevLett.87.161602 | V-CR | §4.7 |
| S. B. Giddings, S. Thomas (2002). High energy colliders as black hole factories: the end of short distance physics. *Phys. Rev. D* 65, 056010 | 10.1103/PhysRevD.65.056010 | V-CR | §4.7 |
| R. Emparan, G. T. Horowitz, R. C. Myers (2000). Black holes radiate mainly on the brane. *Phys. Rev. Lett.* 85, 499–502 | 10.1103/PhysRevLett.85.499 | V-CR | complément |
| S. B. Giddings, M. L. Mangano (2008). Astrophysical implications of hypothetical stable TeV-scale black holes. *Phys. Rev. D* 78, 035009 | 10.1103/PhysRevD.78.035009 | V-CR | §4.7 |
| CMS Collaboration (2011). Search for microscopic black hole signatures at the Large Hadron Collider. *Phys. Lett. B* 697, 434 | arXiv:1012.3375 | V-AX | §4.7 |
| CMS Collaboration (2018). Search for black holes and sphalerons in high-multiplicity final states in proton-proton collisions at √s = 13 TeV. *JHEP* 11 (2018) 042 | arXiv:1805.06013 | V-AX | §4.7 |
| J. G. Lee, E. G. Adelberger, T. S. Cook, S. M. Fleischer, B. R. Heckel (2020). New test of the gravitational 1/r² law at separations down to 52 μm. *Phys. Rev. Lett.* 124, 101101 | 10.1103/PhysRevLett.124.101101 | V-CR | dimensions supplémentaires |
| Y. Aharonov, A. Casher, S. Nussinov (1987). The unitarity puzzle and Planck mass stable particles. *Phys. Lett. B* 191, 51–55 | 10.1016/0370-2693(87)91320-7 | V-CR | §4.7 |
| J. H. MacGibbon (1987). Can Planck-mass relics of evaporating black holes close the Universe? *Nature* 329, 308–309 | 10.1038/329308a0 | V-CR | §4.7 |
| R. J. Adler, P. Chen, D. I. Santiago (2001). The generalized uncertainty principle and black hole remnants. *Gen. Relativ. Gravit.* 33, 2101–2108 | 10.1023/A:1015281430411 | V-CR | §4.7 |
| P. Chen, Y. C. Ong, D.-h. Yeom (2015). Black hole remnants and the information loss paradox. *Phys. Rep.* 603, 1–45 | 10.1016/j.physrep.2015.10.007 | V-CR | §4.7 |
| J. Maldacena (2021). Comments on magnetic black holes. *JHEP* 04 (2021) 079 | 10.1007/JHEP04(2021)079 ; arXiv:2004.06084 † | V-CR, V-AX | §12.1 |
| R. M. Wald (1974). Black hole in a uniform magnetic field. *Phys. Rev. D* 10, 1680–1685 | 10.1103/PhysRevD.10.1680 | V-CR | §8.1, Q5 |
| S. W. Hawking (1988). *A Brief History of Time*. Bantam (trad. fr. *Une brève histoire du temps*) | — | **NV** | §4.2 (source possible, [HYP]) |
| K. S. Thorne (1972). Conjecture du cerceau, dans *Magic Without Magic: John Archibald Wheeler*, Freeman | — | **NV** | §4.7 |

## 4. Dilatation du temps, fonctions de temps, mesures

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| S. W. Hawking (1969). The existence of cosmic time functions. *Proc. R. Soc. A* 308, 433–435 | 10.1098/rspa.1969.0018 | V-CR | §5.5, D1 |
| R. Geroch (1970). Domain of dependence. *J. Math. Phys.* 11, 437–449 | 10.1063/1.1665157 | V-CR | D1 |
| A. N. Bernal, M. Sánchez (2003). On smooth Cauchy hypersurfaces and Geroch's splitting theorem. *Commun. Math. Phys.* 243, 461–470 | 10.1007/s00220-003-0982-6 | V-CR | D1 |
| E. Minguzzi (2019). Lorentzian causality theory. *Living Rev. Relativ.* 22 | 10.1007/s41114-019-0019-x | V-CR | D1 |
| R. Geroch (1967). Topology in general relativity. *J. Math. Phys.* 8, 782–786 | 10.1063/1.1705276 | V-CR | complément |
| H. A. Buchdahl (1959). General relativistic fluid spheres. *Phys. Rev.* 116, 1027–1034 | 10.1103/PhysRev.116.1027 | V-CR | §5.3, D5 |
| H. Andréasson (2008). Sharp bounds on 2m/r of general spherically symmetric static objects. *J. Differ. Equ.* 245, 2243–2266 | 10.1016/j.jde.2008.05.010 | V-CR | §5.3, D5 |
| L. Lindblom (1984). Limits on the gravitational redshift form neutron stars [*sic*]. *Astrophys. J.* 278, 364 | 10.1086/161800 | V-CR | complément |
| R. C. Tolman (1930). On the weight of heat and thermal equilibrium in general relativity. *Phys. Rev.* 35, 904–924 | 10.1103/PhysRev.35.904 | V-CR | §5.4 |
| R. C. Tolman, P. Ehrenfest (1930). Temperature equilibrium in a static gravitational field. *Phys. Rev.* 36, 1791–1798 | 10.1103/PhysRev.36.1791 | V-CR | §5.4 |
| R. V. Pound, G. A. Rebka (1960). Apparent weight of photons. *Phys. Rev. Lett.* 4, 337–341 | 10.1103/PhysRevLett.4.337 | V-CR | contexte |
| J. C. Hafele, R. E. Keating (1972). Around-the-world atomic clocks: predicted relativistic time gains. *Science* 177, 166–168 | 10.1126/science.177.4044.166 | V-CR | §5.5, §13 |
| J. C. Hafele, R. E. Keating (1972). Around-the-world atomic clocks: observed relativistic time gains. *Science* 177, 168–170 | 10.1126/science.177.4044.168 | V-CR | §5.5, §13 |
| J. Bailey et al. (1977). Measurements of relativistic time dilatation for positive and negative muons in a circular orbit. *Nature* 268, 301–305 | 10.1038/268301a0 | V-CR | §5.5 |
| R. F. C. Vessot, M. W. Levine et al. (1980). Test of relativistic gravitation with a space-borne hydrogen maser. *Phys. Rev. Lett.* 45, 2081–2084 | 10.1103/PhysRevLett.45.2081 | V-CR | contexte |
| C. W. Chou, D. B. Hume, T. Rosenband, D. J. Wineland (2010). Optical clocks and relativity. *Science* 329, 1630–1633 | 10.1126/science.1192720 | V-CR | §5.5 |
| T. Bothwell et al. (2022). Resolving the gravitational redshift across a millimetre-scale atomic sample. *Nature* 602, 420–424 | 10.1038/s41586-021-04349-7 | V-CR | §5.5, Q6 |
| W. F. McGrew et al. (2018). Atomic clock performance enabling geodesy below the centimetre level. *Nature* 564, 87–90 | 10.1038/s41586-018-0738-2 | V-CR | contexte |
| A. Aeppli, K. Kim, W. Warfield, M. S. Safronova, J. Ye (2024). Clock with 8 × 10⁻¹⁹ systematic uncertainty. *Phys. Rev. Lett.* 133, 023401 | 10.1103/PhysRevLett.133.023401 | V-CR | §3.5 |
| C. W. F. Everitt et al. (2011). Gravity Probe B: final results of a space experiment to test general relativity. *Phys. Rev. Lett.* 106, 221101 | 10.1103/PhysRevLett.106.221101 | V-CR | §3.5 |
| I. Ciufolini, E. C. Pavlis (2004). A confirmation of the general relativistic prediction of the Lense–Thirring effect. *Nature* 431, 958–960 | 10.1038/nature03007 | V-CR | contexte |
| T. Westphal, H. Hepach, J. Pfaff, M. Aspelmeyer (2021). Measurement of gravitational coupling between millimetre-sized masses. *Nature* 591, 225–228 | 10.1038/s41586-021-03250-7 | V-CR | Q6 |
| T. M. Niebauer, G. S. Sasagawa, J. E. Faller, R. Hilt, F. Klopping (1995). A new generation of absolute gravimeters. *Metrologia* 32, 159–180 | 10.1088/0026-1394/32/3/004 | V-CR | §7.4 |
| V. Ménoret et al. (2018). Gravity measurements below 10⁻⁹ g with a transportable absolute quantum gravimeter. *Sci. Rep.* 8 | 10.1038/s41598-018-30608-1 | V-CR | §7.4 |

## 5. Autres voies vers les CTC ; conditions d'énergie

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| K. Gödel (1949). An example of a new type of cosmological solutions of Einstein's field equations of gravitation. *Rev. Mod. Phys.* 21, 447–450 | 10.1103/RevModPhys.21.447 | V-CR | §6 |
| J. R. Gott (1991). Closed timelike curves produced by pairs of moving cosmic strings: exact solutions. *Phys. Rev. Lett.* 66, 1126–1129 | 10.1103/PhysRevLett.66.1126 | V-CR | §6.1, D6 |
| S. Deser, R. Jackiw, G. 't Hooft (1992). Physical cosmic strings do not generate closed timelike curves. *Phys. Rev. Lett.* 68, 267–269 | 10.1103/PhysRevLett.68.267 | V-CR | §6.1 |
| S. M. Carroll, E. Farhi, A. H. Guth (1992). An obstacle to building a time machine. *Phys. Rev. Lett.* 68, 263–266 (erratum 68, 3368) | 10.1103/PhysRevLett.68.263 | V-CR | §6.1 |
| S. M. Carroll, E. Farhi, A. H. Guth, K. D. Olum (1994). Energy-momentum restrictions on the creation of Gott time machines. *Phys. Rev. D* 50, 6190–6206 | 10.1103/PhysRevD.50.6190 | V-CR | §6.1 |
| G. 't Hooft (1992). Causality in (2+1)-dimensional gravity. *Class. Quantum Grav.* 9, 1335–1348 | 10.1088/0264-9381/9/5/015 | V-CR | §6.1 |
| C. Cutler (1992). Global structure of Gott's two-string spacetime. *Phys. Rev. D* 45, 487–494 | 10.1103/PhysRevD.45.487 | V-CR | complément |
| A. Vilenkin (1981). Gravitational field of vacuum domain walls and strings. *Phys. Rev. D* 23, 852–857 | 10.1103/PhysRevD.23.852 | V-CR | corde conique |
| W. A. Hiscock (1985). Exact gravitational field of a string. *Phys. Rev. D* 31, 3288–3290 | 10.1103/PhysRevD.31.3288 | V-CR | corde conique |
| M. S. Morris, K. S. Thorne (1988). Wormholes in spacetime and their use for interstellar travel. *Am. J. Phys.* 56, 395–412 | 10.1119/1.15620 | V-CR | §6.2 |
| M. S. Morris, K. S. Thorne, U. Yurtsever (1988). Wormholes, time machines, and the weak energy condition. *Phys. Rev. Lett.* 61, 1446–1449 | 10.1103/PhysRevLett.61.1446 | V-CR | §5.5, §6.2, D1 |
| V. P. Frolov, I. D. Novikov (1990). Physical effects in wormholes and time machines. *Phys. Rev. D* 42, 1057–1065 | 10.1103/PhysRevD.42.1057 | V-CR | §5.5, D1 (résumé non relu) |
| J. L. Friedman, K. Schleich, D. M. Witt (1993). Topological censorship. *Phys. Rev. Lett.* 71, 1486–1489 | 10.1103/PhysRevLett.71.1486 | V-CR | §6.2 |
| D. Hochberg, M. Visser (1998). Null energy condition in dynamic wormholes. *Phys. Rev. Lett.* 81, 746–749 | 10.1103/PhysRevLett.81.746 | V-CR | §6.2 |
| M. Visser, S. Kar, N. Dadhich (2003). Traversable wormholes with arbitrarily small energy condition violations. *Phys. Rev. Lett.* 90, 201102 | 10.1103/PhysRevLett.90.201102 | V-CR | complément |
| C. J. Fewster, T. A. Roman (2005). On wormholes with arbitrarily small quantities of exotic matter. *Phys. Rev. D* 72, 044023 | 10.1103/PhysRevD.72.044023 | V-CR | complément |
| H. Epstein, V. Glaser, A. Jaffe (1965). Nonpositivity of the energy density in quantized field theories. *Nuovo Cimento* 36, 1016–1022 | 10.1007/BF02749799 | V-CR | §6.2 |
| L. H. Ford (1978). Quantum coherence effects and the second law of thermodynamics. *Proc. R. Soc. A* 364, 227–236 | 10.1098/rspa.1978.0197 | V-CR | §6.2 |
| L. H. Ford, T. A. Roman (1995). Averaged energy conditions and quantum inequalities. *Phys. Rev. D* 51, 4277–4286 | 10.1103/PhysRevD.51.4277 | V-CR | §6.2 |
| L. H. Ford, T. A. Roman (1996). Quantum field theory constrains traversable wormhole geometries. *Phys. Rev. D* 53, 5496–5507 | 10.1103/PhysRevD.53.5496 | V-CR | §6.2 |
| C. J. Fewster (2012). Lectures on quantum energy inequalities | arXiv:1208.5399 | V-AX | revue |
| E.-A. Kontou, K. Sanders (2020). Energy conditions in general relativity and quantum field theory. *Class. Quantum Grav.* 37, 193001 | 10.1088/1361-6382/ab8fcf | V-CR | revue |
| N. Graham, K. D. Olum (2007). Achronal averaged null energy condition. *Phys. Rev. D* 76, 064001 | 10.1103/PhysRevD.76.064001 | V-CR | §6.2 |
| T. Faulkner, R. G. Leigh, O. Parrikar, H. Wang (2016). Modular Hamiltonians for deformed half-spaces and the averaged null energy condition. *JHEP* 09 (2016) 038 | 10.1007/JHEP09(2016)038 | V-CR | §6.2 |
| T. Hartman, S. Kundu, A. Tajdini (2017). Averaged null energy condition from causality. *JHEP* 07 (2017) 066 | 10.1007/JHEP07(2017)066 | V-CR | §6.2 |
| P. Gao, D. L. Jafferis, A. C. Wall (2017). Traversable wormholes via a double trace deformation. *JHEP* 12 (2017) 151 | 10.1007/JHEP12(2017)151 | V-CR | §6.2 |
| J. Maldacena, A. Milekhin, F. Popov (2023). Traversable wormholes in four dimensions. *Class. Quantum Grav.* 40, 155016 | 10.1088/1361-6382/acde30 ; arXiv:1807.04726 | V-CR, V-AX | §6.2 |
| J. Maldacena, A. Milekhin (2021). Humanly traversable wormholes. *Phys. Rev. D* 103, 066007 | 10.1103/PhysRevD.103.066007 | V-CR | §6.2 |
| H. B. G. Casimir (1948). On the attraction between two perfectly conducting plates. *Proc. K. Ned. Akad. Wet.* 51, 793 | — | **NV** | §6.2 |
| L. S. Brown, G. J. Maclay (1969). Vacuum stress between conducting plates: an image solution. *Phys. Rev.* 184, 1272–1279 | 10.1103/PhysRev.184.1272 | V-CR | §6.2 |
| S. K. Lamoreaux (1997). Demonstration of the Casimir force in the 0.6 to 6 μm range. *Phys. Rev. Lett.* 78, 5–8 | 10.1103/PhysRevLett.78.5 | V-CR | §6.2 |
| U. Mohideen, A. Roy (1998). Precision measurement of the Casimir force from 0.1 to 0.9 μm. *Phys. Rev. Lett.* 81, 4549–4552 | 10.1103/PhysRevLett.81.4549 | V-CR | §6.2 |
| M. Alcubierre (1994). The warp drive: hyper-fast travel within general relativity. *Class. Quantum Grav.* 11, L73–L77 | 10.1088/0264-9381/11/5/001 | V-CR | §6.3, D9 |
| A. E. Everett (1996). Warp drive and causality. *Phys. Rev. D* 53, 7365–7368 | 10.1103/PhysRevD.53.7365 | V-CR | §6.3 |
| S. V. Krasnikov (1998). Hyperfast travel in general relativity. *Phys. Rev. D* 57, 4760–4766 | 10.1103/PhysRevD.57.4760 | V-CR | §6 |
| A. E. Everett, T. A. Roman (1997). Superluminal subway: the Krasnikov tube. *Phys. Rev. D* 56, 2100–2108 | 10.1103/PhysRevD.56.2100 | V-CR | §6 |
| M. J. Pfenning, L. H. Ford (1997). The unphysical nature of 'warp drive'. *Class. Quantum Grav.* 14, 1743–1751 | 10.1088/0264-9381/14/7/011 | V-CR | §6.3, D9 |
| E. W. Lentz (2021). Breaking the warp barrier: hyper-fast solitons in Einstein–Maxwell-plasma theory. *Class. Quantum Grav.* 38, 075015 | 10.1088/1361-6382/abe692 | V-CR | §6.3 |
| A. Bobrick, G. Martire (2021). Introducing physical warp drives. *Class. Quantum Grav.* 38, 105009 | 10.1088/1361-6382/abdf6e | V-CR | §6.3 |
| J. Santiago, S. Schuster, M. Visser (2022). Generic warp drives violate the null energy condition. *Phys. Rev. D* 105, 064038 | 10.1103/PhysRevD.105.064038 | V-CR | §6.3 |
| R. L. Mallett (2000). Weak gravitational field of the electromagnetic radiation in a ring laser. *Phys. Lett. A* 269, 214–217 | 10.1016/S0375-9601(00)00260-7 | V-CR | §6.4 |
| R. L. Mallett (2003). The gravitational field of a circulating light beam. *Found. Phys.* 33, 1307–1314 | 10.1023/A:1025689110828 | V-CR | §6.4 |
| K. D. Olum, A. Everett (2005). Can a circulating light beam produce a time machine? *Found. Phys. Lett.* 18, 379–385 | 10.1007/s10702-005-7127-4 ; arXiv:gr-qc/0410078 † | V-CR, V-AX | §6.4 |
| R. C. Tolman, P. Ehrenfest, B. Podolsky (1931). On the gravitational field produced by light. *Phys. Rev.* 37, 602–615 | 10.1103/PhysRev.37.602 | V-CR | §6.4 |
| A. Ori (1993). Must time-machine construction violate the weak energy condition? *Phys. Rev. Lett.* 71, 2517–2520 | 10.1103/PhysRevLett.71.2517 | V-CR | §3.4, §6.5 |
| A. Ori, Y. Soen (1994). Causality violation and the weak energy condition. *Phys. Rev. D* 49, 3990–3997 | 10.1103/PhysRevD.49.3990 | V-CR | complément |
| A. Ori (2005). A class of time-machine solutions with a compact vacuum core. *Phys. Rev. Lett.* 95, 021101 | 10.1103/PhysRevLett.95.021101 ; arXiv:gr-qc/0503077 † | V-CR, V-AX | §6.5 |
| A. Ori (2007). Formation of closed timelike curves in a composite vacuum/dust asymptotically flat spacetime. *Phys. Rev. D* 76, 044002 | 10.1103/PhysRevD.76.044002 ; arXiv:gr-qc/0701024 † | V-CR, V-AX | §6.5 |
| B. K. Tippett, D. Tsang (2017). Traversable acausal retrograde domains in spacetime. *Class. Quantum Grav.* 34, 095006 | 10.1088/1361-6382/aa6549 | V-CR | complément |
| D. Fermi, L. Pizzocchero (2018). A time machine for free fall into the past. *Class. Quantum Grav.* 35, 165003 | 10.1088/1361-6382/aace6e | V-CR | complément |
| S. Krasnikov (2018). *Back-in-Time and Faster-than-Light Travel in General Relativity*. Springer | 10.1007/978-3-319-72754-7 | V-CR | monographie |

## 6. Causalité, protection chronologique, modèles quantiques

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| S. W. Hawking (1992). Chronology protection conjecture. *Phys. Rev. D* 46, 603–611 | 10.1103/PhysRevD.46.603 | V-CR | §3.4, §7.1 |
| S.-W. Kim, K. S. Thorne (1991). Do vacuum fluctuations prevent the creation of closed timelike curves? *Phys. Rev. D* 43, 3929–3947 | 10.1103/PhysRevD.43.3929 | V-CR | §7.1 |
| B. S. Kay, M. J. Radzikowski, R. M. Wald (1997). Quantum field theory on spacetimes with a compactly generated Cauchy horizon. *Commun. Math. Phys.* 183, 533–556 | 10.1007/s002200050042 ; arXiv:gr-qc/9603012 † | V-CR, V-AX | §7.1 |
| S. V. Krasnikov (1996). Quantum stability of the time machine. *Phys. Rev. D* 54, 7322–7327 | 10.1103/PhysRevD.54.7322 | V-CR | §7.1 |
| M. Visser (1993). From wormhole to time machine: remarks on Hawking's chronology protection conjecture. *Phys. Rev. D* 47, 554–565 | 10.1103/PhysRevD.47.554 | V-CR | complément |
| M. Visser (2002). The quantum physics of chronology protection | arXiv:gr-qc/0204022 | V-AX | §7.1 |
| J. L. Friedman, A. Higuchi (2006). Topological censorship and chronology protection. *Ann. Phys.* 518 (= 15 de la 8ᵉ série), 109–128 (Crossref : mise en ligne 2005) | 10.1002/andp.200651801-209 | V-CR | revue |
| S. Krasnikov (2002). No time machines in classical general relativity. *Class. Quantum Grav.* 19, 4109–4129 | 10.1088/0264-9381/19/15/316 | V-CR | §6.5 |
| J. Earman, C. Smeenk, C. Wüthrich (2009). Do the laws of physics forbid the operation of time machines? *Synthese* 169, 91–124 | 10.1007/s11229-008-9338-2 | V-CR | §6.5 |
| J. Friedman, M. S. Morris, I. D. Novikov, F. Echeverria, G. Klinkhammer, K. S. Thorne, U. Yurtsever (1990). Cauchy problem in spacetimes with closed timelike curves. *Phys. Rev. D* 42, 1915–1930 | 10.1103/PhysRevD.42.1915 | V-CR | §7.2 |
| F. Echeverria, G. Klinkhammer, K. S. Thorne (1991). Billiard balls in wormhole spacetimes with closed timelike curves: classical theory. *Phys. Rev. D* 44, 1077–1099 | 10.1103/PhysRevD.44.1077 | V-CR | §7.2 |
| D. Deutsch (1991). Quantum mechanics near closed timelike lines. *Phys. Rev. D* 44, 3197–3217 | 10.1103/PhysRevD.44.3197 | V-CR | §7.3, §7.4 |
| D. Deutsch, M. Lockwood (1994). The quantum physics of time travel. *Sci. Am.* 270 (3), 68–74 | 10.1038/scientificamerican0394-68 | V-CR | §7.4 |
| H. D. Politzer (1992). Simple quantum systems in spacetimes with closed timelike curves. *Phys. Rev. D* 46, 4470–4476 | 10.1103/PhysRevD.46.4470 | V-CR | §7.3 |
| J. B. Hartle (1994). Unitarity and causality in generalized quantum mechanics for nonchronal spacetimes. *Phys. Rev. D* 49, 6543–6555 | 10.1103/PhysRevD.49.6543 | V-CR | §7.3 |
| S. Lloyd et al. (2011). Closed timelike curves via postselection: theory and experimental test of consistency. *Phys. Rev. Lett.* 106, 040403 | 10.1103/PhysRevLett.106.040403 | V-CR | §7.3 |
| S. Lloyd, L. Maccone, R. Garcia-Patron, V. Giovannetti, Y. Shikano (2011). Quantum mechanics of time travel through post-selected teleportation. *Phys. Rev. D* 84, 025007 | 10.1103/PhysRevD.84.025007 | V-CR | §7.3 |
| C. H. Bennett, D. Leung, G. Smith, J. A. Smolin (2009). Can closed timelike curves or nonlinear quantum mechanics improve quantum state discrimination or help solve hard problems? *Phys. Rev. Lett.* 103, 170502 | 10.1103/PhysRevLett.103.170502 | V-CR | §7.3 |
| S. Aaronson, J. Watrous (2009). Closed timelike curves make quantum and classical computing equivalent. *Proc. R. Soc. A* 465, 631–647 | 10.1098/rspa.2008.0350 | V-CR | §7.3 |
| M. Ringbauer, M. A. Broome, C. R. Myers, A. G. White, T. C. Ralph (2014). Experimental simulation of closed timelike curves. *Nat. Commun.* 5, 4145 | 10.1038/ncomms5145 | V-CR | §7.3 |
| J.-M. A. Allen (2014). Treating time travel quantum mechanically. *Phys. Rev. A* 90, 042107 | 10.1103/PhysRevA.90.042107 | V-CR | §7.3 |
| G. Tobar, F. Costa (2020). Reversible dynamics with closed time-like curves and freedom of choice. *Class. Quantum Grav.* 37, 205011 | 10.1088/1361-6382/aba4bc | V-CR | §7.3 |
| A. Everett (2004). Time travel paradoxes, path integrals, and the many worlds interpretation of quantum mechanics. *Phys. Rev. D* 69, 124023 | 10.1103/PhysRevD.69.124023 | V-CR | §7.4 |
| H. Everett (1957). "Relative state" formulation of quantum mechanics. *Rev. Mod. Phys.* 29, 454–462 | 10.1103/RevModPhys.29.454 | V-CR | §7.4 |
| B. S. DeWitt, N. Graham (dir.) (1973). *The Many-Worlds Interpretation of Quantum Mechanics*. Princeton Univ. Press (rééd. 2015) | 10.1515/9781400868056 | V-CR (réédition) | origine du sigle « Everett-Wheeler-Graham » |
| W. H. Zurek (2003). Decoherence, einselection, and the quantum origins of the classical. *Rev. Mod. Phys.* 75, 715–775 | 10.1103/RevModPhys.75.715 | V-CR | §7.4 |
| D. Wallace (2012). *The Emergent Multiverse*. Oxford Univ. Press | 10.1093/acprof:oso/9780199546961.001.0001 | V-CR | §7.4 |
| S. Weinberg (1989). Testing quantum mechanics. *Ann. Phys.* 194, 336–386 | 10.1016/0003-4916(89)90276-5 | V-CR | §7.4 |
| N. Gisin (1990). Weinberg's non-linear quantum mechanics and supraluminal communications. *Phys. Lett. A* 143, 1–2 | 10.1016/0375-9601(90)90786-N | V-CR | §7.4 |
| J. Polchinski (1991). Weinberg's nonlinear quantum mechanics and the Einstein-Podolsky-Rosen paradox. *Phys. Rev. Lett.* 66, 397–400 | 10.1103/PhysRevLett.66.397 | V-CR | §7.4 |
| J. J. Bollinger, D. J. Heinzen, W. M. Itano, S. L. Gilbert, D. J. Wineland (1989). Test of the linearity of quantum mechanics by rf spectroscopy of the ⁹Be⁺ ground state. *Phys. Rev. Lett.* 63, 1031–1034 | 10.1103/PhysRevLett.63.1031 | V-CR | §7.4 |

## 7. Champs électromagnétiques et gravité

| Référence | Identifiant | Statut | Usage |
|---|---|---|---|
| H. Reissner (1916). Über die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie. *Ann. Phys.* 355, 106–120 | 10.1002/andp.19163550905 | V-CR | §8.1 |
| G. Nordström (1918). On the energy of the gravitation field in Einstein's theory. *Proc. K. Ned. Akad. Wet.* 20, 1238 | — | **NV** | §8.1 |
| W. B. Bonnor (1954). Static magnetic fields in general relativity. *Proc. Phys. Soc. A* 67, 225–232 | 10.1088/0370-1298/67/3/305 | V-CR | §8.1 |
| M. A. Melvin (1964). Pure magnetic and electric geons. *Phys. Lett.* 8, 65–68 | 10.1016/0031-9163(64)90801-7 | V-CR | §8.2 |
| F. J. Ernst (1976). Black holes in a magnetic universe. *J. Math. Phys.* 17, 54–56 | 10.1063/1.522781 | V-CR | §8.1, Q5 |
| A. Füzfa (2016). How current loops and solenoids curve spacetime. *Phys. Rev. D* 93, 024014 | 10.1103/PhysRevD.93.024014 | V-CR | §8.1 |
| L. B. Kreuzer (1968). Experimental measurement of the equivalence of active and passive gravitational mass. *Phys. Rev.* 169, 1007–1012 | 10.1103/PhysRev.169.1007 | V-CR | §8.1 |
| D. F. Bartlett, D. Van Buren (1986). Equivalence of active and passive gravitational mass using the moon. *Phys. Rev. Lett.* 57, 21–24 | 10.1103/PhysRevLett.57.21 | V-CR | §8.1 |
| S. Hahn et al. (2019). 45.5-tesla direct-current magnetic field generated with a high-temperature superconducting magnet. *Nature* 570, 496–499 | 10.1038/s41586-019-1293-1 | V-CR | §8.3 |
| D. Nakamura, A. Ikeda, H. Sawabe, Y. H. Matsuda, S. Takeyama (2018). Record indoor magnetic field of 1200 T generated by electromagnetic flux-compression. *Rev. Sci. Instrum.* 89 | 10.1063/1.5044557 | V-CR | §8.3 |

## 8. Ouvrages généraux

| Référence | Identifiant | Statut |
|---|---|---|
| S. W. Hawking, G. F. R. Ellis (1973). *The Large Scale Structure of Space-Time*. Cambridge Univ. Press | 10.1017/CBO9780511524646 | V-CR |
| R. M. Wald (1984). *General Relativity*. Univ. of Chicago Press | 10.7208/chicago/9780226870373.001.0001 | V-CR |
| E. Poisson (2004). *A Relativist's Toolkit*. Cambridge Univ. Press | 10.1017/CBO9780511606601 | V-CR |
| C. W. Misner, K. S. Thorne, J. A. Wheeler (1973). *Gravitation*. Freeman | recension : 10.1063/1.3128805 | V-ind |
| S. Chandrasekhar (1983). *The Mathematical Theory of Black Holes*. Oxford Univ. Press | recension : 10.1126/science.222.4628.1116.a | V-ind |
| M. Visser (1995). *Lorentzian Wormholes: From Einstein to Hawking*. AIP Press | notice : 10.5860/choice.33-5168 | V-ind |
| K. S. Thorne (1994). *Black Holes and Time Warps*. Norton | recension : 10.1063/1.2808700 | V-ind |

## 9. Références recherchées mais non retenues ou non confirmées

| Élément | Résultat |
|---|---|
| « Tipler sinusoid » (expression exacte) | 0 résultat dans les métadonnées d'arXiv ; 1 occurrence en texte intégral (INSPIRE) : arXiv:1008.3244, 2010, postérieure au récit |
| A. A. Starobinsky (1973), amplification d'ondes par un trou noir en rotation (*Sov. Phys. JETP* 37, 28) | non trouvée sur Crossref : **NV**, non citée dans le rapport |
| I. D. Novikov (1989), analyse d'une machine temporelle (*Sov. Phys. JETP* 68, 439) | non recherchée : **NV**, non citée (remplacée par Friedman et al. 1990) |
| J. Lense, H. Thirring (1918), *Phys. Z.* 19, 156 | non trouvée sur Crossref : **NV**, non citée (remplacée par Everitt et al. 2011) |
| R. Penrose (1968), « Structure of space-time », Battelle Rencontres | non trouvée : **NV**, non citée (remplacée par Simpson & Penrose 1973) |
| C. W. Misner (1967), « Taub-NUT space as a counterexample to almost anything » | non trouvée : **NV**, non citée |
| Collaboration Planck (2014), recherche de cordes cosmiques | requête non concluante : **NV** ; la borne Gμ/c² ≲ 10⁻⁷ est donnée en ordre de grandeur sans référence |
| Valeurs numériques de MacGibbon & Webber (pics spectraux, facteur f(M)) | non reprises : remplacées par notre calcul (script 02) |
