window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.RecordsQuery = function RecordsQuery() {
  return `
    <section class="panel query-panel" id="records">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">06</span>宿舍用电明细查询</h2>
        <span class="panel-note">主表数据 · 支持宿舍、楼层、时间、风险筛选</span>
      </div>

      <div class="query-filters record-filters">
        <label>
          <span>宿舍号</span>
          <select id="recordDormFilter">
            <option value="">全部宿舍</option>
            ${buildDormOptions()}
          </select>
        </label>
        <label>
          <span>楼层</span>
          <select id="recordFloorFilter">
            <option value="">全部楼层</option>
            <option value="1">1楼</option>
            <option value="2">2楼</option>
            <option value="3">3楼</option>
            <option value="4">4楼</option>
            <option value="5">5楼</option>
          </select>
        </label>
        <label>
          <span>风险等级</span>
          <select id="recordRiskFilter">
            <option value="">全部风险</option>
            <option value="低">低</option>
            <option value="中">中</option>
            <option value="高">高</option>
          </select>
        </label>
        <label>
          <span>开始时间</span>
          <input id="recordStartFilter" type="text" placeholder="2026-05-12 00:00" />
        </label>
        <label>
          <span>结束时间</span>
          <input id="recordEndFilter" type="text" placeholder="2026-05-18 23:30" />
        </label>
        <button class="query-button" id="recordSearchButton" type="button">查询</button>
      </div>

      <div class="query-summary" id="recordSummary"></div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>宿舍</th>
              <th>楼层</th>
              <th>功率(W)</th>
              <th>累计用电(kWh)</th>
              <th>是否有人</th>
              <th>温度</th>
              <th>异常类型</th>
              <th>风险</th>
              <th>建议</th>
            </tr>
          </thead>
          <tbody id="recordsTable"></tbody>
        </table>
      </div>
    </section>
  `;
};

window.EnergyTeacher.components.getRecordFilters = function getRecordFilters() {
  return {
    dormId: valueOf("recordDormFilter"),
    floor: valueOf("recordFloorFilter"),
    riskLevel: valueOf("recordRiskFilter"),
    startTime: valueOf("recordStartFilter"),
    endTime: valueOf("recordEndFilter")
  };
};

window.EnergyTeacher.components.attachRecordQuery = function attachRecordQuery(onSearch) {
  document.getElementById("recordSearchButton").addEventListener("click", onSearch);
  ["recordDormFilter", "recordFloorFilter", "recordRiskFilter"].forEach((id) => {
    document.getElementById(id).addEventListener("change", onSearch);
  });
};

window.EnergyTeacher.components.renderRecords = function renderRecords(result) {
  const records = result.data || [];
  const body = document.getElementById("recordsTable");
  document.getElementById("recordSummary").textContent = `共匹配 ${result.total || 0} 条记录，当前显示 ${records.length} 条`;

  if (!records.length) {
    body.innerHTML = `<tr><td colspan="10" class="empty">暂无匹配的用电明细</td></tr>`;
    return;
  }

  body.innerHTML = records.map((item) => `
    <tr>
      <td>${textValue(item.time)}</td>
      <td><strong>${textValue(item.dorm_id)}</strong></td>
      <td>${item.floor || "--"}楼</td>
      <td>${numberValue(item.power, 1)}</td>
      <td>${numberValue(item.energy, 2)}</td>
      <td>${item.occupied ? "有人" : "无人"}</td>
      <td>${numberValue(item.temperature, 1)}℃</td>
      <td>${textValue(item.abnormal_type)}</td>
      <td><span class="risk-tag ${riskClass(item.risk_level)}">${textValue(item.risk_level)}</span></td>
      <td>${textValue(item.suggestion)}</td>
    </tr>
  `).join("");
};

function buildDormOptions() {
  const options = [];
  for (let floor = 1; floor <= 5; floor += 1) {
    for (let room = 1; room <= 10; room += 1) {
      const dormId = `A${floor}${String(room).padStart(2, "0")}`;
      options.push(`<option value="${dormId}">${dormId}</option>`);
    }
  }
  return options.join("");
}

function valueOf(id) {
  const node = document.getElementById(id);
  return node ? node.value.trim() : "";
}

function textValue(value) {
  return value === null || value === undefined || value === "" ? "--" : value;
}

function numberValue(value, digits) {
  if (value === null || value === undefined || value === "") return "--";
  return Number(value).toFixed(digits);
}
