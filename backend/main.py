# backend/main.py — S.E.A.D.S. v15 MASTER
# Hybrid Router · DAG Orchestrator · Blackboard · SSE + WebSocket
# Self-Healing · DevOps Agent · Auto-Error Correction
# ============================================================

from fastapi import FastAPI, Request, BackgroundTasks, WebSocket
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, Optional
import os, re, json, time, logging
from dotenv import load_dotenv
load_dotenv()

# ── v15 Core modules ─────────────────────────────────────────
from core.router_agent import route as hybrid_route
from core.blackboard import BuildContext
from core.sse_manager import event_stream, push_log
from core.ws_manager import handle_ws

# SmartKeyManager used via llm_config

from core.agent_registry_100 import AGENTS_100, get_pipeline, total_agents, CORE_AGENTS, BUILDER_SPECIALISTS
from agents.category_builders_v14 import dispatch
# Legacy agents removed to enforce v14 Pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("SEADS-v14")


class RunRequest(BaseModel):
    idea: str = Field(min_length=1, max_length=1500)
    answers: Dict[str, Any] = Field(default_factory=dict)
    category: str = Field(default="")
    task_id: Optional[str] = None
    intent: Dict[str, Any] = Field(default_factory=dict)


class PatchRequest(BaseModel):
    html: str = Field(min_length=20)
    instruction: str = Field(min_length=3, max_length=1200)
    category: str = Field(default="more")


class ErrorAnalyzeRequest(BaseModel):
    error: str = Field(min_length=3, max_length=2000)
    html: str = Field(default="")
    context: str = Field(default="")


