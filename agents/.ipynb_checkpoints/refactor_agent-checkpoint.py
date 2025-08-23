def run_refactor(code, pipe, call_agent):
    prompt = f"Refactor this code for readability and modularity:\n{code}"
    return call_agent(prompt, pipe)
