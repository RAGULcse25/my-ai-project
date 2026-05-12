from core.llm_config import get_llm
from core.parallel_llm import run_parallel_agents
from agents.file_writer import create_project_folder, write_all_files
from langchain_core.prompts import PromptTemplate
import re

# ─────────────────────────────────────────
# CODER AGENT
# Input  : plan dict (from planner)
# Output : writes all code files to disk
# ─────────────────────────────────────────

CODE_PROMPT = PromptTemplate(
    input_variables=[
        "project_name",
        "description", 
        "filename",
        "tech_stack",
        "all_files",
        "tasks"
    ],
    template="""
You are S.E.A.D.S. Coder Agent — an expert Python developer.

Project: {project_name}
Description: {description}
Tech Stack: {tech_stack}
All files in project: {all_files}
Tasks: {tasks}

Now write the complete code for: {filename}

Rules:
- Write ONLY the code. No explanation outside comments.
- Include helpful inline comments
- If {filename} is requirements.txt → list only package names, one per line
- If {filename} is README.md → write proper markdown documentation
- Make code production-ready and complete (no placeholders like "# TODO")
- For ML files: use scikit-learn, pandas, numpy
- For API files: use FastAPI with proper routes
- For data files: include sample data loading logic

Write the full {filename} content now:
"""
)


def run_coder(plan: dict) -> str:
    """
    Main coder agent function
    Generates all files in PARALLEL and writes to disk
    Returns: path to project folder
    """
    
    project_name = plan.get("project_name", "my_project")
    files_to_create = plan.get("files_to_create", [])
    
    print(f"\n💻 CODER AGENT: Starting code generation...")
    print(f"📋 Files to generate: {files_to_create}\n")
    
    # Step 1: Create project folder
    folder_path = create_project_folder(project_name)
    
    # Step 2: Prepare parallel tasks
    tech_str = str(plan.get("tech_stack", {}))
    files_str = ", ".join(files_to_create)
    tasks_str = "\n".join(plan.get("tasks", []))
    
    agent_tasks = []
    for filename in files_to_create:
        prompt = CODE_PROMPT.format(
            project_name=project_name,
            description=plan.get("description", ""),
            filename=filename,
            tech_stack=tech_str,
            all_files=files_str,
            tasks=tasks_str
        )
        agent_tasks.append({
            "prompt": prompt,
            "system": "Expert Python developer.",
            "max_tokens": 2500 # Higher for code
        })
    
    # Step 3: Run in parallel
    print(f"  🔨 Generating {len(files_to_create)} files in parallel...")
    responses = run_parallel_agents(agent_tasks)
    
    # Step 4: Clean and map responses
    generated_files = {}
    for i, filename in enumerate(files_to_create):
        raw_code = responses[i]
        
        # Strip markdown code blocks if LLM adds them
        clean_code = re.sub(r"```[\w]*\n?", "", raw_code)
        clean_code = clean_code.replace("```", "").strip()
        
        generated_files[filename] = clean_code
        print(f"  ✅ Generated: {filename} ({len(clean_code)} chars)")
    
    # Step 5: Write all to disk
    print(f"\n💾 Writing files to: {folder_path}")
    write_all_files(folder_path, generated_files)
    
    print(f"\n✅ CODER AGENT DONE!")
    print(f"📂 Project ready at: {folder_path}")
    
    return folder_path
