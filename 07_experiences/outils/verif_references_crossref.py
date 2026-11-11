#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe F — vérification bibliographique en ligne (API publique Crossref).

Pour chaque référence candidate : soit un DOI connu (recherche directe), soit une
requête bibliographique (auteur + titre). On enregistre ce que renvoie Crossref
(auteur, année, revue, volume, page, titre, DOI) pour comparaison manuelle.

Aucune donnée personnelle n'est transmise (User-Agent générique, pas d'adresse).
Les réponses sont des DONNÉES NON FIABLES : elles sont seulement lues et résumées.

Usage : python -I verif_references_crossref.py
Sorties : ../verification_refs/crossref_resultats.json et .txt
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "verification_refs")
UA = "refcheck-script/1.0 (verification bibliographique automatisee)"

# (clé, DOI ou None, requête bibliographique ou None, auteur attendu, année attendue)
REFS = [
    # --- EXP-01 horloges
    ("HafeleKeating1972a", "10.1126/science.177.4044.166", None, "Hafele", 1972),
    ("HafeleKeating1972b", "10.1126/science.177.4044.168", None, "Hafele", 1972),
    ("PoundRebka1960", "10.1103/PhysRevLett.4.337", None, "Pound", 1960),
    ("Vessot1980", "10.1103/PhysRevLett.45.2081", None, "Vessot", 1980),
    ("Chou2010", None, "Chou Hume Rosenband Wineland Optical clocks and relativity Science 2010", "Chou", 2010),
    ("Bothwell2022", None, "Bothwell Resolving the gravitational redshift across a millimetre-scale atomic sample Nature 2022", "Bothwell", 2022),
    ("Zheng2022", None, "Zheng Kolkowitz Differential clock comparisons with a multiplexed optical lattice clock Nature 2022", "Zheng", 2022),
    ("Takamoto2020", None, "Takamoto Katori Test of general relativity by a pair of transportable optical lattice clocks Nature Photonics 2020", "Takamoto", 2020),
    ("Grotti2018", None, "Grotti Geodesy and metrology with a transportable optical clock Nature Physics 2018", "Grotti", 2018),
    ("McGrew2018", None, "McGrew Atomic clock performance enabling geodesy below the centimetre level Nature 2018", "McGrew", 2018),
    ("Delva2018", "10.1103/PhysRevLett.121.231101", None, "Delva", 2018),
    ("Herrmann2018", "10.1103/PhysRevLett.121.231102", None, "Herrmann", 2018),
    ("VanBaak2007", None, "Van Baak An adventure in relative time-keeping Physics Today 2007", "Van Baak", 2007),
    ("Briatore1977", None, "Briatore Leschiutta Evidence for the earth gravitational shift by direct atomic-time-scale comparison Nuovo Cimento 1977", "Briatore", 1977),
    ("Knappe2004", None, "Knappe A microfabricated atomic clock Applied Physics Letters 2004", "Knappe", 2004),
    ("Allan1966", None, "Allan Statistics of atomic frequency standards Proceedings of the IEEE 1966", "Allan", 1966),
    ("Ashby2003", None, "Ashby Relativity in the Global Positioning System Living Reviews in Relativity 2003", "Ashby", 2003),
    # --- EXP-02 transfert de temps
    ("AllanWeiss1980", None, "Allan Weiss Accurate time and frequency transfer during common-view of a GPS satellite Frequency Control Symposium 1980", "Allan", 1980),
    ("Lipinski2011", None, "Lipinski Wlostowski Serrano Alvarez White Rabbit: a PTP application for robust sub-nanosecond synchronization ISPCS 2011", "Lipi", 2011),
    ("Lisdat2016", None, "Lisdat A clock network for geodesy and fundamental science Nature Communications 2016", "Lisdat", 2016),
    ("OPERA2012", None, "OPERA Measurement of the neutrino velocity with the OPERA detector in the CNGS beam JHEP 2012", "Adam", 2012),
    ("Mills1991", None, "Mills Internet time synchronization: the network time protocol IEEE Transactions on Communications 1991", "Mills", 1991),
    # --- EXP-03 G et test nul
    ("Cavendish1798", None, "Cavendish Experiments to determine the density of the Earth Philosophical Transactions 1798", "Cavendish", 1798),
    ("Gundlach2000", "10.1103/PhysRevLett.85.2869", None, "Gundlach", 2000),
    ("Quinn2013", "10.1103/PhysRevLett.111.101102", None, "Quinn", 2013),
    ("Rosi2014", None, "Rosi Tino Precision measurement of the Newtonian gravitational constant using cold atoms Nature 2014", "Rosi", 2014),
    ("Li2018", None, "Li Luo Measurements of the gravitational constant using two independent methods Nature 2018", "Li", 2018),
    ("Westphal2021", None, "Westphal Aspelmeyer Measurement of gravitational coupling between millimetre-sized masses Nature 2021", "Westphal", 2021),
    ("Kapner2007", "10.1103/PhysRevLett.98.021101", None, "Kapner", 2007),
    ("Lee2020", "10.1103/PhysRevLett.124.101101", None, "Lee", 2020),
    ("Schlamminger2008", "10.1103/PhysRevLett.100.041101", None, "Schlamminger", 2008),
    ("Adelberger2009", None, "Adelberger Torsion balance experiments: A low-energy frontier of particle physics Progress in Particle and Nuclear Physics 2009", "Adelberger", 2009),
    ("Tolman1931", "10.1103/PhysRev.37.602", None, "Tolman", 1931),
    ("Fuzfa2016", "10.1103/PhysRevD.93.024014", None, "Füzfa", 2016),
    ("Hathaway2003", None, "Hathaway Cleveland Bao Gravity modification experiment using a rotating superconducting disk and radio frequency fields Physica C 2003", "Hathaway", 2003),
    ("Tajmar2004", None, "Tajmar Biefeld-Brown effect: misinterpretation of corona wind phenomena AIAA Journal 2004", "Tajmar", 2004),
    ("CODATA2018", "10.1103/RevModPhys.93.025010", None, "Tiesinga", 2021),
    ("CODATA2022", "10.1103/RevModPhys.97.025002", None, "Mohr", 2025),
    # --- EXP-04 gravimétrie
    ("Peters1999", None, "Peters Chung Chu Measurement of gravitational acceleration by dropping atoms Nature 1999", "Peters", 1999),
    ("Middlemiss2016", None, "Middlemiss Hammond Measurement of the Earth tides with a MEMS gravimeter Nature 2016", "Middlemiss", 2016),
    ("Menoret2018", None, "Menoret Gravity measurements below 10-9 g with a transportable absolute quantum gravimeter Scientific Reports 2018", "Ménoret", 2018),
    ("Stray2022", None, "Stray Holynski Quantum sensing for gravity cartography Nature 2022", "Stray", 2022),
    ("Niebauer1995", None, "Niebauer Sasagawa Faller A new generation of absolute gravimeters Metrologia 1995", "Niebauer", 1995),
    ("Goodkind1999", None, "Goodkind The superconducting gravimeter Review of Scientific Instruments 1999", "Goodkind", 1999),
    ("Staacks2018", None, "Staacks Advanced tools for smartphone-based experiments: phyphox Physics Education 2018", "Staacks", 2018),
    # --- EXP-05 Casimir
    ("Lamoreaux1997", "10.1103/PhysRevLett.78.5", None, "Lamoreaux", 1997),
    ("MohideenRoy1998", "10.1103/PhysRevLett.81.4549", None, "Mohideen", 1998),
    ("Bressi2002", "10.1103/PhysRevLett.88.041804", None, "Bressi", 2002),
    ("Chan2001", None, "Chan Aksyuk Kleiman Bishop Capasso Quantum mechanical actuation of microelectromechanical systems by the Casimir force Science 2001", "Chan", 2001),
    ("Munday2009", None, "Munday Capasso Parsegian Measured long-range repulsive Casimir-Lifshitz forces Nature 2009", "Munday", 2009),
    ("Sushkov2011", None, "Sushkov Kim Dalvit Lamoreaux Observation of the thermal Casimir force Nature Physics 2011", "Sushkov", 2011),
    ("Decca2007", "10.1103/PhysRevD.75.077101", None, "Decca", 2007),
    ("Garrett2018", "10.1103/PhysRevLett.120.040401", None, "Garrett", 2018),
    ("Wilson2011", None, "Wilson Johansson Delsing Observation of the dynamical Casimir effect in a superconducting circuit Nature 2011", "Wilson", 2011),
    ("FordRoman1995", "10.1103/PhysRevD.51.4277", None, "Ford", 1995),
    ("FordRoman1996", "10.1103/PhysRevD.53.5496", None, "Ford", 1996),
    ("MTY1988", "10.1103/PhysRevLett.61.1446", None, "Morris", 1988),
    ("Jaffe2005", "10.1103/PhysRevD.72.021301", None, "Jaffe", 2005),
    ("Lamoreaux2005", None, "Lamoreaux The Casimir force: background, experiments, and applications Reports on Progress in Physics 2005", "Lamoreaux", 2005),
    # --- EXP-06 gravité analogue
    ("Unruh1981", "10.1103/PhysRevLett.46.1351", None, "Unruh", 1981),
    ("SchutzholdUnruh2002", "10.1103/PhysRevD.66.044019", None, "Schützhold", 2002),
    ("Rousseaux2008", None, "Rousseaux Observation of negative-frequency waves in a water tank: a classical analogue to the Hawking effect New Journal of Physics 2008", "Rousseaux", 2008),
    ("Weinfurtner2011", "10.1103/PhysRevLett.106.021302", None, "Weinfurtner", 2011),
    ("Jannes2011", "10.1103/PhysRevE.83.056312", None, "Jannes", 2011),
    ("Volovik2005", None, "Volovik Hydraulic jump as a white hole JETP Letters 2005", "Volovik", 2005),
    ("Torres2017", None, "Torres Patrick Coutant Richartz Tedford Weinfurtner Rotational superradiant scattering in a vortex flow Nature Physics 2017", "Torres", 2017),
    ("Euve2016", "10.1103/PhysRevLett.117.121301", None, "Euvé", 2016),
    ("Steinhauer2016", None, "Steinhauer Observation of quantum Hawking radiation and its entanglement in an analogue black hole Nature Physics 2016", "Steinhauer", 2016),
    ("MunozdeNova2019", None, "Munoz de Nova Golubkov Kolobov Steinhauer Observation of thermal Hawking radiation and its temperature in an analogue black hole Nature 2019", "Nova", 2019),
    ("Philbin2008", None, "Philbin Kuklewicz Robertson Hill Konig Leonhardt Fiber-optical analog of the event horizon Science 2008", "Philbin", 2008),
    ("Belgiorno2010", "10.1103/PhysRevLett.105.203901", None, "Belgiorno", 2010),
    ("Drori2019", "10.1103/PhysRevLett.122.010404", None, "Drori", 2019),
    ("Barcelo2011", None, "Barcelo Liberati Visser Analogue gravity Living Reviews in Relativity 2011", "Barceló", 2011),
    ("Torres2020", "10.1103/PhysRevLett.125.011301", None, "Torres", 2020),
    ("Cromb2020", None, "Cromb Gibson Toninelli Padgett Wright Faccio Amplification of waves from a rotating body Nature Physics 2020", "Cromb", 2020),
    ("Svancara2024", None, "Svancara Rotating curved spacetime signatures from a giant quantum vortex Nature 2024", "Švančara", 2024),
    ("BushAristoff2003", None, "Bush Aristoff The influence of surface tension on the circular hydraulic jump Journal of Fluid Mechanics 2003", "Bush", 2003),
    ("Watson1964", None, "Watson The radial spread of a liquid jet over a horizontal plane Journal of Fluid Mechanics 1964", "Watson", 1964),
    ("Bohr1993", None, "Bohr Dimon Putkaradze Shallow-water approach to the circular hydraulic jump Journal of Fluid Mechanics 1993", "Bohr", 1993),
    ("Bhagat2018", None, "Bhagat Jha Linden Wilson On the origin of the circular hydraulic jump in a thin liquid film Journal of Fluid Mechanics 2018", "Bhagat", 2018),
    # --- EXP-07 pièges
    ("Paul1990", "10.1103/RevModPhys.62.531", None, "Paul", 1990),
    ("Wuerker1959", None, "Wuerker Shelton Langmuir Electrodynamic containment of charged particles Journal of Applied Physics 1959", "Wuerker", 1959),
    ("WinterOrtjohann1991", None, "Winter Ortjohann Simple demonstration of storing macroscopic particles in a Paul trap American Journal of Physics 1991", "Winter", 1991),
    ("BerryGeim1997", None, "Berry Geim Of flying frogs and levitrons European Journal of Physics 1997", "Berry", 1997),
    ("SimonGeim2000", None, "Simon Geim Diamagnetic levitation: Flying frogs and floating magnets Journal of Applied Physics 2000", "Simon", 2000),
    ("Simon1997", None, "Simon Heflinger Ridgway Spin stabilized magnetic levitation American Journal of Physics 1997", "Simon", 1997),
    ("LibbrechtBlack2018", None, "Libbrecht Black Improved microparticle electrodynamic ion traps for physics teaching American Journal of Physics 2018", "Libbrecht", 2018),
    ("Rueckner1995", None, "Rueckner Georgi Goodale Rosenberg Tavilla Rotating saddle Paul trap American Journal of Physics 1995", "Rueckner", 1995),
    ("Thompson2002", None, "Thompson Harmon Ball The rotating-saddle trap: a mechanical analogy to RF-electric-quadrupole ion trapping Canadian Journal of Physics 2002", "Thompson", 2002),
    # --- EXP-08 déviation de la lumière
    ("Dyson1920", None, "Dyson Eddington Davidson A determination of the deflection of light by the Sun's gravitational field Philosophical Transactions 1920", "Dyson", 1920),
    ("Shapiro2004", "10.1103/PhysRevLett.92.121101", None, "Shapiro", 2004),
    ("Bertotti2003", None, "Bertotti Iess Tortora A test of general relativity using radio links with the Cassini spacecraft Nature 2003", "Bertotti", 2003),
    # --- EXP-09 Sagnac / Lense-Thirring
    ("MichelsonGale1925", None, "Michelson Gale The effect of the Earth's rotation on the velocity of light Astrophysical Journal 1925", "Michelson", 1925),
    ("Post1967", "10.1103/RevModPhys.39.475", None, "Post", 1967),
    ("ValiShorthill1976", None, "Vali Shorthill Fiber ring interferometer Applied Optics 1976", "Vali", 1976),
    ("SchreiberWells2013", None, "Schreiber Wells Invited Review Article: Large ring lasers for rotation sensing Review of Scientific Instruments 2013", "Schreiber", 2013),
    ("Everitt2011", "10.1103/PhysRevLett.106.221101", None, "Everitt", 2011),
    ("CiufoliniPavlis2004", None, "Ciufolini Pavlis A confirmation of the general relativistic prediction of the Lense-Thirring effect Nature 2004", "Ciufolini", 2004),
    ("Ciufolini2016", None, "Ciufolini A test of general relativity using the LARES and LAGEOS satellites and a GRACE Earth gravity model European Physical Journal C 2016", "Ciufolini", 2016),
    ("Bosi2011", "10.1103/PhysRevD.84.122002", None, "Bosi", 2011),
    ("VenkatramanKrishnan2020", None, "Venkatraman Krishnan Lense-Thirring frame dragging induced by a fast-rotating white dwarf in a binary pulsar system Science 2020", "Krishnan", 2020),
    # --- EXP-10 optique quantique et causalité
    ("ScullyDruhl1982", "10.1103/PhysRevA.25.2208", None, "Scully", 1982),
    ("Kim2000", "10.1103/PhysRevLett.84.1", None, "Kim", 2000),
    ("Walborn2002", "10.1103/PhysRevA.65.033818", None, "Walborn", 2002),
    ("Jacques2007", None, "Jacques Wu Grosshans Treussart Grangier Aspect Roch Experimental realization of Wheeler's delayed-choice gedanken experiment Science 2007", "Jacques", 2007),
    ("Ma2013", None, "Ma Kofler Qarry Zeilinger Quantum erasure with causally disconnected choice PNAS 2013", "Ma", 2013),
    ("Ma2016", "10.1103/RevModPhys.88.015005", None, "Ma", 2016),
    ("Lloyd2011", "10.1103/PhysRevLett.106.040403", None, "Lloyd", 2011),
    ("Ringbauer2014", None, "Ringbauer Broome Myers White Ralph Experimental simulation of closed timelike curves Nature Communications 2014", "Ringbauer", 2014),
    ("Deutsch1991", "10.1103/PhysRevD.44.3197", None, "Deutsch", 1991),
    ("Chiribella2013", "10.1103/PhysRevA.88.022318", None, "Chiribella", 2013),
    ("Procopio2015", None, "Procopio Experimental superposition of orders of quantum gates Nature Communications 2015", "Procopio", 2015),
    ("Rubino2017", None, "Rubino Rozema Experimental verification of an indefinite causal order Science Advances 2017", "Rubino", 2017),
    ("Goswami2018", "10.1103/PhysRevLett.121.090503", None, "Goswami", 2018),
    ("Oreshkov2012", None, "Oreshkov Costa Brukner Quantum correlations with no causal order Nature Communications 2012", "Oreshkov", 2012),
    ("HillmerKwiat2007", None, "Hillmer Kwiat A do-it-yourself quantum eraser Scientific American 2007", "Hillmer", 2007),
    # --- EXP-11 rayonnement
    ("Hawking1974", None, "Hawking Black hole explosions? Nature 1974", "Hawking", 1974),
    ("Hawking1975", None, "Hawking Particle creation by black holes Communications in Mathematical Physics 1975", "Hawking", 1975),
    ("Page1976", "10.1103/PhysRevD.13.198", None, "Page", 1976),
    ("MacGibbonWebber1990", "10.1103/PhysRevD.41.3052", None, "MacGibbon", 1990),
    # --- EXP-12 banc d'essai
    ("Lamport1982", None, "Lamport Shostak Pease The Byzantine Generals Problem ACM Transactions on Programming Languages and Systems 1982", "Lamport", 1982),
    ("LyonsVanderkulk1962", None, "Lyons Vanderkulk The use of triple-modular redundancy to improve computer reliability IBM Journal of Research and Development 1962", "Lyons", 1962),
    ("KleinRoodman2005", None, "Klein Roodman Blind analysis in nuclear and particle physics Annual Review of Nuclear and Particle Science 2005", "Klein", 2005),
    ("MacCounPerlmutter2015", None, "MacCoun Perlmutter Blind analysis: Hide results to seek the truth Nature 2015", "MacCoun", 2015),
    # --- compléments (second passage)
    ("OPERA2012doi", "10.1007/JHEP10(2012)093", None, "Adam", 2012),
    ("Ambrosini1997", None, "Ambrosini Ponticiello Schirripa Spagnolo Borghi Gori Bouncing light beams and the Hamiltonian analogy European Journal of Physics 1997", "Ambrosini", 1997),
    ("Kolobov2021", None, "Kolobov Golubkov Munoz de Nova Steinhauer Observation of stationary spontaneous Hawking radiation and the time evolution of an analogue black hole Nature Physics 2021", "Kolobov", 2021),
    ("Duchesne2019", None, "Duchesne Andersen Bohr Surface tension and the origin of the circular hydraulic jump in a thin liquid film Physical Review Fluids 2019", "Duchesne", 2019),
    ("Vinitsky2015", None, "Vinitsky Black Libbrecht Particle dynamics in damped nonlinear quadrupole ion traps American Journal of Physics 2015", "Vinitsky", 2015),
    ("Gibbons1975", None, "Gibbons Vacuum polarization and the spontaneous loss of charge by black holes Communications in Mathematical Physics 1975", "Gibbons", 1975),
    ("Lefevre2014", None, "Lefevre The fiber-optic gyroscope, a century after Sagnac's experiment: The ultimate rotation-sensing technology? Comptes Rendus Physique 2014", "Lefèvre", 2014),
    ("Schreiber2011", None, "Schreiber Klugel Velikoseltsev Schluter Stedman Wells How to detect the Chandler and the annual wobble of the Earth with a large ring laser gyroscope Physical Review Letters 2011", "Schreiber", 2011),
    ("Lutwak2009", None, "Lutwak The Chip-Scale Atomic Clock - Recent developments IEEE International Frequency Control Symposium 2009", "Lutwak", 2009),
    ("Greenberger1983", None, "Greenberger The neutron interferometer as a device for illustrating the strange behavior of quantum systems Reviews of Modern Physics 1983", "Greenberger", 1983),
    ("Pease1980", None, "Pease Shostak Lamport Reaching agreement in the presence of faults Journal of the ACM 1980", "Pease", 1980),
    ("Peres2004", None, "Peres Terno Quantum information and relativity theory Reviews of Modern Physics 2004", "Peres", 2004),
    ("Brun2009", None, "Brun Harrington Wilde Localized closed timelike curves can perfectly distinguish quantum states Physical Review Letters 2009", "Brun", 2009),
    ("Overstreet2022", None, "Overstreet Asenbaum Curti Kim Kasevich Observation of a gravitational Aharonov-Bohm effect Science 2022", "Overstreet", 2022),
    ("Rothleitner2017", None, "Rothleitner Schlamminger Invited Review Article: Measurements of the Newtonian constant of gravitation, G Review of Scientific Instruments 2017", "Rothleitner", 2017),
    ("Klimchitskaya2009", None, "Klimchitskaya Mohideen Mostepanenko The Casimir force between real materials: Experiment and theory Reviews of Modern Physics 2009", "Klimchitskaya", 2009),
    ("Visser2002", None, "Visser Barcelo Liberati Analogue models of and for gravity General Relativity and Gravitation 2002", "Visser", 2002),
    ("Euve2020", None, "Euve Robertson James Fabbri Rousseaux Scattering of co-current surface waves on an analogue black hole Physical Review Letters 2020", "Euvé", 2020),
    ("Denardo2009", None, "Denardo Puda Larraza A water wave analog of the Casimir effect American Journal of Physics 2009", "Denardo", 2009),
    ("Larraza1998", None, "Larraza Denardo An acoustic Casimir effect Physics Letters A 1998", "Larraza", 1998),
    ("Jekeli2006", None, "Jekeli Precision free-inertial navigation with gravity compensation by an onboard gradiometer Journal of Guidance Control and Dynamics 2006", "Jekeli", 2006),
    ("Casimir1948", None, "Casimir On the attraction between two perfectly conducting plates Proceedings Koninklijke Nederlandse Akademie van Wetenschappen 1948", "Casimir", 1948),
    ("LenseThirring1918", None, "Lense Thirring Uber den Einfluss der Eigenrotation der Zentralkorper auf die Bewegung der Planeten und Monde Physikalische Zeitschrift 1918", "Lense", 1918),
    ("Mashhoon1984", None, "Mashhoon Hehl Theiss On the gravitational effects of rotating masses: The Thirring-Lense papers General Relativity and Gravitation 1984", "Mashhoon", 1984),
    ("Sagnac1913", None, "Sagnac L'ether lumineux demontre par l'effet du vent relatif d'ether dans un interferometre en rotation uniforme Comptes Rendus 1913", "Sagnac", 1913),
    ("Levine2002", None, "Levine Time and frequency distribution using satellites Reports on Progress in Physics 2002", "Levine", 2002),
    ("Novick2015", None, "Novick Lombardi Practical limitations of NTP time transfer IEEE International Frequency Control Symposium European Frequency and Time Forum 2015", "Novick", 2015),
    ("Tipler1974", "10.1103/PhysRevD.9.2203", None, "Tipler", 1974),
    ("Tipler1977", None, "Tipler Singularities and causality violation Annals of Physics 1977", "Tipler", 1977),
    ("Hawking1992", "10.1103/PhysRevD.46.603", None, "Hawking", 1992),
]


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for essai in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8", errors="replace"))
        except Exception as exc:  # noqa: BLE001
            err = repr(exc)
            time.sleep(2 + 2 * essai)
    return {"erreur": err}


