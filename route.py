from fastapi import FastAPI

app = FastAPI()

@app.get("/student/{student_id}")
def get(student_id:int):
    return {"student_id": student_id}
