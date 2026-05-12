# agents/category_builders.py — v14 Enterprise Multi-Agent Builders
# ============================================================

import os, json, time, re, concurrent.futures, logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("CategoryBuilders")
OUTPUT_DIR = Path(os.getenv("ONLINE_APP_DIR", r"E:\seads\online_app"))

# -----------------------------------------------------------------
# CORE LLM WRAPPER: Routes to the correct Agent Type
# -----------------------------------------------------------------
def llm(prompt: str, tokens: int = 10000, agent_name: str = "", task_type: str = "code", progress: int = None, task_id: str = None) -> str:
    from core.llm_config import get_llm_response, SEADS_V14_SYSTEM_PROMPT
    if progress is not None:
        if task_id:
            try:
                from main import PROGRESS_DATA
                PROGRESS_DATA[task_id] = {"percent": progress, "status": f"{agent_name} is active..."}
            except: pass
    
    try:
        log.info(f"  [{agent_name}] -> {task_type}")
    except: pass

    for attempt in range(1, 4):
        try:
            result = get_llm_response(
                prompt=prompt,
                max_tokens=tokens,
                temperature=0.1,
                system=SEADS_V14_SYSTEM_PROMPT,
                task_type=task_type,
            )
            if result and len(result) > 50:
                return result
        except Exception:
            time.sleep(2)
    return ""

def strip(raw: str) -> str:
    if not raw: return ""
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", raw)
    if match: return match.group(1).strip()
    return re.sub(r"```[\w]*\n?","",raw).replace("```","").strip()

def parse_multi_files(raw: str) -> dict:
    """
    Parses output following the SEADS v14 multi-file format:
    === FILE: [path] === then [code] === END ===
    """
    files = {}
    pattern = r"=== FILE: (.*?) ===\s*([\s\S]*?)(?===\s*FILE:|$|===\s*END)"
    matches = re.finditer(pattern, raw)
    for m in matches:
        path = m.group(1).strip()
        content = m.group(2).strip()
        if path and content:
            files[path] = content
    
    # Fallback to single index.html if no pattern found
    if not files and "<!DOCTYPE html>" in raw:
        files["index.html"] = strip(raw)
    return files

def save_files(slug: str, files: dict) -> dict:
    project_dir = OUTPUT_DIR / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for fname, content in files.items():
        if not content: continue
        fpath = project_dir / Path(fname)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8", errors="replace")
        paths[fname] = str(fpath)
    return paths

def quality_fix(html: str) -> str:
    html = re.sub(r'alert\s*\([^)]*\)\s*;?', '/* toast-instead */', html)
    html = re.sub(r'confirm\s*\([^)]*\)', 'true', html)
    html = re.sub(
        r'<img([^>]*?)src=["\'](?!http|data:)[^"\']{3,}["\']',
        lambda m: f'<img{m.group(1)}src="https://picsum.photos/seed/{abs(hash(m.group(0)))%9999}/800/600"',
        html
    )
    return html

