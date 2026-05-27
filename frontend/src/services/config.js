window.EnergyApp = window.EnergyApp || {};

window.EnergyApp.config = {
  // staticJson: 读取算法端输出目录中的 5 个 JSON 文件
  // algorithmApi: 读取算法端 Flask 服务 http://localhost:5000/export/*.json
  // demoMock: 使用最初展示版模拟数据
  // fallbackMock: 使用 5 个 JSON 结构的小样例
  dataMode: "staticJson",
  defaultDormId: "A101",
  apiBaseUrl: "http://localhost:5000",
  plugMonitorEnabled: true,
  plugMonitorUrl: "http://localhost:8080/api/plug/monitor",
  plugOnUrl: "http://localhost:8080/api/plug/on",
  plugOffUrl: "http://localhost:8080/api/plug/off",
  endpoints: {
    energyDetail: "../algorithm/算法端输出/dorm_energy_data.json",
    abnormalRecords: "../algorithm/算法端输出/abnormal_list.json",
    floorLoadSummary: "../algorithm/算法端输出/floor_load_data.json",
    peakPrediction: "../algorithm/算法端输出/load_prediction_result.json",
    energySuggestions: "../algorithm/算法端输出/suggestion_data.json"
  },
  apiEndpoints: {
    energyDetail: "/export/dorm_energy_data.json",
    abnormalRecords: "/export/abnormal_list.json",
    floorLoadSummary: "/export/floor_load_data.json",
    peakPrediction: "/export/load_prediction_result.json",
    energySuggestions: "/export/suggestion_data.json"
  },
  refreshIntervalMs: 5000
};
