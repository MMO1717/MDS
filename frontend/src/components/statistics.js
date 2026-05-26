window.EnergyApp = window.EnergyApp || {};
window.EnergyApp.components = window.EnergyApp.components || {};

window.EnergyApp.components.Statistics = function Statistics() {
  return `
    <section class="content-grid" id="stats">
      <div class="charts">
        <article class="panel chart-panel">
          <div class="panel-header">
            <h2 class="module-title"><span class="module-index">02</span>每日/每周能耗统计</h2>
            <span class="panel-note">今日分时用电折线图 · 单位：kWh / 小时</span>
          </div>
          <div class="chart-wrap">
            <canvas id="lineChart" width="900" height="280" aria-label="今日分时用电折线图"></canvas>
          </div>
        </article>

        <article class="panel chart-panel">
          <div class="panel-header">
            <h2>本周用电统计</h2>
            <span class="panel-note">周一至周日模拟数据</span>
          </div>
          <div class="chart-wrap">
            <canvas id="barChart" width="900" height="280" aria-label="本周用电柱状图"></canvas>
          </div>
        </article>
      </div>
      <aside class="side" id="rightSide"></aside>
    </section>
  `;
};

window.EnergyApp.components.renderCharts = function renderCharts(data) {
  const lineCanvas = document.getElementById("lineChart");
  const barCanvas = document.getElementById("barChart");

  if (lineCanvas) {
    window.EnergyApp.charts.drawLineChart(lineCanvas, data.hourlyUsage);
  }
  if (barCanvas) {
    window.EnergyApp.charts.drawBarChart(barCanvas, data.weeklyUsage);
  }
};
