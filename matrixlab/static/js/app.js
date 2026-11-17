import {renderIcons} from './icons.js';
import {initializeMatrixEditor} from './matrix-editor.js';
import {renderGraph} from './graph-view.js';

const pages = {matrices: 'Matrizes', graphs: 'Grafos', guide: 'Guia'};

function navigate(focus = true) {
  const requested = location.hash.slice(1);
  // Preserve old bookmarks after simplifying the navigation.
  const page = requested === 'roadmap' ? 'guide' : Object.hasOwn(pages, requested) ? requested : 'matrices';
  if (requested && requested !== page) history.replaceState(null, '', `#${page}`);
  document.querySelectorAll('.view').forEach(view => { view.hidden = view.id !== `view-${page}`; });
  document.querySelectorAll('.nav-link').forEach(link => {
    const current = link.hash === `#${page}`;
    link.classList.toggle('active', current);
    if (current) link.setAttribute('aria-current', 'page'); else link.removeAttribute('aria-current');
  });
  document.title = `${pages[page]} · MatrixLab`;
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
    status.replaceChildren(indicator, document.createTextNode('Servidor conectado'));
  } catch {
    status.className = 'server-status offline';
    status.replaceChildren(indicator, document.createTextNode('Servidor indisponível'));
  }
}

async function loadGraph() {
  const error = document.getElementById('graph-error');
  const canvas = document.getElementById('graph-canvas');
  error.hidden = true;
  canvas.setAttribute('aria-busy', 'true');
  canvas.textContent = 'Carregando exemplo…';
  try { renderGraph(await fetchJSON('/api/graph/example')); }
  catch {
    error.hidden = false;
    canvas.textContent = 'Exemplo indisponível. Tente novamente.';
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
document.getElementById('retry-graph').addEventListener('click', () => { loadGraph(); checkHealth(); });
