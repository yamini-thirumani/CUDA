import ast

from agents.codewriter_agent import OfflineCodeWriterAgent
from services.pipeline import run_all_agents


class PlannerAgent:
    def __init__(self, code_writer_agent: OfflineCodeWriterAgent):
        self.code_writer_agent = code_writer_agent

    def is_code_snippet(self, text: str) -> bool:
        """Return True if the input is Python code rather than an English task.

        Uses Python's own parser: real code parses, while most English sentences
        ("check if a number is even") raise a SyntaxError. A lone word like
        "hello" also parses (as a variable name), so bare names and constants
        are not treated as code.
        """
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return False
        return any(
            not (isinstance(node, ast.Expr) and isinstance(node.value, (ast.Name, ast.Constant)))
            for node in tree.body
        )

    async def handle_input(self, input_text: str):
        if self.is_code_snippet(input_text):
            try:
                result = await run_all_agents(input_text)
                return result
            except Exception as e:
                return {
                    "final_code": input_text,
                    "winner": "N/A",
                    "reason": f"PlannerAgent Error: Failed to run agents: {str(e)}"
                }
        else:
            prompt = f"# Python function\n# Task: {input_text.strip()}\n"
            generated_code = self.code_writer_agent.generate_code(prompt)
            # After generating code from prompt, also pass it through CUDA agents
            try:
                result = await run_all_agents(generated_code)
                return result
            except Exception as e:
                # Fallback to just the generated code if agents fail
                return {
                    "final_code": generated_code,
                    "winner": "N/A",
                    "reason": f"CUDA agents unavailable; returning generated code. Details: {str(e)}"
                }
