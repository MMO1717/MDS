window.EnergyApp = window.EnergyApp || {};

(function registerCharts(app) {
  function fitCanvas(canvas) {
    const ratio = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = Math.floor(rect.width * ratio);
    canvas.height = Math.floor(rect.height * ratio);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    return { ctx, width: rect.width, height: rect.height };
  }

  function drawAxes(ctx, width, height, padding) {
    ctx.strokeStyle = "#e6edf5";
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + ((height - padding.top - padding.bottom) / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();
    }
  }

  function drawLineChart(canvas, data) {
    const { ctx, width, height } = fitCanvas(canvas);
    const padding = { top: 18, right: 22, bottom: 32, left: 36 };
    const max = Math.max(...data.map((item) => item.value), 1) * 1.15;

    ctx.clearRect(0, 0, width, height);
    drawAxes(ctx, width, height, padding);

    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;
    const points = data.map((item, index) => {
      const x = padding.left + (chartW / (data.length - 1)) * index;
      const y = padding.top + chartH - (item.value / max) * chartH;
      return { ...item, x, y };
    });

    const gradient = ctx.createLinearGradient(0, padding.top, 0, height - padding.bottom);
    gradient.addColorStop(0, "rgba(37,99,235,0.16)");
    gradient.addColorStop(1, "rgba(37,99,235,0)");

    ctx.beginPath();
    points.forEach((point, index) => {
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.lineTo(points[points.length - 1].x, height - padding.bottom);
    ctx.lineTo(points[0].x, height - padding.bottom);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();

    ctx.beginPath();
    points.forEach((point, index) => {
      if (index === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    });
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 3;
    ctx.stroke();

    ctx.fillStyle = "#2563eb";
    ctx.font = "12px Arial";
    points.forEach((point) => {
      ctx.beginPath();
      ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = "#687586";
      ctx.fillText(point.label, point.x - 14, height - 10);
      ctx.fillStyle = "#2563eb";
    });
  }

  function drawBarChart(canvas, data) {
    const { ctx, width, height } = fitCanvas(canvas);
    const padding = { top: 18, right: 22, bottom: 32, left: 36 };
    const max = Math.max(...data.map((item) => item.value), 1) * 1.1;

    ctx.clearRect(0, 0, width, height);
    drawAxes(ctx, width, height, padding);

    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;
    const gap = 16;
    const barW = Math.max(22, (chartW - gap * (data.length - 1)) / data.length);

    data.forEach((item, index) => {
      const x = padding.left + index * (barW + gap);
      const barH = (item.value / max) * chartH;
      const y = padding.top + chartH - barH;
      const gradient = ctx.createLinearGradient(0, y, 0, y + barH);
      gradient.addColorStop(0, "#18a66a");
      gradient.addColorStop(1, "#0ea5b7");

      ctx.fillStyle = "#f3f7fb";
      ctx.beginPath();
      roundRect(ctx, x, padding.top, barW, chartH, 6);
      ctx.fill();

      ctx.fillStyle = gradient;
      ctx.beginPath();
      roundRect(ctx, x, y, barW, barH, 6);
      ctx.fill();

      ctx.fillStyle = "#17212b";
      ctx.font = "12px Arial";
      ctx.textAlign = "center";
      ctx.fillText(item.value.toFixed(1), x + barW / 2, y - 8);
      ctx.fillStyle = "#687586";
      ctx.fillText(item.label, x + barW / 2, height - 10);
    });
    ctx.textAlign = "left";
  }

  function roundRect(ctx, x, y, width, height, radius) {
    const r = Math.min(radius, width / 2, height / 2);
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + width, y, x + width, y + height, r);
    ctx.arcTo(x + width, y + height, x, y + height, r);
    ctx.arcTo(x, y + height, x, y, r);
    ctx.arcTo(x, y, x + width, y, r);
    ctx.closePath();
  }

  app.charts = {
    drawLineChart,
    drawBarChart
  };
})(window.EnergyApp);
