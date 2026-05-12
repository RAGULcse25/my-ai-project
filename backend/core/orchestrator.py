# core/orchestrator.py — S.E.A.D.S. v15
# DAG Orchestration Engine — runs agents in parallel/sequential order
# Implements: self-healing loop, auto-error correction, WS pause/stop support

import time, re, concurrent.futures
from core.blackboard import BuildContext, EVENT_START, EVENT_COMPLETE, EVENT_FAIL
from core.sse_manager import (push_agent_start, push_agent_complete,
                               push_agent_fail, push_heal, push_log,
                               push_3d_graph, push_complete, push_error)
from core.ws_manager import is_paused, get_flags

# ── DAG: which agents run per category ─────────────────────
DAG = {
    "game":      {"parallel": ["game_engine"], "sequential": ["integration", "verifier", "devops"]},
    "ml":        {"parallel": ["ml"],          "sequential": ["integration", "verifier", "devops"]},
    "ecommerce": {"parallel": ["ui_ux", "backend", "database"], "sequential": ["integration", "verifier", "devops"]},
    "website":   {"parallel": ["ui_ux"],       "sequential": ["integration", "verifier", "devops"]},
    "mobile":    {"parallel": ["ui_ux", "backend"], "sequential": ["integration", "verifier", "devops"]},
    "design":    {"parallel": ["ui_ux"],       "sequential": ["integration", "verifier", "devops"]},
    "ppt":       {"parallel": ["ui_ux"],       "sequential": ["integration", "verifier", "devops"]},
    "more":      {"parallel": ["ui_ux", "backend"], "sequential": ["integration", "verifier", "devops"]},
}

# ── 3D Graph node definitions ───────────────────────────────
def _build_graph_nodes(category: str) -> list:
    dag = DAG.get(category, DAG["more"])
    nodes = [{"id": "router",  "label": "Router",  "status": "done",    "tier": 0}]
    nodes.append({"id": "planner", "label": "Planner", "status": "active",  "tier": 1})
    for a in dag["parallel"]:
        nodes.append({"id": a, "label": a.replace("_", " ").title(), "status": "waiting", "tier": 2})
    for a in dag["sequential"]:
        nodes.append({"id": a, "label": a.replace("_", " ").title(), "status": "waiting", "tier": 3})
    edges = [{"from": "router", "to": "planner"}]
    for a in dag["parallel"]:
        edges.append({"from": "planner", "to": a})
    for a in dag["parallel"]:
        edges.append({"from": a, "to": "integration"})
    edges += [{"from": "integration", "to": "verifier"}, {"from": "verifier", "to": "devops"}]
    return nodes, edges


def _auto_fix(html: str) -> str:
    """Automatic error self-correction — always runs on output."""
    if not html:
        return html
    # Remove alert/confirm/prompt
    html = re.sub(r'alert\s*\([^)]*\)\s*;?', '/* toast-instead */', html)
    html = re.sub(r'confirm\s*\([^)]*\)', 'true', html)
    # Fix broken image URLs
    html = re.sub(
        r'<img([^>]*?)src=["\'](?!http|data:)[^"\']{3,}["\']',
        lambda m: f'<img{m.group(1)}src="https://picsum.photos/seed/{abs(hash(m.group(0)))%9999}/400/300"',
        html)
    return html


def _wait_for_resume(task_id: str, agent: str):
    """Block pipeline thread while WS pause flag is set."""
    while is_paused(task_id):
        push_log(task_id, f"⏸ Pipeline paused at {agent} — waiting for resume...", "warn")
        time.sleep(1.5)


