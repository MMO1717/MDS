window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.FloorLoad = function FloorLoad() {
  return `
    <section class="panel floor-panel" id="floors">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">02</span>楼层负载状态</h2>
        <span class="panel-note">按楼层聚合当前负载和异常数量</span>
      </div>
      <div id="floorCards" class="module-strip floor-strip"></div>
    </section>
  `;
};

window.EnergyTeacher.components.renderFloorLoad = function renderFloorLoad(floors) {
  document.getElementById("floorCards").innerHTML = floors.map((item) => `
    <article class="module-pill floor-card">
      <span>${item.floor}楼</span>
      <strong>${formatPower(item.floor_total_power)}</strong>
      <span class="risk-tag ${riskClass(item.risk_level)}">${item.risk_level}</span>
      <p>异常记录 ${item.abnormal_count} 条</p>
    </article>
  `).join("");
};
