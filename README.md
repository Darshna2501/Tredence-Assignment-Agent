# Workflow Engine — AI Engineering Assignment

## 🚀 Features
- Node-based workflow engine
- Shared state dictionary between nodes
- Supports conditional branching, loops
- Tool registry
- FastAPI endpoints

## ▶️ How to Run
1. `pip install fastapi uvicorn`
2. `uvicorn app.main:app --reload`

## 🧠 Example Workflow
Implemented: **Code Review Agent**
1. Extract functions  
2. Check complexity  
3. Detect issues  
4. Suggest improvements (loops until quality ≥ threshold)

## 📦 Future Improvements
- WebSocket streaming logs  
- Async task execution  
- Persistent DB storage  