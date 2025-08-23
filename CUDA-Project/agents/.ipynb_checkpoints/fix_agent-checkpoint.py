def rootcause_fix(code, pipe, call_agent):
    if "/0" in code or "ZeroDivisionError" in code:
        prompt = f"Fix bugs in this Python code and return only the corrected code:\n{code}"
    else:
        prompt = f"The code below is logically correct but may contain edge-case bugs or inefficiencies. Suggest an improved version:\n{code}"

    return call_agent(prompt, pipe)  # Make sure this returns string
