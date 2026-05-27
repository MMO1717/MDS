window.EnergyTeacher = window.EnergyTeacher || {};

(async function bootstrap(app) {
  const root = document.getElementById("app");
  const {
    Header,
    ModuleStrip,
    Overview,
    renderOverview,
    FloorLoad,
    renderFloorLoad,
    Alerts,
    attachAlertFilters,
    renderAlerts,
    Insights,
    renderInsights
  } = app.components;

  try {
    root.innerHTML = `
      <main class="app">
        ${Header()}
        ${ModuleStrip()}
        ${Overview()}
        ${FloorLoad()}
        ${Alerts()}
        ${Insights()}
        <section class="footer-script">
          <b>教师端说明：</b>本页面只负责管理端展示和查询；异常判断、风险等级和建议文本均来自算法端输出，后端负责读取、筛选和统计。
        </section>
      </main>
    `;

    async function refreshDashboard() {
      app.components.setApiStatus(false, "连接中");

      const [dashboard, abnormal, predictions, suggestions] = await Promise.all([
        app.teacherService.getDashboard(),
        app.teacherService.getAbnormalRecords(app.components.getAlertFilters()),
        app.teacherService.getHighRiskPredictions(),
        app.teacherService.getSuggestions()
      ]);

      renderOverview(dashboard.overview, dashboard.top_energy_dorms);
      renderFloorLoad(dashboard.floor_summary);
      renderAlerts(abnormal.data);
      renderInsights(predictions.data, suggestions.data);
      app.components.setApiStatus(true, "后端已连接");
    }

    async function refreshAlerts() {
      const abnormal = await app.teacherService.getAbnormalRecords(app.components.getAlertFilters());
      renderAlerts(abnormal.data);
    }

    document.getElementById("refreshBtn").addEventListener("click", () => {
      refreshDashboard().catch(showError);
    });

    attachAlertFilters(() => refreshAlerts().catch(showError));
    await refreshDashboard();
  } catch (error) {
    root.innerHTML = `
      <main class="app">
        <section class="panel footer-script">
          <b>页面加载失败：</b>${error.message}
        </section>
      </main>
    `;
  }

  function showError(error) {
    console.error(error);
    app.components.setApiStatus(false, "后端未连接");
    const body = document.getElementById("abnormalTable");
    if (body) {
      body.innerHTML = `
        <tr>
          <td colspan="7" class="empty">无法连接后端，请先启动 Spring Boot 后端。</td>
        </tr>
      `;
    }
  }
})(window.EnergyTeacher);
