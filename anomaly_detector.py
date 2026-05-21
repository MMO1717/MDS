"""
宿舍能源管理系统 - 异常检测引擎
实时分析每条数据，检测异常并生成建议
"""

import config


class AnomalyDetector:
    """异常检测引擎，维护楼层历史数据用于负载预测"""

    def __init__(self):
        # 每层的历史功率序列（用于预测）
        self._floor_history: dict[int, list[float]] = {f: [] for f in range(1, config.FLOORS + 1)}
        # 最近一次每层总功率
        self._floor_current: dict[int, float] = {f: 0.0 for f in range(1, config.FLOORS + 1)}
        # 本次采集各宿舍功率（用于计算楼层总功率）
        self._current_batch_powers: dict[int, float] = {f: 0.0 for f in range(1, config.FLOORS + 1)}

    def reset_batch(self):
        """每轮采集开始时重置"""
        self._current_batch_powers = {f: 0.0 for f in range(1, config.FLOORS + 1)}

    def analyze_record(self, record: dict) -> dict:
        """
        分析单条记录，添加异常标注
        输入：原始记录（dorm_id, floor, time, power, energy, temperature, occupied）
        输出：添加了 abnormal_status, abnormal_type, risk_level, suggestion 的完整记录
        """
        power = record["power"]
        occupied = record["occupied"]
        floor = record["floor"]

        # 累加楼层功率
        self._current_batch_powers[floor] += power

        # 单条记录的异常检测（不含楼层过载，楼层过载在批次结束后处理）
        abnormal_status, abnormal_type, risk_level, suggestion = self._detect_single(
            power, occupied
        )

        result = record.copy()
        result["abnormal_status"] = abnormal_status
        result["abnormal_type"] = abnormal_type
        result["risk_level"] = risk_level
        result["suggestion"] = suggestion
        return result

    def finalize_batch(self, records: list[dict]) -> list[dict]:
        """
        一轮采集结束后，处理楼层过载检测和负载预测
        返回更新后的记录列表
        """
        # 更新楼层历史
        for floor in range(1, config.FLOORS + 1):
            total = self._current_batch_powers[floor]
            self._floor_current[floor] = total
            self._floor_history[floor].append(total)
            # 只保留最近20个时间点
            if len(self._floor_history[floor]) > 20:
                self._floor_history[floor] = self._floor_history[floor][-20:]

        # 楼层过载检测
        floor_overloaded = {}
        for floor in range(1, config.FLOORS + 1):
            total = self._floor_current[floor]
            floor_overloaded[floor] = total > config.FLOOR_OVERLOAD_THRESHOLD

        # 更新记录中的楼层过载标记
        updated = []
        for r in records:
            r = r.copy()
            floor = r["floor"]
            if floor_overloaded[floor] and r["abnormal_status"] == "normal":
                r["abnormal_status"] = "abnormal"
                r["abnormal_type"] = "楼层过载风险"
                r["risk_level"] = "高"
                r["suggestion"] = "当前楼层总负载较高，建议引导学生错峰使用高功率设备。"
            updated.append(r)

        return updated

    def _detect_single(self, power: float, occupied: bool) -> tuple[str, str, str, str]:
        """单条记录异常检测"""
        abnormal_status = "normal"
        abnormal_type = "无"
        risk_level = "低"
        suggestion = "当前用电状态正常。"

        # 1. 无人宿舍耗电
        if not occupied and power > config.UNOCCUPIED_POWER_THRESHOLD:
            abnormal_status = "abnormal"
            abnormal_type = "无人宿舍耗电"
            risk_level = "中"
            suggestion = "检测到宿舍无人但仍有较高用电，建议关闭照明、插座或其他待机设备。"

        # 2. 高功率异常用电（优先级最高）
        if power > config.HIGH_POWER_THRESHOLD:
            abnormal_status = "abnormal"
            abnormal_type = "疑似高功率违规用电"
            risk_level = "高"
            suggestion = "检测到宿舍瞬时功率过高，疑似存在高功率设备使用，请管理员重点关注。"
        elif power > config.HIGH_POWER_WARNING:
            if abnormal_status == "normal":
                risk_level = "中"
                suggestion = "当前用电偏高，请注意合理使用电器。"

        return abnormal_status, abnormal_type, risk_level, suggestion

    def get_floor_load(self) -> list[dict]:
        """获取当前楼层负载数据"""
        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = []
        for floor in range(1, config.FLOORS + 1):
            total = self._floor_current[floor]
            result.append({
                "floor": floor,
                "time": now,
                "floor_total_power": round(total, 1),
                "risk_level": self._get_floor_risk(total),
            })
        return result

    def get_predictions(self) -> list[dict]:
        """获取高峰负载预测"""
        results = []
        for floor in range(1, config.FLOORS + 1):
            history = self._floor_history[floor]
            if len(history) < config.PREDICTION_HISTORY_POINTS + 1:
                continue

            current_load = history[-1]
            recent = history[-(config.PREDICTION_HISTORY_POINTS + 1):]
            predicted = self._predict_load(recent)
            risk = self._get_floor_risk(predicted)

            suggestion = "预计负载保持稳定。"
            if predicted > config.FLOOR_OVERLOAD_THRESHOLD:
                suggestion = "预计该楼层未来30分钟进入用电高峰，建议提前进行负载预警。"
            elif predicted > config.FLOOR_WARNING_THRESHOLD:
                suggestion = "预计负载将有所上升，请关注楼层用电情况。"

            results.append({
                "floor": floor,
                "current_load": round(current_load, 1),
                "predicted_load": round(predicted, 1),
                "risk_level": risk,
                "suggestion": suggestion,
            })

        return results

    def _predict_load(self, recent_powers: list[float]) -> float:
        """用平均增长量预测"""
        if len(recent_powers) < 2:
            return recent_powers[-1] if recent_powers else 0
        growths = []
        for i in range(1, len(recent_powers)):
            growths.append(recent_powers[i] - recent_powers[i - 1])
        avg_growth = sum(growths) / len(growths)
        return max(0, recent_powers[-1] + avg_growth)

    def _get_floor_risk(self, total_power: float) -> str:
        if total_power > config.FLOOR_OVERLOAD_THRESHOLD:
            return "高"
        elif total_power > config.FLOOR_WARNING_THRESHOLD:
            return "中"
        return "低"

    def generate_suggestions(self, records: list[dict]) -> list[dict]:
        """从分析后的记录中提取节能建议"""
        suggestions = []
        for r in records:
            if r["abnormal_status"] == "abnormal":
                suggestions.append({
                    "dorm_id": r["dorm_id"],
                    "time": r["time"],
                    "abnormal_type": r["abnormal_type"],
                    "risk_level": r["risk_level"],
                    "suggestion": r["suggestion"],
                })

        # 加入预测建议
        for p in self.get_predictions():
            if p["risk_level"] in ("中", "高"):
                suggestions.append({
                    "dorm_id": f"楼层{p['floor']}",
                    "time": "实时",
                    "abnormal_type": "高峰负载风险",
                    "risk_level": p["risk_level"],
                    "suggestion": p["suggestion"],
                })

        return suggestions
