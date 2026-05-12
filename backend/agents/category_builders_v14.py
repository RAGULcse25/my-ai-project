# agents/category_builders_v14.py — S.E.A.D.S. v14 IIT-Level Enterprise Multi-Agent Builders
# ============================================================
# 7 Core Categories: Website, Mobile, Design, PPT, Game, ML, E-Commerce
# + More (catch-all)
# Pipeline: Search → Plan → Code(2X) → Verify(2X) → Preview
# Tech stacks enforced per user specification
# ============================================================

import os, json, time, re, logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("CategoryBuilders")
OUTPUT_DIR = Path(os.getenv("ONLINE_APP_DIR", r"E:\seads\online_app"))

# ─────────────────────────────────────────────────────────────
# IIT-LEVEL UI/UX STANDARD INJECTED INTO EVERY CODE PROMPT
# ─────────────────────────────────────────────────────────────
IIT_UI_STANDARD = """
╔══════════════════════════════════════════════════════════════╗
║           IIT-LEVEL DESIGN & ENGINEERING MANDATE            ║
╚══════════════════════════════════════════════════════════════╝

DESIGN SYSTEM (Non-negotiable):
  • Color: EXTREMELY COLORFUL AND VIBRANT. Deep space dark (#070B14 base) with highly vibrant accent gradients
    (e.g., #6C63FF → #FF6B9D → #4ECDE6). NEVER plain grey/white. The design must be colorful.
  • Typography: Google Fonts (Inter + Outfit or Poppins). Font hierarchy:
    hero=4rem, h2=2.5rem, body=1rem, code=0.9rem.
  • Glassmorphism: backdrop-filter:blur(20px); background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.12); border-radius:16px.
  • Gradients: Use CSS linear/radial gradients on backgrounds, buttons, text-clips thoroughly.
  • Shadows: box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.08).
  • Icons: Use Lucide via CDN (https://unpkg.com/lucide@latest/dist/umd/lucide.min.js).

ANIMATION MANDATE (minimum 5 types - EVERY PROCESS MUST BE ANIMATED):
  • Page load: Staggered fade-up for sections (opacity 0→1, translateY 30px→0).
  • Hover: Scale (1.02-1.05), glow box-shadow, color shift with transition:all 0.3s ease.
  • Scroll: IntersectionObserver for reveal animations on scroll.
  • Micro-interactions: Button press scale(0.96), ripple effect on click for EACH interaction.
  • Loading: Skeleton shimmer animation for async states. EVERY process/action must have visual animated feedback.

LAYOUT RULES:
  • Mobile-first CSS Grid/Flexbox. Breakpoints: 480px, 768px, 1024px, 1440px.
  • Max-width container: 1280px, centered with auto margins.
  • Generous spacing: padding 24px→48px→96px across breakpoints.
  • STICKY NAVBAR: Must be a sticky glassmorphism navbar (position: sticky; top: 0; z-index: 50;) with blur + logo + nav links.

QUALITY RULES:
  • ZERO alert()/confirm()/prompt() — always toast notifications.
  • ZERO broken images — use https://picsum.photos/seed/{N}/800/600.
  • ZERO lorem ipsum — generate domain-realistic content.
  • ZERO placeholder comments like "// add code here".
  • ZERO incomplete functions — every feature fully implemented.
  • STRICT LOGIC & ROLES: If building a game or complex app (like Chess/Ludo), strictly enforce legal rules, turn-taking, multiple roles, and win/loss states flawlessly.
  • UX EXCELLENCE: Apply animations not just to buttons, but to game pieces, data visualizations, and state transitions. No sudden teleports or unstyled elements.
  • Keyboard accessible (tabIndex, aria-labels, focus styles).
  • LocalStorage persistence where applicable.
  • Error states, empty states, loading states — all implemented.
"""

IIT_CODE_PREFIX = """ULTRA-DETAILED GENERATION — IIT FINAL YEAR PROJECT LEVEL:
Write COMPLETE, MASSIVE, PRODUCTION-READY code. Implement EVERY feature fully.
Apply the IIT Design Standard (glassmorphism, animations, micro-interactions).
AIM: Code quality that would pass IIT Bombay's CS Department review.
ZERO PLACEHOLDERS. ZERO TRUNCATION. EVERY FUNCTION COMPLETE.\n\n"""


# -----------------------------------------------------------------
# CORE LLM WRAPPER
# -----------------------------------------------------------------
def llm(prompt, agent_name="Agent", task_type="code", progress=None, task_id=None, tokens=8000):
    """Call LLM with progress tracking. Respects MAX_TOKENS_PER_REQUEST cap in llm_config."""
    from core.llm_config import get_llm_response, SEADS_V14_SYSTEM_PROMPT
    if progress is not None and task_id:
        progress_update(task_id, progress, f"[{agent_name}] working...")

    api_keys = {
        "YOUTUBE":     os.getenv("YOUTUBE_API_KEY"),
        "UNSPLASH":    os.getenv("UNSPLASH_API_KEY"),
        "NEWS":        os.getenv("NEWS_API_KEY"),
        "OPENWEATHER": os.getenv("WEATHER_API_KEY"),
        "PEXELS":      os.getenv("PEXELS_API_KEY"),
    }
    keys_str = "\n".join([f"- {k}: {v}" for k, v in api_keys.items() if v])
    env_context = f"\nAVAILABLE API KEYS (use these in code):\n{keys_str}" if keys_str else ""

    if task_type == "code":
        prompt = IIT_CODE_PREFIX + IIT_UI_STANDARD + "\n\n" + prompt

    result = get_llm_response(
        prompt=prompt,
        max_tokens=tokens,
        temperature=0.1,
        system=SEADS_V14_SYSTEM_PROMPT + env_context,
        task_type=task_type,
    )
    return result or ""


def parallel_llm(tasks):
    """Run multiple LLM calls simultaneously."""
    import concurrent.futures
    from core.llm_config import get_llm_response, SEADS_V14_SYSTEM_PROMPT

    api_keys = {
        "YOUTUBE":     os.getenv("YOUTUBE_API_KEY"),
        "UNSPLASH":    os.getenv("UNSPLASH_API_KEY"),
        "NEWS":        os.getenv("NEWS_API_KEY"),
        "OPENWEATHER": os.getenv("WEATHER_API_KEY"),
        "PEXELS":      os.getenv("PEXELS_API_KEY"),
    }
    keys_str = "\n".join([f"- {k}: {v}" for k, v in api_keys.items() if v])
    env_context = f"\nAVAILABLE API KEYS:\n{keys_str}" if keys_str else ""
    system = SEADS_V14_SYSTEM_PROMPT + env_context

    def _call_one(task):
        p = task["prompt"]
        if task.get("task_type") == "code":
            p = IIT_CODE_PREFIX + IIT_UI_STANDARD + "\n\n" + p
        return get_llm_response(
            prompt=p,
            max_tokens=task.get("tokens", 8000),
            temperature=0.1,
            system=system,
            task_type=task.get("task_type", "code"),
        ) or ""

    results = [None] * len(tasks)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as ex:
        futs = {ex.submit(_call_one, t): i for i, t in enumerate(tasks)}
        for fut in concurrent.futures.as_completed(futs):
            idx = futs[fut]
            try:
                results[idx] = fut.result()
            except Exception as e:
                log.error(f"parallel_llm task {idx} failed: {e}")
                results[idx] = ""
    return results


