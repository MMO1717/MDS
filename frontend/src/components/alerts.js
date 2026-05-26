window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.Alerts = function Alerts(items) {
  return `
    <article class="panel" id="alerts">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">04</span>异常提醒通知</h2>
        <span class="panel-note">今日 ${items.length} 条</span>
      </div>
      <div class="notice-list">
        ${items.map((item) => `
          <div class="notice ${item.level}">
            <div class="time">${item.time}</div>
            <div>
              <b>${item.title}</b>
              <p>${item.content}</p>
            </div>
          </div>
        `).join("")}
      </div>
    </article>
  `;
};
