import ast
import json
import re
from typing import Dict, Tuple, List

try:
    # Reuse the already loaded model pipeline
    from agents.model_loader import pipe
except Exception:
    pipe = None


def _safe_json_extract(text: str):
    try:
        # Try direct load first
        return json.loads(text)
    except Exception:
        # Fallback: extract the largest {...} block
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            candidate = text[first:last + 1]
            try:
                return json.loads(candidate)
            except Exception:
                pass
    return None


def _score_code_heuristic(code: str) -> Tuple[int, List[str]]:
    score = 0
    reasons: List[str] = []

    # Syntax validity
    try:
        ast.parse(code)
        score += 5
        reasons.append("Parses without syntax errors")
    except SyntaxError as e:
        # Provide more specific syntax error information
        error_msg = str(e)
        if "invalid syntax" in error_msg:
            # Try to extract line number and provide more context
            if "line" in error_msg:
                reasons.append(f"Syntax error on {error_msg}")
            else:
                reasons.append("Contains syntax errors that prevent execution")
        else:
            reasons.append(f"Syntax error: {error_msg}")
        # Heavy penalty; still allow comparison if others also fail
        score -= 5
    except Exception as e:
        reasons.append("Code parsing failed")
        # Heavy penalty; still allow comparison if others also fail
        score -= 5

    # Robustness: try/except
    if "try" in code and "except" in code:
        score += 2
        reasons.append("Has try/except error handling")

    # Functions present
    if "def " in code:
        score += 1
        reasons.append("Defines functions")

    # Type hints / return annotations
    if "->" in code:
        score += 1
        reasons.append("Uses return type hints")

    # Docstrings
    if '"""' in code or "'''" in code:
        score += 1
        reasons.append("Has docstrings")

    # Comments
    comment_lines = sum(1 for line in code.splitlines() if line.strip().startswith('#'))
    if comment_lines > 0:
        score += 1
        reasons.append("Includes comments")

    # Length (conciseness vs verbosity)
    num_lines = len(code.splitlines())
    if num_lines <= 60:
        score += 1
        reasons.append("Concise")
    elif num_lines > 200:
        score -= 2
        reasons.append("Very long")

    # Basic complexity penalty
    complexity_tokens = [" if ", " for ", " while ", " and ", " or ", " try:", " except "]
    complexity = sum(code.count(tok) for tok in complexity_tokens)
    if complexity > 12:
        score -= 2
        reasons.append("High branching/complexity")

    # Common robustness pattern: division by zero guard
    if "ZeroDivisionError" in code or re.search(r"if\s+\w+\s*==\s*0", code):
        score += 1
        reasons.append("Handles division by zero")

    # Micro performance signals
    if "set(" in code or "dict(" in code:
        score += 1
        reasons.append("Uses efficient data structures where appropriate")

    return score, reasons


