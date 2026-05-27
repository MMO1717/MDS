window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.Insights = function Insights() {
  return `
    <section class="content-grid bottom-grid">
      <article class="panel" id="predictions">
        <div class="panel-header">
          <h2 class="module-title"><span class="module-index">04</span>高峰负载预测</h2>
          <span class="panel-note">高风险优先</span>
        </div>
        <div id="predictionList" class="notice-list"></div>
      </article>

      <article class="panel" id="suggestions">
        <div class="panel-header">
          <h2 class="module-title"><span class="module-index">05</span>节能建议</h2>
          <span class="panel-note">异常处理提醒</span>
        </div>
        <div id="suggestionList" class="advice-list"></div>
      </article>
    </section>
  `;
};

window.EnergyTeacher.components.renderInsights = function renderInsights(predictions, suggestions) {
  document.getElementById("predictionList").innerHTML = predictions.slice(0, 8).map((item) => `
    <div class="compact-item">
      <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
      <div>
        <strong>${item.floor}楼 ${item.time}</strong>
        <p>当前 ${formatPower(item.current_load)}，预测 ${formatPower(item.predicted_load)}</p>
      </div>
    </div>
  `).join("");

  document.getElementById("suggestionList").innerHTML = suggestions.slice(0, 8).map((item) => `
    <div class="compact-item">
      <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
      <div>
        <strong>${item.dorm_id} · ${item.abnormal_type}</strong>
        <p>${item.suggestion}</p>
      </div>
    </div>
  `).join("");
};

function riskClass(risk) {
  if (risk === "高") return "risk-high";
  if (risk === "中") return "risk-mid";
  return "risk-low";
}

function formatPower(value) {
  return `${Number(value || 0).toFixed(1)} W`;
}

function formatEnergy(value) {
  return `${Number(value || 0).toFixed(2)} 度`;
}
