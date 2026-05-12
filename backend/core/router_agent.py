# core/router_agent.py — S.E.A.D.S. v15
# ============================================================
# HYBRID ROUTER AGENT (2-Pass)
# Pass 1: Keyword pre-filter (0ms, no LLM)
# Pass 2: Gemini Flash LLM fallback (only when confidence < 0.85)
# Output: RouterManifest dict
# ============================================================

import os, json, re, time
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from dotenv import load_dotenv
load_dotenv()

# ── RouterManifest schema ────────────────────────────────────
@dataclass
class RouterManifest:
    category:       str             # website|mobile|design|ppt|game|ml|ecommerce|more
    sub_type:       str             # portfolio|chess|sentiment|flipkart|...
    confidence:     float           # 0.0 – 1.0
    features:       List[str]       = field(default_factory=list)
    constraints:    List[str]       = field(default_factory=list)
    persona:        str             = ""
    tone:           str             = "professional"
    routing_method: str             = "keyword"   # keyword | llm_fallback
    raw_idea:       str             = ""

    def to_dict(self) -> dict:
        return asdict(self)


# ── Keyword maps (confidence weights) ────────────────────────
KEYWORD_MAP = {
    "game": {
        "keywords": ["chess","ludo","snake","tetris","shooter","fps","zombie","game",
                     "arcade","puzzle","platformer","space invader","temple run",
                     "endless run","subway surf","car race","car racing","flappy",
                     "gravity flip","2048","pacman","breakout","minesweeper","sudoku",
                     "tic tac toe","hangman","wordle","battleship"],
        "weight": 1.0,
    },
    "ml": {
        "keywords": ["machine learning","ml project","prediction","recommender",
                     "recommendation","classifier","classification","clustering",
                     "neural network","deep learning","random forest","xgboost",
                     "sentiment analysis","spam detector","churn prediction",
                     "house price","fraud detection","image recognition"],
        "weight": 1.0,
    },
    "ecommerce": {
        "keywords": ["ecommerce","flipkart","amazon","shopping","shop","store",
                     "cart","buy","product listing","online store","marketplace",
                     "myntra","meesho","nykaa","bigbasket","grofers"],
        "weight": 1.0,
    },
    "design": {
        "keywords": ["photo editor","background remover","image editor","design tool",
                     "canva","banner maker","logo maker","filter tool","image filter",
                     "thumbnail maker","poster maker"],
        "weight": 1.0,
    },
    "ppt": {
        "keywords": ["ppt","presentation","slide","deck","pitch","keynote","slideshow",
                     "powerpoint","google slides"],
        "weight": 1.0,
    },
    "mobile": {
        "keywords": ["mobile app","android app","calculator app","grade tracker",
                     "expense tracker","budget app","flask app","django app",
                     "fastapi app","python app","kivy","beeware","simple app"],
        "weight": 0.9,
    },
    "website": {
        "keywords": ["website","landing page","portfolio site","blog","corporate site",
                     "web page","web design","company website","personal website",
                     "restaurant website","agency website","ngo site","portfolio"],
        "weight": 0.9,
    },
    "more": {
        "keywords": ["youtube","netflix","spotify","jiotv","booking","hotel booking",
                     "appointment","food delivery","swiggy","zomato","weather",
                     "quiz","trivia","chat","kanban","pomodoro","dashboard",
                     "analytics","data viz","visualization","kpi","chart"],
        "weight": 0.9,
    },
}

