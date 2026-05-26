window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.ModuleStrip = function ModuleStrip() {
  const modules = [
    ["模块 01", "宿舍实时用电显示"],
    ["模块 02", "每日/每周能耗统计"],
    ["模块 03", "节能建议提示"],
    ["模块 04", "异常提醒通知"]
  ];

  return `
    <section class="module-strip" aria-label="学生端四项核心功能">
      ${modules.map(([index, title]) => `
        <div class="module-pill"><span>${index}</span><b>${title}</b></div>
      `).join("")}
    </section>
  `;
};
