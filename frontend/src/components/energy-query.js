window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.EnergyQuery = function EnergyQuery(records) {
  const dormOptions = unique(records.map((item) => item.dorm_id));
  const floorOptions = unique(records.map((item) => item.floor));
  const dateOptions = unique(records.map((item) => item.time.slice(0, 10)));

  return `
    <section class="panel query-panel" id="records">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">05</span>宿舍用电明细查询</h2>
        <span class="panel-note">主表数据 · 支持按宿舍、楼层、日期、风险等级筛选</span>
      </div>

      <div class="query-filters">
        <label>
          <span>宿舍号</span>
          <select id="filterDorm">
            <option value="">全部宿舍</option>
            ${dormOptions.map((item) => `<option value="${item}">${item}</option>`).join("")}
          </select>
        </label>
        <label>
          <span>楼层</span>
          <select id="filterFloor">
            <option value="">全部楼层</option>
            ${floorOptions.map((item) => `<option value="${item}">${item} 层</option>`).join("")}
          </select>
        </label>
        <label>
          <span>日期</span>
          <select id="filterDate">
            <option value="">全部日期</option>
            ${dateOptions.map((item) => `<option value="${item}">${item}</option>`).join("")}
          </select>
        </label>
        <label>
          <span>风险等级</span>
          <select id="filterRisk">
            <option value="">全部等级</option>
            <option value="低">低</option>
            <option value="中">中</option>
            <option value="高">高</option>
          </select>
        </label>
        <label>
          <span>异常状态</span>
          <select id="filterAbnormal">
            <option value="">全部状态</option>
            <option value="normal">正常</option>
            <option value="abnormal">异常</option>
          </select>
        </label>
        <button class="query-button" id="resetFilters" type="button">重置</button>
      </div>

      <div class="query-summary" id="querySummary"></div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>宿舍号</th>
              <th>楼层</th>
              <th>功率(W)</th>
              <th>累计用电(kWh)</th>
              <th>是否有人</th>
              <th>温度</th>
              <th>异常类型</th>
              <th>风险</th>
              <th>处理建议</th>
            </tr>
          </thead>
          <tbody id="recordsBody"></tbody>
        </table>
      </div>
    </section>
  `;
};

window.EnergyApp.components.attachEnergyQuery = function attachEnergyQuery(records) {
  const controls = {
    dorm: document.getElementById("filterDorm"),
    floor: document.getElementById("filterFloor"),
    date: document.getElementById("filterDate"),
    risk: document.getElementById("filterRisk"),
    abnormal: document.getElementById("filterAbnormal")
  };
  const resetButton = document.getElementById("resetFilters");
  const body = document.getElementById("recordsBody");
  const summary = document.getElementById("querySummary");

  function renderRows() {
    const filtered = records.filter((item) => {
      const abnormalStatus = item.abnormal_status === "abnormal" ? "abnormal" : "normal";
      return (!controls.dorm.value || item.dorm_id === controls.dorm.value)
        && (!controls.floor.value || String(item.floor || "") === controls.floor.value)
        && (!controls.date.value || String(item.time || "").startsWith(controls.date.value))
        && (!controls.risk.value || item.risk_level === controls.risk.value)
        && (!controls.abnormal.value || abnormalStatus === controls.abnormal.value);
    });

    const visibleRows = filtered.slice(0, 80);
    summary.textContent = `共匹配 ${filtered.length} 条记录，当前显示前 ${visibleRows.length} 条`;
    body.innerHTML = visibleRows.map((item) => `
      <tr>
        <td>${textValue(item.time)}</td>
        <td>${textValue(item.dorm_id)}</td>
        <td>${item.floor ? `${item.floor} 层` : "--"}</td>
        <td>${numberValue(item.power, 1)}</td>
        <td>${numberValue(item.energy, 2)}</td>
        <td>${occupiedValue(item.occupied)}</td>
        <td>${temperatureValue(item.temperature)}</td>
        <td>${textValue(item.abnormal_type)}</td>
        <td><span class="risk-tag ${riskClass(item.risk_level)}">${textValue(item.risk_level)}</span></td>
        <td>${textValue(item.suggestion)}</td>
      </tr>
    `).join("");
  }

  Object.values(controls).forEach((control) => control.addEventListener("change", renderRows));
  resetButton.addEventListener("click", () => {
    Object.values(controls).forEach((control) => {
      control.value = "";
    });
    renderRows();
  });
  renderRows();
};

function unique(items) {
  return Array.from(new Set(items.filter((item) => item !== "" && item !== null && item !== undefined))).sort();
}

function riskClass(level) {
  if (level === "高") return "risk-high";
  if (level === "中") return "risk-mid";
  return "risk-low";
}

function textValue(value) {
  return value === "" || value === null || value === undefined ? "--" : value;
}

function numberValue(value, digits) {
  return value === "" || value === null || value === undefined ? "--" : Number(value).toFixed(digits);
}

function temperatureValue(value) {
  return value === "" || value === null || value === undefined ? "--" : `${Number(value).toFixed(1)}℃`;
}

function occupiedValue(value) {
  if (value === "" || value === null || value === undefined) return "--";
  return value ? "有人" : "无人";
}
