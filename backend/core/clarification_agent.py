# core/clarification_agent.py — S.E.A.D.S. v14
# ============================================================
# CLARIFICATION AGENT
# Step 1 + 2 from v14 Master: Intent Parsing + Dynamic Questions
# Returns: { questions: [...], intent: {...} }
# ============================================================

from core.llm_config import get_llm_response
from core.agent_registry import BUDGETS   # token budgets
import json, re

CLARIFY_SYSTEM = """You are a product manager AI. Return ONLY valid JSON. No markdown, no commentary."""

CLARIFY_PROMPT = """
User wants to build: "{idea}"

Your task: The user provided a short text. You must expand it into a proper, highly detailed project description. Generate exactly 4 smart, specific clarification questions AND parse the intent, including choosing the best AI model for this task.

Return this EXACT JSON structure:
{{
  "intent": {{
    "intent":   "build",
    "category": "<detected category: website|mobile|design|ppt|game|ml|ecommerce|more>",
    "sub_type": "<specific sub-type, e.g. portfolio|restaurant|house_price|churn>",
    "proper_description": "<expand the user's short idea into a proper, highly detailed project description>",
    "best_model": "<choose best model for this: e.g. DeepSeek V3, Claude 3 Opus, Qwen 2.5, etc.>",
    "persona":  "<target user/persona if mentioned, else empty string>",
    "tone":     "<professional|creative|technical|playful>",
    "features": ["<key feature 1>","<key feature 2>"],
    "implicit": ["<inferred feature 1, e.g. dark theme>","<inferred feature 2>"],
    "constraints": []
  }},
  "questions": [
    {{
      "id": "q1",
      "text": "<specific question relevant to '{idea}'>",
      "type": "choice",
      "options": ["<option A>","<option B>","<option C>","<option D>"]
    }},
    {{
      "id": "q2",
      "text": "<feature/functionality question>",
      "type": "multi",
      "options": ["<opt 1>","<opt 2>","<opt 3>","<opt 4>","<opt 5>"]
    }},
    {{
      "id": "q3",
      "text": "<design/theme/style question>",
      "type": "choice",
      "options": ["<dark style>","<light style>","<colorful style>","<minimal style>"]
    }},
    {{
      "id": "q4",
      "text": "<target audience or special requirement question>",
      "type": "choice",
      "options": ["<option 1>","<option 2>","<option 3>"]
    }}
  ]
}}

Make sure the proper_description is exhaustive. Make ALL questions SPECIFIC to "{idea}". Do NOT use generic questions.
Return ONLY valid JSON:
"""

# ── Pre-built question sets (zero tokens for common apps!) ──
PRESET_QUESTIONS = {
    "chess": [
        {"id":"q1","text":"Game mode?","type":"choice","options":["vs Computer AI","2 Players local","AI vs AI"]},
        {"id":"q2","text":"AI difficulty?","type":"choice","options":["Easy","Medium","Hard","All levels"]},
        {"id":"q3","text":"Board theme?","type":"choice","options":["Classic wood","Dark neon","Minimal white","Retro pixel"]},
        {"id":"q4","text":"Extra features?","type":"multi","options":["Move history","Hints","Undo move","Timer","Chat"]},
    ],
    "car": [
        {"id":"q1","text":"Game view?","type":"choice","options":["Top-down 2D","Side scroll","3D perspective"]},
        {"id":"q2","text":"Game style?","type":"choice","options":["Dodge obstacles","Race track","Open world","Police chase"]},
        {"id":"q3","text":"Difficulty?","type":"choice","options":["Casual","Medium","Hard","Progressive"]},
        {"id":"q4","text":"Extra features?","type":"multi","options":["High scores","Power-ups","Multiple cars","Sound effects","Night mode"]},
    ],
    "fps": [
        {"id":"q1","text":"FPS type?","type":"choice","options":["Zombie shooter","Space shooter","Military","Sci-fi"]},
        {"id":"q2","text":"Mode?","type":"choice","options":["Single player","Multiplayer","Wave survival","Story mode"]},
        {"id":"q3","text":"Weapons?","type":"multi","options":["Pistol","Shotgun","Sniper","Rifle","Grenades"]},
        {"id":"q4","text":"Map style?","type":"choice","options":["Urban city","Jungle","Space station","Desert"]},
    ],
    "linkedin": [
        {"id":"q1","text":"Main features?","type":"multi","options":["Profile page","Job feed","Connections","Messaging","Notifications"]},
        {"id":"q2","text":"Color theme?","type":"choice","options":["LinkedIn blue","Dark mode","Professional grey","Green tech"]},
        {"id":"q3","text":"User type focus?","type":"choice","options":["Job seeker","Recruiter","Company","Student"]},
        {"id":"q4","text":"Extra?","type":"multi","options":["AI job match","Skills endorsement","Post feed","Stories","Analytics"]},
    ],
    "chat": [
        {"id":"q1","text":"Chat type?","type":"choice","options":["1-on-1 only","Group chats","Channels","All types"]},
        {"id":"q2","text":"Extra features?","type":"multi","options":["File sharing","Voice notes","Reactions","Threads","Search"]},
        {"id":"q3","text":"Theme?","type":"choice","options":["WhatsApp style","Telegram style","Discord style","Custom dark"]},
        {"id":"q4","text":"AI features?","type":"multi","options":["Smart replies","Translation","Summarize chat","Bot integration"]},
    ],
    "ecommerce": [
        {"id":"q1","text":"Shop type?","type":"choice","options":["General store","Fashion","Electronics","Food delivery","Services"]},
        {"id":"q2","text":"Features?","type":"multi","options":["Cart","Wishlist","Reviews","Search filter","Compare"]},
        {"id":"q3","text":"Payment?","type":"choice","options":["Show UI only","Stripe integration","PayPal","Multiple options"]},
        {"id":"q4","text":"Theme?","type":"choice","options":["Modern minimal","Bold colorful","Luxury dark","Clean white"]},
    ],
    "zombie": [
        {"id":"q1","text":"Perspective?","type":"choice","options":["3D First Person","Top-down 2D","Side-scroller"]},
        {"id":"q2","text":"Gameplay?","type":"choice","options":["Wave survival","Story campaign","Open world loot","Tower defense"]},
        {"id":"q3","text":"Visuals?","type":"choice","options":["Hyper-realistic dark","Pixel art retro","Stylized low-poly"]},
        {"id":"q4","text":"Multiplayer?","type":"choice","options":["Single player only","Co-op squads","PvP Arena"]},
    ],
}


