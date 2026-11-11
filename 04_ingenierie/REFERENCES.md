# Programme C204 — Équipe C — Références et statut de vérification

Vérification effectuée le 10 novembre 2026 (API Crossref, API arXiv, pages constructeur/institut).
Aucune référence n'est inventée ; ce qui n'a pas pu être contrôlé est marqué comme tel.

| Code | Signification |
|---|---|
| **[C]** | Métadonnées (auteurs, année, revue, volume, page, DOI) confirmées par Crossref ou l'éditeur |
| **[C+]** | Idem, et chiffres utilisés confirmés dans le résumé ou le texte |
| **[P]** | Source primaire (constructeur, institut, norme) lue en ligne |
| **[E]** | Valeur vue seulement dans un extrait de moteur de recherche ou une source secondaire |
| **[N]** | Non vérifiée en ligne (citée de mémoire ; à contrôler avant réutilisation) |
| **[R]** | Résultat reproduit par nos propres calculs |

## A. Trous noirs : rayonnement, charge, rotation, capture

1. S. W. Hawking, « Black hole explosions? », *Nature* **248**, 30–31 (1974). DOI 10.1038/248030a0. **[C]**
2. S. W. Hawking, « Particle creation by black holes », *Commun. Math. Phys.* **43**, 199–220 (1975). DOI 10.1007/BF02345020 (erratum : CMP 46, 206, 1976). **[C]**
3. D. N. Page, « Particle emission rates from a black hole: Massless particles from an uncharged, nonrotating hole », *Phys. Rev. D* **13**, 198–206 (1976). DOI 10.1103/PhysRevD.13.198. **[C+][R]** — éq. (29) : P = 2,011×10⁻⁴ ħc⁶G⁻²M⁻² (81,4 % « quatre sortes de neutrinos », 16,7 % photons, 1,9 % gravitons) ; éq. (30) : 3,6×10⁻⁴ avec e± (45/45/9/1 %). Chiffres précis lus dans le corps de l'article (réimpression dans la thèse Caltech de l'auteur, https://thesis.caltech.edu/7179/) ; le résumé ne donne que les valeurs arrondies. Reproduits à 0,02 % près par `calculs/c01_hawking.py` (2,0114×10⁻⁴ ; 81,4/16,7/1,9 % ; 3,648×10⁻⁴).
4. D. N. Page & S. W. Hawking, « Gamma rays from primordial black holes », *Astrophys. J.* **206**, 1 (1976). DOI 10.1086/154350. **[C]** (recoupement des fractions 45/45/9/1 %).
5. D. N. Page, « Particle emission rates from a black hole. II. Massless particles from a rotating hole », *Phys. Rev. D* **14**, 3260–3273 (1976). DOI 10.1103/PhysRevD.14.3260. **[C+]** — le moment cinétique est émis plusieurs fois plus vite que l'énergie.
6. D. N. Page, « Particle emission rates from a black hole. III. Charged leptons from a nonrotating hole », *Phys. Rev. D* **16**, 2402–2411 (1977). DOI 10.1103/PhysRevD.16.2402. **[C+]** — charge rms 6,14 e (GMμ/ħc = 0), 2,76 e (0,4), 2,34 e (≫ 1) ; puissance des leptons massifs à 50 % de la valeur sans masse pour GMμ/ħc = 0,160, à 10 % pour 0,271.
7. G. W. Gibbons, « Vacuum polarization and the spontaneous loss of charge by black holes », *Commun. Math. Phys.* **44**, 245–264 (1975). DOI 10.1007/BF01609829. **[C]** — le résumé distingue deux régimes de part et d'autre de 10¹⁷ g ; il ne donne pas de « masse de décharge » : le seuil de 5×10⁵ M☉ de la fiche F1 est **notre** calcul (critère de Schwinger).
8. J. H. MacGibbon & B. R. Webber, « Quark- and gluon-jet emission from primordial black holes: The instantaneous spectra », *Phys. Rev. D* **41**, 3052–3079 (1990). DOI 10.1103/PhysRevD.41.3052. **[C]**
9. J. H. MacGibbon, « Quark- and gluon-jet emission from primordial black holes. II. The emission over the black-hole lifetime », *Phys. Rev. D* **44**, 376–392 (1991). DOI 10.1103/PhysRevD.44.376. **[C]**
10. J. H. MacGibbon, B. J. Carr & D. N. Page, « Do evaporating black holes form photospheres? », *Phys. Rev. D* **78**, 064043 (2008). DOI 10.1103/PhysRevD.78.064043. **[C+][R]** — éq. (6) : pics du flux à 2,81 T (s = 0), 4,02 T (s = ½), 5,77 T (s = 1) ; nous obtenons 2,21 ; 4,02 ; 5,73 (une autre source, Ukwatta et al. 2016, donne 2,19 pour s = 0).
11. J. Schwinger, « On Gauge Invariance and Vacuum Polarization », *Phys. Rev.* **82**, 664–679 (1951). DOI 10.1103/PhysRev.82.664. **[C]** — valeur E_S = m²c³/(eħ) = 1,323×10¹⁸ V/m recalculée (CODATA). **[R]**
12. R. Wald, « Gedanken experiments to destroy a black hole », *Ann. Phys.* **82**, 548–556 (1974). DOI 10.1016/0003-4916(74)90125-0. **[C]**
13. W. G. Unruh, « Absorption cross section of small black holes », *Phys. Rev. D* **14**, 3251–3259 (1976). DOI 10.1103/PhysRevD.14.3251. **[C+]** — section efficace de Dirac à basse énergie = 1/8 de celle du scalaire.
14. B. Carter, « Global Structure of the Kerr Family of Gravitational Fields », *Phys. Rev.* **174**, 1559–1571 (1968). DOI 10.1103/PhysRev.174.1559. **[C]** (rapport gyromagnétique g = 2 : attribution **[N]**, contenu non relu).
15. J. M. Bardeen, « Kerr Metric Black Holes », *Nature* **226**, 64–65 (1970). DOI 10.1038/226064a0. **[C]** (facteur √6 : **[N]**, contenu non relu).
16. D. A. Leahy & W. G. Unruh, « Angular dependence of neutrino emission from rotating black holes », *Phys. Rev. D* **19**, 3509–3515 (1979). DOI 10.1103/PhysRevD.19.3509. **[C+]**
17. B. J. Carr, K. Kohri, Y. Sendouda & J. Yokoyama, « New cosmological constraints on primordial black holes », *Phys. Rev. D* **81**, 104019 (2010). DOI 10.1103/PhysRevD.81.104019. **[C]**
18. L. Crane & S. Westmoreland, « Are Black Hole Starships Possible », arXiv:0908.1803 [gr-qc] (2009) ; prépublication, non évaluée par les pairs. **[C]**
19. S. Dimopoulos & G. Landsberg, « Black Holes at the Large Hadron Collider », *Phys. Rev. Lett.* **87**, 161602 (2001). DOI 10.1103/PhysRevLett.87.161602. **[C]**
20. S. B. Giddings & S. Thomas, « High energy colliders as black hole factories: The end of short distance physics », *Phys. Rev. D* **65**, 056010 (2002). DOI 10.1103/PhysRevD.65.056010. **[C]**
21. Collaboration CMS, recherche de trous noirs et de sphalérons, *JHEP* **11** (2018) 042. DOI 10.1007/JHEP11(2018)042 — trous noirs semi-classiques exclus jusqu'à 10,1 TeV. **[P]** https://cms-results.web.cern.ch/cms-results/public-results/publications/EXO-17-023/index.html
22. Conjecture du cerceau (K. S. Thorne, 1972). **[N]** — non retrouvée dans Crossref ; non utilisée dans les calculs.

