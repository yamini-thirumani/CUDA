from agents.fix_agent import rootcause_fix
from agents.refactor_agent import run_refactor
from agents.optimizer_agent import run_optimizer
from agents.judge_agent import judge_agent
from agents.model_loader import pipe
import asyncio

def call_agent(prompt, pipe):
    response = pipe(prompt, max_new_tokens=200)

    # DeepSeek returns list of dicts → [{'generated_text': '...'}]
    if isinstance(response, list) and len(response) > 0:
        if isinstance(response[0], dict) and 'generated_text' in response[0]:
            return response[0]['generated_text'].strip()
        else:
            return str(response[0]).strip()

    return str(response).strip()

async def run_all_agents(code: str):
    """Run fix, refactor, and optimize agents in parallel and return the best solution."""
    loop = asyncio.get_event_loop()

    # Run agents concurrently using executor
    fixed_future = loop.run_in_executor(None, rootcause_fix, code, pipe, call_agent)
    refactored_future = loop.run_in_executor(None, run_refactor, code, pipe, call_agent)
    optimized_future = loop.run_in_executor(None, run_optimizer, code, pipe, call_agent)

    # Await results
    fixed_code, refactored_code, optimized_code = await asyncio.gather(
        fixed_future, refactored_future, optimized_future
    )

    versions = {
        "fixed": fixed_code,
        "refactored": refactored_code,
        "optimized": optimized_code,
    }

    # ✅ Log agent outputs for debugging
    print("✅ Agent outputs:")
    print("->Fixed:\n", fixed_code)
    print("->Refactored:\n", refactored_code)
    print("->Optimized:\n", optimized_code)

    # Use the aliased judge agent
    final = judge_agent(versions)

    result = {
        "final_code": final.get("code", ""),
        "winner": final.get("winner", ""),
        "reason": final.get("reason", ""),
        "metrics": final.get("metrics", {}),
        "versions": versions,
        "baseline": code,
    }

    return result
