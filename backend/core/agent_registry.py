# core/agent_registry.py
# ============================================================
# 20+ SPECIALIZED AGENTS — each has ONE job, minimal tokens
# Orchestrator decides which agents run based on task type
# All agents run CONCURRENTLY via ThreadPoolExecutor
# ============================================================

from core.llm_config import get_llm_response
import concurrent.futures
import time

# ── Token budgets per agent (keep LOW!) ─────────────────────
BUDGETS = {
    "clarify":      150,   # Just 3 questions
    "architect":    300,   # File structure only
    "game_logic":  2000,   # Chess/game rules — needs more
    "ui_designer": 2000,   # HTML/CSS shell — needs room for full UI
    "backend":     1200,   # FastAPI/Flask routes
    "database":     400,   # Schema only
    "auth":         600,   # Login/register
    "state":        500,   # State management
    "animation":    600,   # CSS/JS animations
    "api_design":   400,   # Endpoint list
    "ai_feature":   800,   # AI/ML integration
    "search":       500,   # Search functionality
    "social":       700,   # Social features (like/comment)
    "realtime":     600,   # WebSocket/real-time
    "payment":      800,   # Payment UI
    "dashboard":    800,   # Analytics/charts
    "mobile":       400,   # Mobile responsive
    "security":     300,   # Security checklist
    "integrator":  8000,   # Combines all pieces — MUST be large for full HTML
    "reviewer":     400,   # Quality check
    "preview":     6000,   # Final runnable HTML
    "docs":         300,   # README
}

# ── Which agents to spawn per app type ──────────────────────
AGENT_PROFILES = {
    "chess": [
        "architect", "game_logic", "ui_designer",
        "state", "animation", "integrator", "preview"
    ],
    "car_game": [
        "architect", "game_logic", "ui_designer",
        "state", "animation", "integrator", "preview"
    ],
    "fps_game": [
        "architect", "game_logic", "ui_designer",
        "state", "animation", "ai_feature", "integrator", "preview"
    ],
    "rpg": [
        "architect", "game_logic", "ui_designer",
        "state", "database", "ai_feature", "animation", "integrator", "preview"
    ],
    "mmo": [
        "architect", "game_logic", "ui_designer",
        "state", "database", "auth", "realtime",
        "ai_feature", "animation", "integrator", "preview"
    ],
    "battle_royale": [
        "architect", "game_logic", "ui_designer",
        "state", "realtime", "ai_feature",
        "animation", "integrator", "preview"
    ],
    "linkedin": [
        "architect", "backend", "database", "auth",
        "ui_designer", "social", "search",
        "animation", "mobile", "integrator", "preview"
    ],
    "ecommerce": [
        "architect", "backend", "database", "auth",
        "ui_designer", "search", "payment",
        "dashboard", "mobile", "integrator", "preview"
    ],
    "chat_app": [
        "architect", "backend", "database", "auth",
        "ui_designer", "realtime", "ai_feature",
        "animation", "mobile", "integrator", "preview"
    ],
    "dashboard": [
        "architect", "backend", "database",
        "ui_designer", "dashboard", "api_design",
        "animation", "mobile", "integrator", "preview"
    ],
    "todo": [
        "architect", "ui_designer", "database",
        "animation", "mobile", "integrator", "preview"
    ],
    "default": [
        "architect", "backend", "ui_designer",
        "database", "animation", "integrator", "preview"
    ],
}


def detect_profile(user_input: str, answers: dict) -> str:
    u = user_input.lower()
    a = str(answers).lower()
    combined = u + " " + a

    if any(w in combined for w in ["chess", "checkers", "board game"]):
        return "chess"
    if any(w in combined for w in ["car", "racing", "drive", "speed"]):
        return "car_game"
    if any(w in combined for w in ["fps", "shoot", "bullet", "sniper", "counter"]):
        return "fps_game"
    if any(w in combined for w in ["rpg", "role play", "dungeon", "quest", "adventure"]):
        return "rpg"
    if any(w in combined for w in ["mmo", "massively", "multiplayer online", "world of"]):
        return "mmo"
    if any(w in combined for w in ["battle royale", "pubg", "fortnite", "free fire"]):
        return "battle_royale"
    if any(w in combined for w in ["linkedin", "professional", "network", "job"]):
        return "linkedin"
    if any(w in combined for w in ["shop", "store", "ecommerce", "product", "buy",
                                     "flipkart", "amazon", "myntra", "cart", "checkout",
                                     "e-commerce", "shopping", "marketplace"]):
        return "ecommerce"
    if any(w in combined for w in ["chat", "message", "whatsapp", "telegram"]):
        return "chat_app"
    if any(w in combined for w in ["dashboard", "analytics", "chart", "kpi"]):
        return "dashboard"
    if any(w in combined for w in ["todo", "task", "note", "reminder"]):
        return "todo"
    return "default"


def get_agent_list(profile: str, answers: dict) -> list:
    agents = AGENT_PROFILES.get(profile, AGENT_PROFILES["default"]).copy()

    # Dynamically add agents based on answers
    features = str(answers).lower()
    if "multiplayer" in features and "realtime" not in agents:
        agents.insert(-2, "realtime")
    if "login" in features or "auth" in features and "auth" not in agents:
        agents.insert(-2, "auth")
    if "payment" in features and "payment" not in agents:
        agents.insert(-2, "payment")
    if "ai" in features or "smart" in features and "ai_feature" not in agents:
        agents.insert(-2, "ai_feature")

    return agents
