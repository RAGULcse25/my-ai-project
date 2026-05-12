# agents/preview_agent.py — S.E.A.D.S. v14 LOVABLE AI Preview Engine
# ═══════════════════════════════════════════════════════════════
# Generates FULLY INTERACTIVE, SELF-CONTAINED HTML previews
# that run 100% in browser — no backend, no server needed.
# Just like Lovable AI / v0.dev — user can actually USE the preview.
# ═══════════════════════════════════════════════════════════════

import re
from core.llm_config import get_llm_response

PREVIEW_SYSTEM = """You are the SEADS Preview Engine — a world-class expert at building
fully interactive, self-contained single-file HTML5 applications.

ABSOLUTE RULES:
1. Return ONLY raw <!DOCTYPE html> — zero markdown fences, zero explanations
2. 100% self-contained: all CSS in <style>, all JS in <script>, no external REST calls
3. Use CDN links ONLY: React (CDN), Tailwind (CDN), Chart.js (CDN), Lucide (CDN)
   CDN links must load from reliable CDNs (unpkg, cdnjs, jsdelivr)
4. Never use alert(), confirm(), prompt() — always toast/DOM notifications
5. All sample data HARDCODED in JS arrays (no fetch() to localhost)
6. Every button, form, and interaction FULLY WORKS in a sandboxed iframe
7. Dark glassmorphism UI (#070B14 base, vibrant accent colors, backdrop-blur)
8. Minimum 3 interactive features working end-to-end
9. Mobile responsive with smooth animations
10. Start with <!DOCTYPE html> — NOTHING before it"""

