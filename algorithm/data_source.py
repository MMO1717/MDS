"""
宿舍能源管理系统 - 数据源抽象与实现
支持模拟数据源和硬件数据源（预留）
"""

import random
import time
from abc import ABC, abstractmethod

import config


class DataSource(ABC):
    """数据源抽象基类"""

    @abstractmethod
    def get_current_data(self) -> list[dict]:
        """获取当前所有宿舍的用电数据，返回列表"""
        pass

    @abstractmethod
    def get_source_type(self) -> str:
        """返回数据源类型标识"""
        pass


class SimulatedSource(DataSource):
    """
    模拟数据源
    实时生成当前时刻的模拟用电数据，模拟真实传感器上报
    """

    def __init__(self):
        self._last_power = {}  # 每间宿舍上次功率，用于模拟连续性
        self._dorm_ids = self._generate_dorm_ids()
        self._energy_accumulator = {d: 0.0 for d in self._dorm_ids}
        self._last_collect_time = time.time()

    def _generate_dorm_ids(self) -> list[str]:
        dorm_ids = []
        for floor in range(1, config.FLOORS + 1):
            for room in range(1, config.ROOMS_PER_FLOOR + 1):
                dorm_ids.append(f"{config.BUILDING}{floor}{room:02d}")
        return dorm_ids

    def _get_dorm_type(self, dorm_id: str) -> str:
        return config.ANOMALY_DORMS.get(dorm_id, "正常")

    def _get_floor(self, dorm_id: str) -> int:
        return int(dorm_id[1])

    def _generate_power(self, dorm_id: str, hour: int) -> float:
        """生成单间宿舍的当前功率，保持连续性"""
        dorm_type = self._get_dorm_type(dorm_id)
        last = self._last_power.get(dorm_id)

        # 基础功率范围
        if 0 <= hour < 7:
            base_min, base_max = 20, 80
            if dorm_type == "无人耗电":
                base_min, base_max = 200, 450
        elif 18 <= hour <= 23:
            # 晚间高峰
            ranges = {
                "正常": (300, 800),
                "无人耗电": (350, 550),
                "高功率异常": (1500, 2500),
                "高耗能": (900, 1400),
            }
            base_min, base_max = ranges.get(dorm_type, (300, 800))
        else:
            # 白天
            ranges = {
                "正常": (100, 400),
                "无人耗电": (250, 500),
                "高功率异常": (200, 600),
                "高耗能": (500, 1000),
            }
            base_min, base_max = ranges.get(dorm_type, (100, 400))

        # 高功率异常宿舍白天偶尔突变
        if dorm_type == "高功率异常" and not (18 <= hour <= 23):
            if random.random() < 0.05:  # 5%概率突变
                base_min, base_max = 1500, 2500

        # 生成新功率，与上次值保持连续性
        if last is not None:
            # 在上次值附近波动，偶尔有较大变化
            if random.random() < 0.02:  # 2%概率大突变（模拟设备开关）
                new_power = random.uniform(base_min, base_max)
            else:
                # 小幅波动
                delta = random.uniform(-50, 50)
                new_power = last + delta
                new_power = max(base_min * 0.5, min(base_max * 1.2, new_power))
        else:
            new_power = random.uniform(base_min, base_max)

        new_power = round(max(0, new_power), 1)
        self._last_power[dorm_id] = new_power
        return new_power

    def _generate_occupied(self, dorm_id: str, hour: int) -> bool:
        dorm_type = self._get_dorm_type(dorm_id)
        if dorm_type == "无人耗电":
            return random.random() < 0.1
        if 0 <= hour < 7:
            return random.random() < 0.85
        if 9 <= hour <= 17:
            return random.random() < 0.4
        return random.random() < 0.8

    def _generate_temperature(self, hour: int) -> float:
        if 6 <= hour <= 14:
            base = 26 + random.uniform(0, 4)
        elif 14 < hour <= 18:
            base = 27 + random.uniform(0, 3)
        elif 18 < hour <= 23:
            base = 25 + random.uniform(0, 2)
        else:
            base = 22 + random.uniform(0, 2)
        return round(base, 1)

    def get_current_data(self) -> list[dict]:
        now = time.time()
        elapsed_hours = (now - self._last_collect_time) / 3600
        self._last_collect_time = now

        from datetime import datetime
        current_time = datetime.now()
        hour = current_time.hour

        records = []
        for dorm_id in self._dorm_ids:
            floor = self._get_floor(dorm_id)
            power = self._generate_power(dorm_id, hour)
            occupied = self._generate_occupied(dorm_id, hour)
            temperature = self._generate_temperature(hour)

            # 累计能耗
            self._energy_accumulator[dorm_id] += power / 1000 * elapsed_hours

            records.append({
                "dorm_id": dorm_id,
                "floor": floor,
                "time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "power": power,
                "energy": round(self._energy_accumulator[dorm_id], 3),
                "temperature": temperature,
                "occupied": occupied,
            })

        return records

    def get_source_type(self) -> str:
        return "simulated"


class HardwareSource(DataSource):
    """
    硬件数据源（预留接口）
    通过 POST /api/data 接收硬件上报的数据
    """

    def __init__(self):
        self._pending_data = []

    def push_data(self, record: dict):
        """硬件通过API推送数据时调用"""
        self._pending_data.append(record)

    def get_current_data(self) -> list[dict]:
        data = self._pending_data.copy()
        self._pending_data.clear()
        return data

    def get_source_type(self) -> str:
        return "hardware"
