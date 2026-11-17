/** Read-only views share one server-provided graph. No path-finding in JavaScript. */
const namespace = 'http://www.w3.org/2000/svg';

function svgElement(tag, attributes, content) {
  const element = document.createElementNS(namespace, tag);
  Object.entries(attributes).forEach(([key, value]) => element.setAttribute(key, value));
  if (content !== undefined) element.textContent = content;
  return element;
}

export function renderGraph(graph) {
  const svg = svgElement('svg', {viewBox: '0 0 530 340', role: 'group', 'aria-label': 'Grafo de exemplo. Selecione um nó para conhecer suas conexões.'});
  graph.nodes.forEach((start, i) => {
    graph.nodes.slice(i + 1).forEach((end, offset) => {
      const weight = graph.adjacency[i][i + offset + 1];
      if (weight === null) return;
      const x = (start.x + end.x) / 2;
      const y = (start.y + end.y) / 2;
      svg.append(svgElement('line', {x1: start.x, y1: start.y, x2: end.x, y2: end.y, class: 'graph-edge'}));
      svg.append(svgElement('rect', {x: x - 14, y: y - 12, width: 28, height: 24, rx: 6, class: 'edge-weight-bg'}));
      svg.append(svgElement('text', {x, y: y + 4, class: 'edge-weight'}, weight));
    });
  });
  graph.nodes.forEach((node, index) => {
    const connections = graph.adjacency[index].flatMap((weight, neighbor) =>
      weight !== null && neighbor !== index ? [`${graph.nodes[neighbor].id} (peso ${weight})`] : []);
    const group = svgElement('g', {class: 'graph-node', tabindex: 0, role: 'button', 'aria-label': `Nó ${node.id}. Conexões: ${connections.join(', ')}.`, 'aria-pressed': 'false'});
    group.append(svgElement('circle', {cx: node.x, cy: node.y, r: 23}));
    group.append(svgElement('text', {x: node.x, y: node.y + 5}, node.id));
    const select = () => {
      svg.querySelectorAll('.graph-node').forEach(other => {
        other.classList.toggle('selected', other === group);
        other.setAttribute('aria-pressed', String(other === group));
      });
      document.getElementById('node-detail').textContent = `Nó ${node.id} → ${connections.join(' · ')}`;
    };
    group.addEventListener('click', select);
    group.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); select(); }
    });
    svg.append(group);
  });
  const canvas = document.getElementById('graph-canvas');
  canvas.replaceChildren(svg);
  canvas.setAttribute('aria-busy', 'false');
  renderAdjacency(graph);
}

function renderAdjacency(graph) {
  const table = document.createElement('table');
  table.setAttribute('aria-label', 'Matriz de adjacência do grafo de exemplo, somente leitura');
  const header = table.createTHead().insertRow();
  ['', ...graph.nodes.map(node => node.id)].forEach(label => {
    const cell = document.createElement('th'); cell.scope = 'col'; cell.textContent = label; header.append(cell);
  });
  const body = table.createTBody();
  graph.adjacency.forEach((values, row) => {
    const tr = body.insertRow();
    const label = document.createElement('th'); label.scope = 'row'; label.textContent = graph.nodes[row].id; tr.append(label);
    values.forEach((weight, column) => {
      const cell = tr.insertCell();
      cell.textContent = weight === null ? '—' : String(weight);
      if (weight === null) { cell.className = 'empty'; cell.setAttribute('aria-label', 'Sem conexão'); }
      if (row === column) cell.className = 'diagonal';
    });
  });
  document.getElementById('adjacency').replaceChildren(table);
}