def _resume(item):
    if not isinstance(item, dict):
        return {}
    auteurs = item.get("author") or []
    premier = (auteurs[0].get("family") or auteurs[0].get("name") or "") if auteurs else ""
    annee = None
    for champ in ("published-print", "issued", "published-online", "created"):
        dp = (item.get(champ) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            annee = dp[0][0]
            break
    return {
        "doi": item.get("DOI"),
        "premier_auteur": premier,
        "nb_auteurs": len(auteurs),
        "annee": annee,
        "revue": "; ".join(item.get("container-title") or []),
        "volume": item.get("volume"),
        "page": item.get("page") or item.get("article-number"),
        "titre": "; ".join(item.get("title") or []),
        "type": item.get("type"),
    }


def verifier(ref):
    cle, doi, requete, auteur, annee = ref
    if doi:
        d = _get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
        res = [_resume(d.get("message", {}))] if "message" in d else []
        err = d.get("erreur")
    else:
        q = urllib.parse.urlencode({"query.bibliographic": requete, "rows": 3,
                                    "select": "DOI,title,author,issued,published-print,container-title,volume,page,type"})
        d = _get("https://api.crossref.org/works?" + q)
        res = [_resume(it) for it in (d.get("message", {}).get("items") or [])] if "message" in d else []
        err = d.get("erreur")
    return {"cle": cle, "doi_demande": doi, "requete": requete, "auteur_attendu": auteur,
            "annee_attendue": annee, "resultats": res, "erreur": err}


def main():
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, "crossref_resultats.json")
    cache = {}
    if os.path.exists(chemin):
        with open(chemin, encoding="utf-8") as f:
            for t in json.load(f):
                if t.get("resultats") and not t.get("erreur"):
                    cache[t["cle"]] = t
    a_faire = [r for r in REFS if r[0] not in cache]
    print(f"{len(cache)} références déjà en cache, {len(a_faire)} à interroger", file=sys.stderr)
    for r in a_faire:                       # passage séquentiel, poli (évite HTTP 429)
        cache[r[0]] = verifier(r)
        time.sleep(1.5)
    tout = [cache[r[0]] for r in REFS]
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(tout, f, ensure_ascii=False, indent=1)
    lignes = []
    for t in tout:
        lignes.append(f"=== {t['cle']} (attendu : {t['auteur_attendu']} {t['annee_attendue']})")
        if t["erreur"]:
            lignes.append(f"    ERREUR : {t['erreur']}")
        for r in t["resultats"]:
            titre = " ".join((r.get("titre") or "").split())
            lignes.append(f"    {r.get('premier_auteur')} ({r.get('annee')}) | {r.get('revue')} | vol. {r.get('volume')} | "
                          f"p. {r.get('page')} | {titre} | doi:{r.get('doi')}")
    txt = "\n".join(lignes)
    with open(os.path.join(SORTIE, "crossref_resultats.txt"), "w", encoding="utf-8") as f:
        f.write(txt + "\n")
    for t in tout:
        if t["cle"] in [r[0] for r in a_faire]:
            print("===", t["cle"], t.get("erreur") or "")
            for r in t["resultats"]:
                print("    ", r.get("premier_auteur"), r.get("annee"), "|", r.get("revue"), "|", r.get("volume"), "|",
                      r.get("page"), "|", " ".join((r.get("titre") or "").split())[:150], "|", r.get("doi"))


if __name__ == "__main__":
    sys.exit(main())
