// Équipe E — Programme C204 — essais de simulateur.html dans Chrome sans tête, piloté par le protocole DevTools
// (clics, glissements, molette, pincement à deux doigts et touches réels ; aucune dépendance : Node 22 ou plus récent).
//
//   node essais_simulateur.mjs [dossier des captures] [bureau|mobile|special|langue|visionneuse|tout]
//
// Profils : « bureau » 1280×800 à la souris, « mobile » 375×812 tactile (densité 2), « special » : thème sombre du
// système, mouvement réduit, CDN de three.js bloqué ; « langue » : bascule français / anglais dans les quatre modes aux
// deux tailles, ouverture par #lang=en, persistance, et contrôle qu'aucun texte français ne subsiste en anglais (ni
// l'inverse) ; « visionneuse » : bandeau bilingue de visionneuse.html. Sans dossier indiqué, les captures vont dans un
// dossier temporaire.
// Chrome est cherché à l'emplacement habituel de macOS ; sinon, donner son chemin dans la variable CHROME.
// Chaque séance relance un Chrome neuf et dure moins de 25 s (le Chrome sans tête utilisé s'arrêtait seul après ~31 s).
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const SP = mkdtempSync(join(tmpdir(), 'c204-essais-'));
const PAGE = pathToFileURL(join(dirname(fileURLToPath(import.meta.url)), 'simulateur.html')).href;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const OUT = process.argv[2] || join(SP, 'captures');
const QUOI = process.argv[3] || 'tout';
mkdirSync(OUT, { recursive: true });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

let chrome = null, ws = null, idc = 0, tLance = 0;
const attente = new Map(); const journal = { console: [], exceptions: [], requetes: [], echecs: [] };
const send = (method, params = {}) => new Promise((r, j) => { const id = ++idc; attente.set(id, { r, j }); ws.send(JSON.stringify({ id, method, params })); });
async function arreter() { if (ws) { ws.onclose = null; try { ws.close(); } catch (e) {} ws = null; } if (chrome) { chrome.removeAllListeners('exit'); chrome.kill(); chrome = null; await sleep(350); } }
async function demarrer() {
  await arreter();
  const port = 9333 + Math.floor(Math.random() * 400);
  chrome = spawn(CHROME, [
    '--headless=new', `--user-data-dir=${SP}/chrome-profil-cdp`, '--no-first-run', '--no-default-browser-check', '--disable-extensions',
    '--hide-scrollbars', '--enable-unsafe-swiftshader', `--remote-debugging-port=${port}`, '--window-size=1280,800', 'about:blank'], { stdio: 'ignore' });
  tLance = Date.now();
  chrome.on('exit', (c) => console.log('      (Chrome s\'est arrêté de lui-même après ' + ((Date.now() - tLance) / 1000).toFixed(1) + ' s)'));
  let cible = null;
  for (let i = 0; i < 60 && !cible; i++) { await sleep(200); try { const L = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); cible = L.find((t) => t.type === 'page'); } catch (e) {} }
  if (!cible) throw new Error('Chrome ne répond pas');
  ws = new WebSocket(cible.webSocketDebuggerUrl);
  await new Promise((r, j) => { ws.onopen = r; ws.onerror = j; });
  ws.onclose = () => { attente.forEach(({ j }) => j(new Error('connexion à Chrome perdue'))); attente.clear(); };
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && attente.has(m.id)) { const { r, j } = attente.get(m.id); attente.delete(m.id); if (m.error) j(new Error(m.error.message)); else r(m.result); return; }
    if (m.method === 'Runtime.consoleAPICalled') journal.console.push(m.params.type + ': ' + m.params.args.map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300));
    if (m.method === 'Runtime.exceptionThrown') journal.exceptions.push((m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text || '').slice(0, 400));
    if (m.method === 'Log.entryAdded') journal.console.push('log.' + m.params.entry.level + ': ' + m.params.entry.text.slice(0, 300));
    if (m.method === 'Network.requestWillBeSent') { const u = m.params.request.url; if (!u.startsWith('data:')) journal.requetes.push(u.length > 120 ? u.slice(0, 120) + '…' : u); }
    if (m.method === 'Network.loadingFailed') journal.echecs.push(m.params.errorText + (m.params.blockedReason ? ' (' + m.params.blockedReason + ')' : ''));
  };
  await send('Runtime.enable'); await send('Page.enable'); await send('Log.enable'); await send('Network.enable');
}
// une « séance » = un Chrome neuf, réglé sur le profil d'écran, ouvert sur la page avec le lien profond voulu (chaque séance dure moins de 25 s)
async function seance(prof, hash, media = {}) {
  await demarrer();
  await send('Emulation.setDeviceMetricsOverride', { width: prof.w, height: prof.h, deviceScaleFactor: prof.dsf, mobile: prof.mobile });
  await send('Emulation.setTouchEmulationEnabled', { enabled: prof.mobile, maxTouchPoints: prof.mobile ? 5 : 1 });
  await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-color-scheme', value: media.sombre ? 'dark' : 'light' }, { name: 'prefers-reduced-motion', value: media.reduit ? 'reduce' : 'no-preference' }] });
  if (media.bloquer) { await send('Network.setCacheDisabled', { cacheDisabled: true }); await send('Network.setBlockedURLs', { urls: media.bloquer }); }
  TACTILE = prof.mobile;
  await charger(hash);
}

