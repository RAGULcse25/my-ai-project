# core/sse_manager.py — S.E.A.D.S. v15
# ============================================================
# SERVER-SENT EVENTS (SSE) — Real-time passive streaming
# Endpoint: GET /api/stream/{task_id}
# Pushes agent state changes, logs, 3D graph updates to frontend
# ============================================================

import asyncio, json, time
from typing import AsyncGenerator, Dict, Any
from collections import defaultdict

# ── In-memory SSE queues (one per task_id) ──────────────────
_sse_queues: Dict[str, asyncio.Queue] = defaultdict(lambda: asyncio.Queue(maxsize=200))


def get_queue(task_id: str) -> asyncio.Queue:
    return _sse_queues[task_id]


def cleanup_queue(task_id: str):
    """Remove queue after build completes (memory cleanup)."""
    if task_id in _sse_queues:
        del _sse_queues[task_id]


# ── Push event from synchronous pipeline thread ──────────────
def push_event(task_id: str, event_type: str, data: Dict[str, Any]):
    """
    Called by agents (sync context) to push events to the SSE stream.
    Uses asyncio-safe put_nowait.
    """
    payload = {
        "type": event_type,
        "timestamp": time.time(),
        **data,
    }
    try:
        queue = get_queue(task_id)
        queue.put_nowait(json.dumps(payload))
    except asyncio.QueueFull:
        pass  # Drop if client disconnected


def push_agent_start(task_id: str, agent: str, percent: int, description: str = ""):
    push_event(task_id, "agent_start", {
        "agent":       agent,
        "percent":     percent,
        "description": description,
    })


def push_agent_complete(task_id: str, agent: str, percent: int,
                         tokens: int = 0, provider: str = "", model: str = ""):
    push_event(task_id, "agent_complete", {
        "agent":    agent,
        "percent":  percent,
        "tokens":   tokens,
        "provider": provider,
        "model":    model,
    })


def push_agent_fail(task_id: str, agent: str, error: str, auto_fixing: bool = True):
    push_event(task_id, "agent_fail", {
        "agent":      agent,
        "error":      error,
        "auto_fixing": auto_fixing,
    })


def push_heal(task_id: str, iteration: int, score: float, target_agent: str):
    push_event(task_id, "heal_triggered", {
        "iteration":    iteration,
        "score":        round(score, 2),
        "target_agent": target_agent,
    })


def push_log(task_id: str, message: str, level: str = "info"):
    push_event(task_id, "log", {
        "message": message,
        "level":   level,
    })


def push_3d_graph(task_id: str, nodes: list, edges: list):
    """Update the 3D pipeline visualization graph in the frontend."""
    push_event(task_id, "3d_graph_update", {
        "nodes": nodes,
        "edges": edges,
    })


def push_complete(task_id: str, response_data: dict):
    push_event(task_id, "complete", {"data": response_data})
    # Signal end of stream
    push_event(task_id, "done", {})


def push_error(task_id: str, message: str, auto_fixing: bool = False):
    push_event(task_id, "error", {
        "message":    message,
        "auto_fixing": auto_fixing,
    })


# ── SSE stream generator (async, for FastAPI StreamingResponse) ──
async def event_stream(task_id: str, timeout: int = 300) -> AsyncGenerator[str, None]:
    """
    Async generator consumed by FastAPI StreamingResponse.
    Yields SSE-formatted strings until 'done' event or timeout.
    """
    queue = get_queue(task_id)
    deadline = time.time() + timeout

    # Send initial connection event
    yield f"data: {json.dumps({'type': 'connected', 'task_id': task_id})}\n\n"

    while time.time() < deadline:
        try:
            raw = await asyncio.wait_for(queue.get(), timeout=1.0)
            payload = json.loads(raw)
            yield f"data: {raw}\n\n"

            # Stop streaming when done
            if payload.get("type") == "done":
                break

        except asyncio.TimeoutError:
            # Send heartbeat to keep connection alive
            yield f": heartbeat\n\n"
            continue
        except Exception:
            break

    cleanup_queue(task_id)
