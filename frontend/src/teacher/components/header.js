window.EnergyTeacher = window.EnergyTeacher || {};
window.EnergyTeacher.components = window.EnergyTeacher.components || {};

window.EnergyTeacher.components.Header = function Header() {
  return `
    <header class="topbar">
      <div class="brand">
        <div class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M13 2 4 14h7l-1 8 9-12h-7l1-8Z"></path>
          </svg>
        </div>
        <div>
          <h1>AIoT 智慧宿舍能源管理端</h1>
          <p class="subtitle">教师端网页原型 · Spring Boot 后端 · 算法端 JSON 数据</p>
        </div>
      </div>

      <nav class="nav-links" aria-label="页面导航">
        <a href="#overview" class="active">管理概览</a>
        <a href="#floors">楼层负载</a>
        <a href="#plug">真实插座</a>
        <a href="#alerts">异常报警</a>
        <a href="#predictions">高峰预测</a>
        <a href="#suggestions">节能建议</a>
        <a href="#records">明细查询</a>
      </nav>

      <div class="top-actions">
        <div id="apiStatus" class="status-pill"><span class="pulse"></span> 连接中</div>
        <button id="refreshBtn" class="query-button" type="button">刷新</button>
      </div>
    </header>
  `;
};

window.EnergyTeacher.components.setApiStatus = function setApiStatus(online, text) {
  const status = document.getElementById("apiStatus");
  if (!status) return;
  status.innerHTML = `<span class="pulse"></span> ${text}`;
  status.classList.toggle("online", online);
  status.classList.toggle("offline", !online);
};


