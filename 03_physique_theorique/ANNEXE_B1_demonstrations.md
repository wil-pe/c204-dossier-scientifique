# Annexe B1 — Démonstrations (Équipe B)

Complément de `RAPPORT_B.md`. Chaque démonstration indique ses hypothèses, sa portée et le script qui la contrôle.
Signature (−+++). Sauf mention contraire, $G$ et $c$ sont écrits explicitement.

---

## D1. La dilatation du temps ne permet pas d'aller vers le passé

**Définitions.** $(\mathcal M, g)$ espace-temps orientable en temps. Une *fonction temporelle* est une fonction
lisse $t$ dont le gradient $\nabla t$ est partout de genre temps et dirigé vers le passé. Un espace-temps est
*stablement causal* si et seulement s'il admet une telle fonction (Hawking 1969 ; Bernal & Sánchez 2003 ; revue :
Minguzzi 2019). Tout espace-temps globalement hyperbolique est stablement causal et se décompose en
$\mathbb R \times \Sigma$ (Geroch 1970).

**Lemme.** Si $\nabla t$ est de genre temps dirigé vers le passé et $u$ un vecteur causal dirigé vers le futur,
alors $u^\mu\partial_\mu t > 0$.

*Preuve.* Posons $-\nabla t = \alpha\,e_0$ avec $\alpha > 0$ et $e_0$ unitaire dirigé vers le futur. Dans une base
orthonormée $(e_0, e_i)$, $u = u^0e_0 + u^ie_i$ avec $u^0 \ge |\vec u|$ et $u^0 > 0$. Alors
$u^\mu\partial_\mu t = g(u, \nabla t) = -\alpha\,g(u, e_0) = \alpha u^0 > 0$. ∎

**Théorème.** Dans un espace-temps stablement causal, le long de toute ligne d'univers physique (courbe causale
dirigée vers le futur, paramétrée par le temps propre $\tau$) :

$$
\frac{dt}{d\tau} > 0 \quad\text{et}\quad d\tau > 0 .
$$

Aucune courbe causale ne revient donc à une valeur antérieure de $t$ ; en particulier il n'y a pas de courbe
causale fermée. ∎

**Application.**

- *Minkowski.* Le temps $t'$ de **tout** référentiel inertiel est une fonction temporelle. Quels que soient la
  vitesse et l'accélération, $dt'/d\tau = \gamma' \ge 1 > 0$. Le « paradoxe des jumeaux » donne
  $\Delta\tau = \int\sqrt{1 - v^2/c^2}\,dt \in\, ]0, \Delta t]$ : une différence d'âge, jamais un retour.
- *Schwarzschild, $r > r_s$.* $g^{tt} = -[c^2(1 - r_s/r)]^{-1} < 0$ : $t$ est temporelle. Le facteur
  $\Gamma = dt/d\tau$ diverge quand $r \to r_s$, mais reste positif.
- *Kerr-Newman, $r > r_+$.* Voir D4.

**Contraposée.** Atteindre un événement de son propre passé causal exige que l'espace-temps ne soit pas
stablement causal : il faut une structure causale non triviale (courbes causales fermées), ce que ni une grande
vitesse ni un potentiel profond ne créent. *Portée* : théorème de géométrie lorentzienne, indépendant des
équations d'Einstein ; le retour par dilatation est impossible **dans tout espace-temps stablement causal**.
Confiance élevée.

**Réserve (raccourci topologique).** La dilatation *seule* ne crée pas de courbe fermée. Dans un espace-temps à
trou de ver traversable, c'est en revanche une différence de dilatation entre les deux bouches — cinématique
(Morris, Thorne & Yurtsever 1988) ou gravitationnelle (Frolov & Novikov 1990) — qui engendre l'horizon
chronologique : au-delà de cet horizon l'espace-temps n'est plus stablement causal et le théorème ne s'applique
plus. L'ingrédient est alors le trou de ver, donc l'énergie négative (`RAPPORT_B.md` §6.2), non la dilatation.