def get_preset(user_input: str) -> list | None:
    u = user_input.lower()
    if any(w in u for w in ["chess", "checkers"]): return PRESET_QUESTIONS["chess"]
    if any(w in u for w in ["car", "racing", "drive"]): return PRESET_QUESTIONS["car"]
    if any(w in u for w in ["fps", "shoot", "sniper"]): return PRESET_QUESTIONS["fps"]
    if any(w in u for w in ["linkedin", "professional network"]): return PRESET_QUESTIONS["linkedin"]
    if any(w in u for w in ["chat", "message", "whatsapp"]): return PRESET_QUESTIONS["chat"]
    if any(w in u for w in ["shop", "store", "ecommerce"]): return PRESET_QUESTIONS["ecommerce"]
    if any(w in u for w in ["zombie", "horror", "undead"]): return PRESET_QUESTIONS["zombie"]
    if any(w in u for w in ["shooter", "fps", "gun", "war"]): return PRESET_QUESTIONS["fps"]
    return None


def run_clarification(user_input: str) -> list:
    """
    Returns list of questions for user to answer dynamically via LLM.
    Also returns structured intent if available via run_clarification_full().
    """
    # Try LLM to generate smart questions + intent
    print(f"  [LLM] Generating v14 smart questions + intent parse...")
    try:
        raw = get_llm_response(
            prompt=CLARIFY_PROMPT.format(idea=user_input),
            max_tokens=BUDGETS.get("clarify", 400) * 2,
            system=CLARIFY_SYSTEM,
            task_type="smart"
        )
        clean = re.sub(r"```json|```", "", raw).strip()
        data  = json.loads(clean)

        # Handle both formats: {questions:[...]} and {intent:{...}, questions:[...]}
        if "questions" in data:
            return data["questions"]
    except Exception as e:
        print(f"  [WARN] LLM clarification failed: {e}")

    return []


def run_clarification_full(user_input: str) -> dict:
    """
    v14: Returns BOTH questions AND structured intent.
    Used by /api/clarify to expose intent object to frontend.
    """
    print(f"  [LLM] v14 full clarification (intent + questions)...")
    try:
        raw = get_llm_response(
            prompt=CLARIFY_PROMPT.format(idea=user_input),
            max_tokens=BUDGETS.get("clarify", 400) * 2,
            system=CLARIFY_SYSTEM,
            task_type="smart"
        )
        if not raw:
            raise ValueError("Empty LLM response")

        # Step 1: Strip think tags (DeepSeek R1)
        clean = re.sub(r"<think>[\s\S]*?</think>", "", raw).strip()

        # Step 2: Try to extract JSON block (most robust)
        # Try: outermost { ... } block
        json_match = re.search(r"(\{[\s\S]*\})", clean)
        if json_match:
            clean = json_match.group(1)
        else:
            # Fallback: strip markdown fences
            clean = re.sub(r"```json|```", "", clean).strip()

        # Step 3: Parse JSON
        data = json.loads(clean)
        questions = data.get("questions", [])
        intent    = data.get("intent", {})

        # Validate questions format
        valid_questions = []
        for q in questions:
            if isinstance(q, dict) and "id" in q and "text" in q:
                if "options" not in q:
                    q["options"] = []
                if "type" not in q:
                    q["type"] = "choice"
                valid_questions.append(q)
        
        return {"questions": valid_questions, "intent": intent}

    except Exception as e:
        print(f"  [WARN] Full clarification failed: {e}")
        # Fallback: use preset questions based on keywords
        preset = get_preset(user_input)
        return {"questions": preset or [], "intent": {}}
