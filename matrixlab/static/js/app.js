import {renderIcons} from './icons.js';
import {initializeMatrixEditor} from './matrix-editor.js';
import {renderGraph} from './graph-view.js';

const pages = {overview: 'Visão geral', matrices: 'Matrizes', graphs: 'Grafos & Dijkstra', guide: 'Guia de conceitos', roadmap: 'Plano de desenvolvimento'};
const sidebar = document.getElementById('sidebar');
const menuButton = document.getElementById('menu-toggle');
const scrim = document.getElementById('scrim');

function setMenu(open, returnFocus = false) {
  sidebar.classList.toggle('open', open);
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  scrim.hidden = !open;
  document.body.style.overflow = open ? 'hidden' : '';
  sidebar.inert = window.matchMedia('(max-width: 760px)').matches && !open;
  if (open) sidebar.querySelector('a').focus();
  else if (returnFocus) menuButton.focus();
}

function navigate(focus = true) {
  let page = location.hash.slice(1) || 'overview';
  if (!Object.hasOwn(pages, page)) { page = 'overview'; history.replaceState(null, '', '#overview'); }
  document.querySelectorAll('.view').forEach(view => { view.hidden = view.id !== `view-${page}`; });
  document.querySelectorAll('.nav-link').forEach(link => {
    const current = link.hash === `#${page}`;
    link.classList.toggle('active', current);
    if (current) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
  });
  document.getElementById('breadcrumb').textContent = pages[page];
  document.title = `${pages[page]} · MatrixLab`;
  setMenu(false);
  if (focus) { document.getElementById('main').focus(); window.scrollTo(0, 0); }
}

async function fetchJSON(url) {
  const response = await fetch(url, {signal: AbortSignal.timeout(8000)});
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

async function checkHealth() {
  const status = document.getElementById('server-status');
  const indicator = document.createElement('i');
  try {
    const result = await fetchJSON('/api/health');
    if (result.status !== 'ok') throw new Error('Unavailable');
    status.className = 'server-status online';
    status.replaceChildren(indicator, document.createTextNode('Servidor local conectado'));
  } catch {
    status.className = 'server-status offline';
    status.replaceChildren(indicator, document.createTextNode('Servidor indisponível'));
  }
}

async function loadGraph() {
  const error = document.getElementById('graph-error');
  const canvas = document.getElementById('graph-canvas');
  error.hidden = true; canvas.setAttribute('aria-busy', 'true');
  canvas.textContent = 'Carregando exemplo…';
  try { renderGraph(await fetchJSON('/api/graph/example')); }
  catch {
    error.hidden = false;
    canvas.textContent = 'O exemplo está indisponível. Verifique o servidor e tente novamente.';
    canvas.setAttribute('aria-busy', 'false');
  }
}

renderIcons();
initializeMatrixEditor();
navigate(false);
checkHealth();
loadGraph();
window.addEventListener('hashchange', () => navigate());
document.querySelector('.skip-link').addEventListener('click', event => {
  event.preventDefault();
  document.getElementById('main').focus();
});
menuButton.addEventListener('click', () => setMenu(!sidebar.classList.contains('open')));
scrim.addEventListener('click', () => setMenu(false, true));
sidebar.addEventListener('click', event => { if (event.target.closest('a')?.hash === location.hash) setMenu(false, true); });
document.getElementById('retry-graph').addEventListener('click', () => { loadGraph(); checkHealth(); });
window.matchMedia('(max-width: 760px)').addEventListener('change', () => setMenu(false));
document.addEventListener('keydown', event => {
  if (!sidebar.classList.contains('open')) return;
  if (event.key === 'Escape') { setMenu(false, true); return; }
  if (event.key === 'Tab') {
    const links = [...sidebar.querySelectorAll('a')];
    const first = links[0]; const last = links[links.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }
});
