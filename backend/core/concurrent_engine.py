# core/concurrent_engine.py — FINAL FIXED
# Root cause fixed: integrator now runs AFTER parallel agents complete
# Anti-gravity app added, all game types improved

import concurrent.futures, re, time
from core.llm_config import get_llm_response

BUDGETS = {
    "architect":  300, "game_logic": 3500, "ui_designer": 2000,
    "state": 800, "animation": 800, "backend": 1200, "database": 400,
    "auth": 600, "realtime": 600, "ai_feature": 800, "search": 500,
    "social": 700, "dashboard": 800, "mobile": 400, "security": 300,
    "docs": 300, "integrator": 5000,
}
AGENT_MODELS = {
    "game_logic":"code","integrator":"code",
    "ui_designer":"code","default":"code",
    "architect":"fast","docs":"fast","mobile":"code",
}

def _game_logic(idea, answers):
    u = idea.lower()
    if "chess" in u:
        return f"""Write COMPLETE chess game JavaScript.
Mode:{answers.get('q1','vs Computer AI')}, Difficulty:{answers.get('q2','Medium')}
MUST include: all 6 piece types with correct movement rules,
check/checkmate detection, castling, en passant, pawn promotion,
minimax AI (depth 3), move highlighting on click, captured pieces display.
Return ONLY JavaScript."""

    if "ludo" in u:
        return """Write COMPLETE Ludo game JavaScript using Canvas.
MUST include: 4 colored players (Red/Green/Yellow/Blue) on proper Ludo board,
dice roll animation, token movement along correct path (52 squares),
home column, safe squares, capturing, star squares, winning condition,
computer AI for 3 opponents, turn indicator.
Return ONLY JavaScript."""

    if any(w in u for w in ["anti gravity","antigravity","anti-gravity","gravity flip"]):
        return """Write COMPLETE anti-gravity arcade game JavaScript using Canvas.
MUST include:
- Player spaceship that flips gravity with SPACE bar or tap
- Ship moves right automatically, player controls gravity direction
- Cave/tunnel that narrows over time, procedurally generated
- Smooth physics: velocity += gravity each frame
- Neon particle trail behind ship (10 particles)
- Collision with top/bottom walls = game over
- Score increases with distance survived
- Speed gradually increases
- Best score saved to localStorage
- Colorful neon aesthetic on black background
- Restart on R or button click
Return ONLY JavaScript."""

    if any(w in u for w in ["car","racing","drive","speed"]):
        return f"""Write COMPLETE top-down car racing game JavaScript using Canvas.
MUST include: smooth car controls (arrow keys/WASD), scrolling road with lane markings,
enemy cars spawning and moving down, collision detection (player explodes),
speed increases over time, distance score, lives system (3 lives), best score localStorage.
Return ONLY JavaScript."""

    if any(w in u for w in ["snake"]):
        return """Write COMPLETE snake game JavaScript using Canvas.
MUST: smooth grid movement, food spawning, growth, wall+self collision,
score, high score localStorage, increasing speed, restart on space/button.
Return ONLY JavaScript."""

    if any(w in u for w in ["battle royale","free fire","pubg","shoot"]):
        return f"""Write COMPLETE top-down battle royale JavaScript using Canvas.
MUST: WASD movement, mouse aim+click to shoot, enemy AI, shrinking safe zone circle,
health bar, ammo counter, kill counter, minimap (top-right corner), 
loot boxes, game over screen. Return ONLY JavaScript."""

    if any(w in u for w in ["tetris"]):
        return """Write COMPLETE Tetris JavaScript using Canvas.
MUST: all 7 tetromino shapes, rotation (up arrow), movement, hard drop (space),
line clearing with animation, score (level up every 10 lines), speed increase,
next piece preview, game over detection. Return ONLY JavaScript."""

    if any(w in u for w in ["platformer","mario","jump","run"]):
        return f"""Write COMPLETE platformer game JavaScript using Canvas.
MUST: player with jump (space/up), gravity, platforms procedurally placed,
enemies that patrol, coins to collect, score counter, camera follows player,
death pit detection, restart. Return ONLY JavaScript."""

    # Generic
    return f"""Write COMPLETE game/app JavaScript using Canvas for: {idea}
User wants: {answers}
MUST be fully playable: game loop, controls, collision, score, game over, restart.
Return ONLY JavaScript code."""

def _ui(idea, answers):
    theme = answers.get("q3","Dark neon")
    u = idea.lower()
    is_game = any(w in u for w in ["game","chess","ludo","car","snake","tetris",
                                    "shoot","battle","gravity","platformer"])
    if is_game:
        return f"""Create HTML+CSS game UI for: {idea}, theme: {theme}
MUST include:
- <canvas id="gameCanvas"> centered, 800x500px, dark background
- Score display top-left, lives/health top-right  
- Start screen overlay (id="startScreen") with title + START button
- Game over overlay (id="gameOverScreen") with score + RESTART button
- HUD bar above canvas
- Neon glow CSS effects: text-shadow, box-shadow
- Smooth CSS animations for overlays
Return ONLY HTML structure + embedded <style>. No JavaScript."""
    else:
        return f"""Create stunning HTML+CSS UI for: {idea}, theme: {theme}
MUST: complete structure, beautiful CSS, proper IDs for JS to hook into,
animations, responsive layout. Return ONLY HTML+CSS. No JavaScript."""

