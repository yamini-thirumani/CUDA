from fastapi import FastAPI, Request
from agents.judge_agent import judge_agent
from pydantic import BaseModel
from agents.codewriter_agent import OfflineCodeWriterAgent
from agents.planner_agent import PlannerAgent
from services.pipeline import run_all_agents
import logging

app = FastAPI()

# Initialize agents
code_writer = OfflineCodeWriterAgent()
planner_agent = PlannerAgent(code_writer)

# Request models
class InputCode(BaseModel):
    code: str

class PlannerInput(BaseModel):
    text: str
    
@app.get("/")
def read_root():
    return {"message": "Welcome to CUDA Agent Server! Use /docs to explore."}

@app.post("/planner")
async def planner(data: PlannerInput):
    text = data.text
    output = await planner_agent.handle_input(text)
    return {"output": output}

@app.post("/run-agents")
async def run_agents_api(data: InputCode):
    logging.info(f"Run agents received code: {data.code}")
    try:
        result = await run_all_agents(data.code)
    except Exception as e:
        logging.error(f"Run agents error: {e}")
        result = {"error": str(e)}
    return result