async function js(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
  if (r.exceptionDetails) throw new Error('JS : ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text) + '\n  dans : ' + expr.slice(0, 200));
  return r.result.value;
}
async function capture(nom) { const r = await send('Page.captureScreenshot', { format: 'png' }); writeFileSync(`${OUT}/${nom}.png`, Buffer.from(r.data, 'base64')); return `${OUT}/${nom}.png`; }
// « - » : adresse nue (sans fragment) ; sinon, la langue française est imposée quand le fragment n'en donne pas (les essais historiques lisent du français)
async function charger(hash = '') {
  if (hash === '-') hash = ''; else if (!/(^|&)lang=/.test(hash)) hash = (hash ? hash + '&' : '') + 'lang=fr';
  await send('Page.navigate', { url: 'about:blank' }); await sleep(150);
  await send('Page.navigate', { url: PAGE + (hash ? '#' + hash : '') });
  for (let i = 0; i < 80; i++) { await sleep(150); if (await js('document.readyState === "complete" && (typeof window.C204SIM === "object")').catch(() => false)) break; }
  await sleep(500);
}
const resultats = [];
const T0 = Date.now();
function noter(profil, nom, ok, detail = '') { resultats.push({ profil, nom, ok: !!ok, detail: String(detail) }); console.log(`${ok ? 'OK    ' : 'ÉCHEC '} ${((Date.now() - T0) / 1000).toFixed(1).padStart(5)} s [${profil}] ${nom}${detail !== '' ? ' — ' + detail : ''}`); }

// ------------------------------------------------------------------ entrées réelles
let TACTILE = false;
async function rect(sel) {
  return js(`(function(){var e=document.querySelector(${JSON.stringify(sel)}); if(!e) return null; if(e.closest('#panneaux')) e.scrollIntoView({block:'center'}); var r=e.getBoundingClientRect(); return {x:r.left,y:r.top,w:r.width,h:r.height};})()`);
}
async function pointer(x, y) {
  if (TACTILE) {
    await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x, y, id: 1 }] }); await sleep(40);
    await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  } else {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x, y });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 }); await sleep(30);
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
  }
  await sleep(120);
}
async function cliquer(sel) { const r = await rect(sel); if (!r) throw new Error('introuvable : ' + sel); await sleep(60); await pointer(r.x + r.w / 2, r.y + r.h / 2); return r; }
async function glisser(x0, y0, x1, y1, pas = 12) {
  if (TACTILE) {
    await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: x0, y: y0, id: 1 }] });
    for (let i = 1; i <= pas; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: x0 + (x1 - x0) * i / pas, y: y0 + (y1 - y0) * i / pas, id: 1 }] }); await sleep(12); }
    await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] });
  } else {
    await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0, y: y0 });
    await send('Input.dispatchMouseEvent', { type: 'mousePressed', x: x0, y: y0, button: 'left', clickCount: 1 });
    for (let i = 1; i <= pas; i++) { await send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: x0 + (x1 - x0) * i / pas, y: y0 + (y1 - y0) * i / pas, button: 'left', buttons: 1 }); await sleep(12); }
    await send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: x1, y: y1, button: 'left', clickCount: 1 });
  }
  await sleep(150);
}
// amène un curseur <input type=range> à la fraction voulue en le faisant glisser réellement
async function curseur(sel, fraction) {
  const r = await rect(sel); await sleep(60);
  const f0 = await js(`(function(){var e=document.querySelector(${JSON.stringify(sel)}); return (e.value-e.min)/(e.max-e.min);})()`);
  const m = 9, x0 = r.x + m + (r.w - 2 * m) * f0, x1 = r.x + m + (r.w - 2 * m) * fraction, y = r.y + r.h / 2;
  await glisser(x0, y, x1, y, 14);
  return js(`+document.querySelector(${JSON.stringify(sel)}).value`);
}
async function touche(key, code, n = 1, keyCode = 0) {
  const text = key === 'Enter' ? '\r' : (key === ' ' ? ' ' : undefined);      // Entrée et Espace doivent produire un caractère pour activer un bouton
  for (let i = 0; i < n; i++) { await send('Input.dispatchKeyEvent', { type: 'keyDown', key, code, text, windowsVirtualKeyCode: keyCode, nativeVirtualKeyCode: keyCode }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key, code, windowsVirtualKeyCode: keyCode, nativeVirtualKeyCode: keyCode }); await sleep(25); }
  await sleep(80);
}
const S = (chemin) => js(`(function(){var s=window.C204SIM.etat; return ${chemin};})()`);
const texte = (sel) => js(`(function(){var e=document.querySelector(${JSON.stringify(sel)}); return e ? e.textContent.trim() : null;})()`);
const CHEVAUCHEMENTS = `(function(){
  var vis=[].slice.call(document.querySelectorAll('.etq')).filter(function(e){return e.style.display!=='none';}).map(function(e){return {t:e.textContent,r:e.getBoundingClientRect(),tronque:e.scrollWidth>e.clientWidth+1};});
  var vue=document.getElementById('vue').getBoundingClientRect(), pb=[];
  (function(){var cam=C204SIM.camera(), tl=document.getElementById('toile'), w=tl.clientWidth, h=tl.clientHeight; cam.updateMatrixWorld(true);
    C204SIM.etiquettes().forEach(function(e){ if(!e.vis) return; var p=e.cible(); if(!p) return; var v=p.clone().project(cam), x=(v.x+1)/2*w, y=(1-v.y)/2*h, dx=Math.abs(x-parseFloat(e.ln.getAttribute('x2'))), dy=Math.abs(y-parseFloat(e.ln.getAttribute('y2'))); if(dx>2||dy>2) pb.push('trait décalé de sa cible : '+e.long+' ('+Math.round(dx)+', '+Math.round(dy)+' px)'); });})();
  function croise(a,b){return a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1;}
  for(var i=0;i<vis.length;i++){var a=vis[i].r; if(a.left<vue.left-0.5||a.right>vue.right+0.5||a.top<vue.top-0.5||a.bottom>vue.bottom+0.5) pb.push('hors cadre : '+vis[i].t); if(vis[i].tronque) pb.push('tronquée : '+vis[i].t);
    for(var j=i+1;j<vis.length;j++) if(croise(a,vis[j].r)) pb.push(vis[i].t+' × '+vis[j].t);}
  ['hud','sous-titre'].forEach(function(id){var el=document.getElementById(id); if(el.hidden) return; var K=id==='hud'?[].slice.call(el.children):[el];
    K.forEach(function(k){var b=k.getBoundingClientRect(); vis.forEach(function(v){ if(croise(v.r,b)) pb.push(v.t+' × #'+id); });});});
  var hud=document.getElementById('hud'), st=document.getElementById('sous-titre');
  if(!hud.hidden&&!st.hidden&&hud.children.length){var hb=hud.getBoundingClientRect(), sb=st.getBoundingClientRect(); if(croise(hb,sb)) pb.push('#hud × #sous-titre');}
  return {n:vis.length,pb:pb};})()`;
const DEBORDEMENTS = `(function(){
  var pb=[]; if(document.documentElement.scrollWidth>window.innerWidth+1) pb.push('page plus large que la fenêtre : '+document.documentElement.scrollWidth);
  var pan=document.getElementById('panneaux'); if(pan.scrollWidth>pan.clientWidth+1) pb.push('panneau : défilement horizontal '+pan.scrollWidth+' > '+pan.clientWidth);
  [].slice.call(document.querySelectorAll('#panneaux [role=tabpanel]:not([hidden]) *, header *, #bandeau, #onglets button')).forEach(function(e){
    if(e.tagName==='INPUT'||e.tagName==='SELECT'||e.tagName==='OPTION'||e.closest('details:not([open])')&&e.tagName!=='SUMMARY') return; var cs=getComputedStyle(e); if(cs.display==='none'||cs.position==='absolute') return;
    if(e.scrollWidth>e.clientWidth+2&&cs.overflow==='visible'&&e.clientWidth>0&&cs.display!=='inline') pb.push((e.id||e.className||e.tagName)+' : '+e.scrollWidth+' > '+e.clientWidth+' « '+e.textContent.trim().slice(0,40)+' »');});
  var on=document.getElementById('onglets'); return {pb:pb, ongletsDefilent:on.scrollWidth>on.clientWidth+1};})()`;

const proche = (a, b, tol) => Math.abs(a - b) <= tol * Math.abs(b);

// ------------------------------------------------------------------ contrôle de langue
// Rassemble tout le texte que voit ou entend le lecteur : texte affiché, titre de la page, options des listes, étiquettes 3D,
// attributs aria-label / title / alt / placeholder. Les éléments marqués lang="fr" ou lang="en" (boutons de langue) sont exclus.
const TEXTES = `(function(autre){
  var T=[document.title, (document.querySelector('meta[name=description]')||{content:''}).content];
  var clone=function(){ var out=[]; (function va(n){ if(n.nodeType===3){ out.push(n.nodeValue); return; } if(n.nodeType!==1) return; if(n.getAttribute('lang')===autre||n.tagName==='SCRIPT'||n.tagName==='STYLE'||n.tagName==='NOSCRIPT') return;
      var cs=getComputedStyle(n); if(cs.display==='none') return; for(var c=n.firstChild;c;c=c.nextSibling) va(c); })(document.body); return out.join(' '); };
  T.push(clone());
  [].forEach.call(document.querySelectorAll('option'),function(o){T.push(o.textContent);});
  [].forEach.call(document.querySelectorAll('[aria-label],[title],[alt],[placeholder]'),function(e){ if(e.closest('[lang="'+autre+'"]')) return; ['aria-label','title','alt','placeholder'].forEach(function(a){ if(e.hasAttribute(a)) T.push(e.getAttribute(a)); }); });
  return T.join(' \\n ');})`;
// en mode anglais : aucun caractère accentué français, aucun mot français courant
const MOTS_FR = 'le|la|les|des|du|de|un|une|et|est|sont|dans|pour|avec|sur|au|aux|ce|cette|ces|qui|que|ne|pas|par|ou|selon|vers|sans|sous|entre|chaque|deux|trois|quatre|heure|heures|ans|fois|vue|lecture|puissance|masse|trajet|horloge|horloges|calculateur|calculateurs|panne|couvercle|platine|coffre|soit|aucun|aucune|moins|texte|voir|dessus|taux|bruit|champ|temps|corps|logement|logements|bobine|carter|bande|raie|paroi|fond|rayon|sol|poche|anneau|seul|seule';
const SCAN_FR = `(function(){ var t=${TEXTES}('fr'), pb=[], m;
  var acc=/[àâäçéèêëîïôöùûüÿœæÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸŒÆ«»]/g; while((m=acc.exec(t))&&pb.length<10) pb.push('accent ou guillemet français « '+t.slice(Math.max(0,m.index-22),m.index+22).replace(/\\s+/g,' ')+' »');
  var mots=new RegExp('(^|[^A-Za-z0-9_/.\\\\-])(${MOTS_FR})(?![A-Za-z0-9_\\\\-])','gi'); while((m=mots.exec(t))&&pb.length<20) pb.push('mot français « '+t.slice(Math.max(0,m.index-22),m.index+26).replace(/\\s+/g,' ')+' »');
  return {longueur:t.length, pb:pb};})()`;
// en mode français : aucun mot-outil anglais (les légendes d'origine citées, en anglais, n'en contiennent pas)
const SCAN_EN = `(function(){ var t=${TEXTES}('en'), pb=[], m;
  var mots=/(^|[^A-Za-z0-9_\\/.\\-])(the|and|of|is|are|with|from|this|that|by|for|to|story|according|click|drag|wheel|stated|shown)(?![A-Za-z0-9_\\-])/gi; while((m=mots.exec(t))&&pb.length<12) pb.push('mot anglais « '+t.slice(Math.max(0,m.index-22),m.index+26).replace(/\\s+/g,' ')+' »');
  return {longueur:t.length, pb:pb};})()`;
