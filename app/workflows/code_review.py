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
    state["quality_score"] = score

    if score < state["threshold"]:
        return {"next": "suggest_improvements"}   # loop
    return {}
