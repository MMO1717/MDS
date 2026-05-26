# 前端说明

本目录包含宿舍能源协同管理系统的两个静态前端入口：

- `index.html`：教师端 / 后勤管理端页面
- `student.html`：学生端网页原型

两个页面都可以直接用浏览器打开，不需要安装 Node.js、Vue 或其他前端依赖。

## 教师端

教师端页面会请求本地后端：

```text
http://localhost:8000
```

先启动教师端后端：

```powershell
cd "C:\Users\Sansuf\Desktop\学校资料\创新创业\MDS\backend"
C:\Users\Sansuf\miniconda3\python.exe app.py
```

再打开：

```text
frontend/index.html
```

主要功能：

- 教师端首页统计卡片
- 当前楼层负载状态
- 宿舍累计能耗排行
- 异常宿舍报警表
- 按楼层、风险等级、异常类型筛选
- 高峰负载预测
- 节能建议列表

主要接口：

- `GET /api/teacher/dashboard`
- `GET /api/teacher/abnormal`
- `GET /api/teacher/predictions`
- `GET /api/teacher/suggestions`

后端由 `backend/app.py` 提供。

## 学生端

学生端是“基于物联网的高校宿舍智能能源协同管理系统”的网页原型。当前版本不接真实硬件、不接数据库、不做登录，使用前端模拟数据完成中期展示。

打开：

```text
frontend/student.html
```

目录结构：

```text
student.html                 页面入口
src/styles/main.css          页面样式
src/app.js                   应用初始化和页面组装
src/components/              页面区块组件
src/data/mock-json/          按 5 个 JSON 文件拆分的模拟数据
src/services/config.js       数据源配置
src/services/data-adapter.js 算法 JSON 数据到页面数据的转换层
src/services/energy-service.js 数据服务层
src/utils/charts.js          canvas 图表绘制
```

模拟数据文件：

```text
src/data/mock-json/energy-detail.js        宿舍用电明细主表
src/data/mock-json/abnormal-records.js     异常记录
src/data/mock-json/floor-load-summary.js   楼层负载汇总
src/data/mock-json/peak-prediction.js      高峰预测
src/data/mock-json/energy-suggestions.js   节能建议
```

核心模块：

- 宿舍实时用电显示
- 每日/每周能耗统计
- 节能建议提示
- 异常提醒通知

后续如果有后端接口，可以修改 `src/services/config.js`：

```js
useMockData: false,
apiBaseUrl: "http://你的后端地址/api"
```

建议接口方向：

- `GET /student/dashboard`：一次性返回页面所有数据
- `GET /student/realtime`：返回当前功率、电压、电流、状态等实时数据
- `GET /student/statistics`：返回今日分时用电、本周用电
- `GET /student/advice`：返回节能建议
- `GET /student/alerts`：返回异常提醒
