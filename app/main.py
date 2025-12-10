# app/main.py

from fastapi import FastAPI, HTTPException
from engine.graph_engine import GraphEngine
from models.graph_models import CreateGraphModel, RunGraphModel
from workflow import code_review

app = FastAPI()
engine = GraphEngine()

FUNCTION_MAP = {
    "extract_functions": code_review.extract_functions,
    "check_complexity": code_review.check_complexity,
    "detect_issues": code_review.detect_issues,
    "suggest_improvements": code_review.suggest_improvements,
}

@app.post("/graph/create")
def create_graph(payload: CreateGraphModel):
    nodes = {name: FUNCTION_MAP[fn] for name, fn in payload.nodes.items()}
    graph_id = engine.create_graph(nodes, payload.edges)
    return {"graph_id": graph_id}


@app.post("/graph/run")
def run_graph(payload: RunGraphModel):
    run_id = engine.start_run(payload.graph_id, payload.initial_state)
    state, logs = engine.run(run_id)
    return {"run_id": run_id, "final_state": state, "logs": logs}


@app.get("/graph/state/{run_id}")
def get_state(run_id: str):
    data = engine.get_state(run_id)
    if not data:
        raise HTTPException(status_code=404)
    return data
