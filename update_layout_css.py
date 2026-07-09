import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Checkbox border-radius in CSS
content = re.sub(r'(\.chk\{[^}]*border-radius:)6px([^}]*\})', r'\g<1>4px\g<2>', content)
# Wait, it was 6px in CSS initially. 4px looks more like the mockup (almost square).

# 2. Add Carta do Dia CSS, tweak task-list CSS, button outline CSS
css_additions = """
.task-list { background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 2px 10px rgba(0,0,0,0.02); padding: 0 10px; }
.task-row:last-child { border-bottom: none; }
.task-row { padding: 12px 6px; }
.btn-outline { background: var(--bg-page); color: var(--accent-strong); border: 1.5px solid var(--border-strong); padding: 6px 14px; font-weight: 700; border-radius: var(--radius-sm); font-size: 13.5px; transition: all 0.2s; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; }
.btn-outline:hover { background: var(--hover); border-color: var(--accent); color: var(--accent-strong); }
.carta-widget { background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border); padding: 18px; display:flex; flex-direction:column; gap:16px; margin-top: 16px;}
.carta-content { display: flex; align-items: center; gap: 16px; justify-content: center; padding-top: 8px;}
.carta-img { width: 90px; height: 135px; background: var(--bg-page); border-radius: 6px; border: 1.5px solid var(--border-strong); display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: inset 0 0 10px rgba(0,0,0,0.02); position:relative; overflow:hidden;}
.carta-img::before { content:''; position:absolute; top:4px; left:4px; right:4px; bottom:4px; border: 1px solid var(--border-strong); border-radius: 4px; pointer-events:none;}
.carta-text { flex: 1; text-align: center; }
.carta-title { font-family: var(--font-display); font-size: 17px; color: var(--text); margin-bottom: 2px; font-weight: 600; }
.carta-sub { font-size: 12px; color: var(--text-tertiary); font-style: italic; }
"""
content = content.replace('</style>', css_additions + '\n</style>')

# 3. Modify renderHoje
render_hoje_target = re.search(r'function renderHoje\(\)\{.*?(?=function updateFocus)', content, re.DOTALL).group(0)

render_hoje_replace = """function renderHoje(){
  const today = todayStr();
  const listaHoje = state.tasks.filter(t=>!t.parentId && t.data===today && t.status!=='Feito').sort(byPriority);
  const atrasadas = state.tasks.filter(t=>!t.parentId && t.data && t.data<today && t.status!=='Feito');

  let habitosHTML = '';
  if (state.habitos && state.habitos.length > 0) {
    habitosHTML = `
      <div class="carta-widget" style="margin-top:0;">
        <div class="section-label" style="text-transform:uppercase; font-size:11px; letter-spacing:1px; color:var(--text-secondary); margin-bottom:8px;">Hábitos de Hoje <span style="color:var(--accent);font-size:14px;margin-left:4px;">✴️</span></div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          ${state.habitos.map(h => {
            const done = state.habitosLog[today] && state.habitosLog[today].includes(h.id);
            return \`<div class="card" style="margin-bottom:0;display:flex;align-items:center;gap:12px;padding:10px 14px;box-shadow:none;border:1px solid var(--border);border-radius:10px;cursor:pointer;" onclick="toggleHabit('\${h.id}', '\${today}')">
              <div class="chk \${done ? 'checked' : ''}" style="width:18px;height:18px;border-radius:4px;background:\${done?'var(--'+(h.cor||'blue')+'-bg)':'var(--bg-input)'};border-color:\${done?'var(--'+(h.cor||'blue')+'-text)':'var(--border-strong)'};color:\${done?'var(--'+(h.cor||'blue')+'-text)':'transparent'};display:flex;align-items:center;justify-content:center;font-size:12px;">\${done ? '✓' : ''}</div>
              <div style="font-size:16px;">\${h.icone}</div>
              <div class="task-name" style="font-size:14px; font-weight:600; \${done ? 'text-decoration:line-through;color:var(--text-tertiary);' : ''}">\${escapeHtml(h.nome)}</div>
            </div>\`;
          }).join('')}
        </div>
      </div>
    `;
  }

  const cartaHTML = `
    <div class="carta-widget">
      <div class="section-label" style="text-transform:none; font-family:var(--font-display); font-size:16px; color:var(--text); letter-spacing:0; font-weight:500;">✨ Carta do dia</div>
      <div style="height:1px; background:var(--border); margin:4px 0;"></div>
      <div class="carta-content">
        <div class="carta-img"><span style="color:var(--accent);font-size:24px;">🍷</span></div>
        <div class="carta-text">
          <div class="carta-title">Temperança</div>
          <div class="carta-sub">ritmo, foco e presença</div>
        </div>
      </div>
    </div>
  `;

  return `
    <div style="display:flex; align-items:center; gap:12px; margin-bottom: 4px;">
      <span style="color:var(--accent-strong); font-size:28px; line-height:1; font-family:var(--font-display);">✴️</span>
      <h1 class="page-title" style="margin:0; font-family:var(--font-display); font-size:32px; font-weight:600; color:var(--accent-strong);">Hoje</h1>
    </div>
    <div style="color:var(--text-tertiary); font-size:13px; margin-bottom:32px;">Um dia de cada vez, com intenção e leveza.</div>

    <div style="display:flex; gap: 32px; flex-wrap: wrap; align-items: flex-start;">
      
      <div style="flex: 1; min-width: 300px;">
        <div class="callout" style="margin-bottom: 32px; background: var(--accent-soft); border: 1px solid var(--grad-a); border-radius: 12px; padding: 20px 24px;">
          <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
            <div class="callout-icon" style="color: var(--accent-strong); margin:0;">🎯</div>
            <div class="callout-label" style="color: var(--accent-strong); text-transform: uppercase; font-size: 11px; letter-spacing: 1px; font-weight: 800; margin:0;">Resultado mais importante de hoje</div>
          </div>
          <div class="callout-text" contenteditable="true" data-placeholder="Escreva aqui a única coisa que mais importa hoje..." oninput="updateFocus(this.innerText)" style="color: var(--text-secondary); font-style: italic; font-size: 14.5px; padding-left: 34px;">\${escapeHtml(state.focus||'')}</div>
        </div>

        <div class="section-label" style="margin-top:0; text-transform:uppercase; font-size:11px; letter-spacing:1px; color:var(--text-secondary); margin-bottom:12px; font-weight:700;">Lista de hoje <span class="count" style="background:var(--accent-soft); color:var(--accent-strong); font-size:11px;">\${listaHoje.length}</span></div>
        \${renderTaskList(listaHoje)}
        <button class="btn-outline" style="margin-top:20px" onclick="openQuickAdd('hoje')"><span style="color:var(--accent-strong);font-size:16px;line-height:1;">+</span> Nova tarefa rápida</button>
        
        <div class="toggle \${ui.openToggles.atrasadas?'open':''}" style="margin-top:32px">
          <div class="toggle-head" onclick="toggleSection('atrasadas')"><span class="toggle-arrow">▸</span> <span style="text-transform:uppercase; font-size:11px; letter-spacing:1px; font-weight:700; color:var(--text-secondary);">Atrasadas</span> <span class="count" style="font-size:11px;">\${atrasadas.length}</span></div>
          <div class="toggle-body">\${atrasadas.length ? renderTaskList(atrasadas) : '<div class="empty">Nada atrasado.</div>'}</div>
        </div>
      </div>

      <div style="width: 300px; flex-shrink: 0;">
        \${habitosHTML}
        \${cartaHTML}
      </div>

    </div>
  `;
}
"""
content = content.replace(render_hoje_target, render_hoje_replace)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