# -----------------------------------------------------------------
# UTILITY FUNCTIONS
# -----------------------------------------------------------------
def progress_update(task_id, percent, status):
    if task_id:
        try:
            from core.shared import PROGRESS_DATA
            PROGRESS_DATA[task_id] = {"percent": percent, "status": status}
        except Exception:
            pass


def strip(raw):
    if not raw:
        return ""
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", raw)
    if match:
        return match.group(1).strip()
    cleaned = re.sub(r"```[\w]*\n?", "", raw).replace("```", "").strip()
    return cleaned


def parse_multi_files(raw):
    """Parse === FILE: path === ... === END === format, with fallbacks."""
    if not raw:
        return {}
    files = {}
    pattern = r"===\s*FILE:\s*(.*?)\s*===\s*([\s\S]*?)(?===\s*FILE:|===\s*END|$)"
    for m in re.finditer(pattern, raw):
        fname = m.group(1).strip()
        content = m.group(2).strip()
        if fname and content:
            files[fname] = content

    if not files:
        blocks = re.findall(r"```(?:\w+)?\n([\s\S]*?)```", raw)
        for i, block in enumerate(blocks):
            b = block.strip()
            if not b:
                continue
            if "<!DOCTYPE" in b or "<html" in b.lower():
                name = "index.html"
            elif b.startswith("import ") or "def " in b or "class " in b:
                name = f"main.py" if i == 0 else f"module_{i}.py"
            elif "{" in b and "\"name\"" in b:
                name = "package.json"
            else:
                name = f"file_{i}.txt"
            files[name] = b

    if not files and ("<!DOCTYPE html>" in raw or "<html" in raw.lower()):
        files["index.html"] = strip(raw)

    return files


def save_files(slug, files):
    project_dir = OUTPUT_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for fname, content in files.items():
        if not content:
            continue
        fpath = project_dir / Path(fname)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8", errors="replace")
        paths[fname] = str(fpath)
    return paths


def quality_fix(html):
    """Remove alert/confirm/prompt, fix broken local images."""
    if not html:
        return html
    html = re.sub(r'alert\s*\([^)]*\)\s*;?', 'console.log("toast")', html)
    html = re.sub(r'confirm\s*\([^)]*\)', 'true', html)
    html = re.sub(r'prompt\s*\([^)]*\)', '"user-input"', html)
    html = re.sub(
        r'<img([^>]*?)src=["\'](?!http|data:)["\']["\']',
        lambda m: f'<img{m.group(1)}src="https://picsum.photos/seed/{abs(hash(m.group(0)))%9999}/800/600"',
        html
    )
    return html


def build_result(slug, files, preview_html, idea=""):
    preview_html = quality_fix(preview_html or "")
    file_objs = [{"name": k, "content": v, "size": len(v)} for k, v in files.items()]
    return {
        "preview_html": preview_html,
        "files": file_objs,
        "slug": slug,
        "file_count": len(files),
        "total_size": sum(len(v) for v in files.values()),
    }


def make_slug(idea):
    return re.sub(r'[^a-z0-9-]', '', idea.replace(" ", "-").lower())[:35]


def generate_preview(idea, context_code, task_id, category="more"):
    """Generate standalone interactive HTML preview using Lovable Preview Engine."""
    from agents.preview_agent import run_preview_agent
    progress_update(task_id, 92, "Lovable Preview Agent: Generating interactive preview...")
    html = run_preview_agent(idea, category, context_code)
    return html


