import os
import git
import requests
import time
from dotenv import load_dotenv
from core.logger import log_event

load_dotenv()

# ─────────────────────────────────────────
# DEPLOYER AGENT
# Input  : project folder path + plan dict
# Output : GitHub URL + Render deploy URL
# ─────────────────────────────────────────

GITHUB_TOKEN    = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "ragulcse25")
RENDER_API_KEY  = os.getenv("RENDER_API_KEY")

GITHUB_API = "https://api.github.com"


# ══════════════════════════════════════════
# PART 1 — GITHUB
# ══════════════════════════════════════════

def create_github_repo(repo_name: str, description: str) -> str:
    """
    Creates a new GitHub repo via API
    Returns: repo URL
    """
    
    print(f"\n🐙 Creating GitHub repo: {repo_name}...")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": False
    }
    
    response = requests.post(
        f"{GITHUB_API}/user/repos",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 201:
        repo_url = response.json()["html_url"]
        clone_url = response.json()["clone_url"]
        print(f"  ✅ Repo created: {repo_url}")
        return clone_url
    
    elif response.status_code == 422:
        # Repo already exists
        clone_url = f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
        print(f"  ⚠️  Repo already exists. Using: {clone_url}")
        return clone_url
    
    else:
        print(f"  ❌ GitHub error: {response.json()}")
        return ""


def push_to_github(folder_path: str, repo_name: str, clone_url: str) -> bool:
    """
    Git init → add → commit → push
    Returns True if successful
    """
    
    print(f"\n📤 Pushing code to GitHub...")
    
    try:
        # ── Init repo ──────────────────────
        repo = git.Repo.init(folder_path)
        
        # ── Configure git identity ─────────
        repo.config_writer().set_value(
            "user", "name", "S.E.A.D.S. Bot"
        ).release()
        repo.config_writer().set_value(
            "user", "email", "seads@bot.ai"
        ).release()
        
        # ── Create .gitignore ──────────────
        gitignore_path = os.path.join(folder_path, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("__pycache__/\n*.pyc\n.env\n*.egg-info/\ndist/\n")
        
        # ── Stage all files ────────────────
        repo.git.add(A=True)
        
        # ── Commit ─────────────────────────
        commit_msg = f"🤖 S.E.A.D.S. Auto-generated: {repo_name}"
        repo.index.commit(commit_msg)
        print(f"  ✅ Committed: '{commit_msg}'")
        
        # ── Add remote ─────────────────────
        # Inject token into URL for auth
        auth_url = clone_url.replace(
            "https://",
            f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@"
        )
        
        # Remove existing remote if any
        if "origin" in [r.name for r in repo.remotes]:
            repo.delete_remote("origin")
        
        origin = repo.create_remote("origin", auth_url)
        
        # ── Push ───────────────────────────
        origin.push(refspec="HEAD:main")
        
        public_url = clone_url.replace(".git", "")
        print(f"  ✅ Pushed to: {public_url}")
        
        log_event("GITHUB_PUSH", {
            "repo": repo_name,
            "url": public_url,
            "success": True
        })
        
        return public_url
    
    except Exception as e:
        print(f"  ❌ Git push failed: {e}")
        log_event("GITHUB_PUSH", {"repo": repo_name, "error": str(e)})
        return ""


# ══════════════════════════════════════════
# PART 2 — RENDER DEPLOY
# ══════════════════════════════════════════

def create_render_service(
    repo_name: str,
    github_url: str,
    plan: dict
) -> str:
    """
    Triggers Render deploy via API
    Returns: deployed app URL
    """
    
    if not RENDER_API_KEY:
        print("\n⚠️  No Render API key. Skipping auto-deploy.")
        print(f"  👉 Manual deploy: render.com → New → Web Service")
        print(f"  👉 Connect repo : {github_url}")
        return ""
    
    print(f"\n🚀 Deploying to Render...")
    
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Detect start command from tech stack
    tech = plan.get("tech_stack", {})
    framework = tech.get("framework", "").lower()
    
    if "streamlit" in framework:
        start_cmd = "streamlit run main.py --server.port $PORT"
    elif "fastapi" in framework:
        start_cmd = "uvicorn main:app --host 0.0.0.0 --port $PORT"
    else:
        start_cmd = "python main.py"
    
    payload = {
        "type": "web_service",
        "name": repo_name,
        "env": "python",
        "repo": github_url,
        "branch": "main",
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": start_cmd,
        "plan": "free"
    }
    
    response = requests.post(
        "https://api.render.com/v1/services",
        json=payload,
        headers=headers
    )
    
    if response.status_code in [200, 201]:
        service = response.json()
        service_url = f"https://{service.get('service', {}).get('slug', repo_name)}.onrender.com"
        print(f"  ✅ Render service created!")
        print(f"  🌐 Deploy URL: {service_url}")
        print(f"  ⏳ Build in progress (~3-5 mins)...")
        
        log_event("RENDER_DEPLOY", {
            "repo": repo_name,
            "url": service_url,
            "success": True
        })
        
        return service_url
    else:
        print(f"  ❌ Render error: {response.text}")
        return ""


# ══════════════════════════════════════════
# MAIN DEPLOYER FUNCTION
# ══════════════════════════════════════════

def run_deployer(folder_path: str, plan: dict) -> dict:
    """
    Full deployment pipeline
    Returns dict with github_url and deploy_url
    """
    
    print(f"\n🚀 DEPLOYER AGENT: Starting deployment...")
    
    project_name = plan.get("project_name", "my_project")
    description  = plan.get("description", "Built by S.E.A.D.S.")
    
    # Clean repo name (GitHub format)
    repo_name = project_name.lower()\
        .replace(" ", "-")\
        .replace("_", "-")
    
    result = {
        "github_url": "",
        "deploy_url": "",
        "repo_name" : repo_name
    }
    
    # ── Step 1: Create GitHub Repo ─────────
    clone_url = create_github_repo(repo_name, description)
    if not clone_url:
        print("❌ GitHub repo creation failed.")
        return result
    
    # ── Step 2: Push Code ──────────────────
    github_url = push_to_github(folder_path, repo_name, clone_url)
    if not github_url:
        print("❌ GitHub push failed.")
        return result
    
    result["github_url"] = github_url
    
    # ── Step 3: Deploy to Render ───────────
    deploy_url = create_render_service(repo_name, github_url, plan)
    result["deploy_url"] = deploy_url
    
    return result