const regler = (sel, v) => js(`(function(){var e=document.querySelector(${JSON.stringify(sel)}); e.value=${JSON.stringify(String(v))}; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));})()`);

// visionneuse.html reste en français : bandeau bilingue renvoyant au simulateur en anglais
async function essaisVisionneuse() {
  const profil = 'visionneuse', PAGE_V = PAGE.replace('simulateur.html', 'visionneuse.html');
  for (const prof of [{ w: 1280, h: 800, dsf: 1, mobile: false }, { w: 375, h: 812, dsf: 2, mobile: true }]) {
    journal.console.length = 0; journal.exceptions.length = 0; journal.echecs.length = 0;
    await demarrer();
    await send('Emulation.setDeviceMetricsOverride', { width: prof.w, height: prof.h, deviceScaleFactor: prof.dsf, mobile: prof.mobile });
    await send('Emulation.setTouchEmulationEnabled', { enabled: prof.mobile, maxTouchPoints: prof.mobile ? 5 : 1 });
    TACTILE = prof.mobile;
    await send('Page.navigate', { url: PAGE_V }); await sleep(2500);
    const v = await js(`(function(){var n=document.getElementById('note-langue'), r=n.getBoundingClientRect(), c=document.getElementById('toile'), a=n.querySelector('[lang=en] a'); return {texte:n.innerText, haut:Math.round(r.height), visible:r.height>0&&r.top>=0&&r.bottom<=innerHeight&&r.right<=innerWidth+1, lien:a.getAttribute('href'), toile:[c.clientWidth,c.clientHeight], modele: typeof window.C204, large:document.documentElement.scrollWidth<=innerWidth+1, deborde:n.scrollWidth>n.clientWidth+1};})()`);
    noter(profil, `${prof.w} px : bandeau bilingue visible, vue 3D intacte`, v.visible && v.lien === 'simulateur.html#lang=en' && v.toile[0] > 200 && v.toile[1] > 200 && v.modele === 'object' && v.large && !v.deborde && /This page is in French/.test(v.texte) && journal.exceptions.length === 0,
      `${v.texte.replace(/\s+/g, ' ')} | hauteur ${v.haut} px | toile ${v.toile.join('×')} | exceptions ${journal.exceptions.length}`);
    await capture(`visionneuse_bandeau_${prof.w}`);
    await cliquer('#note-langue [lang=en] a'); await sleep(2500);
    const s = await js('({sim: typeof window.C204SIM, lang: window.C204SIM ? C204SIM.langue() : null, titre: document.title})');
    noter(profil, `${prof.w} px : le lien ouvre le simulateur en anglais`, s.sim === 'object' && s.lang === 'en' && s.titre === 'C204 — 3D simulator', s.titre);
    await js('try{localStorage.removeItem("c204-lang")}catch(e){}');
  }
}

