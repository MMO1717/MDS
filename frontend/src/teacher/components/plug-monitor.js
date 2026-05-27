window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.PlugMonitor = function PlugMonitor() {
  return `
    <section class="panel live-panel plug-panel" id="plug">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">03</span>真实插座实时监控</h2>
        <span class="panel-note">对接 Tuya /api/plug/monitor · 每 5 秒刷新</span>
      </div>
      <div class="plug-main">
        <div>
          <div class="room">监测宿舍：<span id="plugDormId">A101</span> · 智能插座</div>
          <div class="watts"><strong id="plugPower">--</strong><span>W</span></div>
          <div class="readout-meta">
            <span class="mini-chip">开关 <b id="plugSwitch">--</b></span>
            <span class="mini-chip">电压 <b id="plugVoltage">--</b></span>
            <span class="mini-chip">电流 <b id="plugCurrent">--</b></span>
            <span class="mini-chip">累计 <b id="plugEnergy">--</b></span>
            <span class="mini-chip">风险 <b id="plugRisk">--</b></span>
          </div>
          <div class="plug-actions">
            <button class="plug-toggle" id="plugToggleButton" type="button">读取中</button>
            <span id="plugActionTip">等待真实插座数据</span>
          </div>
        </div>
        <div class="risk-box plug-risk-box">
          <span>插座状态</span>
          <strong id="plugStatusText">--</strong>
          <p id="plugSuggestion">请先启动后端并配置 Tuya 密钥</p>
        </div>
      </div>
    </section>
  `;
};

window.EnergyTeacher.components.renderPlugMonitor = function renderPlugMonitor(monitor) {
  setText("plugDormId", monitor.dormId || "A101");
  setText("plugPower", Number(monitor.power || 0).toFixed(1));
  setText("plugSwitch", monitor.switchOn ? "开启" : "关闭");
  setText("plugVoltage", formatUnit(monitor.voltage, "V"));
  setText("plugCurrent", formatUnit(monitor.current, "A"));
  setText("plugEnergy", formatUnit(monitor.energy, "kWh"));
  setText("plugRisk", monitor.riskLevel || "低");
  setText("plugStatusText", monitor.abnormalStatus ? "异常" : monitor.switchOn ? "正常" : "关闭");
  setText("plugSuggestion", monitor.suggestion || "当前暂无建议。");

  const button = document.getElementById("plugToggleButton");
  if (button) {
    button.textContent = monitor.switchOn ? "关闭插座" : "打开插座";
    button.dataset.switchOn = monitor.switchOn ? "true" : "false";
    button.classList.toggle("is-on", Boolean(monitor.switchOn));
    button.disabled = false;
  }

  const box = document.querySelector(".plug-risk-box");
  if (box) {
    box.classList.toggle("is-high", monitor.riskLevel === "高");
    box.classList.toggle("is-mid", monitor.riskLevel === "中");
  }
};

window.EnergyTeacher.components.renderPlugError = function renderPlugError(message) {
  setText("plugStatusText", "未连接");
  setText("plugSuggestion", message || "无法读取真实插座，请确认 Tuya 配置和网络。 ");
  setText("plugPower", "--");
  const button = document.getElementById("plugToggleButton");
  if (button) {
    button.textContent = "插座不可用";
    button.disabled = true;
  }
};

window.EnergyTeacher.components.attachPlugControl = function attachPlugControl(onToggle) {
  const button = document.getElementById("plugToggleButton");
  if (!button) return;

  button.addEventListener("click", async () => {
    const nextSwitch = button.dataset.switchOn !== "true";
    button.disabled = true;
    setText("plugActionTip", nextSwitch ? "正在打开插座..." : "正在关闭插座...");
    try {
      await onToggle(nextSwitch);
      setText("plugActionTip", nextSwitch ? "插座已打开，正在刷新" : "插座已关闭，正在刷新");
    } catch (error) {
      console.error(error);
      setText("plugActionTip", "控制失败，请检查 Tuya 后端配置");
      button.disabled = false;
    }
  });
};

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function formatUnit(value, unit) {
  if (value === null || value === undefined || value === "") return "--";
  return `${Number(value).toFixed(1)}${unit}`;
}
