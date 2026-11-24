import {Playback} from './playback.js';

function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function matrixGrid(container, label, values, {blank = false, originalColumns} = {}) {
  const figure = el('figure');
  const scroll = el('div', undefined, 'resolution-scroll');
  const table = el('table');
  table.setAttribute('aria-label', label);
  const body = table.createTBody();
  const cells = values.map((row, i) => {
    const tr = body.insertRow();
    return row.map((value, j) => {
      const cell = tr.insertCell();
      cell.dataset.position = `Linha ${i + 1}, coluna ${j + 1}`;
      if (j >= originalColumns) {
        cell.classList.add('resolution-copy');
        cell.dataset.position += ' (coluna repetida)';
      }
      fill(cell, blank ? null : value);
      return cell;
    });
  });
  scroll.tabIndex = 0;
  scroll.setAttribute('role', 'region');
  scroll.setAttribute('aria-label', label);
  scroll.append(table);
  figure.append(el('figcaption', label), scroll);
  container.append(figure);
  return {figure, cells, rows: [...body.rows]};
}

function fill(cell, value) {
  cell.textContent = value ?? '·';
  cell.setAttribute('aria-label', `${cell.dataset.position}. ${value ?? 'Ainda não preenchida'}`);
}

function clearHighlights(grid) {
  for (const cell of grid.cells.flat()) {
    cell.classList.remove('resolution-active', 'resolution-factor', 'resolution-candidate', 'resolution-pivot');
    cell.removeAttribute('aria-current');
  }
}

function highlight(cell, className = 'resolution-active') {
  cell.classList.add(className);
  cell.setAttribute('aria-current', 'step');
}

function renderMatrixOperation(matrices, data, result, animate, view) {
  const transpose = data.tipo === 'transpor';
  const multiply = data.tipo === 'multiplicar';
  matrices.classList.toggle('resolution-unary', transpose);
  const a = matrixGrid(matrices, 'A · matriz original', data.a);
  if (transpose) {
    const arrow = el('span', '→', 'resolution-arrow');
    arrow.setAttribute('aria-hidden', 'true');
    matrices.append(arrow);
  }
  const b = transpose ? null : matrixGrid(matrices, 'B · segunda matriz', data.b);
  const c = matrixGrid(matrices, transpose ? 'Aᵀ · matriz transposta' : 'C · resultado em construção', result, {blank: true});
  return (index, moving) => {
    for (const grid of [a, b, c].filter(Boolean)) clearHighlights(grid);
    c.cells.flat().forEach(cell => fill(cell, null));
    for (const step of data.etapas.slice(0, index + 1)) {
      if (step.fase === 'produto') continue;
      const line = transpose ? step.linha_transposta : step.linha;
      const column = transpose ? step.coluna_transposta : step.coluna;
      fill(c.cells[line][column], step.valor);
    }
    const step = data.etapas[index];
    if (!step) return;
    if (transpose) {
      const from = a.cells[step.linha_original][step.coluna_original];
      const to = c.cells[step.linha_transposta][step.coluna_transposta];
      highlight(from, 'resolution-pivot');
      highlight(to, 'resolution-factor');
      if (moving) transfer(from, to, step.valor, view, animate);
    } else if (multiply) {
      a.cells[step.linha].forEach(cell => highlight(cell));
      b.cells.forEach(row => highlight(row[step.coluna]));
      if (step.fase === 'produto') {
        highlight(a.cells[step.linha][step.indice], 'resolution-factor');
        highlight(b.cells[step.indice][step.coluna], 'resolution-factor');
      }
      highlight(c.cells[step.linha][step.coluna]);
    } else {
      for (const grid of [a, b, c]) highlight(grid.cells[step.linha][step.coluna]);
    }
  };
}

function transfer(from, to, value, view, animate) {
  // If a wide matrix scrolls, keep the copy inside the visible viewport.
  const source = from.getBoundingClientRect();
  const target = to.getBoundingClientRect();
  const visible = (cell, rect) => {
    const scroll = cell.closest('.resolution-scroll').getBoundingClientRect();
    return rect.left >= scroll.left && rect.right <= scroll.right && rect.top >= 0 && rect.bottom <= innerHeight;
  };
  if (!visible(from, source) || !visible(to, target)) {
    animate(to, [{opacity: .35}, {opacity: 1}], 350);
    return;
  }
  const token = el('span', value, 'resolution-transfer');
  token.setAttribute('aria-hidden', 'true');
  const origin = view.getBoundingClientRect();
  token.style.left = `${source.left - origin.left}px`;
  token.style.top = `${source.top - origin.top}px`;
  token.style.width = `${source.width}px`;
  token.style.height = `${source.height}px`;
  view.append(token);
  const animation = animate(token, [
    {transform: 'translate(0, 0)', opacity: 1},
    {transform: `translate(${target.left - source.left}px, ${target.top - source.top}px)`, opacity: .85},
  ], 520);
  if (animation) {
    animate(to, [{opacity: .2}, {opacity: .2, offset: .75}, {opacity: 1}], 520);
    animation.finished.then(() => token.remove(), () => token.remove());
  } else token.remove();
}