async function essaisLangue(profil, w, h, dsf, mobile) {
  const prof = { w, h, dsf, mobile }, P = (n, ok, d) => noter(profil, n, ok, d), suf = mobile ? '375_' : '';
  journal.console.length = 0; journal.exceptions.length = 0; journal.echecs.length = 0;
  const etatLangue = () => js(`({lang:C204SIM.langue(), html:document.documentElement.lang, titre:document.title, bandeau:document.getElementById('bandeau').textContent, hash:location.hash, fr:document.querySelector('#langue [data-lang=fr]').getAttribute('aria-pressed'), en:document.querySelector('#langue [data-lang=en]').getAttribute('aria-pressed')})`);
  const controleAnglais = async (nom) => { const s = await js(SCAN_FR), db = await js(DEBORDEMENTS), ch = await js(CHEVAUCHEMENTS);
    P(`anglais, ${nom} : aucun texte français`, s.pb.length === 0 && s.longueur > 500, `${s.longueur} caractères examinés ${s.pb.join(' | ')}`);
    P(`anglais, ${nom} : ni débordement de texte ni chevauchement d'étiquettes`, db.pb.length === 0 && ch.pb.length === 0 && !db.ongletsDefilent, db.pb.concat(ch.pb).join(' | ') + (db.ongletsDefilent ? ' onglets défilants' : '')); };
  const controleFrancais = async (nom) => { const s = await js(SCAN_EN); P(`français, ${nom} : aucun texte anglais hors légendes d'origine`, s.pb.length === 0 && s.longueur > 500, `${s.longueur} caractères examinés ${s.pb.join(' | ')}`); };

  // ----- ouverture directe en anglais dans un mode donné
  await seance(prof, 'mode=physique&lang=en');
  let e = await etatLangue();
  P('ouverture directe avec #mode=physique&lang=en', e.lang === 'en' && e.html === 'en' && e.titre === 'C204 — 3D simulator' && (await S('s.mode')) === 'physique' && /lang=en/.test(e.hash) && e.en === 'true' && e.fr === 'false', `${e.titre} | ${e.bandeau} | ${e.hash}`);
  P('anglais : avertissement du mode 3', e.bandeau === 'Calculation of the real consequences of the figures in the story — no object of this kind has ever been observed.', e.bandeau);
  const v3 = await js(`[].slice.call(document.querySelectorAll('#ph-res .mesure')).map(function(m){return m.querySelector('.nom').textContent+' = '+m.querySelector('.val').textContent;})`);
  P('anglais : point décimal et unités (mode 3)', v3.some((l) => /= 4\.38×10¹² kg/.test(l)) && v3.some((l) => /= 59\.6 g/.test(l)) && v3.some((l) => /6\.91×10³ Gy\/s/.test(l)) && (await texte('#ph-r-v')) === '1.0 m' && (await texte('#ph-res')).indexOf('500 lb (227 kg)') > 0 && (await texte('#ph-res')).indexOf('1,500 kg') > 0, v3.join(' ; '));
  await js('document.querySelector("#ph-ctl-d").open = true; document.querySelectorAll("#p-physique details")[1].open = true'); await controleAnglais('mode 3, hypothèse A, tableaux ouverts');
  await capture(`simulateur_en_${suf}3_physique`);
  await cliquer('#ph-opt input[value="B"]'); await controleAnglais('mode 3, hypothèse B');
  // bascule vers le français sans perdre l'état
  await cliquer('#ph-opt input[value="A"]'); await curseur('#ph-P', 0); await regler('#ph-r', 2.5);
  await cliquer('#langue button[data-lang="fr"]'); await sleep(250); e = await etatLangue();
  P('bascule EN → FR en mode 3 : état conservé, textes français', e.lang === 'fr' && e.html === 'fr' && e.titre === 'C204 — simulateur 3D' && /lang=fr/.test(e.hash) && (await S('s.ph.P')) === 300 && (await S('s.ph.r')) === 2.5 && (await S('s.mode')) === 'physique' && (await texte('#ph-r-v')) === '2,5 m' && /5,06×10¹² kg/.test(await texte('#ph-res')), `${e.bandeau} | ${e.hash}`);
  await controleFrancais('mode 3');

  // ----- mode 1 : éclaté, fiche ouverte
  await seance(prof, 'mode=explorer&ecl=60');
  const c1 = await js(`(function(){var o=C204SIM.ensembles().C.objets.filter(function(o){return /Carter d'entraînement de singularité \\(1\\) — principale/.test(o.p.nom);})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); v.project(C204SIM.camera()); var r=document.getElementById('toile').getBoundingClientRect(); return {x:r.left+(v.x+1)/2*r.width, y:r.top+(1-v.y)/2*r.height};})()`);
  await pointer(c1.x, c1.y); await sleep(500); await js('document.querySelector("#panneaux").scrollTop = 0');
  await controleFrancais('mode 1 avec fiche');
  const temoinFr = await js(SCAN_FR);
  P('témoin : le détecteur de français réagit bien sur la page française', temoinFr.pb.length >= 10, temoinFr.pb.slice(0, 2).join(' | '));
  const selAvant = await S('s.ex.sel && s.ex.sel.p.id');
  await cliquer('#langue button[data-lang="en"]'); await sleep(300); e = await etatLangue();
  const fiche = await texte('#ex-fiche');
  P('bascule FR → EN en mode 1 : état conservé (éclatement, pièce sélectionnée)', e.lang === 'en' && (await S('s.ex.ecl')) === 0.6 && (await S('s.ex.sel && s.ex.sel.p.id')) === selAvant && !!selAvant && (await texte('#ex-ecl-v')) === '60%', `pièce ${selAvant} | ${e.bandeau}`);
  P('anglais : fiche de pièce — nom repris de la légende d\'origine, présentée comme telle', /“Singularity (drive|cooling) housing”|“Singularity magnetic field coil”/.test(fiche) && fiche.indexOf('Original caption (as written in the document)') > 0 && fiche.indexOf('Function claimed by the documents') > 0 && fiche.indexOf('Level of evidence') > 0 && fiche.indexOf('Source document') > 0, fiche.slice(0, 230));
  P('anglais : étiquettes de preuve [DOC] documented, [DED] deduced, [HYP] assumed', /\[DOC\] Documented/.test(await texte('#ex-legende')) && /\[DED\] Deduced/.test(await texte('#ex-legende')) && /\[HYP\] Assumed/.test(await texte('#ex-legende')), (await texte('#ex-legende')).slice(0, 90));
  await controleAnglais('mode 1, vue éclatée');
  const temoinEn = await js(SCAN_EN);
  P('témoin : le détecteur d\'anglais réagit bien sur la page anglaise', temoinEn.pb.length >= 10, temoinEn.pb.slice(0, 2).join(' | '));
  await capture(`simulateur_en_${suf}1_explorer`);
  await js('document.querySelector("#ex-fiche").scrollIntoView({block:"start"})'); await sleep(250); await controleAnglais('mode 1, fiche de pièce'); await capture(`simulateur_en_${suf}1_fiche`);
  // sélecteur au clavier
  await js('document.querySelector("#langue button[data-lang=fr]").focus()'); await touche('Enter', 'Enter', 1, 13); await sleep(200);
  const lf = await js('C204SIM.langue()'); await touche('Tab', 'Tab', 1, 9); const foc = await js('document.activeElement.getAttribute("data-lang")'); await touche(' ', 'Space', 1, 32); await sleep(200);
  P('sélecteur de langue au clavier (Entrée sur FR, Tab, Espace sur EN)', lf === 'fr' && foc === 'en' && (await js('C204SIM.langue()')) === 'en' && (await js('document.querySelector("#langue").getAttribute("aria-label")')) === 'Language', `${lf} → ${await js('C204SIM.langue()')}`);

  // ----- mode 2 : frise en cours, bascule sans perte, chaque étape en anglais
  await seance(prof, 'mode=recit&ech=doc014&cible=2000');
  await regler('#re-t', 430); await sleep(300);
  await cliquer('#langue button[data-lang="en"]'); await sleep(300); e = await etatLangue();
  P('bascule FR → EN en mode 2 : position de la frise, échelle et date cible conservées', e.lang === 'en' && Math.abs((await S('s.re.t')) - 0.43) < 1e-9 && (await S('s.re.ech')) === 'doc014' && (await S('s.re.cible')) === 2000, e.hash);
  P('anglais : avertissement du mode 2 intact', e.bandeau === 'Reconstruction of a story — none of these images corresponds to an observed phenomenon.', e.bandeau);
  P('anglais : étape de la frise légendée « According to the story »', /^4\. The “field” appears\. According to the story: /.test(await texte('#sous-titre')) && (await texte('#etapes button[aria-current="step"]')) === 'The “field” appears', (await texte('#sous-titre')).slice(0, 110));
  await controleAnglais('mode 2, étape 4, échelle DOC-014'); await capture(`simulateur_en_${suf}2_recit`);
  for (const t of [50, 200, 300, 485, 700, 960]) { await regler('#re-t', t); await sleep(200); const s = await js(SCAN_FR), ch = await js(CHEVAUCHEMENTS); if (s.pb.length || ch.pb.length) P(`anglais, mode 2 à t = ${t / 1000}`, false, s.pb.concat(ch.pb).join(' | ')); }
  P('anglais : les sept étapes de la frise sans texte français', true, await js(`[].slice.call(document.querySelectorAll('#etapes button')).map(function(b){return b.textContent;}).join(' · ')`));
  P('anglais : durée du trajet et divergence (mode 2)', /^Gap: 36 years → a 3\.6 h trip on board; elapsed: /.test(await texte('#re-duree')) && /%$/.test(await texte('#re-div')) && !/ %$/.test(await texte('#re-div')), `${await texte('#re-duree')} | ${await texte('#re-div')} | ${await texte('#re-date')}`);
  await cliquer('#re-ech button[data-ech="texte"]'); await regler('#re-t', 430); await controleAnglais('mode 2, échelle du texte');
  await cliquer('#re-jouer'); await sleep(600); await cliquer('#langue button[data-lang="fr"]'); await sleep(500);
  P('bascule de langue pendant la lecture : la frise continue', (await S('s.re.lecture')) === true && (await S('s.re.t')) > 0.43 && (await texte('#re-jouer')) === '⏸ Pause', 't = ' + (await S('s.re.t')).toFixed(3));
  await cliquer('#re-jouer'); await controleFrancais('mode 2');

  // ----- mode 4 : simulation en cours et panne injectée
  await seance(prof, 'mode=r1&trajet=avion&vit=3600');
  await cliquer('#r1-jouer'); await sleep(1200); await cliquer('#r1-panne'); await sleep(200);
  const avant4 = await js('({t:C204SIM.etat.r1.t, panne:C204SIM.etat.r1.panne, mu:C204SIM.etat.r1.mu})');
  await cliquer('#langue button[data-lang="en"]'); await sleep(400); e = await etatLangue();
  const apres4 = await js('({t:C204SIM.etat.r1.t, panne:C204SIM.etat.r1.panne, mu:C204SIM.etat.r1.mu, lecture:C204SIM.etat.r1.lecture, trajet:C204SIM.etat.r1.trajet})');
  P('bascule FR → EN en mode 4 : simulation non remise à zéro, panne et trajet conservés', e.lang === 'en' && apres4.t > avant4.t && apres4.panne === avant4.panne && apres4.panne > 0 && apres4.mu >= avant4.mu && apres4.lecture && apres4.trajet === 'avion', `t ${Math.round(avant4.t)} → ${Math.round(apres4.t)} s ; panne n° ${apres4.panne}`);
  await cliquer('#r1-jouer');
  const p4 = await texte('#p-r1');
  P('anglais : avertissements du mode 4 (signaux simulés, « R1 computes it »)', /simulated signals/.test(e.bandeau) && p4.indexOf('Undergone by any object on this route; R1 computes it, it does not produce it.') > 0 && p4.indexOf('simulated') > 0, e.bandeau);
  P('anglais : panne injectée', /rejected by the voter/.test(await texte('#r1-calc')) && /fault of computer \d masked/.test(await texte('#r1-vote')) && /^\+6\.2380 ns per hour$/.test(await texte('#r1-y')) && (await js('document.querySelector("#r1-trajet").selectedOptions[0].textContent')) === 'Aircraft, westbound (10.7 km, 250 m/s)', `${await texte('#r1-vote')} | ${await texte('#r1-y')}`);
  await js('document.querySelector("#r1-legende-d").open = true'); await controleAnglais('mode 4, panne injectée');
  const c4 = await js(`(function(){var o=C204SIM.ensembles().R.objets.filter(function(o){return /Batterie LiFePO4/.test(o.p.nom);})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); v.project(C204SIM.camera()); var r=document.getElementById('toile').getBoundingClientRect(); return {x:r.left+(v.x+1)/2*r.width, y:r.top+(1-v.y)/2*r.height};})()`);
  await pointer(c4.x, c4.y); await sleep(700);
  P('anglais : fiche d\'un composant R1 (fonction réelle traduite)', /Real function \(stage R1\)/.test(await texte('#r1-fiche')) && /battery/i.test(await texte('#r1-fiche h3')), await texte('#r1-fiche h3'));
  await controleAnglais('mode 4, fiche de composant');
  await js('document.querySelector("#r1-calc").scrollIntoView({block:"center"})'); await sleep(250); await capture(`simulateur_en_${suf}4_r1`);

  // ----- persistance après rechargement, puis langue du navigateur
  await seance(prof, 'mode=explorer&lang=en');
  await cliquer('#langue button[data-lang="fr"]'); await cliquer('#langue button[data-lang="en"]');
  await charger('-'); e = await etatLangue();
  P('persistance : après rechargement sans fragment, l\'anglais choisi est conservé', e.lang === 'en' && e.html === 'en' && /lang=en/.test(e.hash), e.hash);
  await controleAnglais('mode 1 au chargement'); if (!mobile) await capture('simulateur_en_0_accueil');
  await cliquer('#langue button[data-lang="fr"]'); await charger('-'); e = await etatLangue();
  P('persistance : après rechargement sans fragment, le français choisi est conservé', e.lang === 'fr' && e.html === 'fr', e.hash);
  await js('try{localStorage.removeItem("c204-lang")}catch(e){}'); await charger('-');
  const nav = await js('navigator.language'); e = await etatLangue();
  P('sans choix mémorisé : langue du navigateur (français si elle commence par « fr », anglais sinon)', e.lang === (nav.toLowerCase().startsWith('fr') ? 'fr' : 'en'), `navigator.language = ${nav} → ${e.lang}`);
  await js('try{localStorage.removeItem("c204-lang")}catch(e){}');
  for (const loc of ['fr-FR', 'de-DE']) {
    try { await send('Emulation.setLocaleOverride', { locale: loc }); await send('Emulation.setUserAgentOverride', { userAgent: await js('navigator.userAgent'), acceptLanguage: loc }); await charger('-');
      const n2 = await js('navigator.language'), l2 = await js('C204SIM.langue()');
      P(`langue du navigateur simulée : ${loc}`, n2 === loc && l2 === (loc.startsWith('fr') ? 'fr' : 'en'), `navigator.language = ${n2} → ${l2}`);
    } catch (err) { P(`langue du navigateur simulée : ${loc} (émulation indisponible)`, true, err.message); }
    await js('try{localStorage.removeItem("c204-lang")}catch(e){}');
  }
  P('langue : aucune erreur ni exception dans la console', journal.exceptions.length === 0 && journal.console.filter((c) => /^(error|log\.error|assert)/.test(c)).length === 0, journal.console.concat(journal.exceptions).slice(0, 5).join(' | '));
}