def _anim(idea, answers):
    return f"""Write visual effects JavaScript for: {idea}
Include: particle system (canvas overlay), score popup animation (+points floating up),
screen flash on hit, smooth number counter animation.
Return ONLY JavaScript. Under 50 lines."""

def _integrator(idea, answers, outputs):
    ui   = outputs.get("ui_designer","")[:2500]
    game = outputs.get("game_logic","")[:4000]
    anim = outputs.get("animation","")[:600]
    rest = "".join(outputs.get(k,"")[:300] for k in
                   ["state","social","search","ai_feature","mobile"])

    return f"""You are an expert integrator. Combine into ONE complete HTML file for: {idea}
User preferences: {answers}

=== UI HTML+CSS ===
{ui or "Create beautiful dark-themed game UI with canvas"}

=== GAME LOGIC JAVASCRIPT ===
{game or "Create complete working game"}

=== ANIMATIONS ===
{anim}

=== EXTRAS ===
{rest}

ABSOLUTE RULES:
1. Return ONLY the complete HTML — start with <!DOCTYPE html>
2. All CSS in <style> inside <head>  
3. All JS in <script> at end of <body>
4. 100% self-contained (Google Fonts only external)
5. EVERYTHING MUST WORK — no placeholders
6. Game must be immediately playable (show start screen or autostart)
7. No TODO / placeholder comments

Output the FULL HTML file now:"""

def _simple_prompt(agent, idea, answers):
    m = {
        "architect": f'Return JSON: {{"files":["index.html"],"tech":"HTML5/JS"}} for {idea}',
        "state":     f"Write localStorage save/load state class for {idea}. JS only.",
        "backend":   f"Write FastAPI backend for {idea}. Python only.",
        "database":  f"Write SQLite schema for {idea}. SQL+Python only.",
        "auth":      f"Write JWT auth endpoints for {idea}. Python+HTML only.",
        "realtime":  f"Write WebSocket client JS for {idea}. Brief.",
        "ai_feature":f"Write smart AI behavior JS for {idea}. No external APIs.",
        "search":    f"Write real-time search/filter JS for {idea}.",
        "social":    f"Write like/comment/share JS for {idea}. DOM manipulation.",
        "dashboard": f"Write Canvas charts (bar/line/pie) for {idea}. JS only.",
        "mobile":    f"Write mobile responsive CSS + touch events for {idea}.",
        "security":  f"Write input validation JS for {idea}.",
        "docs":      f"Write README.md for {idea}. Under 150 words. Markdown only.",
    }
    return m.get(agent, f"Write code for {agent} in {idea}. Code only.")

def _get_prompt(agent, ctx, outputs=None):
    idea    = ctx["idea"]
    answers = ctx.get("answers",{})
    if agent == "game_logic":  return _game_logic(idea, answers)
    if agent == "ui_designer": return _ui(idea, answers)
    if agent == "animation":   return _anim(idea, answers)
    if agent == "integrator":  return _integrator(idea, answers, outputs or {})
    return _simple_prompt(agent, idea, answers)

def _run_one(agent, ctx, outputs=None):
    start = time.time()
    try:
        prompt = _get_prompt(agent, ctx, outputs)
        task_type = AGENT_MODELS.get(agent, AGENT_MODELS["default"])
        budget = BUDGETS.get(agent, 800)
        result = get_llm_response(
            prompt=prompt, model=None, max_tokens=budget,
            system="Expert developer. Write complete working code only. No explanations.",
            temperature=0.15,
            task_type=task_type,
        )
        elapsed = round(time.time()-start,1)
        print(f"  ✅ [{agent:12}] {elapsed}s | {len(result or ''):,} chars")
        return agent, result or ""
    except Exception as e:
        print(f"  ❌ [{agent:12}] failed: {e}")
        return agent, ""

def run_concurrent_agents(agent_list, ctx):
    """
    PHASE A: All non-integrator agents run in parallel
    PHASE B: Integrator runs AFTER with all outputs (FIXED!)
    """
    parallel = [a for a in agent_list if a not in ("integrator","docs")]
    finals   = [a for a in agent_list if a in ("integrator","docs")]
    outputs  = {}

    print(f"\n⚡ Phase A: {len(parallel)} agents parallel...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(parallel),8)) as ex:
        futs = {ex.submit(_run_one,a,ctx): a for a in parallel}
        for f in concurrent.futures.as_completed(futs):
            name, res = f.result()
            outputs[name] = res
    print(f"  📦 Phase A done — {sum(len(v) for v in outputs.values()):,} chars total")

    if "integrator" in finals:
        print(f"\n⚡ Phase B: Integrator combining all {len(outputs)} pieces...")
        _, html = _run_one("integrator", ctx, outputs)
        # Clean markdown fences
        html = re.sub(r"^```html\s*","",html.strip())
        html = re.sub(r"^```\s*","",html.strip())
        html = re.sub(r"```\s*$","",html.strip()).strip()
        # Find DOCTYPE if buried
        if not html.startswith("<!DOCTYPE") and not html.startswith("<html"):
            for m in ["<!DOCTYPE","<html"]:
                idx = html.find(m)
                if idx != -1: html = html[idx:]; break
        outputs["integrator"] = html
        print(f"  📄 Integrator: {len(html):,} chars")

    if "docs" in finals:
        _, docs = _run_one("docs", ctx)
        outputs["docs"] = docs

    return outputs
