from fastapi import HTTPException
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{id}")
def get_user(id: int):
    if id != 1:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return {"id":1, "name": "John"}