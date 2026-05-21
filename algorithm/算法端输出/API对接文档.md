# 算法端 API 对接文档

## 概述

算法端提供两种数据获取方式：
1. **静态JSON文件** — 直接使用 `算法端输出/` 目录下的5个JSON文件
2. **实时API服务** — 启动 `python3 app.py` 后通过HTTP接口获取实时数据

---

## 快速开始

### 方式一：使用静态JSON（简单直接）

直接读取 `算法端输出/` 目录下的JSON文件：
- `dorm_energy_data.json` — 宿舍用电数据
- `abnormal_list.json` — 异常列表
- `floor_load_data.json` — 楼层负载
- `load_prediction_result.json` — 高峰预测
- `suggestion_data.json` — 节能建议

### 方式二：使用实时API（推荐）

```bash
# 启动服务
python3 app.py

# 服务地址
http://localhost:5000
```

---

## API 接口列表

### 兼容接口（推荐，返回格式与静态JSON一致）

| 接口 | 说明 | 返回格式 |
|------|------|---------|
| `GET /export/dorm_energy_data.json` | 宿舍用电数据 | `[{...}, ...]` |
| `GET /export/abnormal_list.json` | 异常列表 | `[{...}, ...]` |
| `GET /export/floor_load_data.json` | 楼层负载 | `[{...}, ...]` |
| `GET /export/load_prediction_result.json` | 高峰预测 | `[{...}, ...]` |
| `GET /export/suggestion_data.json` | 节能建议 | `[{...}, ...]` |

> 这些接口返回的数据格式与静态JSON文件完全一致，可直接替换。

### 查询接口（带分页包装）

| 接口 | 说明 |
|------|------|
| `GET /api/dorms` | 所有宿舍当前状态 |
| `GET /api/dorms/A101` | 单个宿舍详情 |
| `GET /api/abnormal` | 当前异常列表 |
| `GET /api/floor-load` | 楼层负载数据 |
| `GET /api/predictions` | 高峰预测结果 |
| `GET /api/suggestions` | 节能建议 |
| `GET /api/events` | 功率突变事件日志 |
| `GET /api/status` | 系统运行状态 |

> 返回格式：`{"count": 数量, "data": [...]}`

### 数据上报接口

```
POST /api/data
Content-Type: application/json

# 单条上报
{"dorm_id": "A101", "power": 850.0, "occupied": true, "temperature": 26.5}

# 批量上报
[
  {"dorm_id": "A101", "power": 850.0},
  {"dorm_id": "A102", "power": 320.0}
]
```

---

## 数据字段说明

### 宿舍用电数据

| 字段 | 类型 | 说明 |
|------|------|------|
| dorm_id | string | 宿舍编号，如 A101 |
| floor | int | 楼层（1-5） |
| time | string | 时间（YYYY-MM-DD HH:MM:SS） |
| power | float | 当前功率（W） |
| energy | float | 累计能耗（kWh） |
| temperature | float | 温度（°C） |
| occupied | bool | 是否有人 |
| abnormal_status | string | normal / abnormal |
| abnormal_type | string | 异常类型 |
| risk_level | string | 低 / 中 / 高 |
| suggestion | string | 建议文本 |

### 楼层负载

| 字段 | 类型 | 说明 |
|------|------|------|
| floor | int | 楼层 |
| time | string | 时间 |
| floor_total_power | float | 楼层总功率（W） |
| risk_level | string | 风险等级 |

### 高峰预测

| 字段 | 类型 | 说明 |
|------|------|------|
| floor | int | 楼层 |
| current_load | float | 当前负载（W） |
| predicted_load | float | 预测负载（W） |
| risk_level | string | 风险等级 |
| suggestion | string | 建议 |

---

## 前端对接示例（JavaScript）

```javascript
// 获取所有宿舍数据
const res = await fetch('http://localhost:5000/export/dorm_energy_data.json');
const dorms = await res.json();

// 获取异常列表
const abRes = await fetch('http://localhost:5000/export/abnormal_list.json');
const abnormals = await abRes.json();

// 获取楼层负载
const flRes = await fetch('http://localhost:5000/export/floor_load_data.json');
const floorLoad = await flRes.json();

// 上报硬件数据
await fetch('http://localhost:5000/api/data', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({dorm_id: 'A101', power: 850, occupied: true})
});
```

---

## 异常类型说明

| 异常类型 | 触发条件 | 风险等级 |
|---------|---------|---------|
| 无人宿舍耗电 | 无人且功率 > 300W | 中 |
| 疑似高功率违规用电 | 功率 > 1500W | 高 |
| 楼层过载风险 | 楼层总功率 > 8000W | 高 |
| 高峰负载风险 | 预测负载超过阈值 | 中/高 |
