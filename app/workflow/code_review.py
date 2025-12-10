# app/workflows/code_review.py

def extract_functions(state):
    code = state["code"]
    funcs = code.count("def ")
    return {"functions": funcs}


def check_complexity(state):
    complexity = state["functions"] * 2
    return {"complexity": complexity}


def detect_issues(state):
    issues = max(1, state["complexity"] // 3)
    return {"issues": issues}


def suggest_improvements(state):
    score = 100 - (state["issues"] * 10)
    result = {"quality_score": score}

    if score < state.get("threshold", 70):
        result["next"] = "suggest_improvements"   # loop
    return result