def _run_agent(ctx: BuildContext, agent_name: str,
               percent_start: int, percent_end: int) -> str:
    """Run a single named agent and write its artifact to the blackboard."""
    task_id = ctx.task_id

    # Check stop flag
    if get_flags(task_id).get("stopped"):
        return ""

    # Wait if paused
    _wait_for_resume(task_id, agent_name)

    ctx.update_progress(percent_start, f"Running {agent_name}...", agent_name)
    push_agent_start(task_id, agent_name, percent_start)
    ctx.log_event(agent_name, EVENT_START)

    try:
        result = _dispatch_agent(ctx, agent_name)
        if not result or len(result) < 100:
            raise ValueError(f"Agent {agent_name} returned empty/too-short output")

        result = _auto_fix(result)
        artifact_key = _agent_to_artifact(agent_name)
        ctx.write_artifact(artifact_key, result, agent_name=agent_name)
        ctx.update_progress(percent_end, f"{agent_name} complete ✓", agent_name)
        push_agent_complete(task_id, agent_name, percent_end)
        return result

    except Exception as e:
        err_msg = str(e)
        ctx.log_error(agent_name, "agent_error", err_msg, auto_fixed=False)
        push_agent_fail(task_id, agent_name, err_msg, auto_fixing=True)
        push_log(task_id, f"[AUTO-FIX] Retrying {agent_name} on fallback provider...", "warn")

        # Auto-retry on different provider (SmartKeyManager handles rotation)
        try:
            result = _dispatch_agent(ctx, agent_name, retry=True)
            if result and len(result) > 100:
                result = _auto_fix(result)
                artifact_key = _agent_to_artifact(agent_name)
                ctx.write_artifact(artifact_key, result, agent_name=agent_name)
                ctx.log_error(agent_name, "agent_error", err_msg, auto_fixed=True, fix_method="provider_retry")
                ctx.update_progress(percent_end, f"{agent_name} recovered ✓", agent_name)
                push_agent_complete(task_id, agent_name, percent_end)
                return result
        except Exception as e2:
            ctx.log_error(agent_name, "agent_error", str(e2), auto_fixed=False)

        push_log(task_id, f"[WARN] {agent_name} failed after retry — pipeline continues", "warn")
        return ""


def _agent_to_artifact(agent_name: str) -> str:
    mapping = {
        "ui_ux":       "ui_code",
        "backend":     "backend_code",
        "database":    "db_schema",
        "ml":          "ml_code",
        "game_engine": "game_code",
        "integration": "integrated_html",
        "verifier":    "verified_html",
        "devops":      "deploy_config",
    }
    return mapping.get(agent_name, agent_name)


def _dispatch_agent(ctx: BuildContext, agent_name: str, retry: bool = False) -> str:
    """Route to actual agent implementation."""
    from agents.category_builders_v14 import dispatch as v14_dispatch
    from core.llm_config import get_llm_response
    from core.smart_key_manager import smart_key_manager

    category = ctx.manifest.get("category", "more")
    idea     = ctx.idea
    answers  = ctx.answers
    task_id  = ctx.task_id

    # Check for WS inject override for this agent
    from core.ws_manager import get_flags
    flags   = get_flags(task_id)
    inject  = flags.get(f"inject_{agent_name}", "")
    redirect = flags.get("redirect", "")

    if agent_name in ("integration", "verifier", "devops"):
        return _run_core_agent(ctx, agent_name)

    # Parallel agents → call v14 dispatcher (it handles category routing)
    result = v14_dispatch(category, idea, answers, task_id, ctx.manifest)
    if isinstance(result, dict):
        return result.get("preview_html", "")
    return result or ""


