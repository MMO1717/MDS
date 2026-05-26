window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.dataFiles = window.EnergyApp.dataFiles || {};

// 对应 JSON 文件 1：宿舍用电明细（主表）
window.EnergyApp.dataFiles.energyDetail = [
  {
    dorm_id: "A101",
    timestamp: "2026-05-21 08:00:00",
    power: 420,
    energy: 126.8,
    occupied: true,
    temperature: 26.4,
    abnormal_status: false,
    abnormal_type: "",
    risk_level: "低",
    suggestion: "当前用电正常，保持良好用电习惯。"
  },
  {
    dorm_id: "A101",
    timestamp: "2026-05-21 08:30:00",
    power: 785,
    energy: 127.2,
    occupied: true,
    temperature: 27.1,
    abnormal_status: false,
    abnormal_type: "",
    risk_level: "低",
    suggestion: "当前用电正常，建议离寝前关闭插排电源。"
  },
  {
    dorm_id: "A201",
    timestamp: "2026-05-21 08:30:00",
    power: 1480,
    energy: 139.5,
    occupied: false,
    temperature: 28.6,
    abnormal_status: true,
    abnormal_type: "无人耗电",
    risk_level: "中",
    suggestion: "疑似无人时段持续耗电，建议联系宿舍成员确认电器状态。"
  },
  {
    dorm_id: "A305",
    timestamp: "2026-05-21 08:30:00",
    power: 2320,
    energy: 158.9,
    occupied: true,
    temperature: 29.4,
    abnormal_status: true,
    abnormal_type: "高功率违规",
    risk_level: "高",
    suggestion: "瞬时功率过高，建议立即检查是否存在违规大功率电器。"
  }
];
