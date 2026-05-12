# backend/agents/planner.pyfrom core.llm_config import get_llm
from langchain_core.prompts import PromptTemplate
import json
import re

# ─────────────────────────────────────────
# PLANNER AGENT
# Input  : project idea (string)
# Output : structured project plan (dict)
# ─────────────────────────────────────────

PLANNER_PROMPT = PromptTemplate(
    input_variables=["project_idea"],
    template="""
You are S.E.A.D.S. Planner Agent — an expert software architect.

Given this project idea: "{project_idea}"

Return a JSON object with this EXACT structure:
{{
  "project_name": "...",
  "description": "...",
  "tech_stack": {{
    "language": "Python",
    "framework": "FastAPI or Streamlit",
    "ml_library": "scikit-learn / pandas / etc",
    "database": "SQLite or MongoDB",
    "frontend": "Streamlit or React"
  }},
  "files_to_create": [
    "main.py",
    "model.py",
    "data_loader.py",
    "requirements.txt",
    "README.md"
  ],
  "tasks": [
    "Task 1: Load and clean dataset",
    "Task 2: Train ML model",
    "Task 3: Build API endpoint",
    "Task 4: Create frontend UI",
    "Task 5: Write documentation"
  ],
  "dataset_suggestion": "...",
  "deployment_target": "Streamlit Cloud or Render"
}}

Return ONLY valid JSON. No explanation. No extra text.
"""
)

def run_planner(project_idea: str) -> dict:
    llm = get_llm()
    chain = PLANNER_PROMPT | llm
    
    print(f"\n🧠 PLANNER AGENT: Analyzing '{project_idea}'...")
    
    response = chain.invoke({"project_idea": project_idea})
    raw_output = response.content
    
    # Clean and parse JSON safely
    try:
        # Remove markdown code blocks if present
        clean = re.sub(r"```json|```", "", raw_output).strip()
        plan = json.loads(clean)
        print("✅ Plan generated successfully!")
        return plan
    except json.JSONDecodeError:
        print("⚠️ JSON parse failed. Raw output:")
        print(raw_output)
        return {}

if __name__ == "__main__":
    idea = input("💡 Enter your project idea: ")
    plan = run_planner(idea)
    
    if plan:
        print("\n" + "="*50)
        print("📋 PROJECT PLAN:")
        print("="*50)
        print(json.dumps(plan, indent=2))
