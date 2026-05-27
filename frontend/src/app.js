window.EnergyApp = window.EnergyApp || {};

(async function bootstrap(app) {
  const root = document.getElementById("app");
  const {
    Header,
    ModuleStrip,
    LivePower,
    DataSource,
    Statistics,
    Advice,
    Alerts,
    EnergyQuery,
    attachEnergyQuery,
    attachPlugControl,
    updateLivePower,
    renderCharts
  } = app.components;

  try {
    const data = await app.energyService.getDashboardData();

    root.innerHTML = `
      <main class="app">
        ${Header()}
        ${ModuleStrip()}
        <section class="hero-grid">
          ${LivePower(data.realtime)}
          ${DataSource(data.hardware)}
        </section>
        ${Statistics()}
        ${EnergyQuery(data.energyRecords)}
      </main>
    `;

    document.getElementById("rightSide").innerHTML = `
      ${Advice(data.advice)}
      ${Alerts(data.alerts)}
    `;

    updateLivePower(data.realtime);
    renderCharts(data);
    attachEnergyQuery(data.energyRecords);

    async function refreshRealtime() {
      const realtime = await app.energyService.getRealtimeData(data.realtime);
      updateLivePower(realtime);
      data.realtime = realtime;
    }

    attachPlugControl(refreshRealtime);

    window.addEventListener("resize", () => renderCharts(data));

    setInterval(refreshRealtime, app.config.refreshIntervalMs);
  } catch (error) {
    root.innerHTML = `
      <main class="app">
        <section class="panel footer-script">
          <b>页面加载失败：</b>${error.message}
        </section>
      </main>
    `;
  }
})(window.EnergyApp);
