# Frontend - Teacher Page

本目录是宿舍能源协同管理系统的教师端 / 后勤管理端前端页面。

实现方式已经调整为和学生端一致：

- `index.html` 只作为入口文件
- `src/styles/main.css` 存放页面样式
- `src/teacher/services/` 存放接口配置和请求逻辑
- `src/teacher/components/` 存放页面组件
- `src/teacher/app.js` 负责组装页面和绑定事件

## 使用步骤

先启动教师端后端：

```powershell
cd "C:\Users\Sansuf\Desktop\school information\chuangXin\MDS\backend"
mvn spring-boot:run
```

再打开前端文件：

```text
frontend/index.html
```

页面默认请求：

```text
http://localhost:8080
```

配置位置：

```text
frontend/src/teacher/services/config.js
```

## 页面功能

- 教师端首页统计卡片
- 当前楼层负载状态
- 宿舍累计能耗排行
- 真实插座实时监控与开关控制
- 异常宿舍报警表
- 按楼层、风险等级、异常类型筛选
- 高峰负载预测
- 节能建议列表
- 宿舍用电明细查询

## 对接接口

主要使用：

- `GET /api/teacher/dashboard`
- `GET /api/teacher/abnormal`
- `GET /api/teacher/predictions`
- `GET /api/teacher/suggestions`
- `GET /api/teacher/dorms`
- `GET /api/plug/monitor`
- `POST /api/plug/on`
- `POST /api/plug/off`

后端由 `backend` 目录下的 Spring Boot 服务提供。