# Sub-type maps per category
SUB_TYPE_MAP = {
    "game": {
        "chess":      ["chess","checkers"],
        "ludo":       ["ludo","pachisi"],
        "snake":      ["snake"],
        "tetris":     ["tetris","block"],
        "shooter":    ["shooter","fps","zombie","gun","sniper"],
        "puzzle":     ["puzzle","match","sliding","2048","minesweeper","sudoku","wordle"],
        "platformer": ["platformer","runner","jump","side-scroll","temple run","endless run","subway surf","flappy"],
        "arcade":     ["space invader","pacman","breakout","arcade","retro"],
        "racing":     ["car race","racing","drive","speed"],
        "board":      ["board game","tic tac toe","hangman","battleship"],
    },
    "ml": {
        "house_price":    ["house","property","real estate","price prediction"],
        "recommender":    ["recommend","movie recommender","collaborative"],
        "spam":           ["spam","fraud","fake","phishing"],
        "churn":          ["churn","attrition","retention"],
        "sentiment":      ["sentiment","nlp","review","opinion"],
        "classifier":     ["classifier","classification","image recognition"],
        "clustering":     ["clustering","segmentation","k-means"],
    },
    "website": {
        "portfolio":  ["portfolio","personal site","my work"],
        "restaurant": ["restaurant","cafe","food","bakery"],
        "startup":    ["startup","saas","landing page"],
        "corporate":  ["corporate","company","business"],
        "agency":     ["agency","studio","creative"],
        "blog":       ["blog","news","magazine"],
        "ngo":        ["ngo","nonprofit","charity"],
    },
    "ecommerce": {
        "fashion":      ["fashion","clothing","boutique","apparel","myntra","meesho"],
        "electronics":  ["electronics","gadget","laptop","mobile"],
        "grocery":      ["grocery","supermarket","bigbasket"],
        "beauty":       ["beauty","cosmetics","skincare","nykaa"],
        "flipkart":     ["flipkart"],
        "amazon":       ["amazon","international"],
    },
    "more": {
        "youtube_clone": ["youtube","video platform"],
        "netflix_clone":  ["netflix","movie app","hotstar","prime video"],
        "spotify_clone":  ["spotify","music streaming","music app"],
        "food_delivery":  ["swiggy","zomato","food delivery"],
        "weather":        ["weather"],
        "chat":           ["chat","messenger","whatsapp"],
        "dashboard":      ["dashboard","analytics","kpi","data viz"],
    },
}

PERSONA_KEYWORDS = {
    "data scientist":  ["data scientist","data science","data analyst"],
    "developer":       ["developer","programmer","coder","software engineer"],
    "designer":        ["designer","ui designer","ux designer","graphic designer"],
    "photographer":    ["photographer","photography"],
    "student":         ["student","college","university","school"],
    "freelancer":      ["freelancer","freelance"],
    "doctor":          ["doctor","medical","healthcare"],
    "teacher":         ["teacher","educator","professor"],
}

FEATURE_SIGNALS = {
    "auth":       ["login","register","signup","authentication","auth","jwt"],
    "dark mode":  ["dark","dark mode","dark theme"],
    "real-time":  ["real-time","realtime","websocket","live","multiplayer"],
    "payment":    ["payment","razorpay","stripe","checkout","buy"],
    "ai":         ["ai","smart","intelligent","ml","chatbot","gpt"],
    "search":     ["search","filter","find"],
    "mobile":     ["mobile","responsive","pwa","app"],
    "3d":         ["3d","three.js","webgl","threejs"],
}

CONSTRAINT_SIGNALS = {
    "no backend":    ["no backend","frontend only","static","client-side only"],
    "single file":   ["single file","one file","all in one","self-contained"],
    "no database":   ["no db","no database","without database"],
    "open source":   ["open source","free","no paid api"],
}


