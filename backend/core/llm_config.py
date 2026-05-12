# core/llm_config.py -- S.E.A.D.S. v14 Multi-Provider Smart Router
# ============================================================
# Routes every LLM call to the BEST available provider:
#   Groq -> Cerebras -> Together -> Gemini -> OpenRouter
# - 10,000 token cap per call (v14 upgrade)
# - Auto-fallback on rate-limit / quota / any error
# - Tracks all usage via SmartKeyManager
# - SEADS v14 Master System Prompt injected by default
# ============================================================

import time
import requests
from groq import Groq
from core.smart_key_manager import smart_key_manager

MAX_TOKENS_PER_REQUEST = 8000  # v14 IIT-Level (capped to 8000 to prevent provider 400 errors)
MAX_RETRIES            = 3      # Fail faster — 3 attempts max per call


# ============================================================
# S.E.A.D.S. v14 MASTER SYSTEM PROMPT
# This controls ALL code generation across every category
# ============================================================
SEADS_V14_SYSTEM_PROMPT = """You are S.E.A.D.S. Core Engine (Self-Evolving Autonomous Developer Swarm), an enterprise-grade AI software architect powered by Claude Sonnet 4.6.

You are NOT a simple code generator. You are a multi-agent pipeline orchestrator that thinks, plans, retrieves context, then builds production-quality applications component by component -- exactly like Lovable AI, v0.dev, and Replit Agent combined.

MULTI-AGENT PIPELINE ARCHITECTURE (Enforced):
- Search Agent: Real-time RAG & Best Practices (Perplexity Sonar)
- Planning Agent: Task Decomposition & Logic (DeepSeek-R1)
- Coding Agent: Component Implementation (DeepSeek V3 / Qwen 2.5)
- Verify Agent: Code Quality & Debugging (Claude 3 Opus)
- Frontend Stack: UI/UX Layer (React + Tailwind + Shadcn)

When a user gives short text, first use Gemini 3.1 FlashLite (or fastest available model) to create a proper description and choose the best model. Then route to the following specific pipelines:

CATEGORY SPECIFIC INSTRUCTIONS:
1. WEBSITE (Landing pages, portfolios, blogs, corporate sites):
   - Use search deeply using Perplexity to see how that website is built.
   - Must use React, Tailwind CSS, and Shadcn UI components.
   - Frontend Stack UI/UX Layer: React + Tailwind + Shadcn.

2. MOBILE APP (Python apps: Flask / Django / FastAPI + SQLite):
   - MUST be Python. Use Kivy or BeeWare.
   - Follow the 7-step lifecycle:
     1. Choose Framework (BeeWare for native, Kivy for custom/OpenGL).
     2. Set Up Env (venv, install briefcase/kivy).
     3. Develop the Application (main.py for logic, .kv for UI in Kivy).
     4. Package for Mobile (Briefcase for BeeWare, Buildozer for Kivy).
     5. Compile Binary (.apk/.aab for Android, .ipa for iOS).
     6. Testing & Debugging.
     7. Show live preview (place show proper user interactive).

3. DESIGN TOOL (Photo editors, background remover, Canva-like tools):
   - Use the best libraries based on task:
     - OpenCV: Real-time & AI, extremely fast.
     - Pillow: Basic Editing (resizing, cropping, text).
     - scikit-image: Scientific Tasks (filtering, segmentation).
     - Albumentations: Machine Learning augmentation.
     - SimpleCV: Rapid Prototyping.

4. SLIDES / PPT (Auto-generate beautiful presentations instantly):
   - Use the best libraries:
     - python-pptx: The industry standard. Automate text/images/charts.
     - Marp (via Markdown): Convert Markdown to PDF/HTML slides.
     - Reveal.js (with Rise): For Jupyter Notebooks live slideshows.
     - Manim: For animated educational/mathematical presentations.

5. DATA VIZ & GAMES (Problem → Collect → Clean → EDA → Visualize / Create Game):
   - If Game/Interactive Web:
     - JavaScript (The Native Choice): Phaser (2D Sandbox), PlayCanvas (3D), Three.js (3D).
     - Lua (Lightweight Option): microStudio (browser-based live coding).

6. ML PROJECT (Full ML projects: data → model → prediction UI):
   - Choose best framework based on type:
     - Traditional ML (tabular/spreadsheets): Scikit-learn
     - Deep Learning (research/prototyping): PyTorch
     - Enterprise / Prod (scale/mobile/edge): TensorFlow / TF Lite
     - NLP / Text: Hugging Face
     - Computer Vision: OpenCV
     - AI Agents: LangChain

7. E-COMMERCE (Shopping sites only: catalog, cart, checkout, payment):
   - Step 1: Frontend (React.js + Tailwind CSS)
   - Step 2: Backend (Node.js + Express)
   - Step 3: Database (MongoDB)
   - Step 4: Authentication (JWT or NextAuth)
   - Step 5: Payment Integration (Stripe or Razorpay API)
   - Step 6: Deployment (Vercel or Render)

STEP 5 -- ITERATIVE SELF-HEALING (Diffing)
When an error occurs, the full code won't be sent back to the AI. Only the error message will be sent, and the AI will provide just a 'patch' (the changed lines). Self-Healing Rules: TypeScript error -> fix types. Logic error -> rewrite specific function.

STEP 10 -- SANDBOX & PREVIEW GENERATION
Create a lovable AI preview interface where the AI is visually appealing, approachable, and friendly. The preview should be properly displayed with smooth design elements, ensuring clarity and accessibility. Include interactive features that allow the user to engage with the AI preview naturally, such as clickable buttons, hover effects, or simple dialogue interactions. The overall experience should feel welcoming, intuitive, and easy to navigate.

ABSOLUTE RULES:
1. NEVER generate single HTML file for multi-file requested websites
2. NEVER use alert(), confirm(), prompt() (always Toast/Dialog)
3. ALWAYS output file path before code
4. ALWAYS create lovable preview HTML alongside multi-file output
5. For web apps, ALWAYS use HTML 5.2 semantics, advanced-level structure, and include dynamic/realistic images (via Unsplash, e.g., https://images.unsplash.com/photo-...)."""