# ──────────────────────────────────────────────────────────────
# CATEGORY-SMART PREVIEW PROMPTS
# Each category gets a deeply tailored prompt for maximum interactivity
# ──────────────────────────────────────────────────────────────
CATEGORY_PROMPTS = {

"website": """Build a COMPLETE, INTERACTIVE preview of: {idea}

Make it a stunning multi-section website that works 100% in browser:

SECTIONS (all implemented):
1. STICKY NAVBAR: Logo + nav links (smooth scroll), mobile hamburger menu
2. HERO: Full-viewport animated gradient bg, headline, subtitle, 2 CTA buttons
3. FEATURES: 6 glassmorphism cards with icons, hover glow, staggered reveal on scroll
4. ABOUT: Stats counter (animate 0→value using IntersectionObserver), split layout
5. GALLERY/PORTFOLIO: Grid with hover overlay and lightbox modal on click
6. TESTIMONIALS: Auto-sliding carousel with star ratings
7. CONTACT FORM: Name/email/message inputs, validation, success toast on submit
8. FOOTER: Multi-column with social icons

INTERACTIVITY:
- Smooth scroll to sections on nav click
- Contact form validates + shows "Message sent! ✓" toast (no backend needed)
- Counter animation on scroll into view
- Hamburger menu opens/closes mobile nav
- Gallery lightbox shows full image + prev/next navigation

DESIGN: Glassmorphism dark (#070B14 base), gradient accents, Inter font from CDN
All animations: CSS keyframes + IntersectionObserver for scroll reveals""",

"mobile": """Build a FULLY INTERACTIVE preview of this mobile app: {idea}

Since this is a Python app, create a BROWSER-BASED SIMULATION that looks and
feels exactly like the real app — user can fully interact with it:

IMPLEMENT:
- App-like layout (mobile viewport: max-width 420px, centered in dark bg)
- Navigation: bottom tab bar with icons (clickable, switches views)
- All core features working with JavaScript + localStorage
- Sample data: 15+ realistic records loaded from JS arrays
- Full CRUD: add new items (form), edit (click to edit), delete (confirm)
- Search/filter working in real-time as user types
- Charts/stats if applicable (Chart.js via CDN)
- Form validation with error messages shown inline

MUST FEEL LIKE A REAL APP:
- Smooth page transitions (slide/fade between views)
- Loading spinner on "save" actions (0.5s delay for realism)
- Toast notifications: "Saved!", "Deleted!", "Updated!"
- Empty state with illustration when no data
- Pull-to-refresh simulation (press refresh icon)

DESIGN: Native mobile feel — bottom nav bar, card-based lists,
FAB (floating action button) to add new item, status bar at top""",

"design": """Build a COMPLETE, WORKING browser-based design tool: {idea}

IMPLEMENT A REAL DESIGN TOOL:
- HTML5 Canvas (fill browser viewport)
- TOOLS PANEL (left or top):
  * Select (click to select elements, drag to move)
  * Text tool (click canvas to place editable text)
  * Rectangle, Circle tool (drag to draw)
  * Color picker for fill + stroke
  * Eraser (erase canvas area)
- PROPERTIES PANEL (right): X, Y, W, H, Opacity, Color inputs
- FILTERS (sliders): Brightness, Contrast, Blur, Saturation
- BUTTONS: Undo (Ctrl+Z), Clear, Save as PNG (download button)
- 5+ TEMPLATES: Click to load preset design

ALL TOOLS MUST WORK:
- Click+drag draws shapes correctly
- Double-click canvas places editable text
- Color picker actually changes fill
- Save PNG downloads the canvas image
- Undo reverts last action""",

"ppt": """Build a COMPLETE, INTERACTIVE presentation: {idea}

Create a beautiful Reveal.js-powered presentation:
- Use Reveal.js 4 via CDN
- 10 full slides with real content (NO placeholders)
- Keyboard navigation: arrows, space bar
- Progress bar visible at bottom
- Slide counter (X/10)
- Speaker notes (press S)
- Fullscreen (press F)
- Overview mode (press O)
- Chart.js chart on at least 2 slides
- Fragment animations (bullet points reveal one by one)
- Presenter timer in top-right corner
ALL slides styled beautifully — hero slide + content slides + final CTA slide""",

"game": """Build a COMPLETE, FULLY PLAYABLE browser game: {idea}

IMPLEMENT A COMPLETE GAME with these mandatory elements:

1. GAME CANVAS:
   - HTML5 Canvas element, full-width, responsive
   - requestAnimationFrame game loop at 60 FPS
   - Clear rendering with anti-aliasing

2. GAME STATES (all implemented):
   - START SCREEN: Title, instructions, "Play" button with glow effect
   - PLAYING: Full game logic, rendering, input handling
   - PAUSED: Press P or Escape, overlay with "Resume" button
   - GAME OVER: Final score, high score (LocalStorage), "Play Again" button

3. GAME MECHANICS:
   - Player entity with smooth keyboard/mouse/touch controls
   - Collision detection (bounding box or circle)
   - Scoring system with animated score display
   - Difficulty progression (speed increases or more enemies)
   - Particle effects on collisions/scoring

4. UI OVERLAY (HTML over canvas):
   - Score display (top-left, animated on change)
   - Level/wave indicator
   - Lives/health bar
   - Pause button (top-right)

5. AUDIO:
   - Web Audio API for sound effects (oscillator beeps)
   - Different sounds for: score, hit, game over, level up

6. VISUAL STYLE:
   - Dark space theme (#070B14 background)
   - Neon glow effects on entities
   - Trail/particle effects
   - Smooth animations and transitions

EVERY interaction must work. The game must be IMMEDIATELY playable on load.""",

"ml": """Build a COMPLETE, BEAUTIFUL ML project preview: {idea}

Create a stunning, FULLY INTERACTIVE ML prediction interface:

LEFT PANEL — Input Form:
- All feature inputs (sliders, dropdowns, number inputs with labels)
- Tooltips on hover explaining each feature
- 5 SAMPLE TEST CASES as clickable buttons that autofill the form
- "Predict" button with loading animation (0.8s spinner then result)

RIGHT PANEL — Results:
- Animated prediction result reveal (slide up from bottom)
- Confidence gauge (circular progress meter, fill on predict)
- Prediction value large text with unit
- "Confidence: XX%" with animated fill bar

BOTTOM SECTION — Visualizations:
- FEATURE IMPORTANCE: horizontal bar chart (Chart.js) with gradient bars
- CONFUSION MATRIX (for classifiers): colored heatmap grid
- PREDICTION HISTORY table (last 10 predictions shown)

MODEL INFO CARD:
- Algorithm name, training accuracy, data size
- "How it works" expandable accordion

DESIGN: Dark glassmorphism (#070B14), gradient buttons,
glowing chart lines, smooth animations on every interaction.
This must look like a real IIT ML project demo — beautiful AND functional.""",

"ecommerce": """Build a COMPLETE, FULLY INTERACTIVE e-commerce store: {idea}

IMPLEMENT ALL PAGES (React 18 + Babel + Tailwind via CDN):

HOME:
- Hero banner carousel (3 slides, auto-slides every 4s)
- Category grid (click to filter products)
- Flash sale countdown timer
- 60+ product cards

PRODUCT LISTING:
- Product card: image (picsum), name, price ₹, MRP strikethrough, % discount
- Hover: Quick add button appears, wishlist heart
- Search bar: live filter as user types (debounced)
- Sort: low-high, high-low, rating, newest
- Filter: price range slider, category checkboxes, rating filter

PRODUCT DETAIL (click any product card):
- Image gallery (main + 4 thumbnails, click to switch)
- Size selector, color selector
- Quantity picker (+/-)
- Add to Cart (animated), Buy Now, Wishlist
- Rating bar chart + 5 sample reviews

CART DRAWER (slides in from right on cart click):
- All added items with quantity input and remove
- Promo code "SAVE10" applies 10% discount
- Order total calculation
- "Checkout" → 3-step checkout flow → success confetti

WISHLIST PAGE, ORDER SUCCESS PAGE

ALL INTERACTIONS WORK: cart persists in localStorage,
filters + search update grid live, checkout flow completes.""",

"shooter": """Build a COMPLETE, FULLY PLAYABLE {idea} game:

HTML5 Canvas game — MUST be immediately playable:
- WASD + Mouse aim controls (instructions on screen)
- 60fps game loop with requestAnimationFrame + delta time
- Player: glowing circle, moves with WASD, aims at mouse, clicks to shoot
- Enemies: 3 types, spawn from edges, pathfind toward player
- Bullets: fast projectiles, particle trail, hit detection
- Wave system: wave announcement, increasing difficulty
- HUD: health bar, ammo counter, score, wave number, minimap
- Particle effects: muzzle flash, blood splatter, explosions
- Game over + restart flow
- Start screen: "Click to Start", controls listed

IMMEDIATELY PLAYABLE — no setup needed, game starts on click.""",

"chess": """Build a COMPLETE, FULLY PLAYABLE chess game: {idea}

CHESS ENGINE INSTRUCTIONS:
- You MUST use <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.3/chess.min.js"></script> for game logic (validating moves, check, checkmate).
- 8x8 board rendered as HTML grid (CSS Grid).
- All pieces render as Unicode chess symbols (♟♞♝♜♛♚).
- CLICK a piece to select it (highlight legal squares using chess.js `moves({{verbose: true}})`).
- CLICK a highlighted square to move the piece.
- Special moves: castling, en passant, pawn promotion handled properly.
- AI opponent using Minimax (depth 2 or 3) evaluating piece values.
- Move history panel (right side).
- Captured pieces shown at bottom of each side.
- Game Over modal with Restart button.
- Make the UI look like a premium AAA game (glassmorphism/dark theme).""",

"ludo": """Build a COMPLETE, FULLY PLAYABLE Ludo game: {idea}

LUDO IN PURE JS + CANVAS:
- Full Ludo board drawn on Canvas (700×700)
- 4 colors: Red, Green, Yellow, Blue with 4 tokens each
- Complete path arrays all 4 colors (57 cells)
- "Roll Dice" button → animated dice → moves token
- AI players (3 AI opponents + 1 human)
- Rules: 6 to enter, capture sends home, safe squares protect
- Token selection: if multiple can move, show options, player chooses
- Turn indicator shows current player's color
- Win detection: first all 4 tokens reach home
- Confetti animation on win
- Score/roll history panel""",

"snake": """Build a COMPLETE, IMMEDIATELY PLAYABLE Snake game: {idea}

60fps Canvas snake game:
- Arrow keys + WASD to control snake direction
- Grid-based movement (30×30 grid)
- Food: regular (green), golden (star, 5×points), power-up (lightning)
- Particle burst when eating food
- Speed increases every 5 food eaten
- High score in localStorage
- Neon glow aesthetic (snake glows, food glows)
- Start screen, pause (Space), game over screen with restart
- Mobile swipe support
- Score combo multiplier""",

"tetris": """Build COMPLETE, PLAYABLE Tetris: {idea}

FULL Tetris implementation:
- 10×20 board, all 7 tetrominoes with SRS rotation
- Arrow keys (move), Up (rotate), Space (hard drop), P (pause)
- Ghost piece (drop preview)
- Hold piece (Shift key)
- Next 3 pieces preview panel
- 7-bag randomizer
- Scoring: 1/2/3/4 line clears = 100/300/500/800 × level
- T-Spin bonus detection
- Line clear animation flash
- Level progression (speed increases)
- High score localStorage
- Mobile on-screen buttons
- Neon colors per piece type""",

"gravity": """Build COMPLETE, PLAYABLE physics/gravity game: {idea}

60fps physics game:
- Click/Space/Tap: jump or flip gravity
- Physical player with gravity, velocity, mass
- Procedural obstacles (pillar pairs with gaps)
- 3-layer parallax background (stars, shapes, foreground)
- Particle trail behind player
- Lives system (3 lives)
- Distance score counter
- High score localStorage
- Power-ups: shield, slow-motion
- Screen shake on collision
- Mobile tap support
- Neon aesthetic with glow effects""",

"more": """Build a COMPLETE, FULLY INTERACTIVE application: {idea}

Create a beautiful, feature-rich web app (React + Tailwind via CDN):
- All core features functional using JS + localStorage
- Dark glassmorphism UI
- At least 5 major features fully implemented
- Realistic sample/demo data (no placeholder lorem ipsum)
- Smooth animations and micro-interactions
- Mobile responsive
- Toast notifications for all user actions
- Loading states, empty states, error states all present
- Search/filter functionality where applicable
- The user should be able to actually USE this app without any backend"""
}

