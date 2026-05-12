# core/blackboard.py — S.E.A.D.S. v15
# ============================================================
# BLACKBOARD PATTERN — Shared Build Context
# Every agent reads from + writes to this object.
# Every write is also persisted to MongoDB as an immutable event.
# ============================================================

import os, time, json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# ── Event types ──────────────────────────────────────────────
EVENT_START    = "start"
EVENT_COMPLETE = "complete"
EVENT_FAIL     = "fail"
EVENT_HEAL     = "heal"
EVENT_SKIP     = "skip"


@dataclass
class AgentEvent:
    task_id:       str
    agent_name:    str
    event_type:    str          # start|complete|fail|heal|skip
    timestamp:     float        = field(default_factory=time.time)
    tokens_used:   int          = 0
    provider:      str          = ""
    model:         str          = ""
    output_size:   int          = 0
    quality_score: Optional[float] = None
    error:         Optional[str]   = None
    message:       str          = ""

    def to_dict(self) -> dict:
        return {
            "task_id":       self.task_id,
            "agent_name":    self.agent_name,
            "event_type":    self.event_type,
            "timestamp":     self.timestamp,
            "datetime":      datetime.utcfromtimestamp(self.timestamp).isoformat(),
            "tokens_used":   self.tokens_used,
            "provider":      self.provider,
            "model":         self.model,
            "output_size":   self.output_size,
            "quality_score": self.quality_score,
            "error":         self.error,
            "message":       self.message,
        }


@dataclass
class AgentError:
    agent_name:  str
    error_type:  str    # empty_output|syntax_error|provider_error|timeout
    message:     str
    timestamp:   float  = field(default_factory=time.time)
    auto_fixed:  bool   = False
    fix_method:  str    = ""


