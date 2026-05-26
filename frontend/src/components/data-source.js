window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.DataSource = function DataSource(hardware) {
  const iconMap = {
    chip: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="4" y="4" width="16" height="16" rx="2"></rect>
        <path d="M9 9h6v6H9z"></path>
        <path d="M9 1v3M15 1v3M9 20v3M15 20v3M1 9h3M1 15h3M20 9h3M20 15h3"></path>
      </svg>
    `,
    meter: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M6 7h12v10H6z"></path>
        <path d="M9 7V4h6v3M9 17v3h6v-3"></path>
        <path d="M10 12h4"></path>
      </svg>
    `,
    wifi: `
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M5 12.55a11 11 0 0 1 14.08 0"></path>
        <path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path>
        <path d="M12 20h.01"></path>
        <path d="M2 8.82a16 16 0 0 1 20 0"></path>
      </svg>
    `
  };

  return `
    <aside class="panel hardware">
      <div class="panel-header">
        <h2>AIoT 数据来源</h2>
        <span class="panel-note">硬件端展示包装</span>
      </div>
      <div class="device-map">
        ${hardware.map((item) => `
          <div class="device-node">
            <div class="node-icon" aria-hidden="true">${iconMap[item.icon] || iconMap.wifi}</div>
            <div>
              <h3>${item.title}</h3>
              <p>${item.description}</p>
            </div>
            <span class="node-tag">${item.tag}</span>
          </div>
        `).join("")}
      </div>
      <div class="signal">
        本原型暂不接入真实硬件、不使用数据库，通过前端模拟数据展示学生端核心功能，适用于中期答辩演示。
      </div>
    </aside>
  `;
};