# ═══════════════════════════════════════════════════════════
# 1. WEBSITE BUILDER
#    Stack: React + Tailwind CSS + Shadcn UI (via CDN)
#    Pipeline: Perplexity Search → DeepSeek-R1 Plan → DeepSeek V3 Code → Claude Opus Verify
# ═══════════════════════════════════════════════════════════
def build_website(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    theme = answers.get("q3", "Glassmorphism")
    style = answers.get("q4", "Modern dark")
    features = answers.get("q2", "Contact form, Gallery, Testimonials")

    lower_idea = idea.lower()
    website_map = {
        "portfolio": "portfolio.html",
        "startup": "startup.html",
        "saas": "startup.html",
        "restaurant": "restaurant.html",
        "blog": "blog.html",
        "corporate": "corporate.html",
        "agency": "agency.html",
        "creative": "agency.html",
        "ngo": "ngo.html",
        "charity": "ngo.html",
        "product": "product.html"
    }

    for key, filename in website_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. Template for {key.title()}...")
            website_path = Path(r"E:\seads\backend\agents\websites") / filename
            if website_path.exists():
                final_html = website_path.read_text(encoding="utf-8")
                files = {"index.html": final_html}
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, final_html, idea)

    # ── Step 1: Parallel Search + Architecture + UX ─────────
    progress_update(task_id, 8, "🔍 [Search Agent] Perplexity deep search — how this website is built...")
    res, plan, ux = parallel_llm([
        {
            "prompt": f"""Deep research: How to build a production-quality {idea} website.
Search for: UI/UX patterns for this type of site, best React component patterns,
Tailwind CSS utilities, Shadcn UI components to use, real-world examples to study,
color palettes for {theme} theme, animation patterns, SEO best practices.
Return a detailed research report with specific technical recommendations.""",
            "task_type": "search", "tokens": 6000
        },
        {
            "prompt": f"""Architecture plan for {idea} website:
MANDATORY STACK: React 18 (via CDN/Babel), Tailwind CSS (CDN), Shadcn UI patterns.
Theme: {theme} | Style: {style} | Features: {features}

Create detailed plan with:
1. Complete component hierarchy (minimum 9 sections: Hero, Features, About, Services,
   Portfolio/Gallery, Testimonials, Team, Pricing, Contact, Footer)
2. State management approach (React hooks)
3. Animation plan (IntersectionObserver for scroll reveals, CSS keyframes, hover effects)
4. Mobile responsive breakpoints
5. Color system and typography scale
6. Data model for all content
Return a structured implementation plan.""",
            "task_type": "smart", "tokens": 6000
        },
        {
            "prompt": f"""UX Design research for {idea} website:
Micro-interactions: button hover effects, scroll animations, parallax, loading states.
Color psychology for {theme} theme. Accessibility requirements.
Mobile-first design considerations. Typography pairing recommendations.
Animation library patterns (CSS keyframes, IntersectionObserver, Framer Motion-style).
Return specific CSS/JS code snippets for each pattern.""",
            "task_type": "search", "tokens": 4000
        }
    ])

    # ── Step 2: Coding Agent — Full implementation ──────────
    progress_update(task_id, 35, "💻 [Coding Agent] Building complete website with React + Tailwind + Shadcn...")
    code = llm(
        f"""Build a COMPLETE, IIT-level {idea} website as a SINGLE SELF-CONTAINED HTML file.

MANDATORY TECH STACK:
- React 18 via CDN: <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
- ReactDOM via CDN: <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
- Babel standalone: <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
- Tailwind CSS via CDN: <script src="https://cdn.tailwindcss.com"></script>
- Lucide Icons via CDN: <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

Research context: {res[:1500]}
Architecture plan: {plan[:2000]}
UX patterns: {ux[:1000]}
Theme: {theme} | Style: {style} | Features: {features}

IMPLEMENT ALL 9+ SECTIONS:
1. Sticky glassmorphism navbar with mobile hamburger menu
2. Hero section with gradient text, CTA buttons, background animation
3. Features/Services section with icon cards and hover effects
4. About section with staggered text + image reveal
5. Portfolio/Gallery with lightbox and filter tabs
6. Testimonials carousel with auto-scroll
7. Team section with social links
8. Pricing/Plans section with hover-highlight
9. Contact form with validation + toast notifications
10. Footer with multi-column links, newsletter, social icons

CONTENT: Generate REALISTIC domain-specific content for {idea}.
NO lorem ipsum. Real product names, realistic testimonials with names, real stats.
All images: https://picsum.photos/seed/UNIQUE_NUMBER/800/600

Return ONLY complete <!DOCTYPE html>:""",
        "Coding Agent", "code", 45, task_id, tokens=8000
    )

    # ── Step 3: Verify Agent — Quality audit ────────────────
    progress_update(task_id, 78, "✨ [Verify Agent] IIT-level audit — fixing all issues...")
    verified = llm(
        f"""Elite Code Review for {idea} website. Enforce IIT-level standards:

CHECKLIST:
✓ All 9+ sections present and fully implemented (no stubs)
✓ React components properly structured with no syntax errors
✓ All CDN scripts (React, Tailwind, Babel, Lucide) correctly loaded
✓ All animations work (IntersectionObserver, CSS keyframes)
✓ Mobile hamburger menu opens/closes correctly
✓ Contact form validates inputs and shows toast on submit
✓ No alert()/confirm() — only toast notifications
✓ All images use picsum.photos or unsplash URLs (no broken src)
✓ Tailwind utility classes used correctly
✓ Responsive at all breakpoints (mobile, tablet, desktop)
✓ Color scheme consistent with {theme} theme
✓ All interactive elements have hover/focus states

CODE:
{code[:6000]}

Fix ALL issues. Return COMPLETE corrected <!DOCTYPE html>:""",
        "Verify Agent", "verify", 82, task_id, tokens=8000
    )

    files_raw = parse_multi_files(verified) or parse_multi_files(code)
    final_html = strip(verified) or strip(code)
    if not files_raw:
        files_raw = {"index.html": final_html}
    save_files(slug, files_raw)

    preview = quality_fix(final_html or files_raw.get("index.html", ""))
    if not preview or len(preview) < 500:
        preview = generate_preview(idea, verified or code, task_id, "website")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files_raw, preview, idea)