def get_llm_response(
    prompt:      str,
    model:       str   = None,     # None = auto-selected per provider
    max_tokens:  int   = 10000,    # v14 default: 10K tokens
    system:      str   = None,     # None = use SEADS_V14_SYSTEM_PROMPT
    temperature: float = 0.2,
    task_type:   str   = "smart",  # "fast" | "smart" | "code"
) -> str:
    """
    Smart LLM router with multi-provider auto-fallback.

    Flow:
      1. SmartKeyManager picks best provider + key (free first)
      2. Calls that provider's API
      3. On rate-limit/quota error -> cooldown + switch provider
      4. Tries up to MAX_RETRIES providers before giving up
      5. Records token usage for daily budget tracking
    """
    # Default to full v14 master prompt
    if system is None:
        system = SEADS_V14_SYSTEM_PROMPT

    # Hard cap -- never exceed per-call limit
    effective_tokens = min(max_tokens, MAX_TOKENS_PER_REQUEST)
    last_error = None

    for attempt in range(MAX_RETRIES):
        provider = "system"
        api_key = None
        try:
            provider, api_key, auto_model = smart_key_manager.get_best_key(
                task_type=task_type,
                max_tokens=effective_tokens,
            )
            use_model = model if model else auto_model

            try:
                print(f"    [KEY] [{provider}] {use_model[:35]} | max={effective_tokens} | attempt {attempt+1}/{MAX_RETRIES}")
            except UnicodeEncodeError:
                pass

            start = time.time()

            # -- Call the right provider ----------------------
            if provider == "groq":
                result = _call_groq(api_key, use_model, prompt,
                                    system, effective_tokens, temperature)

            elif provider == "cerebras":
                result = _call_cerebras(api_key, use_model, prompt,
                                        system, effective_tokens, temperature)

            elif provider == "together":
                result = _call_together(api_key, use_model, prompt,
                                        system, effective_tokens, temperature)

            elif provider == "gemini":
                result = _call_gemini(api_key, use_model, prompt,
                                      effective_tokens, temperature, system)

            elif provider == "openrouter":
                result = _call_openrouter(api_key, use_model, prompt,
                                          system, effective_tokens, temperature)
            else:
                continue

            # -- Record usage ---------------------------------
            elapsed = round(time.time() - start, 2)
            # Estimate tokens from word count (words x 1.3)
            token_est = int(len(result.split()) * 1.3)
            smart_key_manager.record_usage(provider, token_est)

            try:
                print(f"    [OK] {elapsed}s | ~{token_est} tokens | [{provider}]")
            except UnicodeEncodeError:
                pass
            return result

        except Exception as e:
            err = str(e).lower()
            last_error = e

            # If get_best_key raised an exception (no keys available)
            if api_key is None:
                try:
                    print(f"    [FAIL] System Error: {e} -> aborting retries")
                except UnicodeEncodeError:
                    pass
                break

            # Rate limit (429) -> cooldown, try next key/provider
            if "rate limit" in err or "429" in err:
                # TPD (daily) exhaustion needs longer cooldown than RPM
                if "tokens per day" in err or "tpd" in err:
                    smart_key_manager.mark_rate_limited(provider, api_key, 1800)  # 30min
                    try:
                        print(f"    [TPD] [{provider}] Daily limit exhausted -> 30min cooldown")
                    except UnicodeEncodeError:
                        pass
                else:
                    smart_key_manager.mark_rate_limited(provider, api_key, 65)
                    try:
                        print(f"    [RATE] [{provider}] Rate limited -> switching (attempt {attempt+1})")
                    except UnicodeEncodeError:
                        pass
                continue

            # Daily quota / payment required / context too long -> longer cooldown
            elif "quota" in err or "exceeded" in err or "context" in err or "402" in err or "payment required" in err:
                smart_key_manager.mark_rate_limited(provider, api_key, 3600)
                try:
                    print(f"    [QUOTA] [{provider}] Quota/context error -> switching provider")
                except UnicodeEncodeError:
                    pass
                continue

            # 400 / 404 / 500 / model not found -> temporary cooldown, skip to next
            elif "400" in err or "404" in err or "not found" in err or "500" in err or "502" in err or "503" in err or "bad request" in err:
                smart_key_manager.mark_rate_limited(provider, api_key, 5)
                try:
                    print(f"    [SKIP] [{provider}] {err[:60]} -> temporary skip, next provider")
                except UnicodeEncodeError:
                    pass
                continue

            # Auth / invalid key -> disable for 24h
            elif "401" in err or "auth" in err or "invalid" in err or "unauthorized" in err:
                smart_key_manager.mark_rate_limited(provider, api_key, 86400)
                try:
                    print(f"    [AUTH] [{provider}] Auth error -- disabling key")
                except UnicodeEncodeError:
                    pass
                continue

            # Any other error -> 1s pause then retry
            else:
                try:
                    print(f"    [ERR] [{provider}] Error: {str(e)[:100]} -> retrying...")
                except UnicodeEncodeError:
                    pass
                time.sleep(1)
                continue

    try:
        print(f"[FAIL] All {MAX_RETRIES} providers failed. Last: {last_error}")
    except UnicodeEncodeError:
        pass
    return ""


