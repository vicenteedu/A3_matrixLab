/** Phase 1 input state only. All future mathematical operations belong to Python. */
const storageKey = 'matrixlab.matrix.v1';
const example = () => [[2, 4, 1], [0, 3, 7], [5, 1, 6]];
let matrix = example();

function validMatrix(value) {
  return Array.isArray(value) && value.length >= 1 && value.length <= 8 &&
    Array.isArray(value[0]) && value[0].length >= 1 && value[0].length <= 8 &&
    value.every(row => Array.isArray(row) && row.length === value[0].length && row.every(Number.isFinite));
}

function feedback(message, error = false) {
  const target = document.getElementById('matrix-feedback');
  target.textContent = message;
  target.classList.toggle('error', error);
}

function save() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(matrix));
    feedback('Rascunho salvo neste navegador.');
  } catch {
    feedback('Armazenamento indisponível. O rascunho será mantido apenas nesta sessão.', true);
  }
}

function render() {
  const container = document.getElementById('matrix-editor');
  container.replaceChildren();
  container.style.gridTemplateColumns = `repeat(${matrix[0].length}, 1fr)`;
  matrix.forEach((row, i) => row.forEach((value, j) => {
    const input = document.createElement('input');
    input.type = 'number'; input.step = 'any'; input.value = value;
    input.setAttribute('aria-label', `Matriz A, linha ${i + 1}, coluna ${j + 1}`);
    input.setAttribute('aria-describedby', 'matrix-feedback');
    input.addEventListener('input', () => {
      const parsed = input.valueAsNumber;
      const valid = input.value.trim() !== '' && Number.isFinite(parsed);
      input.setAttribute('aria-invalid', String(!valid));
      if (!valid) { feedback('Digite um número finito. O último valor válido será preservado.', true); return; }
      matrix[i][j] = parsed;
      save();
      if (container.querySelector('[aria-invalid="true"]')) feedback('Há células inválidas. Corrija os valores destacados.', true);
    });
    container.append(input);
  }));
  document.getElementById('rows').value = matrix.length;
  document.getElementById('columns').value = matrix[0].length;
  document.getElementById('matrix-shape').textContent = `A · ${matrix.length} × ${matrix[0].length}`;
}

export function initializeMatrixEditor() {
  try {
    const stored = localStorage.getItem(storageKey);
    if (stored !== null) {
      const candidate = JSON.parse(stored);
      if (validMatrix(candidate)) matrix = candidate;
      else feedback('Rascunho incompatível. O exemplo inicial foi carregado.', true);
    }
  } catch { feedback('Não foi possível recuperar o rascunho. O exemplo inicial foi carregado.', true); }
  render();
  document.getElementById('dimension-form').addEventListener('submit', event => {
    event.preventDefault();
    if (document.querySelector('#matrix-editor [aria-invalid="true"]')) {
      feedback('Corrija as células inválidas antes de alterar a dimensão.', true); return;
    }
    const rows = Number(document.getElementById('rows').value);
    const columns = Number(document.getElementById('columns').value);
    if (![rows, columns].every(value => Number.isInteger(value) && value >= 1 && value <= 8)) {
      feedback('Use dimensões inteiras de 1 a 8.', true); return;
    }
    matrix = Array.from({length: rows}, (_, i) => Array.from({length: columns}, (_, j) => matrix[i]?.[j] ?? 0));
    render(); save();
  });
  document.getElementById('reset-matrix').addEventListener('click', () => { matrix = example(); render(); save(); });
}
