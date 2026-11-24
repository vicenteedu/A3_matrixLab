import {mountResolution} from './resolution-view.js';
let disposeResolution = () => {};
/** Coleta os dados e apresenta respostas; todos os cálculos ficam no Python. */
const storageKey = 'matrixlab.matrices.v2';
const legacyKey = 'matrixlab.matrix.v1';
const examples = {a: () => [[2, 4, 1], [0, 3, 7], [5, 1, 6]], b: () => [[1, 0, 2], [3, 1, 0], [0, 2, 1]]};
const operations = {
  somar: {binary: true, label: 'A + B', hint: 'A e B precisam ter as mesmas dimensões.'},
  subtrair: {binary: true, label: 'A − B', hint: 'A e B precisam ter as mesmas dimensões.'},
  multiplicar: {binary: true, label: 'A × B', hint: 'O número de colunas de A deve ser igual ao de linhas de B.'},
  transpor: {label: 'Aᵀ', hint: 'As linhas se tornam colunas.'},
  determinante: {label: 'det(A)', hint: 'Use uma matriz quadrada de ordem 1 a 8.'},
  identidade: {generator: true, label: 'Identidade', hint: 'Uma matriz quadrada com 1 na diagonal e 0 nas demais posições.'},
  nula: {generator: true, label: 'Matriz nula', hint: 'Uma matriz com todas as posições iguais a zero.'}
};
let state = {a: examples.a(), b: examples.b(), operacao: 'somar', linhas: 3, colunas: 3};
let currentRequest = null;
const element = id => document.getElementById(id);
const idFor = (key, id) => key === 'a' ? id : `b-${id}`;

function validMatrix(value) {
  return Array.isArray(value) && value.length >= 1 && value.length <= 8 &&
    Array.isArray(value[0]) && value[0].length >= 1 && value[0].length <= 8 &&
    value.every(row => Array.isArray(row) && row.length === value[0].length && row.every(Number.isFinite));
}

function validDimension(value) { return Number.isInteger(value) && value >= 1 && value <= 8; }

function feedback(key, message, error = false) {
  const target = element(idFor(key, 'matrix-feedback'));
  target.textContent = message;
  target.classList.toggle('error', error);
}

function save() {
  try { localStorage.setItem(storageKey, JSON.stringify(state)); return true; }
  catch { return false; }
}

function setResult(status, message, error = false) {
  disposeResolution(); disposeResolution = () => {};
  element('result-state').textContent = status;
  element('result-message').textContent = message;
  element('matrix-result').classList.toggle('has-error', error);
  element('result-values').replaceChildren();
  element('steps-list').replaceChildren();
  element('result-steps').hidden = true;
  element('result-steps').open = false;
}

function setBusy(busy) {
  element('calculate-matrix').disabled = busy;
  element('calculate-matrix').textContent = busy ? 'Calculando…' : 'Calcular ↗';
  element('matrix-result').setAttribute('aria-busy', String(busy));
}

function invalidate() {
  if (currentRequest) currentRequest.abort();
  currentRequest = null;
  setBusy(false);
  setResult('Aguardando', 'Clique em Calcular para usar os valores atuais.');
}

function render(key) {
  const matrix = state[key];
  const container = element(idFor(key, 'matrix-editor'));
  container.replaceChildren();
  container.style.gridTemplateColumns = `repeat(${matrix[0].length}, 1fr)`;
  matrix.forEach((row, i) => row.forEach((value, j) => {
    const input = document.createElement('input');
    input.type = 'number'; input.step = 'any'; input.value = value;
    input.setAttribute('aria-label', `Matriz ${key.toUpperCase()}, linha ${i + 1}, coluna ${j + 1}`);
    input.setAttribute('aria-describedby', idFor(key, 'matrix-feedback'));
    input.addEventListener('input', () => {
      invalidate();
      const valid = input.value.trim() !== '' && Number.isFinite(input.valueAsNumber);
      input.setAttribute('aria-invalid', String(!valid));
      if (!valid) { feedback(key, 'Digite um número finito. O último valor válido será preservado.', true); return; }
      state[key][i][j] = input.valueAsNumber;
      const saved = save();
      feedback(key, saved ? 'Rascunho salvo neste navegador.' : 'Armazenamento indisponível. Rascunho mantido nesta sessão.', !saved);
      if (container.querySelector('[aria-invalid="true"]')) feedback(key, 'Corrija as células destacadas.', true);
    });
    container.append(input);
  }));
  element(idFor(key, 'rows')).value = matrix.length;
  element(idFor(key, 'columns')).value = matrix[0].length;
  element(idFor(key, 'matrix-shape')).textContent = `${key.toUpperCase()} · ${matrix.length} × ${matrix[0].length}`;
}