---

## D2. Accélération des observateurs statiques : $a = c^2\,\nabla\ln N$

**Hypothèse.** Métrique statique $ds^2 = -N(x)^2c^2dt^2 + h_{ij}(x)\,dx^idx^j$.

**Calcul.** L'observateur statique a pour quadrivitesse $u^\mu = (1/N, 0, 0, 0)$ (en unités $c = 1$). Son
accélération est $a^\mu = u^\nu\nabla_\nu u^\mu = \Gamma^\mu_{tt}(u^t)^2$. Or
$\Gamma^i_{tt} = -\tfrac12 h^{ij}\partial_j g_{tt} = h^{ij}N\partial_jN$, d'où

$$
a_i = \partial_i\ln N \qquad (\text{SI} : a_i = c^2\,\partial_i\ln N).
$$

Forme covariante : pour un vecteur de Killing de genre temps $\xi$, $u = \xi/|\xi|$ et $a_\mu = \nabla_\mu\ln|\xi|$.
Contrôle symbolique : script 06, [D3].

**Corollaire (borne de dilatation).** Deux horloges statiques A et B comparées par signaux stationnaires ont un
rapport de rythmes $d\tau_A/d\tau_B = N_A/N_B$. Le long de tout chemin de points statiques joignant A à B :

$$
\ln\Gamma \equiv \ln\frac{N_B}{N_A} = \frac{1}{c^2}\int_A^B a_i\,dx^i \;\le\; \frac{1}{c^2}\int_A^B|a|\,d\ell
$$

(inégalité de Cauchy-Schwarz pour la métrique $h$).

**Application au récit.** $|a| \le 2g$ sur $L \le 3{,}7$ m donne $\ln\Gamma \le 8{,}1\times10^{-16}$. Pour
$\ln\Gamma = \ln 87\,660 = 11{,}38$ il faut $\langle|a|\rangle \ge c^2\ln\Gamma/L = 2{,}8\times10^{17}$ m/s².

**Hypothèses de l'application** (les quatre sont nécessaires) :

1. la géométrie est **stationnaire** (existence d'un champ de Killing de genre temps $\xi$ ; la démonstration
   ci-dessus est écrite dans le cas statique, la forme covariante $a_\mu = \nabla_\mu\ln|\xi|$ couvre le cas
   stationnaire pour les observateurs qui suivent $\xi$) ;
2. le véhicule est **immobile** dans ce champ (il suit une orbite de $\xi$) ;
3. $|a| \le 2g$ sur **tout** le chemin joignant le véhicule à la zone de référence, y compris hors du véhicule ;
4. le potentiel est négligeable au-delà de $L$ (la zone de référence est « à l'infini » à $10^{-9}$ près).

**Portée et limite.** La borne porte sur les éléments *statiques* du chemin. Un passager peut ne rien ressentir
s'il est en chute libre dans une cavité (potentiel uniforme) ; mais alors la paroi de la cavité, le sol et l'air
qui raccordent l'intérieur à l'extérieur subissent l'intégrale $\int|a|\,d\ell = c^2\ln\Gamma$ : c'est
l'hypothèse 3 qui tombe, et le cas est traité en D5 ($\Gamma \le 5$). Dans le récit, le véhicule, le sol
« emporté » et la poche d'air sont décrits comme immobiles : la borne s'applique.

**Cas non couvert : géométrie non stationnaire.** Hors stationnarité la borne ne contraint rien (un observateur
en chute libre ne ressent aucune accélération et peut avoir un $dt/d\tau$ arbitraire). Or le dispositif est décrit
comme dynamique. Ce cas relève de l'argument d'échelle D3 (a) : toute géométrie de champ fort sur une longueur
$\ell$ exige $M \sim \ell c^2/G$, qu'elle soit stationnaire ou non.

---

## D3. Invariance d'échelle du vide et absence de CTC en champ faible

**(a) Invariance d'échelle.** Pour $\lambda > 0$ constant, $\tilde g = \lambda^2g$ a les mêmes symboles de
Christoffel et le même tenseur de Ricci que $g$. Donc $R_{\mu\nu}[g] = 0 \Rightarrow R_{\mu\nu}[\tilde g] = 0$.
Longueurs et durées sont multipliées par $\lambda$ ; la masse d'ADM par $\lambda$ ; le moment cinétique par
$\lambda^2$. Pour Einstein-Maxwell, la symétrie s'étend avec $A_\mu \to \lambda A_\mu$, $Q \to \lambda Q$.

**Conséquence.** Toute longueur caractéristique $\ell$ d'une solution du vide (rayon d'horizon, taille d'une zone
à CTC) s'écrit

