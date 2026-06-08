from pydantic import BaseModel
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

class Address(BaseModel):
    city : str
    state : str
    pincode: int

class Student(BaseModel):
    name : str
    age : int
    course : Optional[str] = None
    grade : int
    skills : list[str]
    address : Address

@app.post("/student")
def create_student(student: Student):
    return student