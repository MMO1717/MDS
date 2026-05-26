# 教师端前端说明

本目录是宿舍能源协同管理系统的教师端 / 后勤管理端前端页面。

它是一个静态页面，不需要安装 Node.js、Vue 或其他依赖。页面会请求后端：

```text
http://localhost:8000
```

## 使用步骤

先启动教师端后端：

```powershell
cd "C:\Users\Sansuf\Desktop\学校资料\创新创业\MDS\backend"
C:\Users\Sansuf\miniconda3\python.exe app.py
```

再打开前端文件：

```text
frontend/index.html
```

也可以在浏览器地址栏输入本地文件路径打开。

## 页面功能

- 教师端首页统计卡片
- 当前楼层负载状态
- 宿舍累计能耗排行
- 异常宿舍报警表
- 按楼层、风险等级、异常类型筛选
- 高峰负载预测
- 节能建议列表

## 对接接口

主要使用：

- `GET /api/teacher/dashboard`
- `GET /api/teacher/abnormal`
- `GET /api/teacher/predictions`
- `GET /api/teacher/suggestions`

后端由 `backend/app.py` 提供。