$$
\ell = \frac{GM}{c^2}\,f\!\left(\frac{Jc}{GM^2}, \frac{Q}{M\sqrt{4\pi\varepsilon_0G}}, \frac{d_{ij}c^2}{GM}, \dots\right).
$$

On ne peut pas conserver la géométrie (« le même environnement ») en réduisant la masse.

**(b) Proposition (champ faible ⇒ pas de CTC).** Soit $U$ une région munie de coordonnées $(x^0, x^i)$ dans
lesquelles $g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$ avec $|h_{\mu\nu}| \le \varepsilon < 1/8$. Alors $x^0$ est une
fonction temporelle sur $U$, et aucune courbe causale fermée n'est contenue dans $U$.

*Preuve.* $g^{-1} = \eta^{-1}(1 + h\eta^{-1})^{-1}$. La norme d'opérateur de $h\eta^{-1}$ est au plus $4\varepsilon < 1/2$,
donc la série de Neumann converge et $|g^{00} + 1| \le 4\varepsilon/(1 - 4\varepsilon) < 1$. Ainsi $g^{00} < 0$ :
$\nabla x^0$ est de genre temps, et D1 s'applique à $U$. ∎

**Application.** Pour deux trous noirs de masse $\le 5\times10^{12}$ kg, $|h| \sim 4GM/(rc^2) < 1/8$ dès que
$r > 32\,GM/c^2 \approx 1{,}2\times10^{-13}$ m. Toute la région située à plus de $10^{-13}$ m des deux
singularités — donc le véhicule entier — est exempte de CTC. Le résultat vaut que les trous tournent, soient
chargés, orbitent ou non. *Limite* : l'existence de telles coordonnées est supposée (elle est assurée en
jauge harmonique pour des sources compactes en champ faible).

---

## D4. L'extérieur de Kerr-Newman est stablement causal

**Hypothèse : $a^2 + Q^2 \le M^2$** (unités géométriques ; en SI $a^2 + r_Q^2 \le (GM/c^2)^2$), c'est-à-dire
existence d'un horizon. Dans le cas sur-extrémal il n'y a pas d'horizon, la zone $g_{\varphi\varphi} < 0$ est
accessible depuis l'infini et la violation de causalité est totale (Carter 1968) ; la démonstration ci-dessous ne
s'applique pas, et la conclusion pratique repose alors sur D3 (b) — voir la remarque en fin de section.

En coordonnées de Boyer-Lindquist (unités géométriques, $x = \cos\theta$) :

$$
g^{tt} = -\frac{N}{\Delta\,\Sigma},\qquad N = (r^2 + a^2)^2 - \Delta\,a^2\sin^2\theta .
$$

Identité (vérifiée, script 03 [A5]) :

$$
N = r^2(r^2 + a^2) + a^2(2Mr - Q^2) + \Delta\,a^2\cos^2\theta .
$$

Pour $r > r_+$ : $\Delta > 0$, $\Sigma > 0$, et $2Mr - Q^2 > 2Mr_+ - Q^2 = r_+^2 + a^2 > 0$. Donc $N > 0$ et
$g^{tt} < 0$ : $t$ est une fonction temporelle sur tout le domaine extérieur. Par D1, **aucune courbe causale
fermée ne passe par un événement de la région $r > r_+$ en y restant**. Les CTC de Kerr-Newman exigent de
franchir $r_+$ puis $r_-$. ∎

