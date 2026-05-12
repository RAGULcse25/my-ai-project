import re
from core.openrouter_llm import call_llm

# ─────────────────────────────────────────
# FIXER AGENT
# Input  : broken code + error message
# Output : fixed code (string)
# ─────────────────────────────────────────

def run_fixer(filename: str, broken_code: str, error_message: str) -> str:
    """
    Takes broken code + error and returns fixed code
    Uses free llama-3-8b-instruct for extreme token efficiency
    """
    
    print(f"    🔧 Fixer Agent working on {filename}...")
    
    prompt = f"""
File: {filename}

Broken Code:
--------------
{broken_code}
--------------

Error Message:
--------------
{error_message[:1000]}
--------------

Fix the code completely. Rules:
- Return ONLY the fixed, complete code
- No explanation, no markdown, no code blocks
- Keep all original logic intact
- Fix ONLY what's causing the error
- Make sure all imports are present

Return the complete fixed code now:
"""
    
    # Use the free model as defined in the cheapest model strategy
    fixed_code = call_llm(
        prompt=prompt,
        model="openrouter/free",
        max_tokens=2000,
        system="You are an expert Python debugger. Return ONLY code, never chat."
    )
    
    # Clean any accidental markdown
    fixed_code = re.sub(r"```[\w]*\n?", "", fixed_code)
    fixed_code = fixed_code.replace("```", "").strip()
    
    return fixed_code