function bindEditor(key) {
  const form = element(idFor(key, 'dimension-form'));
  form.addEventListener('input', invalidate);
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (element(idFor(key, 'matrix-editor')).querySelector('[aria-invalid="true"]')) {
      feedback(key, 'Corrija as células inválidas antes de alterar a dimensão.', true); return;
    }
    const rows = Number(element(idFor(key, 'rows')).value);
    const columns = Number(element(idFor(key, 'columns')).value);
    if (![rows, columns].every(validDimension)) { feedback(key, 'Use dimensões inteiras de 1 a 8.', true); return; }
    invalidate();
    state[key] = Array.from({length: rows}, (_, i) => Array.from({length: columns}, (_, j) => state[key][i]?.[j] ?? 0));
    render(key);
    const saved = save();
    feedback(key, saved ? 'Dimensão atualizada e rascunho salvo.' : 'Dimensão atualizada apenas nesta sessão.', !saved);
  });
  element(idFor(key, 'reset-matrix')).addEventListener('click', () => {
    invalidate(); state[key] = examples[key](); render(key);
    const saved = save();
    feedback(key, saved ? 'Exemplo restaurado e salvo.' : 'Exemplo restaurado apenas nesta sessão.', !saved);
  });
}

function showOperation() {
  const operation = operations[state.operacao];
  element('matrix-b').hidden = !operation.binary;
  element('matrix-editors').hidden = Boolean(operation.generator);
  element('matrix-editors').classList.toggle('binary', Boolean(operation.binary));
  element('generator-settings').hidden = !operation.generator;
  element('generator-columns-label').hidden = state.operacao === 'identidade';
  element('generator-rows-label').firstChild.textContent = state.operacao === 'identidade' ? 'Ordem' : 'Linhas';
  element('operation-hint').textContent = operation.hint;
  element('calculation-summary').textContent = operation.label;
}

function payload() {
  const data = {operacao: state.operacao};
  const operation = operations[state.operacao];
  if (operation.generator) {
    const rows = element('generator-rows');
    const columns = element('generator-columns');
    if (!rows.reportValidity() || (state.operacao === 'nula' && !columns.reportValidity())) return null;
    if (state.operacao === 'identidade') data.ordem = Number(rows.value);
    else { data.linhas = Number(rows.value); data.colunas = Number(columns.value); }
    return data;
  }
  for (const key of operation.binary ? ['a', 'b'] : ['a']) {
    const invalid = element(idFor(key, 'matrix-editor')).querySelector('[aria-invalid="true"]');
    if (invalid) { invalid.focus(); throw new Error(`Corrija os valores da matriz ${key.toUpperCase()}.`); }
    const rows = element(idFor(key, 'rows'));
    const columns = element(idFor(key, 'columns'));
    if (!rows.reportValidity() || !columns.reportValidity()) return null;
    if (Number(rows.value) !== state[key].length || Number(columns.value) !== state[key][0].length) {
      throw new Error(`Clique em Atualizar na matriz ${key.toUpperCase()} para aplicar a nova dimensão.`);
    }
    data[key] = state[key];
  }
  return data;
}