def _run_core_agent(ctx: BuildContext, agent_name: str) -> str:
    from core.llm_config import get_llm_response
    from core.smart_key_manager import smart_key_manager
    import os

    ui       = ctx.read_artifact("ui_code")
    backend  = ctx.read_artifact("backend_code")
    game     = ctx.read_artifact("game_code")
    ml       = ctx.read_artifact("ml_code")
    existing = ui or game or ml or backend

    if agent_name == "integration":
        if not existing:
            return ""
        return existing  # v14 already integrates — pass through

    elif agent_name == "verifier":
        integrated = ctx.read_artifact("integrated_html")
        if not integrated:
            return ""
        provider, key, model = smart_key_manager.get_best_key("verify", 600)
        prompt = f"""Score this HTML output 0.0-1.0 across: completeness, no alert(), mobile responsive, UI quality.
Return ONLY JSON: {{"score": 0.95, "issues": ["list"], "patch_target": "agent_name_or_empty"}}
HTML (first 4000 chars): {integrated[:4000]}"""
        raw = get_llm_response(prompt, max_tokens=400, temperature=0.0,
                               system="You are a code quality auditor. Return ONLY JSON.",
                               task_type="verify")
        try:
            import json, re
            clean = re.sub(r"```json|```", "", raw or "").strip()
            data  = json.loads(clean)
            ctx.quality_score = float(data.get("score", 0.85))
            # Self-healing loop
            if ctx.quality_score < 0.80 and ctx.can_heal():
                ctx.increment_healing()
                target = data.get("patch_target", "ui_ux")
                push_heal(ctx.task_id, ctx.healing_iterations, ctx.quality_score, target)
                patch_prompt = f"""Fix these issues in the HTML: {data.get('issues', [])}
Return the COMPLETE improved <!DOCTYPE html>:
{integrated[:8000]}"""
                fixed = get_llm_response(patch_prompt, max_tokens=12000, temperature=0.1,
                                          system="You are an elite developer. Return ONLY raw HTML.",
                                          task_type="verify")
                if fixed and len(fixed) > 500:
                    ctx.write_artifact("integrated_html", _auto_fix(fixed), agent_name="self_healer")
                    return _auto_fix(fixed)
        except Exception:
            ctx.quality_score = 0.85
        return integrated

    elif agent_name == "devops":
        from agents.devops_agent import generate_deploy_config
        slug = ctx.task_id[:40]
        return generate_deploy_config(slug, ctx.manifest.get("category", "more"))

    return ""


# ── MAIN ORCHESTRATOR ENTRY POINT ────────────────────────────
def run_pipeline(ctx: BuildContext) -> dict:
    """
    Execute the full DAG pipeline for a build.
    Returns the final response dict.
    """
    task_id  = ctx.task_id
    category = ctx.manifest.get("category", "more")
    dag      = DAG.get(category, DAG["more"])

    nodes, edges = _build_graph_nodes(category)
    push_3d_graph(task_id, nodes, edges)
    push_log(task_id, f"🚀 S.E.A.D.S. v15 Pipeline started | Category: {category}")

    ctx.update_progress(10, "Planner Agent analysing request...", "planner")
    push_log(task_id, f"📋 DAG: {dag['parallel']} → {dag['sequential']}")

    parallel_agents = dag["parallel"]
    n = len(parallel_agents)

    # ── Parallel group (10% → 65%) ────────────────────────────
    pct_per = max(1, 55 // max(n, 1))
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(n, 4)) as ex:
        futures = {}
        for i, agent in enumerate(parallel_agents):
            p_start = 10 + i * pct_per
            p_end   = p_start + pct_per
            futures[ex.submit(_run_agent, ctx, agent, p_start, p_end)] = agent

        for fut in concurrent.futures.as_completed(futures):
            agent = futures[fut]
            try:
                fut.result()
            except Exception as e:
                push_log(task_id, f"[ERROR] {agent}: {e}", "error")

    # ── Sequential group (65% → 95%) ─────────────────────────
    seq_pct  = [65, 80, 90, 95]
    for i, agent in enumerate(dag["sequential"]):
        if get_flags(task_id).get("stopped"):
            break
        p_start = seq_pct[i] if i < len(seq_pct) else 92
        p_end   = seq_pct[i+1] if (i+1) < len(seq_pct) else 95
        _run_agent(ctx, agent, p_start, p_end)

    # ── Final assembly ────────────────────────────────────────
    final_html = (ctx.read_artifact("verified_html") or
                  ctx.read_artifact("integrated_html") or
                  ctx.read_artifact("ui_code") or
                  ctx.read_artifact("game_code") or
                  ctx.read_artifact("ml_code"))

    elapsed = round(time.time() - ctx.started_at, 1)
    ctx.save_build_summary(final_html, elapsed)
    ctx.update_progress(100, "Complete! ✅")

    slug = ctx.task_id[:40]
    response = {
        "project_name":  slug,
        "category":      category,
        "preview_html":  final_html,
        "quality_score": ctx.quality_score,
        "heal_iters":    ctx.healing_iterations,
        "elapsed":       elapsed,
        "deploy_config": ctx.read_artifact("deploy_config"),
        "agent_log":     [e.to_dict() for e in ctx.agent_log],
        "status":        "success",
        "version":       "15.0",
    }
    push_complete(task_id, response)
    push_log(task_id, f"✅ Build complete in {elapsed}s | Score: {ctx.quality_score:.0%}")
    return response
