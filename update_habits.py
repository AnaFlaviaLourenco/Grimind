import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. seedState
seed_state_target = """  const recursos = [
    {id:genId(), titulo:'Mídia kit — Lendo Sáficos', link:''},
    {id:genId(), titulo:'Brand guide', link:''},
    {id:genId(), titulo:'Modelo de contrato de parceria', link:''}
  ];

  return { focus:'', tasks, vendas, recursos, covers:{} };
}"""

seed_state_replace = """  const recursos = [
    {id:genId(), titulo:'Mídia kit — Lendo Sáficos', link:''},
    {id:genId(), titulo:'Brand guide', link:''},
    {id:genId(), titulo:'Modelo de contrato de parceria', link:''}
  ];

  const habitos = [
    {id:genId(), nome:'Beber 2L de água', icone:'💧', cor:'blue'},
    {id:genId(), nome:'Leitura (15 min)', icone:'📖', cor:'orange'},
    {id:genId(), nome:'Exercício físico', icone:'🏃‍♀️', cor:'green'}
  ];
  const habitosLog = {};

  return { focus:'', tasks, vendas, recursos, covers:{}, habitos, habitosLog };
}"""

content = content.replace(seed_state_target, seed_state_replace)


# 2. init
init_target = """  const saved = await loadState();
  if(saved){
    state = saved;
    if(!state.covers) state.covers = {};
    rolloverRecurring();
  } else {"""

init_replace = """  const saved = await loadState();
  if(saved){
    state = saved;
    if(!state.covers) state.covers = {};
    if(!state.habitos) state.habitos = [];
    if(!state.habitosLog) state.habitosLog = {};
    rolloverRecurring();
  } else {"""

content = content.replace(init_target, init_replace)


# 3. Sidebar
sidebar_target = """    <div class="nav-item" data-page="pessoal" onclick="setPage('pessoal')"><span class="nav-emoji">🌱</span>Pessoal</div>
    <div class="nav-item" data-page="recursos" onclick="setPage('recursos')"><span class="nav-emoji">🗂️</span>Recursos &amp; Arquivo</div>"""

sidebar_replace = """    <div class="nav-item" data-page="pessoal" onclick="setPage('pessoal')"><span class="nav-emoji">🌱</span>Pessoal</div>
    <div class="nav-item" data-page="habitos" onclick="setPage('habitos')"><span class="nav-emoji">📅</span>Hábitos</div>
    <div class="nav-item" data-page="recursos" onclick="setPage('recursos')"><span class="nav-emoji">🗂️</span>Recursos &amp; Arquivo</div>"""

content = content.replace(sidebar_target, sidebar_replace)


# 4. renderPage
render_page_target = """  else if(page==='pessoal') content = renderArea('Pessoal','🌱');
  else if(page==='recursos') content = renderRecursos();"""

render_page_replace = """  else if(page==='pessoal') content = renderArea('Pessoal','🌱');
  else if(page==='habitos') content = renderHabitos();
  else if(page==='recursos') content = renderRecursos();"""

content = content.replace(render_page_target, render_page_replace)


# 5. renderHoje
render_hoje_target = """function renderHoje(){
  const today = todayStr();
  const listaHoje = state.tasks.filter(t=>!t.parentId && t.data===today && t.status!=='Feito').sort(byPriority);
  const atrasadas = state.tasks.filter(t=>!t.parentId && t.data && t.data<today && t.status!=='Feito');
  return `
    <div class="page-header"><span class="page-emoji">🏠</span><h1 class="page-title">Hoje</h1></div>
    <div class="callout">
      <div class="callout-icon">🎯</div>
      <div style="flex:1">
        <div class="callout-label">Resultado mais importante de hoje</div>
        <div class="callout-text" contenteditable="true" data-placeholder="Escreva aqui a única coisa que mais importa hoje..." oninput="updateFocus(this.innerText)">${escapeHtml(state.focus||'')}</div>
      </div>
    </div>
    <div class="section-label">Lista de hoje <span class="count">${listaHoje.length}</span></div>
    ${renderTaskList(listaHoje)}
    <button class="btn" style="margin-top:12px" onclick="openQuickAdd('hoje')">+ Nova tarefa rápida</button>
    <div class="toggle ${ui.openToggles.atrasadas?'open':''}">
      <div class="toggle-head" onclick="toggleSection('atrasadas')"><span class="toggle-arrow">▸</span> Atrasadas <span class="count">${atrasadas.length}</span></div>
      <div class="toggle-body">${atrasadas.length ? renderTaskList(atrasadas) : '<div class="empty">Nada atrasado.</div>'}</div>
    </div>
  `;
}"""

