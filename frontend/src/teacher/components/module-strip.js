window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.ModuleStrip = function ModuleStrip() {
  const modules = [
    ["模块 01", "整栋宿舍能耗监控"],
    ["模块 02", "楼层负载状态显示"],
    ["模块 03", "真实插座监控控制"],
    ["模块 04", "异常提醒与节能建议"],
    ["模块 05", "宿舍用电明细查询"]
  ];

  return `
    <section class="module-strip teacher-module-strip" aria-label="教师端核心功能">
      ${modules.map(([index, title]) => `
        <div class="module-pill"><span>${index}</span><b>${title}</b></div>
      `).join("")}
    </section>
  `;
};
