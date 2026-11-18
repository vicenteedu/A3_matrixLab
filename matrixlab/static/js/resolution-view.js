import {Playback} from './playback.js';
const el = (tag, text, className) => { const n = document.createElement(tag); if (text !== undefined) n.textContent = text; if (className) n.className = className; return n; };
export function mountResolution(response) {
  const data = response.visualizacao;
  if (!data || data.versao !== 1 || data.tipo !== 'somar' || !Array.isArray(data.etapas) || !data.etapas.length) return () => {};
  const panel = document.getElementById('matrix-result');
  const root = el('div', undefined, 'resolution');
  const switcher = el('div', undefined, 'resolution-switch');
  const resultButton = el('button', 'Resultado', 'button secondary');
  const visualButton = el('button', 'Visualizar resolução', 'button secondary');
  [resultButton, visualButton].forEach(b => { b.type = 'button'; b.setAttribute('aria-pressed', String(b === resultButton)); switcher.append(b); });
  const view = el('section'); view.hidden = true; view.setAttribute('aria-label', 'Resolução visual da adição');
  const matrices = el('div', undefined, 'resolution-matrices');
  const cells = {};
  for (const [key, values] of [['A', data.a], ['B', data.b], ['C', response.resultado]]) {
    const figure = el('figure'); figure.append(el('figcaption', key === 'C' ? 'C · construção do resultado' : `${key} · valores utilizados`));
    const wrap = el('div', undefined, 'resolution-scroll'); const table = el('table'); table.setAttribute('aria-label', `Matriz ${key} da resolução`);
    cells[key] = []; const body = el('tbody');
    values.forEach((row, i) => { const tr = el('tr'); cells[key][i] = []; row.forEach((value, j) => { const td = el('td', key === 'C' ? '·' : String(value)); td.setAttribute('aria-label', `${key}, linha ${i+1}, coluna ${j+1}`); cells[key][i][j] = td; tr.append(td); }); body.append(tr); });
    table.append(body); wrap.append(table); figure.append(wrap); matrices.append(figure);
  }
  const expression = el('p', 'A + B = C', 'resolution-expression');
  const explanation = el('p', 'Avance ou pressione Reproduzir para acompanhar a primeira célula.'); explanation.setAttribute('role', 'status');
  const progress = el('progress'); progress.max = data.etapas.length; progress.value = 0; progress.setAttribute('aria-label', 'Progresso da resolução');
  const count = el('span'); const controls = el('div', undefined, 'resolution-controls');
  let player;
  const buttons = {};
  for (const [key, label, action] of [['restart','Reiniciar',()=>player.restart()],['previous','Anterior',()=>player.previous()],['play','Reproduzir',()=>player.timer === null ? player.play() : player.pause()],['next','Próximo',()=>player.next()]]) {
    const b = el('button', label, 'button secondary'); b.type = 'button'; b.addEventListener('click', action); controls.append(b); buttons[key] = b;
  }
  const speedLabel = el('label', 'Velocidade '); const speed = el('select');
  for (const value of [.5,1,1.5,2]) { const option = el('option', `${value}×`); option.value = value; option.selected = value === 1; speed.append(option); }
  speed.addEventListener('change',()=>player.setSpeed(Number(speed.value))); speedLabel.append(speed); controls.append(speedLabel);
  player = new Playback(data.etapas.length, (index, playing) => {
    Object.values(cells).forEach(rows=>rows.flat().forEach(td=>td.classList.remove('resolution-active')));
    cells.C.flat().forEach(td=>td.textContent='·');
    data.etapas.slice(0,index+1).forEach(step=>{cells.C[step.linha][step.coluna].textContent=String(step.valor);});
    const step = data.etapas[index];
    if (step) { for (const key of ['A','B','C']) cells[key][step.linha][step.coluna].classList.add('resolution-active'); }
    expression.textContent = step ? step.expressao : 'A + B = C';
    explanation.textContent = step ? step.explicacao : 'Avance ou pressione Reproduzir para acompanhar a primeira célula.';
    progress.value = index+1; count.textContent = `${index+1} de ${data.etapas.length} células`;
    buttons.play.textContent = playing ? 'Pausar' : 'Reproduzir'; buttons.previous.disabled = index < 0; buttons.next.disabled = index === data.etapas.length-1;
  });
  const result = document.getElementById('result-values'); const steps = document.getElementById('result-steps'); const hadSteps = !steps.hidden;
  const toggle = visual => { player.pause(); view.hidden = !visual; result.hidden = visual; steps.hidden = visual || !hadSteps; visualButton.setAttribute('aria-pressed', String(visual)); resultButton.setAttribute('aria-pressed', String(!visual)); };
  visualButton.addEventListener('click',()=>toggle(true)); resultButton.addEventListener('click',()=>toggle(false));
  view.tabIndex = 0; view.addEventListener('keydown', event=> { if (event.target !== view) return; const actions = {ArrowRight:()=>player.next(), ArrowLeft:()=>player.previous(), Home:()=>player.restart(), ' ':()=>player.timer === null ? player.play() : player.pause()}; if (actions[event.key]) {event.preventDefault(); actions[event.key]();} });
  view.append(matrices,expression,explanation,progress,count,controls,el('p','Teclado nesta área: ← anterior · → próximo · Espaço reproduzir/pausar · Home reiniciar','helper'));
  root.append(switcher,view); panel.append(root); player.emit();
  const visibility = () => { if (document.hidden || document.getElementById('view-matrices').hidden) player.pause(); };
  document.addEventListener('visibilitychange',visibility); window.addEventListener('hashchange',visibility);
  return () => {player.pause(); document.removeEventListener('visibilitychange',visibility); window.removeEventListener('hashchange',visibility); root.remove(); result.hidden=false;};
}
