"""
Teacher/admin backend for the dormitory energy management system.

This service reads the five JSON files produced by the algorithm side and
provides query/statistics APIs for the teacher management dashboard.

It only uses Python's standard library, so it can run without installing Flask
or other third-party packages.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from data_store import EnergyDataStore, paginate


HOST = "0.0.0.0"
PORT = 8000
store = EnergyDataStore()


def _first(query: dict[str, list[str]], name: str, default=None):
    values = query.get(name)
    if not values:
        return default
    return values[0]


def _int_arg(query: dict[str, list[str]], name: str, default=None):
    value = _first(query, name)
    if value in (None, ""):
        return default
    return int(value)


def _filters(query: dict[str, list[str]]) -> dict:
    return {
        "dorm_id": _first(query, "dorm_id"),
        "floor": _int_arg(query, "floor"),
        "risk_level": _first(query, "risk_level"),
        "abnormal_type": _first(query, "abnormal_type"),
        "start_time": _first(query, "start_time"),
        "end_time": _first(query, "end_time"),
    }


def _page_args(query: dict[str, list[str]]) -> tuple[int, int]:
    return (
        _int_arg(query, "page", 1),
        _int_arg(query, "page_size", 20),
    )


class TeacherApiHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._send_json({"status": "ok"})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/teacher/reload":
            store.reload()
            self._send_json({"status": "ok", "message": "data reloaded"})
            return
        self._send_error(404, "接口不存在")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        try:
            data = self._route_get(path, query)
            self._send_json(data)
        except ValueError as exc:
            self._send_error(400, str(exc))
        except LookupError as exc:
            self._send_error(404, str(exc))

    def _route_get(self, path: str, query: dict[str, list[str]]):
        if path == "/api/teacher/health":
            return {"status": "ok", "message": "teacher backend is running"}

        if path == "/api/teacher/overview":
            return store.get_overview()

        if path == "/api/teacher/dashboard":
            limit = _int_arg(query, "limit", 10)
            return {
                "overview": store.get_overview(),
                "floor_summary": store.get_floor_summary(),
                "top_energy_dorms": store.get_top_dorms_by_energy(limit=limit),
            }

        if path == "/api/teacher/dorms":
            records = store.query_dorm_records(_filters(query))
            page, page_size = _page_args(query)
            return paginate(records, page, page_size)

        if path.startswith("/api/teacher/dorms/"):
            dorm_id = unquote(path.rsplit("/", 1)[-1]).upper()
            summary = store.get_dorm_summary(dorm_id)
            if summary is None:
                raise LookupError(f"宿舍 {dorm_id} 不存在")
            return summary

        if path == "/api/teacher/abnormal":
            records = store.query_abnormal_records(_filters(query))
            page, page_size = _page_args(query)
            return paginate(records, page, page_size)

        if path == "/api/teacher/floor-load":
            records = store.query_floor_load(_filters(query))
            page, page_size = _page_args(query)
            return paginate(records, page, page_size)

        if path == "/api/teacher/floor-summary":
            return {"data": store.get_floor_summary()}

        if path == "/api/teacher/predictions":
            records = store.query_predictions(_filters(query))
            page, page_size = _page_args(query)
            return paginate(records, page, page_size)

        if path == "/api/teacher/suggestions":
            records = store.query_suggestions(_filters(query))
            page, page_size = _page_args(query)
            return paginate(records, page, page_size)

        if path == "/api/teacher/rankings/energy":
            limit = _int_arg(query, "limit", 10)
            return {"data": store.get_top_dorms_by_energy(limit=limit)}

        raise LookupError("接口不存在")

    def _send_json(self, data, status: int = 200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(payload)

    def _send_error(self, status: int, message: str):
        self._send_json({"error": message}, status=status)

    def log_message(self, format, *args):
        print("[教师端后端]", format % args)


def main():
    server = ThreadingHTTPServer((HOST, PORT), TeacherApiHandler)
    print("=" * 50)
    print("宿舍能源协同管理系统 - 教师端后端")
    print("=" * 50)
    print(f"服务地址: http://localhost:{PORT}")
    print("健康检查: GET /api/teacher/health")
    print("教师端汇总: GET /api/teacher/dashboard")
    print()
    server.serve_forever()


if __name__ == "__main__":
    main()