# ═══════════════════════════════════════════════════════════
# 2. MOBILE APP BUILDER
#    Stack: Python Kivy / BeeWare
#    Lifecycle: Choose Framework → Setup → Develop → Package → Compile → Test → Preview
#    Preview: Interactive HTML simulation of the mobile app
# ═══════════════════════════════════════════════════════════
def build_mobile_app(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    framework = answers.get("q1", "Kivy")

    lower_idea = idea.lower()
    mobile_map = {
        "calculator": "calculator",
        "guessing": "guessing",
        "grade": "grade",
        "expense": "expense",
        "todo": "todo",
        "health": "health",
        "bmi": "health",
        "quiz": "quiz",
        "planner": "planner"
    }

    for key, prefix in mobile_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. Mobile App for {key.title()}...")
            app_dir = Path(r"E:\seads\backend\agents\mobile")
            py_path = app_dir / f"{prefix}.py"
            html_path = app_dir / f"{prefix}.html"
            
            if py_path.exists() and html_path.exists():
                files = {"main.py": py_path.read_text(encoding="utf-8")}
                preview_html = html_path.read_text(encoding="utf-8")
                
                enc = preview_html.replace('"', "&quot;").replace("'", "&#39;")
                final_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{idea} — Mobile Preview</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{display:flex;align-items:center;justify-content:center;min-height:100vh;background:#0f172a;overflow:hidden}}
  .phone-frame{{position:relative;width:375px;height:812px;background:#000;border-radius:40px;box-shadow:inset 0 0 0 12px #1e293b,0 25px 50px -12px rgba(0,0,0,0.5);overflow:hidden}}
  .notch{{position:absolute;top:0;left:50%;transform:translateX(-50%);width:150px;height:30px;background:#1e293b;border-bottom-left-radius:20px;border-bottom-right-radius:20px;z-index:999}}
  iframe{{width:100%;height:100%;border:none;border-radius:28px}}
</style>
</head>
<body>
  <div class="phone-frame">
    <div class="notch"></div>
    <iframe srcdoc="{enc}"></iframe>
  </div>
</body>
</html>"""
                
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, final_preview, idea)

    # ── Search + Plan in parallel ───────────────────────────
    progress_update(task_id, 8, "🔍 [Search Agent] Researching Python mobile app patterns...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research how to build a Python mobile app: {idea}
Framework choice: {framework}

LIFECYCLE TO FOLLOW:
1. Choose Framework: BeeWare for native look, Kivy for custom/OpenGL
2. Setup: venv, install briefcase (BeeWare) or buildozer (Kivy)
3. Develop: main.py for logic, .kv file for UI layout (Kivy)
4. Package: Briefcase for BeeWare, Buildozer for Kivy
5. Compile: .apk/.aab for Android, .ipa for iOS
6. Test on emulator/simulator
7. Live preview

Research: Best UI patterns for this type of mobile app,
widget hierarchies, data persistence with SQLite, animations in {framework}.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan a complete Python {framework} mobile app for: {idea}

Define:
- Screen hierarchy (list all screens with their widgets)
- Navigation flow between screens
- Data model (SQLite tables or in-memory structures)
- Widget tree for each screen
- Event handlers and callbacks
- File structure: main.py, screens/, models/, utils/
- If Kivy: .kv layout files for each screen
- If BeeWare: Toga widget hierarchy
- How to create the interactive preview simulation""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    # ── Coding Agent ────────────────────────────────────────
    progress_update(task_id, 38, f"💻 [Coding Agent] Building Python {framework} mobile app...")
    code = llm(
        f"""Build a COMPLETE Python mobile app using {framework} for: {idea}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT FORMAT: Generate multiple files using this format:
=== FILE: main.py ===
(complete Python code)
=== FILE: app.kv ===  (if Kivy)
(complete KV layout)
=== FILE: requirements.txt ===
(dependencies)
=== END ===

REQUIREMENTS:
- Complete main.py with all app logic
- If Kivy: separate .kv file for UI layout
- If BeeWare: Toga widgets defined in main.py
- SQLite database for data persistence
- Proper screen management and navigation
- Input validation on all forms
- Beautiful UI with custom colors and spacing
- All features fully functional, no stubs""",
        "Coding Agent", "code", 50, task_id, tokens=8000
    )

    # ── Verify ──────────────────────────────────────────────
    progress_update(task_id, 72, "✨ [Verify Agent] Checking Python app quality...")
    verified = llm(
        f"""Verify this Python {framework} mobile app for {idea}:

CHECKLIST:
✓ main.py runs without import errors
✓ All screens defined and navigable
✓ Database operations (CRUD) work correctly
✓ Input validation present on all forms
✓ No placeholder functions — everything implemented
✓ .kv file properly structured (if Kivy)
✓ requirements.txt includes all dependencies

CODE:
{code[:5000]}

Fix ALL issues. Return corrected files in === FILE: === format:""",
        "Verify Agent", "verify", 78, task_id, tokens=8000
    )

    files = parse_multi_files(verified) or parse_multi_files(code)
    if not files:
        files = {"main.py": strip(verified) or strip(code)}
    save_files(slug, files)

    # ── Generate interactive preview simulation ─────────────
    progress_update(task_id, 88, "📱 [Preview] Generating interactive mobile simulation...")
    preview_html = generate_preview(idea, verified or code, task_id, "mobile")

    # Wrap in phone frame
    if preview_html and len(preview_html) > 200:
        enc = preview_html.replace('"', "&quot;").replace("'", "&#39;")
        final_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{idea} — Mobile Preview</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{background:linear-gradient(135deg,#070B14 0%,#0D1421 100%);
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    min-height:100vh;font-family:'Inter',sans-serif;padding:20px}}
  .label{{color:#8b5cf6;font-size:11px;letter-spacing:2px;text-transform:uppercase;
    margin-bottom:16px;font-weight:600}}
  .phone-wrap{{width:375px;height:812px;
    border:12px solid rgba(255,255,255,0.08);border-radius:50px;overflow:hidden;
    position:relative;box-shadow:0 0 0 1px rgba(255,255,255,0.05),
    0 40px 80px rgba(0,0,0,0.7),0 0 60px rgba(139,92,246,0.15)}}
  .phone-wrap iframe{{width:100%;height:100%;border:none}}
  .badge{{margin-top:14px;color:#4b5563;font-size:9px;font-family:monospace}}
</style>
</head>
<body>
  <div class="label">📱 {idea} — Live Mobile Preview</div>
  <div class="phone-wrap">
    <iframe srcdoc="{enc}" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe>
  </div>
  <div class="badge">S.E.A.D.S. v14 · Python {framework} · Interactive Simulation</div>
</body>
</html>"""
    else:
        final_preview = preview_html

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, final_preview or preview_html, idea)


# ═══════════════════════════════════════════════════════════
# 3. DESIGN TOOL BUILDER
#    Libraries: OpenCV, Pillow, scikit-image, Albumentations, SimpleCV
#    Preview: Interactive browser-based design tool simulation
# ═══════════════════════════════════════════════════════════
def build_design_tool(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    features = answers.get("q1", "Photo filters, Crop, Text overlay")
    use_case = answers.get("q2", "Photo editor")

    lower_idea = idea.lower()
    design_map = {
        "photo": "photo",
        "bg remover": "bg",
        "background": "bg",
        "banner": "banner",
        "logo": "logo",
        "thumbnail": "thumbnail",
        "palette": "palette",
        "text effect": "text",
        "canva": "canva"
    }

    for key, prefix in design_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. Design Tool for {key.title()}...")
            app_dir = Path(r"E:\seads\backend\agents\design")
            py_path = app_dir / f"{prefix}.py"
            html_path = app_dir / f"{prefix}.html"
            
            if py_path.exists() and html_path.exists():
                files = {"main.py": py_path.read_text(encoding="utf-8")}
                preview_html = html_path.read_text(encoding="utf-8")
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, preview_html, idea)

    progress_update(task_id, 8, "🔍 [Search Agent] Researching image processing libraries...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research how to build: {idea}

LIBRARIES TO CONSIDER (pick best for the task):
- OpenCV: Real-time & AI, industry standard, extremely fast, 2500+ algorithms
- Pillow: Basic editing — resizing, cropping, text overlay
- scikit-image: Scientific tasks — filtering, segmentation
- Albumentations: ML augmentation pipelines
- SimpleCV: Rapid prototyping, beginner-friendly

For a browser preview: use HTML5 Canvas API, Fabric.js, or Konva.js
to simulate the tool interactions.

Research UI patterns for design tools like Figma, Canva, Photopea.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan a complete design tool: {idea}
Features: {features} | Use case: {use_case}

Define:
- Canvas/workspace layout (toolbar, canvas, layers panel, properties)
- Tool hierarchy (select, draw, text, shapes, filters)
- Layer system design
- Undo/redo stack
- Export functionality (PNG, JPG)
- File structure: main.py (backend), index.html (frontend)
- Python backend: which library for each feature
- Interactive HTML preview with Canvas API""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    progress_update(task_id, 38, "💻 [Coding Agent] Building design tool...")
    code = llm(
        f"""Build a COMPLETE design tool for: {idea}
Features: {features} | Use case: {use_case}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT: Generate multiple files:
=== FILE: main.py ===
(Python backend using OpenCV/Pillow for image processing)
=== FILE: index.html ===
(Interactive frontend with Canvas API, toolbars, layers)
=== FILE: requirements.txt ===
(opencv-python, Pillow, scikit-image, flask)
=== END ===

The index.html MUST be a fully working design tool with:
- Canvas workspace with zoom/pan
- Toolbar with drawing tools, shapes, text
- Filter panel (blur, sharpen, contrast, brightness)
- Layer system
- Color picker
- Export button
- Dark theme matching IIT standards""",
        "Coding Agent", "code", 50, task_id, tokens=8000
    )

    progress_update(task_id, 78, "✨ [Verify Agent] Verifying design tool...")
    verified = llm(
        f"""Verify this design tool for {idea}:
✓ Canvas renders and accepts mouse events
✓ All tools work (draw, shapes, text, select)
✓ Filters apply correctly
✓ Export functionality works
✓ No errors in console
✓ Dark themed UI

CODE:
{code[:5000]}

Fix ALL issues. Return corrected files in === FILE: === format:""",
        "Verify Agent", "verify", 84, task_id, tokens=8000
    )

    files = parse_multi_files(verified) or parse_multi_files(code)
    if not files:
        files = {"index.html": strip(verified) or strip(code)}
    save_files(slug, files)

    preview = quality_fix(files.get("index.html", "") or strip(verified) or strip(code))
    if not preview or len(preview) < 500:
        preview = generate_preview(idea, verified or code, task_id, "design")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, preview, idea)


# ═══════════════════════════════════════════════════════════
# 4. SLIDES / PPT BUILDER
#    Tools: python-pptx, Marp (Markdown), Reveal.js, Manim
#    Preview: Reveal.js interactive HTML slideshow
# ═══════════════════════════════════════════════════════════
def build_ppt(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    ppt_type = answers.get("q1", "Business pitch")
    slides_count = answers.get("q2", "10 slides")
    style = answers.get("q3", "Dark professional")

    progress_update(task_id, 8, "🔍 [Search Agent] Researching presentation tools...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research how to create beautiful presentations for: {idea}

TOOLS:
- python-pptx: Industry standard. Create/read/edit .pptx files. Automate text, images, charts.
- Marp (Markdown): Convert Markdown to beautiful PDF/HTML slides.
- Reveal.js (with RISE): Interactive slideshow from code. Live code cells.
- Manim: By 3Blue1Brown. Best for animated educational presentations.

For browser preview: Use Reveal.js to create interactive HTML slides.

Research best slide layouts, color schemes for {style}, content structure for {ppt_type}.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan a {slides_count} presentation for: {idea}
Type: {ppt_type} | Style: {style}

Create:
1. Slide-by-slide content outline
2. Visual design system (colors, fonts, spacing)
3. Which slides need charts/diagrams
4. Animation/transition plan
5. Speaker notes for each slide
6. File structure: slides.html (Reveal.js preview) + generate_pptx.py (python-pptx backend)""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    progress_update(task_id, 38, "💻 [Coding Agent] Creating presentation...")
    code = llm(
        f"""Create a COMPLETE, beautiful presentation for: {idea}
Type: {ppt_type} | Slides: {slides_count} | Style: {style}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT AS SINGLE HTML FILE using Reveal.js:
- Include Reveal.js CDN: <link rel="stylesheet" href="https://unpkg.com/reveal.js@4/dist/reveal.css">
- Include theme: <link rel="stylesheet" href="https://unpkg.com/reveal.js@4/dist/theme/black.css">
- Include script: <script src="https://unpkg.com/reveal.js@4/dist/reveal.js"></script>

EACH SLIDE must have:
- Stunning visual design matching {style}
- Custom CSS (not just default Reveal.js theme)
- Background gradients and glassmorphism
- Real content (no lorem ipsum) — domain-specific to {idea}
- Charts/diagrams where appropriate (use inline SVG)
- Progress bar
- Keyboard navigation (arrows, space)
- Slide counter

Return ONLY complete <!DOCTYPE html>:""",
        "Coding Agent", "code", 55, task_id, tokens=8000
    )

    progress_update(task_id, 80, "✨ [Verify Agent] Polishing presentation...")
    verified = llm(
        f"""Verify this Reveal.js presentation for {idea}:
✓ All {slides_count} slides present with real content
✓ Reveal.js CDN loaded correctly
✓ Custom CSS theme applied (not default plain)
✓ Keyboard navigation works
✓ Animations/transitions between slides
✓ Progress bar visible
✓ Mobile responsive
✓ No lorem ipsum anywhere

CODE:
{code[:5000]}

Fix ALL issues. Return complete <!DOCTYPE html>:""",
        "Verify Agent", "verify", 84, task_id, tokens=8000
    )

    final_html = strip(verified) or strip(code)
    files = {"index.html": final_html}
    save_files(slug, files)

    preview = quality_fix(final_html)
    if not preview or len(preview) < 500:
        preview = generate_preview(idea, verified or code, task_id, "ppt")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, preview, idea)


# ═══════════════════════════════════════════════════════════
# 5. GAME BUILDER (replaces dataviz)
#    Stack: JavaScript — Phaser (2D), Three.js (3D), PlayCanvas, Canvas API
#    Also: Lua (microStudio-style)
# ═══════════════════════════════════════════════════════════
def build_game(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)

    lower_idea = idea.lower()
    game_map = {
        "chess": "chess_game.html",
        "snake": "snake_game.html",
        "tetris": "tetris_game.html",
        "ludo": "ludo_game.html",
        "shooter": "shooter_game.html",
        "zombie": "shooter_game.html",
        "platform": "platformer_game.html",
        "puzzle": "puzzle_game.html",
        "invader": "space_invaders_game.html",
        "temple run": "temple_run_game.html",
        "endless": "temple_run_game.html",
        "runner": "temple_run_game.html"
    }

    for key, filename in game_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. Engine for {key.title()}...")
            game_path = Path(r"E:\seads\backend\agents\games") / filename
            if game_path.exists():
                final_html = game_path.read_text(encoding="utf-8")
                files = {"index.html": final_html}
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, final_html, idea)

    progress_update(task_id, 8, "🔍 [Search Agent] Researching game development patterns...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research how to build a browser game: {idea}

FRAMEWORKS (pick best for this game):
JavaScript (native browser):
- Phaser (2D): Most popular 2D web game framework. Sprites, physics, animations.
- PlayCanvas (3D): Industry-standard cloud 3D engine.
- Three.js (3D): Library for 3D scenes, WebGL rendering.
- Canvas API: Raw HTML5 canvas for simple 2D games.

Lua:
- microStudio: Browser-based, live coding, microScript language.

Research: game mechanics for this type of game, collision detection,
scoring systems, level progression, graphics patterns, sound effects.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan a complete browser game: {idea}

Define:
1. Game mechanics & STRICT RULES (e.g., if Chess/Ludo/Board Game: exact board logic, legal move validation, win/lose/draw conditions).
2. Entity system & Roles (Player 1 vs Player 2, AI opponents, pieces, items).
3. Board/Grid Architecture or Physics/collision approach (depending on game type).
4. Turn-based state management or Level progression.
5. IIT-Level UI elements (premium glassmorphism, score, lives, timer, pause menu, interactive game over screen).
6. Input handling (drag-and-drop, click-to-move, keyboard, touch).
7. Advanced Animation system (smooth piece movement, move highlighting, CSS/canvas transitions).
8. Audio feedback strategy (move sounds, win/lose sounds).
9. Framework choice with justification.
10. Robust State machine (menu → playing → paused → game over).""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    extra_rules = ""
    if "chess" in idea.lower():
        extra_rules = """
CRITICAL CHESS INSTRUCTION:
To guarantee perfect game rules, exact board, and exact piece movements (coins), you MUST use 'chess.js' via CDN for game logic:
<script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script>
Use it to validate moves, checkmate, and turns. Build the 8x8 board UI using DOM elements (CSS Grid) and map it perfectly to the chess.js state. Use Unicode chess pieces (♚♛♜♝♞♟). Ensure drag-and-drop or click-to-move works perfectly.
"""

    progress_update(task_id, 35, "💻 [Coding Agent] Building game engine...")
    code = llm(
        f"""Build a COMPLETE, FULLY PLAYABLE browser game: {idea}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT: Single self-contained HTML file.

REQUIREMENTS FOR ALL GAMES:
- For Board/Logic Games (Chess, Ludo, etc): YOU MUST IMPLEMENT EXACT STRICT DOMAIN RULES. Implement legal move validation, piece behaviors, turn-taking logic, exact board layout, capturing mechanics, and win/draw detection perfectly.
- High-Fidelity UI/UX: Implement a stunning, highly polished "IIT-Level" UI using DOM elements overlaid on the canvas, or beautifully drawn canvas elements (gradients, glassmorphism, drop shadows, rich colors).
- Roles & Multiplayer: Correctly handle Player 1 vs Player 2 turns, and if applicable, a basic AI opponent.
- Animations: Smoothly animate pieces moving from one state to another (do not instantly teleport pieces), highlight legal moves.
- If 2D/Action: Complete game loop, collision detection, physics.
- Include interactive Start Menu, Playing view, Pause Menu, and Game Over screen with Play Again button.
- Responsive design adjusting to screen sizes (Canvas API or Phaser).
- Visual effects (particles, screen shake, move highlighting).
- Sound effects using Web Audio API.
{extra_rules}

EVERY game interaction must work flawlessly. The UX must feel like a premium AAA browser game.

Return ONLY complete <!DOCTYPE html>:""",
        "Coding Agent", "code", 50, task_id, tokens=8000
    )

    progress_update(task_id, 80, "✨ [Verify Agent] Testing game playability...")
    verified = llm(
        f"""Verify this browser game for {idea}:

PLAYABILITY CHECKLIST:
✓ Game starts when user clicks Start/Play
✓ Player entity responds to keyboard/mouse input
✓ Collision detection works correctly
✓ Score increments properly
✓ Game over triggers correctly
✓ Restart works from game over screen
✓ No JavaScript errors that would crash the game
✓ Canvas renders at correct size
✓ Touch input works for mobile
✓ UI overlay (score/lives) is visible
✓ Audio feedback present (even simple beeps)
✓ Performance: 60 FPS with requestAnimationFrame

CODE:
{code[:5000]}

Fix ALL bugs. Return complete <!DOCTYPE html>:""",
        "Verify Agent", "verify", 86, task_id, tokens=8000
    )

    final_html = strip(verified) or strip(code)
    files = {"index.html": final_html}
    save_files(slug, files)

    preview = quality_fix(final_html)
    if not preview or len(preview) < 500:
        preview = generate_preview(idea, verified or code, task_id, "game")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, preview, idea)


# ═══════════════════════════════════════════════════════════
# 6. ML PROJECT BUILDER
#    Frameworks: Scikit-learn, PyTorch, TensorFlow, Hugging Face,
#                OpenCV, LangChain
#    Preview: Interactive prediction dashboard with simulated model
# ═══════════════════════════════════════════════════════════
def build_ml_project(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    ml_type = answers.get("q1", "Price/Value Prediction")

    lower_idea = idea.lower()
    ml_map = {
        "house": "house",
        "movie": "movie",
        "spam": "spam",
        "churn": "churn",
        "sentiment": "sentiment",
        "fraud": "fraud",
        "disease": "disease",
        "diabetes": "disease",
        "customer": "customer",
        "clustering": "customer",
        "segments": "customer"
    }

    for key, prefix in ml_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. ML Model for {key.title()}...")
            app_dir = Path(r"E:\seads\backend\agents\ml")
            py_path = app_dir / f"{prefix}.py"
            html_path = app_dir / f"{prefix}.html"
            
            if py_path.exists() and html_path.exists():
                files = {"main.py": py_path.read_text(encoding="utf-8")}
                preview_html = html_path.read_text(encoding="utf-8")
                
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, preview_html, idea)

    progress_update(task_id, 8, "🔍 [Search Agent] Researching ML frameworks and patterns...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research ML project: {idea}

FRAMEWORK SELECTION GUIDE:
- Scikit-learn: Best for tabular data, regression, clustering (traditional ML)
- PyTorch: Preferred for research, dynamic computation graphs
- TensorFlow: Built for scale, mobile/edge deployment with TF Lite
- Hugging Face Transformers: Pre-trained models for NLP/text
- OpenCV: Real-time image and video processing
- LangChain: Connecting LLMs to external data and APIs
- Keras: Quick prototyping without deep coding

HOW TO CHOOSE:
1. Tabular data → Scikit-learn
2. Images/video → OpenCV + PyTorch/TensorFlow
3. Text/NLP → Hugging Face Transformers
4. Mobile deployment → TensorFlow Lite
5. AI Agents → LangChain

Research: best model for this problem, data preprocessing steps,
feature engineering, evaluation metrics, visualization.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan complete ML project: {idea}
Type: {ml_type}

Define complete pipeline:
1. Problem Definition (classification/regression/clustering/NLP)
2. Data Collection (sources, format, sample data)
3. Data Preprocessing (cleaning, handling missing values, encoding)
4. Feature Engineering (feature selection, scaling, PCA)
5. Model Selection (which algorithm and why)
6. Training Pipeline (train/test split, cross-validation)
7. Evaluation (accuracy, precision, recall, confusion matrix)
8. Prediction UI (input form → model → result display)
9. Visualization (feature importance, learning curves, ROC)
10. File structure: main.py, model.py, data_loader.py, requirements.txt""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    progress_update(task_id, 35, "💻 [Coding Agent] Building ML pipeline + prediction UI...")
    code = llm(
        f"""Build a COMPLETE ML project: {idea}
Type: {ml_type}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT: Generate multiple files:
=== FILE: main.py ===
(Complete ML pipeline: load data → preprocess → train → evaluate → save model)
=== FILE: model.py ===
(Model definition, training, prediction functions)
=== FILE: data_loader.py ===
(Data loading, preprocessing, feature engineering)
=== FILE: requirements.txt ===
(scikit-learn, pandas, numpy, matplotlib, seaborn, flask)
=== END ===

REQUIREMENTS:
- Generate REALISTIC sample dataset (hardcoded in data_loader.py)
- Complete preprocessing pipeline
- Model training with evaluation metrics
- Print classification report / RMSE / R² score
- Feature importance visualization
- Prediction function that takes input and returns result
- All code runs without errors""",
        "Coding Agent", "code", 50, task_id, tokens=8000
    )

    progress_update(task_id, 72, "✨ [Verify Agent] Checking ML pipeline...")
    verified = llm(
        f"""Verify this ML project for {idea}:

CHECKLIST:
✓ Data loading works with sample data
✓ Preprocessing handles all edge cases
✓ Model trains without errors
✓ Evaluation metrics printed
✓ Prediction function works for new inputs
✓ No import errors
✓ requirements.txt complete

CODE:
{code[:5000]}

Fix ALL issues. Return corrected files in === FILE: === format:""",
        "Verify Agent", "verify", 80, task_id, tokens=8000
    )

    files = parse_multi_files(verified) or parse_multi_files(code)
    if not files:
        files = {"main.py": strip(verified) or strip(code)}
    save_files(slug, files)

    # ── Generate interactive prediction dashboard ───────────
    progress_update(task_id, 88, "📊 [Preview] Generating ML prediction dashboard...")
    preview_html = generate_preview(idea, verified or code, task_id, "ml")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, preview_html, idea)


# ═══════════════════════════════════════════════════════════
# 7. E-COMMERCE BUILDER
#    Step 1: Frontend (React + Tailwind CSS)
#    Step 2: Backend (Node.js + Express)
#    Step 3: Database (MongoDB)
#    Step 4: Authentication (JWT / NextAuth)
#    Step 5: Payment (Stripe / Razorpay API)
# ═══════════════════════════════════════════════════════════
def build_ecommerce(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)

    lower_idea = idea.lower()
    ecom_map = {
        "flipkart": "flipkart",
        "amazon": "amazon",
        "fashion": "fashion",
        "boutique": "fashion",
        "electronic": "electronics",
        "laptop": "electronics",
        "mobile": "electronics",
        "grocery": "grocery",
        "bigbasket": "grocery",
        "beauty": "beauty",
        "cosmetic": "beauty",
        "nykaa": "beauty",
        "book": "bookstore",
        "shoe": "shoes",
        "footwear": "shoes"
    }

    for key, prefix in ecom_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. E-Commerce for {key.title()}...")
            app_dir = Path(r"E:\seads\backend\agents\ecommerce")
            html_path = app_dir / f"{prefix}.html"
            
            if html_path.exists():
                files = {"index.html": html_path.read_text(encoding="utf-8")}
                preview_html = html_path.read_text(encoding="utf-8")
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, preview_html, idea)

    progress_update(task_id, 8, "🔍 [Search Agent] Researching e-commerce architecture...")
    res, plan = parallel_llm([
        {
            "prompt": f"""Research how to build a production e-commerce site: {idea}

TECHNICAL STACK:
Step 1: Frontend — React.js + Tailwind CSS
  - Product Gallery, Product Detail, Cart pages
  - Redux or Context API for cart state management
Step 2: Backend — Node.js + Express
  - REST APIs: GET products, POST orders, user auth
Step 3: Database — MongoDB
  - NoSQL for flexible product attributes
Step 4: Authentication — JWT or NextAuth
  - Secure login, protected routes, admin dashboard
Step 5: Payment — Stripe or Razorpay API
  - Never handle card data directly, use their secure APIs

Research: Product catalog design, cart persistence, checkout flow,
real product images for this type of store.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan complete e-commerce platform: {idea}

Architecture:
1. Frontend pages: Home, Category, Product Detail, Cart, Checkout, Account, Admin
2. Backend API routes: /products, /cart, /orders, /auth, /admin
3. Database schema: users, products, orders, categories, reviews
4. Authentication flow: signup → login → JWT → protected routes
5. Payment integration: Stripe/Razorpay checkout session
6. Cart logic: add/remove/update quantity, persist in LocalStorage
7. Search and filter: by category, price range, rating, brand
8. Image requirements: real product images (use picsum.photos with relevant seeds)""",
            "task_type": "smart", "tokens": 5000
        }
    ])

    progress_update(task_id, 35, "💻 [Coding Agent] Building full e-commerce platform...")
    code = llm(
        f"""Build a COMPLETE e-commerce platform: {idea}

Research: {res[:1500]}
Plan: {plan[:2000]}

OUTPUT: SINGLE SELF-CONTAINED HTML with React + Tailwind via CDN.

MUST INCLUDE ALL PAGES (as React components with routing):
1. HOME PAGE: Hero banner, featured products grid, category cards
2. PRODUCT LISTING: Filter sidebar (category, price, rating), product grid with sort
3. PRODUCT DETAIL: Image gallery, reviews, size/variant selector, Add to Cart
4. SHOPPING CART: Item list, quantity controls, price summary, checkout CTA
5. CHECKOUT: Address form, payment method selection, order summary
6. USER ACCOUNT: Login/Signup forms (simulated with LocalStorage)

PRODUCT DATA:
- Hardcode 20+ realistic products with names, prices, images, ratings, descriptions
- Images: use https://picsum.photos/seed/PRODUCT_NAME/400/400
- For fashion store: use clothing images; electronics: device images, etc.
- Categories with product counts

FUNCTIONALITY:
- Cart persists in LocalStorage
- Add/remove items, update quantity
- Total price calculation with tax
- Search bar with instant filter
- Category navigation
- Star rating display
- Toast notifications for add-to-cart
- Mobile responsive product grid
- Checkout form validation

CDN Stack:
- React 18 + ReactDOM + Babel
- Tailwind CSS CDN
- Lucide Icons CDN

Return ONLY complete <!DOCTYPE html>:""",
        "Coding Agent", "code", 55, task_id, tokens=8000
    )

    progress_update(task_id, 80, "✨ [Verify Agent] Testing e-commerce checkout flow...")
    verified = llm(
        f"""Verify this e-commerce platform for {idea}:

CHECKLIST:
✓ Products display correctly with images, prices, ratings
✓ Add to cart works and shows toast notification
✓ Cart page shows correct items and quantities
✓ Quantity increase/decrease works
✓ Remove from cart works
✓ Total price + tax calculation correct
✓ Checkout form validates all fields
✓ Search filter works
✓ Category navigation works
✓ Mobile responsive (products stack on mobile)
✓ LocalStorage persistence for cart
✓ No alert() — toast only
✓ All 20+ products have real images (picsum.photos)
✓ Login/Signup UI exists (simulated)

CODE:
{code[:5500]}

Fix ALL issues. Return complete <!DOCTYPE html>:""",
        "Verify Agent", "verify", 86, task_id, tokens=8000
    )

    final_html = strip(verified) or strip(code)
    files = {"index.html": final_html}
    save_files(slug, files)

    preview = quality_fix(final_html)
    if not preview or len(preview) < 500:
        preview = generate_preview(idea, verified or code, task_id, "ecommerce")

    progress_update(task_id, 98, "Finalizing...")
    return build_result(slug, files, preview, idea)


# ═══════════════════════════════════════════════════════════
# 8. MORE / CATCH-ALL BUILDER
#    Handles any category not explicitly matched above
# ═══════════════════════════════════════════════════════════
def build_more(idea, answers, task_id=None, intent=None):
    slug = make_slug(idea)
    theme = answers.get("q3", "Dark minimal")
    style = answers.get("q4", "Modern")
    features = ", ".join([str(v) for v in answers.values() if v]) or "responsive, dark theme"

    lower_idea = idea.lower()
    more_map = {
        "weather": "weather.html",
        "quiz": "quiz.html",
        "chat": "chat.html",
        "messenger": "chat.html",
        "kanban": "kanban.html",
        "todo": "kanban.html",
        "portfolio": "portfolio.html",
        "pomodoro": "pomodoro.html",
        "timer": "pomodoro.html",
        "blog": "blog.html",
        "convert": "converter.html"
    }

    for key, filename in more_map.items():
        if key in lower_idea:
            progress_update(task_id, 10, f"Loading pristine S.E.A.D.S. WebApp for {key.title()}...")
            app_dir = Path(r"E:\seads\backend\agents\more")
            html_path = app_dir / filename
            if html_path.exists():
                final_html = html_path.read_text(encoding="utf-8")
                files = {"index.html": final_html}
                save_files(slug, files)
                progress_update(task_id, 100, "Done!")
                return build_result(slug, files, final_html, idea)

    # Detect app type from idea
    u = idea.lower()
    if any(w in u for w in ["game", "play", "shoot", "chess", "snake", "tetris", "ludo"]):
        app_type = "game"
    elif any(w in u for w in ["weather", "forecast"]):
        app_type = "weather app"
    elif any(w in u for w in ["quiz", "trivia"]):
        app_type = "quiz app"
    elif any(w in u for w in ["chat", "messenger", "whatsapp"]):
        app_type = "chat app"
    elif any(w in u for w in ["todo", "kanban", "task"]):
        app_type = "todo app"
    elif any(w in u for w in ["portfolio", "resume", "cv"]):
        app_type = "portfolio website"
    elif any(w in u for w in ["blog", "article"]):
        app_type = "blog website"
    elif any(w in u for w in ["calculator", "convert"]):
        app_type = "utility app"
    elif any(w in u for w in ["dashboard", "analytics", "chart", "visualization"]):
        app_type = "data dashboard"
    else:
        app_type = "web application"

    progress_update(task_id, 8, f"🔍 [Search Agent] Researching {app_type} patterns...")
    res, plan, ux = parallel_llm([
        {
            "prompt": f"""Research how to build: {idea}
App type: {app_type}. Find best frameworks, UI patterns, feature lists,
and real-world examples to study.""",
            "task_type": "search", "tokens": 5000
        },
        {
            "prompt": f"""Plan a MASSIVE, production-quality {app_type} for: {idea}
Features requested: {features} | Theme: {theme} | Style: {style}

Define:
- Complete feature list (minimum 10 features)
- Data model and state structure
- UI components hierarchy
- Business logic and algorithms
- LocalStorage schema for persistence
- Error states and edge cases""",
            "task_type": "smart", "tokens": 5000
        },
        {
            "prompt": f"""UX & Design research for {app_type}: {idea}
Find: UI patterns, animation techniques, micro-interaction details,
color psychology for {theme} theme, accessibility requirements.""",
            "task_type": "search", "tokens": 4000
        }
    ])

    progress_update(task_id, 40, f"💻 [Coding Agent] Building {app_type}...")
    code = llm(
        f"""Build a COMPLETE, IIT-level {app_type} as single HTML: {idea}
Research: {res[:1500]}
Plan: {plan[:2000]}
UX: {ux[:1000]}
Theme: {theme} | Style: {style}

IMPLEMENT EVERYTHING:
- React 18 + Babel + Tailwind + Lucide via CDN
- All planned features fully implemented
- IIT-level UI/UX (glassmorphism, animations, micro-interactions)
- LocalStorage persistence
- Real domain content (no lorem ipsum)
- Loading states, error states, empty states
- Mobile responsive
- Toast notifications (no alert())
- Minimum 5 major features fully working

Return ONLY complete <!DOCTYPE html>:""",
        "Coding Agent", "code", 50, task_id, tokens=8000
    )

    progress_update(task_id, 80, f"✨ [Verify Agent] Auditing {app_type}...")
    verified = llm(
        f"""Audit this {app_type} for: {idea}
✓ All planned features implemented (not stubbed)
✓ React components render without error
✓ All interactive elements respond
✓ LocalStorage reads/writes correctly
✓ No alert()/confirm() — toast only
✓ Mobile layout works
✓ Loading and error states present
✓ Animations smooth (no jank)
✓ Content is realistic (no lorem ipsum)
CODE:
{code[:5000]}
Fix ALL bugs. Return complete <!DOCTYPE html>:""",
        "Verify Agent", "verify", 84, task_id, tokens=8000
    )

    final_html = strip(verified) or strip(code)
    files = {"index.html": final_html}
    save_files(slug, files)
    progress_update(task_id, 96, "Finalizing...")
    preview_html = quality_fix(final_html)
    if not preview_html or len(preview_html) < 500:
        preview_html = generate_preview(idea, verified or code, task_id, "more")
    return build_result(slug, files, preview_html, idea)


# ─────────────────────────────────────────────────────────────
# MASTER DISPATCHER — Routes to correct builder
# ─────────────────────────────────────────────────────────────
def dispatch(category, idea, answers, task_id=None, intent=None):
    builders = {
        # 7 Core Categories
        "website":     build_website,
        "mobile":      build_mobile_app,
        "design":      build_design_tool,
        "ppt":         build_ppt,
        "game":        build_game,
        "ml":          build_ml_project,
        "ecommerce":   build_ecommerce,
        "more":        build_more,
        # Legacy aliases (backward compat)
        "dataviz":     build_game,     # dataviz replaced by game
        "shooter":     build_game,
        "chess":       build_game,
        "ludo":        build_game,
        "snake":       build_game,
        "tetris":      build_game,
        "gravity":     build_game,
        # Media / misc through catch-all
        "youtube":     build_more,
        "movies":      build_more,
        "spotify":     build_more,
    }
    builder = builders.get(category, build_more)

    log.info(f"[DISPATCH] category={category} builder={builder.__name__} idea={idea[:50]}")
    progress_update(task_id, 3, f"🚀 Dispatching to {builder.__name__} [IIT-Level Mode]...")

    try:
        result = builder(idea, answers, task_id, intent)
        if result:
            return result
    except Exception as e:
        log.error(f"[BUILDER ERROR] {builder.__name__}: {e}", exc_info=True)
        progress_update(task_id, 0, f"Builder error: {str(e)[:100]}")

    # Emergency fallback
    progress_update(task_id, 50, "Emergency fallback builder...")
    return build_more(idea, answers, task_id, intent)
