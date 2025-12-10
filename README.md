# 🔄 Tredance - Workflow Engine

A powerful, node-based workflow orchestration engine built with FastAPI. Execute complex workflows with conditional branching, loops, and shared state management across nodes.

## ✨ Features

- **Node-Based Architecture**: Create flexible workflows by connecting nodes
- **Shared State Management**: Pass data seamlessly between nodes via a shared dictionary
- **Conditional Branching**: Support for conditional logic within workflows
- **Loop Support**: Implement loops and iterative workflows
- **REST API**: Full REST endpoints for creating and executing workflows
- **Tool Registry**: Built-in function registry for easy node mapping
- **Code Review Workflow**: Pre-built example workflow for code analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone the repository:
```bash
cd d:\Projects\Tredance
```

2. Install dependencies:
```bash
pip install fastapi uvicorn
```

3. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## 📚 Project Structure

```
Tredance/
├── main.py                          # FastAPI application & endpoints
├── engine/
│   ├── __init__.py
│   ├── graph_engine.py             # Core workflow engine
│   └── tool_reg.py                 # Tool/function registry
├── models/
│   ├── __init__.py
│   └── graph_models.py             # Pydantic data models
├── workflow/
│   ├── __init__.py
│   └── code_review.py              # Code review workflow example
└── README.md
```

## 🔌 API Endpoints

### 1. Create a Workflow Graph

**POST** `/graph/create`

Creates a new workflow graph with nodes and edges.

**Request Body:**
```json
{
  "nodes": {
    "extract_functions": "extract_functions",
    "check_complexity": "check_complexity",
    "detect_issues": "detect_issues",
    "suggest_improvements": "suggest_improvements"
  },
  "edges": {
    "extract_functions": "check_complexity",
    "check_complexity": "detect_issues",
    "detect_issues": "suggest_improvements"
  }
}
```

**Response:**
```json
{
  "graph_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 2. Execute a Workflow

**POST** `/graph/run`

Executes a workflow graph with initial state.

**Request Body:**
```json
{
  "graph_id": "550e8400-e29b-41d4-a716-446655440000",
  "initial_state": {
    "code": "def hello():\n    return 'world'\n\ndef goodbye():\n    return 'world'",
    "threshold": 70
  }
}
```

**Response:**
```json
{
  "run_id": "660e8400-e29b-41d4-a716-446655440001",
  "final_state": {
    "code": "...",
    "functions": 2,
    "complexity": 4,
    "issues": 1,
    "quality_score": 90,
    "threshold": 70
  },
  "logs": [
    "Running node: extract_functions",
    "Running node: check_complexity",
    "Running node: detect_issues",
    "Running node: suggest_improvements"
  ]
}
```

### 3. Get Workflow State

**GET** `/graph/state/{run_id}`

Retrieves the state of a completed or running workflow.

**Response:**
```json
{
  "graph_id": "550e8400-e29b-41d4-a716-446655440000",
  "state": { ... },
  "log": [ ... ],
  "current_node": "suggest_improvements",
  "finished": true
}
```

## 🎯 Example: Code Review Workflow

The included **Code Review Workflow** analyzes Python code and provides quality feedback.

### Workflow Steps:

1. **Extract Functions** - Counts function definitions in code
2. **Check Complexity** - Calculates complexity score based on function count
3. **Detect Issues** - Identifies potential issues based on complexity
4. **Suggest Improvements** - Generates quality score and loops if below threshold

### Sample Request:

```bash
curl -X POST "http://localhost:8000/graph/create" \
  -H "Content-Type: application/json" \
  -d '{
    "nodes": {
      "extract_functions": "extract_functions",
      "check_complexity": "check_complexity",
      "detect_issues": "detect_issues",
      "suggest_improvements": "suggest_improvements"
    },
    "edges": {
      "extract_functions": "check_complexity",
      "check_complexity": "detect_issues",
      "detect_issues": "suggest_improvements"
    }
  }'
```

```bash
curl -X POST "http://localhost:8000/graph/run" \
  -H "Content-Type: application/json" \
  -d '{
    "graph_id": "YOUR_GRAPH_ID",
    "initial_state": {
      "code": "def example():\n    pass",
      "threshold": 70
    }
  }'
```

## 🏗️ How It Works

### GraphEngine

The `GraphEngine` is the core orchestrator that:

- **Creates graphs** with nodes and edges
- **Manages runs** with unique run IDs
- **Executes workflows** following the node connections
- **Maintains state** across node executions
- **Supports branching** via the `"next"` state key
- **Logs execution** for debugging and monitoring

### State Management

- Each workflow has a shared state dictionary
- Nodes receive the current state and return updates
- Updates are merged into the state automatically
- Use `"next"` key in returned dict for conditional routing

### Conditional Branching Example

```python
def my_node(state):
    if state["value"] > 10:
        return {"next": "high_value_node"}
    else:
        return {"next": "low_value_node"}
```

## � Creating Custom Workflows

### 1. Create a new workflow file:

```python
# workflow/my_workflow.py

def my_first_node(state):
    result = do_something(state["input"])
    return {"output": result}

def my_second_node(state):
    processed = process(state["output"])
    return {"final_result": processed}
```

### 2. Register in main.py:

```python
from workflow import my_workflow

FUNCTION_MAP = {
    "my_first": my_workflow.my_first_node,
    "my_second": my_workflow.my_second_node,
}
```

### 3. Use via API as shown above

## 📋 Requirements

- **fastapi**: Modern web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation

Install all at once:
```bash
pip install fastapi uvicorn pydantic
```

## 🧪 Testing the API

### Using Python requests library:

```python
import requests

# Create graph
response = requests.post(
    "http://localhost:8000/graph/create",
    json={
        "nodes": {
            "node1": "extract_functions",
            "node2": "check_complexity"
        },
        "edges": {"node1": "node2"}
    }
)
graph_id = response.json()["graph_id"]

# Run workflow
response = requests.post(
    "http://localhost:8000/graph/run",
    json={
        "graph_id": graph_id,
        "initial_state": {"code": "def test(): pass", "threshold": 70}
    }
)
print(response.json())
```

## 🚨 Error Handling

- **404 Not Found**: Run ID doesn't exist
- **400 Bad Request**: Invalid request payload
- **500 Internal Server Error**: Workflow execution error

## 🔮 Future Enhancements

- [ ] WebSocket streaming for real-time logs
- [ ] Async/concurrent node execution
- [ ] Persistent database storage (PostgreSQL)
- [ ] Workflow visualization UI
- [ ] Advanced error recovery and retry logic
- [ ] Performance monitoring and metrics
- [ ] Workflow templates and versioning

## 📝 License

This project is provided as-is for educational purposes.

## 💬 Support

For issues or questions, please refer to the code comments and docstrings for detailed implementation details.