render_hoje_replace = """function renderHoje(){
  const today = todayStr();
  const listaHoje = state.tasks.filter(t=>!t.parentId && t.data===today && t.status!=='Feito').sort(byPriority);
  const atrasadas = state.tasks.filter(t=>!t.parentId && t.data && t.data<today && t.status!=='Feito');

  let habitosHTML = '';
  if (state.habitos && state.habitos.length > 0) {
    habitosHTML = `
      <div style="width: 250px; flex-shrink: 0;">
        <div class="section-label" style="margin-top:0">Hábitos de Hoje</div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          ${state.habitos.map(h => {
            const done = state.habitosLog[today] && state.habitosLog[today].includes(h.id);
            return \`<div class="card" style="margin-bottom:0;display:flex;align-items:center;gap:12px;padding:12px 14px;box-shadow:none;" onclick="toggleHabit('\${h.id}', '\${today}')">
              <div class="chk \${done ? 'checked' : ''}" style="border-radius:50%;width:22px;height:22px;background:\${done?'var(--'+(h.cor||'blue')+'-bg)':'var(--bg-input)'};border-color:\${done?'var(--'+(h.cor||'blue')+'-text)':'var(--border-strong)'};color:\${done?'var(--'+(h.cor||'blue')+'-text)':'transparent'}">\${done ? '✓' : ''}</div>
              <div style="font-size:18px;">\${h.icone}</div>
              <div class="task-name" style="\${done ? 'text-decoration:line-through;color:var(--text-tertiary);' : ''}">\${escapeHtml(h.nome)}</div>
            </div>\`;
          }).join('')}
        </div>
      </div>
    `;
  }

  return `
    <div class="page-header"><span class="page-emoji">🏠</span><h1 class="page-title">Hoje</h1></div>
    <div style="display:flex; gap: 32px; flex-wrap: wrap; align-items: flex-start;">
      ${habitosHTML}
      <div style="flex: 1; min-width: 300px;">
        <div class="callout" style="margin-bottom: 24px;">
          <div class="callout-icon">🎯</div>
          <div style="flex:1">
            <div class="callout-label">Resultado mais importante de hoje</div>
            <div class="callout-text" contenteditable="true" data-placeholder="Escreva aqui a única coisa que mais importa hoje..." oninput="updateFocus(this.innerText)">${escapeHtml(state.focus||'')}</div>
          </div>
        </div>
        <div class="section-label" style="margin-top:0">Lista de hoje <span class="count">${listaHoje.length}</span></div>
        ${renderTaskList(listaHoje)}
        <button class="btn" style="margin-top:12px" onclick="openQuickAdd('hoje')">+ Nova tarefa rápida</button>
        <div class="toggle ${ui.openToggles.atrasadas?'open':''}" style="margin-top:24px">
          <div class="toggle-head" onclick="toggleSection('atrasadas')"><span class="toggle-arrow">▸</span> Atrasadas <span class="count">${atrasadas.length}</span></div>
          <div class="toggle-body">${atrasadas.length ? renderTaskList(atrasadas) : '<div class="empty">Nada atrasado.</div>'}</div>
        </div>
      </div>
    </div>
  `;
}"""

content = content.replace(render_hoje_target, render_hoje_replace)