Zone génératrice des CTC (script 03 [A3]) : sur l'équateur,
$g_{\varphi\varphi} = r^2 + a^2 + a^2(2Mr - Q^2)/r^2$. Pour Kerr, $g_{\varphi\varphi} < 0 \iff r_c < r < 0$ avec
$r_c^3 + a^2r_c + 2Ma^2 = 0$ ; on vérifie $|r_c| \le M$ pour $a \le M$ (égalité à $a = M$) et $|r_c| \to 2M$ pour $a \gg M$.

**Remarque : cas sur-extrémal ($a^2 + Q^2 > M^2$).** Alors $\Delta > 0$ partout, il n'y a ni $r_+$ ni $r_-$, et
l'argument précédent ne ferme plus la région $r > 0$ : une courbe peut traverser le disque $r = 0$, parcourir la
zone $g_{\varphi\varphi} < 0$ et revenir. Deux résultats subsistent.

- *D3 (b)*, qui ne suppose pas d'horizon : toute courbe causale fermée doit quitter la région de champ faible,
  donc passer à moins de $\sim 32\,GM/c^2$ de la singularité.
- *Temps de Kerr-Schild* : $dt_{\rm KS} = dt + \dfrac{2Mr - Q^2}{\Delta}\,dr$. On vérifie (script 03 [A6])

$$
g^{tt}_{\rm KS} = g^{tt} + \left[\frac{2Mr - Q^2}{\Delta}\right]^2 g^{rr} = -\left(1 + \frac{2Mr - Q^2}{\Sigma}\right).
$$

  C'est la forme de Kerr-Schild $g_{\mu\nu} = \eta_{\mu\nu} + 2Hk_\mu k_\nu$, $H = (2Mr - Q^2)/2\Sigma$, $k$ de genre
  lumière. Le temps de Kerr-Schild est donc une fonction temporelle sur les deux feuillets, **sans hypothèse
  d'horizon**, sauf là où $\Sigma + 2Mr - Q^2 \le 0$, c'est-à-dire dans le tube
  $(r + M)^2 + a^2\cos^2\theta \le M^2 + Q^2$ entourant l'anneau. Par D1, toute courbe causale fermée traverse ce
  tube, dont la taille est fixée par $M$ et $Q$ ($\sim 10^{-15}$ m pour $10^{12}$ kg) quel que soit $a$.

---

## D5. Bornes sur la dilatation à l'intérieur d'une distribution statique de matière

**(a) Coquille mince.** Intérieur plat, extérieur de Schwarzschild de masse $M$, coquille de rayon aréolaire $R$.
Avec $k = \sqrt{1 - 2GM/(Rc^2)}$, les conditions de jonction d'Israel (1966) donnent ($G = c = 1$) :

$$
\sigma = \frac{1 - k}{4\pi R},\qquad p = \frac{1}{8\pi R}\left[\frac{1 - M/R}{k} - 1\right] = \frac{(1 - k)^2}{16\pi Rk},\qquad \frac{p}{\sigma} = \frac{1 - k}{4k}.
$$

La continuité de $g_{tt}$ impose $N_{\rm int} = k$, donc $\Gamma_{\rm int} = 1/k$. La condition d'énergie
dominante $p \le \sigma$ équivaut à $k \ge 1/5$, soit $R \ge \tfrac{25}{24}r_s$ et

$$
\Gamma_{\rm int} \le 5 .
$$

Contrôle : script 06 [D4]. Avec la seule condition d'énergie faible, $k \to 0$ est permis mais $p/\sigma \to \infty$.

**(b) Étoile homogène** (solution intérieure de Schwarzschild). $N_c = (3k - 1)/2$ et
$p_c/\rho c^2 = (1 - k)/(3k - 1)$. La condition $p_c \le \rho c^2$ donne $k \ge 1/2$, donc $\Gamma_c \le 4$. La
pression centrale diverge à $k = 1/3$ (borne de Buchdahl 1959, $R = \tfrac98r_s$) ; plus généralement
$2GM/(Rc^2) \le 8/9$ pour toute matière vérifiant $p_r + 2p_t \le \rho c^2$ (Andréasson 2008).

