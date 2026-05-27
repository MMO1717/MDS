window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.ModuleStrip = function ModuleStrip() {
  const modules = [
    ["模块 01", "整栋宿舍能耗监控"],
    ["模块 02", "楼层负载状态显示"],
    ["模块 03", "异常宿舍报警筛选"],
    ["模块 04", "高峰负载与节能建议"]
  ];

  return `
    <section class="module-strip" aria-label="教师端核心功能">
      ${modules.map(([index, title]) => `
        <div class="module-pill"><span>${index}</span><b>${title}</b></div>
      `).join("")}
    </section>
  `;
};