## B. Piégeage, champs électriques et magnétiques

23. S. Earnshaw, « On the Nature of the Molecular Forces which regulate the Constitution of the Luminiferous Ether », *Trans. Camb. Phil. Soc.* **7**, 97–112 (1842). **[P]** scan https://archive.org/details/transactionsofca07camb (page de fin non contrôlée).
24. L. S. Brown & G. Gabrielse, « Geonium theory: Physics of a single electron or ion in a Penning trap », *Rev. Mod. Phys.* **58**, 233–311 (1986). DOI 10.1103/RevModPhys.58.233. **[C]**
25. W. Paul, « Electromagnetic traps for charged and neutral particles », *Rev. Mod. Phys.* **62**, 531–540 (1990). DOI 10.1103/RevModPhys.62.531. **[C]**
26. M. V. Berry & A. K. Geim, « Of flying frogs and levitrons », *Eur. J. Phys.* **18**, 307–313 (1997). DOI 10.1088/0143-0807/18/4/012. **[C]**
27. S. Hahn et al., « 45.5-tesla direct-current magnetic field generated with a high-temperature superconducting magnet », *Nature* **570**, 496–499 (2019). DOI 10.1038/s41586-019-1293-1. **[C]** — insert REBCO de 14,4 T dans un fond résistif de 31,1 T **[E]**.
28. National High Magnetic Field Laboratory : aimant hybride 45 T (11,5 T supra + 33,5 T résistif ; 30 MW selon la fiche, 33 MW selon « by the numbers ») ; record pulsé non destructif 100,75 T. **[P]** https://nationalmaglab.org/about-the-maglab/around-the-lab/meet-the-magnets/meet-the-45-tesla-hybrid-magnet/ ; https://nationalmaglab.org/about-the-maglab/facts-figures/by-the-numbers/ . Hybride de Hefei 45,22 T (2022) **[E]** ; aimant tout supraconducteur 32 T (2017) puis 35,1 T (2025) **[E]**.
29. D. Nakamura, A. Ikeda, H. Sawabe, Y. H. Matsuda & S. Takeyama, « Record indoor magnetic field of 1200 T generated by electromagnetic flux-compression », *Rev. Sci. Instrum.* **89**, 095106 (2018). DOI 10.1063/1.5044557. **[C+]** ; banc de 5 MJ : **[P]** https://www.issp.u-tokyo.ac.jp/maincontents/highlight/2018/28_en.html
30. Boriskov et al., *Phys.-Usp.* (2011), DOI 10.3367/UFNe.0181.201104n.0441 — ~28 MG (2 800 T) par compression explosive (VNIIEF). **[P]** pour la valeur ; année de l'expérience non confirmée.
31. F. C. Moon, « The virial theorem and scaling laws for superconducting magnet systems », *J. Appl. Phys.* **53**, 9112–9121 (1982). DOI 10.1063/1.330423. **[C]**
32. Gradient accélérateur CLIC : 100 MV/m en charge (linac 3 TeV). **[E]** https://accelconf.web.cern.ch/IPAC2012/papers/weya01.pdf ; rapport CLIC : https://arxiv.org/abs/1812.06018 **[P]**
33. Champ d'évaporation du tungstène, 57 V/nm (Seidman 2007). **[E]** https://panitz.unm.edu/home/References_files/Seidman_(2007a).pdf
34. Champ critique idéal du diamant ~10 MV/cm (Hollis et al., SAND2020-13717C). **[P]** https://www.osti.gov/servlets/purl/1835966
35. J. W. Yoon et al., « Realization of laser intensity over 10²³ W/cm² », *Optica* **8**, 630 (2021). DOI 10.1364/OPTICA.420520. **[C]**

