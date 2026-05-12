# core/agent_system.py — S.E.A.D.S. v9.0 Enterprise
# ============================================================
# 50+ SPECIALIZED AGENTS organized in teams
# Each agent: ONE job, minimal tokens, maximum quality
# ============================================================

# ════════════════════════════════════════════════════════════
# AGENT REGISTRY — All 50+ agents
# ════════════════════════════════════════════════════════════

AGENTS = {

    # ── TIER 1: ORCHESTRATION (5 agents) ────────────────────
    "master_orchestrator": {
        "role":    "Routes user request to correct pipeline",
        "tokens":  0,   # Pure Python logic, no LLM
        "team":    "orchestration",
    },
    "task_analyzer": {
        "role":    "Analyzes complexity, estimates agent count needed",
        "tokens":  150,
        "team":    "orchestration",
    },
    "clarification_agent": {
        "role":    "Generates smart questions before building",
        "tokens":  0,   # Preset questions, no LLM
        "team":    "orchestration",
    },
    "planner_agent": {
        "role":    "Breaks task into ordered subtasks",
        "tokens":  200,
        "team":    "orchestration",
    },
    "quality_controller": {
        "role":    "Final validation, removes alert(), fixes images",
        "tokens":  0,   # Pure regex/string processing
        "team":    "orchestration",
    },

    # ── TIER 2: RESEARCH (5 agents) ─────────────────────────
    "web_researcher": {
        "role":    "Searches Serper for patterns and examples",
        "tokens":  100,
        "team":    "research",
        "api":     "SERPER_API_KEY",
    },
    "github_fetcher": {
        "role":    "Downloads source code from GitHub",
        "tokens":  0,   # HTTP request
        "team":    "research",
        "api":     "GITHUB_TOKEN",
    },
    "rule_engine": {
        "role":    "Provides game/app rules (chess, ludo, social)",
        "tokens":  0,   # Hardcoded rules
        "team":    "research",
    },
    "pattern_matcher": {
        "role":    "Matches user intent to best code pattern",
        "tokens":  0,   # Keyword matching
        "team":    "research",
    },

    # ── TIER 3: ARCHITECTURE (4 agents) ─────────────────────
    "system_architect": {
        "role":    "Designs overall system structure",
        "tokens":  200,
        "team":    "architecture",
    },
    "database_designer": {
        "role":    "Schema design (SQLite/MongoDB)",
        "tokens":  300,
        "team":    "architecture",
    },
    "api_designer": {
        "role":    "REST/WebSocket API endpoint design",
        "tokens":  200,
        "team":    "architecture",
    },
    "state_designer": {
        "role":    "App/game state management design",
        "tokens":  200,
        "team":    "architecture",
    },

    # ── TIER 4: BACKEND (6 agents) ──────────────────────────
    "backend_core": {
        "role":    "FastAPI app setup, CORS, startup",
        "tokens":  400,
        "team":    "backend",
    },
    "backend_routes": {
        "role":    "Route handlers (GET/POST/PUT/DELETE)",
        "tokens":  600,
        "team":    "backend",
    },
    "backend_models": {
        "role":    "Pydantic models, data validation",
        "tokens":  400,
        "team":    "backend",
    },
    "backend_db": {
        "role":    "SQLite/SQLAlchemy setup, migrations",
        "tokens":  300,
        "team":    "backend",
    },
    "backend_auth": {
        "role":    "JWT auth, login/register, middleware",
        "tokens":  500,
        "team":    "backend",
    },
    "backend_websocket": {
        "role":    "WebSocket handlers for real-time features",
        "tokens":  400,
        "team":    "backend",
    },

    # ── TIER 5: FRONTEND (8 agents) ─────────────────────────
    "frontend_layout": {
        "role":    "HTML structure, semantic markup",
        "tokens":  800,
        "team":    "frontend",
    },
    "frontend_styles": {
        "role":    "Advanced CSS, theme, animations",
        "tokens":  700,
        "team":    "frontend",
    },
    "frontend_components": {
        "role":    "Reusable UI components (cards, modals, etc.)",
        "tokens":  600,
        "team":    "frontend",
    },
    "frontend_navigation": {
        "role":    "Nav bars, routing, breadcrumbs",
        "tokens":  300,
        "team":    "frontend",
    },
    "frontend_forms": {
        "role":    "Forms, validation, error states",
        "tokens":  400,
        "team":    "frontend",
    },
    "frontend_data": {
        "role":    "Data fetching, state updates, localStorage",
        "tokens":  500,
        "team":    "frontend",
    },
    "frontend_responsive": {
        "role":    "Mobile CSS, touch events, breakpoints",
        "tokens":  300,
        "team":    "frontend",
    },
    "frontend_accessibility": {
        "role":    "ARIA labels, keyboard nav, contrast",
        "tokens":  200,
        "team":    "frontend",
    },

    # ── TIER 6: GAME (6 agents) ─────────────────────────────
    "game_logic": {
        "role":    "Core game mechanics and rules",
        "tokens":  4000,
        "team":    "game",
    },
    "game_renderer": {
        "role":    "Canvas rendering, draw calls",
        "tokens":  800,
        "team":    "game",
    },
    "game_physics": {
        "role":    "Physics engine (gravity, collision)",
        "tokens":  600,
        "team":    "game",
    },
    "game_ai": {
        "role":    "AI opponents (minimax, pathfinding)",
        "tokens":  1000,
        "team":    "game",
    },
    "game_audio": {
        "role":    "Web Audio API sound effects",
        "tokens":  300,
        "team":    "game",
    },
    "game_state": {
        "role":    "Save/load, high scores, achievements",
        "tokens":  300,
        "team":    "game",
    },

    # ── TIER 7: MEDIA (5 agents) ─────────────────────────────
    "youtube_agent": {
        "role":    "YouTube API integration, video player",
        "tokens":  0,   # Prebuilt HTML
        "team":    "media",
        "api":     "YOUTUBE_API_KEY",
    },
    "music_agent": {
        "role":    "Spotify-like player, Web Audio API",
        "tokens":  3000,
        "team":    "media",
    },
    "movie_agent": {
        "role":    "OMDb movie data, Netflix-like UI",
        "tokens":  0,   # Prebuilt HTML
        "team":    "media",
        "api":     "OMDB_API_KEY",
    },
    "tv_agent": {
        "role":    "JioTV-like live TV streaming UI",
        "tokens":  3000,
        "team":    "media",
    },
    "image_agent": {
        "role":    "Pexels/Unsplash image fetching",
        "tokens":  0,
        "team":    "media",
        "api":     "PEXELS_API_KEY",
    },

    # ── TIER 8: E-COMMERCE (5 agents) ───────────────────────
    "ecommerce_catalog": {
        "role":    "Product listing, search, filter",
        "tokens":  1500,
        "team":    "ecommerce",
    },
    "ecommerce_cart": {
        "role":    "Cart, wishlist, checkout flow",
        "tokens":  800,
        "team":    "ecommerce",
    },
    "ecommerce_payment": {
        "role":    "Payment UI (Razorpay/Stripe integration)",
        "tokens":  600,
        "team":    "ecommerce",
    },
    "ecommerce_orders": {
        "role":    "Order tracking, history, returns",
        "tokens":  500,
        "team":    "ecommerce",
    },
    "ecommerce_recommendations": {
        "role":    "AI product recommendations",
        "tokens":  400,
        "team":    "ecommerce",
    },

    # ── TIER 9: DESIGN TOOLS (4 agents) ─────────────────────
    "canva_integrator": {
        "role":    "Canva-like drag-drop design editor",
        "tokens":  2000,
        "team":    "design",
    },
    "color_palette_agent": {
        "role":    "Generates cohesive color palettes",
        "tokens":  100,
        "team":    "design",
    },
    "typography_agent": {
        "role":    "Font selection and pairing",
        "tokens":  100,
        "team":    "design",
    },

    # ── TIER 10: MOBILE APP (4 agents) ──────────────────────
    "mobile_layout_agent": {
        "role":    "Mobile-first HTML layout",
        "tokens":  600,
        "team":    "mobile",
    },
    "mobile_navigation_agent": {
        "role":    "Bottom nav, drawer, tab bar",
        "tokens":  400,
        "team":    "mobile",
    },
    "pwa_agent": {
        "role":    "Progressive Web App manifest + service worker",
        "tokens":  300,
        "team":    "mobile",
    },
    "mobile_gestures_agent": {
        "role":    "Swipe, pinch, touch gestures",
        "tokens":  300,
        "team":    "mobile",
    },

    # ── TIER 11: BOOKING/SERVICES (3 agents) ────────────────
    "booking_calendar_agent": {
        "role":    "Calendar UI, date/time picker",
        "tokens":  600,
        "team":    "booking",
    },
    "booking_slots_agent": {
        "role":    "Available slots, conflict detection",
        "tokens":  400,
        "team":    "booking",
    },
    "booking_confirmation_agent": {
        "role":    "Confirmation flow, notifications",
        "tokens":  300,
        "team":    "booking",
    },

    # ── TIER 12: INTEGRATION (3 agents) ─────────────────────
    "integration_master": {
        "role":    "Combines all agent outputs into final HTML",
        "tokens":  5000,
        "team":    "integration",
    },
    "backend_integrator": {
        "role":    "Combines backend sub-agents",
        "tokens":  1200,
        "team":    "integration",
    },
    "fixer_agent": {
        "role":    "Fixes bugs in generated code",
        "tokens":  500,
        "team":    "integration",
    },

    # ── TIER 13: QUALITY (3 agents) ──────────────────────────
    "testing_agent": {
        "role":    "Identifies potential bugs in output",
        "tokens":  200,
        "team":    "quality",
    },
    "security_agent": {
        "role":    "XSS prevention, input sanitization",
        "tokens":  200,
        "team":    "quality",
    },
    "performance_agent": {
        "role":    "Lazy loading, code optimization hints",
        "tokens":  200,
        "team":    "quality",
    },

    # ── TIER 14: DOCUMENTATION (2 agents) ───────────────────
    "readme_agent": {
        "role":    "README.md with setup instructions",
        "tokens":  200,
        "team":    "docs",
    },
    "comment_agent": {
        "role":    "Inline code comments",
        "tokens":  0,   # Done by other agents
        "team":    "docs",
    },
}

