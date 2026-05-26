"""
Teacher-side data access for the dormitory energy management backend.

The algorithm team has already produced JSON files with anomaly decisions and
suggestions. This module loads those files and provides query/statistics helpers
for the teacher/admin API.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "algorithm" / "算法端输出"


class EnergyDataStore:
    """In-memory data store backed by the algorithm output JSON files."""

    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.reload()

    def reload(self) -> None:
        self.dorm_records = self._load_json("dorm_energy_data.json")
        self.abnormal_records = self._load_json("abnormal_list.json")
        self.floor_load_records = self._load_json("floor_load_data.json")
        self.prediction_records = self._load_json("load_prediction_result.json")
        self.suggestion_records = self._load_json("suggestion_data.json")

    def _load_json(self, filename: str) -> list[dict[str, Any]]:
        path = self.data_dir / filename
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError(f"{filename} should contain a JSON array")
        return data

    def query_dorm_records(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return self._filter_records(self.dorm_records, filters)

    def query_abnormal_records(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return self._filter_records(self.abnormal_records, filters)

    def query_floor_load(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return self._filter_records(self.floor_load_records, filters)

    def query_predictions(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return self._filter_records(self.prediction_records, filters)

    def query_suggestions(self, filters: dict[str, Any]) -> list[dict[str, Any]]:
        return self._filter_records(self.suggestion_records, filters)

    def get_dorm_summary(self, dorm_id: str) -> dict[str, Any] | None:
        records = [r for r in self.dorm_records if r.get("dorm_id") == dorm_id]
        if not records:
            return None

        latest = max(records, key=lambda r: r.get("time", ""))
        abnormal_count = sum(1 for r in records if r.get("abnormal_status") == "abnormal")
        total_energy = max((float(r.get("energy", 0) or 0) for r in records), default=0)
        avg_power = sum(float(r.get("power", 0) or 0) for r in records) / len(records)

        return {
            "dorm_id": dorm_id,
            "floor": latest.get("floor"),
            "latest": latest,
            "record_count": len(records),
            "abnormal_count": abnormal_count,
            "total_energy": round(total_energy, 2),
            "avg_power": round(avg_power, 1),
        }

    def get_overview(self) -> dict[str, Any]:
        dorm_ids = {r.get("dorm_id") for r in self.dorm_records if r.get("dorm_id")}
        latest_time = max((r.get("time", "") for r in self.dorm_records), default="")
        latest_records = [r for r in self.dorm_records if r.get("time") == latest_time]

        total_power = sum(float(r.get("power", 0) or 0) for r in latest_records)
        abnormal_now = [r for r in latest_records if r.get("abnormal_status") == "abnormal"]
        high_risk_now = [r for r in latest_records if r.get("risk_level") == "高"]
        total_energy = sum(self._latest_energy_by_dorm().values())

        risk_counter = Counter(r.get("risk_level", "未知") for r in self.abnormal_records)
        type_counter = Counter(r.get("abnormal_type", "未知") for r in self.abnormal_records)

        return {
            "building": "A",
            "floor_count": 5,
            "dorm_count": len(dorm_ids),
            "record_count": len(self.dorm_records),
            "latest_time": latest_time,
            "current_total_power": round(total_power, 1),
            "total_energy": round(total_energy, 2),
            "current_abnormal_count": len(abnormal_now),
            "current_high_risk_count": len(high_risk_now),
            "abnormal_record_count": len(self.abnormal_records),
            "suggestion_count": len(self.suggestion_records),
            "risk_distribution": dict(risk_counter),
            "abnormal_type_distribution": dict(type_counter),
        }

    def get_floor_summary(self) -> list[dict[str, Any]]:
        latest_by_floor: dict[int, dict[str, Any]] = {}
        for record in self.floor_load_records:
            floor = record.get("floor")
            if floor is None:
                continue
            old = latest_by_floor.get(floor)
            if old is None or record.get("time", "") > old.get("time", ""):
                latest_by_floor[floor] = record

        abnormal_by_floor = Counter(r.get("floor") for r in self.abnormal_records)
        result = []
        for floor in sorted(latest_by_floor):
            item = latest_by_floor[floor].copy()
            item["abnormal_count"] = abnormal_by_floor.get(floor, 0)
            result.append(item)
        return result

    def get_top_dorms_by_energy(self, limit: int = 10) -> list[dict[str, Any]]:
        latest_energy = self._latest_energy_by_dorm()
        abnormal_counts = Counter(r.get("dorm_id") for r in self.abnormal_records)
        rows = [
            {
                "dorm_id": dorm_id,
                "energy": round(energy, 2),
                "abnormal_count": abnormal_counts.get(dorm_id, 0),
            }
            for dorm_id, energy in latest_energy.items()
        ]
        rows.sort(key=lambda r: r["energy"], reverse=True)
        return rows[:limit]

    def _latest_energy_by_dorm(self) -> dict[str, float]:
        latest: dict[str, dict[str, Any]] = {}
        for record in self.dorm_records:
            dorm_id = record.get("dorm_id")
            if not dorm_id:
                continue
            old = latest.get(dorm_id)
            if old is None or record.get("time", "") > old.get("time", ""):
                latest[dorm_id] = record
        return {
            dorm_id: float(record.get("energy", 0) or 0)
            for dorm_id, record in latest.items()
        }

    def _filter_records(
        self,
        records: list[dict[str, Any]],
        filters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        result = records

        if filters.get("dorm_id"):
            dorm_id = str(filters["dorm_id"]).upper()
            result = [r for r in result if str(r.get("dorm_id", "")).upper() == dorm_id]

        if filters.get("floor") is not None:
            floor = int(filters["floor"])
            result = [r for r in result if r.get("floor") == floor]

        if filters.get("risk_level"):
            risk_level = str(filters["risk_level"])
            result = [r for r in result if r.get("risk_level") == risk_level]

        if filters.get("abnormal_type"):
            abnormal_type = str(filters["abnormal_type"])
            result = [r for r in result if r.get("abnormal_type") == abnormal_type]

        if filters.get("start_time"):
            start_time = str(filters["start_time"])
            result = [r for r in result if str(r.get("time", "")) >= start_time]

        if filters.get("end_time"):
            end_time = str(filters["end_time"])
            result = [r for r in result if str(r.get("time", "")) <= end_time]

        return result


def paginate(records: list[dict[str, Any]], page: int, page_size: int) -> dict[str, Any]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 200)
    total = len(records)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": records[start:end],
    }
