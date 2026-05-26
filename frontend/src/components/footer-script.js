window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.FooterScript = function FooterScript() {
  return `
    <section class="footer-script">
      <b>答辩介绍：</b>我负责的是学生端网页。页面通过模拟 AIoT 智慧计量插座采集到的宿舍用电数据，展示当前功率、今日用电、本周用电、能耗趋势、节能建议和异常提醒。学生可以通过网页实时了解宿舍用电情况，并根据系统建议调整用电行为，从而实现节能和安全预警。
    </section>
  `;
};
