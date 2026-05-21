"""
宿舍能源管理系统 - Flask API 服务
启动后自动开始实时数据采集
"""

from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

import config
from collector import DataCollector
from data_source import SimulatedSource, HardwareSource

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 默认使用模拟数据源
collector = DataCollector(SimulatedSource())


# ============================================================
# API 路由 - 实时数据（带包装）
# ============================================================

@app.route("/api/status")
def status():
    """系统状态"""
    return jsonify({
        "status": "running",
        "stats": collector.get_stats(),
    })


@app.route("/api/dorms")
def get_dorms():
    """所有宿舍当前状态"""
    records = collector.get_latest_records()
    return jsonify({"count": len(records), "data": records})


@app.route("/api/dorms/<dorm_id>")
def get_dorm(dorm_id):
    """单个宿舍详情"""
    record = collector.get_dorm_detail(dorm_id)
    if record:
        return jsonify(record)
    return jsonify({"error": f"宿舍 {dorm_id} 不存在"}), 404


@app.route("/api/abnormal")
def get_abnormal():
    """当前异常列表"""
    abnormal = collector.get_latest_abnormal()
    return jsonify({"count": len(abnormal), "data": abnormal})


@app.route("/api/floor-load")
def get_floor_load():
    """楼层负载数据"""
    load = collector.get_floor_load()
    return jsonify({"data": load})


@app.route("/api/predictions")
def get_predictions():
    """高峰负载预测"""
    predictions = collector.get_predictions()
    return jsonify({"count": len(predictions), "data": predictions})


@app.route("/api/suggestions")
def get_suggestions():
    """节能建议"""
    suggestions = collector.get_latest_suggestions()
    return jsonify({"count": len(suggestions), "data": suggestions})


@app.route("/api/events")
def get_events():
    """事件日志（功率突变记录）"""
    events = collector.get_event_log()
    return jsonify({"count": len(events), "data": events})


# ============================================================
# API 路由 - 兼容静态JSON格式（直接返回数组，无包装）
# 软件端可直接用这些接口替换静态JSON文件
# ============================================================

@app.route("/export/dorm_energy_data.json")
def export_dorm_data():
    """导出宿舍用电数据（兼容静态JSON格式）"""
    return jsonify(collector.get_latest_records())


@app.route("/export/abnormal_list.json")
def export_abnormal():
    """导出异常列表（兼容静态JSON格式）"""
    return jsonify(collector.get_latest_abnormal())


@app.route("/export/floor_load_data.json")
def export_floor_load():
    """导出楼层负载（兼容静态JSON格式）"""
    return jsonify(collector.get_floor_load())


@app.route("/export/load_prediction_result.json")
def export_predictions():
    """导出预测结果（兼容静态JSON格式）"""
    return jsonify(collector.get_predictions())


@app.route("/export/suggestion_data.json")
def export_suggestions():
    """导出节能建议（兼容静态JSON格式）"""
    return jsonify(collector.get_latest_suggestions())


# ============================================================
# API 路由 - 硬件数据上报
# ============================================================

@app.route("/api/data", methods=["POST"])
def push_data():
    """
    硬件数据上报入口
    POST JSON 格式：
    {
        "dorm_id": "A101",
        "power": 850.0,
        "occupied": true,
        "temperature": 26.5
    }
    或批量上报：
    [
        {"dorm_id": "A101", "power": 850.0},
        {"dorm_id": "A102", "power": 320.0}
    ]
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请提供JSON数据"}), 400

    # 支持批量上报
    if isinstance(data, list):
        records = data
    else:
        records = [data]

    results = []
    for item in records:
        required = ["dorm_id", "power"]
        missing = [f for f in required if f not in item]
        if missing:
            results.append({"dorm_id": item.get("dorm_id", "?"), "error": f"缺少字段: {missing}"})
            continue

        item.setdefault("floor", int(item["dorm_id"][1]))
        item.setdefault("time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        item.setdefault("energy", 0)
        item.setdefault("temperature", 25.0)
        item.setdefault("occupied", True)

        try:
            collector.push_hardware_data(item)
            results.append({"dorm_id": item["dorm_id"], "status": "ok"})
        except ValueError as e:
            results.append({"dorm_id": item["dorm_id"], "error": str(e)})

    return jsonify({"results": results})


# ============================================================
# 启动
# ============================================================

def main():
    print("=" * 50)
    print("宿舍能源管理系统 - 实时数据采集服务")
    print("=" * 50)
    print()
    collector.start()
    print()
    print(f"API 服务启动: http://{config.HOST}:{config.PORT}")
    print()
    print("=== 实时查询接口（带包装） ===")
    print(f"  GET  /api/status      - 系统状态")
    print(f"  GET  /api/dorms       - 所有宿舍数据")
    print(f"  GET  /api/dorms/<id>  - 单个宿舍详情")
    print(f"  GET  /api/abnormal    - 异常列表")
    print(f"  GET  /api/floor-load  - 楼层负载")
    print(f"  GET  /api/predictions - 高峰预测")
    print(f"  GET  /api/suggestions - 节能建议")
    print(f"  GET  /api/events      - 事件日志")
    print()
    print("=== 兼容接口（直接返回数组，替换静态JSON） ===")
    print(f"  GET  /export/dorm_energy_data.json")
    print(f"  GET  /export/abnormal_list.json")
    print(f"  GET  /export/floor_load_data.json")
    print(f"  GET  /export/load_prediction_result.json")
    print(f"  GET  /export/suggestion_data.json")
    print()
    print("=== 数据上报接口 ===")
    print(f"  POST /api/data        - 硬件数据上报（支持批量）")
    print()

    try:
        app.run(host=config.HOST, port=config.PORT, debug=False, threaded=True)
    finally:
        collector.stop()


if __name__ == "__main__":
    main()