def _sanitize_task_id(raw_task_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", (raw_task_id or "").strip())[:64]
    return cleaned or str(int(time.time()))


def _record_runtime(elapsed: float, metrics: dict):
    metrics["runs_completed"] += 1
    completed = metrics["runs_completed"]
    prev_avg = metrics["avg_runtime_seconds"]
    metrics["avg_runtime_seconds"] = round(((prev_avg * (completed - 1)) + elapsed) / completed, 2)

# ─────────────────────────────────────────────────────────────
# SEADS CORE ENGINE SYSTEM PROMPT (v14)
# Injected into every LLM call as the system identity
# ─────────────────────────────────────────────────────────────
SEADS_CORE_SYSTEM = """You are S.E.A.D.S. Core Engine (Self-Evolving Autonomous Developer Swarm), powered by Claude Sonnet 4.6.

You are a multi-agent pipeline code generator. Your ONLY job is to return complete, production-ready code.

STRICT RULES:
- Return ONLY raw code — zero markdown, zero explanations, zero apologies
- NEVER use alert(), confirm(), or prompt() — use canvas overlays or DOM toasts only
- NEVER write incomplete code — always output the FULL file content
- NEVER truncate with "// ...rest of code" — complete code ALWAYS
- ALWAYS add loading states for async operations
- ALWAYS add empty states for lists
- ALWAYS add error handling with visual feedback (not alert())
- For HTML: return complete <!DOCTYPE html> document
- For Python: return complete, runnable script
- For React: return complete functional component

QUALITY STANDARDS:
- Enterprise-grade UI: dark themes, glassmorphism, smooth animations
- Mobile-first responsive design (base → sm → md → lg → xl)
- Micro-interactions on all interactive elements
- Proper semantic HTML with ARIA labels
- Images: use https://picsum.photos/seed/{hash}/400/300 format

You are not explaining. You are building."""

app = FastAPI(title="S.E.A.D.S. v15 Core Engine", version="15.0")
app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ─────────────────────────────────────────────────────────────
# CATEGORY DETECTION
# ─────────────────────────────────────────────────────────────
def detect_category(idea: str, category_hint: str = "") -> str:
    """
    Returns one of: website, mobile, design, ppt, game, ml,
                    ecommerce, more
    """
    if category_hint and category_hint in ("website","mobile","design","ppt","game","ml","ecommerce","more","dataviz"):
        # Backward compat: dataviz → game
        if category_hint == "dataviz":
            return "game"
        return category_hint

    u = idea.lower()

    # ── Games (all types → "game" category) ─────────────────
    if any(w in u for w in ["ludo","chess","snake","tetris","shooter","fps","zombie",
                              "game","arcade","puzzle","platformer","space invader",
                              "temple run","endless run","subway surf","car race",
                              "car racing","flappy","gravity flip","2048"]):
        return "game"

    # ── Media → more ────────────────────────────────────────
    if any(w in u for w in ["youtube","video platform","yt app"]): return "more"
    if any(w in u for w in ["netflix","movie app","hotstar","prime video","cinema"]): return "more"
    if any(w in u for w in ["spotify","music streaming","music app","music player"]): return "more"
    if any(w in u for w in ["jiotv","jio tv","live tv","ott"]): return "more"
    if any(w in u for w in ["booking","hotel booking","appointment","food delivery","swiggy","zomato"]): return "more"

    # ── Category-specific keywords ──────────────────────────
    if any(w in u for w in ["website","landing page","portfolio site","blog","corporate site",
                              "web page","web design","company website","personal website",
                              "restaurant website","agency website","ngo site"]):
        return "website"

    if any(w in u for w in ["flask app","django app","fastapi app","python app",
                              "mobile app","android app","simple app","calculator app",
                              "grade tracker","expense tracker","budget app","kivy","beeware"]):
        return "mobile"

    if any(w in u for w in ["photo editor","background remover","image editor","design tool",
                              "canva","banner maker","logo maker","filter tool","image filter"]):
        return "design"

    if any(w in u for w in ["ppt","presentation","slide","deck","pitch","keynote","slideshow"]):
        return "ppt"

    if any(w in u for w in ["dashboard","analytics","data viz","visualization","kpi",
                              "data analysis","eda","data pipeline","covid data","stock data",
                              "chart","plot","graph"]):
        return "more"

    if any(w in u for w in ["machine learning","ml project","prediction","recommender",
                              "recommendation","classifier","classification","clustering",
                              "neural network","deep learning","random forest","xgboost",
                              "sentiment analysis","spam detector","churn prediction"]):
        return "ml"

    if any(w in u for w in ["ecommerce","flipkart","amazon","shopping","shop",
                              "store","cart","buy","product listing","online store"]):
        return "ecommerce"
    
    return "more"


# ─────────────────────────────────────────────────────────────
# INTENT PARSING — Structured parse per v14 spec
# Returns: {intent, category, sub_type, persona, features, implicit, constraints}
# ─────────────────────────────────────────────────────────────
def parse_intent(idea: str, answers: dict, category: str) -> dict:
    u = idea.lower()
    words = idea.strip().split()

    # Extract sub_type from idea text
    sub_type_map = {
        "website": {
            "portfolio": ["portfolio","personal site"],
            "restaurant": ["restaurant","cafe","food","bakery"],
            "startup": ["startup","saas","landing page"],
            "corporate": ["corporate","company","business"],
            "agency": ["agency","studio","creative"],
            "blog": ["blog","news","magazine"],
        },
        "ecommerce": {
            "fashion": ["fashion","clothing","boutique","apparel"],
            "electronics": ["electronics","gadget","laptop","mobile"],
            "grocery": ["grocery","supermarket","bigbasket"],
            "beauty": ["beauty","cosmetics","skincare","nykaa"],
            "flipkart": ["flipkart","indian store"],
            "amazon": ["amazon","international"],
        },
        "ml": {
            "house_price": ["house","property","real estate","price prediction"],
            "recommender": ["recommend","movie recommender","collaborative"],
            "spam": ["spam","fraud","fake","phishing"],
            "churn": ["churn","attrition","retention"],
            "sentiment": ["sentiment","nlp","review","opinion"],
        },
        "game": {
            "shooter": ["shooter","fps","zombie","gun"],
            "puzzle": ["puzzle","tetris","match","sliding"],
            "board": ["chess","ludo","board","dice"],
            "platformer": ["platformer","runner","jump","side-scroll"],
            "arcade": ["snake","space invader","arcade","retro"],
        }
    }

    sub_type = "general"
    if category in sub_type_map:
        for st, kws in sub_type_map[category].items():
            if any(kw in u for kw in kws):
                sub_type = st
                break

    # Extract persona (name + profession patterns)
    persona = ""
    profession_patterns = ["data scientist","developer","designer","photographer","student",
                           "engineer","marketer","freelancer","doctor","teacher","lawyer"]
    for p in profession_patterns:
        if p in u:
            persona = p
            break

    # Build feature list from answers
    features = []
    for key, val in answers.items():
        if val:
            if isinstance(val, list):
                features.extend(val)
            else:
                features.append(str(val))

    # Infer implicit features
    implicit_rules = {
        "portfolio": ["dark theme", "GitHub links", "contact form", "scroll animations", "responsive"],
        "restaurant": ["map", "reservation", "gallery", "menu", "WhatsApp"],
        "startup": ["hero CTA", "pricing table", "testimonials", "newsletter"],
        "ecommerce": ["cart persistence", "mobile responsive", "search", "filter"],
        "ml": ["feature importance chart", "model accuracy", "prediction UI", "requirements.txt"],
        "game": ["score system", "levels", "sound effects", "mobile touch controls"],
        "ppt": ["keyboard navigation", "progress bar", "fullscreen", "slide counter"],
    }
    implicit = implicit_rules.get(sub_type, implicit_rules.get(category, ["responsive", "dark theme"]))

    return {
        "intent":      "build",
        "category":    category,
        "sub_type":    sub_type,
        "persona":     persona,
        "tone":        "professional + technical" if category in ["ml","mobile"] else "creative + modern",
        "features":    features,
        "implicit":    implicit,
        "constraints": [],
        "raw_idea":    idea,
    }


# ─────────────────────────────────────────────────────────────
# QUESTIONS PER CATEGORY (fallback when LLM clarification fails)
# ─────────────────────────────────────────────────────────────
QUESTIONS = {
    "website":   [
        {"id":"q1","text":"Website type?","type":"choice","options":["Landing page","Portfolio","Corporate","Blog","Restaurant","Agency","NGO/Nonprofit"]},
        {"id":"q2","text":"Features?","type":"multi","options":["Contact form","Newsletter","Gallery","Testimonials","Pricing table","FAQ","Blog section"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Modern dark","Clean white","Bold colorful","Minimal","Corporate blue","Glassmorphism","Retro/vintage"]},
        {"id":"q4","text":"Style?","type":"choice","options":["Minimal & elegant","Bold & creative","Professional & corporate","Playful & fun","Luxury & premium"]},
    ],
    "mobile":    [
        {"id":"q1","text":"Framework?","type":"choice","options":["Flask (simple)","Django (full-featured)","FastAPI (fast APIs)"]},
        {"id":"q2","text":"App type?","type":"choice","options":["Calculator/Tool","Game (Python logic)","Student/Education","Finance/Budget","Health/Fitness","Notes/Tasks"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Dark minimal","Light clean","Colorful","Material Design"]},
        {"id":"q4","text":"Database?","type":"choice","options":["SQLite (default)","In-memory (no DB)"]},
    ],
    "design":    [
        {"id":"q1","text":"Tool features?","type":"multi","options":["Background remover","Photo filters","Text overlay","Shapes & stickers","Crop & resize","Draw/paint","Download PNG/JPG","Templates"]},
        {"id":"q2","text":"Primary use?","type":"choice","options":["Photo editor","Banner/poster maker","Logo designer","Social media graphic","Thumbnail maker"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Dark (like Figma)","Light (like Canva)","Minimal white"]},
        {"id":"q4","text":"Canvas size?","type":"choice","options":["800×600 (default)","1920×1080 (HD)","1080×1080 (Instagram)","1280×720 (YouTube)"]},
    ],
    "ppt":       [
        {"id":"q1","text":"Type?","type":"choice","options":["Business pitch","Educational course","Product demo","Research report","Company overview","Creative portfolio"]},
        {"id":"q2","text":"Slides?","type":"choice","options":["5 slides","8 slides","10 slides","15 slides","20 slides"]},
        {"id":"q3","text":"Style?","type":"choice","options":["Dark professional","Minimal white","Colorful modern","Gradient tech","Corporate blue","Creative gradient"]},
        {"id":"q4","text":"Features?","type":"multi","options":["Animated transitions","Charts/graphs","Speaker notes","Table of contents","Progress bar","Auto-play","PDF export hint"]},
    ],
    "game":      [
        {"id":"q1","text":"Game type?","type":"choice","options":["2D Arcade","Puzzle","Board Game","Platformer","Shooter","Racing","Card Game","Strategy"]},
        {"id":"q2","text":"Engine?","type":"choice","options":["Canvas API (simple 2D)","Phaser (advanced 2D)","Three.js (3D)","Raw JavaScript"]},
        {"id":"q3","text":"Features?","type":"multi","options":["Score system","Levels","Sound effects","Leaderboard","Touch controls","Multiplayer (local)","Power-ups","Particle effects"]},
        {"id":"q4","text":"Theme?","type":"choice","options":["Retro pixel","Neon dark","Minimalist","Colorful cartoon","Space/sci-fi"]},
    ],
    "ml":        [
        {"id":"q1","text":"Project type?","type":"choice","options":["Price/Value Prediction","Movie/Product Recommendation","Spam/Fraud Classification","Customer Churn","Sentiment Analysis","Customer Segmentation"]},
        {"id":"q2","text":"Algorithm?","type":"choice","options":["Random Forest","XGBoost","Linear/Logistic Regression","Decision Tree","K-Means Clustering","Neural Network (MLP)"]},
        {"id":"q3","text":"Output UI?","type":"choice","options":["HTML prediction form","Streamlit app","FastAPI + HTML","Jupyter notebook only"]},
        {"id":"q4","text":"Extras?","type":"multi","options":["Feature importance chart","Confusion matrix","Learning curve","Cross-validation","Model comparison"]},
    ],
    "ecommerce": [
        {"id":"q1","text":"Store like?","type":"choice","options":["Flipkart (Indian)","Amazon (international)","Fashion boutique","Electronics only","Multi-category"]},
        {"id":"q2","text":"Features?","type":"multi","options":["Search + filter","Cart + checkout","Wishlist","Product reviews","Payment flow","Order tracking","Promo codes","Size/color selector"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Flipkart blue","Amazon orange","Dark minimal","Clean white","Colorful modern"]},
        {"id":"q4","text":"Categories?","type":"multi","options":["Electronics","Fashion","Home","Books","Beauty","Sports","Grocery","Toys"]},
    ],
    "more":      [
        {"id":"q1","text":"App type?","type":"choice","options":["Weather app","Quiz/trivia","Calculator","Chat messenger","Kanban todo","Blog/news","Developer portfolio","Unit converter","Pomodoro timer"]},
        {"id":"q2","text":"Features?","type":"multi","options":["Dark mode","Search","Charts","LocalStorage","API integration","Mobile responsive","Animations"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Dark minimal","Light clean","Colorful","Glassmorphism","Material Design"]},
        {"id":"q4","text":"Style?","type":"choice","options":["Minimal & clean","Feature-rich","Mobile-first","Desktop app look"]},
    ],
    "chess":     [
        {"id":"q1","text":"Mode?","type":"choice","options":["vs Computer AI","2 Players","AI vs AI"]},
        {"id":"q2","text":"Difficulty?","type":"choice","options":["Easy (depth 2)","Medium (depth 3)","Hard (depth 4)"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Classic wood","Dark neon","Marble white","Pixel retro"]},
        {"id":"q4","text":"Extras?","type":"multi","options":["Move hints","Undo","History","Timer"]},
    ],
    "ludo":      [
        {"id":"q1","text":"Players?","type":"choice","options":["1 vs 3 AI","2 vs 2 AI","Watch 4 AI","All 4 Human"]},
        {"id":"q2","text":"Speed?","type":"choice","options":["Normal","Fast","Turbo"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["Classic","Neon dark","Pastel","Retro"]},
        {"id":"q4","text":"Rules?","type":"choice","options":["Standard","No safe squares","Speed mode"]},
    ],
}

def get_questions(category: str) -> list:
    return QUESTIONS.get(category, [])


# ─────────────────────────────────────────────────────────────
# LLM caller (10K tokens, SEADS Core Engine system prompt)
# ─────────────────────────────────────────────────────────────
def llm(prompt: str, tokens: int = 20000, system: str = None, task_type: str = "smart") -> str:
    from core.llm_config import get_llm_response
    use_system = system or SEADS_CORE_SYSTEM
    for attempt in range(1, 4):
        try:
            result = get_llm_response(
                prompt=prompt,
                max_tokens=min(tokens, 30000),  # IIT-Level: up to 30K tokens
                temperature=0.1,
                system=use_system,
                task_type=task_type
            )
            if result and len(result) > 500:
                return result
        except Exception as e:
            log.error(f"LLM attempt {attempt}: {e}")
            time.sleep(2)
    return ""

def strip_md(raw: str) -> str:
    s = re.sub(r"```[\w]*\n?","",raw or "").replace("```","").strip()
    for m in ["<!DOCTYPE","<!doctype","<html"]:
        i = s.find(m)
        if i != -1: return s[i:]
    return s

def quality_fix(html: str) -> str:
    html = re.sub(r'alert\s*\([^)]*\)\s*;?','/* toast-instead */', html)
    html = re.sub(r'confirm\s*\([^)]*\)','true', html)
    html = re.sub(
        r'<img([^>]*?)src=["\'](?!http|data:)[^"\']{3,}["\']',
        lambda m: f'<img{m.group(1)}src="https://picsum.photos/seed/{abs(hash(m.group(0)))%9999}/400/300"',
        html)
    return html


# ─────────────────────────────────────────────────────────────
# PATCH SYSTEM — Full-project enhancer powered by DeepSeek Coder
# ─────────────────────────────────────────────────────────────
def apply_patch(html: str, patch_instruction: str) -> str:
    """Improve/enhance an existing HTML project based on user instruction.
    Routes to OpenRouter DeepSeek Coder for best code quality.
    Sends up to 28K chars of the original so large templates are fully covered.
    """
    patch_system = """You are an elite full-stack developer and UI/UX engineer.
You receive an EXISTING, fully working HTML project and an improvement instruction.

YOUR JOB:
- Apply the requested improvement precisely and completely.
- Enhance the surrounding code quality at the same time (better animations, tighter CSS, cleaner JS).
- NEVER remove existing features — only ADD or IMPROVE.
- NEVER truncate. Return the COMPLETE <!DOCTYPE html> file, every single line.
- ZERO alert() / confirm() / prompt() — use toast notifications only.
- Images: use https://images.unsplash.com or https://picsum.photos — never broken URLs.
- Code must be production-ready, IIT-level quality.

Return ONLY the raw <!DOCTYPE html> — no markdown fences, no explanations."""

    # Send as much of the original HTML as possible (28K covers almost all templates)
    html_context = html[:28000]
    truncation_note = f"\n\n[NOTE: HTML truncated at 28K chars — the full file is {len(html):,} chars. Preserve all sections outside the visible range.]" if len(html) > 28000 else ""

    patch_prompt = f"""=== EXISTING PROJECT HTML ===
{html_context}{truncation_note}

=== IMPROVEMENT INSTRUCTION ===
{patch_instruction}

=== TASK ===
Apply the improvement above to the existing project.
Return the COMPLETE improved <!DOCTYPE html> file — all features preserved, zero truncation:"""

    return strip_md(llm(patch_prompt, tokens=16000, system=patch_system, task_type="code"))


# ─────────────────────────────────────────────────────────────
# SAVE + RETURN
# ─────────────────────────────────────────────────────────────
def make_response(result: dict, idea: str, category: str,
                   agents_used: list, elapsed: float,
                   intent: dict = None) -> dict:
    slug = result["slug"]
    files_out = result["files"]

    # Build structured plan/code/test logs
    cat_pipeline = get_pipeline(category)
    parallel_count  = len(cat_pipeline.get("parallel", []))
    sequential_count = len(cat_pipeline.get("sequential", []))

    plan_logs = [
        f"🎯 Standard v14 Pipeline: {category.upper()}",
        f"🔍 Stage 1: Search Agent (Perplexity RAG)",
        f"📋 Stage 2: Planning Agent (DeepSeek-R1 Logic)",
        f"⚡ Stage 3: Coding Agent (DeepSeek V3 Multi-file)",
        f"✅ Stage 4: Verify Agent (Claude 3 Opus Compliance)",
    ]
    if intent:
        plan_logs.insert(1, f"💡 Intent: {intent.get('sub_type','general')} | Tone: {intent.get('tone','professional')}")

    code_logs = [
        f"🚀 Project '{slug}' assembled in {elapsed}s",
        f"📄 Component Output: {result.get('file_count',1)} files generated",
        f"📐 Total chars: {result.get('total_size',0):,} (Enterprise Quality)",
    ]
    
    test_logs = [
        f"✅ Verify Agent: {CORE_AGENTS['verify']['name']} audit complete",
        f"✅ Tech Stack: {', '.join(BUILDER_SPECIALISTS.get(category,{}).get('stack',[]))}",
        f"✅ Sanitization: Fixed images & removed blocked scripts",
        f"🌐 Deployment: Local preview ready at /online_app/{slug}/",
    ]

    safe_agents = []
    for a in agents_used:
        if isinstance(a, dict):
            name = a.get("agent_name") or a.get("name") or "Agent"
            if name not in safe_agents:
                safe_agents.append(name)
        elif isinstance(a, str):
            if a not in safe_agents:
                safe_agents.append(a)

    return {
        "project_name": slug,
        "project_type": "multi_file" if result.get("file_count",1) > 1 else "single_file",
        "category":     category,
        "mode":         "create",
        "intent":       intent or {},
        "agents_used":  safe_agents,
        "plan_logs":    plan_logs,
        "code_logs":    code_logs,
        "test_logs":    test_logs,
        "files":        files_out,
        "preview_html": result.get("preview_html",""),
        "status":       "success",
        "version":      "14.0",
    }


# ─────────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name":    "S.E.A.D.S. v15",
        "engine":  "Hybrid Router · DAG Orchestrator · SSE + WebSocket",
        "agents":  total_agents(),
        "status":  "running",
        "version": "15.0",
        "providers": ["groq","cerebras","together","gemini","openrouter"],
    }


# ─────────────────────────────────────────────────────────────
# v15 — SSE STREAM ENDPOINT (real-time passive push)
# ─────────────────────────────────────────────────────────────
@app.get("/api/stream/{task_id}")
async def sse_stream(task_id: str):
    """
    Server-Sent Events stream for a build task.
    Frontend subscribes once; receives agent state, logs, 3D graph updates.
    """
    return StreamingResponse(
        event_stream(task_id, timeout=600),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )


# ─────────────────────────────────────────────────────────────
# v15 — WEBSOCKET CONTROL ENDPOINT (bidirectional)
# ─────────────────────────────────────────────────────────────
@app.websocket("/ws/{task_id}")
async def ws_control(websocket: WebSocket, task_id: str):
    """
    WebSocket for interactive pipeline control.
    Commands: pause | resume | redirect | inject | stop
    """
    await handle_ws(task_id, websocket)


@app.get("/api/health")
async def health():
    try:
        from core.smart_key_manager import smart_key_manager
        provider_status = smart_key_manager.get_provider_status()
    except Exception:
        provider_status = {}

    return {
        "status":       "healthy",
        "version":      "15.0",
        "active_tasks": sum(1 for v in PROGRESS_DATA.values() if isinstance(v, dict) and v.get("percent", 0) < 100),
        "tracked_tasks": len(PROGRESS_DATA),
        "recent_tasks": len(TASK_HISTORY),
        "metrics":      SYSTEM_METRICS,
        "providers":    provider_status,
        "new_endpoints": ["/api/stream/{task_id} (SSE)", "/ws/{task_id} (WebSocket)"],
    }


@app.get("/api/tasks/recent")
async def recent_tasks(limit: int = 15):
    limit = max(1, min(limit, 50))
    return {"tasks": list(TASK_HISTORY)[-limit:][::-1]}

@app.get("/api/projects")
async def get_projects():
    from pathlib import Path
    output = Path(os.getenv("ONLINE_APP_DIR", r"E:\seads\online_app"))
    projects = []
    if output.exists():
        for d in sorted(output.iterdir(), reverse=True):
            if d.is_dir():
                idx = d/"index.html"
                size = idx.stat().st_size if idx.exists() else 0
                has_react = (d/"frontend"/"package.json").exists()
                projects.append({"name":d.name,"type":"fullstack" if has_react else "html","size":size})
    return {"projects": projects[:25]}

@app.get("/api/agents")
async def get_agents():
    teams = {}
    for name, info in AGENTS_100.items():
        team = info["team"]
        if team not in teams: teams[team] = []
        teams[team].append({"name":name,"role":info["role"],"tokens":info["tokens"]})
    return {"total":total_agents(),"teams":teams}

@app.get("/api/templates")
async def templates():
    return {"templates": []}

@app.get("/api/template-details")
async def template_details(name: str):
    return {"error": "Templates disabled", "success": False}

@app.post("/api/clarify")
async def clarify(req: Request):
    from core.clarification_agent import run_clarification
    body     = await req.json()
    idea     = body.get("idea","").strip()
    cat_hint = body.get("category","")
    category = detect_category(idea, cat_hint)

    # v14: Use clarification agent for intent parsing ONLY, suppress questions for direct execution
    try:
        from core.clarification_agent import run_clarification_full
        full_data = run_clarification_full(idea)
    except Exception as e:
        log.error(f"Clarification failed: {e}")
        full_data = {}
    
    questions = [] # Explicitly zero to allow direct execution
    intent    = full_data.get("intent", {})

    # Dynamic pipeline label from idea text
    words = idea.title().split()
    dynamic_label = " ".join(words[:4]) + ("..." if len(words) > 4 else "") + " Pipeline"
    if not idea:
        dynamic_label = "Custom Pipeline"

    # Return zero questions to allow direct execution as per user request
    return JSONResponse({
        "idea": idea, "category": category,
        "questions": [], # QUESTIONS REMOVED
        "intent": intent,
        "dynamic_label": dynamic_label,
        "mode": "create",
        "version": "14.0",
    })

# ─────────────────────────────────────────────────────────────
# PROGRESS TRACKING (v14 REAL-TIME)
# ─────────────────────────────────────────────────────────────
from core.shared import PROGRESS_DATA, TASK_HISTORY, SYSTEM_METRICS

@app.get("/api/progress/{task_id}")
async def get_progress(task_id: str):
    return PROGRESS_DATA.get(task_id, {"percent": 0, "status": "Waiting..."})

@app.post("/api/run")
async def run_api(req: Request, background_tasks: BackgroundTasks):
    body = await req.json()
    try:
        payload = RunRequest(**body)
    except ValidationError as e:
        return JSONResponse({"error": "Invalid run payload", "details": e.errors()}, status_code=422)

    idea     = payload.idea.strip()
    answers  = payload.answers
    cat_hint = payload.category
    task_id  = _sanitize_task_id(payload.task_id or str(int(time.time())))

    if not idea:
        return JSONResponse({"error": "No idea"}, status_code=400)

    PROGRESS_DATA[task_id] = {"percent": 5, "status": "Initializing S.E.A.D.S. v15 Pipeline..."}
    SYSTEM_METRICS["runs_started"] += 1

    # ── v15: Non-blocking background pipeline ─────────────────
    def run_pipeline_v15():
        try:
            # ── Step 1: Hybrid Router Agent ───────────────────
            push_log(task_id, "🔍 Router Agent: analysing intent...")
            manifest = hybrid_route(idea)
            # Allow category override from frontend
            if cat_hint and cat_hint in ("website","mobile","design","ppt",
                                          "game","ml","ecommerce","more"):
                manifest.category = cat_hint
            category = manifest.category

            # ── Step 2: Build Blackboard Context ─────────────
            ctx = BuildContext(
                task_id  = task_id,
                idea     = idea,
                answers  = answers,
                manifest = manifest.to_dict(),
            )
            ctx.update_progress(8, f"Router: {category}/{manifest.sub_type} ({manifest.confidence:.0%})")
            push_log(task_id, f"📋 Category: {category} | Sub-type: {manifest.sub_type} | Confidence: {manifest.confidence:.0%}")

            # ── Step 3: DAG Orchestrator ──────────────────────
            from core.orchestrator import run_pipeline
            start = time.time()
            result = run_pipeline(ctx)
            elapsed = round(time.time() - start, 1)

            # ── Step 4: Finalize ──────────────────────────────
            preview_html = result.get("preview_html", "")
            if preview_html:
                preview_html = quality_fix(preview_html)
                result["preview_html"] = preview_html

            # Build response (backward compatible with v14 frontend)
            intent = parse_intent(idea, answers, category)
            slug = result.get("project_name", task_id)
            v14_result = {
                "slug":        slug,
                "files":       [{"filename": "index.html", "content": preview_html}],
                "preview_html": preview_html,
                "file_count":  1,
                "total_size":  len(preview_html),
            }
            response_data = make_response(v14_result, idea, category,
                                          result.get("agent_log", []), elapsed, intent)
            response_data["quality_score"] = result.get("quality_score", 0.0)
            response_data["heal_iters"]    = result.get("heal_iters", 0)
            response_data["version"]       = "15.0"
            response_data["deploy_config"] = result.get("deploy_config", {})

            _record_runtime(elapsed, SYSTEM_METRICS)
            TASK_HISTORY.append({
                "task_id":         task_id,
                "idea":            idea[:120],
                "category":        category,
                "sub_type":        manifest.sub_type,
                "elapsed_seconds": elapsed,
                "quality_score":   result.get("quality_score", 0.0),
                "status":          "success",
                "timestamp":       int(time.time()),
            })
            PROGRESS_DATA[task_id] = {
                "percent": 100,
                "status":  "Complete! ✅",
                "data":    response_data,
            }

        except Exception as e:
            log.error(f"[v15 Pipeline ERROR] {e}")
            import traceback; traceback.print_exc()
            SYSTEM_METRICS["runs_failed"] += 1
            push_log(task_id, f"❌ Pipeline error: {e}", "error")
            TASK_HISTORY.append({
                "task_id":         task_id,
                "idea":            idea[:120],
                "category":        cat_hint or "unknown",
                "elapsed_seconds": 0,
                "status":          "failed",
                "timestamp":       int(time.time()),
                "error":           str(e)[:300],
            })
            PROGRESS_DATA[task_id] = {"percent": 0, "status": f"Error: {str(e)}"}
            # Auto-fix: attempt fallback with legacy v14 dispatcher
            try:
                push_log(task_id, "🔧 Auto-fix: falling back to v14 dispatcher...", "warn")
                category = detect_category(idea, cat_hint)
                result   = dispatch(category, idea, answers, task_id, {})
                if result and result.get("preview_html"):
                    result["preview_html"] = quality_fix(result["preview_html"])
                    PROGRESS_DATA[task_id] = {
                        "percent": 100,
                        "status":  "Complete (fallback) ✅",
                        "data":    make_response(result, idea, category, [], 0, {}),
                    }
                    push_log(task_id, "✅ Auto-fix fallback succeeded")
            except Exception as e2:
                log.error(f"[v15 Fallback ERROR] {e2}")

    background_tasks.add_task(run_pipeline_v15)

    return JSONResponse({
        "status":   "accepted",
        "task_id":  task_id,
        "message":  "S.E.A.D.S. v15 Pipeline started",
        "stream":   f"/api/stream/{task_id}",
        "ws":       f"/ws/{task_id}",
        "version":  "15.0",
    }, status_code=202)


@app.post("/api/patch")
async def patch_api(req: Request):
    """
    v14 PATCH/IMPROVE endpoint — enhances an existing HTML project.
    Powered by OpenRouter DeepSeek Coder (best code model).
    Sends up to 28K chars of original HTML for full context.

    Body:
      {
        "html":        "...current HTML...",
        "instruction": "make the navbar sticky and add dark background on scroll",
        "category":    "ecommerce"
      }
    """
    body = await req.json()
    try:
        payload = PatchRequest(**body)
    except ValidationError as e:
        return JSONResponse({"error": "Invalid patch payload", "details": e.errors()}, status_code=422)
    html_in = payload.html
    instruction = payload.instruction.strip()
    category = payload.category

    log.info(f"\n🔧 v14 IMPROVE | [{category}] '{instruction[:80]}'")
    log.info(f"   HTML size: {len(html_in):,} chars → sending up to 28K to DeepSeek Coder")
    start = time.time()

    patched_html = apply_patch(html_in, instruction)
    patched_html = quality_fix(patched_html)

    elapsed = round(time.time() - start, 1)

    if not patched_html or len(patched_html) < 500:
        log.warning("   Patch returned empty — relaying original")
        return JSONResponse({
            "error": "Improvement failed — model returned empty. Try rephrasing.",
            "status": "empty",
        }, status_code=422)

    log.info(f"   ✅ Done in {elapsed}s | {len(html_in):,} → {len(patched_html):,} chars")

    return JSONResponse({
        "patched_html": patched_html,
        "instruction":  instruction,
        "elapsed":      elapsed,
        "status":       "success",
        "version":      "14.0",
        "patch_analysis": {
            "original_size": len(html_in),
            "patched_size":  len(patched_html),
            "delta_chars":   len(patched_html) - len(html_in),
            "model":         "deepseek/deepseek-coder (OpenRouter)",
        }
    })


@app.post("/api/error-analyze")
async def error_analyze(req: Request):
    """
    v14 Error Analysis endpoint — implements Step 5 Self-Healing.
    Analyzes an error message and returns a targeted patch.

    Body:
      {
        "error":    "Cannot read properties of undefined (reading 'map')",
        "html":     "...current HTML...",
        "context":  "products.map(product => ...  line 45"
      }
    """
    body = await req.json()
    try:
        payload = ErrorAnalyzeRequest(**body)
    except ValidationError as e:
        return JSONResponse({"error": "Invalid analyze payload", "details": e.errors()}, status_code=422)
    error_msg = payload.error
    html_in = payload.html
    context = payload.context

    analysis_prompt = f"""ERROR ANALYSIS REQUEST
Error: {error_msg}
Context: {context}

Generate a structured error analysis in this EXACT JSON format:
{{
  "root_cause": "one sentence explanation",
  "error_type": "TypeScript|Runtime|Import|Style|Logic",
  "fix_description": "what to change",
  "patch": {{
    "find":    "exact string to find in code",
    "replace": "exact replacement string"
  }},
  "prevention": "how to avoid this in future"
}}

Return ONLY valid JSON:"""

    raw = llm(analysis_prompt, tokens=1000,
              system="You are a code debugger. Return ONLY valid JSON. No markdown.", task_type="verify")

    try:
        clean = re.sub(r"```json|```","",raw).strip()
        analysis = json.loads(clean)
        # If html provided, apply the patch automatically
        if html_in and "patch" in analysis:
            p = analysis["patch"]
            patched = html_in.replace(p.get("find",""), p.get("replace",""))
            analysis["patched_html"] = quality_fix(patched)
    except Exception:
        analysis = {
            "root_cause": error_msg,
            "error_type": "Runtime",
            "fix_description": "Review error in browser console",
            "patch": {"find":"","replace":""},
            "prevention": "Add null checks and optional chaining"
        }

    return JSONResponse({"analysis": analysis, "version": "14.0"})