class BuildContext:
    """
    Central blackboard for a single build pipeline run.
    Thread-safe for concurrent agent reads/writes.
    """

    def __init__(self, task_id: str, idea: str, answers: dict, manifest: dict):
        self.task_id  = task_id
        self.idea     = idea
        self.answers  = answers
        self.manifest = manifest    # RouterManifest dict

        # ── Agent Artifacts ──────────────────────────────────
        self.artifacts: Dict[str, str] = {
            "architecture":    "",
            "ui_code":         "",
            "backend_code":    "",
            "db_schema":       "",
            "ml_code":         "",
            "game_code":       "",
            "integrated_html": "",
            "verified_html":   "",
            "deploy_config":   "",
        }

        # ── Execution Tracking ───────────────────────────────
        self.agent_log:          List[AgentEvent] = []
        self.errors:             List[AgentError] = []
        self.healing_iterations: int   = 0
        self.quality_score:      float = 0.0
        self.max_healing:        int   = 2

        # ── Progress (fed to SSE stream) ─────────────────────
        self.percent:       int  = 0
        self.current_agent: str  = ""
        self.status:        str  = "Initializing..."
        self.started_at:    float = time.time()

        # ── MongoDB connection (lazy) ─────────────────────────
        self._mongo_collection = None
        self._init_mongo()

    # ─────────────────────────────────────────────────────────
    # MONGO INIT
    # ─────────────────────────────────────────────────────────
    def _init_mongo(self):
        try:
            from pymongo import MongoClient
            uri = os.getenv("MONGODB_URI") or os.getenv("MONGO_URI")
            if not uri:
                return
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            db = client.get_default_database()
            self._mongo_collection = db["agent_events"]
        except Exception as e:
            print(f"[BLACKBOARD] MongoDB unavailable: {e} — running in-memory only")

    # ─────────────────────────────────────────────────────────
    # ARTIFACT WRITE (with Mongo event log)
    # ─────────────────────────────────────────────────────────
    def write_artifact(self, key: str, value: str,
                       agent_name: str = "", tokens: int = 0,
                       provider: str = "", model: str = ""):
        """Write an artifact and log the event to MongoDB."""
        self.artifacts[key] = value

        event = AgentEvent(
            task_id=self.task_id,
            agent_name=agent_name or key,
            event_type=EVENT_COMPLETE,
            tokens_used=tokens,
            provider=provider,
            model=model,
            output_size=len(value),
            message=f"Artifact '{key}' written ({len(value):,} chars)",
        )
        self.agent_log.append(event)
        self._persist_event(event)

    def read_artifact(self, key: str) -> str:
        return self.artifacts.get(key, "")

    # ─────────────────────────────────────────────────────────
    # EVENT LOGGING
    # ─────────────────────────────────────────────────────────
    def log_event(self, agent_name: str, event_type: str,
                  tokens: int = 0, provider: str = "", model: str = "",
                  quality_score: float = None, error: str = None,
                  message: str = ""):
        event = AgentEvent(
            task_id=self.task_id,
            agent_name=agent_name,
            event_type=event_type,
            tokens_used=tokens,
            provider=provider,
            model=model,
            quality_score=quality_score,
            error=error,
            message=message,
        )
        self.agent_log.append(event)
        self._persist_event(event)
        return event

    def log_error(self, agent_name: str, error_type: str, message: str,
                  auto_fixed: bool = False, fix_method: str = ""):
        err = AgentError(
            agent_name=agent_name,
            error_type=error_type,
            message=message,
            auto_fixed=auto_fixed,
            fix_method=fix_method,
        )
        self.errors.append(err)
        self.log_event(agent_name, EVENT_FAIL, error=message,
                       message=f"[{error_type}] {message}")

    # ─────────────────────────────────────────────────────────
    # PROGRESS UPDATE (fed to SSE stream)
    # ─────────────────────────────────────────────────────────
    def update_progress(self, percent: int, status: str, agent: str = ""):
        self.percent       = min(percent, 100)
        self.status        = status
        self.current_agent = agent
        # Also update shared PROGRESS_DATA for polling compatibility
        try:
            from core.shared import PROGRESS_DATA
            PROGRESS_DATA[self.task_id] = {
                "percent":       self.percent,
                "status":        self.status,
                "current_agent": self.current_agent,
                "agent_log":     [e.to_dict() for e in self.agent_log[-5:]],
            }
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────
    # SELF-HEALING GATE
    # ─────────────────────────────────────────────────────────
    def can_heal(self) -> bool:
        return self.healing_iterations < self.max_healing

    def increment_healing(self):
        self.healing_iterations += 1
        self.log_event(
            "self_healer", EVENT_HEAL,
            message=f"Healing iteration {self.healing_iterations}/{self.max_healing}"
        )

    # ─────────────────────────────────────────────────────────
    # MONGO PERSISTENCE
    # ─────────────────────────────────────────────────────────
    def _persist_event(self, event: AgentEvent):
        if self._mongo_collection is None:
            return
        try:
            self._mongo_collection.insert_one(event.to_dict())
        except Exception:
            pass  # Never let Mongo failure crash the pipeline

    def save_build_summary(self, final_html: str, elapsed: float):
        """Save completed build record to MongoDB."""
        if self._mongo_collection is None:
            return
        try:
            self._mongo_collection.database["builds"].insert_one({
                "task_id":      self.task_id,
                "idea":         self.idea[:200],
                "category":     self.manifest.get("category", ""),
                "sub_type":     self.manifest.get("sub_type", ""),
                "status":       "success",
                "elapsed_s":    elapsed,
                "output_size":  len(final_html),
                "agents_run":   len(self.agent_log),
                "heal_iters":   self.healing_iterations,
                "quality_score": self.quality_score,
                "timestamp":    datetime.utcnow(),
            })
        except Exception:
            pass

    # ─────────────────────────────────────────────────────────
    # SNAPSHOT (for SSE graph updates)
    # ─────────────────────────────────────────────────────────
    def snapshot(self) -> dict:
        return {
            "task_id":        self.task_id,
            "percent":        self.percent,
            "status":         self.status,
            "current_agent":  self.current_agent,
            "quality_score":  self.quality_score,
            "healing_iter":   self.healing_iterations,
            "artifacts_ready": [k for k, v in self.artifacts.items() if v],
            "errors":         len(self.errors),
            "log_count":      len(self.agent_log),
        }
