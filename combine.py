from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

class Student(BaseModel):
    name: str
    age: int

@app.put("/students/{student_id}")
def update_student(
    student_id : int,
    student : Student
):
    return {
        "id" : student_id,
        "student" : student
    }