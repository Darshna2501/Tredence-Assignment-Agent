# app/models/graph_models.py
from pydantic import BaseModel
from typing import Dict, Callable

class CreateGraphModel(BaseModel):
    nodes: Dict[str, str]   # function names
    edges: Dict[str, str]

class RunGraphModel(BaseModel):
    graph_id: str
    initial_state: Dict
