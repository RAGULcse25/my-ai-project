"""
setup_templates.py
==================
Run this ONCE to:
1. Create proper folder structure in E:\online_template
2. Scan and index all your existing templates
3. Show you what templates are available
4. Fix any naming issues

Run: python setup_templates.py
"""

import os, json, shutil
from pathlib import Path

TEMPLATE_DIR = Path(r"E:\online_template")

# ── Expected folder structure ────────────────────────────────
STRUCTURE = {
    "html": "HTML5UP templates (arcana, forty, hyperspace, etc.)",
    "css":  "Templatemo CSS templates (neural_glass, crypto_vault, etc.)",
    "game": "Game templates and assets (godot, phaser, assets)",
    "apps": "Web app templates (linkedin, dashboard, ecommerce)",
    "ppt":  "Presentation templates",
}

def setup():
    print("="*60)
    print("S.E.A.D.S. Template Setup")
    print("="*60)

    # Create folder structure
    print(f"\n📁 Creating folders in: {TEMPLATE_DIR}")
    for folder, desc in STRUCTURE.items():
        path = TEMPLATE_DIR / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ {folder}/ — {desc}")

    # Scan what's already there
    print(f"\n🔍 Scanning {TEMPLATE_DIR}...")
    all_files = {"html":[], "css":[], "js":[], "other":[]}

    for root, dirs, files in os.walk(TEMPLATE_DIR):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules",".git"]]
        for f in files:
            full = os.path.join(root, f)
            rel  = str(Path(full).relative_to(TEMPLATE_DIR))
            ext  = f.rsplit(".",1)[-1].lower() if "." in f else "other"
            size = os.path.getsize(full)
            if ext in ("html","htm"):
                all_files["html"].append({"file":f,"path":rel,"size":size})
            elif ext == "css":
                all_files["css"].append({"file":f,"path":rel,"size":size})
            elif ext == "js":
                all_files["js"].append({"file":f,"path":rel,"size":size})

    # Report
    print(f"\n📊 Found:")
    print(f"  HTML files : {len(all_files['html'])}")
    print(f"  CSS files  : {len(all_files['css'])}")
    print(f"  JS files   : {len(all_files['js'])}")

    # Show top HTML templates by size
    print(f"\n🏆 Top HTML Templates (by size):")
    sorted_html = sorted(all_files["html"], key=lambda x: x["size"], reverse=True)
    for t in sorted_html[:15]:
        size_kb = t["size"] // 1024
        print(f"  {t['path']:<50} {size_kb:>5} KB")

    # Save index
    index_path = TEMPLATE_DIR / "template_index.json"
    index = {
        "html_templates": [{"path":t["path"],"size":t["size"]} for t in sorted_html],
        "css_count": len(all_files["css"]),
        "js_count":  len(all_files["js"]),
        "total":     len(all_files["html"]) + len(all_files["css"]) + len(all_files["js"]),
    }
    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)
    print(f"\n💾 Index saved: {index_path}")

    # Suggestions
    print(f"\n💡 SETUP TIPS:")
    print(f"""
Your template folders in {TEMPLATE_DIR}:

html/ ← Put html5up-arcana/, html5up-forty/, html5up-hyperspace/ etc. HERE
         (your downloaded HTML5UP folders go here directly)

css/  ← Put templatemo_597_neural_glass/, templatemo_607_glass_admin/ etc. HERE
         (your Templatemo folders go here)

game/ ← Put Godot-Game-Template-main/, Phaser_project/ etc. HERE

apps/ ← Put any social media / dashboard templates HERE

EXAMPLE - after setup your structure should be:
E:\\online_template\\
├── html\\
│   ├── html5up-arcana\\
│   │   ├── index.html  ← S.E.A.D.S. will use this
│   │   └── assets\\
│   ├── html5up-forty\\
│   │   └── index.html
│   └── html5up-hyperspace\\
│       └── index.html
├── css\\
│   ├── templatemo_597_neural_glass\\
│   │   ├── index.html
│   │   └── css\\
│   └── templatemo_609_crypto_vault\\
│       └── index.html
└── game\\
    └── Godot-Game-Template-main\\
""")

    print("="*60)
    print("✅ Setup complete! Restart backend to use templates.")
    print("="*60)

if __name__ == "__main__":
    setup()
