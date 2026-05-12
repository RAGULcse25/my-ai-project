# core/shared.py
# Shared state for progress tracking and other cross-module data

from collections import deque

PROGRESS_DATA = {}

# Keep recent pipeline runs for dashboards/debugging.
TASK_HISTORY = deque(maxlen=100)

SYSTEM_METRICS = {
    "runs_started": 0,
    "runs_completed": 0,
    "runs_failed": 0,
    "avg_runtime_seconds": 0.0,
}
