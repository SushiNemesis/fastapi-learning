from fastapi import FastAPI
from fastapi import Depends

app = FastAPI()

def get_username():
    return "Username"

@app.get("/products")
def get_products(user = Depends(get_username)):
    return {"user": user}
