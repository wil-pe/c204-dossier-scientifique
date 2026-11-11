#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe B — vérification en ligne des références bibliographiques (Crossref + arXiv).

Pour chaque référence candidate, on interroge l'API publique Crossref
(query.bibliographic) et on enregistre les 3 premiers résultats. La comparaison
finale (titre / auteurs / année / revue / volume / page) est faite à la main
dans REFERENCES.md : ce script ne fait que collecter.

Aucune donnée personnelle n'est transmise (User-Agent générique, pas de mailto).
Les réponses sont des données non fiables : elles sont seulement lues comme texte JSON.

Usage : python 00_verif_references_crossref.py
Sortie : sorties/refs_crossref_resume.txt (+ JSON bruts dans sorties/refs_crossref/)
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER = os.path.join(ICI, "sorties", "refs_crossref")
os.makedirs(DOSSIER, exist_ok=True)
RESUME = os.path.join(ICI, "sorties", "refs_crossref_resume.txt")

UA = "bibliography-check-script/1.0"

# (clé, requête bibliographique)
REFS = [
    # --- Kerr, Kerr-Newman, structure interne
    ("Kerr1963", "Kerr Gravitational field of a spinning mass as an example of algebraically special metrics Physical Review Letters 1963"),
    ("Newman1965", "Newman Couch Chinnapared Exton Prakash Torrence Metric of a rotating charged mass Journal of Mathematical Physics 1965"),
    ("BoyerLindquist1967", "Boyer Lindquist Maximal analytic extension of the Kerr metric Journal of Mathematical Physics 1967"),
    ("Carter1968", "Carter Global structure of the Kerr family of gravitational fields Physical Review 1968"),
    ("Penrose1969", "Penrose Gravitational collapse: the role of general relativity"),
    ("PenroseFloyd1971", "Penrose Floyd Extraction of rotational energy from a black hole Nature Physical Science 1971"),
    ("ChristodoulouRuffini1971", "Christodoulou Ruffini Reversible transformations of a charged black hole Physical Review D 1971"),
    ("SimpsonPenrose1973", "Simpson Penrose Internal instability in a Reissner-Nordstrom black hole International Journal of Theoretical Physics 1973"),
    ("PoissonIsrael1990", "Poisson Israel Internal structure of black holes Physical Review D 1990"),
    ("Ori1991", "Ori Inner structure of a charged black hole: an exact mass-inflation solution Physical Review Letters 1991"),
    ("Ori1992", "Ori Structure of the singularity inside a realistic rotating black hole Physical Review Letters 1992"),
    ("DafermosLuk", "Dafermos Luk The interior of dynamical vacuum black holes I: The C0-stability of the Kerr Cauchy horizon"),
    ("BirrellDavies1978", "Birrell Davies On falling through a black hole into another universe Nature 1978"),
    ("ZilbermanLeviOri2020", "Zilberman Levi Ori Quantum fluxes at the inner horizon of a spherical charged black hole Physical Review Letters 2020"),
    ("Zilberman2022", "Zilberman Casals Ori Ottewill Quantum fluxes at the inner horizon of a spinning black hole Physical Review Letters 2022"),
    ("HawkingEllis1973", "Hawking Ellis The Large Scale Structure of Space-Time Cambridge University Press 1973"),
    ("MarolfOri2012", "Marolf Ori Outgoing gravitational shock-wave at the inner horizon: the late-time limit of black hole interiors Physical Review D 2012"),
    ("Dafermos2005", "Dafermos The interior of charged black holes and the problem of uniqueness in general relativity Communications on Pure and Applied Mathematics 2005"),
    # --- van Stockum, Tipler
    ("vanStockum1937", "van Stockum The gravitational field of a distribution of particles rotating about an axis of symmetry Proceedings of the Royal Society of Edinburgh 1937"),
    ("Tipler1974", "Tipler Rotating cylinders and the possibility of global causality violation Physical Review D 1974"),
    ("Tipler1976", "Tipler Causality violation in asymptotically flat space-times Physical Review Letters 1976"),
    ("Tipler1977", "Tipler Singularities and causality violation Annals of Physics 1977"),
    ("Bonnor1980", "Bonnor The rigidly rotating relativistic dust cylinder Journal of Physics A 1980"),
    ("Lanczos1924", "Lanczos Uber eine stationare Kosmologie im Sinne der Einsteinschen Gravitationstheorie Zeitschrift fur Physik 1924"),
    # --- deux trous noirs
    ("Majumdar1947", "Majumdar A class of exact solutions of Einstein's field equations Physical Review 1947"),
    ("Papapetrou1947", "Papapetrou A static solution of the equations of the gravitational field for an arbitrary charge-distribution Proceedings of the Royal Irish Academy 1947"),
    ("HartleHawking1972", "Hartle Hawking Solutions of the Einstein-Maxwell equations with many black holes Communications in Mathematical Physics 1972"),
    ("KramerNeugebauer1980", "Kramer Neugebauer The superposition of two Kerr solutions Physics Letters A 1980"),
    ("NeugebauerHennig2009", "Neugebauer Hennig Non-existence of stationary two-black-hole configurations General Relativity and Gravitation 2009"),
    ("HennigNeugebauer2011", "Hennig Neugebauer Non-existence of stationary two-black-hole configurations: the degenerate case General Relativity and Gravitation 2011"),
    ("Peters1964", "Peters Gravitational radiation and the motion of two point masses Physical Review 1964"),
    ("BachWeyl1922", "Bach Weyl Neue Losungen der Einsteinschen Gravitationsgleichungen Mathematische Zeitschrift 1922"),
    ("DietzHoenselaers1985", "Dietz Hoenselaers Two mass solutions of Einstein's vacuum equations: the double Kerr solution Annals of Physics 1985"),
    ("Wald1972", "Wald Gravitational spin interaction Physical Review D 1972"),
    ("MankoRuiz2019", "Manko Ruiz Metric for two arbitrary Kerr sources Physics Letters B 2019"),
    # --- Hawking, micro-trous noirs
    ("Hawking1971", "Hawking Gravitationally collapsed objects of very low mass Monthly Notices of the Royal Astronomical Society 1971"),
    ("Hawking1974", "Hawking Black hole explosions? Nature 1974"),
    ("Hawking1975", "Hawking Particle creation by black holes Communications in Mathematical Physics 1975"),
    ("Page1976a", "Page Particle emission rates from a black hole: Massless particles from an uncharged, nonrotating hole Physical Review D 1976"),
    ("Page1976b", "Page Particle emission rates from a black hole. II. Massless particles from a rotating hole Physical Review D 1976"),
    ("Page1977", "Page Particle emission rates from a black hole. III. Charged leptons from a nonrotating hole Physical Review D 1977"),
    ("MacGibbonWebber1990", "MacGibbon Webber Quark- and gluon-jet emission from primordial black holes: The instantaneous spectra Physical Review D 1990"),
    ("MacGibbon1991", "MacGibbon Quark- and gluon-jet emission from primordial black holes. II. The emission over the black-hole lifetime Physical Review D 1991"),
    ("MacGibbonCarrPage2008", "MacGibbon Carr Page Do evaporating black holes form photospheres? Physical Review D 2008"),
    ("Carr2010", "Carr Kohri Sendouda Yokoyama New cosmological constraints on primordial black holes Physical Review D 2010"),
    ("Gibbons1975", "Gibbons Vacuum polarization and the spontaneous loss of charge by black holes Communications in Mathematical Physics 1975"),
    ("Zaumen1974", "Zaumen Upper bound on the electric charge of a black hole Nature 1974"),
    ("Carter1974", "Carter Charge and particle conservation in black-hole decay Physical Review Letters 1974"),
    ("Schwinger1951", "Schwinger On gauge invariance and vacuum polarization Physical Review 1951"),
    ("TeukolskyPress1974", "Teukolsky Press Perturbations of a rotating black hole. III. Interaction of the hole with gravitational and electromagnetic radiation Astrophysical Journal 1974"),
    ("PressTeukolsky1972", "Press Teukolsky Floating orbits, superradiant scattering and the black-hole bomb Nature 1972"),
    ("BritoCardosoPani2015", "Brito Cardoso Pani Superradiance Lecture Notes in Physics"),
    ("GiddingsThomas2002", "Giddings Thomas High energy colliders as black hole factories: the end of short distance physics Physical Review D 2002"),
    ("DimopoulosLandsberg2001", "Dimopoulos Landsberg Black holes at the Large Hadron Collider Physical Review Letters 2001"),
    ("CMS2011", "CMS Collaboration Search for microscopic black hole signatures at the Large Hadron Collider Physics Letters B 2011"),
    ("GiddingsMangano2008", "Giddings Mangano Astrophysical implications of hypothetical stable TeV-scale black holes Physical Review D 2008"),
    ("ADD1998", "Arkani-Hamed Dimopoulos Dvali The hierarchy problem and new dimensions at a millimeter Physics Letters B 1998"),
    ("AharonovCasherNussinov1987", "Aharonov Casher Nussinov The unitarity puzzle and Planck mass stable particles Physics Letters B 1987"),
    ("MacGibbon1987", "MacGibbon Can Planck-mass relics of evaporating black holes close the Universe? Nature 1987"),
    ("AdlerChenSantiago2001", "Adler Chen Santiago The generalized uncertainty principle and black hole remnants General Relativity and Gravitation 2001"),
    ("ChenOngYeom2015", "Chen Ong Yeom Black hole remnants and the information loss paradox Physics Reports 2015"),
    ("Maldacena2021", "Maldacena Comments on magnetic black holes Journal of High Energy Physics 2021"),
    ("Wald1974", "Wald Black hole in a uniform magnetic field Physical Review D 1974"),
    ("LeahyUnruh1979", "Leahy Unruh Angular dependence of neutrino emission from rotating black holes Physical Review D 1979"),
    ("ChambersHiscockTaylor1997", "Chambers Hiscock Taylor Spinning down a black hole with scalar fields Physical Review Letters 1997"),
    ("Bekenstein1973", "Bekenstein Black holes and entropy Physical Review D 1973"),
    # --- dilatation du temps, mesures
    ("HafeleKeating1972a", "Hafele Keating Around-the-world atomic clocks: predicted relativistic time gains Science 1972"),
    ("HafeleKeating1972b", "Hafele Keating Around-the-world atomic clocks: observed relativistic time gains Science 1972"),
    ("PoundRebka1960", "Pound Rebka Apparent weight of photons Physical Review Letters 1960"),
    ("Chou2010", "Chou Hume Rosenband Wineland Optical clocks and relativity Science 2010"),
    ("Bothwell2022", "Bothwell Resolving the gravitational redshift across a millimetre-scale atomic sample Nature 2022"),
    ("Buchdahl1959", "Buchdahl General relativistic fluid spheres Physical Review 1959"),
    ("Andreasson2008", "Andreasson Sharp bounds on 2m/r of general spherically symmetric static objects Journal of Differential Equations 2008"),
    ("Everitt2011", "Everitt Gravity Probe B: final results of a space experiment to test general relativity Physical Review Letters 2011"),
    ("Westphal2021", "Westphal Hepach Pfaff Aspelmeyer Measurement of gravitational coupling between millimetre-sized masses Nature 2021"),
    ("Bailey1977", "Bailey Measurements of relativistic time dilatation for positive and negative muons in a circular orbit Nature 1977"),
    ("CiufoliniPavlis2004", "Ciufolini Pavlis A confirmation of the general relativistic prediction of the Lense-Thirring effect Nature 2004"),
    # --- autres voies vers les CTC
    ("Godel1949", "Godel An example of a new type of cosmological solutions of Einstein's field equations of gravitation Reviews of Modern Physics 1949"),
    ("Gott1991", "Gott Closed timelike curves produced by pairs of moving cosmic strings: exact solutions Physical Review Letters 1991"),
    ("DeserJackiwtHooft1992", "Deser Jackiw 't Hooft Physical cosmic strings do not generate closed timelike curves Physical Review Letters 1992"),
    ("CarrollFarhiGuth1992", "Carroll Farhi Guth An obstacle to building a time machine Physical Review Letters 1992"),
    ("MorrisThorne1988", "Morris Thorne Wormholes in spacetime and their use for interstellar travel: a tool for teaching general relativity American Journal of Physics 1988"),
    ("MTY1988", "Morris Thorne Yurtsever Wormholes, time machines, and the weak energy condition Physical Review Letters 1988"),
    ("Alcubierre1994", "Alcubierre The warp drive: hyper-fast travel within general relativity Classical and Quantum Gravity 1994"),
    ("Krasnikov1998", "Krasnikov Hyperfast travel in general relativity Physical Review D 1998"),
    ("Everett1996", "Everett Warp drive and causality Physical Review D 1996"),
    ("EverettRoman1997", "Everett Roman Superluminal subway: The Krasnikov tube Physical Review D 1997"),
    ("PfenningFord1997", "Pfenning Ford The unphysical nature of warp drive Classical and Quantum Gravity 1997"),
    ("FordRoman1995", "Ford Roman Averaged energy conditions and quantum inequalities Physical Review D 1995"),
    ("FordRoman1996", "Ford Roman Quantum field theory constrains traversable wormhole geometries Physical Review D 1996"),
    ("Ford1978", "Ford Quantum coherence effects and the second law of thermodynamics Proceedings of the Royal Society A 1978"),
    ("Mallett2000", "Mallett Weak gravitational field of the electromagnetic radiation in a ring laser Physics Letters A 2000"),
    ("Mallett2003", "Mallett The gravitational field of a circulating light beam Foundations of Physics 2003"),
    ("OlumEverett2005", "Olum Everett Can a circulating light beam produce a time machine? Foundations of Physics Letters 2005"),
    ("Casimir1948", "Casimir On the attraction between two perfectly conducting plates 1948"),
    ("Lamoreaux1997", "Lamoreaux Demonstration of the Casimir force in the 0.6 to 6 micrometer range Physical Review Letters 1997"),
    ("Ori2005", "Ori A class of time-machine solutions with a compact vacuum core Physical Review Letters 2005"),
    ("FriedmanSchleichWitt1993", "Friedman Schleich Witt Topological censorship Physical Review Letters 1993"),
    ("GaoJafferisWall2017", "Gao Jafferis Wall Traversable wormholes via a double trace deformation Journal of High Energy Physics 2017"),
    ("MaldacenaMilekhinPopov", "Maldacena Milekhin Popov Traversable wormholes in four dimensions"),
    ("MaldacenaMilekhin2021", "Maldacena Milekhin Humanly traversable wormholes Physical Review D 2021"),
    ("Faulkner2016", "Faulkner Leigh Parrikar Wang Modular Hamiltonians for deformed half-spaces and the averaged null energy condition Journal of High Energy Physics 2016"),
    ("HartmanKunduTajdini2017", "Hartman Kundu Tajdini Averaged null energy condition from causality Journal of High Energy Physics 2017"),
    ("GrahamOlum2007", "Graham Olum Achronal averaged null energy condition Physical Review D 2007"),
    ("TippettTsang2017", "Tippett Tsang Traversable acausal retrograde domains in spacetime Classical and Quantum Gravity 2017"),
    ("Visser1995", "Visser Lorentzian Wormholes: From Einstein to Hawking 1995"),
    ("Hiscock1985", "Hiscock Exact gravitational field of a string Physical Review D 1985"),
    ("Vilenkin1981", "Vilenkin Gravitational field of vacuum domain walls and strings Physical Review D 1981"),
    # --- causalité
    ("Hawking1992", "Hawking Chronology protection conjecture Physical Review D 1992"),
    ("KRW1997", "Kay Radzikowski Wald Quantum field theory on spacetimes with a compactly generated Cauchy horizon Communications in Mathematical Physics 1997"),
    ("KimThorne1991", "Kim Thorne Do vacuum fluctuations prevent the creation of closed timelike curves? Physical Review D 1991"),
    ("Visser2003", "Visser The quantum physics of chronology protection"),
    ("Friedman1990", "Friedman Morris Novikov Echeverria Klinkhammer Thorne Yurtsever Cauchy problem in spacetimes with closed timelike curves Physical Review D 1990"),
    ("EKT1991", "Echeverria Klinkhammer Thorne Billiard balls in wormhole spacetimes with closed timelike curves: Classical theory Physical Review D 1991"),
    ("Deutsch1991", "Deutsch Quantum mechanics near closed timelike lines Physical Review D 1991"),
    ("Lloyd2011PRL", "Lloyd Maccone Garcia-Patron Giovannetti Shikano Pirandola Closed timelike curves via postselection: theory and experimental test of consistency Physical Review Letters 2011"),
    ("Lloyd2011PRD", "Lloyd Maccone Garcia-Patron Giovannetti Shikano Quantum mechanics of time travel through post-selected teleportation Physical Review D 2011"),
    ("Politzer1992", "Politzer Simple quantum systems in spacetimes with closed timelike curves Physical Review D 1992"),
    ("Hartle1994", "Hartle Unitarity and causality in generalized quantum mechanics for nonchronal spacetimes Physical Review D 1994"),
    ("AEverett2004", "Everett Time travel paradoxes, path integrals, and the many worlds interpretation of quantum mechanics Physical Review D 2004"),
    ("HEverett1957", "Everett Relative state formulation of quantum mechanics Reviews of Modern Physics 1957"),
    ("Polchinski1991", "Polchinski Weinberg's nonlinear quantum mechanics and the Einstein-Podolsky-Rosen paradox Physical Review Letters 1991"),
    ("Bollinger1989", "Bollinger Heinzen Itano Gilbert Wineland Test of the linearity of quantum mechanics by rf spectroscopy of the 9Be+ ground state Physical Review Letters 1989"),
    ("Ringbauer2014", "Ringbauer Broome Myers White Ralph Experimental simulation of closed timelike curves Nature Communications 2014"),
    ("AaronsonWatrous2009", "Aaronson Watrous Closed timelike curves make quantum and classical computing equivalent Proceedings of the Royal Society A 2009"),
    ("Bennett2009", "Bennett Leung Smith Smolin Can closed timelike curves or nonlinear quantum mechanics improve quantum state discrimination or help solve hard problems? Physical Review Letters 2009"),
    ("DeutschLockwood1994", "Deutsch Lockwood The quantum physics of time travel Scientific American 1994"),
    ("Geroch1967", "Geroch Topology in general relativity Journal of Mathematical Physics 1967"),
    ("Hawking1969", "Hawking The existence of cosmic time functions Proceedings of the Royal Society A 1969"),
    ("Krasnikov2002", "Krasnikov No time machines in classical general relativity Classical and Quantum Gravity 2002"),
    ("EarmanSmeenkWuthrich2009", "Earman Smeenk Wuthrich Do the laws of physics forbid the operation of time machines? Synthese 2009"),
    ("Weinberg1989", "Weinberg Testing quantum mechanics Annals of Physics 1989"),
    ("Gisin1990", "Gisin Weinberg's non-linear quantum mechanics and supraluminal communications Physics Letters A 1990"),
    ("Thorne1993", "Thorne Closed timelike curves General Relativity and Gravitation 1992 proceedings"),
    # --- champs électromagnétiques et gravité
    ("Melvin1964", "Melvin Pure magnetic and electric geons Physics Letters 1964"),
    ("Reissner1916", "Reissner Uber die Eigengravitation des elektrischen Feldes nach der Einsteinschen Theorie Annalen der Physik 1916"),
    ("Kreuzer1968", "Kreuzer Experimental measurement of the equivalence of active and passive gravitational mass Physical Review 1968"),
    ("Bonnor1954", "Bonnor Static magnetic fields in general relativity Proceedings of the Physical Society A 1954"),
    ("TolmanEhrenfestPodolsky1931", "Tolman Ehrenfest Podolsky On the gravitational field produced by light Physical Review 1931"),
    ("Fuzfa2016", "Fuzfa How current loops and solenoids curve spacetime Physical Review D 2016"),
    ("Nakamura2018", "Nakamura Ikeda Sawabe Matsuda Takeyama Record indoor magnetic field of 1200 T generated by electromagnetic flux-compression Review of Scientific Instruments 2018"),
    ("Hahn2019", "Hahn 45.5-tesla direct-current magnetic field generated with a high-temperature superconducting magnet Nature 2019"),
    ("BartlettVanBuren1986", "Bartlett Van Buren Equivalence of active and passive gravitational mass using the moon Physical Review Letters 1986"),
    # --- second lot (ajouté après relecture du premier)
    ("CMS2011b", "Search for microscopic black hole signatures at the Large Hadron Collider Physics Letters B 697 434"),
    ("CMS2018", "CMS Search for black holes and sphalerons in high-multiplicity final states in proton-proton collisions at 13 TeV Journal of High Energy Physics 2018"),
    ("Krasnikov1996", "Krasnikov Quantum stability of the time machine Physical Review D 1996"),
    ("TobarCosta2020", "Tobar Costa Reversible dynamics with closed time-like curves and freedom of choice Classical and Quantum Gravity 2020"),
    ("Lee2020", "Lee Adelberger Cook Fleischer Heckel New test of the gravitational 1/r2 law at separations down to 52 um Physical Review Letters 2020"),
    ("Unruh1976", "Unruh Absorption cross section of small black holes Physical Review D 1976"),
    ("DeWittGraham1973", "DeWitt Graham The Many-Worlds Interpretation of Quantum Mechanics Princeton University Press 1973"),
    ("tHooft1992", "'t Hooft Causality in (2+1)-dimensional gravity Classical and Quantum Gravity 1992"),
    ("Cutler1992", "Cutler Global structure of Gott's two-string spacetime Physical Review D 1992"),
    ("BardeenPressTeukolsky1972", "Bardeen Press Teukolsky Rotating black holes: locally nonrotating frames, energy extraction, and scalar synchrotron radiation Astrophysical Journal 1972"),
    ("Wald1984", "Wald General Relativity University of Chicago Press 1984"),
    ("Chandrasekhar1983", "Chandrasekhar The Mathematical Theory of Black Holes Oxford University Press 1983"),
    ("MTW1973", "Misner Thorne Wheeler Gravitation 1973"),
    ("Krasnikov2018", "Krasnikov Back-in-Time and Faster-than-Light Travel in General Relativity Springer 2018"),
    ("FriedmanHiguchi2006", "Friedman Higuchi Topological censorship and chronology protection Annalen der Physik 2006"),
    ("FewsterRoman2005", "Fewster Roman On wormholes with arbitrarily small quantities of exotic matter Physical Review D 2005"),
    ("KontouSanders2020", "Kontou Sanders Energy conditions in general relativity and quantum field theory Classical and Quantum Gravity 2020"),
    ("BobrickMartire2021", "Bobrick Martire Introducing physical warp drives Classical and Quantum Gravity 2021"),
    ("Lentz2021", "Lentz Breaking the warp barrier: hyper-fast solitons in Einstein-Maxwell-plasma theory Classical and Quantum Gravity 2021"),
    ("SantiagoSchusterVisser2022", "Santiago Schuster Visser Generic warp drives violate the null energy condition Physical Review D 2022"),
    ("MohideenRoy1998", "Mohideen Roy Precision measurement of the Casimir force from 0.1 to 0.9 um Physical Review Letters 1998"),
    ("BrownMaclay1969", "Brown Maclay Vacuum stress between conducting plates: an image solution Physical Review 1969"),
    ("EpsteinGlaserJaffe1965", "Epstein Glaser Jaffe Nonpositivity of the energy density in quantized field theories Il Nuovo Cimento 1965"),
    ("HochbergVisser1998", "Hochberg Visser Null energy condition in dynamic wormholes Physical Review Letters 1998"),
    ("VisserKarDadhich2003", "Visser Kar Dadhich Traversable wormholes with arbitrarily small energy condition violations Physical Review Letters 2003"),
    ("FrolovNovikov1990", "Frolov Novikov Physical effects in wormholes and time machines Physical Review D 1990"),
    ("Allen2014", "Allen Treating time travel quantum mechanically Physical Review A 2014"),
    ("Wallace2012", "Wallace The Emergent Multiverse: Quantum Theory according to the Everett Interpretation Oxford University Press 2012"),
    ("Zurek2003", "Zurek Decoherence, einselection, and the quantum origins of the classical Reviews of Modern Physics 2003"),
    ("Niebauer1995", "Niebauer Sasagawa Faller Hilt Klopping A new generation of absolute gravimeters Metrologia 1995"),
    ("Menoret2018", "Menoret Vermeulen Le Moigne Bonvalot Bouyer Landragin Desruelle Gravity measurements below 10-9 g with a transportable absolute quantum gravimeter Scientific Reports 2018"),
    ("Aeppli2024", "Aeppli Kim Warfield Safronova Ye Clock with 8e-19 systematic uncertainty Physical Review Letters 2024"),
    ("McGrew2018", "McGrew Atomic clock performance enabling geodesy below the centimetre level Nature 2018"),
    ("HiscockWeems1990", "Hiscock Weems Evolution of charged evaporating black holes Physical Review D 1990"),
    ("DamourRuffini1975", "Damour Ruffini Quantum electrodynamical effects in Kerr-Newmann geometries Physical Review Letters 1975"),
    ("Unruh1974", "Unruh Second quantization in the Kerr metric Physical Review D 1974"),
    ("BekensteinSchiffer1998", "Bekenstein Schiffer The many faces of superradiance Physical Review D 1998"),
    ("Israel1967", "Israel Event horizons in static vacuum space-times Physical Review 1967"),
    ("Carter1971", "Carter Axisymmetric black hole has only two degrees of freedom Physical Review Letters 1971"),
    ("Robinson1975", "Robinson Uniqueness of the Kerr black hole Physical Review Letters 1975"),
    ("Penrose1965", "Penrose Gravitational collapse and space-time singularities Physical Review Letters 1965"),
    ("Geroch1970", "Geroch Domain of dependence Journal of Mathematical Physics 1970"),
    ("BernalSanchez2003", "Bernal Sanchez On smooth Cauchy hypersurfaces and Geroch's splitting theorem Communications in Mathematical Physics 2003"),
    ("Minguzzi2019", "Minguzzi Lorentzian causality theory Living Reviews in Relativity 2019"),
    ("Casimir1948b", "Casimir On the attraction between two perfectly conducting plates Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen 51 793"),
    ("Thorne1994", "Thorne Black Holes and Time Warps: Einstein's Outrageous Legacy 1994"),
    ("LevinOri1996", "Levin Ori Inner structure of an evaporating charged black hole Physical Review D 1996"),
    ("Hiscock1977", "Hiscock Stress-energy tensor near a charged, rotating, evaporating black hole Physical Review D 1977"),
    ("HollandsWaldZahn2020", "Hollands Wald Zahn Quantum instability of the Cauchy horizon in Reissner-Nordstrom-deSitter spacetime Classical and Quantum Gravity 2020"),
    ("Vessot1980", "Vessot Levine Test of relativistic gravitation with a space-borne hydrogen maser Physical Review Letters 1980"),
    ("Lense1918", "Lense Thirring Uber den Einfluss der Eigenrotation der Zentralkorper auf die Bewegung der Planeten und Monde nach der Einsteinschen Gravitationstheorie Physikalische Zeitschrift 1918"),
    ("Emparan2000", "Emparan Horowitz Myers Black holes radiate mainly on the brane Physical Review Letters 2000"),
    ("Dyson1979", "Carter Thorne time machine cosmic censorship chronology"),
    ("FermiPizzocchero2018", "Fermi Pizzocchero A time machine for free fall into the past Classical and Quantum Gravity 2018"),
    ("OriSoen1994", "Ori Soen Causality violation and the weak energy condition Physical Review D 1994"),
    ("Ori2007", "Ori Formation of closed timelike curves in a composite vacuum/dust asymptotically flat spacetime Physical Review D 2007"),
    ("Ori1993", "Ori Must time-machine construction violate the weak energy condition? Physical Review Letters 1993"),
    ("Hawking1976b", "Hawking Black holes and thermodynamics Physical Review D 1976"),
    ("Thorne1974", "Thorne Disk-accretion onto a black hole. II. Evolution of the hole Astrophysical Journal 1974"),
    # --- troisième lot
    ("Ernst1976", "Ernst Black holes in a magnetic universe Journal of Mathematical Physics 1976"),
    ("KinnersleyWalker1970", "Kinnersley Walker Uniformly accelerating charged mass in general relativity Physical Review D 1970"),
    ("Planck2013XXV", "Planck Collaboration Planck 2013 results. XXV. Searches for cosmic strings and other topological defects Astronomy and Astrophysics 2014"),
    ("CMS2018b", "Search for black holes and sphalerons in high-multiplicity final states in proton-proton collisions at sqrt(s) = 13 TeV JHEP 2018"),
    ("Misner1967", "Misner Taub-NUT space as a counterexample to almost anything"),
    ("Christodoulou1970", "Christodoulou Reversible and irreversible transformations in black-hole physics Physical Review Letters 1970"),
    ("PoissonIsrael1989", "Poisson Israel Inner-horizon instability and mass inflation in black holes Physical Review Letters 1989"),
    ("CarrollFarhiGuthOlum1994", "Carroll Farhi Guth Olum Energy-momentum restrictions on the creation of Gott time machines Physical Review D 1994"),
    ("Ori1999", "Ori Oscillatory null singularity inside realistic spinning black holes Physical Review Letters 1999"),
    ("Visser1993", "Visser From wormhole to time machine: remarks on Hawking's chronology protection conjecture Physical Review D 1993"),
    ("Schwarzschild1916", "Schwarzschild Uber das Gravitationsfeld eines Massenpunktes nach der Einsteinschen Theorie 1916"),
    ("NANOGrav2023", "NANOGrav 15 yr data set: search for signals from new physics Astrophysical Journal Letters 2023"),
    ("Lewis1932", "Lewis Some special solutions of the equations of axially symmetric gravitational fields Proceedings of the Royal Society A 1932"),
    ("Thorne1972hoop", "Thorne Nonspherical gravitational collapse: a short review Magic Without Magic 1972"),
    ("Lindblom1984", "Lindblom Limits on the gravitational redshift from neutron stars Astrophysical Journal 1984"),
    ("Israel1966", "Israel Singular hypersurfaces and thin shells in general relativity Il Nuovo Cimento B 1966"),
    # --- quatrième lot
    ("Tolman1930", "Tolman On the weight of heat and thermal equilibrium in general relativity Physical Review 1930"),
    ("TolmanEhrenfest1930", "Tolman Ehrenfest Temperature equilibrium in a static gravitational field Physical Review 1930"),
    ("Nordstrom1918", "Nordstrom On the energy of the gravitation field in Einstein's theory 1918"),
    ("Starobinsky1973", "Starobinskii Amplification of waves during reflection from a rotating black hole 1973"),
    ("Penrose1968", "Penrose Structure of space-time Battelle Rencontres 1968"),
    ("Hiscock1981", "Hiscock Evolution of the interior of a charged black hole Physics Letters A 1981"),
    ("Poisson2004", "Poisson A Relativist's Toolkit: The Mathematics of Black-Hole Mechanics Cambridge University Press 2004"),
    ("ONeill1995", "O'Neill The Geometry of Kerr Black Holes 1995"),
    ("Visser2007Kerr", "Visser The Kerr spacetime: a brief introduction 2007"),
]