def _keyword_pass(idea: str) -> RouterManifest:
    """Pass 1: Fast keyword matching — returns manifest with confidence score."""
    u = idea.lower()
    best_category = "more"
    best_confidence = 0.0

    for category, config in KEYWORD_MAP.items():
        for kw in config["keywords"]:
            if kw in u:
                score = config["weight"]
                # Boost for exact/longer matches
                if u.startswith(kw) or f" {kw}" in u:
                    score = min(score + 0.05, 1.0)
                if score > best_confidence:
                    best_confidence = score
                    best_category = category

    # Detect sub_type
    sub_type = "general"
    if best_category in SUB_TYPE_MAP:
        for st, kws in SUB_TYPE_MAP[best_category].items():
            if any(kw in u for kw in kws):
                sub_type = st
                break

    # Detect persona
    persona = ""
    for p, kws in PERSONA_KEYWORDS.items():
        if any(kw in u for kw in kws):
            persona = p
            break

    # Detect features
    features = [feat for feat, kws in FEATURE_SIGNALS.items() if any(kw in u for kw in kws)]

    # Detect constraints
    constraints = [c for c, kws in CONSTRAINT_SIGNALS.items() if any(kw in u for kw in kws)]

    # Tone
    tone = "professional + technical" if best_category in ["ml","mobile"] else "creative + modern"

    return RouterManifest(
        category=best_category,
        sub_type=sub_type,
        confidence=best_confidence,
        features=features,
        constraints=constraints,
        persona=persona,
        tone=tone,
        routing_method="keyword",
        raw_idea=idea,
    )


def _llm_pass(idea: str) -> RouterManifest:
    """Pass 2: Gemini Flash semantic fallback for ambiguous inputs."""
    try:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_KEY_1") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No Gemini key")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""You are a routing classifier for an AI product factory.
Analyze this user request and return ONLY valid JSON (no markdown):

User request: "{idea}"

Return this exact schema:
{{
  "category": "website|mobile|design|ppt|game|ml|ecommerce|more",
  "sub_type": "specific sub-category string",
  "confidence": 0.95,
  "features": ["list", "of", "detected", "features"],
  "constraints": ["list", "of", "constraints"],
  "persona": "detected user persona or empty string",
  "tone": "professional|creative|playful|technical"
}}

Categories:
- website: landing pages, portfolios, corporate sites, blogs
- mobile: Python/Flask apps, calculator tools, simple apps
- design: photo editors, banner makers, logo tools, Canva-like
- ppt: presentations, slides, pitch decks
- game: any game (chess, snake, shooter, puzzle, racing, etc.)
- ml: machine learning, prediction, classification, recommendation
- ecommerce: online stores, shopping, cart, product listings
- more: YouTube/Netflix/Spotify clones, booking, weather, chat, dashboard

Return ONLY the JSON object:"""

        response = model.generate_content(prompt)
        raw = response.text.strip()
        raw = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(raw)

        return RouterManifest(
            category=data.get("category", "more"),
            sub_type=data.get("sub_type", "general"),
            confidence=float(data.get("confidence", 0.80)),
            features=data.get("features", []),
            constraints=data.get("constraints", []),
            persona=data.get("persona", ""),
            tone=data.get("tone", "professional"),
            routing_method="llm_fallback",
            raw_idea=idea,
        )

    except Exception as e:
        print(f"[ROUTER] LLM fallback failed: {e} — using keyword result")
        return None


def route(idea: str, threshold: float = 0.85) -> RouterManifest:
    """
    Main entry point.
    Returns RouterManifest via hybrid 2-pass routing.
    """
    t0 = time.time()

    # Pass 1: Keyword
    manifest = _keyword_pass(idea)
    method = "keyword"

    # Pass 2: LLM fallback if confidence below threshold
    if manifest.confidence < threshold:
        print(f"[ROUTER] Confidence {manifest.confidence:.2f} < {threshold} → LLM fallback")
        llm_result = _llm_pass(idea)
        if llm_result:
            manifest = llm_result
            method = "llm_fallback"

    elapsed = round((time.time() - t0) * 1000, 1)
    print(f"[ROUTER] '{idea[:60]}' → {manifest.category}/{manifest.sub_type} "
          f"(conf={manifest.confidence:.2f}, method={method}, {elapsed}ms)")

    return manifest


# ── Standalone test ──────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        "build a chess game with AI opponent",
        "create something like Notion but for teams",
        "make a flipkart clone with cart and payment",
        "sentiment analysis on twitter data with XGBoost",
        "I want a dark glassmorphism portfolio website",
        "build an app to track my daily expenses",
    ]
    for t in tests:
        m = route(t)
        print(f"  → {m.category}/{m.sub_type} [{m.confidence:.0%}] via {m.routing_method}")
        print()
