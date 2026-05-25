window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.dataFiles = window.EnergyApp.dataFiles || {};

// 对应 JSON 文件 2：异常记录（筛选过的）
window.EnergyApp.dataFiles.abnormalRecords = [
  {
    dorm_id: "A305",
    time: "21:36",
    timestamp: "2026-05-20 21:36:00",
    abnormal_type: "高功率违规",
    risk_level: "高",
    message: "疑似大功率电器，待确认",
    suggestion: "瞬时功率超过宿舍安全阈值，建议管理员核查。",
    read: false
  },
  {
    dorm_id: "A201",
    time: "23:10",
    timestamp: "2026-05-20 23:10:00",
    abnormal_type: "无人耗电",
    risk_level: "中",
    message: "夜间异常用电，已提醒",
    suggestion: "夜间持续功率偏高，建议检查未关闭设备。",
    read: false
  },
  {
    dorm_id: "A101",
    time: "08:20",
    timestamp: "2026-05-21 08:20:00",
    abnormal_type: "无人耗电",
    risk_level: "低",
    message: "无人宿舍持续耗电，已处理",
    suggestion: "学生确认后关闭插排，状态恢复正常。",
    read: true
  }
];
