from fastapi import FastAPI

app = FastAPI()


@app.get("/multiply")
def multiply_query(a:int,b:int):
    return {"result":a*b}


@app.get("/search")
def get_user(name: str,age: int):
    return {"name":name,"age" :age}