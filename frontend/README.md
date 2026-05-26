# AIoT 智慧宿舍能源助手

这是“基于物联网的高校宿舍智能能源协同管理系统”的学生端网页原型。

当前版本不接真实硬件、不接数据库、不做登录，使用前端模拟数据完成中期展示。项目已拆成多个区块组件，方便后续对接后端接口或 AIoT 数据平台。

## 目录结构

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

## 数据文件结构

当前前端按算法端提供的 5 类 JSON 数据拆分：

```text
src/data/mock-json/energy-detail.js        宿舍用电明细主表
src/data/mock-json/abnormal-records.js     异常记录
src/data/mock-json/floor-load-summary.js   楼层负载汇总
src/data/mock-json/peak-prediction.js      高峰预测
src/data/mock-json/energy-suggestions.js   节能建议
```

## 四个核心模块

- 宿舍实时用电显示
- 每日/每周能耗统计
- 节能建议提示
- 异常提醒通知

## 后续接入真实数据

现在默认使用模拟数据：

```js
useMockData: true
```

以后如果有后端接口，只需要修改 `src/services/config.js`：

```js
useMockData: false,
apiBaseUrl: "http://你的后端地址/api"
```

并让后端接口返回与 `src/data/mock-json/` 中字段类似的数据结构即可。页面组件不用大改。

## 建议接口方向

- `GET /student/dashboard`：一次性返回页面所有数据
- `GET /student/realtime`：返回当前功率、电压、电流、状态等实时数据
- `GET /student/statistics`：返回今日分时用电、本周用电
- `GET /student/advice`：返回节能建议
- `GET /student/alerts`：返回异常提醒
