# agents/devops_agent.py — S.E.A.D.S. v15
# ============================================================
# DEVOPS AGENT — generates Firebase + Vercel deploy configs
# Also generates: ZIP manifest, Dockerfile, CLI commands
# Model: gemini-2.0-flash (free, lightweight config generation)
# ============================================================

import os, json
from dotenv import load_dotenv
load_dotenv()

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "multi-agent-bb44e")
VERCEL_TOKEN        = os.getenv("VERCEL_TOKEN", "")
FIREBASE_TOKEN      = os.getenv("FIREBASE_TOKEN", "")
ONLINE_APP_DIR      = os.getenv("ONLINE_APP_DIR", r"E:\seads\online_app")


def generate_deploy_config(slug: str, category: str) -> str:
    """
    Returns a JSON string with all deploy configs.
    Called by Orchestrator after Verifier passes.
    """
    project_path = os.path.join(ONLINE_APP_DIR, slug)
    is_react = category in ("ecommerce",)  # Future: Next.js outputs

    config = {
        "slug": slug,
        "category": category,
        "local_path": project_path,
        "local_url": f"http://localhost:8000/online_app/{slug}/",

        # ── Firebase (HTML projects) ────────────────────────
        "firebase": {
            "project_id": FIREBASE_PROJECT_ID,
            "estimated_url": f"https://{FIREBASE_PROJECT_ID}.web.app",
            "firebase_json": {
                "hosting": {
                    "public": ".",
                    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
                    "rewrites": [{"source": "**", "destination": "/index.html"}],
                    "headers": [{
                        "source": "**/*.@(js|css)",
                        "headers": [{"key": "Cache-Control", "value": "max-age=31536000"}]
                    }]
                }
            },
            "cli_commands": [
                f"cd {project_path}",
                f"firebase use {FIREBASE_PROJECT_ID}",
                "firebase deploy --only hosting",
            ],
            "env_check": bool(FIREBASE_TOKEN),
        },

        # ── Vercel (React/Next.js projects) ─────────────────
        "vercel": {
            "estimated_url": f"https://{slug}.vercel.app",
            "vercel_json": {
                "version": 2,
                "builds": [{"src": "index.html", "use": "@vercel/static"}] if not is_react else [
                    {"src": "package.json", "use": "@vercel/next"}
                ],
                "routes": [{"src": "/(.*)", "dest": "/index.html"}],
            },
            "cli_commands": [
                f"cd {project_path}",
                "vercel --prod --yes",
            ],
            "env_check": bool(VERCEL_TOKEN),
        },

        # ── Dockerfile (optional) ────────────────────────────
        "dockerfile": _generate_dockerfile(slug),
    }

    return json.dumps(config, indent=2)


def _generate_dockerfile(slug: str) -> str:
    return f"""FROM nginx:alpine
COPY . /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""


def write_firebase_json(slug: str) -> str:
    """Write firebase.json to the output folder."""
    project_path = os.path.join(ONLINE_APP_DIR, slug)
    os.makedirs(project_path, exist_ok=True)

    firebase_config = {
        "hosting": {
            "public": ".",
            "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
            "rewrites": [{"source": "**", "destination": "/index.html"}],
        }
    }
    path = os.path.join(project_path, "firebase.json")
    with open(path, "w") as f:
        json.dump(firebase_config, f, indent=2)

    # Also write .firebaserc
    firebaserc = {"projects": {"default": FIREBASE_PROJECT_ID}}
    with open(os.path.join(project_path, ".firebaserc"), "w") as f:
        json.dump(firebaserc, f, indent=2)

    return path


def write_vercel_json(slug: str) -> str:
    """Write vercel.json to the output folder."""
    project_path = os.path.join(ONLINE_APP_DIR, slug)
    os.makedirs(project_path, exist_ok=True)

    vercel_config = {
        "version": 2,
        "builds": [{"src": "index.html", "use": "@vercel/static"}],
        "routes": [{"src": "/(.*)", "dest": "/index.html"}],
    }
    path = os.path.join(project_path, "vercel.json")
    with open(path, "w") as f:
        json.dump(vercel_config, f, indent=2)
    return path


def prepare_deploy_files(slug: str, category: str) -> dict:
    """
    Write all deploy config files to the output folder.
    Called after a successful build.
    Returns dict with paths and CLI commands.
    """
    fb_path  = write_firebase_json(slug)
    vcl_path = write_vercel_json(slug)
    project_path = os.path.join(ONLINE_APP_DIR, slug)

    return {
        "firebase_json": fb_path,
        "vercel_json":   vcl_path,
        "firebase_cmd":  f'firebase deploy --only hosting --project {FIREBASE_PROJECT_ID}',
        "vercel_cmd":    "vercel --prod --yes",
        "local_url":     f"http://localhost:8000/online_app/{slug}/",
        "firebase_url":  f"https://{FIREBASE_PROJECT_ID}.web.app",
        "vercel_url":    f"https://{slug}.vercel.app",
        "project_path":  project_path,
    }
