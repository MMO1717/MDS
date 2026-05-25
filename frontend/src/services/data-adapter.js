window.EnergyApp = window.EnergyApp || {};

(function registerDataAdapter(app) {
  function latestRecord(records, dormId) {
    const filtered = records.filter((record) => record.dorm_id === dormId);
    return filtered[filtered.length - 1] || records[records.length - 1];
  }

  function mapRiskToStatus(record) {
    if (!record.abnormal_status || record.abnormal_status === "normal") return "正常";
    if (record.risk_level === "高") return "异常";
    return "高耗电";
  }

  function mapRiskToNoticeLevel(riskLevel) {
    if (riskLevel === "高") return "danger";
    if (riskLevel === "中") return "warning";
    return "ok";
  }

  function buildHourlyUsage(records, dormId) {
    const roomRecords = records.filter((record) => record.dorm_id === dormId);
    const recentRecords = roomRecords.slice(-48);
    const sampledRecords = recentRecords.filter((_, index) => index % 6 === 0 || index === recentRecords.length - 1);

    return sampledRecords.map((record) => ({
      label: formatTime(record.time),
      value: Number((record.power / 1000 / 2).toFixed(2))
    }));
  }

  function buildWeeklyUsage(records, dormId) {
    const byDate = new Map();
    records
      .filter((record) => record.dorm_id === dormId)
      .forEach((record) => {
        const date = record.time.slice(5, 10);
        const value = byDate.get(date) || 0;
        byDate.set(date, value + record.power / 1000 / 2);
      });

    return Array.from(byDate.entries()).slice(-7).map(([date, value]) => ({
      label: date,
      value: Number(value.toFixed(1))
    }));
  }

  function formatTime(time) {
    return time ? time.slice(11, 16) : "";
  }

  function uniqueSuggestions(items, dormId) {
    const seen = new Set();
    return items
      .filter((item) => item.dorm_id === dormId || item.risk_level !== "低")
      .filter((item) => {
        const key = `${item.abnormal_type}-${item.suggestion}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      })
      .slice(0, 3);
  }

  function buildDashboardData(dataFiles, dormId = "A101") {
    const current = latestRecord(dataFiles.energyDetail, dormId);
    const loadRate = Math.min(100, Math.round((current.power / 1250) * 100));

    return {
      realtime: {
        room: current.dorm_id,
        roomType: "四人间",
        power: current.power,
        todayUsage: Number((current.energy || 0).toFixed(1)),
        weekUsage: buildWeeklyUsage(dataFiles.energyDetail, dormId)
          .reduce((sum, item) => sum + item.value, 0)
          .toFixed(1),
        voltage: "",
        current: "",
        totalUsage: current.energy,
        loadRate,
        status: mapRiskToStatus(current),
        weekChangePercent: ""
      },
      hardware: [
        {
          title: "ESP32 控制模块",
          description: "负责 Wi-Fi 联网、数据读取与 MQTT 上传。",
          tag: "在线",
          icon: "chip"
        },
        {
          title: "PZEM-004T 电能计量模块",
          description: "采集电压、电流、实时功率、累计电量。",
          tag: "采集中",
          icon: "meter"
        },
        {
          title: "智慧计量插座 / 宿舍采集模块",
          description: "将宿舍用电数据同步到学生端网页平台。",
          tag: "模拟",
          icon: "wifi"
        }
      ],
      hourlyUsage: buildHourlyUsage(dataFiles.energyDetail, dormId),
      weeklyUsage: buildWeeklyUsage(dataFiles.energyDetail, dormId),
      advice: uniqueSuggestions(dataFiles.energySuggestions, dormId).map((item, index) => ({
        icon: index === 0 ? "AI" : index === 1 ? "%" : "!",
        title: item.abnormal_type || "节能建议",
        content: item.suggestion
      })),
      alerts: dataFiles.abnormalRecords.slice(-3).reverse().map((item) => ({
        time: formatTime(item.time),
        level: mapRiskToNoticeLevel(item.risk_level),
        title: item.abnormal_type,
        content: item.suggestion
      })),
      energyRecords: dataFiles.energyDetail,
      floorLoadSummary: dataFiles.floorLoadSummary,
      peakPrediction: dataFiles.peakPrediction
    };
  }

  app.dataAdapter = {
    buildDashboardData
  };
})(window.EnergyApp);
