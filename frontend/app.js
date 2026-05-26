const API_BASE = "http://localhost:8000";

const $ = (id) => document.getElementById(id);

const riskClass = (risk) => {
  if (risk === "高") return "risk-high";
  if (risk === "中") return "risk-mid";
  return "risk-low";
};

const formatPower = (value) => `${Number(value || 0).toFixed(1)} W`;
const formatEnergy = (value) => `${Number(value || 0).toFixed(2)} 度`;

async function request(path) {
  const response = await fetch(`${API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`接口请求失败：${response.status}`);
  }
  return response.json();
}

function setStatus(online, text) {
  const status = $("apiStatus");
  status.innerHTML = `<span class="pulse"></span> ${text}`;
  status.classList.toggle("online", online);
  status.classList.toggle("offline", !online);
}

function renderOverview(overview) {
  $("dormCount").textContent = overview.dorm_count;
  $("dormCountMirror").textContent = overview.dorm_count;
  $("buildingInfo").textContent = `${overview.building}栋 / ${overview.floor_count}层`;
  $("currentPower").textContent = Number(overview.current_total_power || 0).toFixed(1);
  $("latestTime").textContent = overview.latest_time;
  $("currentAbnormal").textContent = overview.current_abnormal_count;
  $("currentAbnormalMirror").textContent = overview.current_abnormal_count;
  $("highRiskCount").textContent = overview.current_high_risk_count;
  $("totalEnergy").textContent = Number(overview.total_energy || 0).toFixed(2);
  $("abnormalTotal").textContent = overview.abnormal_record_count;
}

function renderFloors(floors) {
  $("floorCards").innerHTML = floors
    .map(
      (item) => `
        <article class="module-pill floor-card">
          <span>${item.floor}楼</span>
          <strong>${formatPower(item.floor_total_power)}</strong>
          <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
          <p>异常记录 ${item.abnormal_count} 条</p>
        </article>
      `,
    )
    .join("");
}

function renderRanking(items) {
  $("rankingList").innerHTML = items
    .map(
      (item, index) => `
        <div class="rank-item">
          <span class="rank-num">${index + 1}</span>
          <div>
            <strong>${item.dorm_id}</strong>
            <p>异常 ${item.abnormal_count} 条</p>
          </div>
          <b>${formatEnergy(item.energy)}</b>
        </div>
      `,
    )
    .join("");
}

function renderAbnormalTable(records) {
  const tbody = $("abnormalTable");
  if (!records.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty">暂无匹配的异常记录</td></tr>`;
    return;
  }

  tbody.innerHTML = records
    .map(
      (item) => `
        <tr>
          <td>${item.time}</td>
          <td><strong>${item.dorm_id}</strong></td>
          <td>${item.floor}楼</td>
          <td>${formatPower(item.power)}</td>
          <td>${item.abnormal_type}</td>
          <td><span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span></td>
          <td>${item.suggestion}</td>
        </tr>
      `,
    )
    .join("");
}

function renderPredictions(records) {
  $("predictionList").innerHTML = records
    .slice(0, 8)
    .map(
      (item) => `
        <div class="compact-item">
          <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
          <div>
            <strong>${item.floor}楼 ${item.time}</strong>
            <p>当前 ${formatPower(item.current_load)}，预测 ${formatPower(item.predicted_load)}</p>
          </div>
        </div>
      `,
    )
    .join("");
}

function renderSuggestions(records) {
  $("suggestionList").innerHTML = records
    .slice(0, 8)
    .map(
      (item) => `
        <div class="compact-item">
          <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
          <div>
            <strong>${item.dorm_id} · ${item.abnormal_type}</strong>
            <p>${item.suggestion}</p>
          </div>
        </div>
      `,
    )
    .join("");
}

function buildAbnormalQuery() {
  const params = new URLSearchParams({
    page: "1",
    page_size: "12",
  });

  const floor = $("floorFilter").value;
  const risk = $("riskFilter").value;
  const type = $("typeFilter").value;

  if (floor) params.set("floor", floor);
  if (risk) params.set("risk_level", risk);
  if (type) params.set("abnormal_type", type);

  return `/api/teacher/abnormal?${params.toString()}`;
}

async function loadAbnormalTable() {
  const abnormal = await request(buildAbnormalQuery());
  renderAbnormalTable(abnormal.data);
}

async function loadDashboard() {
  setStatus(false, "连接中");

  const [dashboard, abnormal, predictions, suggestions] = await Promise.all([
    request("/api/teacher/dashboard?limit=10"),
    request(buildAbnormalQuery()),
    request("/api/teacher/predictions?risk_level=高&page=1&page_size=8"),
    request("/api/teacher/suggestions?page=1&page_size=8"),
  ]);

  renderOverview(dashboard.overview);
  renderFloors(dashboard.floor_summary);
  renderRanking(dashboard.top_energy_dorms);
  renderAbnormalTable(abnormal.data);
  renderPredictions(predictions.data);
  renderSuggestions(suggestions.data);

  setStatus(true, "后端已连接");
}

function bindEvents() {
  $("refreshBtn").addEventListener("click", () => {
    loadDashboard().catch(showError);
  });

  ["floorFilter", "riskFilter", "typeFilter"].forEach((id) => {
    $(id).addEventListener("change", () => {
      loadAbnormalTable().catch(showError);
    });
  });
}

function showError(error) {
  console.error(error);
  setStatus(false, "后端未连接");
  $("abnormalTable").innerHTML = `
    <tr>
      <td colspan="7" class="empty">无法连接后端，请先启动 backend/app.py</td>
    </tr>
  `;
}

bindEvents();
loadDashboard().catch(showError);
