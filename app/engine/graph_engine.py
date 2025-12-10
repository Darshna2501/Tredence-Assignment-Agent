import uuid
from typing import Dict, Callable, Any, List

class GraphEngine:
    def __init__(self):
        self.graphs: Dict[str, Dict] = {}
        self.runs: Dict[str, Dict] = {}

    def create_graph(self, nodes: Dict[str, Callable], edges: Dict[str, str]):
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = {
            "nodes": nodes,
            "edges": edges
        }
        return graph_id

    def start_run(self, graph_id: str, initial_state: Dict):
        run_id = str(uuid.uuid4())
        self.runs[run_id] = {
            "graph_id": graph_id,
            "state": initial_state,
            "log": [],
            "current_node": None,
            "finished": False
        }
        return run_id

    def run(self, run_id: str):
        run = self.runs[run_id]
        graph = self.graphs[run["graph_id"]]
        nodes = graph["nodes"]
        edges = graph["edges"]

        current = list(nodes.keys())[0]
        run["current_node"] = current

        while current:
            func = nodes[current]
            run["log"].append(f"Running node: {current}")

            output = func(run["state"])
            run["state"].update(output)

            if "next" in run["state"]:      # conditional branching
                current = run["state"]["next"]
                run["state"].pop("next")
                continue

            if current in edges:
                current = edges[current]
            else:
                current = None

        run["finished"] = True
        return run["state"], run["log"]

    def get_state(self, run_id: str):
        return self.runs.get(run_id)
