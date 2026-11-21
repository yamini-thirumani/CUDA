from pydantic import BaseModel


class InputCode(BaseModel):
    """Request body for /run-agents: the code to improve."""
    code: str


class PlannerInput(BaseModel):
    """Request body for /planner: a natural-language task or a code snippet."""
    text: str
