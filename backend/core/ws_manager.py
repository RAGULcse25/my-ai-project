# core/ws_manager.py — S.E.A.D.S. v15
# ============================================================
# WEBSOCKET MANAGER — Bidirectional interactive pipeline control
# Endpoint: WS /ws/{task_id}
# Client → Server: pause | redirect | inject | stop
# Server → Client: paused | redirected | error | ack
# ============================================================

import json, asyncio, time
from typing import Dict, Set
from fastapi import WebSocket, WebSocketDisconnect

# ── Active connections registry ──────────────────────────────
_connections: Dict[str, Set[WebSocket]] = {}

# ── Pipeline control flags (read by orchestrator) ────────────
_control_flags: Dict[str, dict] = {}


def get_flags(task_id: str) -> dict:
    return _control_flags.get(task_id, {})


def set_flag(task_id: str, key: str, value):
    if task_id not in _control_flags:
        _control_flags[task_id] = {}
    _control_flags[task_id][key] = value


def clear_flags(task_id: str):
    _control_flags.pop(task_id, None)


def is_paused(task_id: str) -> bool:
    return _control_flags.get(task_id, {}).get("paused", False)


def get_redirect(task_id: str) -> str | None:
    return _control_flags.get(task_id, {}).get("redirect", None)


def consume_redirect(task_id: str) -> str | None:
    """Get and clear the redirect instruction (one-shot)."""
    flags = _control_flags.get(task_id, {})
    redirect = flags.pop("redirect", None)
    return redirect


# ── Connection management ────────────────────────────────────
async def connect(task_id: str, ws: WebSocket):
    await ws.accept()
    if task_id not in _connections:
        _connections[task_id] = set()
    _connections[task_id].add(ws)
    await _send(ws, {"event": "connected", "task_id": task_id})


async def disconnect(task_id: str, ws: WebSocket):
    if task_id in _connections:
        _connections[task_id].discard(ws)
    try:
        await ws.close()
    except Exception:
        pass


async def broadcast(task_id: str, data: dict):
    """Broadcast a message to all clients watching this task."""
    dead = set()
    for ws in _connections.get(task_id, set()):
        try:
            await ws.send_json(data)
        except Exception:
            dead.add(ws)
    for ws in dead:
        _connections.get(task_id, set()).discard(ws)


async def _send(ws: WebSocket, data: dict):
    try:
        await ws.send_json(data)
    except Exception:
        pass


# ── Command handler ──────────────────────────────────────────
async def handle_ws(task_id: str, ws: WebSocket):
    """
    Main WebSocket handler — call this from the FastAPI WS route.
    Processes incoming commands and updates control flags.
    """
    await connect(task_id, ws)
    try:
        while True:
            raw = await ws.receive_text()
            try:
                cmd = json.loads(raw)
            except Exception:
                await _send(ws, {"event": "error", "message": "Invalid JSON"})
                continue

            action = cmd.get("action", "")

            # ── PAUSE ────────────────────────────────────────
            if action == "pause":
                set_flag(task_id, "paused", True)
                await broadcast(task_id, {
                    "event": "paused",
                    "task_id": task_id,
                    "message": "Pipeline paused. Send resume to continue.",
                    "timestamp": time.time(),
                })

            # ── RESUME ───────────────────────────────────────
            elif action == "resume":
                set_flag(task_id, "paused", False)
                await broadcast(task_id, {
                    "event": "resumed",
                    "task_id": task_id,
                    "timestamp": time.time(),
                })

            # ── REDIRECT ─────────────────────────────────────
            elif action == "redirect":
                instruction = cmd.get("instruction", "")
                agent = cmd.get("agent", "")
                if instruction:
                    set_flag(task_id, "redirect", instruction)
                    set_flag(task_id, "redirect_agent", agent)
                    await broadcast(task_id, {
                        "event":       "redirected",
                        "instruction": instruction,
                        "agent":       agent,
                        "timestamp":   time.time(),
                    })

            # ── INJECT ───────────────────────────────────────
            elif action == "inject":
                agent    = cmd.get("agent", "")
                override = cmd.get("override", "")
                set_flag(task_id, f"inject_{agent}", override)
                await broadcast(task_id, {
                    "event":    "injected",
                    "agent":    agent,
                    "override": override,
                    "timestamp": time.time(),
                })

            # ── STOP ─────────────────────────────────────────
            elif action == "stop":
                set_flag(task_id, "stopped", True)
                await broadcast(task_id, {
                    "event":     "stopped",
                    "task_id":   task_id,
                    "timestamp": time.time(),
                })

            # ── UNKNOWN ──────────────────────────────────────
            else:
                await _send(ws, {
                    "event":   "error",
                    "message": f"Unknown action: {action}",
                })

    except WebSocketDisconnect:
        await disconnect(task_id, ws)
    except Exception as e:
        await _send(ws, {"event": "error", "message": str(e)})
        await disconnect(task_id, ws)