def interroger(cle, requete):
    params = {
        "query.bibliographic": requete,
        "rows": "3",
        "select": "DOI,title,author,issued,container-title,volume,page,type",
    }
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for essai in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as rep:
                brut = rep.read().decode("utf-8", errors="replace")
            with open(os.path.join(DOSSIER, cle + ".json"), "w", encoding="utf-8") as f:
                f.write(brut)
            return json.loads(brut)
        except Exception as exc:  # réseau : on réessaie
            derniere = exc
            time.sleep(2 + 2 * essai)
    return {"erreur": str(derniere)}


def formater(item):
    titre = (item.get("title") or ["?"])[0]
    auteurs = ", ".join(a.get("family", "?") for a in item.get("author", [])[:6])
    annee = (item.get("issued", {}).get("date-parts") or [[None]])[0][0]
    revue = (item.get("container-title") or [""])[0]
    return f"{auteurs} ({annee}). {titre}. {revue} {item.get('volume', '')}, {item.get('page', '')}. DOI:{item.get('DOI', '')} [{item.get('type', '')}]"


def main():
    seulement = set(sys.argv[1:])
    lignes = []
    for cle, requete in REFS:
        if seulement and cle not in seulement:
            continue
        data = interroger(cle, requete)
        lignes.append(f"### {cle}\n  requête : {requete}")
        if "erreur" in data:
            lignes.append(f"  ERREUR : {data['erreur']}")
        else:
            for it in data.get("message", {}).get("items", []):
                lignes.append("  - " + formater(it))
        lignes.append("")
        time.sleep(0.25)
    texte = "\n".join(lignes)
    mode = "a" if seulement else "w"
    with open(RESUME, mode, encoding="utf-8") as f:
        f.write(texte + "\n")
    print(texte)


if __name__ == "__main__":
    main()
