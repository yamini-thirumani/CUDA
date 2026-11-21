# CUDA – Collaborative Unified Developer Assistant

A multi-agent LLM system that improves Python code. You give it code (or a task in plain English). Three specialised agents each produce an improved version in parallel, and a **Judge** agent picks the best one.

Built during a summer research internship with the University of North Texas (2025), on the theme *AI agents for software development*.

## How it works

```
Streamlit UI ──► FastAPI backend
                   │
   /planner ───────┤  text → TinyLlama 1.1B writes a first draft
   /run-agents ────┤  code
                   ▼
   ┌──────────── run concurrently ────────────┐
   │  Fix agent   │ Refactor agent │ Optimizer │   (DeepSeek-Coder 6.7B, 4-bit)
   └──────────────────────┬───────────────────┘
                          ▼
                     Judge agent
      1. LLM judge: scores each version 0–10 on correctness,
         readability, performance, robustness, consistency (JSON)
      2. Fallback: heuristic scoring (ast syntax check, error
         handling, docstrings, complexity penalty, ...)
                          ▼
     Best version + all versions + scores + diff shown in the UI
```

| Component | File | What it does |
|---|---|---|
| API | `main.py` | FastAPI app with `/`, `/planner`, `/run-agents` |
| Request models | `models/schemas.py` | Pydantic models for request bodies |
| Pipeline | `services/pipeline.py` | Runs the three agents concurrently (`run_in_executor` + `asyncio.gather`), then calls the judge |
| Model | `agents/model_loader.py` | Loads DeepSeek-Coder 6.7B Instruct with 4-bit NF4 quantization (bitsandbytes) so it fits on a single GPU |
| Agents | `agents/fix_agent.py`, `refactor_agent.py`, `optimizer_agent.py` | Each agent is a focused prompt to the shared model |
| Judge | `agents/judge_agent.py` | LLM-based scoring with a heuristic fallback |
| Planner | `agents/planner_agent.py` | Detects code vs. natural language using Python's `ast` parser; generates code with TinyLlama when needed |
| Code writer | `agents/codewriter_agent.py` | TinyLlama 1.1B for lightweight code generation |
| UI | `frontend/app.py` | Streamlit app: prompt or code input, winner, all versions, scores, diff |

## Running it

Requirements: Python 3.9+, a CUDA-capable GPU (about 6 GB+ VRAM for the 4-bit 6.7B model).

```bash
pip install -r requirements.txt

# Backend (http://127.0.0.1:8000, API docs at /docs)
uvicorn main:app --host 0.0.0.0 --port 8000

# Frontend (http://localhost:8501)
CUDA_BACKEND_URL=http://127.0.0.1:8000 streamlit run frontend/app.py

# Optional: smoke-test both endpoints while the backend is running
python scripts/smoke_test.py
```

## API

| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET | `/` | – | Health message |
| POST | `/run-agents` | `{"code": "..."}` | `final_code`, `winner`, `reason`, `metrics`, `versions`, `baseline` |
| POST | `/planner` | `{"text": "..."}` | Same shape as `/run-agents` |

## Known limitations and next steps

- **Shared GPU model:** the three agents run concurrently from the server's point of view, but they share one model on one GPU, so generation is largely serialized. Batching the three prompts or using an inference server (e.g. vLLM) would give a real speed-up.
- **Heuristic judge is shallow:** checks like `"try" in code` can be fooled. The strongest improvement would be to execute each version against test cases in a sandbox and score on pass rate.
- **Self-evaluation bias:** the same model generates and judges. A different judge model or test-based scoring would be fairer.
- **Output length:** agents are capped at 200 new tokens, which can truncate longer code.
- Future scope: more languages, cloud deployment, and more specialised agents (security audit, SQL query optimisation).

## License

MIT
