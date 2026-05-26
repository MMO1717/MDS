window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.LivePower = function LivePower(realtime) {
  return `
    <article class="panel live-panel" id="live">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">01</span>宿舍实时用电显示</h2>
        <span class="panel-note">数据刷新：每 5 秒模拟更新</span>
      </div>
      <div class="live-main">
        <div class="power-readout">
          <div class="room">当前宿舍：${realtime.room} · ${realtime.roomType}</div>
          <div class="watts"><strong id="powerValue">${realtime.power}</strong><span>W</span></div>
          <div class="readout-meta">
            <span class="mini-chip">电压 <span id="voltageValue">${formatValue(realtime.voltage, "V")}</span></span>
            <span class="mini-chip">电流 <span id="currentValue">${formatValue(realtime.current, "A")}</span></span>
            <span class="mini-chip">累计 ${realtime.totalUsage}kWh</span>
            <span class="mini-chip">当前状态：<span id="statusValue">${realtime.status}</span></span>
            <span class="mini-chip">状态类型：正常 / 高耗电 / 异常</span>
          </div>
        </div>
        <div class="gauge" aria-label="宿舍用电负载率">
          <svg viewBox="0 0 200 200">
            <defs>
              <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#18a66a"></stop>
                <stop offset="100%" stop-color="#0ea5b7"></stop>
              </linearGradient>
            </defs>
            <circle class="gauge-track" cx="100" cy="100" r="80"></circle>
            <circle id="gaugeValue" class="gauge-value" cx="100" cy="100" r="80"></circle>
          </svg>
          <div class="gauge-center">
            <b id="loadRateValue">${realtime.loadRate}%</b>
            <span>实时负载率</span>
          </div>
        </div>
      </div>
      <div class="metric-grid">
        <div class="metric">
          <label>今日用电</label>
          <strong>${realtime.todayUsage}</strong><span>kWh</span>
        </div>
        <div class="metric">
          <label>本周用电</label>
          <strong>${realtime.weekUsage}</strong><span>kWh</span>
        </div>
        <div class="metric">
          <label>当前状态</label>
          <span class="status-text" id="statusTextValue">${realtime.status}</span>
        </div>
        <div class="metric">
          <label>较上周变化</label>
          <strong style="color: var(--amber);">${formatValue(realtime.weekChangePercent, "%", true)}</strong>
        </div>
      </div>
    </article>
  `;
};

window.EnergyApp.components.updateLivePower = function updateLivePower(realtime) {
  const powerValue = document.getElementById("powerValue");
  const currentValue = document.getElementById("currentValue");
  const voltageValue = document.getElementById("voltageValue");
  const statusValue = document.getElementById("statusValue");
  const statusTextValue = document.getElementById("statusTextValue");
  const loadRateValue = document.getElementById("loadRateValue");
  const gaugeValue = document.getElementById("gaugeValue");
  const circumference = 502;

  if (powerValue) powerValue.textContent = realtime.power;
  if (voltageValue) voltageValue.textContent = formatValue(realtime.voltage, "V");
  if (currentValue) currentValue.textContent = formatValue(realtime.current, "A");
  if (statusValue) statusValue.textContent = realtime.status;
  if (statusTextValue) statusTextValue.textContent = realtime.status;
  if (loadRateValue) loadRateValue.textContent = `${realtime.loadRate}%`;
  if (gaugeValue) {
    gaugeValue.style.strokeDashoffset = circumference - (circumference * realtime.loadRate) / 100;
  }
};

function formatValue(value, unit = "", showPlus = false) {
  if (value === "" || value === null || value === undefined) return "--";
  const prefix = showPlus && Number(value) > 0 ? "+" : "";
  return `${prefix}${value}${unit}`;
}
