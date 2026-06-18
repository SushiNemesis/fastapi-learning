from fastapi import FastAPI

app = FastAPI()

@app.get("/tasks")
def get_tasks():
    return []

@app.post("/tasks")
def create_task():
    return {"message": "Task created"}

@app.put("/tasks/1")
def update_task():
    return {"message": "Task updated"}

@app.delete("/tasks/1")
def delete_task():
    return {"message": "Task deleted"} 