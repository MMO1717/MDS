window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.Advice = function Advice(items) {
  return `
    <article class="panel" id="advice">
      <div class="panel-header">
        <h2 class="module-title"><span class="module-index">03</span>节能建议提示</h2>
        <span class="panel-note">智能提示</span>
      </div>
      <div class="advice-list">
        ${items.map((item) => `
          <div class="advice">
            <div class="advice-icon">${item.icon}</div>
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
