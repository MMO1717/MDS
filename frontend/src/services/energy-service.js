window.EnergyApp = window.EnergyApp || {};

(function registerEnergyService(app) {
  function clone(data) {
    return JSON.parse(JSON.stringify(data));
  }

  function buildApiUrl(path) {
    return `${app.config.apiBaseUrl}${path}`;
  }

  async function request(url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`接口请求失败：${response.status}`);
    }
    return response.json();
  }

  async function loadJsonGroupFromStaticFiles() {
    const endpoints = app.config.endpoints;
    const [energyDetail, abnormalRecords, floorLoadSummary, peakPrediction, energySuggestions] =
      await Promise.all([
        request(endpoints.energyDetail),
        request(endpoints.abnormalRecords),
        request(endpoints.floorLoadSummary),
        request(endpoints.peakPrediction),
        request(endpoints.energySuggestions)
      ]);

    return { energyDetail, abnormalRecords, floorLoadSummary, peakPrediction, energySuggestions };
  }

  async function loadJsonGroupFromApi() {
    const endpoints = app.config.apiEndpoints;
    const [energyDetail, abnormalRecords, floorLoadSummary, peakPrediction, energySuggestions] =
      await Promise.all([
        request(buildApiUrl(endpoints.energyDetail)),
        request(buildApiUrl(endpoints.abnormalRecords)),
        request(buildApiUrl(endpoints.floorLoadSummary)),
        request(buildApiUrl(endpoints.peakPrediction)),
        request(buildApiUrl(endpoints.energySuggestions))
      ]);

    return { energyDetail, abnormalRecords, floorLoadSummary, peakPrediction, energySuggestions };
  }

  async function loadJsonGroup() {
    if (app.config.dataMode === "algorithmApi") {
      return loadJsonGroupFromApi();
    }

    if (app.config.dataMode === "demoMock") {
      return clone(app.demoData);
    }

    if (app.config.dataMode === "fallbackMock") {
      return clone(app.dataFiles);
    }

    return loadJsonGroupFromStaticFiles();
  }

  async function getDashboardData() {
    if (app.config.dataMode === "demoMock") {
      return clone(app.demoData);
    }

    const jsonGroup = await loadJsonGroup();
    const dashboard = app.dataAdapter.buildDashboardData(jsonGroup, app.config.defaultDormId);
    dashboard.realtime = await getRealtimeData(dashboard.realtime);
    return dashboard;
  }

  async function getRealtimeData(fallbackRealtime) {
    const fallback = fallbackRealtime || (await getDashboardDataWithoutPlug()).realtime;

    if (!app.config.plugMonitorEnabled) {
      return fallback;
    }

    try {
      const monitor = await request(app.config.plugMonitorUrl);
      return normalizePlugMonitor(monitor, fallback);
    } catch (error) {
      console.warn("智能插座实时接口不可用，已使用模拟数据。", error);
      return fallback;
    }
  }

  async function setPlugSwitch(on) {
    const url = on ? app.config.plugOnUrl : app.config.plugOffUrl;
    const response = await fetch(url, { method: "POST" });
    if (!response.ok) {
      throw new Error(`插座控制失败：${response.status}`);
    }
    return response.json();
  }

  async function getDashboardDataWithoutPlug() {
    if (app.config.dataMode === "demoMock") {
      return clone(app.demoData);
    }

    const jsonGroup = await loadJsonGroup();
    return app.dataAdapter.buildDashboardData(jsonGroup, app.config.defaultDormId);
  }

  function normalizePlugMonitor(monitor, fallback) {
    const power = Number(monitor.power || 0);
    const status = monitor.abnormalStatus
      ? monitor.abnormalType || "异常"
      : monitor.switchOn
        ? "正常"
        : "关闭";

    return {
      ...fallback,
      room: monitor.dormId || fallback.room,
      power,
      voltage: monitor.voltage,
      current: monitor.current,
      totalUsage: monitor.energy,
      loadRate: Math.min(100, Math.round((power / 1250) * 100)),
      switchOn: Boolean(monitor.switchOn),
      status
    };
  }

  app.energyService = {
    getDashboardData,
    getRealtimeData,
    setPlugSwitch
  };
})(window.EnergyApp);