# -----------------------------------------------------------------
# Provider-specific API callers
# -----------------------------------------------------------------

def _call_groq(key, model, prompt, system, max_tokens, temperature):
    """Groq -- fastest free provider, high output token cap"""
    client = Groq(api_key=key)
    r = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return r.choices[0].message.content


def _call_cerebras(key, model, prompt, system, max_tokens, temperature):
    """Cerebras -- 900 tokens/sec, 1M tokens/day free per key"""
    r = requests.post(
        "https://api.cerebras.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
        },
        json={
            "model":       model,
            "max_tokens":  min(max_tokens, 8192),
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
        },
        timeout=180,  # Longer timeout for larger outputs
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_together(key, model, prompt, system, max_tokens, temperature):
    """Together.ai -- good Llama models, free credits"""
    r = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
        },
        json={
            "model":       model,
            "max_tokens":  min(max_tokens, 8192),
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_gemini(key, model, prompt, max_tokens, temperature, system=None):
    """Google Gemini -- generous free tier, with system prompt support"""
    # Build contents: inject system as first user message if provided
    contents = []
    if system:
        contents.append({"role": "user", "parts": [{"text": f"SYSTEM INSTRUCTIONS:\n{system}\n\nUSER REQUEST:\n{prompt}"}]})
    else:
        contents.append({"role": "user", "parts": [{"text": prompt}]})

    r = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        json={
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens, # Gemini supports 30k+ output
                "temperature":     temperature,
            },
        },
        timeout=300, # Large output takes time
    )
    r.raise_for_status()
    data = r.json()
    # Handle safety blocks or empty responses
    candidates = data.get("candidates", [])
    if not candidates:
        finish = data.get("promptFeedback", {}).get("blockReason", "UNKNOWN")
        raise Exception(f"Gemini no candidates (blockReason={finish}): {str(data)[:200]}")
    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        raise Exception(f"Gemini empty parts in response")
    return parts[0]["text"]


def _call_openrouter(key, model, prompt, system, max_tokens, temperature):
    """OpenRouter -- paid fallback ($3 budget)"""
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://seads.app",
            "X-Title":       "S.E.A.D.S. Builder",
        },
        json={
            "model":       model,
            "max_tokens":  min(max_tokens, 8000),
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
        },
        timeout=90,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


# -- Backwards-compatibility shim ----------------------------
def get_llm(model_name: str = "llama-3.3-70b-versatile", temperature: float = 0.3):
    """Legacy helper -- returns None; use get_llm_response() instead."""
    return None