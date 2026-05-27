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
    PlugMonitor,
    renderPlugMonitor,
    renderPlugError,
    attachPlugControl,
    Alerts,
    attachAlertFilters,
    renderAlerts,
    Insights,
    renderInsights,
    RecordsQuery,
    attachRecordQuery,
    renderRecords
  } = app.components;

  try {
    root.innerHTML = `
      <main class="app">
        ${Header()}
        ${ModuleStrip()}
        ${Overview()}
        ${FloorLoad()}
        ${PlugMonitor()}
        ${Alerts()}
        ${Insights()}
        ${RecordsQuery()}
        <section class="footer-script">
          <b>教师端说明：</b>本页面现在同时具备学生端的实时插座监控、开关控制、节能建议、异常提醒和明细查询能力；教师端额外保留楼层负载、能耗排行和整栋统计。
        </section>
      </main>
    `;

    async function refreshDashboard() {
      app.components.setApiStatus(false, "连接中");

      const [dashboard, abnormal, predictions, suggestions, records] = await Promise.all([
        app.teacherService.getDashboard(),
        app.teacherService.getAbnormalRecords(app.components.getAlertFilters()),
        app.teacherService.getHighRiskPredictions(),
        app.teacherService.getSuggestions(),
        app.teacherService.getDormRecords(app.components.getRecordFilters())
      ]);

      renderOverview(dashboard.overview, dashboard.top_energy_dorms);
      renderFloorLoad(dashboard.floor_summary);
      renderAlerts(abnormal.data);
      renderInsights(predictions.data, suggestions.data);
      renderRecords(records);
      app.components.setApiStatus(true, "后端已连接");
    }

    async function refreshAlerts() {
      const abnormal = await app.teacherService.getAbnormalRecords(app.components.getAlertFilters());
      renderAlerts(abnormal.data);
    }

    async function refreshRecords() {
      const records = await app.teacherService.getDormRecords(app.components.getRecordFilters());
      renderRecords(records);
    }

    async function refreshPlug() {
      try {
        const monitor = await app.teacherService.getPlugMonitor();
        renderPlugMonitor(monitor);
      } catch (error) {
        console.warn("真实插座接口不可用", error);
        renderPlugError("无法读取真实插座，请确认 Tuya 密钥、device_id 和网络连接。 ");
      }
    }

    document.getElementById("refreshBtn").addEventListener("click", () => {
      Promise.all([refreshDashboard(), refreshPlug()]).catch(showError);
    });

    attachAlertFilters(() => refreshAlerts().catch(showError));
    attachRecordQuery(() => refreshRecords().catch(showError));
    attachPlugControl(async (nextSwitch) => {
      await app.teacherService.setPlugSwitch(nextSwitch);
      await refreshPlug();
    });

    await refreshDashboard();
    await refreshPlug();
    setInterval(refreshPlug, app.config.refreshIntervalMs);
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
