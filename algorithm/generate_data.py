"""
宿舍能源管理系统 - 算法端数据生成与分析脚本
生成模拟数据、异常检测、负载预测、节能建议
"""

import json
import random
from datetime import datetime, timedelta

random.seed(42)

# ============================================================
# 配置
# ============================================================
BUILDING = "A"
FLOORS = 5
ROOMS_PER_FLOOR = 10
DAYS = 7
INTERVAL_MINUTES = 30
START_DATE = datetime(2026, 5, 12, 0, 0)  # 从5月12日开始，覆盖7天

# 宿舍类型分配（按宿舍编号）
# A101-A102: 无人耗电宿舍
# A201-A202: 高功率异常宿舍
# A301-A303: 高耗能宿舍
# A301-A310 整层: 楼层过载宿舍群（第3层多间功率偏高）
# 其余: 正常宿舍

ANOMALY_DORMS = {
    "A101": "无人耗电",
    "A102": "无人耗电",
    "A201": "高功率异常",
    "A202": "高功率异常",
    "A301": "高耗能",
    "A302": "高耗能",
    "A303": "高耗能",
    "A401": "无人耗电",
    "A501": "高功率异常",
}


def get_dorm_type(dorm_id):
    """判断宿舍类型"""
    return ANOMALY_DORMS.get(dorm_id, "正常")


def get_floor(dorm_id):
    """从宿舍编号提取楼层"""
    return int(dorm_id[1])


def is_peak_hour(hour):
    """是否为用电高峰时段"""
    return 18 <= hour <= 23


def is_active_hour(hour):
    """是否为活跃用电时段"""
    return 7 <= hour <= 23


def generate_base_power(hour, dorm_type):
    """根据时间和宿舍类型生成基础功率"""
    if not is_active_hour(hour):
        # 深夜/凌晨，低功率
        base = random.uniform(20, 80)
        if dorm_type == "无人耗电":
            base = random.uniform(200, 450)  # 无人但有设备在耗电
        return base

    if is_peak_hour(hour):
        # 晚间高峰
        if dorm_type == "正常":
            return random.uniform(300, 800)
        elif dorm_type == "无人耗电":
            return random.uniform(350, 550)
        elif dorm_type == "高功率异常":
            return random.uniform(1500, 2500)
        elif dorm_type == "高耗能":
            return random.uniform(900, 1400)
    else:
        # 白天非高峰
        if dorm_type == "正常":
            return random.uniform(100, 400)
        elif dorm_type == "无人耗电":
            return random.uniform(250, 500)
        elif dorm_type == "高功率异常":
            # 白天偶尔也会有高功率
            if random.random() < 0.3:
                return random.uniform(1500, 2200)
            return random.uniform(200, 600)
        elif dorm_type == "高耗能":
            return random.uniform(500, 1000)

    return random.uniform(100, 400)


def generate_occupied(dorm_type, hour):
    """生成是否有人状态"""
    if dorm_type == "无人耗电":
        # 无人耗电宿舍，大部分时间没人
        return random.random() < 0.1

    if not is_active_hour(hour):
        # 深夜大部分人在
        return random.random() < 0.85

    if 9 <= hour <= 17:
        # 上课时间，部分人不在
        return random.random() < 0.4

    # 其他时间大部分人在
    return random.random() < 0.8


def generate_temperature(hour):
    """生成温度数据"""
    # 模拟5月中旬温度，白天高晚上低
    base_temp = 24
    if 6 <= hour <= 14:
        base_temp = 26 + random.uniform(0, 4)
    elif 14 < hour <= 18:
        base_temp = 27 + random.uniform(0, 3)
    elif 18 < hour <= 23:
        base_temp = 25 + random.uniform(0, 2)
    else:
        base_temp = 22 + random.uniform(0, 2)
    return round(base_temp, 1)


