window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.LivePower = function LivePower(realtime) {
  return `
    <article class="panel live-panel" id="live">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">01</span>宿舍实时用电显示</h2>
        <span class="panel-note">数据刷新：每 5 秒读取智能插座</span>
      </div>
      <div class="live-main">
        <div class="power-readout">
          <div class="room">当前宿舍：<span id="roomValue">${realtime.room}</span> · ${realtime.roomType}</div>
          <div class="watts"><strong id="powerValue">${realtime.power}</strong><span>W</span></div>
          <div class="readout-meta">
            <span class="mini-chip">电压 <span id="voltageValue">${formatValue(realtime.voltage, "V")}</span></span>
            <span class="mini-chip">电流 <span id="currentValue">${formatValue(realtime.current, "A")}</span></span>
            <span class="mini-chip">累计 <span id="totalUsageValue">${formatValue(realtime.totalUsage)}</span>kWh</span>
            <span class="mini-chip">当前状态：<span id="statusValue">${realtime.status}</span></span>
            <span class="mini-chip">状态类型：正常 / 高耗电 / 异常</span>
          </div>
          <div class="plug-actions">
            <button class="plug-toggle" id="plugToggleButton" type="button">
              ${realtime.switchOn ? "关闭插座" : "打开插座"}
            </button>
            <span id="plugActionTip">真实 Tuya 智能插座控制</span>
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
  const roomValue = document.getElementById("roomValue");
  const powerValue = document.getElementById("powerValue");
  const currentValue = document.getElementById("currentValue");
  const voltageValue = document.getElementById("voltageValue");
  const totalUsageValue = document.getElementById("totalUsageValue");
  const statusValue = document.getElementById("statusValue");
  const statusTextValue = document.getElementById("statusTextValue");
  const loadRateValue = document.getElementById("loadRateValue");
  const gaugeValue = document.getElementById("gaugeValue");
  const plugToggleButton = document.getElementById("plugToggleButton");
  const circumference = 502;

  if (roomValue) roomValue.textContent = realtime.room;
  if (powerValue) powerValue.textContent = realtime.power;
  if (voltageValue) voltageValue.textContent = formatValue(realtime.voltage, "V");
  if (currentValue) currentValue.textContent = formatValue(realtime.current, "A");
  if (totalUsageValue) totalUsageValue.textContent = formatValue(realtime.totalUsage);
  if (statusValue) statusValue.textContent = realtime.status;
  if (statusTextValue) statusTextValue.textContent = realtime.status;
  if (loadRateValue) loadRateValue.textContent = `${realtime.loadRate}%`;
  if (plugToggleButton) {
    plugToggleButton.textContent = realtime.switchOn ? "关闭插座" : "打开插座";
    plugToggleButton.dataset.switchOn = realtime.switchOn ? "true" : "false";
    plugToggleButton.classList.toggle("is-on", Boolean(realtime.switchOn));
  }
  if (gaugeValue) {
    gaugeValue.style.strokeDashoffset = circumference - (circumference * realtime.loadRate) / 100;
  }
};

window.EnergyApp.components.attachPlugControl = function attachPlugControl(onRefresh) {
  const button = document.getElementById("plugToggleButton");
  const tip = document.getElementById("plugActionTip");
  if (!button) return;

  button.addEventListener("click", async () => {
    const nextSwitch = button.dataset.switchOn !== "true";
    button.disabled = true;
    if (tip) tip.textContent = nextSwitch ? "正在打开插座..." : "正在关闭插座...";

    try {
      await window.EnergyApp.energyService.setPlugSwitch(nextSwitch);
      if (tip) tip.textContent = nextSwitch ? "插座已打开，正在刷新功率" : "插座已关闭，正在刷新状态";
      await onRefresh();
    } catch (error) {
      if (tip) tip.textContent = "控制失败，请确认后端和 Tuya 项目在线";
      console.error(error);
    } finally {
      button.disabled = false;
    }
  });
};

function formatValue(value, unit = "", showPlus = false) {
  if (value === "" || value === null || value === undefined) return "--";
  const prefix = showPlus && Number(value) > 0 ? "+" : "";
  return `${prefix}${value}${unit}`;
}
