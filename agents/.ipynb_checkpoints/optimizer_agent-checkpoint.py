def run_optimizer(code, pipe, call_agent):
    prompt = f"Optimize this code for speed and efficiency:\n{code}"
    return call_agent(prompt, pipe)