def get_preview_prompt(category: str, idea: str) -> str:
    u = idea.lower()
    if category == "game":
        if "chess" in u: return CATEGORY_PROMPTS["chess"].format(idea=idea)
        if "ludo" in u: return CATEGORY_PROMPTS["ludo"].format(idea=idea)
        if "snake" in u: return CATEGORY_PROMPTS["snake"].format(idea=idea)
        if "tetris" in u: return CATEGORY_PROMPTS["tetris"].format(idea=idea)
        if "gravity" in u: return CATEGORY_PROMPTS["gravity"].format(idea=idea)
        if "shooter" in u: return CATEGORY_PROMPTS["shooter"].format(idea=idea)
    template = CATEGORY_PROMPTS.get(category, CATEGORY_PROMPTS["more"])
    return template.format(idea=idea)


def run_preview_agent(user_input: str, category: str = "more",
                      context_code: str = "", plan: dict = None) -> str:
    """
    Generate a FULLY INTERACTIVE, self-contained HTML preview.
    Works 100% in browser — no backend server needed.
    Like Lovable AI / v0.dev.
    """
    print(f"\n🎨 LOVABLE PREVIEW AGENT: Generating for '{user_input}' [{category}]...")

    base_prompt = get_preview_prompt(category, user_input)

    context_hint = ""
    if context_code and len(context_code) > 100:
        snippet = context_code[:4000]
        context_hint = f"""
CONTEXT (from generated code — use this as reference for features/data):
{snippet}
Extract: feature names, data fields, UI sections, color scheme from this code
and replicate them in the interactive preview.
"""

    full_prompt = f"""{base_prompt}

{context_hint}

CRITICAL OUTPUT RULES:
1. Return ONLY raw HTML starting with <!DOCTYPE html>
2. ZERO markdown fences (no ```html), ZERO explanations
3. Fully self-contained — works in <iframe sandbox="allow-scripts allow-same-origin allow-forms">
4. All sample data hardcoded in JS (no fetch() to localhost)
5. Every single button and interaction MUST WORK immediately
6. Beautiful dark glassmorphism design (#070B14 base)
7. Google Fonts: @import Inter or Poppins or Outfit
8. CDN only for libraries (React, Tailwind, Chart.js, Lucide — all via CDN)

Build the complete interactive preview for: {user_input}
"""

    html = get_llm_response(
        prompt=full_prompt,
        task_type="code",
        max_tokens=20000,
        system=PREVIEW_SYSTEM,
        temperature=0.15
    )

    if not html:
        return _fallback_preview(user_input, category)

    # Clean markdown fences
    html = re.sub(r"^```html\s*", "", html.strip(), flags=re.IGNORECASE)
    html = re.sub(r"^```\s*", "", html.strip())
    html = re.sub(r"```\s*$", "", html.strip())
    html = html.strip()

    # Find DOCTYPE start
    for marker in ["<!DOCTYPE", "<!doctype", "<html"]:
        idx = html.find(marker)
        if idx != -1:
            html = html[idx:]
            break

    # Remove broken src attributes
    html = re.sub(r'alert\s*\([^)]*\)\s*;?', 'console.log("toast")', html)

    print(f"  ✅ Lovable preview: {len(html):,} chars")
    return html