const determinantMethods = {
  direto: 'Determinante de ordem 1',
  formula_2x2: 'Fórmula do determinante 2 × 2',
  sarrus: 'Regra de Sarrus',
  gauss: 'Eliminação de Gauss com pivoteamento parcial',
};

function renderDeterminant(matrices, data, updates, animate) {
  matrices.classList.add('resolution-determinant');
  const grid = matrixGrid(matrices, data.metodo === 'sarrus' ? 'A · duas primeiras colunas repetidas' : 'A · matriz de trabalho', data.matriz,
    {originalColumns: data.metodo === 'sarrus' ? 3 : undefined});

  return (index, moving) => {
    const step = data.etapas[index];
    clearHighlights(grid);
    const values = step?.matriz ?? data.matriz;
    grid.cells.forEach((row, i) => row.forEach((cell, j) => fill(cell, values[i][j])));
    for (const [i, j] of step?.candidatos ?? []) grid.cells[i][j].classList.add('resolution-candidate');
    if (step?.linha !== undefined) grid.cells[step.linha].forEach(cell => cell.classList.add('resolution-candidate'));
    for (const [i, j] of step?.celulas ?? []) {
      const style = step.sinal === 'negativa' ? 'resolution-pivot' : 'resolution-factor';
      highlight(grid.cells[i][j], style);
    }
    if (step?.pivo) {
      const [i, j] = step.pivo;
      highlight(grid.cells[i][j], 'resolution-pivot');
    }
    if (step?.linhas) {
      const [first, second] = step.linhas.map(index => grid.rows[index]);
      step.linhas.forEach(index => grid.cells[index].forEach(cell => highlight(cell)));
      if (moving) {
        const offset = second.getBoundingClientRect().top - first.getBoundingClientRect().top;
        animate(first, [{transform: `translateY(${offset}px)`}, {transform: 'translateY(0)'}], 470);
        animate(second, [{transform: `translateY(${-offset}px)`}, {transform: 'translateY(0)'}], 470);
      }
    }
    if (moving && step?.tipo === 'eliminacao') {
      animate(grid.rows[step.linha], [{opacity: .45}, {opacity: 1}], 360);
    }
    const calculations = step?.atualizacoes ?? [];
    updates.replaceChildren(...calculations.map(text => el('li', text)));
    updates.hidden = calculations.length === 0;
  };
}