def _llm_judge(versions: Dict[str, str]):
    if pipe is None:
        return None

    prompt = (
        "You are a strict code judge. Evaluate three Python code variants for the same task.\n"
        "Score each on integer scales 0-10 for metrics: correctness, readability, performance, robustness, consistency.\n"
        "Return ONLY valid JSON with this shape: {\n"
        "  \"fixed\": {\"correctness\": int, \"readability\": int, \"performance\": int, \"robustness\": int, \"consistency\": int, \"explanation\": str},\n"
        "  \"refactored\": { ... },\n"
        "  \"optimized\": { ... },\n"
        "  \"winner\": one of [\"fixed\", \"refactored\", \"optimized\"],\n"
        "  \"reason\": str\n"
        "}\n"
        "Do not include code fences or extra text.\n\n"
        f"fixed:\n{versions.get('fixed','')}\n\n"
        f"refactored:\n{versions.get('refactored','')}\n\n"
        f"optimized:\n{versions.get('optimized','')}\n"
    )

    try:
        response = pipe(prompt, max_new_tokens=400)
        if isinstance(response, list) and response and isinstance(response[0], dict) and 'generated_text' in response[0]:
            text = response[0]['generated_text'].strip()
        else:
            text = str(response).strip()
        data = _safe_json_extract(text)
        if not isinstance(data, dict):
            return None
        winner = data.get("winner")
        if winner not in versions:
            return None
        reason = data.get("reason") or "Selected by LLM judge"
        # Collect per-metric scores if present
        metrics: Dict[str, Dict[str, int]] = {}
        for key in ("fixed", "refactored", "optimized"):
            if isinstance(data.get(key), dict):
                entry = data[key]
                metrics[key] = {
                    "correctness": int(entry.get("correctness", 0)),
                    "readability": int(entry.get("readability", 0)),
                    "performance": int(entry.get("performance", 0)),
                    "robustness": int(entry.get("robustness", 0)),
                    "consistency": int(entry.get("consistency", 0)),
                }
                # Attach explanation if present
                if isinstance(entry.get("explanation"), str):
                    metrics[key]["explanation"] = entry["explanation"]
                # Add total
                metrics[key]["total"] = (
                    metrics[key]["correctness"]
                    + metrics[key]["readability"]
                    + metrics[key]["performance"]
                    + metrics[key]["robustness"]
                    + metrics[key]["consistency"]
                )

        return {"winner": winner, "code": versions[winner], "reason": reason, "metrics": metrics}
    except Exception:
        return None


def judge_agent(versions: dict) -> dict:
    # Try LLM-based judgment first
    llm_result = _llm_judge(versions)
    if llm_result is not None:
        return llm_result

    # Fallback to heuristic scoring
    explanations: Dict[str, str] = {}
    scores: Dict[str, int] = {}
    metrics_out: Dict[str, Dict[str, int]] = {}

    for name, code in versions.items():
        score, reasons = _score_code_heuristic(code)
        scores[name] = score
        explanations[name] = "; ".join(reasons)

        # Derive a coarse per-metric breakdown on 0..10 scales
        # These are heuristics to surface in UI when no LLM metrics are available
        correctness = 7 if "Syntax error" not in explanations[name] else 2
        readability = 5 + (1 if '"""' in code or "'''" in code else 0) + (1 if '#' in code else 0)
        performance = 5 + (1 if "set(" in code or "dict(" in code else 0)
        robustness = 4 + (2 if ("try" in code and "except" in code) else 0)
        consistency = 5 + (1 if 'def ' in code else 0)
        metrics_out[name] = {
            "correctness": max(0, min(10, correctness)),
            "readability": max(0, min(10, readability)),
            "performance": max(0, min(10, performance)),
            "robustness": max(0, min(10, robustness)),
            "consistency": max(0, min(10, consistency)),
            "explanation": explanations[name],
        }
        metrics_out[name]["total"] = (
            metrics_out[name]["correctness"]
            + metrics_out[name]["readability"]
            + metrics_out[name]["performance"]
            + metrics_out[name]["robustness"]
            + metrics_out[name]["consistency"]
        )

    # Choose best by score (break ties by preferring optimized > refactored > fixed)
    preference = {"optimized": 3, "refactored": 2, "fixed": 1}
    winner = max(scores.keys(), key=lambda k: (scores[k], preference.get(k, 0)))

    # Generate a more meaningful reason
    winner_reason = explanations[winner] or "Selected based on heuristic quality metrics."
    
    # If the winner has syntax errors, provide a more helpful message
    if "Syntax error" in winner_reason:
        winner_reason = "Selected despite syntax issues - other variants had similar problems. Consider reviewing the code for syntax errors."
    elif "Code parsing failed" in winner_reason:
        winner_reason = "Selected as best available option - code may need manual review for syntax issues."
    
    return {
        "winner": winner,
        "code": versions[winner],
        "reason": winner_reason,
        "metrics": metrics_out,
    }
