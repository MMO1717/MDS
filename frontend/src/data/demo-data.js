window.EnergyApp = window.EnergyApp || {};

window.EnergyApp.demoData = {
  realtime: {
    room: "3栋502",
    roomType: "四人间",
    power: 785,
    todayUsage: 6.8,
    weekUsage: 42.5,
    voltage: 220.6,
    current: 3.56,
    totalUsage: 128.4,
    loadRate: 62,
    status: "正常",
    weekChangePercent: 12
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
  hourlyUsage: [
    { label: "00:00", value: 0.2 },
    { label: "04:00", value: 0.18 },
    { label: "08:00", value: 0.42 },
    { label: "12:00", value: 0.68 },
    { label: "16:00", value: 0.82 },
    { label: "20:00", value: 1.24 },
    { label: "23:00", value: 1.05 }
  ],
  weeklyUsage: [
    { label: "周一", value: 5.8 },
    { label: "周二", value: 6.2 },
    { label: "周三", value: 7.5 },
    { label: "周四", value: 6.9 },
    { label: "周五", value: 8.1 },
    { label: "周六", value: 9.3 },
    { label: "周日", value: 7.0 }
  ],
  advice: [
    {
      icon: "AI",
      title: "错峰用电建议",
      content: "晚间 19:00-23:00 为宿舍用电高峰，建议错峰使用部分电器。"
    },
    {
      icon: "%",
      title: "本周能耗上升",
      content: "本周用电量较上周上升 12%，建议减少空调空转和长时间待机。"
    },
    {
      icon: "!",
      title: "离寝断电提醒",
      content: "检测到无人时段仍存在持续耗电，建议离寝前关闭插排电源。"
    }
  ],
  alerts: [
    {
      time: "21:36",
      level: "danger",
      title: "疑似大功率电器，待确认",
      content: "瞬时功率超过宿舍安全阈值，系统已标记。"
    },
    {
      time: "23:10",
      level: "warning",
      title: "夜间异常用电，已提醒",
      content: "夜间持续功率偏高，建议检查未关闭设备。"
    },
    {
      time: "08:20",
      level: "ok",
      title: "无人宿舍持续耗电，已处理",
      content: "学生确认后关闭插排，状态恢复正常。"
    }
  ],
  energyRecords: [
    {
      dorm_id: "3栋502",
      floor: "",
      time: "",
      power: 785,
      energy: 6.8,
      occupied: "",
      temperature: "",
      abnormal_status: "normal",
      abnormal_type: "",
      risk_level: "低",
      suggestion: ""
    }
  ],
  floorLoadSummary: [],
  peakPrediction: []
};
