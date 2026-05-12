# agents/prebuilt_games.py — S.E.A.D.S. v11
# All games are prebuilt = instant, zero LLM tokens, always work

import os
from pathlib import Path

_DIR = Path(__file__).parent.parent / "prebuilt"

def _load(name):
    p = _DIR / name
    if p.exists():
        return p.read_text(encoding="utf-8")
    # Fallback: look in outputs dir
    alt = Path(__file__).parent.parent.parent / "prebuilt" / name
    if alt.exists():
        return alt.read_text(encoding="utf-8")
    return ""


# ── Load all prebuilt games ───────────────────────────────

# Temple Run — loaded from prebuilt/temple_run.html
TEMPLE_RUN_HTML = _load("temple_run.html")

# 3D Car Race — loaded from prebuilt/car_3d_race.html
CAR_3D_HTML = _load("car_3d_race.html")


# ─────────────────────────────────────────────────────────
# CUSTOMIZERS
# ─────────────────────────────────────────────────────────

def customize_temple_run(html: str, answers: dict) -> str:
    """Apply theme/difficulty to Temple Run"""
    if not html: return html
    theme = answers.get("q3","").lower()
    diff  = answers.get("q2","Normal").lower()

    if "easy" in diff:
        html = html.replace("const GRAVITY=0.6","const GRAVITY=0.5")
        html = html.replace("speed=Math.min(12","speed=Math.min(9")
    elif "hard" in diff or "insane" in diff:
        html = html.replace("const GRAVITY=0.6","const GRAVITY=0.7")
        html = html.replace("let speed     = 4","let speed     = 6")

    return html


def customize_car_3d(html: str, answers: dict) -> str:
    """Apply theme/style to 3D Car"""
    if not html: return html
    style = answers.get("q2","Endless highway").lower()
    theme = answers.get("q3","Neon night").lower()

    if "sunny" in theme or "desert" in theme:
        html = html.replace("'#0a0020'","'#1a3a6a'")
        html = html.replace("'#2d1200'","'#ff8c00'")
        html = html.replace("'#1a3a1a'","'#c8a84b'")

    return html


def get_prebuilt(idea: str, answers: dict) -> tuple:
    """
    Returns (html, source_name) for any prebuilt game.
    Returns (None, None) if not a prebuilt game.
    """
    u = idea.lower()

    if any(w in u for w in ["temple run","temple runner","endless run","subway surfer"]):
        html = customize_temple_run(TEMPLE_RUN_HTML, answers)
        return html or None, "prebuilt_temple_run"

    if any(w in u for w in ["3d car","car race","car game","3d race","racing game",
                              "car racing","outrun","highway race"]):
        html = customize_car_3d(CAR_3D_HTML, answers)
        return html or None, "prebuilt_car_3d"

    return None, None