# ═══════════════════════════════════════════════════════════
# 🌐 WEBSITE BUILDER (React + Tailwind + Shadcn)
# ═══════════════════════════════════════════════════════════
def build_website(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🌐 WEBSITE PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    # 1. Search Agent (Perplexity)
    research = llm(f"Research UI/UX best practices for {idea} landing page/portfolio.", 
                   agent_name="Search Agent (Perplexity)", task_type="search", progress=10, task_id=task_id)

    # 2. Planning Agent (DeepSeek-R1)
    plan = llm(f"Decompose this project into a multi-file React architecture (src/components, src/pages, etc): {idea}\nResearch: {research}", 
               agent_name="Planning Agent (DeepSeek-R1)", task_type="smart", progress=30, task_id=task_id)

    # 3. Coding Agent (DeepSeek V3 / Qwen)
    code = llm(f"Build COMPLETE React + Tailwind + Shadcn project based on plan: {plan}\nRequirements: {json.dumps(answers)}\n\nUSE FORMAT: === FILE: [path] === [code] === END ===", 
               agent_name="Coding Agent (DeepSeek V3)", task_type="code", progress=70, task_id=task_id)

    # 4. Verify Agent (Claude 3 Opus)
    verified_code = llm(f"Audit the following project code. Fix bugs and ensure enterprise React patterns. Return the CORRECTED code for ALL files using the === FILE: [path] === format.\n\nCode: {code}", 
                        agent_name="Verify Agent (Claude 3 Opus)", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)

    # Generate a single-file preview for the UI
    preview_prompt = f"Convert this multi-file project into a single-file React CDN Preview: {json.dumps(list(files.keys()))}\n\nCode context: {verified_code[:5000]}"
    preview = llm(preview_prompt, agent_name="Preview Generator", task_type="fast", progress=95, task_id=task_id)

    return {
        "preview_html": quality_fix(strip(preview)),
        "files": [{"name":k,"content":v,"size":len(v)} for k,v in files.items()],
        "slug": slug, "paths": paths, "file_count": len(files)
    }

# ═══════════════════════════════════════════════════════════
# 📱 MOBILE APP BUILDER (Kivy / BeeWare)
# ═══════════════════════════════════════════════════════════
def build_mobile_app(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"📱 MOBILE PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    frame = answers.get("q1", "Kivy")
    mobile_lifecycle = """
    1. Choose Framework: BeeWare (Native UI) or Kivy (OpenGL/Custom).
    2. Environment: python -m venv myapp_env, pip install briefcase/kivy.
    3. Coding Phase: Write main.py (Logic) and design UI (.kv for Kivy or Python for BeeWare).
    4. Package: briefcase create android/ios or buildozer.
    5. Compile: .apk / Xcode project.
    6. Testing: Emulator/Sideload.
    7. User Interactive Preview.
    """

    plan = llm(f"Plan a {frame} mobile app for: {idea}. Strictly follow this 7-step lifecycle: {mobile_lifecycle}", 
               agent_name="Planning Agent", task_type="smart", progress=30, task_id=task_id)

    code = llm(f"Implement FULL Python code for the {frame} mobile app: {idea}.\nUse format: === FILE: main.py === [code] === FILE: requirements.txt === [code] === END ===", 
          # ═══════════════════════════════════════════════════════════
# 🎨 DESIGN TOOL BUILDER (OpenCV/Pillow/scikit-image/Albumentations)
# ═══════════════════════════════════════════════════════════
def build_design_tool(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🎨 DESIGN PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    # 1. Search Agent
    research = llm(f"Research computer vision best practices for {idea}. Libraries: OpenCV, Pillow, Albumentations.", 
                   agent_name="Search Agent (Perplexity)", task_type="search", progress=10, task_id=task_id)

    # 2. Planning Agent
    plan = llm(f"Plan a modular design tool architecture for {idea}. Plan for Canvas API + Background Engine.\nResearch: {research}", 
               agent_name="Planning Agent (DeepSeek-R1)", task_type="smart", progress=30, task_id=task_id)

    # 3. Coding Agent
    code = llm(f"Implement UI and Filter Engine using React + OpenCV.js/Fabric.js. Use format === FILE: [path] === [code] === END ===\n{plan}", 
               agent_name="Coding Agent (DeepSeek V3)", task_type="code", progress=70, task_id=task_id)

    # 4. Verify Agent
    verified_code = llm(f"Verify and optimize this design tool code: {code}", 
                        agent_name="Verify Agent (Opus)", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)

    # Preview from first HTML file found or generate one
    preview_html = files.get("index.html") or files.get("app.html") or "<h1>Design Tool Generated</h1>"
    
    return {"preview_html": quality_fix(preview_html), "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug, "paths": paths}

# ═══════════════════════════════════════════════════════════
# 📊 PPT BUILDER (python-pptx / Marp / Manim)
# ═══════════════════════════════════════════════════════════
def build_ppt(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"📊 PPT PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    tech = answers.get("q1", "python-pptx")
    # 1. Search Agent
    research = llm(f"Research high-quality presentation structures for {idea} using {tech}.", 
                   agent_name="Search Agent", task_type="search", progress=10, task_id=task_id)

    # 2. Planning Agent
    plan = llm(f"Plan a slide deck or animation project for {idea} using {tech}. Research: {research}", 
               agent_name="Planning Agent", task_type="smart", progress=30, task_id=task_id)

    # 3. Coding Agent
    code = llm(f"Write the {tech} scripts or Markdown code. Include multi-file README and requirements.\n{plan}", 
               agent_name="Coding Agent", task_type="code", progress=70, task_id=task_id)

    # 4. Verify Agent
    verified_code = llm(f"Verify the presentation code: {code}", 
                        agent_name="Verify Agent", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)

    return {"preview_html": f"<h1>Presentation ({tech})</h1>", "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug}

# ═══════════════════════════════════════════════════════════
# 🎮 GAME & DATA VIZ BUILDER (Phaser / Three.js / Lua)
# ═══════════════════════════════════════════════════════════
def build_dataviz(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🎮 GAME/VIZ PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    stack = answers.get("q1", "Three.js")
    research = llm(f"Research {stack} patterns for {idea}.", agent_name="Search Agent", task_type="search", progress=10, task_id=task_id)
    plan = llm(f"Plan the game/viz architecture: {idea}. Stack: {stack}.", agent_name="Planning Agent", task_type="smart", progress=30, task_id=task_id)
    code = llm(f"Implement high-end {stack} logic. USE FORMAT: === FILE: [path] === [code] === END ===\n{plan}", 
               agent_name="Coding Agent", task_type="code", progress=70, task_id=task_id)
    verified_code = llm(f"Audit and polish the visual code: {code}", agent_name="Verify Agent", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)
    preview = files.get("index.html") or "<h1>Visual Engine Active</h1>"

    return {"preview_html": quality_fix(preview), "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug}

# ═══════════════════════════════════════════════════════════
# 🤖 ML PROJECT BUILDER (Scikit-learn / PyTorch / LangChain)
# ═══════════════════════════════════════════════════════════
def build_ml_project(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🤖 ML PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    lib = answers.get("q1", "Scikit-learn")
    research = llm(f"Research ML pipeline details (data, algo, evaluation) for {idea} using {lib}.", agent_name="Search Agent", task_type="search", progress=10, task_id=task_id)
    plan = llm(f"Plan full ML project: Data source, Preprocessing, Model training, and Prediction UI.\nResearch: {research}", agent_name="Planning Agent", task_type="smart", progress=30, task_id=task_id)
    code = llm(f"Implement Python logic and React UI. USE FORMAT: === FILE: [path] === [code] === END ===\n{plan}", agent_name="Coding Agent", task_type="code", progress=70, task_id=task_id)
    verified_code = llm(f"Verify and audit the ML files: {code}", agent_name="Verify Agent", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)

    return {"preview_html": "<h1>ML Model & UI Ready</h1>", "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug}

# ═══════════════════════════════════════════════════════════
# 🛒 E-COMMERCE BUILDER (React + Node + MongoDB + Stripe)
# ═══════════════════════════════════════════════════════════
def build_ecommerce(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🛒 ECOMMERCE PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    guide = "Step 1: Frontend (React+Tailwind) | Step 2: Backend (Node+Express) | Step 3: DB (MongoDB) | Step 4: Auth (JWT) | Step 5: Payment (Stripe) | Step 6: Deploy (Vercel)"
    research = llm(f"Research ecommerce best practices for {idea} niche.", agent_name="Search Agent", task_type="search", progress=10, task_id=task_id)
    plan = llm(f"Plan enterprise ecommerce for {idea} using this guide: {guide}.", agent_name="Planning Agent", task_type="smart", progress=30, task_id=task_id)
    code = llm(f"Implement Full-Stack Ecommerce. USE FORMAT: === FILE: [path] === [code] === END ===\n{plan}", 
               agent_name="Coding Agent", task_type="code", progress=70, task_id=task_id)
    verified_code = llm(f"Audit the ecommerce system for security and payments: {code}", agent_name="Verify Agent", task_type="verify", progress=90, task_id=task_id)

    files = parse_multi_files(verified_code)
    paths = save_files(slug, files)
    preview = files.get("index.html") or "<h1>Ecommerce Preview Ready</h1>"

    return {"preview_html": quality_fix(preview), "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug}

def build_more(idea: str, answers: dict, task_id: str = None) -> dict:
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]
    code = llm(f"Build {idea} using v14 Multi-Agent Pipeline.", agent_name="Coding Agent", task_type="code", progress=90, task_id=task_id)
    files = parse_multi_files(code)
    save_files(slug, files)
    return {"preview_html": files.get("index.html", ""), "slug": slug}
# 🛒 E-COMMERCE BUILDER (React + Node + MongoDB + Stripe)
# ═══════════════════════════════════════════════════════════
def build_ecommerce(idea: str, answers: dict, task_id: str = None) -> dict:
    log.info(f"🛒 ECOMMERCE PIPELINE: {idea}")
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]

    guide = """
    Step 1: Frontend (React + Tailwind)
    Step 2: Backend (Node + Express)
    Step 3: Database (MongoDB)
    Step 4: Auth (JWT/NextAuth)
    Step 5: Payment (Stripe/Razorpay)
    Step 6: Deployment (Vercel)
    """

    plan = llm(f"Plan enterprise ecommerce for {idea}. Following: {guide}", 
               agent_name="DeepSeek-R1", task_type="smart", progress=30, task_id=task_id)

    code = llm(f"Implement full-stack Ecommerce (React + Tailwind frontend). {plan}", 
               agent_name="Coding Agent", task_type="code", progress=70, task_id=task_id)

    final_html = quality_fix(strip(code))
    files = {"index.html": final_html, "README.md": guide}
    paths = save_files(slug, files)

    return {"preview_html": final_html, "files": [{"name":k,"content":v} for k,v in files.items()], "slug": slug}

def build_more(idea: str, answers: dict, task_id: str = None) -> dict:
    slug = re.sub(r'[^a-z0-9-]','',idea.replace(" ","-").lower())[:35]
    res = llm(f"Build {idea}", agent_name="Coding Agent", task_type="code", progress=90, task_id=task_id)
    files = {"index.html": strip(res)}
    save_files(slug, files)
    return {"preview_html": files["index.html"], "slug": slug}

def dispatch(category: str, idea: str, answers: dict, task_id: str = None) -> dict:
    builders = {
        "website": build_website, "mobile": build_mobile_app, "design": build_design_tool,
        "ppt": build_ppt, "dataviz": build_dataviz, "ml": build_ml_project,
        "ecommerce": build_ecommerce, "more": build_more
    }
    return builders.get(category, build_more)(idea, answers, task_id=task_id)

