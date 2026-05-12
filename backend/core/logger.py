from datetime import datetime
import json
import os

# ─────────────────────────────────────────
# LOGGER
# Tracks every test run & fix attempt
# ─────────────────────────────────────────

LOG_FILE = "seads_log.json"

def log_event(event_type: str, data: dict):
    """Append a log event to seads_log.json"""
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "data": data
    }
    
    # Load existing logs
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(entry)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)

def log_test_result(filename: str, success: bool, error: str = ""):
    log_event("TEST_RUN", {
        "file": filename,
        "success": success,
        "error": error[:500] if error else ""
    })

def log_fix_attempt(filename: str, attempt: int, fixed: bool):
    log_event("FIX_ATTEMPT", {
        "file": filename,
        "attempt": attempt,
        "fixed": fixed
    })
