import logging

from fastapi import FastAPI

from agents.codewriter_agent import OfflineCodeWriterAgent
from agents.planner_agent import PlannerAgent
from models.schemas import InputCode, PlannerInput
from services.pipeline import run_all_agents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CUDA - Collaborative Unified Developer Assistant")

# Load the models once at startup and share them across requests
code_writer = OfflineCodeWriterAgent()
planner_agent = PlannerAgent(code_writer)


@app.get("/")
def read_root():
    return {"message": "Welcome to CUDA Agent Server! Use /docs to explore."}


@app.post("/planner")
async def planner(data: PlannerInput):
    """Natural-language task (or code) -> generated code -> agent pipeline."""
    return await planner_agent.handle_input(data.text)


@app.post("/run-agents")
async def run_agents_api(data: InputCode):
    """Code -> Fix / Refactor / Optimize agents in parallel -> Judge picks the best."""
    logger.info("Run agents received %d characters of code", len(data.code))
    try:
        return await run_all_agents(data.code)
    except Exception as e:
        logger.exception("Run agents error")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
