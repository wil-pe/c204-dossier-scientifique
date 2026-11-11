#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Équipe E — Programme C204 — génération de la visionneuse interactive autonome.

    modele_c204.json  ──►  visionneuse.html   (un seul fichier ; données embarquées en JSON)

La page charge three.js r128 depuis cdnjs (version figée) et construit les primitives three.js
DIRECTEMENT à partir du JSON embarqué (aucun chargeur glTF). Fonctions : rotation / zoom / panoramique
(souris et tactile), bascule fermé / ouvert / éclaté / à plat, coloration par classement, aspect ou
système, filtres par classement et par couche, enveloppes translucides, clic sur une pièce → fiche,
bascule variante A / A′ / B, thème clair et sombre.

Usage : python generer_visionneuse.py
"""
import json
from pathlib import Path

ICI = Path(__file__).resolve().parent
CHAMPS = ("id", "nom", "ensemble", "repere", "source", "classement", "existence", "fonction_revendiquee", "systeme", "primitive",
          "position", "quaternion", "liaison", "eclate", "couleur", "opacite", "couche", "masque", "fantome", "notes", "appui")


def donnees_embarquees(modele):
    d = {"meta": {k: modele["meta"][k] for k in ("titre", "avertissement", "genere_le", "classements", "systemes")}, "variantes": {}}
    for cle, v in modele["variantes"].items():
        d["variantes"][cle] = {
            "nom": v["nom"], "description": v["description"], "documents": v["documents"], "etats": v["etats"],
            "articulations": v["articulations"], "cotes_cles": v["cotes_cles"], "bilan_classement": v["bilan_classement"],
            "pieces": [{k: p[k] for k in CHAMPS if k in p} for p in v["pieces"]],
        }
    d["echelle"] = {"L": modele["cotes"]["L"]["valeur"], "incertitude": modele["cotes"]["L"]["incertitude"], "source": modele["cotes"]["L"]["source"]}
    return d


GABARIT = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>C204 — visionneuse du modèle 3D</title>
<meta name="description" content="Visionneuse interactive du modèle 3D reconstruit de l'unité « C204 » (reconstruction documentaire, objet non attesté).">
<style>
:root{
  --fond:#f3f4f6; --scene:#e9ebef; --carte:#ffffff; --carte2:#f6f7f9; --texte:#16181d; --texte2:#4b5262; --trait:#d5d9e0;
  --accent:#0b5cad; --accent-texte:#ffffff; --alerte:#8a4b00; --alerte-fond:#fff4dc; --ombre:0 6px 24px rgba(15,23,42,.14);
  --doc:#0072B2; --ded:#E69F00; --hyp:#CC79A7; --rayon:10px;
  color-scheme: light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --fond:#101216; --scene:#171a20; --carte:#1c2027; --carte2:#232831; --texte:#e9ecf1; --texte2:#a6adbb; --trait:#343b47;
    --accent:#6fb2ff; --accent-texte:#0b1320; --alerte:#ffcf7a; --alerte-fond:#33270f; --ombre:0 6px 24px rgba(0,0,0,.5);
    color-scheme: dark;
  }
}
:root[data-theme="dark"]{
  --fond:#101216; --scene:#171a20; --carte:#1c2027; --carte2:#232831; --texte:#e9ecf1; --texte2:#a6adbb; --trait:#343b47;
  --accent:#6fb2ff; --accent-texte:#0b1320; --alerte:#ffcf7a; --alerte-fond:#33270f; --ombre:0 6px 24px rgba(0,0,0,.5);
  color-scheme: dark;
}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--fond);color:var(--texte);font:14px/1.45 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;overflow:hidden}
#app{position:fixed;inset:0;display:grid;grid-template-rows:auto auto 1fr}
#note-langue{margin:0;padding:4px 14px;font-size:12.5px;line-height:1.35;background:var(--alerte-fond);color:var(--alerte);border-bottom:1px solid var(--trait)}
#note-langue a{color:inherit;font-weight:650}
header{display:flex;align-items:center;gap:12px;padding:8px 14px;background:var(--carte);border-bottom:1px solid var(--trait);min-width:0}
header h1{font-size:15px;margin:0;font-weight:650;white-space:nowrap}
header p{margin:0;color:var(--alerte);background:var(--alerte-fond);padding:3px 9px;border-radius:999px;font-size:12px;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1 1 auto}
header .droite{display:flex;gap:6px;flex:0 0 auto}
main{position:relative;min-height:0}
#scene{position:absolute;inset:0;background:var(--scene)}
canvas{display:block;width:100%;height:100%;touch-action:none;outline:none;cursor:grab}
canvas.saisie{cursor:grabbing}
.panneau{position:absolute;top:12px;left:12px;width:292px;max-height:calc(100% - 24px);overflow:auto;background:var(--carte);border:1px solid var(--trait);border-radius:var(--rayon);box-shadow:var(--ombre);padding:10px 12px 12px}
.panneau h2{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--texte2);margin:12px 0 5px;font-weight:650}
.panneau h2:first-child{margin-top:2px}
.seg{display:flex;flex-wrap:wrap;gap:4px}
button{font:inherit;color:var(--texte);background:var(--carte2);border:1px solid var(--trait);border-radius:7px;padding:5px 9px;cursor:pointer;line-height:1.2}
button:hover{border-color:var(--accent)}
button:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-texte);font-weight:600}
button:disabled{opacity:.42;cursor:not-allowed}
.seg button{flex:1 1 auto}
label.coche{display:flex;align-items:center;gap:7px;padding:2px 0;cursor:pointer}
label.coche input{width:16px;height:16px;accent-color:var(--accent);margin:0}
.pastille{display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid rgba(0,0,0,.35);flex:0 0 auto}
.compte{color:var(--texte2);margin-left:auto;font-variant-numeric:tabular-nums}
.grille2{display:grid;grid-template-columns:1fr}
.desc{color:var(--texte2);font-size:12.5px;margin:6px 0 0}
#legende{position:absolute;left:328px;bottom:12px;background:var(--carte);border:1px solid var(--trait);border-radius:var(--rayon);padding:7px 10px;box-shadow:var(--ombre);max-width:min(620px,calc(100% - 340px));font-size:12.5px;display:flex;flex-wrap:wrap;gap:4px 14px;pointer-events:none}
#legende span{display:inline-flex;align-items:center;gap:6px}
#fiche{position:absolute;top:12px;right:12px;width:340px;max-height:calc(100% - 24px);overflow:auto;background:var(--carte);border:1px solid var(--trait);border-radius:var(--rayon);box-shadow:var(--ombre);padding:12px 14px}
#fiche[hidden]{display:none}
#fiche h3{margin:0 30px 6px 0;font-size:15.5px;line-height:1.3}
#fiche .fermer{position:absolute;top:8px;right:8px;width:28px;height:28px;padding:0;border-radius:50%}
.badge{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:2px 9px;font-size:12px;font-weight:650;border:1px solid var(--trait);margin:0 4px 4px 0;background:var(--carte2)}
dl{margin:8px 0 0;display:grid;grid-template-columns:1fr;gap:1px 0}
dt{font-size:11px;letter-spacing:.05em;text-transform:uppercase;color:var(--texte2);margin-top:8px}
dd{margin:0;overflow-wrap:anywhere}
dd small{color:var(--texte2)}
#bulle{position:absolute;pointer-events:none;background:var(--texte);color:var(--carte);padding:3px 8px;border-radius:6px;font-size:12px;max-width:280px;transform:translate(12px,14px);z-index:5}
#bulle[hidden]{display:none}
#erreur{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;padding:24px;text-align:center}
#erreur[hidden]{display:none}
#erreur div{background:var(--carte);border:1px solid var(--trait);border-radius:var(--rayon);padding:18px 22px;max-width:520px;box-shadow:var(--ombre)}
details summary{cursor:pointer;color:var(--texte2);font-size:11px;letter-spacing:.06em;text-transform:uppercase;font-weight:650;margin:12px 0 5px}
#recherche{width:100%;font:inherit;padding:5px 8px;border-radius:7px;border:1px solid var(--trait);background:var(--carte2);color:var(--texte)}
#liste{list-style:none;margin:6px 0 0;padding:0;max-height:220px;overflow:auto;border:1px solid var(--trait);border-radius:7px}
#liste li button{display:flex;gap:7px;align-items:center;width:100%;text-align:left;border:0;border-bottom:1px solid var(--trait);border-radius:0;background:transparent;padding:5px 8px;font-size:12.5px}
#liste li:last-child button{border-bottom:0}
#liste li button:hover{background:var(--carte2)}
#bascule-panneau{display:none}
.aide{color:var(--texte2);font-size:12px;margin:8px 0 0}
@media (max-width: 760px){
  header{padding:6px 16px;gap:8px}
  header h1{font-size:14px;min-width:0;overflow:hidden;text-overflow:ellipsis;flex:1 1 auto}
  header button{padding:5px 8px;white-space:nowrap}
  header p{display:none}
  #bascule-panneau{display:inline-block}
  .panneau{top:8px;left:16px;right:16px;width:auto;max-height:62%}
  .panneau[data-replie="1"]{display:none}
  #fiche{top:auto;bottom:0;left:0;right:0;width:auto;max-height:46%;border-radius:14px 14px 0 0;border-bottom:0;padding:12px 16px calc(12px + env(safe-area-inset-bottom))}
  #legende{left:16px;right:16px;bottom:8px;max-width:none;font-size:12px}
  #fiche:not([hidden]) ~ #legende{display:none}
}
</style>
</head>
<body>
<div id="app">
  <header>
    <h1>C204 — modèle 3D reconstruit</h1>
    <p title="__AVERT__">Reconstruction documentaire : objet décrit, non attesté — échelle hypothétique (L = __ECHELLE__)</p>
    <div class="droite">
      <button id="bascule-panneau" type="button" aria-expanded="false">Réglages</button>
      <button id="theme" type="button" title="Thème : automatique, clair, sombre">Thème : auto</button>
    </div>
  </header>
  <p id="note-langue"><span lang="en">This page is in French — <a href="simulateur.html#lang=en">the simulator has an English version</a>.</span> <span lang="fr">Page en français ; <a href="simulateur.html#lang=fr">le simulateur existe aussi en anglais</a>.</span></p>
  <main>
    <div id="scene"><canvas id="toile" tabindex="0" aria-label="Vue 3D du modèle ; glisser pour tourner, molette ou pincement pour zoomer"></canvas></div>

    <section class="panneau" id="panneau" data-replie="1" aria-label="Réglages de la vue">
      <h2>Variante</h2>
      <div class="seg" id="g-variante">
        <button type="button" data-v="A" title="Coffre plat (DOC-001 à 004, 007) et composants de DOC-008 — disposition interne I1">A · coffre</button>
        <button type="button" data-v="A2" title="Même coffre, autre disposition interne hypothétique (I2)">A′ · disposition I2</button>
        <button type="button" data-v="B" title="Écorché DOC-005 : enveloppe prismatique et volumes principaux">B · écorché DOC-005</button>
      </div>
      <p class="desc" id="desc-variante"></p>

      <h2>État</h2>
      <div class="seg" id="g-etat">
        <button type="button" data-e="ferme">Fermé</button>
        <button type="button" data-e="ouvert">Ouvert</button>
        <button type="button" data-e="eclate">Éclaté</button>
        <button type="button" data-e="a_plat" title="Couvercle rabattu à 180°, comme sur la vue de dessus DOC-007">À plat</button>
      </div>

      <h2>Couleurs</h2>
      <div class="seg" id="g-couleur">
        <button type="button" data-c="classement">Classement</button>
        <button type="button" data-c="aspect">Aspect</button>
        <button type="button" data-c="systeme">Système</button>
      </div>

      <h2>Classement affiché</h2>
      <div id="g-classes"></div>

      <h2>Couches</h2>
      <div class="grille2" id="g-couches"></div>
      <label class="coche" style="margin-top:6px"><input type="checkbox" id="fantome"> Enveloppes translucides (voir l'intérieur)</label>

      <h2>Vue</h2>
      <div class="seg" id="g-vue">
        <button type="button" data-vue="iso">3/4</button>
        <button type="button" data-vue="dessus">Dessus</button>
        <button type="button" data-vue="face">Face</button>
        <button type="button" data-vue="cote">Côté</button>
        <button type="button" data-vue="cadrer">Recadrer</button>
      </div>

      <details>
        <summary>Liste des pièces</summary>
        <input id="recherche" type="search" placeholder="Filtrer : nom, repère, document…" aria-label="Filtrer la liste des pièces">
        <ul id="liste"></ul>
      </details>
      <p class="aide">Quadrillage au sol : mailles de 10 cm (échelle hypothétique, L = __ECHELLE__). Glisser : tourner · molette ou pincement : zoom · clic droit, Maj+glisser ou deux doigts : déplacer · clic sur une pièce : fiche.</p>
    </section>

    <aside id="fiche" hidden aria-live="polite" aria-label="Fiche de la pièce sélectionnée"></aside>
    <div id="legende" aria-hidden="true"></div>
    <div id="bulle" hidden></div>
    <div id="erreur" hidden><div><strong>Affichage 3D indisponible.</strong><p id="erreur-texte">La bibliothèque three.js (r128) n'a pas pu être chargée depuis cdnjs.cloudflare.com : une connexion Internet est nécessaire à l'ouverture de cette page.</p></div></div>
  </main>
</div>

<script id="donnees" type="application/json">__DONNEES__</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script id="programme">
(function () {
  'use strict';
  var D = JSON.parse(document.getElementById('donnees').textContent);
  var $ = function (s) { return document.querySelector(s); };
  var CL = D.meta.classements, SY = D.meta.systemes;
  var COUCHES = { coque: 'Coque', couvercle: 'Couvercle', platine: 'Platine / pupitre', interne: 'Composants internes', mobile: 'Télécommande' };
  var S = { variante: 'A', etat: 'ouvert', couleur: 'classement', fantome: false,
            classes: { 'DOC': true, 'DÉD': true, 'HYP': true },
            couches: { coque: true, couvercle: true, platine: true, interne: true, mobile: true },
            sel: null, angle: 0, ecl: 0 };
  function esc(t) { return String(t == null ? '' : t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function fr(x, n) { return Number(x).toFixed(n == null ? 3 : n).replace('.', ','); }

  /* ---------- thème ---------- */
  var themes = ['auto', 'light', 'dark'], iTheme = 0;
  try { var th = localStorage.getItem('c204-theme'); if (themes.indexOf(th) > 0) iTheme = themes.indexOf(th); } catch (e) {}
  function appliquerTheme() {
    var t = themes[iTheme];
    if (t === 'auto') document.documentElement.removeAttribute('data-theme'); else document.documentElement.setAttribute('data-theme', t);
    $('#theme').textContent = 'Thème : ' + { auto: 'auto', light: 'clair', dark: 'sombre' }[t];
    try { localStorage.setItem('c204-theme', t); } catch (e) {}
    if (rendu) { majFond(); demander(); }
  }
  $('#theme').addEventListener('click', function () { iTheme = (iTheme + 1) % 3; appliquerTheme(); });

  /* ---------- panneau repliable (mobile) ---------- */
  $('#bascule-panneau').addEventListener('click', function () {
    var p = $('#panneau'), r = p.getAttribute('data-replie') === '1';
    p.setAttribute('data-replie', r ? '0' : '1'); this.setAttribute('aria-expanded', r ? 'true' : 'false');
    if (rendu) dimensionner();
  });

  var rendu = null;
  if (typeof THREE === 'undefined') { $('#erreur').hidden = false; appliquerTheme(); return; }

  /* ---------- scène ---------- */
  var toile = $('#toile');
  try {
    rendu = new THREE.WebGLRenderer({ canvas: toile, antialias: true, logarithmicDepthBuffer: true });
  } catch (e) {
    $('#erreur-texte').textContent = 'WebGL n\'est pas disponible dans ce navigateur : ' + e.message;
    $('#erreur').hidden = false; appliquerTheme(); return;
  }
  rendu.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(32, 1, 0.02, 200);
  camera.up.set(0, 0, 1);
  scene.add(camera);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8f99, 0.78));
  var phare = new THREE.DirectionalLight(0xffffff, 0.62); phare.position.set(-0.6, 0.9, 1.2); camera.add(phare);
  var appoint = new THREE.DirectionalLight(0xffffff, 0.22); appoint.position.set(0.8, -0.2, 0.6); camera.add(appoint);
  var matAretes = new THREE.LineBasicMaterial({ color: 0x0c0d10, transparent: true, opacity: 0.55 });
  var sol = new THREE.GridHelper(4, 40, 0x888888, 0x888888);
  sol.rotation.x = Math.PI / 2; sol.material.transparent = true; sol.material.opacity = 0.22; scene.add(sol);

  function majFond() {
    var c = getComputedStyle(document.documentElement).getPropertyValue('--scene').trim() || '#e9ebef';
    rendu.setClearColor(new THREE.Color(c), 1);
  }

  /* ---------- primitives three.js construites à partir du JSON ---------- */
  function geometrie(g) {
    var geo;
    switch (g.type) {
      case 'boite': geo = new THREE.BoxGeometry(g.dimensions[0], g.dimensions[1], g.dimensions[2]); break;
      case 'cylindre': geo = new THREE.CylinderGeometry(g.rayon, g.rayon, g.hauteur, 40); geo.rotateX(Math.PI / 2); break;
      case 'sphere': geo = new THREE.SphereGeometry(g.rayon, 30, 20); geo.rotateX(Math.PI / 2);
        if (g.echelle) geo.scale(g.echelle[0], g.echelle[1], g.echelle[2]); break;
      case 'tore': geo = new THREE.TorusGeometry(g.rayon_majeur, g.rayon_mineur, 12, 48); break;
      case 'prisme':
        var f = new THREE.Shape(g.profil.map(function (p) { return new THREE.Vector2(p[0], p[1]); }));
        (g.trous || []).forEach(function (t) { f.holes.push(new THREE.Path(t.map(function (p) { return new THREE.Vector2(p[0], p[1]); }))); });
        geo = new THREE.ExtrudeGeometry(f, { depth: g.hauteur, bevelEnabled: false, curveSegments: 1 });
        geo.translate(0, 0, -g.hauteur / 2); break;
      default: throw new Error('primitive inconnue : ' + g.type);
    }
    return geo;
  }

  var construits = {};
  function construire(cle) {
    if (construits[cle]) return construits[cle];
    var v = D.variantes[cle], grp = new THREE.Group(), objets = [];
    v.pieces.forEach(function (p) {
      var geo = geometrie(p.primitive);
      var mat = new THREE.MeshStandardMaterial({ roughness: 0.82, metalness: 0.04 });
      var mesh = new THREE.Mesh(geo, mat);
      mesh.position.fromArray(p.position); mesh.quaternion.fromArray(p.quaternion);
      var aretes = new THREE.LineSegments(new THREE.EdgesGeometry(geo, 28), matAretes);
      aretes.raycast = function () {};
      mesh.add(aretes);
      var porteur = new THREE.Group(); porteur.matrixAutoUpdate = false; porteur.add(mesh);
      var o = { p: p, mesh: mesh, porteur: porteur, mat: mat, aretes: aretes };
      mesh.userData.o = o; grp.add(porteur); objets.push(o);
    });
    grp.visible = false; scene.add(grp);
    construits[cle] = { grp: grp, objets: objets, v: v };
    return construits[cle];
  }
  function courant() { return construits[S.variante]; }

  /* ---------- état : ouverture du couvercle et éclatement ---------- */
  var mT = new THREE.Matrix4(), mR = new THREE.Matrix4(), mT2 = new THREE.Matrix4();
  function appliquerEtat() {
    var c = courant(), art = c.v.articulations.couvercle;
    c.objets.forEach(function (o) {
      var m = o.porteur.matrix.identity();
      if (art && o.p.liaison === 'couvercle' && S.angle !== 0) {
        var a = new THREE.Vector3().fromArray(art.axe).normalize();
        mT.makeTranslation(art.point[0], art.point[1], art.point[2]);
        mR.makeRotationAxis(a, S.angle * Math.PI / 180);
        mT2.makeTranslation(-art.point[0], -art.point[1], -art.point[2]);
        m.multiply(mT).multiply(mR).multiply(mT2);
      }
      if (S.ecl !== 0) { mT.makeTranslation(o.p.eclate[0] * S.ecl, o.p.eclate[1] * S.ecl, o.p.eclate[2] * S.ecl); m.premultiply(mT); }
      o.porteur.matrixWorldNeedsUpdate = true;
    });
  }

  /* ---------- couleurs, opacité, visibilité ---------- */
  function couleurPiece(p) {
    var a = new THREE.Color(p.couleur);
    if (S.couleur === 'aspect') return a;
    var b = new THREE.Color(S.couleur === 'classement' ? CL[p.classement].couleur : SY[p.systeme].couleur);
    var k = 0.62 + 0.55 * (0.2126 * a.r + 0.7152 * a.g + 0.0722 * a.b);
    return new THREE.Color(Math.min(1, b.r * k), Math.min(1, b.g * k), Math.min(1, b.b * k));
  }
  function visible(p) {
    if (!S.classes[p.classement] || !S.couches[p.couche]) return false;
    if (p.masque && p.masque.indexOf(S.etat) >= 0) return false;
    return true;
  }
  function appliquerAspect() {
    var c = courant();
    c.objets.forEach(function (o) {
      var p = o.p, op = p.opacite == null ? 1 : p.opacite;
      if (S.fantome && p.fantome) op = Math.min(op, 0.13);
      o.mat.color.copy(couleurPiece(p));
      o.mat.transparent = op < 0.999; o.mat.opacity = op; o.mat.depthWrite = op >= 0.999;
      o.mat.side = op < 0.999 ? THREE.DoubleSide : THREE.FrontSide;
      o.mesh.renderOrder = op < 0.999 ? 2 : 0;
      o.mat.emissive.setHex(S.sel === o ? 0x2a6cff : 0x000000);
      o.mat.emissiveIntensity = S.sel === o ? 0.55 : 0;
      o.mat.needsUpdate = true;
      o.mesh.visible = visible(p);
    });
    majLegende(); demander();
  }

  /* ---------- caméra orbitale (Z vers le haut) ---------- */
  var orb = { cible: new THREE.Vector3(0.6, 0.18, 0.2), r: 3.2, az: -0.6, el: 0.55 };
  function majCamera() {
    orb.el = Math.max(-1.553, Math.min(1.553, orb.el));
    orb.r = Math.max(0.08, Math.min(40, orb.r));
    var ce = Math.cos(orb.el);
    camera.position.set(orb.cible.x + orb.r * Math.sin(orb.az) * ce, orb.cible.y - orb.r * Math.cos(orb.az) * ce, orb.cible.z + orb.r * Math.sin(orb.el));
    camera.lookAt(orb.cible);
    demander();
  }
  function boiteVisible() {
    var b = new THREE.Box3(); scene.updateMatrixWorld(true);
    courant().objets.forEach(function (o) { if (o.mesh.visible) b.expandByObject(o.mesh); });
    return b;
  }
  function decalage() {      /* largeur masquée par le panneau de réglages (écran large) */
    var p = $('#panneau');
    if (window.innerWidth <= 760 || getComputedStyle(p).display === 'none') return 0;
    return p.offsetWidth + 12;
  }
  function cadrer() {
    var b = boiteVisible(); if (b.isEmpty()) return;
    var s = new THREE.Sphere(); b.getBoundingSphere(s);
    orb.cible.copy(s.center);
    var sc = $('#scene'), utile = Math.max(0.3, (sc.clientWidth - decalage()) / Math.max(sc.clientHeight, 1));
    var fv = camera.fov * Math.PI / 180, fh = 2 * Math.atan(Math.tan(fv / 2) * utile);
    orb.r = s.radius / Math.sin(Math.min(fv, fh) / 2) * 1.02;
    sol.position.set(s.center.x, s.center.y, Math.min(b.min.z, 0) - 0.001);
    majCamera();
  }
  var VUES = { iso: [-0.6, 0.55], dessus: [0, 1.553], face: [0, 0.0], cote: [-Math.PI / 2, 0.0] };

  /* ---------- boucle de rendu à la demande ---------- */
  var enAttente = false, anim = null;
  function demander() { if (!enAttente) { enAttente = true; requestAnimationFrame(image); } }
  function image(t) {
    enAttente = false;
    if (anim) {
      var k = Math.min(1, (t - anim.t0) / anim.duree); var e = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      S.angle = anim.a0 + (anim.a1 - anim.a0) * e; S.ecl = anim.e0 + (anim.e1 - anim.e0) * e;
      appliquerEtat();
      if (k >= 1) { anim = null; if (anim_cadre) { anim_cadre = false; cadrer(); } } else demander();
    }
    rendu.render(scene, camera);
  }
  var anim_cadre = false;
  function allerEtat(etat, immediat) {
    S.etat = etat;
    var e = courant().v.etats[etat];
    courant().objets.forEach(function (o) { o.mesh.visible = visible(o.p); });
    if (immediat) { S.angle = e.angle_couvercle_deg; S.ecl = e.eclate; appliquerEtat(); cadrer(); }
    else { anim = { t0: performance.now(), duree: 650, a0: S.angle, a1: e.angle_couvercle_deg, e0: S.ecl, e1: e.eclate }; anim_cadre = true; demander(); }
    majBoutons();
  }

  /* ---------- sélection et fiche ---------- */
  var rayon = new THREE.Raycaster(), souris = new THREE.Vector2();
  function viser(x, y) {
    var r = toile.getBoundingClientRect();
    souris.set((x - r.left) / r.width * 2 - 1, -(y - r.top) / r.height * 2 + 1);
    rayon.setFromCamera(souris, camera);
    var cibles = courant().objets.filter(function (o) { return o.mesh.visible; }).map(function (o) { return o.mesh; });
    var touches = rayon.intersectObjects(cibles, false);
    if (!touches.length) return null;
    if (S.fantome) { for (var i = 0; i < touches.length; i++) { if (!touches[i].object.userData.o.p.fantome) return touches[i].object.userData.o; } }
    for (var j = 0; j < touches.length; j++) { var o = touches[j].object.userData.o; if ((o.p.opacite == null ? 1 : o.p.opacite) > 0.5 || j === touches.length - 1) return o; }
    return touches[0].object.userData.o;
  }
  function decrirePrimitive(g) {
    var mm = function (v) { return Math.round(v * 1000); };
    switch (g.type) {
      case 'boite': return 'Boîte ' + g.dimensions.map(mm).join(' × ') + ' mm';
      case 'cylindre': return 'Cylindre Ø ' + mm(2 * g.rayon) + ' × ' + mm(g.hauteur) + ' mm';
      case 'sphere': return (g.echelle ? 'Ellipsoïde, rayon de base ' : 'Sphère Ø ') + mm((g.echelle ? 1 : 2) * g.rayon) + ' mm';
      case 'tore': return 'Tore Ø moyen ' + mm(2 * g.rayon_majeur) + ' mm, fil Ø ' + mm(2 * g.rayon_mineur) + ' mm';
      case 'prisme': return 'Prisme extrudé, ' + g.profil.length + ' sommets' + (g.trous ? ', ' + g.trous.length + ' trou(s)' : '') + ', épaisseur ' + (g.hauteur * 1000).toFixed(1).replace('.', ',') + ' mm';
    }
    return g.type;
  }
  function selectionner(o) {
    S.sel = o; appliquerAspect();
    var f = $('#fiche');
    if (!o) { f.hidden = true; f.innerHTML = ''; return; }
    var p = o.p, c = CL[p.classement];
    f.innerHTML = '<button class="fermer" type="button" aria-label="Fermer la fiche">×</button>' +
      '<h3>' + esc(p.nom) + '</h3>' +
      '<span class="badge"><i class="pastille" style="background:' + c.couleur + '"></i>[' + esc(p.classement) + '] ' + esc(c.libelle) + '</span>' +
      '<span class="badge">Existence : ' + esc(p.existence) + '</span>' +
      '<dl>' +
      '<dt>Repère d\'origine</dt><dd>' + esc(p.repere) + '</dd>' +
      '<dt>Document source</dt><dd>' + esc(p.source) + (p.appui ? '<br><small>Appui : ' + esc(p.appui) + '</small>' : '') + '</dd>' +
      '<dt>Fonction revendiquée</dt><dd>' + esc(p.fonction_revendiquee) + '<br><small>Telle que la donnent les légendes ou le texte : ni vérifiée, ni physiquement établie.</small></dd>' +
      '<dt>Classement</dt><dd>' + esc(c.definition) + '</dd>' +
      '<dt>Système · ensemble</dt><dd>' + esc(SY[p.systeme].libelle) + ' · ' + esc(p.ensemble) + '</dd>' +
      '<dt>Primitive (échelle hypothétique)</dt><dd>' + esc(decrirePrimitive(p.primitive)) + '<br><small>Centre : x ' + fr(p.position[0]) + ' · y ' + fr(p.position[1]) + ' · z ' + fr(p.position[2]) + ' m (couvercle fermé) — ' + esc(p.id) + '</small></dd>' +
      (p.notes ? '<dt>Notes</dt><dd>' + esc(p.notes) + '</dd>' : '') + '</dl>';
    f.hidden = false; f.scrollTop = 0;
    f.querySelector('.fermer').addEventListener('click', function () { selectionner(null); });
  }

  /* ---------- interactions pointeur ---------- */
  var ptrs = {}, nPtr = 0, deplace = 0, dernier = null, pince = null;
  toile.addEventListener('contextmenu', function (e) { e.preventDefault(); });
  toile.addEventListener('pointerdown', function (e) {
    try { toile.setPointerCapture(e.pointerId); } catch (err) {}
    ptrs[e.pointerId] = { x: e.clientX, y: e.clientY }; nPtr = Object.keys(ptrs).length;
    deplace = 0; dernier = { x: e.clientX, y: e.clientY, bouton: e.button, maj: e.shiftKey || e.ctrlKey || e.metaKey }; pince = null;
    toile.classList.add('saisie'); $('#bulle').hidden = true;
  });
  toile.addEventListener('pointermove', function (e) {
    if (!ptrs[e.pointerId]) { survol(e); return; }
    var p = ptrs[e.pointerId], dx = e.clientX - p.x, dy = e.clientY - p.y; p.x = e.clientX; p.y = e.clientY;
    deplace += Math.abs(dx) + Math.abs(dy);
    var ids = Object.keys(ptrs);
    if (ids.length >= 2) {
      var a = ptrs[ids[0]], b = ptrs[ids[1]], d = Math.hypot(a.x - b.x, a.y - b.y), mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
      if (pince) { orb.r *= pince.d / Math.max(d, 1); panoramique(mx - pince.mx, my - pince.my); }
      pince = { d: d, mx: mx, my: my }; majCamera(); return;
    }
    if (dernier && (dernier.bouton === 2 || dernier.bouton === 1 || dernier.maj)) panoramique(dx, dy);
    else { orb.az -= dx * 0.0065; orb.el += dy * 0.0065; }
    majCamera();
  });
  function fin(e) {
    if (!ptrs[e.pointerId]) return;
    delete ptrs[e.pointerId]; nPtr = Object.keys(ptrs).length; pince = null;
    if (nPtr === 0) {
      toile.classList.remove('saisie');
      if (e.type === 'pointerup' && deplace < 6 && dernier && dernier.bouton === 0) selectionner(viser(e.clientX, e.clientY));
    }
  }
  toile.addEventListener('pointerup', fin); toile.addEventListener('pointercancel', fin);
  toile.addEventListener('wheel', function (e) { e.preventDefault(); orb.r *= Math.exp((e.deltaMode === 1 ? e.deltaY * 16 : e.deltaY) * 0.0012); majCamera(); }, { passive: false });
  toile.addEventListener('keydown', function (e) {
    var k = e.key, f = true;
    if (k === 'ArrowLeft') orb.az += 0.08; else if (k === 'ArrowRight') orb.az -= 0.08; else if (k === 'ArrowUp') orb.el += 0.06; else if (k === 'ArrowDown') orb.el -= 0.06;
    else if (k === '+' || k === '=') orb.r *= 0.9; else if (k === '-') orb.r *= 1.1; else if (k === 'Escape') selectionner(null); else f = false;
    if (f) { e.preventDefault(); majCamera(); }
  });
  function panoramique(dx, dy) {
    var h = toile.clientHeight || 1, ech = 2 * orb.r * Math.tan(camera.fov * Math.PI / 360) / h;
    var d = new THREE.Vector3(), haut = new THREE.Vector3();
    d.setFromMatrixColumn(camera.matrix, 0); haut.setFromMatrixColumn(camera.matrix, 1);
    orb.cible.addScaledVector(d, -dx * ech).addScaledVector(haut, dy * ech);
  }
  var survolPrevu = false, dernierSurvol = null;
  function survol(e) {
    if (e.pointerType !== 'mouse') return;
    dernierSurvol = { x: e.clientX, y: e.clientY };
    if (survolPrevu) return; survolPrevu = true;
    requestAnimationFrame(function () {
      survolPrevu = false; var o = viser(dernierSurvol.x, dernierSurvol.y), b = $('#bulle');
      if (!o) { b.hidden = true; toile.style.cursor = ''; return; }
      var r = $('main').getBoundingClientRect();
      b.textContent = '[' + o.p.classement + '] ' + o.p.nom; b.style.left = (dernierSurvol.x - r.left) + 'px'; b.style.top = (dernierSurvol.y - r.top) + 'px'; b.hidden = false;
      toile.style.cursor = 'pointer';
    });
  }
  toile.addEventListener('pointerleave', function () { $('#bulle').hidden = true; });

  /* ---------- interface ---------- */
  function majBoutons() {
    document.querySelectorAll('#g-variante button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.v === S.variante); });
    document.querySelectorAll('#g-etat button').forEach(function (b) {
      b.setAttribute('aria-pressed', b.dataset.e === S.etat);
      b.disabled = S.variante === 'B' && (b.dataset.e === 'ferme' || b.dataset.e === 'a_plat');
      if (b.dataset.e === 'ouvert') b.textContent = S.variante === 'B' ? 'Assemblé' : 'Ouvert';
    });
    document.querySelectorAll('#g-couleur button').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.c === S.couleur); });
  }
  function majLegende() {
    var v = courant().v, h = '';
    if (S.couleur === 'classement') {
      Object.keys(CL).forEach(function (k) { h += '<span><i class="pastille" style="background:' + CL[k].couleur + '"></i>[' + k + '] ' + esc(CL[k].libelle) + ' — ' + (v.bilan_classement[k] || 0) + '</span>'; });
    } else if (S.couleur === 'systeme') {
      var vus = {}; v.pieces.forEach(function (p) { vus[p.systeme] = 1; });
      Object.keys(SY).forEach(function (k) { if (vus[k]) h += '<span><i class="pastille" style="background:' + SY[k].couleur + '"></i>' + esc(SY[k].libelle) + '</span>'; });
    } else {
      h = '<span>Aspect : teintes relevées sur les photos (coque sombre, bandes jaune et noir, étiquette orange) ; neutres ailleurs.</span>';
    }
    $('#legende').innerHTML = h;
  }
  function majCompteurs() {
    var v = courant().v, n = {}, nc = {};
    v.pieces.forEach(function (p) { n[p.classement] = (n[p.classement] || 0) + 1; nc[p.couche] = (nc[p.couche] || 0) + 1; });
    var h = '';
    Object.keys(CL).forEach(function (k) {
      h += '<label class="coche"><input type="checkbox" data-cl="' + k + '"' + (S.classes[k] ? ' checked' : '') + '><i class="pastille" style="background:' + CL[k].couleur + '"></i>[' + k + '] ' + esc(CL[k].libelle) + '<span class="compte">' + (n[k] || 0) + '</span></label>';
    });
    $('#g-classes').innerHTML = h;
    h = '';
    Object.keys(COUCHES).forEach(function (k) {
      if (!nc[k]) return;
      h += '<label class="coche"><input type="checkbox" data-co="' + k + '"' + (S.couches[k] ? ' checked' : '') + '>' + COUCHES[k] + '<span class="compte">' + nc[k] + '</span></label>';
    });
    $('#g-couches').innerHTML = h;
    $('#desc-variante').textContent = v.description;
  }
  function majListe() {
    var q = $('#recherche').value.trim().toLowerCase(), h = '', n = 0;
    courant().objets.forEach(function (o, i) {
      var p = o.p, t = (p.nom + ' ' + p.repere + ' ' + p.source + ' ' + p.ensemble + ' ' + p.classement).toLowerCase();
      if (q && t.indexOf(q) < 0) return; n++;
      h += '<li><button type="button" data-i="' + i + '"><i class="pastille" style="background:' + CL[p.classement].couleur + '"></i>' + esc(p.nom) + '</button></li>';
    });
    $('#liste').innerHTML = h || '<li><button type="button" disabled>Aucune pièce</button></li>';
  }
  $('#recherche').addEventListener('input', majListe);
  $('#liste').addEventListener('click', function (e) { var b = e.target.closest('button[data-i]'); if (b) selectionner(courant().objets[+b.dataset.i]); });
  $('#g-classes').addEventListener('change', function (e) { var k = e.target.dataset.cl; if (k) { S.classes[k] = e.target.checked; appliquerAspect(); } });
  $('#g-couches').addEventListener('change', function (e) { var k = e.target.dataset.co; if (k) { S.couches[k] = e.target.checked; appliquerAspect(); } });
  $('#fantome').addEventListener('change', function (e) { S.fantome = e.target.checked; appliquerAspect(); });
  $('#g-couleur').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) { S.couleur = b.dataset.c; majBoutons(); appliquerAspect(); } });
  $('#g-etat').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b && !b.disabled) { allerEtat(b.dataset.e, false); appliquerAspect(); } });
  $('#g-vue').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.vue !== 'cadrer') { orb.az = VUES[b.dataset.vue][0]; orb.el = VUES[b.dataset.vue][1]; }
    cadrer();
  });
  $('#g-variante').addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) choisirVariante(b.dataset.v); });
  function choisirVariante(cle) {
    if (construits[S.variante]) construits[S.variante].grp.visible = false;
    S.variante = cle; S.sel = null; $('#fiche').hidden = true;
    construire(cle).grp.visible = true;
    if (cle === 'B' && (S.etat === 'ferme' || S.etat === 'a_plat')) S.etat = 'ouvert';
    majCompteurs(); majListe(); allerEtat(S.etat, true); appliquerAspect(); majBoutons();
  }

  /* ---------- dimensionnement ---------- */
  function dimensionner() {
    var c = $('#scene'), w = c.clientWidth, h = c.clientHeight; if (!w || !h) return;
    rendu.setSize(w, h, false); camera.aspect = w / h;
    var d = decalage();
    if (d > 0) camera.setViewOffset(w, h, -d / 2, 0, w, h); else camera.clearViewOffset();
    camera.updateProjectionMatrix(); demander();
  }
  if (window.ResizeObserver) new ResizeObserver(dimensionner).observe($('#scene')); else window.addEventListener('resize', dimensionner);
  if (window.matchMedia) { var mq = window.matchMedia('(prefers-color-scheme: dark)'); var surTheme = function () { majFond(); demander(); }; if (mq.addEventListener) mq.addEventListener('change', surTheme); else if (mq.addListener) mq.addListener(surTheme); }

  /* ---------- démarrage ---------- */
  if (window.innerWidth > 760) { $('#panneau').setAttribute('data-replie', '0'); }
  appliquerTheme(); majFond(); dimensionner();
  choisirVariante('A');
  window.C204 = { etat: S, donnees: D, scene: scene, camera: camera, cadrer: cadrer, choisirVariante: choisirVariante, allerEtat: allerEtat, selectionner: selectionner, courant: courant };
})();
</script>
</body>
</html>
"""


def main():
    modele = json.loads((ICI / "modele_c204.json").read_text(encoding="utf-8"))
    donnees = json.dumps(donnees_embarquees(modele), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    _Lp = json.loads((ICI / "parametres.json").read_text(encoding="utf-8"))["echelle"]["L"]
    _ech = ("%.2f m ± %.2f m" % (_Lp["valeur"], _Lp["incertitude"])).replace(".", ",")
    html = GABARIT.replace("__ECHELLE__", _ech).replace("__DONNEES__", donnees).replace("__AVERT__", modele["meta"]["avertissement"].replace('"', "&quot;"))
    (ICI / "visionneuse.html").write_text(html, encoding="utf-8")
    print("écrit : visionneuse.html (%.0f ko, %d pièces embarquées)" % (len(html.encode("utf-8")) / 1024, sum(len(v["pieces"]) for v in modele["variantes"].values())))


if __name__ == "__main__":
    main()
