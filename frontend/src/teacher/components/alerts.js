window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.Alerts = function Alerts() {
  return `
    <section class="panel query-panel" id="alerts">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">03</span>异常宿舍报警</h2>
        <span class="panel-note">支持按楼层、风险等级、异常类型筛选</span>
      </div>

      <div class="query-filters teacher-filters">
        <label>
          <span>楼层</span>
          <select id="floorFilter" aria-label="楼层筛选">
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
          <select id="riskFilter" aria-label="风险筛选">
            <option value="">全部风险</option>
            <option value="中">中风险</option>
            <option value="高">高风险</option>
          </select>
        </label>
        <label>
          <span>异常类型</span>
          <select id="typeFilter" aria-label="异常类型筛选">
            <option value="">全部类型</option>
            <option value="无人宿舍耗电">无人宿舍耗电</option>
            <option value="疑似高功率违规用电">高功率违规</option>
            <option value="楼层过载风险">楼层过载</option>
          </select>
        </label>
      </div>

      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>时间</th>
              <th>宿舍</th>
              <th>楼层</th>
              <th>功率(W)</th>
              <th>异常类型</th>
              <th>风险</th>
              <th>处理建议</th>
            </tr>
          </thead>
          <tbody id="abnormalTable"></tbody>
        </table>
      </div>
    </section>
  `;
};

window.EnergyTeacher.components.getAlertFilters = function getAlertFilters() {
  return {
    floor: valueOf("floorFilter"),
    riskLevel: valueOf("riskFilter"),
    abnormalType: valueOf("typeFilter")
  };
};

window.EnergyTeacher.components.attachAlertFilters = function attachAlertFilters(onChange) {
  ["floorFilter", "riskFilter", "typeFilter"].forEach((id) => {
    document.getElementById(id).addEventListener("change", onChange);
  });
};

window.EnergyTeacher.components.renderAlerts = function renderAlerts(records) {
  const tbody = document.getElementById("abnormalTable");
  if (!records.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty">暂无匹配的异常记录</td></tr>`;
    return;
  }

  tbody.innerHTML = records.map((item) => `
    <tr>
      <td>${item.time}</td>
      <td><strong>${item.dorm_id}</strong></td>
      <td>${item.floor}楼</td>
      <td>${formatPower(item.power)}</td>
      <td>${item.abnormal_type}</td>
      <td><span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span></td>
      <td>${item.suggestion}</td>
    </tr>
  `).join("");
};

function valueOf(id) {
  const node = document.getElementById(id);
  return node ? node.value : "";
}
