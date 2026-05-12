import concurrent.futures
from core.llm_config import get_llm_response

# ─────────────────────────────────────────
# PARALLEL LLM CALLER
# Run multiple agents simultaneously!
# Each uses different key = max speed!
# ─────────────────────────────────────────

def run_parallel_agents(agent_tasks: list) -> list:
    """
    Run multiple LLM calls in parallel
    
    agent_tasks = [
        {"prompt": "...", "model": "...", "max_tokens": 500, "system": "..."},
        {"prompt": "...", "model": "...", "max_tokens": 800},
        ...
    ]
    
    Returns: list of responses in same order
    """
    
    print(f"\n⚡ Running {len(agent_tasks)} agents in PARALLEL...")
    
    results = [None] * len(agent_tasks)
    
    def call_agent(index: int, task: dict) -> tuple:
        response = get_llm_response(
            prompt     = task.get("prompt", ""),
            model      = task.get("model", "llama-3.3-70b-versatile"),
            max_tokens = task.get("max_tokens", 800),
            system     = task.get("system", "Be concise."),
            temperature = task.get("temperature", 0.2)
        )
        return index, response
    
    # Run all in parallel using ThreadPool
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=min(len(agent_tasks), 10) # Limit workers
    ) as executor:
        
        futures = [
            executor.submit(call_agent, i, task)
            for i, task in enumerate(agent_tasks)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            idx, response = future.result()
            results[idx] = response
            print(f"  ✅ Agent {idx+1} done!")
    
    return results
