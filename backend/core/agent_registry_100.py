# core/agent_registry_100.py — S.E.A.D.S. Multi-Agent Ecosystem (v14)
# ============================================================

# -- The 4 Core Agent Types (Standard Pipeline)
CORE_AGENTS = {
    "search": {
        "name": "Perplexity Sonar",
        "role": "Search Agent (RAG)",
        "desc": "Real-time research on UI/UX trends, technology stacks, and market best practices."
    },
    "plan": {
        "name": "DeepSeek-R1",
        "role": "Planning Agent (Logic)",
        "desc": "Architectural decomposition, logic flow mapping, and multi-file dependency planning."
    },
    "code": {
        "name": "DeepSeek V3 / Qwen 2.5",
        "role": "Coding Agent (Implementation)",
        "desc": "High-speed implementation in React + Tailwind + Shadcn or Python (Kivy/BeeWare)."
    },
    "verify": {
        "name": "Claude 3 Opus",
        "role": "Verify Agent (Quality)",
        "desc": "Rigorous code verification, security auditing, and iterative UX/UI refinement."
    }
}

# -- Category-Specific Builder Specialists
BUILDER_SPECIALISTS = {
    "website":   {"role": "React Web Architect", "stack": ["React", "Tailwind CSS", "Shadcn UI"]},
    "mobile":    {"role": "Python Mobile Expert", "stack": ["Kivy", "BeeWare", "Python"]},
    "design":    {"role": "CV/Graphics Engineer", "stack": ["OpenCV", "Pillow", "Albumentations"]},
    "ppt":       {"role": "Presentation Specialist", "stack": ["python-pptx", "Marp", "Manim"]},
    "game":      {"role": "Game Engine Specialist", "stack": ["Phaser", "Three.js", "Canvas API"]},
    "ml":        {"role": "Data Science Expert", "stack": ["Scikit-learn", "PyTorch", "LangChain"]},
    "ecommerce": {"role": "Full-Stack Retail Expert", "stack": ["React", "Node.js", "MongoDB", "Stripe"]},
    "more":      {"role": "General Asset Builder", "stack": ["Any"]}
}

# Mapping legacy team names to new architecture for UI compatibility
TEAMS = {
    "Orchestration": ["plan"],
    "Research":      ["search"],
    "Coding":        ["code"],
    "Quality":       ["verify"],
    "Builders":      list(BUILDER_SPECIALISTS.keys())
}

# Compatibility Shims for main.py logs
AGENTS_100 = {k: {"role": v["role"], "team": "Builders", "tokens": 10000} for k, v in BUILDER_SPECIALISTS.items()}
AGENTS_100.update({k: {"role": v["role"], "team": "Core", "tokens": 10000} for k, v in CORE_AGENTS.items()})

def get_pipeline(category):
    # Standard v14 pipeline: Search -> Plan -> Code -> Verify
    return {
        "parallel": ["Search Agent"],
        "sequential": ["Planning Agent", "Coding Agent"],
        "quality": ["Verify Agent"]
    }

def get_agent_info(agent_key):
    return CORE_AGENTS.get(agent_key) or BUILDER_SPECIALISTS.get(agent_key)

def total_agents():
    return len(CORE_AGENTS) + len(BUILDER_SPECIALISTS)