export function mountResolution(response) {
  const data = response.visualizacao;
  const names = {somar: 'Adição', subtrair: 'Subtração', multiplicar: 'Multiplicação', transpor: 'Transposição'};
  const formulas = {somar: 'A + B = C', subtrair: 'A − B = C', multiplicar: 'A × B = C', transpor: 'A[i][j] → Aᵀ[j][i]'};
  const determinant = data?.tipo === 'determinante';
  const title = determinant ? determinantMethods[data.metodo] : names[data?.tipo];
  if (!title || data.versao !== 1 || !Array.isArray(data.etapas) || !data.etapas.length) return () => {};
  const formula = determinant ? title : formulas[data.tipo];
  const intro = 'Avance ou pressione Reproduzir para acompanhar a primeira etapa.';
  const panel = document.getElementById('matrix-result');
  const result = document.getElementById('result-values');
  const steps = document.getElementById('result-steps');
  const hadSteps = !steps.hidden;
  const root = el('div', undefined, 'resolution');
  const switcher = el('div', undefined, 'resolution-switch');
  const resultButton = el('button', 'Resultado', 'button secondary');
  const visualButton = el('button', 'Visualizar resolução', 'button secondary');
  for (const button of [resultButton, visualButton]) {
    button.type = 'button';
    button.setAttribute('aria-pressed', String(button === resultButton));
    switcher.append(button);
  }
  const view = el('section', undefined, 'resolution-view');
  view.hidden = true;
  view.tabIndex = 0;
  view.setAttribute('aria-label', title);
  const matrices = el('div', undefined, 'resolution-matrices');
  const updates = el('ul', undefined, 'resolution-updates');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  function stopMotion() {
    for (const animation of animations) animation.cancel();
    animations.clear();
    view.querySelectorAll('.resolution-transfer').forEach(token => token.remove());
  }
  function animate(node, frames, duration) {
    if (motion.matches || view.hidden || !node.animate) return null;
    const animation = node.animate(frames, {duration, easing: 'ease-in-out'});
    animations.add(animation);
    const forget = () => animations.delete(animation);
    animation.finished.then(forget, forget);
    return animation;
  }

  const render = determinant
    ? renderDeterminant(matrices, data, updates, animate)
    : renderMatrixOperation(matrices, data, response.resultado, animate, view);
  updates.hidden = true;
  const expression = el('p', formula, 'resolution-expression');
  const explanation = el('p', intro);
  const progress = el('progress');
  progress.max = data.etapas.length;
  progress.setAttribute('aria-label', 'Progresso da resolução');
  const count = el('span');
  const status = el('div', undefined, 'resolution-status');
  status.setAttribute('role', 'status');
  status.append(expression, explanation);
  const controls = el('div', undefined, 'resolution-controls');
  function togglePlay() {
    if (player.timer === null) player.play();
    else {
      player.pause();
      stopMotion();
    }
  }
  const buttons = {};
  for (const [key, label, action] of [
    ['restart', 'Reiniciar', () => player.restart()], ['previous', 'Anterior', () => player.previous()],
    ['play', 'Reproduzir', togglePlay], ['next', 'Próximo', () => player.next()],
  ]) {
    const button = el('button', label, 'button secondary');
    button.type = 'button';
    button.addEventListener('click', action);
    controls.append(button);
    buttons[key] = button;
  }
  const speedLabel = el('label', 'Velocidade ');
  const speed = el('select');
  for (const value of [.5, 1, 1.5, 2]) {
    const option = el('option', `${value}×`);
    option.value = value;
    option.selected = value === 1;
    speed.append(option);
  }
  speed.addEventListener('change', () => player.setSpeed(Number(speed.value)));
  speedLabel.append(speed);
  controls.append(speedLabel);

  let last = -2;
  const player = new Playback(data.etapas.length, (index, playing) => {
    if (index !== last) {
      stopMotion();
      render(index, index >= 0 && index === last + 1 && !motion.matches);
      last = index;
      const step = data.etapas[index];
      expression.textContent = step?.expressao ?? formula;
      explanation.textContent = step?.explicacao ?? intro;
      progress.value = index + 1;
      count.textContent = `${index + 1} de ${data.etapas.length} etapas`;
    }
    buttons.play.textContent = playing ? 'Pausar' : 'Reproduzir';
    buttons.previous.disabled = index < 0;
    buttons.next.disabled = index === data.etapas.length - 1;
  });

  function toggle(visual) {
    player.pause();
    stopMotion();
    view.hidden = !visual;
    result.hidden = visual;
    steps.hidden = visual || !hadSteps;
    visualButton.setAttribute('aria-pressed', String(visual));
    resultButton.setAttribute('aria-pressed', String(!visual));
  }
  visualButton.addEventListener('click', () => toggle(true));
  resultButton.addEventListener('click', () => toggle(false));
  view.addEventListener('keydown', event => {
    if (event.target !== view) return;
    const actions = {ArrowRight: () => player.next(), ArrowLeft: () => player.previous(), Home: () => player.restart(), ' ': togglePlay};
    if (actions[event.key]) { event.preventDefault(); actions[event.key](); }
  });
  view.append(controls, matrices, status, updates, progress, count,
    el('p', 'Teclado nesta área: ← anterior · → próximo · Espaço reproduzir/pausar · Home reiniciar', 'helper'));
  root.append(switcher, view);
  panel.append(root);
  player.emit();
  function visibility() {
    if (document.hidden || document.getElementById('view-matrices').hidden) {
      player.pause();
      stopMotion();
    }
  }
  document.addEventListener('visibilitychange', visibility);
  window.addEventListener('hashchange', visibility);
  motion.addEventListener('change', stopMotion);
  return () => {
    player.pause();
    stopMotion();
    motion.removeEventListener('change', stopMotion);
    document.removeEventListener('visibilitychange', visibility);
    window.removeEventListener('hashchange', visibility);
    root.remove();
    result.hidden = false;
  };
}
