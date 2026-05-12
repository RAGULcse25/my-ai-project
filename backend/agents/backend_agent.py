from core.openrouter_llm import call_llm
from agents.file_writer import write_file
import os

# ─────────────────────────────────────────
# AGENT 3: BACKEND CODER
# Uses DeepSeek Coder (cheapest + best)
# Token usage: MEDIUM (use templates!)
# ─────────────────────────────────────────

BACKEND_TEMPLATES = {
    "flask_base": """
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# DATABASE SETUP
def init_db():
    conn = sqlite3.connect('app.db')
    # TABLES_HERE
    conn.close()

# ROUTES_HERE

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
""",
    "fastapi_base": """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# ROUTES_HERE

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
"""
}


def generate_backend(
    app_type:     str,
    template_info: dict,
    output_path:  str
) -> str:
    """
    Generate Python backend
    Uses template + small modification = less tokens!
    """
    
    print(f"\n🐍 AGENT 3: Generating backend...")
    
    # Pick framework based on app type
    if "game" in app_type or "real-time" in app_type:
        framework = "flask"
        base = BACKEND_TEMPLATES["flask_base"]
    else:
        framework = "fastapi"
        base = BACKEND_TEMPLATES["fastapi_base"]
    
    # SHORT prompt — template already handles structure!
    prompt = f"""
App: {app_type}
Framework: {framework}
Base template is provided. Fill in ONLY:
1. Database tables SQL
2. API routes (max 5)
3. Business logic

Base:
{base}

Return complete app.py. Be concise. No comments.
"""
    
    backend_code = call_llm(
        prompt,
        model="deepseek/deepseek-chat",
        max_tokens=1000,
        system="Expert Python developer. Write clean, minimal code."
    )
    
    # Write to disk
    backend_path = os.path.join(output_path, "backend")
    os.makedirs(backend_path, exist_ok=True)
    
    write_file(backend_path, "app.py", backend_code)
    
    # Generate requirements.txt (token-free, hardcoded!)
    reqs = {
        "flask": "flask\nflask-cors\nsqlite3\ngunicorn\n",
        "fastapi": "fastapi\nuvicorn\npython-multipart\n"
    }
    write_file(backend_path, "requirements.txt", reqs[framework])
    
    print(f"  ✅ Backend generated at: {backend_path}")
    
    return backend_path