**Portée.** Deux modèles, pas un théorème général sur le lapse central. Ils suffisent à montrer que
$\Gamma \sim 10^5$ n'est atteignable par aucune configuration statique « ordinaire » : il faut se tenir à
$10^{-10}\,r_s$ d'un horizon.

---

## D6. Critère de Gott par holonomie

En gravité 2+1 (cordes parallèles), une corde au repos de masse linéique $\mu$ est représentée par une rotation
$R(\delta)$ d'angle $\delta = 8\pi G\mu/c^2$ ; en mouvement à la rapidité $\xi$ : $B(\xi)R(\delta)B(-\xi)$.
Pour deux cordes identiques de rapidités opposées, la holonomie totale $T$ vérifie

$$
\cos\frac{\delta_{\rm tot}}{2} = 1 - 2\sin^2\!\alpha\,\cosh^2\!\xi,\qquad \alpha = \frac{\delta}{2} = \frac{4\pi G\mu}{c^2}.
$$

$T$ est une rotation (masse totale de genre temps) si le membre de droite est dans $[-1, 1]$ ; c'est un boost
(impulsion totale de genre espace, CTC de Gott) si

$$
\gamma\,\sin\alpha > 1,\qquad \gamma = \cosh\xi .
$$

Contrôle numérique : $\mathrm{Tr}\,T > 3 \iff \gamma\sin\alpha > 1$ sur 20 000 tirages (script 05 [B5]).
Références : Gott (1991) ; Deser, Jackiw & 't Hooft (1992) ; Carroll, Farhi & Guth (1992).

---

## D7. Charge maximale d'un trou noir

**Extrémalité.** $r_Q \le GM/c^2 \iff |Q| \le M\sqrt{4\pi\varepsilon_0G} = 8{,}62\times10^{-11}$ C/kg × $M$.

**Grand trou noir** ($r_+ \gg \hbar/m_ec$, soit $M \gg 2{,}6\times10^{14}$ kg). Le champ à l'horizon est quasi
uniforme à l'échelle de Compton ; la création de paires de Schwinger, de taux
$\propto E^2\exp(-\pi E_S/E)$ avec $E_S = m_e^2c^3/(e\hbar)$, décharge le trou tant que $E_h \gtrsim E_S$.
Pour un trou extrémal, $E_h = c^4/(G^{3/2}M\sqrt{4\pi\varepsilon_0})$ ; $E_h < E_S \iff M > 1{,}06\times10^{36}$ kg
(5 × 10⁵ masses solaires ; Gibbons 1975 donne le même ordre de grandeur).

**Micro-trou noir** ($r_+ \ll \hbar/m_ec$). Le champ n'est intense que sur une région bien plus petite que la
longueur de Compton : le critère pertinent est celui d'une charge ponctuelle, pour laquelle l'état fondamental
de Dirac plonge dans le continuum négatif quand $Z\alpha \gtrsim 1$. D'où une **borne supérieure d'ordre de
grandeur**, $|Q| \lesssim e/\alpha \approx 137\,e$.

