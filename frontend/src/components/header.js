window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.Header = function Header() {
  return `
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"></path>
          </svg>
        </div>
        <div>
          <h1>AIoT 智慧宿舍能源助手</h1>
          <p class="subtitle">学生端网页原型 · 模拟 AIoT 智慧计量插座采集数据 · 中期展示版</p>
        </div>
      </div>
      <nav class="nav-links" aria-label="页面导航">
        <a href="#live" class="active">用电概览</a>
        <a href="#stats">能耗统计</a>
        <a href="#advice">节能建议</a>
        <a href="#alerts">异常提醒</a>
        <a href="#records">明细查询</a>
      </nav>
      <div class="status-pill"><span class="pulse"></span> 设备在线 · MQTT 模拟连接</div>
    </header>
  `;
};
