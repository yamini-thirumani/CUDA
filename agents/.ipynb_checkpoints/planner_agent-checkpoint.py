from agents.codewriter_agent import OfflineCodeWriterAgent

class PlannerAgent:
    def __init__(self, code_writer_agent: OfflineCodeWriterAgent):
        self.code_writer_agent = code_writer_agent

    def is_code_snippet(self, text: str) -> bool:
        code_indicators = [
            'def ', 'class ', 'import ', '=', 'return',
            'print(', '(', ')', '{', '}', 'if ', 'while ', 'for '
        ]
        return any(indicator in text for indicator in code_indicators)

    async def handle_input(self, input_text: str) -> str:
        if self.is_code_snippet(input_text):
            try:
                result = await run_all_agents(input_text)
                return result.get("final_code", "[PlannerAgent] No final code returned.")
            except Exception as e:
                return f"[PlannerAgent Error] Failed to run agents: {str(e)}"
        else:
            prompt = f"# Python function\n# Task: {input_text.strip()}\n"
            return self.code_writer_agent.generate_code(prompt)
