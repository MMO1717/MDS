window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.dataFiles = window.EnergyApp.dataFiles || {};

// 对应 JSON 文件 4：高峰预测
window.EnergyApp.dataFiles.peakPrediction = [
  { time_range: "19:00-20:00", predicted_power: 8600, risk_level: "中" },
  { time_range: "20:00-21:00", predicted_power: 9800, risk_level: "中" },
  { time_range: "21:00-22:00", predicted_power: 12600, risk_level: "高" },
  { time_range: "22:00-23:00", predicted_power: 11200, risk_level: "高" }
];
