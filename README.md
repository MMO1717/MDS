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
├── backend/            # 后端（待开发）
├── frontend/           # 前端（待开发）
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

待开发

## 前端

待开发
