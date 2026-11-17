/** Local SVG icons: no CDN, fonts or network dependencies. */
const paths = {
  overview: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
  matrix: '<path d="M6 3H3v18h3M18 3h3v18h-3"/><path d="M8 7h1m6 0h1M8 12h1m6 0h1M8 17h1m6 0h1"/>',
  graph: '<path d="m5 16 6-11 8 10-14 1 8 4 6-5M11 5l2 15"/><circle cx="11" cy="5" r="2"/><circle cx="5" cy="16" r="2"/><circle cx="19" cy="15" r="2"/><circle cx="13" cy="20" r="2"/>',
  book: '<path d="M12 5v16M3 4c3-1 6-1 9 1 3-2 6-2 9-1v15c-3-1-6-1-9 1-3-2-6-2-9-1z"/>',
  bulb: '<path d="M8 16c0-3-3-3-3-7a7 7 0 0 1 14 0c0 4-3 4-3 7M8 17h8M9 20h6M10 22h4M9 9l3 3 3-3M12 12v5"/>',
  info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>',
  menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
};

export function renderIcons() {
  document.querySelectorAll('[data-icon]').forEach(element => {
    element.innerHTML = `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[element.dataset.icon] || paths.info}</svg>`;
  });
}