## C. Faisceaux d'électrons

36. B. Dunham et al., « Record high-average current from a high-brightness photoinjector », *Appl. Phys. Lett.* **102**, 034105 (2013). DOI 10.1063/1.4789395. **[C+]** — 65 mA à 4–5 MeV.
37. A. J. Gonsalves et al., « Petawatt Laser Guiding and Electron Beam Acceleration to 8 GeV in a Laser-Heated Capillary Discharge Waveguide », *Phys. Rev. Lett.* **122**, 084801 (2019). DOI 10.1103/PhysRevLett.122.084801. **[C]**
38. R. Erni, M. D. Rossell, C. Kisielowski & U. Dahmen, « Atomic-Resolution Imaging with a Sub-50-pm Electron Probe », *Phys. Rev. Lett.* **102**, 096101 (2009). DOI 10.1103/PhysRevLett.102.096101. **[C]**
39. T. Okugi, exposé LINAC2016 MO3A02 : taille verticale de 41 nm à ATF2 (KEK). **[P]** https://proceedings.jacow.org/linac2016/talks/mo3a02_talk.pdf (exposé de conférence, non évalué par les pairs).

## D. Thermique, énergie, grandes installations

40. I. Mudawar & M. B. Bowers, « Ultra-high critical heat flux (CHF) for subcooled water flow boiling — I: CHF data and parametric effects for small diameter tubes », *Int. J. Heat Mass Transfer* **42**, 1405–1428 (1999). DOI 10.1016/S0017-9310(98)00241-5. **[C]** ; 276 MW/m² : **[E]** (résumé indexé).
41. ITER : aimants 51 GJ (41 GJ pour les bobines toroïdales) ; divertor 10 MW/m² permanent, 20 MW/m² en transitoires lents. **[P]** https://www.iter.org/machine/magnets ; https://www.iter.org/machine/divertor
42. Moteur SSME : flux au col ~163 MW/m² (Kazaroff, NASA TP, 1987) **[P]** https://ntrs.nasa.gov/api/citations/19870007469/downloads/19870007469.pdf ; turbopompe hydrogène haute pression 72 000 hp, 775 lb **[P]** https://ntrs.nasa.gov/api/citations/20090017765/downloads/20090017765.pdf
43. Réacteur HFIR (ORNL) : 85 MW, 1,7 MW/L en moyenne (Chandler et al., PHYSOR 2018). **[P]** https://www.osti.gov/servlets/purl/1465056
44. CMS : solénoïde 4 T, 2,6 GJ (JINST 3 S08004) **[E]** ; LHC : dipôles 8,82 GJ, faisceau nominal 362 MJ **[P]** https://ar5iv.labs.arxiv.org/html/1608.02433
45. NIF : 2,05 MJ → 3,15 MJ (5 déc. 2022) ; 2,2 MJ → 5,2 MJ (12 fév. 2024) ; 2,08 MJ → 8,6 MJ (7 avr. 2025). **[P]** https://lmf.llnl.gov/science/achieving-fusion-ignition ; banc de condensateurs ~400 MJ nominal **[E]**.
46. Z machine (Sandia) : 22 MJ stockés, 26 MA ; rayonnement X 350 TW, 2,7 MJ. **[P]** https://www.sandia.gov/z-machine/about-z/ ; https://www.osti.gov/servlets/purl/1658486
47. Densités d'énergie des batteries : plomb ≈ 30 Wh/kg, packs Li-ion 120–180 Wh/kg (National Academies, 2020) **[P]** https://www.nationalacademies.org/read/25542/chapter/10 ; cellules ≥ 270 Wh/kg : J. T. Frith, M. J. Lacey & U. Ulissi, « A non-academic perspective on the future of lithium-based batteries », *Nat. Commun.* **14**, 420 (2023), DOI 10.1038/s41467-023-35933-2 **[C]** (valeur : **[E]**).
48. Energy Institute, *Statistical Review of World Energy 2024* : 620 EJ d'énergie primaire et 29 925 TWh d'électricité en 2023. **[E]** (résumé https://dieselnet.com/news/2024/06energyreview.php ; site primaire inaccessible). Ember 2025 : 30 856 TWh en 2024 **[P]**.

## E. Rayonnement et radioprotection

49. NIST, *X-Ray Mass Attenuation Coefficients* (plomb, tungstène, eau) et base XCOM (plomb à 30, 50, 100 MeV). **[P]** https://physics.nist.gov/PhysRefData/XrayMassCoef/ElemTab/z82.html ; …/z74.html ; …/ComTab/water.html ; https://physics.nist.gov/PhysRefData/Xcom/html/xcom1.html — valeurs recopiées dans `calculs/c05_refroidissement_rayonnement.py`.
50. Particle Data Group (2024), *Atomic and Nuclear Properties of Materials* : X₀ = 0,5612 cm (Pb), 0,3504 cm (W), 1,757 cm (Fe), 36,08 cm (eau) ; énergies critiques 7,43 MeV (Pb), 7,97 MeV (W). **[P]** https://pdg.lbl.gov/2024/AtomicNuclearProperties/
51. AIEA, LiveChart of Nuclides : énergies de séparation du neutron (seuils (γ,n)) ²⁰⁸Pb 7,368 MeV ; ²⁰⁷Pb 6,738 MeV ; ¹⁸⁴W 7,411 MeV ; ¹⁸³W 6,191 MeV. **[P]** https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides=208pb
52. NCRP Report 151, tableau B.2 (reproduit par Biggs, AAPM 2014) : couche de déci-transmission du plomb 5,7 cm (4–20 MV) ; béton 45 cm (18 MV). **[P]** (source secondaire fidèle) https://www.aapm.org/meetings/2014AM/ReviewCourses/documents/T08BiggsslidesShielding_2014.pdf — extrapolé par nous au-delà de 20 MV.
53. CIPR, Publication 103 : public 1 mSv/an ; travailleurs 20 mSv/an en moyenne sur 5 ans. **[P]** https://icrpaedia.org/Dose_limits
54. CDC, syndrome d'irradiation aiguë : DL50/60 ≈ 2,5–5 Gy. **[P]** https://www.cdc.gov/radiation-emergencies/hcp/clinical-guidance/ars.html

## F. Gravimétrie

55. Micro-g LaCoste FG5-X, brochure : 2 µGal ; 15 µGal/√Hz ; 20–30 °C ; ~500 W ; 150 kg. **[P]** http://microglacoste.com/wp-content/uploads/2018/02/FG5-X-Brochure.pdf
56. Scintrex CG-6 Autograv, brochure : résolution 0,1 µGal ; écart-type < 5 µGal ; plage 8 000 mGal ; −40 à +45 °C ; 5,5 kg ; 5,2 W. **[P]** https://microglacoste.com/wp-content/uploads/2019/01/CG-6-Brochure_R5.pdf
57. GWR Instruments, iGrav : 1 nGal (fréquentiel) ; 0,3 µGal/√Hz ; dérive < 0,5 µGal/mois ; 4–38 °C. **[P]** https://gwrinstruments.com/igrav-gravity-sensors.html
58. Exail, gravimètres quantiques AQG : 500 nm/s²/√τ ; stabilité ≤ 20 nm/s² ; AQG-B 0–40 °C, < 140 kg, 500 W. **[P]** https://www.exail.com/product/quantum-gravimeters
59. V. Ménoret et al., « Gravity measurements below 10⁻⁹ g with a transportable absolute quantum gravimeter », *Sci. Rep.* **8**, 12300 (2018). DOI 10.1038/s41598-018-30608-1. **[C+]**
60. R. P. Middlemiss et al., « Measurement of the Earth tides with a MEMS gravimeter », *Nature* **531**, 614–617 (2016). DOI 10.1038/nature17397. **[C+]** — 40 µGal/√Hz.
61. B. Stray et al., « Quantum sensing for gravity cartography », *Nature* **602**, 590–594 (2022). DOI 10.1038/s41586-021-04315-3. **[C+]** — 20 E.
62. Gradiométrie aéroportée : Fairhead et al., *Exploration 17* (2017). **[P]** https://www.sgl.com/technicalpapers/Fairhead%20et%20al%20Advances%20in%20Airborne%20Gravity%20and%20Magnetics.pdf (pas de fiche constructeur trouvée).
63. C. Jekeli, « Precision Free-Inertial Navigation with Gravity Compensation by an Onboard Gradiometer », *J. Guid. Control Dyn.* **29**, 704–713 (2006). DOI 10.2514/1.15368. **[C]** — traite la compensation *in situ* de la gravité par gradiomètre embarqué pour une centrale inertielle, sans carte (d'après son titre et la relecture de la Red Team n° 2, correction n° 34 ; contenu non relu par nous). Cité dans la fiche F6 uniquement pour dire que cette technique ne fournit pas non plus de position absolue. La navigation par corrélation de carte gravimétrique est mentionnée sans référence : **[N]**.
64. Gradient vertical normal à l'air libre 308,6 µGal/m ; amplitude de la marée terrestre ; vitesses orbitale et galactique de la Terre. **[N]** (valeurs usuelles de manuel).

## G. Horloges

65. Étalon à césium 5071A (fiche Agilent hébergée par la NASA) : ±5×10⁻¹³ (option 001) ; palier ≤ 1×10⁻¹⁴ ; 30 kg ; 133,4 × 425,5 × 523,9 mm ; 50 W ; 0–50 °C garanti. **[P]** https://ilrs.gsfc.nasa.gov/docs/timing/HP5071A.pdf ; introduction en 1992 (fiche Microchip 5071B) **[P]**.
66. Microchip CSAC SA.45s (DS00002982E) : < 17 cm³ ; < 35 g ; < 120 mW ; 3×10⁻¹⁰ à 1 s ; −10 à +70 °C. **[P]** (copie distributeur) https://datasheet.sic-components.com/00002982.pdf ; disponibilité générale janvier 2011 **[E]**.
67. T. P. Heavner et al., « First accuracy evaluation of NIST-F2 », *Metrologia* **51**, 174–182 (2014). DOI 10.1088/0026-1394/51/3/174. **[C+]** — 1,1×10⁻¹⁶ (incertitude de type B).
68. S. M. Brewer et al., « ²⁷Al⁺ Quantum-Logic Clock with a Systematic Uncertainty below 10⁻¹⁸ », *Phys. Rev. Lett.* **123**, 033201 (2019). DOI 10.1103/PhysRevLett.123.033201. **[C+]** — 9,4×10⁻¹⁹.
69. NIST, « A brief history of atomic clocks at NIST » : NIST-7 (1993), NIST-F1 (1999). **[P]** https://www.nist.gov/pml/time-and-frequency-division/time-services/brief-history-atomic-clocks-nist
70. GPS Block II/IIA : 2 horloges au rubidium + 2 au césium (Van Melle, PTTI 1995) **[P]** https://ntrs.nasa.gov/api/citations/19960042628/downloads/19960042628.pdf ; Galileo : 2 masers à hydrogène passifs + 2 rubidium **[P]** https://www.esa.int/Applications/Satellite_navigation/Hyper-accurate_clocks_the_beating_heart_of_Galileo
71. BIPM, définition de la seconde : Δν_Cs = 9 192 631 770 Hz. **[P]** https://www.bipm.org/en/si-base-units/second

## H. Calculateurs redondants et vote

72. J. von Neumann, « Probabilistic Logics and the Synthesis of Reliable Organisms From Unreliable Components », in *Automata Studies*, Princeton Univ. Press (1956), p. 43–98. DOI 10.1515/9781400882618-003. **[C]**
73. R. E. Lyons & W. Vanderkulk, « The Use of Triple-Modular Redundancy to Improve Computer Reliability », *IBM J. Res. Dev.* **6**, 200–209 (1962). DOI 10.1147/rd.62.0200. **[C]**
74. L. Lamport, R. Shostak & M. Pease, « The Byzantine Generals Problem », *ACM Trans. Program. Lang. Syst.* **4**, 382–401 (1982). DOI 10.1145/357172.357176. **[C]**
75. Y. C. Yeh, « Triple-triple redundant 777 primary flight computer », *1996 IEEE Aerospace Applications Conference*, vol. 1, 293–307. DOI 10.1109/AERO.1996.495891. **[C]**
76. T. K. Ho, J. J. Hull & S. N. Srihari, « Decision combination in multiple classifier systems », *IEEE Trans. Pattern Anal. Mach. Intell.* **16**, 66–75 (1994). DOI 10.1109/34.273716. **[C+]** — emploie le décompte de Borda pour fusionner des classifieurs.
77. J.-C. de Borda, « Mémoire sur les élections au scrutin », *Histoire de l'Académie Royale des Sciences*, année 1781 (Paris, 1784), p. 657–665. **[E]** (sources secondaires concordantes ; traduction : https://gtfp.cs.rhul.ac.uk/pulskamp/Borda/voting.pdf).
78. « Borda error correcting protocol » : **aucune occurrence** trouvée dans Crossref, OpenAlex ni la recherche web en dehors des archives des messages de John Titor (constat du 10 novembre 2026).
79. ISO 13850 (arrêt d'urgence) et IEC 60204-1 (catégories d'arrêt). **[N]**
80. Travaux de J.-C. de Borda en métrologie (cercle répétiteur, pendule battant la seconde). **[N]**

## I. Valeurs non confirmées utilisées comme hypothèses

- Charge utile d'un pick-up Chevrolet K-series de 1987 : aucune source constructeur exploitable ; 700–1 500 kg retenu comme **[HYP]**.
- Résistances des matériaux (acier 2 GPa, fibre de carbone 3,5 GPa, limite idéale 130 GPa, diamant ~100 GPa, granite ~200 MPa, béton ~40 MPa), propriétés thermiques du tungstène et de l'eau : valeurs usuelles **[N]**.
- Section efficace neutrino-nucléon ~10⁻⁴¹ cm² à ~10 MeV : ordre de grandeur **[N]**.
- Puissance d'un cryoréfrigérateur (~7 kW), des calculateurs (30 W), pertes de charge (10 bar) : **[HYP]** d'ingénieur.

## J. Sources du programme

- `00_DOSSIER_DE_BASE.md` (transcriptions DOC-005 à DOC-011, affirmations chiffrées, ordres de grandeur préliminaires).
- `01_archive/sources_web/corpus_technique_extrait.txt` (propos attribués à « John Titor », compilation secondaire non vérifiée contre les archives primaires).
- `01_archive/ameliores/MT7016…`, `MT7017…`, `MT7018…`, `MT7013…`, `MT7012…` (images consultées en lecture seule).