# 6. Add renderHabitos and toggleHabit after updateFocus
update_focus_target = """function updateFocus(txt){ state.focus = txt; saveState(); }"""
new_habits_code = """function updateFocus(txt){ state.focus = txt; saveState(); }

/* ---------- Hábitos ---------- */
function toggleHabit(id, dateStr) {
  if (!state.habitosLog[dateStr]) state.habitosLog[dateStr] = [];
  const log = state.habitosLog[dateStr];
  const idx = log.indexOf(id);
  if (idx >= 0) log.splice(idx, 1);
  else log.push(id);
  saveState();
  render();
}

function renderHabitos() {
  const d = new Date();
  const year = d.getFullYear();
  const month = d.getMonth();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  let headerRow = `<th style="width:180px;position:sticky;left:0;background:var(--bg-page);z-index:2;box-shadow: 1px 0 0 var(--border);">Hábito</th>`;
  for(let i=1; i<=daysInMonth; i++) {
    const isToday = i === d.getDate() ? 'background:var(--accent-soft);color:var(--accent-strong);' : '';
    headerRow += `<th style="text-align:center;min-width:36px;padding:10px 4px;${isToday}">${i}</th>`;
  }
  
  let rows = state.habitos.map(h => {
    let cells = `<td style="position:sticky;left:0;background:var(--bg-page);z-index:2;font-weight:600;box-shadow: 1px 0 0 var(--border);">
      <div style="display:flex;align-items:center;gap:8px;padding-right:12px;">
        <span style="font-size:16px">${h.icone}</span>
        <span style="flex:1">${escapeHtml(h.nome)}</span>
        <button class="icon-btn" style="font-size:14px;opacity:0.5" onclick="deleteHabit('${h.id}')" title="Excluir">✕</button>
      </div>
    </td>`;
    for(let i=1; i<=daysInMonth; i++) {
      const dateStr = fmt(new Date(year, month, i));
      const done = state.habitosLog[dateStr] && state.habitosLog[dateStr].includes(h.id);
      const isToday = i === d.getDate() ? 'background:var(--hover);' : '';
      cells += `<td style="text-align:center;padding:8px 4px;${isToday}">
        <div onclick="toggleHabit('${h.id}', '${dateStr}')" class="chk ${done ? 'checked' : ''}" style="border-radius:50%;width:22px;height:22px;margin:0 auto;background:${done?'var(--'+(h.cor||'blue')+'-bg)':'var(--bg-input)'};border-color:${done?'var(--'+(h.cor||'blue')+'-text)':'var(--border-strong)'};color:${done?'var(--'+(h.cor||'blue')+'-text)':'transparent'}">${done?'✓':''}</div>
      </td>`;
    }
    return `<tr>${cells}</tr>`;
  }).join('');

  if (state.habitos.length === 0) {
    rows = `<tr><td colspan="${daysInMonth + 1}"><div class="empty">Nenhum hábito cadastrado.</div></td></tr>`;
  }

  const monthName = d.toLocaleDateString('pt-BR', {month:'long', year:'numeric'}).replace(/^\w/, c => c.toUpperCase());

  return `
    <div class="page-header"><span class="page-emoji">📅</span><h1 class="page-title">Hábitos</h1></div>
    <div class="callout" style="padding: 14px 20px; margin-bottom: 24px; align-items:center;">
      <div style="flex:1; font-weight:700; color:var(--accent-strong); font-size:15px;">Mês atual: ${monthName}</div>
      <button class="btn btn-primary" onclick="promptNewHabit()">+ Novo hábito</button>
    </div>
    <div style="overflow-x:auto; padding-bottom: 20px; margin-left: -20px; margin-right: -20px; padding-left: 20px; padding-right: 20px;">
      <table class="dtable" style="width: max-content; font-size:13px;">
        <thead><tr>${headerRow}</tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </div>
  `;
}

function promptNewHabit() {
  const nome = prompt("Nome do novo hábito (ex: Beber 2L de água):");
  if (!nome || !nome.trim()) return;
  const icone = prompt("Ícone (emoji):", "✨") || "✨";
  const cores = ['blue','purple','orange','pink','green','gray','red','yellow'];
  const cor = cores[Math.floor(Math.random() * cores.length)];
  state.habitos.push({ id: genId(), nome: nome.trim(), icone, cor });
  saveState();
  render();
}

function deleteHabit(id) {
  if (!confirm("Tem certeza que deseja excluir este hábito? O histórico será perdido.")) return;
  state.habitos = state.habitos.filter(h => h.id !== id);
  for (const date in state.habitosLog) {
    state.habitosLog[date] = state.habitosLog[date].filter(hid => hid !== id);
  }
  saveState();
  render();
}"""

content = content.replace(update_focus_target, new_habits_code)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html successfully.")