**Valeur typique.** Si $k_BT_H \gg m_ec^2$, l'émission thermique d'e± est biaisée par le potentiel et neutralise
toute charge ; la charge fluctue. Page (1977, résumé relu sur INSPIRE) calcule sa valeur quadratique moyenne :
**6,14 e** pour $GM\mu/\hbar c \to 0$, 2,76 e pour $GM\mu/\hbar c = 0{,}4$, 2,34 e pour $GM\mu/\hbar c \gg 1$
($\mu$ : masse du lepton). Pour des électrons et $M = 4{,}4\times10^{12}$ kg, $GM\mu/\hbar c = 0{,}008$ : régime
de 6,14 e. Estimation thermique indépendante : $Q_{\rm rms} \sim e/\sqrt{4\pi\alpha} = 3{,}3\,e$ (énergie
électrostatique $Q^2/8\pi\varepsilon_0r_s$ de l'ordre de $k_BT_H/2$).

**Conséquence pour $r_-$.** $r_- = r_Q^2/r_+ \simeq GQ^2/(4\pi\varepsilon_0c^4r_s)$ : pour $M = 10^{12}$ kg,
$4{,}8\times10^{-56}$ m avec la charge typique (6 e) et $2{,}4\times10^{-53}$ m avec la borne (137 e).

**Coût de la charge.** Formule de Christodoulou & Ruffini (1971) : $M = M_{\rm irr} + Q^2/(4M_{\rm irr})$ (unités
géométriques, $J = 0$). À l'extrémalité, $Q = 2M_{\rm irr} = M$ : la moitié de $Mc^2$ est électrostatique.
Le potentiel d'horizon d'un trou extrémal vaut $c^2/\sqrt{4\pi\varepsilon_0G} = 1{,}04\times10^{27}$ V quelle que
soit la masse (soit $\sqrt\alpha$ fois l'énergie de Planck par charge élémentaire).

*Portée* : ordres de grandeur ; l'écart avec l'extrémalité (19 à 20 ordres de grandeur) rend la conclusion robuste.

---

## D8. Puissance de Hawking : méthode de calcul

Unités $G = c = \hbar = k_B = 1$, $M = 1$, $f = 1 - 2/r$, $r_* = r + 2\ln(r/2 - 1)$.

$$
\frac{d^2\psi}{dr_*^2} + \left[\omega^2 - V(r)\right]\psi = 0,\qquad
V_{s=0,1,2} = f\left[\frac{\ell(\ell+1)}{r^2} + \frac{2(1 - s^2)}{r^3}\right],\qquad
V_{1/2} = \frac{\kappa^2f}{r^2} - \frac{\kappa\sqrt f\,(r - 3)}{r^3}.
$$

Condition $\psi \to e^{-i\omega r_*}$ à l'horizon ; à grande distance $\psi \simeq A_{\rm in}e^{-i\omega r_*} + A_{\rm out}e^{i\omega r_*}$ ;
$\Gamma = 1/|A_{\rm in}|^2$, extrait de $|A_{\rm in}|^2 + |A_{\rm out}|^2$ et de la conservation du wronskien
($|A_{\rm in}|^2 - |A_{\rm out}|^2 = 1$). Puissance par degré de liberté :

$$
P_s = \frac{1}{2\pi}\int_0^\infty d\omega\,\omega\,\frac{\sum_{\rm modes}g\,\Gamma(\omega)}{e^{8\pi\omega} \mp 1},\qquad
g = 2\ell + 1\ (\ell \ge s)\ \text{ou}\ 2\kappa\ (\kappa = 1, 2, \dots).
$$

Intégration : DOP853, tolérance relative 10⁻⁹ ; 161 fréquences jusqu'à $\omega = 32\,T$ ; modes jusqu'à 12 ;
erreur relative de flux < 10⁻⁸. Résultats et comparaison à Page (1976) : `RAPPORT_B.md` §4.1.

Seuils de masse **[HYP de modélisation]** : une espèce de masse $m$ reçoit la fraction du spectre sans masse située
au-dessus de $mc^2$ ; quarks et gluons comptés comme partons libres au-dessus de 0,3 et 0,6 GeV (dans l'esprit de
MacGibbon & Webber 1990). Contrôle : la masse dont la durée de vie vaut 13,8 Ga ressort à 5,3 × 10¹¹ kg, contre
≈ 5,0–5,1 × 10¹¹ kg dans la littérature (MacGibbon, Carr & Page 2008).

---

## D9. Énergie de la bulle d'Alcubierre

Métrique $ds^2 = -c^2dt^2 + (dx - v f(r_s)\,dt)^2 + dy^2 + dz^2$. Les tranches $t$ = const. sont plates ; la
contrainte hamiltonienne donne la densité d'énergie vue par les observateurs eulériens :

$$
\rho_E = \frac{c^4}{16\pi G}\left(K^2 - K_{ij}K^{ij}\right),\qquad K_{ij} = \tfrac12(\partial_i\beta_j + \partial_j\beta_i),\quad \beta = (-vf/c, 0, 0).
$$

Seuls $K_{xx}$, $K_{xy}$, $K_{xz}$ sont non nuls, d'où $K^2 - K_{ij}K^{ij} = -2(K_{xy}^2 + K_{xz}^2)$ et

$$
\rho_E = -\frac{c^2v^2}{32\pi G}\,\frac{y^2 + z^2}{r^2}\left(\frac{df}{dr}\right)^2 \le 0 .
$$

Intégrale sur l'espace : $E = -\dfrac{c^2v^2}{12G}\displaystyle\int_0^\infty r^2f'(r)^2\,dr$. Pour un profil linéaire
d'épaisseur $\Delta$ autour de $R$ : $\int r^2f'^2dr = R^2/\Delta + \Delta/12$. Contrôle symbolique : script 07 [E5].
On retrouve l'expression d'Alcubierre (1994) et l'estimation de Pfenning & Ford (1997).

---

## D10. Structure log-périodique de l'extérieur de Tipler

Pour $aR > 1/2$, les fonctions $L$, $M$, $F$ sont égales à $r$ fois une sinusoïde de $\ln r$ : $L/r$, $M/r$ et
$F/r$ sont des sinusoïdes exactes de $\ln r$, tandis que $L$, $M$, $F$ sont log-périodiques d'amplitude
croissante. En particulier $g_{\varphi\varphi} = L \propto r\sin(3\beta + \gamma)$ avec $\gamma = m\ln(r/R)$,
$m = \sqrt{4a^2R^2 - 1}$, $\beta = \arctan m$. Les zéros sont

$$
r_n = R\,\exp\!\left(\frac{n\pi - 3\beta}{m}\right),\qquad \frac{r_{n+1}}{r_n} = e^{\pi/m}.
$$

Entre deux zéros successifs, $\partial_\varphi$ est alternativement de genre temps (cercles = CTC) et de genre
espace. Comme $FL + M^2 = r^2 > 0$, la signature reste lorentzienne partout. Pour $1/2 < aR < 1$, la première
zone à CTC ne commence qu'à $r_1 > R$ ; pour $aR$ proche de 1/2 elle est rejetée très loin
($r_1/R = 3\times10^5$ pour $aR = 0{,}51$). Contrôle : script 04 [V2–V4].

*Attention* : ces zones décrivent le signe de $g_{\varphi\varphi}$, non des domaines causalement séparés. Pour
$aR > 1/2$, une courbe fermée de genre temps joint deux événements quelconques de l'extérieur (Tipler 1974).

---

## D11. Trou noir extrémal à charge magnétique

Charge magnétique $g$ (en A·m, convention $F = gB$). Extrémalité : $GM^2 = \mu_0g^2/4\pi$, soit

$$
M = g\sqrt{\frac{\mu_0}{4\pi G}} .
$$

Charge de Dirac $g_D = h/(\mu_0e)$ : masse par unité $M_1 = m_P/(2\sqrt\alpha) = 5{,}85\,m_P$.
Champ du monopôle : $B(r) = \mu_0g/(4\pi r^2)$ ; pesanteur : $g_{\rm grav}(r) = GM/r^2$. D'où

$$
\frac{B(r)}{g_{\rm grav}(r)} = \sqrt{\frac{\mu_0}{4\pi G}} = 38{,}7\ \text{T par m/s}^2,\qquad
B_{\rm sustentation} = \frac{Mg_0}{g} = g_0\sqrt{\frac{\mu_0}{4\pi G}} = 380\ \text{T}.
$$

Contrôle : script 08 [C4]. *Portée* : suppose l'existence de monopôles magnétiques, jamais observés.
