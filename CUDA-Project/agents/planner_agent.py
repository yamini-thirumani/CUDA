# from agents.codewriter_agent import OfflineCodeWriterAgent
# from services.pipeline import run_all_agents
# class PlannerAgent:
#     def __init__(self, code_writer_agent: OfflineCodeWriterAgent):
#         self.code_writer_agent = code_writer_agent

#     def is_code_snippet(self, text: str) -> bool:
#         code_indicators = [
#             'def ', 'class ', 'import ', '=', 'return',
#             'print(', '(', ')', '{', '}', 'if ', 'while ', 'for '
#         ]
#         return any(indicator in text for indicator in code_indicators)

#     async def handle_input(self, input_text: str) -> str:
#         if self.is_code_snippet(input_text):
#             try:
#                 result = await run_all_agents(input_text)
#                 return result.get("final_code", "[PlannerAgent] No final code returned.")
#             except Exception as e:
#                 return f"[PlannerAgent Error] Failed to run agents: {str(e)}"
#         else:
#             # Generate initial code from NLP input
#             prompt = f"# Python function\n# Task: {input_text.strip()}\n"
#             initial_code = self.code_writer_agent.generate_code(prompt)
            
#             # Now send the generated code through the CUDA agents pipeline
#             try:
#                 result = await run_all_agents(initial_code)
#                 return result.get("final_code", "[PlannerAgent] No final code returned.")
#             except Exception as e:
#                 return f"[PlannerAgent Error] Failed to run agents: {str(e)}"
from agents.codewriter_agent import OfflineCodeWriterAgent
from services.pipeline import run_all_agents
class PlannerAgent:
    def __init__(self, code_writer_agent: OfflineCodeWriterAgent):
        self.code_writer_agent = code_writer_agent

    def is_code_snippet(self, text: str) -> bool:
        code_indicators = [
            'def ', 'class ', 'import ', '=', 'return',
            'print(', '(', ')', '{', '}', 'if ', 'while ', 'for '
        ]
        return any(indicator in text for indicator in code_indicators)

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
