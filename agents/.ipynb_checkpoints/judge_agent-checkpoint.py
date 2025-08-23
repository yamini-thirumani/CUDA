def judge_agent(versions: dict) -> dict:
    explanations = {}
    scores = {}

    for name, code in versions.items():
        score = 0
        explanation = []

        # ✅ Handle ZeroDivisionError
        if "ZeroDivisionError" in code or "if b == 0" in code:
            score += 5
            explanation.append("Handles division by zero.")

        # ✅ Exception handling
        if "try" in code and "except" in code:
            score += 3
            explanation.append("Uses try-except for robust error handling.")

        # ✅ Input validation / readability
        if "def" in code and "input(" in code:
            score += 2
            explanation.append("Includes user input handling and modularity.")

        # ✅ Compactness
        if len(code.splitlines()) <= 12:
            score += 1
            explanation.append("Concise code.")

        # ✅ Comments or documentation
        if "#" in code:
            score += 1
            explanation.append("Includes comments.")

        scores[name] = score
        explanations[name] = "; ".join(explanation)

    # Find the winner
    winner = max(scores, key=scores.get)

    return {
        "winner": winner,
        "code": versions[winner],
        "reason": explanations[winner] or "Selected based on best overall structure and error handling."
    }