def detect_anomaly(dorm_id, power, occupied, floor_total_power=None):
    """异常检测逻辑"""
    abnormal_status = "normal"
    abnormal_type = "无"
    risk_level = "低"
    suggestion = "当前用电状态正常。"

    # 1. 无人宿舍耗电检测
    if not occupied and power > 300:
        abnormal_status = "abnormal"
        abnormal_type = "无人宿舍耗电"
        risk_level = "中"
        suggestion = "检测到宿舍无人但仍有较高用电，建议关闭照明、插座或其他待机设备。"

    # 2. 高功率异常用电检测（优先级高于无人耗电）
    if power > 1500:
        abnormal_status = "abnormal"
        abnormal_type = "疑似高功率违规用电"
        risk_level = "高"
        suggestion = "检测到宿舍瞬时功率过高，疑似存在高功率设备使用，请管理员重点关注。"
    elif power > 1200:
        # 1200-1500W 区间，用电偏高
        if abnormal_status == "normal":
            abnormal_status = "normal"
            abnormal_type = "无"
            risk_level = "中"
            suggestion = "当前用电偏高，请注意合理使用电器。"

    # 3. 楼层过载风险检测（单独在楼层级别处理，这里标记参与过载的宿舍）
    if floor_total_power is not None and floor_total_power > 8000:
        if abnormal_status == "normal":
            abnormal_status = "abnormal"
            abnormal_type = "楼层过载风险"
            risk_level = "高"
            suggestion = "当前楼层总负载较高，建议引导学生错峰使用高功率设备。"

    return abnormal_status, abnormal_type, risk_level, suggestion


def predict_load(recent_powers):
    """高峰负载预测：用最近3个时间点的平均增长量"""
    if len(recent_powers) < 2:
        return recent_powers[-1] if recent_powers else 0

    # 计算最近几个时间点的增长量
    growths = []
    for i in range(1, len(recent_powers)):
        growths.append(recent_powers[i] - recent_powers[i - 1])

    avg_growth = sum(growths) / len(growths)
    predicted = recent_powers[-1] + avg_growth
    return round(max(predicted, 0), 1)


def get_floor_risk_level(total_power):
    """楼层负载风险等级"""
    if total_power > 8000:
        return "高"
    elif total_power > 6000:
        return "中"
    return "低"


def get_suggestion_for_prediction(predicted_load, current_load):
    """根据预测结果生成建议"""
    if predicted_load > 8000:
        return "预计该楼层未来30分钟进入用电高峰，建议提前进行负载预警。"
    elif predicted_load > 6000:
        return "预计负载将有所上升，请关注楼层用电情况。"
    return "预计负载保持稳定。"


