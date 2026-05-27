window.EnergyTeacher = window.EnergyTeacher || {};

(function registerTeacherService(app) {
  function buildUrl(path) {
    return `${app.config.apiBaseUrl}${path}`;
  }

  async function request(path) {
    const response = await fetch(buildUrl(path));
    if (!response.ok) {
      throw new Error(`接口请求失败：${response.status}`);
    }
    return response.json();
  }

  function buildAbnormalQuery(filters = {}) {
    const params = new URLSearchParams({
      page: "1",
      page_size: "12"
    });

    if (filters.floor) params.set("floor", filters.floor);
    if (filters.riskLevel) params.set("risk_level", filters.riskLevel);
    if (filters.abnormalType) params.set("abnormal_type", filters.abnormalType);

    return `/api/teacher/abnormal?${params.toString()}`;
  }

  app.teacherService = {
    getDashboard() {
      return request("/api/teacher/dashboard?limit=10");
    },
    getAbnormalRecords(filters) {
      return request(buildAbnormalQuery(filters));
    },
    getHighRiskPredictions() {
      return request("/api/teacher/predictions?risk_level=高&page=1&page_size=8");
    },
    getSuggestions() {
      return request("/api/teacher/suggestions?page=1&page_size=8");
    }
  };
})(window.EnergyTeacher);
