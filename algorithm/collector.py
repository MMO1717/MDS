"""
宿舍能源管理系统 - 数据采集调度器
支持事件驱动和定时轮询两种采集模式
"""

import threading
import time
from datetime import datetime

import config
from data_source import DataSource, SimulatedSource, HardwareSource
from anomaly_detector import AnomalyDetector


class DataCollector:
    """
    数据采集调度器
    - 事件驱动模式：高频检测，捕捉功率突变
    - 定时轮询模式：按间隔批量采集
    """

    def __init__(self, data_source: DataSource = None):
        self.source = data_source or SimulatedSource()
        self.detector = AnomalyDetector()

        # 存储最新状态
        self._latest_records: list[dict] = []
        self._latest_abnormal: list[dict] = []
        self._latest_suggestions: list[dict] = []
        self._all_history: list[dict] = []  # 所有历史记录
        self._event_log: list[dict] = []  # 事件日志（突变记录）

        # 上一次功率记录（用于事件驱动检测）
        self._last_power: dict[str, float] = {}

        # 线程控制
        self._running = False
        self._polling_thread = None
        self._event_thread = None
        self._lock = threading.Lock()

        # 统计
        self._poll_count = 0
        self._event_count = 0

    def start(self):
        """启动采集"""
        self._running = True
        print(f"[采集器] 启动，数据源: {self.source.get_source_type()}")
        print(f"[采集器] 定时轮询间隔: {config.POLLING_INTERVAL}秒")
        print(f"[采集器] 事件检测间隔: {config.EVENT_CHECK_INTERVAL}秒")
        print(f"[采集器] 功率突变阈值: {config.POWER_CHANGE_THRESHOLD_W}W 或 {config.POWER_CHANGE_THRESHOLD_PERCENT*100}%")

        # 启动定时轮询线程
        self._polling_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self._polling_thread.start()

        # 启动事件驱动线程
        self._event_thread = threading.Thread(target=self._event_loop, daemon=True)
        self._event_thread.start()

    def stop(self):
        """停止采集"""
        self._running = False
        print("[采集器] 已停止")

    def _polling_loop(self):
        """定时轮询主循环"""
        while self._running:
            try:
                self._do_collect(is_event=False)
                self._poll_count += 1
            except Exception as e:
                print(f"[轮询] 错误: {e}")
            time.sleep(config.POLLING_INTERVAL)

    def _event_loop(self):
        """事件驱动主循环"""
        while self._running:
            try:
                # 从数据源获取当前数据
                raw_data = self.source.get_current_data()
                events = []

                for record in raw_data:
                    dorm_id = record["dorm_id"]
                    power = record["power"]
                    last = self._last_power.get(dorm_id)

                    if last is not None:
                        change = abs(power - last)
                        change_pct = change / last if last > 0 else 0

                        # 检测突变
                        if change >= config.POWER_CHANGE_THRESHOLD_W or change_pct >= config.POWER_CHANGE_THRESHOLD_PERCENT:
                            event = {
                                "dorm_id": dorm_id,
                                "time": record["time"],
                                "last_power": last,
                                "current_power": power,
                                "change": round(power - last, 1),
                                "change_percent": f"{change_pct*100:.1f}%",
                                "type": "功率突增" if power > last else "功率突降",
                            }
                            events.append(event)
                            self._event_count += 1

                    self._last_power[dorm_id] = power

                if events:
                    with self._lock:
                        self._event_log.extend(events)
                        if len(self._event_log) > 500:
                            self._event_log = self._event_log[-500:]

                    for e in events:
                        print(f"[事件] {e['dorm_id']} {e['type']}: "
                              f"{e['last_power']}W → {e['current_power']}W "
                              f"(变化: {e['change']}W, {e['change_percent']})")

            except Exception as e:
                print(f"[事件] 错误: {e}")

            time.sleep(config.EVENT_CHECK_INTERVAL)

    def _do_collect(self, is_event: bool = False):
        """执行一次数据采集和分析"""
        mode = "事件" if is_event else "轮询"

        # 获取数据
        raw_data = self.source.get_current_data()

        # 重置批次
        self.detector.reset_batch()

        # 分析每条记录
        analyzed = []
        for record in raw_data:
            result = self.detector.analyze_record(record)
            analyzed.append(result)

        # 完成批次处理（楼层过载检测）
        analyzed = self.detector.finalize_batch(analyzed)

        # 生成建议
        suggestions = self.detector.generate_suggestions(analyzed)

        # 提取异常
        abnormal = [r for r in analyzed if r["abnormal_status"] == "abnormal"]

        # 更新存储
        with self._lock:
            self._latest_records = analyzed
            self._latest_abnormal = abnormal
            self._latest_suggestions = suggestions
            self._all_history.extend(analyzed)
            # 保留最近5000条历史
            if len(self._all_history) > 5000:
                self._all_history = self._all_history[-5000:]

        if abnormal:
            print(f"[{mode}] 采集完成，发现 {len(abnormal)} 条异常")
            for a in abnormal[:3]:  # 只打印前3条
                print(f"  - {a['dorm_id']}: {a['abnormal_type']} ({a['risk_level']})")

    def get_latest_records(self) -> list[dict]:
        """获取最新一轮采集数据"""
        with self._lock:
            return self._latest_records.copy()

    def get_latest_abnormal(self) -> list[dict]:
        """获取当前异常列表"""
        with self._lock:
            return self._latest_abnormal.copy()

    def get_latest_suggestions(self) -> list[dict]:
        """获取最新节能建议"""
        with self._lock:
            return self._latest_suggestions.copy()

    def get_floor_load(self) -> list[dict]:
        """获取楼层负载"""
        return self.detector.get_floor_load()

    def get_predictions(self) -> list[dict]:
        """获取高峰预测"""
        return self.detector.get_predictions()

    def get_event_log(self) -> list[dict]:
        """获取事件日志"""
        with self._lock:
            return self._event_log.copy()

    def get_dorm_detail(self, dorm_id: str) -> dict | None:
        """获取单个宿舍详情"""
        with self._lock:
            for r in self._latest_records:
                if r["dorm_id"] == dorm_id:
                    return r
        return None

    def get_stats(self) -> dict:
        """获取采集统计信息"""
        return {
            "source_type": self.source.get_source_type(),
            "poll_count": self._poll_count,
            "event_count": self._event_count,
            "latest_records_count": len(self._latest_records),
            "abnormal_count": len(self._latest_abnormal),
            "history_count": len(self._all_history),
            "event_log_count": len(self._event_log),
        }

    def push_hardware_data(self, record: dict):
        """硬件数据源推送数据"""
        if isinstance(self.source, HardwareSource):
            self.source.push_data(record)
        else:
            raise ValueError("当前数据源不是硬件模式，无法推送数据")