# ============================================================
# 主流程
# ============================================================
def main():
    # 生成所有宿舍编号
    dorm_ids = []
    for floor in range(1, FLOORS + 1):
        for room in range(1, ROOMS_PER_FLOOR + 1):
            dorm_ids.append(f"{BUILDING}{floor}{room:02d}")

    # 时间点列表
    time_points = []
    current = START_DATE
    end_date = START_DATE + timedelta(days=DAYS)
    while current < end_date:
        time_points.append(current)
        current += timedelta(minutes=INTERVAL_MINUTES)

    print(f"生成 {len(dorm_ids)} 间宿舍 × {len(time_points)} 个时间点 = {len(dorm_ids) * len(time_points)} 条数据")

    # --------------------------------------------------------
    # 第一步：生成模拟数据
    # --------------------------------------------------------
    all_data = []
    energy_accumulator = {}  # 每间宿舍的累计能耗

    for dorm_id in dorm_ids:
        energy_accumulator[dorm_id] = 0.0

    for tp in time_points:
        # 先计算每层总功率（用于楼层过载检测）
        floor_powers = {f: 0.0 for f in range(1, FLOORS + 1)}
        dorm_powers = {}

        for dorm_id in dorm_ids:
            floor = get_floor(dorm_id)
            dorm_type = get_dorm_type(dorm_id)
            power = round(generate_base_power(tp.hour, dorm_type), 1)
            dorm_powers[dorm_id] = power
            floor_powers[floor] += power

        for dorm_id in dorm_ids:
            floor = get_floor(dorm_id)
            dorm_type = get_dorm_type(dorm_id)
            power = dorm_powers[dorm_id]
            occupied = generate_occupied(dorm_type, tp.hour)
            temperature = generate_temperature(tp.hour)

            # 累计能耗（kWh），30分钟间隔
            energy_kwh = power / 1000 * 0.5
            energy_accumulator[dorm_id] += energy_kwh

            # 异常检测
            floor_total = round(floor_powers[floor], 1)
            abnormal_status, abnormal_type, risk_level, suggestion = detect_anomaly(
                dorm_id, power, occupied, floor_total
            )

            record = {
                "dorm_id": dorm_id,
                "floor": floor,
                "time": tp.strftime("%Y-%m-%d %H:%M"),
                "power": power,
                "energy": round(energy_accumulator[dorm_id], 2),
                "temperature": temperature,
                "occupied": occupied,
                "abnormal_status": abnormal_status,
                "abnormal_type": abnormal_type,
                "risk_level": risk_level,
                "suggestion": suggestion,
            }
            all_data.append(record)

    # 输出 dorm_energy_data.json
    with open("dorm_energy_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 dorm_energy_data.json ({len(all_data)} 条)")

    # --------------------------------------------------------
    # 第二步：异常列表
    # --------------------------------------------------------
    abnormal_list = [r for r in all_data if r["abnormal_status"] == "abnormal"]
    with open("abnormal_list.json", "w", encoding="utf-8") as f:
        json.dump(abnormal_list, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 abnormal_list.json ({len(abnormal_list)} 条异常)")

    # --------------------------------------------------------
    # 第三步：楼层负载数据 + 高峰负载预测
    # --------------------------------------------------------
    # 按楼层和时间聚合
    floor_time_data = {}  # {(floor, time_str): total_power}
    for r in all_data:
        key = (r["floor"], r["time"])
        floor_time_data[key] = floor_time_data.get(key, 0) + r["power"]

    # 按楼层组织时间序列
    floor_series = {}  # {floor: [(time_str, total_power), ...]}
    for (floor, time_str), total in sorted(floor_time_data.items()):
        if floor not in floor_series:
            floor_series[floor] = []
        floor_series[floor].append((time_str, round(total, 1)))

    # 生成 floor_load_data.json
    floor_load_data = []
    for floor in sorted(floor_series.keys()):
        for time_str, total_power in floor_series[floor]:
            floor_load_data.append({
                "floor": floor,
                "time": time_str,
                "floor_total_power": total_power,
                "risk_level": get_floor_risk_level(total_power),
            })

    with open("floor_load_data.json", "w", encoding="utf-8") as f:
        json.dump(floor_load_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 floor_load_data.json ({len(floor_load_data)} 条)")

    # 生成 load_prediction_result.json
    prediction_results = []
    for floor in sorted(floor_series.keys()):
        series = floor_series[floor]
        for i in range(3, len(series)):
            time_str = series[i][0]
            current_load = series[i][1]
            recent = [series[j][1] for j in range(i - 3, i + 1)]
            predicted = predict_load(recent)
            risk = get_floor_risk_level(predicted)
            suggestion = get_suggestion_for_prediction(predicted, current_load)

            # 只保留高峰时段的预测（更有意义）
            hour = int(time_str.split(" ")[1].split(":")[0])
            if 17 <= hour <= 23:
                prediction_results.append({
                    "floor": floor,
                    "time": time_str,
                    "current_load": current_load,
                    "predicted_load": predicted,
                    "risk_level": risk,
                    "suggestion": suggestion,
                })

    with open("load_prediction_result.json", "w", encoding="utf-8") as f:
        json.dump(prediction_results, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 load_prediction_result.json ({len(prediction_results)} 条)")

    # --------------------------------------------------------
    # 第四步：节能建议
    # --------------------------------------------------------
    suggestion_data = []
    for r in abnormal_list:
        suggestion_data.append({
            "dorm_id": r["dorm_id"],
            "time": r["time"],
            "abnormal_type": r["abnormal_type"],
            "risk_level": r["risk_level"],
            "suggestion": r["suggestion"],
        })

    # 加入高峰预测的建议
    for p in prediction_results:
        if p["risk_level"] in ("中", "高"):
            suggestion_data.append({
                "dorm_id": f"楼层{p['floor']}",
                "time": p["time"],
                "abnormal_type": "高峰负载风险",
                "risk_level": p["risk_level"],
                "suggestion": p["suggestion"],
            })

    with open("suggestion_data.json", "w", encoding="utf-8") as f:
        json.dump(suggestion_data, f, ensure_ascii=False, indent=2)
    print(f"✓ 已生成 suggestion_data.json ({len(suggestion_data)} 条)")

    # --------------------------------------------------------
    # 统计摘要
    # --------------------------------------------------------
    print("\n=== 数据统计 ===")
    print(f"总数据量: {len(all_data)} 条")
    print(f"异常数据: {len(abnormal_list)} 条")
    print(f"  - 无人耗电: {sum(1 for r in abnormal_list if r['abnormal_type'] == '无人宿舍耗电')} 条")
    print(f"  - 高功率违规: {sum(1 for r in abnormal_list if r['abnormal_type'] == '疑似高功率违规用电')} 条")
    print(f"  - 楼层过载: {sum(1 for r in abnormal_list if r['abnormal_type'] == '楼层过载风险')} 条")
    print(f"高峰预测: {len(prediction_results)} 条")
    print(f"节能建议: {len(suggestion_data)} 条")


if __name__ == "__main__":
    main()
