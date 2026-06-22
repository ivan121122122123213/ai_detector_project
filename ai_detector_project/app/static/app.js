const fileInput = document.getElementById('fileInput');
const scanBtn = document.getElementById('scanBtn');
const statusEl = document.getElementById('status');
const aiSummary = document.getElementById('aiSummary');
const riskBadge = document.getElementById('riskBadge');
const entities = document.getElementById('entities');
const classes = document.getElementById('classes');
const files = document.getElementById('files');
const graph = document.getElementById('graph');
const recent = document.getElementById('recent');
const refreshBtn = document.getElementById('refreshBtn');
const reportLinks = document.getElementById('reportLinks');

function statRow(k,v){return `<div class="stat"><b>${k}</b><span>${v}</span></div>`}
function setBadge(score){
  riskBadge.className = 'badge';
  if(score >= 75){riskBadge.classList.add('high'); riskBadge.textContent = `High · ${score}/100`}
  else if(score >= 40){riskBadge.classList.add('medium'); riskBadge.textContent = `Medium · ${score}/100`}
  else {riskBadge.classList.add('low'); riskBadge.textContent = `Low · ${score}/100`}
}
function renderReport(r){
  document.getElementById('demoScore').textContent = r.risk_score;
  setBadge(r.risk_score);
  aiSummary.textContent = r.ai_summary;
  entities.innerHTML = Object.entries(r.summary || {}).sort((a,b)=>b[1]-a[1]).map(([k,v])=>statRow(k,v)).join('') || '<p class="muted">Нет сущностей</p>';
  classes.innerHTML = Object.entries(r.classifications || {}).sort((a,b)=>b[1]-a[1]).map(([k,v])=>statRow(k,v)).join('') || '<p class="muted">Нет классов</p>';
  files.innerHTML = (r.risky_files || []).slice(0,30).map(f=>{
    const findings = Object.entries(f.findings || {}).map(([k,v])=>`${k}: ${v.count}`).join(' · ');
    return `<div class="file"><div class="file-top"><code>${f.path}</code><span class="risk">${f.risk}</span></div><div class="findings">${f.classification} · ${findings}</div></div>`
  }).join('') || '<p class="muted">Нет рискованных файлов</p>';
  const nodes = (r.graph?.nodes || []).slice(0,120);
  graph.innerHTML = nodes.map(n=>`<span class="node ${n.group}">${n.label}</span>`).join('') || '<p class="muted">Граф появится после анализа.</p>';
  reportLinks.innerHTML = `<a href="/reports/${r.id}.json" target="_blank">JSON report</a><a href="/reports/${r.id}.html" target="_blank">HTML report</a>`;
}
async function scan(){
  const file = fileInput.files[0];
  if(!file){statusEl.textContent='Выбери архив.';return}
  const fd = new FormData();
  fd.append('file', file);
  statusEl.textContent = 'Сканирую архив...';
  scanBtn.disabled = true;
  try{
    const res = await fetch('/api/scan',{method:'POST',body:fd});
    const data = await res.json();
    if(!res.ok) throw new Error(data.detail || 'Scan failed');
    renderReport(data);
    statusEl.textContent = `Готово: ${data.files_total} файлов, risk ${data.risk_score}/100.`;
    loadRecent();
  }catch(e){statusEl.textContent = 'Ошибка: ' + e.message}
  finally{scanBtn.disabled = false}
}
async function loadRecent(){
  const res = await fetch('/api/analyses');
  const data = await res.json();
  recent.innerHTML = data.map(x=>`<div class="recent-item"><div><b>${x.filename}</b><div class="muted">${x.created_at}</div></div><button class="ghost" onclick="loadAnalysis('${x.id}')">Open · ${x.risk_score}</button></div>`).join('') || '<p class="muted">Пока нет анализов.</p>';
}
async function loadAnalysis(id){
  const res = await fetch('/api/analyses/'+id);
  renderReport(await res.json());
}
scanBtn.addEventListener('click', scan);
refreshBtn.addEventListener('click', loadRecent);
fileInput.addEventListener('change', ()=>{statusEl.textContent = fileInput.files[0] ? `Выбран файл: ${fileInput.files[0].name}` : 'Готов к загрузке.'});
loadRecent();
