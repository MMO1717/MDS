#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

TEACHER_BACKEND_PORT="${TEACHER_BACKEND_PORT:-8000}"
FRONTEND_PORT="${FRONTEND_PORT:-8080}"
START_ALGORITHM="${START_ALGORITHM:-0}"

PIDS=()

cleanup() {
  if [ "${#PIDS[@]}" -gt 0 ]; then
    echo
    echo "Stopping services..."
    for pid in "${PIDS[@]}"; do
      kill "$pid" >/dev/null 2>&1 || true
    done
  fi
}
trap cleanup EXIT

require_python() {
  if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python not found: $PYTHON_BIN"
    echo "Install Python 3 or run with: PYTHON_BIN=/path/to/python3 ./start.sh"
    exit 1
  fi
}

wait_for_url() {
  local url="$1"
  local name="$2"
  local retries=30

  for _ in $(seq 1 "$retries"); do
    if "$PYTHON_BIN" - "$url" >/dev/null 2>&1 <<'PY'
import sys
from urllib.request import urlopen

with urlopen(sys.argv[1], timeout=1) as response:
    if response.status < 500:
        raise SystemExit(0)
raise SystemExit(1)
PY
    then
      echo "$name is ready: $url"
      return 0
    fi
    sleep 0.5
  done

  echo "$name did not become ready: $url"
  return 1
}

ensure_alive() {
  local pid="$1"
  local name="$2"
  if ! kill -0 "$pid" >/dev/null 2>&1; then
    echo "$name exited during startup."
    echo "Check whether the port is already in use or blocked."
    exit 1
  fi
}

open_url() {
  local url="$1"
  if command -v open >/dev/null 2>&1; then
    open "$url"
  else
    echo "Open this URL in your browser: $url"
  fi
}

require_python

echo "Project: $ROOT_DIR"
echo "Python: $($PYTHON_BIN --version 2>&1)"
echo

echo "Starting teacher backend on port $TEACHER_BACKEND_PORT..."
(
  cd "$ROOT_DIR/backend"
  "$PYTHON_BIN" app.py
) &
PIDS+=("$!")
TEACHER_PID="$!"

echo "Starting static frontend server on port $FRONTEND_PORT..."
(
  cd "$ROOT_DIR"
  "$PYTHON_BIN" -m http.server "$FRONTEND_PORT"
) &
PIDS+=("$!")
FRONTEND_PID="$!"

if [ "$START_ALGORITHM" = "1" ]; then
  echo "Starting algorithm API on port 5000..."
  (
    cd "$ROOT_DIR/algorithm"
    "$PYTHON_BIN" app.py
  ) &
  PIDS+=("$!")
fi

sleep 1
ensure_alive "$TEACHER_PID" "Teacher backend"
ensure_alive "$FRONTEND_PID" "Frontend server"

wait_for_url "http://localhost:$TEACHER_BACKEND_PORT/api/teacher/health" "Teacher backend"
wait_for_url "http://localhost:$FRONTEND_PORT/frontend/index.html" "Frontend server"

echo
echo "Opening pages..."
open_url "http://localhost:$FRONTEND_PORT/frontend/index.html"
open_url "http://localhost:$FRONTEND_PORT/frontend/student.html"

echo
echo "Running:"
echo "  Teacher backend: http://localhost:$TEACHER_BACKEND_PORT"
echo "  Teacher page:    http://localhost:$FRONTEND_PORT/frontend/index.html"
echo "  Student page:    http://localhost:$FRONTEND_PORT/frontend/student.html"
if [ "$START_ALGORITHM" = "1" ]; then
  echo "  Algorithm API:   http://localhost:5000"
fi
echo
echo "Keep this window open while using the app."
echo "Press Ctrl+C to stop all services."

while true; do
  sleep 3600
done
