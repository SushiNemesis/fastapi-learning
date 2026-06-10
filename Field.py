from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()

class Product(BaseModel):
    name: str= Field(min_length=3,max_length=50)
    price: int= Field(gt=0)

@app.post("/")
def post_product(product: Product):
    return product