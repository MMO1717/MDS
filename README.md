# MDS - 宿舍能源协同管理系统

## 项目结构

```
MDS/
├── algorithm/          # 算法端
│   ├── config.py       # 配置
│   ├── data_source.py  # 数据源
│   ├── collector.py    # 数据采集
│   ├── anomaly_detector.py  # 异常检测
│   ├── app.py          # API服务
│   ├── generate_data.py # 数据生成
│   └── 算法端输出/      # JSON数据和文档
├── backend/            # 教师端后端（Spring Boot）
│   ├── pom.xml
│   └── src/main/
├── frontend/           # 教师端前端（静态组件化页面）
│   ├── index.html
│   └── src/
└── README.md
```

## 算法端

提供宿舍用电数据采集、异常检测、负载预测等功能。

### 启动

```bash
cd algorithm
python3 app.py
```

### API文档

详见 `algorithm/算法端输出/API对接文档.md`

## 后端

教师端后端采用 Spring Boot，与学生端后端保持一致的 Maven 项目结构。

### 启动

```bash
cd backend
mvn spring-boot:run
```

服务地址：

```text
http://localhost:8080
```

主要接口：

```text
GET /api/teacher/dashboard
GET /api/teacher/abnormal
GET /api/teacher/predictions
GET /api/teacher/suggestions
```

## 前端

教师端前端采用和学生端一致的静态组件化结构：

```text
frontend/index.html
frontend/src/styles/main.css
frontend/src/teacher/services/
frontend/src/teacher/components/
frontend/src/teacher/app.js
```

启动后端后，直接打开：

```text
frontend/index.html
```