// ------------------------------------------------------------------ le plan d'essais, pour un profil
async function essais(profil, w, h, dsf, mobile) {
  const prof = { w, h, dsf, mobile };
  const P = (n, ok, d) => noter(profil, n, ok, d);
  journal.console.length = 0; journal.exceptions.length = 0; journal.requetes.length = 0; journal.echecs.length = 0;
  await seance(prof, '');
  const dim = await js('[innerWidth, innerHeight, devicePixelRatio]');
  P('fenêtre', dim[0] === w && dim[1] === h, dim.join(' × '));
  const gl = await js(`(function(){var c=document.createElement('canvas'),g=c.getContext('webgl');var e=g&&g.getExtension('WEBGL_debug_renderer_info');return g?(e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):'webgl'):'aucun';})()`);
  P('WebGL disponible', gl !== 'aucun', gl);
  P('three.js chargé, scène construite', await js('typeof THREE === "object" && C204SIM.ensembles().C.objets.length'), 'pièces : ' + await js('C204SIM.ensembles().C.objets.length'));
  const ext = journal.requetes.filter((u) => !u.startsWith('file:'));
  P('seule ressource externe : three.js r128', ext.length === 1 && ext[0] === 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', ext.join(' , '));

  // ===== MODE 1
  P('mode 1 : bandeau', (await texte('#bandeau')).indexOf('rien n\'atteste') > 0);
  await capture(`simulateur_${profil}_1_explorer_ouvert`);
  await cliquer('#ex-etat button[data-e="ferme"]'); await sleep(900);
  P('mode 1 : bouton « Fermé » (clic réel)', (await S('s.ex.etat')) === 'ferme' && Math.abs(await js('C204SIM.ensembles().C.angle')) < 0.01, 'angle du couvercle : ' + await js('C204SIM.ensembles().C.angle'));
  await capture(`simulateur_${profil}_1_explorer_ferme`);
  await cliquer('#ex-etat button[data-e="ouvert"]'); await sleep(900);
  P('mode 1 : bouton « Ouvert »', Math.abs(await js('C204SIM.ensembles().C.angle') - 108) < 0.5, 'angle : ' + await js('C204SIM.ensembles().C.angle'));
  const pos0 = await js('(function(){var o=C204SIM.ensembles().C.objets.filter(function(o){return o.p.couche==="platine";})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); return v.z;})()');
  const v60 = await curseur('#ex-ecl', 0.6); await sleep(300);
  const pos1 = await js('(function(){var o=C204SIM.ensembles().C.objets.filter(function(o){return o.p.couche==="platine";})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); return v.z;})()');
  P('mode 1 : curseur d\'éclatement glissé (entrée réelle)', v60 >= 50 && v60 <= 70 && pos1 > pos0 + 0.1, `valeur ${v60} % ; la platine monte de ${(pos1 - pos0).toFixed(3)} m`);
  let ch = await js(CHEVAUCHEMENTS);
  P('mode 1 : étiquettes reliées, sans chevauchement', ch.n >= 12 && ch.pb.length === 0, `${ch.n} étiquettes ; ${ch.pb.join(' | ')}`);
  await capture(`simulateur_${profil}_1_explorer_eclate`);
  // curseur au clavier
  await js('document.querySelector("#ex-ecl").focus()'); await touche('End', 'End', 1, 35);
  P('mode 1 : curseur au clavier (touche Fin → 100 %)', (await S('s.ex.ecl')) === 1, 'ecl = ' + await S('s.ex.ecl'));
  ch = await js(CHEVAUCHEMENTS); P('mode 1 : étiquettes à 100 %', ch.pb.length === 0, `${ch.n} ; ${ch.pb.join(' | ')}`);
  await capture(`simulateur_${profil}_1_explorer_eclate100`);
  await touche('Home', 'Home', 1, 36);
  P('mode 1 : curseur ramené à 0 % (touche Début)', (await S('s.ex.ecl')) === 0 && (await js(CHEVAUCHEMENTS)).n === 0);
  // sélection d'une pièce : clic réel sur la toile, au centre projeté d'une pièce connue
  const cible2 = await js(`(function(){var o=C204SIM.ensembles().C.objets.filter(function(o){return o.p.id==='A-063';})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); v.project(C204SIM.camera()); var r=document.getElementById('toile').getBoundingClientRect(); return {x:r.left+(v.x+1)/2*r.width, y:r.top+(1-v.y)/2*r.height + 0, nom:o.p.nom};})()`);
  await pointer(cible2.x, cible2.y); await sleep(400);
  const fiche = await texte('#ex-fiche');
  const champs = ['Nom d\'origine', 'Repère', 'Document source', 'Fonction revendiquée', 'Niveau de preuve'].filter((c) => fiche.toLowerCase().indexOf(c.toLowerCase()) < 0);
  P('mode 1 : clic sur une pièce → fiche complète (nom d\'origine, traduction, repère…)', (await S('!!s.ex.sel && /n°5/.test(s.ex.sel.p.repere)')) && champs.length === 0 && fiche.indexOf('«') > 0, `pièce : ${await S('s.ex.sel && s.ex.sel.p.nom')} ; champs manquants : ${champs.join(', ') || 'aucun'}`);
  await js('document.querySelector("#ex-fiche").scrollIntoView({block:"start"})'); await sleep(200);
  await capture(`simulateur_${profil}_1_explorer_fiche`);
  await js('document.querySelector("#panneaux").scrollTop = 0');
  await cliquer('#ex-coul button[data-c="aspect"]'); P('mode 1 : couleurs « Aspect »', (await S('s.ex.coul')) === 'aspect'); await cliquer('#ex-coul button[data-c="classement"]');
  await cliquer('#ex-fant'); P('mode 1 : enveloppes translucides', (await S('s.ex.fant')) === true); await cliquer('#ex-fant');
  // caméra : glisser, molette ou pincement, clavier
  await seance(prof, 'mode=explorer');
  const tr = await rect('#toile'); const o0 = await js('(function(){var c=C204SIM.camera().position;return [c.x,c.y,c.z];})()');
  await glisser(tr.x + tr.w * 0.5, tr.y + tr.h * 0.5, tr.x + tr.w * 0.5 + 60, tr.y + tr.h * 0.5 + 20);
  const o1 = await js('(function(){var c=C204SIM.camera().position;return [c.x,c.y,c.z];})()');
  P('mode 1 : rotation par glissement', Math.hypot(o1[0] - o0[0], o1[1] - o0[1], o1[2] - o0[2]) > 0.05);
  const d0 = await js('C204SIM.camera().position.length()');
  if (mobile) {
    const cx = tr.x + tr.w / 2, cy = tr.y + tr.h / 2;
    await send('Input.dispatchTouchEvent', { type: 'touchStart', touchPoints: [{ x: cx - 30, y: cy, id: 1 }, { x: cx + 30, y: cy, id: 2 }] });
    for (let i = 1; i <= 8; i++) { await send('Input.dispatchTouchEvent', { type: 'touchMove', touchPoints: [{ x: cx - 30 - 6 * i, y: cy, id: 1 }, { x: cx + 30 + 6 * i, y: cy, id: 2 }] }); await sleep(15); }
    await send('Input.dispatchTouchEvent', { type: 'touchEnd', touchPoints: [] }); await sleep(150);
  } else { await send('Input.dispatchMouseEvent', { type: 'mouseWheel', x: tr.x + tr.w / 2, y: tr.y + tr.h / 2, deltaX: 0, deltaY: -240 }); await sleep(150); }
  const d1 = await js('C204SIM.camera().position.length()');
  P(mobile ? 'mode 1 : zoom par pincement à deux doigts' : 'mode 1 : zoom à la molette', d1 < d0 * 0.97, `distance ${d0.toFixed(2)} → ${d1.toFixed(2)}`);
  await js('document.getElementById("toile").focus()'); const a0 = await js('C204SIM.camera().position.x'); await touche('ArrowLeft', 'ArrowLeft', 3, 37);
  P('mode 1 : rotation au clavier (flèches)', Math.abs(await js('C204SIM.camera().position.x') - a0) > 0.01);
  await cliquer('#ex-vue button[data-vue="dessus"]'); await sleep(200); await capture(`simulateur_${profil}_1_explorer_dessus`); await cliquer('#ex-vue button[data-vue="iso"]');
  let db = await js(DEBORDEMENTS); P('mode 1 : pas de débordement de texte', db.pb.length === 0, db.pb.join(' | ') + (db.ongletsDefilent ? ' (onglets défilants)' : ''));

  // ===== MODE 2
  await seance(prof, 'mode=explorer'); await cliquer('#tab-recit'); await sleep(500);
  P('mode 2 : bandeau permanent exact', (await texte('#bandeau')) === 'Reconstitution d\'un récit — aucune de ces images ne correspond à un phénomène observé.', await texte('#bandeau'));
  P('mode 2 : véhicule schématique affiché, unité fermée à bord', await js('(function(){var s=C204SIM.scene(),n=0;s.traverse(function(o){if(o.isMesh&&o.visible)n++;});return n>5;})()') && (await S('s.mode')) === 'recit');
  await cliquer('#re-jouer'); await sleep(2500);
  const t1 = await S('s.re.t'); P('mode 2 : lecture (la frise avance)', t1 > 0.03 && (await S('s.re.lecture')) === true, 't = ' + t1.toFixed(3) + ' après 2,5 s');
  await cliquer('#re-jouer'); const t2 = await S('s.re.t'); await sleep(700); const t3 = await S('s.re.t');
  P('mode 2 : pause', t3 === t2 && (await S('s.re.lecture')) === false, `t = ${t2.toFixed(3)} puis ${t3.toFixed(3)}`);
  const etapes = [];
  await curseur('#re-t', 0); for (let i = 0; i < 7; i++) { etapes.push((await texte('#etapes button[aria-current="step"]'))); await cliquer('#re-suiv'); }
  P('mode 2 : pas à pas « Étape ▶ » (7 étapes puis fin)', new Set(etapes).size === 7 && (await S('s.re.t')) === 1, etapes.join(' → '));
  await cliquer('#re-prec'); await cliquer('#re-prec');
  P('mode 2 : « ◀ Étape »', (await texte('#etapes button[aria-current="step"]')).indexOf('Noir complet') >= 0, await texte('#etapes button[aria-current="step"]'));
  await cliquer('#etapes button[data-i="3"]'); P('mode 2 : clic sur une étape de la liste', (await S('s.re.t')) > 0.35 && (await S('s.re.t')) < 0.45);
  await seance(prof, 'mode=recit');
  const vues = [['saisie', 0.05], ['puissance', 0.2], ['alarme', 0.3], ['champ', 0.43], ['lumiere', 0.485], ['noir', 0.7], ['arrivee', 0.96]];
  for (const [nom, t] of vues) {
    await js(`(function(){var e=document.querySelector('#re-t'); e.value=${Math.round(t * 1000)}; e.dispatchEvent(new Event('input',{bubbles:true}));})()`); await sleep(350);
    ch = await js(CHEVAUCHEMENTS);
    const etat = await js(`(function(){var s=C204SIM.scene(),v={};s.traverse(function(o){if(o.isMesh&&o.geometry&&o.geometry.type==='TorusGeometry'&&o.visible&&o.parent.visible)v.tores=(v.tores||0)+1;});return {hud:document.getElementById('hud').textContent, st:document.getElementById('sous-titre').textContent.slice(0,60), tores:v.tores||0, g:document.getElementById('re-g').textContent, date:document.getElementById('re-date').textContent, div:document.getElementById('re-div').textContent, temp:document.getElementById('re-temp').textContent};})()`);
    P(`mode 2 : étape « ${nom} » (t = ${t})`, ch.pb.length === 0 && etat.st.indexOf('Selon le récit') > 0, `${etat.hud} | traction ${etat.g} | ${etat.date} | div. ${etat.div} | ${etat.temp} | tores visibles ${etat.tores} | étiquettes ${ch.n} ${ch.pb.join(' | ')}`);
    if (['saisie', 'champ', 'lumiere', 'noir', 'arrivee'].includes(nom)) await capture(`simulateur_${profil}_2_recit_${nom}`);
  }
  const vt = await curseur('#re-t', 0.43); P('mode 2 : curseur de la frise glissé (entrée réelle)', vt > 380 && vt < 480, 'valeur ' + vt + ' / 1000');
  await cliquer('#re-ech button[data-ech="doc014"]'); await sleep(400); ch = await js(CHEVAUCHEMENTS);
  P('mode 2 : échelle DOC-014 (5, 6, 8, 11 m, attribution non établie)', (await S('s.re.ech')) === 'doc014' && (await texte('#re-ech-note')).indexOf('attribution non établie') > 0 && ch.pb.length === 0, `étiquettes ${ch.n} ${ch.pb.join(' | ')}`);
  await capture(`simulateur_${profil}_2_recit_doc014`);
  await cliquer('#re-ech button[data-ech="texte"]');
  P('mode 2 : échelle TEXTE (3,0–3,7 m)', (await texte('#re-ech-note')).indexOf('3,05 à 3,66 m') > 0, (await texte('#re-ech-note')).slice(0, 120));
  await js('document.querySelector("#re-cible").focus()'); await touche('ArrowRight', 'ArrowRight', 24, 39);
  P('mode 2 : date cible réglée au clavier → durée à 10 ans/h', (await S('s.re.cible')) === 2000 && (await texte('#re-duree')).indexOf('36 ans → trajet de 3,6 h') >= 0, await texte('#re-duree'));
  await js(`(function(){var e=document.querySelector('#re-t'); e.value=1000; e.dispatchEvent(new Event('input',{bubbles:true}));})()`);
  P('mode 2 : divergence à l\'arrivée = 1 % × écart / 60 ans', (await texte('#re-div')) === '0,60 %', await texte('#re-div'));
  db = await js(DEBORDEMENTS); P('mode 2 : pas de débordement de texte', db.pb.length === 0, db.pb.join(' | '));

  // ===== MODE 3
  await seance(prof, 'mode=recit'); await cliquer('#tab-physique'); await sleep(500);
  const lire3 = () => js(`[].slice.call(document.querySelectorAll('#ph-res .mesure')).map(function(m){return m.querySelector('.nom').textContent+' = '+m.querySelector('.val').textContent+' ['+m.querySelector('.formule').textContent.slice(0,46)+']';})`);
  const num = (expr) => js(`(function(){var F=C204SIM.formules,K=C204SIM.constantes; return ${expr};})()`);
  let L3 = await lire3();
  P('mode 3 : 7 résultats, chacun avec sa formule', L3.length === 7 && L3.every((l) => /\[.{8,}\]$/.test(l)), '\n      ' + L3.join('\n      '));
  await capture(`simulateur_${profil}_3_physique_A`);
  const vP = await curseur('#ph-P', 1); L3 = await lire3();
  P('mode 3 : curseur de puissance glissé à 500 MW', vP === 500 && L3[0].indexOf('3,92×10¹²') > 0 && /53,3 g/.test(L3[1]), L3[0].split(' [')[0] + ' ; ' + L3[1].split(' [')[0]);
  await curseur('#ph-P', 0); L3 = await lire3();
  P('mode 3 : curseur de puissance glissé à 300 MW', (await S('s.ph.P')) === 300 && L3[0].indexOf('5,06×10¹²') > 0 && /68,[89] g/.test(L3[1]), L3[0].split(' [')[0] + ' ; ' + L3[1].split(' [')[0]);
  const vr = await curseur('#ph-r', 1); L3 = await lire3();
  P('mode 3 : curseur de distance glissé à 4 m', vr === 4, L3.map((l) => l.split(' [')[0].replace(/^[^=]*= /, '')).join(' ; '));
  await js('document.querySelector("#ph-r").focus()'); await touche('Home', 'Home', 1, 36); L3 = await lire3();
  P('mode 3 : distance au clavier → 0,5 m', (await S('s.ph.r')) === 0.5, L3.map((l) => l.split(' [')[0].replace(/^[^=]*= /, '')).join(' ; '));
  // remise à 400 MW / 1 m par le clavier puis sélecteur
  await js('document.querySelector("#ph-P").focus()'); await touche('ArrowRight', 'ArrowRight', 10, 39); await js('document.querySelector("#ph-r").focus()'); await touche('ArrowRight', 'ArrowRight', 5, 39);
  P('mode 3 : retour à 400 MW et 1,0 m au clavier', (await S('s.ph.P')) === 400 && Math.abs((await S('s.ph.r')) - 1) < 1e-9);
  ch = await js(CHEVAUCHEMENTS); P('mode 3 : étiquettes sans chevauchement', ch.pb.length === 0, `${ch.n} ; ${ch.pb.join(' | ')}`);
  await js('document.querySelector("#ph-ctl-d").open = true; document.querySelector("#ph-ctl-d").scrollIntoView({block:"start"})'); await sleep(200);
  if (!mobile) console.log('      [constantes et sources] ' + (await texte('#ph-src')));
  const ctl = await js(`[].slice.call(document.querySelectorAll('#ph-ctl tr')).map(function(r){return r.cells[0].textContent+' → '+r.cells[1].textContent;})`);
  const attendu = { PM2: [await num('F.PM2()'), 7.676e33], M300: [await num('F.masse(300e6)'), 5.058e12], M500: [await num('F.masse(500e6)'), 3.918e12],
    g500: [await num('F.pesanteur(2*F.masse(500e6),1)/K.g0'), 53.33], g300: [await num('F.pesanteur(2*F.masse(300e6),1)/K.g0'), 68.85],
    D1: [await num('F.dose(1,400e6,1)'), 3455], D3: [await num('F.dose(1,400e6,3)'), 383.8], S: [await num('F.surface()'), 1.0747],
    G05: [await num('F.gamma1(2*F.masse(300e6),0.5)'), 1.503e-14], G4: [await num('F.gamma1(2*F.masse(500e6),4)'), 1.455e-15],
    tau: [await num('F.vie(113.5)'), 6.047e-13], E: [await num('227*K.c*K.c'), 2.040e19], muons: [await num('C204SIM.tauxMuons*3600'), 126.7] };
  const ecarts = Object.entries(attendu).filter(([k, v]) => !proche(v[0], v[1], 2e-3));
  P('mode 3 : valeurs de contrôle calculées par la page = valeurs Python', ecarts.length === 0, '\n      ' + ctl.join('\n      ') + (ecarts.length ? '\n      ÉCARTS : ' + JSON.stringify(ecarts) : ''));
  await capture(`simulateur_${profil}_3_physique_controles`);
  await js('document.querySelector("#panneaux").scrollTop = 0');
  await cliquer('#ph-opt input[value="B"]'); await sleep(200);
  L3 = await lire3();
  P('mode 3 : option « 113 kg chacune » — durée de vie et énergie', (await S('s.ph.opt')) === 'B' && L3.some((l) => /Durée de vie = 6,05×10⁻¹³ s/.test(l)) && L3.some((l) => /2,04×10¹⁹ J/.test(l)), '\n      ' + L3.map((l) => l.split(' [')[0]).join('\n      '));
  await capture(`simulateur_${profil}_3_physique_B`);
  db = await js(DEBORDEMENTS); P('mode 3 : pas de débordement de texte', db.pb.length === 0, db.pb.join(' | '));
  await cliquer('#ph-opt input[value="A"]'); P('mode 3 : retour à la première hypothèse (clic réel)', (await S('s.ph.opt')) === 'A');
  ch = await js(CHEVAUCHEMENTS); P('mode 3 : étiquettes et traits de rappel (zones)', ch.pb.length === 0, `${ch.n} ; ${ch.pb.join(' | ')}`);

  // ===== MODE 4
  await seance(prof, 'mode=physique'); await cliquer('#tab-r1'); await sleep(700);
  P('mode 4 : modèle R1 construit', await js('!!C204SIM.ensembles().R && C204SIM.ensembles().R.objets.length'), 'pièces : ' + await js('C204SIM.ensembles().R.objets.length'));
  ch = await js(CHEVAUCHEMENTS); P('mode 4 : étiquettes sans chevauchement', ch.n === 8 && ch.pb.length === 0, `${ch.n} ; ${ch.pb.join(' | ')}`);
  const ATT = { route: -0.5013, train: -1.3279, mine: -0.3927, altitude: 0.3926, avion: 6.2380 }, lus = [];
  for (const id of Object.keys(ATT)) {
    await js(`(function(){var e=document.querySelector('#r1-trajet'); e.value='${id}'; e.dispatchEvent(new Event('change',{bubbles:true}));})()`); await sleep(120);
    const v = parseFloat((await texte('#r1-y')).replace('−', '-').replace(',', '.')); lus.push(`${id} ${await texte('#r1-y')}${Math.abs(v - ATT[id]) < 6e-4 ? '' : ' ≠ ' + ATT[id]}`);
  }
  P('mode 4 : cinq trajets — décalage en ns/h conforme à i01', lus.every((l) => l.indexOf('≠') < 0), lus.join(' ; '));
  P('mode 4 : mention « subi par tout objet… »', (await texte('#p-r1')).indexOf('Subi par tout objet sur ce trajet ; R1 le calcule, il ne le produit pas.') >= 0);
  await js(`(function(){var e=document.querySelector('#r1-trajet'); e.value='route'; e.dispatchEvent(new Event('change',{bubbles:true}));})()`);
  await cliquer('#r1-vit button[data-v="3600"]'); await cliquer('#r1-jouer'); await sleep(3000);
  const r1a = await js('(function(){var r=C204SIM.etat.r1;return {t:r.t,mu:r.mu,x:r.x.map(function(v){return v*1e9;}),lecture:r.lecture};})()');
  P('mode 4 : simulation lancée (× 3 600)', r1a.lecture && r1a.t > 3600, `temps simulé ${(r1a.t / 3600).toFixed(2)} h ; muons ${r1a.mu} (attendu ≈ ${(r1a.t / 3600 * 126.7).toFixed(0)}) ; écarts d'horloges ${r1a.x.map((v) => v.toFixed(1)).join(', ')} ns ; cumul ${await texte('#r1-cumul')}`);
  P('mode 4 : quatre horloges aux écarts visibles', (await js('document.querySelectorAll("#r1-horloges .horloge").length')) === 4 && r1a.x.some((v) => Math.abs(v) > 0.5));
  P('mode 4 : comptage de muons cohérent avec 127/h', Math.abs(r1a.mu - r1a.t / 3600 * 126.7) < 5 * Math.sqrt(r1a.t / 3600 * 126.7) + 3, `${r1a.mu} comptés`);
  await cliquer('#r1-jouer');
  await cliquer('#r1-panne'); await sleep(300);
  const pan = await js(`(function(){var r=C204SIM.etat.r1, L=[].slice.call(document.querySelectorAll('#r1-calc .calc')).map(function(c){return c.textContent.replace(/\\s+/g,' ')+(c.classList.contains('ecarte')?' [ÉCARTÉ]':'');}); var al=C204SIM.ensembles().R.objets.filter(function(o){return o.alerte;}).map(function(o){return o.p.nom;}); return {panne:r.panne,L:L,vote:document.getElementById('r1-vote').textContent,alerte:al,necarte:document.querySelectorAll('#r1-calc .calc.ecarte').length, bouton:document.getElementById('r1-panne').disabled, repare:document.getElementById('r1-repare').disabled};})()`);
  const vvote = parseFloat(pan.vote.replace('−', '-').replace(',', '.'));
  P('mode 4 : bouton « Injecter une panne » — le voteur écarte le calculateur fautif', pan.panne >= 1 && pan.necarte === 1 && Math.abs(vvote - ATT.route) < 1e-3 && pan.alerte.length === 1 && pan.bouton && !pan.repare, `panne sur n° ${pan.panne} ; ${pan.L.join(' | ')} ; vote : ${pan.vote} ; pièce signalée en 3D : ${pan.alerte.join(',')}`);
  await js('document.querySelector("#r1-calc").scrollIntoView({block:"center"})'); await sleep(250);
  await capture(`simulateur_${profil}_4_r1_panne`);
  await cliquer('#r1-repare'); await sleep(200);
  P('mode 4 : bouton « Réparer »', (await S('s.r1.panne')) === 0 && (await js('document.querySelectorAll("#r1-calc .calc.ecarte").length')) === 0);
  await js('document.querySelector("#panneaux").scrollTop = 0'); await sleep(150); await capture(`simulateur_${profil}_4_r1`);
  const c4 = await js(`(function(){var o=C204SIM.ensembles().R.objets.filter(function(o){return /Batterie LiFePO4/.test(o.p.nom);})[0]; var v=new THREE.Vector3(); o.mesh.getWorldPosition(v); v.project(C204SIM.camera()); var r=document.getElementById('toile').getBoundingClientRect(); return {x:r.left+(v.x+1)/2*r.width, y:r.top+(1-v.y)/2*r.height};})()`);
  await pointer(c4.x, c4.y); await sleep(300);
  P('mode 4 : clic sur un composant → fiche avec fonction réelle', (await texte('#r1-fiche')).indexOf('Fonction réelle') >= 0, (await texte('#r1-fiche h3')) || '');
  await sleep(700); await cliquer('#r1-raz'); P('mode 4 : remise à zéro', (await S('s.r1.t')) === 0 && (await S('s.r1.mu')) === 0);
  db = await js(DEBORDEMENTS); P('mode 4 : pas de débordement de texte', db.pb.length === 0, db.pb.join(' | '));

  // ===== onglets au clavier, thème
  await seance(prof, 'mode=r1');
  await js('document.querySelector("#tab-r1").focus()'); await touche('ArrowLeft', 'ArrowLeft', 1, 37);
  P('onglets : navigation au clavier (flèche gauche)', (await S('s.mode')) === 'physique' && await js('document.activeElement.id === "tab-physique"'));
  await touche('Home', 'Home', 1, 36); P('onglets : touche Début → mode 1', (await S('s.mode')) === 'explorer');
  db = await js(DEBORDEMENTS); P('onglets visibles sans défilement', !db.ongletsDefilent);
  await cliquer('#theme'); await cliquer('#theme'); await sleep(300);
  P('thème sombre (bouton)', (await js('document.documentElement.getAttribute("data-theme")')) === 'dark' && (await js('getComputedStyle(document.body).backgroundColor')) === 'rgb(16, 18, 22)');
  await js(`(function(){var e=document.querySelector('#ex-ecl'); e.value=60; e.dispatchEvent(new Event('input',{bubbles:true}));})()`); await sleep(400);
  await capture(`simulateur_${profil}_sombre_explorer`);
  await cliquer('#tab-recit'); await js(`(function(){var e=document.querySelector('#re-t'); e.value=430; e.dispatchEvent(new Event('input',{bubbles:true}));})()`); await sleep(400);
  await capture(`simulateur_${profil}_sombre_recit`);
  await cliquer('#theme'); await js('try{localStorage.removeItem("c204-theme")}catch(e){}');

  // fluidité : cadence d'image pendant la lecture du récit (indicatif)
  await seance(prof, 'mode=recit');
  await js(`(function(){var e=document.querySelector('#re-t'); e.value=380; e.dispatchEvent(new Event('input',{bubbles:true}));})()`); await cliquer('#re-jouer');
  const ips = await js(`new Promise(function(res){var n=0,t0=performance.now(),pire=0,tp=t0;(function b(t){n++;pire=Math.max(pire,t-tp);tp=t;if(t-t0<2000)requestAnimationFrame(b);else res({ips:Math.round(n/(t-t0)*1000),pire:Math.round(pire)});})(t0);})`);
  await cliquer('#re-jouer');
  P('fluidité pendant la lecture (indicatif, ' + gl + ')', ips.ips >= 25, `${ips.ips} images/s ; image la plus longue ${ips.pire} ms`);

  P('aucune erreur ni exception dans la console', journal.exceptions.length === 0 && journal.console.filter((c) => /^(error|log\.error|assert)/.test(c)).length === 0 && journal.echecs.length === 0,
    `${journal.exceptions.length} exception(s), ${journal.console.length} message(s) ${journal.console.concat(journal.exceptions, journal.echecs).slice(0, 6).join(' | ')}`);
}

async function essaisSpeciaux() {
  const profil = 'spécial', prof = { w: 1280, h: 800, dsf: 1, mobile: false };
  journal.console.length = 0; journal.exceptions.length = 0; journal.echecs.length = 0;
  await seance(prof, 'mode=physique', { sombre: true });
  noter(profil, 'thème sombre du système (prefers-color-scheme)', (await js('getComputedStyle(document.body).backgroundColor')) === 'rgb(16, 18, 22)' && (await js('document.documentElement.getAttribute("data-theme")')) === null);
  await capture('simulateur_1280_sombre_physique');
  await seance(prof, 'mode=recit', { reduit: true });
  await cliquer('#re-jouer'); const ta = await S('s.re.t'); await sleep(1200); const tb = await S('s.re.t'); await sleep(2200); const tc = await S('s.re.t');
  noter(profil, 'mouvement réduit : la frise avance par étapes, sans animation continue', ta === tb && tc > tb && Math.abs(tc - 0.12) < 0.02, `t = ${ta} → ${tb} → ${tc}`);
  await cliquer('#re-jouer'); await cliquer('#tab-explorer'); await cliquer('#ex-etat button[data-e="ferme"]'); await sleep(80);
  noter(profil, 'mouvement réduit : fermeture du couvercle immédiate', Math.abs(await js('C204SIM.ensembles().C.angle')) < 0.01);
  noter(profil, 'mouvement réduit : aucune erreur', journal.exceptions.length === 0, journal.exceptions.join(' | '));
  journal.console.length = 0; journal.exceptions.length = 0; journal.echecs.length = 0;
  await demarrer();
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await send('Network.setCacheDisabled', { cacheDisabled: true }); await send('Network.setBlockedURLs', { urls: ['*cdnjs.cloudflare.com*'] });
  TACTILE = false; await send('Page.navigate', { url: PAGE + '#mode=physique&lang=fr' }); await sleep(2500);
  const sans = await js(`(function(){return {three: typeof THREE, sim: typeof window.C204SIM, erreur: !document.getElementById('erreur').hidden, n: document.querySelectorAll('#ph-res .mesure').length, v: (document.querySelector('#ph-res .val')||{}).textContent};})()`);
  await js(`document.querySelector('#tab-r1').click()`); await js(`document.querySelector('#r1-jouer').click()`); await sleep(1200); await js(`document.querySelector('#r1-panne').click()`);
  const sans4 = await js(`(function(){return {t: C204SIM.etat.r1.t, ecarte: document.querySelectorAll('#r1-calc .calc.ecarte').length};})()`);
  noter(profil, 'sans three.js (CDN bloqué) : message d\'indisponibilité, modes 3 et 4 calculent encore', sans.three === 'undefined' && sans.sim === 'object' && sans.erreur && sans.n === 7 && sans4.t > 0 && sans4.ecarte === 1 && journal.exceptions.length === 0,
    `résultats mode 3 : ${sans.n} (${sans.v}) ; mode 4 : t = ${Math.round(sans4.t)} s, ${sans4.ecarte} calculateur écarté ; exceptions : ${journal.exceptions.join(' | ') || 'aucune'}`);
  await capture('simulateur_1280_sans_threejs');
}

try {
  if (QUOI === 'tout' || QUOI === 'bureau') await essais('1280', 1280, 800, 1, false);
  if (QUOI === 'tout' || QUOI === 'mobile') await essais('375', 375, 812, 2, true);
  if (QUOI === 'tout' || QUOI === 'special') await essaisSpeciaux();
  if (QUOI === 'tout' || QUOI === 'langue' || QUOI === 'langue-bureau') await essaisLangue('EN 1280', 1280, 800, 1, false);
  if (QUOI === 'tout' || QUOI === 'langue' || QUOI === 'langue-mobile') await essaisLangue('EN 375', 375, 812, 2, true);
  if (QUOI === 'tout' || QUOI === 'visionneuse') await essaisVisionneuse();
} catch (e) { console.log('INTERRUPTION : ' + e.message); resultats.push({ profil: '-', nom: 'interruption', ok: false, detail: e.message }); }
const ko = resultats.filter((r) => !r.ok);
console.log(`\n${resultats.length - ko.length} essais réussis sur ${resultats.length}` + (ko.length ? ' ; échecs : ' + ko.map((r) => `[${r.profil}] ${r.nom}`).join(' ; ') : ''));
writeFileSync(join(OUT, 'essais_resultats.json'), JSON.stringify(resultats, null, 1));
console.log('captures et essais_resultats.json : ' + OUT);
await arreter(); process.exit(0);
