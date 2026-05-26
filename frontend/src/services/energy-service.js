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
    return app.dataAdapter.buildDashboardData(jsonGroup, app.config.defaultDormId);
  }

  async function getRealtimeData() {
    const dashboard = await getDashboardData();
    return dashboard.realtime;
  }

  app.energyService = {
    getDashboardData,
    getRealtimeData
  };
})(window.EnergyApp);