function showResult(response) {
  const result = response.resultado;
  if (!(Number.isFinite(result) || validMatrix(result)) || !Array.isArray(response.passos) || response.passos.some(step => typeof step !== 'string')) {
    throw new Error('O servidor retornou um resultado em formato inválido.');
  }
  setResult('Concluído', 'Cálculo concluído.');
  if (Array.isArray(result)) {
    const table = document.createElement('table');
    table.setAttribute('aria-label', 'Matriz resultado');
    const body = table.createTBody();
    result.forEach(row => { const tr = body.insertRow(); row.forEach(number => { tr.insertCell().textContent = String(number); }); });
    element('result-values').append(table);
  } else {
    const value = document.createElement('strong'); value.className = 'scalar-result'; value.textContent = response.visualizacao?.resultado_texto ?? String(result);
    element('result-values').append(value);
  }
  response.passos.forEach(step => { const li = document.createElement('li'); li.textContent = step; element('steps-list').append(li); });
  element('result-steps').hidden = response.passos.length === 0;
  disposeResolution = mountResolution(response);
}

async function calculate() {
  let data;
  try { data = payload(); }
  catch (error) { setResult('Verifique os dados', error.message, true); return; }
  if (!data) return;
  const controller = new AbortController();
  currentRequest = controller;
  setResult('Calculando', 'Enviando os dados ao Python…');
  setBusy(true);
  const timeout = setTimeout(() => controller.abort('timeout'), 15000);
  try {
    const response = await fetch('/api/matrices/calculate', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data), signal: controller.signal
    });
    const result = await response.json();
    if (currentRequest !== controller) return;
    if (!response.ok) {
      const pending = result.codigo === 'nao_implementado';
      setResult(pending ? 'Em desenvolvimento' : 'Não foi possível calcular', result.erro || 'Erro ao processar a operação.', !pending);
      return;
    }
    showResult(result);
  } catch (error) {
    if (currentRequest !== controller) return;
    setResult('Não foi possível calcular', controller.signal.aborted ? 'O cálculo demorou demais. Tente novamente.' : 'Não foi possível obter o resultado. Confira o servidor e tente novamente.', true);
  } finally {
    clearTimeout(timeout);
    if (currentRequest === controller) { currentRequest = null; setBusy(false); }
  }
}

export function initializeMatrixEditor() {
  // Reutiliza o mesmo componente para B, com identificadores próprios.
  const b = element('matrix-a').cloneNode(true);
  b.id = 'matrix-b'; b.setAttribute('aria-label', 'Editor da matriz B');
  b.querySelectorAll('[id]').forEach(child => { child.id = `b-${child.id}`; });
  b.querySelector('.matrix-label').textContent = 'B';
  b.querySelector('.matrix-editor').setAttribute('aria-label', 'Elementos da matriz B');
  element('matrix-editors').append(b);
  let warning = '';
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored !== null) {
      const value = JSON.parse(stored);
      if (!value || !validMatrix(value.a) || !validMatrix(value.b) || !Object.hasOwn(operations, value.operacao) || !validDimension(value.linhas) || !validDimension(value.colunas)) throw new Error('Invalid draft');
      state = {a: value.a, b: value.b, operacao: value.operacao, linhas: value.linhas, colunas: value.colunas};
    } else {
      const legacy = localStorage.getItem(legacyKey);
      if (legacy !== null) {
        const value = JSON.parse(legacy);
        if (!validMatrix(value)) throw new Error('Invalid draft');
        state.a = value;
      }
    }
  } catch { warning = 'Não foi possível recuperar o rascunho. O exemplo inicial foi carregado.'; }
  ['a', 'b'].forEach(key => { render(key); bindEditor(key); });
  if (warning) feedback('a', warning, true);
  element('matrix-operation').value = state.operacao;
  element('generator-rows').value = state.linhas;
  element('generator-columns').value = state.colunas;
  showOperation();
  element('matrix-operation').addEventListener('change', event => {
    invalidate(); state.operacao = event.target.value; showOperation();
    if (!save()) setResult('Aguardando', 'Armazenamento indisponível. Os dados ficam apenas nesta sessão.');
  });
  ['generator-rows', 'generator-columns'].forEach(id => element(id).addEventListener('input', () => {
    invalidate();
    const rows = Number(element('generator-rows').value);
    const columns = Number(element('generator-columns').value);
    if (validDimension(rows) && validDimension(columns)) { state.linhas = rows; state.colunas = columns; save(); }
  }));
  element('calculate-matrix').addEventListener('click', calculate);
}
