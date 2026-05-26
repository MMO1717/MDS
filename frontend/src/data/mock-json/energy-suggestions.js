window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.dataFiles = window.EnergyApp.dataFiles || {};

// 对应 JSON 文件 5：节能建议
window.EnergyApp.dataFiles.energySuggestions = [
  {
    scope: "building",
    target: "A栋",
    icon: "AI",
    title: "错峰用电建议",
    content: "晚间 19:00-23:00 为宿舍用电高峰，建议错峰使用部分电器。"
  },
  {
    scope: "room",
    target: "A101",
    icon: "%",
    title: "本周能耗上升",
    content: "本周用电量较上周上升 12%，建议减少空调空转和长时间待机。"
  },
  {
    scope: "room",
    target: "A201",
    icon: "!",
    title: "离寝断电提醒",
    content: "检测到无人时段仍存在持续耗电，建议离寝前关闭插排电源。"
  }
];