# ── PIPELINE PROFILES per app type ──────────────────────────
PIPELINES = {
    "ecommerce": {
        "parallel": [
            "ecommerce_catalog", "ecommerce_cart",
            "frontend_styles",   "frontend_responsive",
            "ecommerce_recommendations", "ecommerce_orders",
        ],
        "sequential": ["integration_master"],
        "optional":   ["ecommerce_payment", "backend_auth"],
        "token_est":  8000,
    },
    "music_app": {
        "parallel": [
            "music_agent", "frontend_styles",
            "frontend_responsive", "mobile_navigation_agent",
            "pwa_agent",
        ],
        "sequential": ["integration_master"],
        "token_est":  5000,
    },
    "tv_streaming": {
        "parallel": [
            "tv_agent", "frontend_styles",
            "frontend_responsive", "mobile_navigation_agent",
        ],
        "sequential": ["integration_master"],
        "token_est":  4500,
    },
    "booking_app": {
        "parallel": [
            "booking_calendar_agent", "booking_slots_agent",
            "frontend_styles", "frontend_responsive",
            "mobile_navigation_agent",
        ],
        "sequential": ["booking_confirmation_agent", "integration_master"],
        "token_est":  4000,
    },
    "design_tool": {
        "parallel": [
            "canva_integrator", "frontend_styles",
            "color_palette_agent", "typography_agent",
        ],
        "sequential": ["integration_master"],
        "token_est":  5000,
    },
    "game": {
        "parallel": [
            "game_logic", "game_renderer",
            "game_physics", "game_ai",
            "game_state", "frontend_styles",
        ],
        "sequential": ["integration_master"],
        "token_est":  7000,
    },
    "generic_app": {
        "parallel": [
            "frontend_layout", "frontend_styles",
            "frontend_components", "frontend_data",
            "frontend_responsive",
        ],
        "sequential": ["integration_master"],
        "token_est":  5000,
    },
}


def get_pipeline(app_type: str) -> dict:
    return PIPELINES.get(app_type, PIPELINES["generic_app"])


def count_agents(pipeline: dict) -> int:
    return len(pipeline.get("parallel",[])) + \
           len(pipeline.get("sequential",[])) + \
           len(pipeline.get("optional",[]))


def get_agent_info(name: str) -> dict:
    return AGENTS.get(name, {"role":"Unknown","tokens":500,"team":"misc"})