def _fallback_preview(idea: str, category: str) -> str:
    """Emergency fallback — at minimum show a working skeleton UI."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{idea}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #070B14; color: #e2e8f0; font-family: 'Inter', sans-serif;
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 100vh; gap: 24px; padding: 24px; }}
  .card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; padding: 40px; text-align: center; max-width: 500px;
    backdrop-filter: blur(20px); }}
  h1 {{ font-size: 1.8rem; font-weight: 700; background: linear-gradient(135deg,#6C63FF,#FF6B9D);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; }}
  p {{ color: #94a3b8; line-height: 1.6; }}
  .badge {{ display: inline-block; background: rgba(108,99,255,0.2); color: #a78bfa;
    border: 1px solid rgba(108,99,255,0.3); border-radius: 20px;
    padding: 6px 16px; font-size: 12px; font-weight: 600; margin-top: 16px; }}
  .pulse {{ animation: pulse 2s ease-in-out infinite; }}
  @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:0.5}} }}
</style>
</head>
<body>
  <div class="card">
    <div class="pulse" style="font-size:3rem;margin-bottom:16px">⚡</div>
    <h1>{idea}</h1>
    <p>Your {category} is being generated with 2X token power.<br>
       The interactive preview will appear here shortly.</p>
    <div class="badge">SEADS v14 — IIT Level</div>
  </div>
</body>
</html>"""
