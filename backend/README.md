# Backend - Teacher API

本后端采用和学生端后端一致的 Spring Boot + Maven 结构。

它面向教师端 / 后勤管理端，负责读取算法端已经生成好的 5 个 JSON 文件，并提供查询、筛选、分页和统计接口。

算法端负责异常判定和建议生成；教师端后端负责数据管理与 API 输出。

## 启动方式

```bash
cd backend
mvn spring-boot:run
```

默认服务地址：

```text
http://localhost:8080
```

## 数据来源

默认读取：

```text
../algorithm/算法端输出/
```

包含：

- `dorm_energy_data.json`：宿舍用电明细
- `abnormal_list.json`：异常记录
- `floor_load_data.json`：楼层负载汇总
- `load_prediction_result.json`：高峰预测
- `suggestion_data.json`：节能建议

如需修改数据目录，可调整：

```text
src/main/resources/application.properties
```

## 教师端接口

| 接口 | 说明 |
| --- | --- |
| `GET /api/teacher/health` | 服务健康检查 |
| `POST /api/teacher/reload` | 重新读取 JSON 数据 |
| `GET /api/teacher/overview` | 教师端首页统计卡片 |
| `GET /api/teacher/dashboard` | 首页汇总：统计、楼层概览、能耗排行 |
| `GET /api/teacher/dorms` | 宿舍用电明细 |
| `GET /api/teacher/dorms/{dorm_id}` | 单个宿舍汇总 |
| `GET /api/teacher/abnormal` | 异常宿舍记录 |
| `GET /api/teacher/floor-load` | 楼层负载历史 |
| `GET /api/teacher/floor-summary` | 各楼层最新状态 |
| `GET /api/teacher/predictions` | 高峰负载预测 |
| `GET /api/teacher/suggestions` | 节能建议 |
| `GET /api/teacher/rankings/energy` | 宿舍累计能耗排行 |

## 常用查询参数

- `page`：页码，默认 1
- `page_size`：每页数量，默认 20，最大 200
- `dorm_id`：宿舍号，例如 `A101`
- `floor`：楼层，例如 `1`
- `risk_level`：风险等级，`低` / `中` / `高`
- `abnormal_type`：异常类型，例如 `无人宿舍耗电`
- `start_time`：开始时间，例如 `2026-05-12 00:00`
- `end_time`：结束时间，例如 `2026-05-12 23:30`

示例：

```text
GET /api/teacher/abnormal?floor=4&risk_level=中&page=1&page_size=10
GET /api/teacher/dorms/A101
GET /api/teacher/predictions?risk_level=高
GET /api/teacher/rankings/energy?limit=10
```

## 智能插座接口

当前后端已合并学生端的 Tuya 智能插座接入能力。前端不要直接调用 Tuya 云 API，而是调用本地 Spring Boot 后端。

运行前需要配置环境变量：

```text
TUYA_ACCESS_ID=你的 Tuya Access ID
TUYA_ACCESS_SECRET=你的 Tuya Access Secret
```

设备配置位于：

```text
src/main/resources/application.properties
```

当前插座接口：

| 接口 | 说明 |
| --- | --- |
| `GET /api/plug/status` | 返回 Tuya 原始设备属性 |
| `GET /api/plug/monitor` | 返回系统统一格式的实时功率、电压、电流、电量和风险判断 |
| `POST /api/plug/on` | 打开智能插座 |
| `POST /api/plug/off` | 关闭智能插座 |

测试地址：

```text
http://localhost:8080/api/plug/monitor
```
