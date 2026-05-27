window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.Overview = function Overview() {
  return `
    <section class="manager-grid" id="overview">
      <article class="panel live-panel manager-hero">
        <div class="panel-header">
          <h2 class="module-title"><span class="module-index">01</span>教师端管理概览</h2>
          <span class="panel-note">实时读取后端 /api/teacher/dashboard</span>
        </div>
        <div class="overview-main">
          <div>
            <div class="room">当前楼栋：<span id="buildingInfo">A栋 / 5层</span></div>
            <div class="watts"><strong id="currentPower">--</strong><span>W</span></div>
            <div class="readout-meta">
              <span class="mini-chip">宿舍数量 <b id="dormCount">--</b></span>
              <span class="mini-chip">最新时刻 <b id="latestTime">--</b></span>
              <span class="mini-chip">异常记录 <b id="abnormalTotal">--</b> 条</span>
            </div>
          </div>
          <div class="risk-box">
            <span>当前异常</span>
            <strong id="currentAbnormal">--</strong>
            <p>其中高风险 <b id="highRiskCount">--</b> 条</p>
          </div>
        </div>
        <div class="metric-grid">
          <div class="metric">
            <label>累计用电</label>
            <strong id="totalEnergy">--</strong><span>kWh</span>
          </div>
          <div class="metric">
            <label>宿舍总数</label>
            <strong id="dormCountMirror">--</strong><span>间</span>
          </div>
          <div class="metric">
            <label>当前异常</label>
            <span class="status-text" id="currentAbnormalMirror">--</span>
          </div>
          <div class="metric">
            <label>数据角色</label>
            <strong class="role-text">教师端</strong>
          </div>
        </div>
      </article>

      <aside class="side">
        <article class="panel">
          <div class="panel-header">
            <h2 class="module-title"><span class="module-index">A</span>能耗排行</h2>
            <span class="panel-note">Top 10</span>
          </div>
          <div id="rankingList" class="ranking-list"></div>
        </article>
      </aside>
    </section>
  `;
};

window.EnergyTeacher.components.renderOverview = function renderOverview(overview, rankingItems) {
  setText("dormCount", overview.dorm_count);
  setText("dormCountMirror", overview.dorm_count);
  setText("buildingInfo", `${overview.building}栋 / ${overview.floor_count}层`);
  setText("currentPower", Number(overview.current_total_power || 0).toFixed(1));
  setText("latestTime", overview.latest_time);
  setText("currentAbnormal", overview.current_abnormal_count);
  setText("currentAbnormalMirror", overview.current_abnormal_count);
  setText("highRiskCount", overview.current_high_risk_count);
  setText("totalEnergy", Number(overview.total_energy || 0).toFixed(2));
  setText("abnormalTotal", overview.abnormal_record_count);

  const rankingList = document.getElementById("rankingList");
  rankingList.innerHTML = rankingItems.map((item, index) => `
    <div class="rank-item">
      <span class="rank-num">${index + 1}</span>
      <div>
        <strong>${item.dorm_id}</strong>
        <p>异常 ${item.abnormal_count} 条</p>
      </div>
      <b>${formatEnergy(item.energy)}</b>
    </div>
  `).join("");
};

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}
