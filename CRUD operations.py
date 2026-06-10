from fastapi import FastAPI
from pydantic import BaseModel,Field
from fastapi import HTTPException


app = FastAPI()

class Product(BaseModel):
    id : int=Field(ge=0)
    name: str= Field(min_length=3,max_length=20)

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"}
]

@app.get("/products")
def get_products():
    return products

@app.get("/products/{id}")
def get_product(id : int):
    for product in products:
        if product["id"] == id:
            return product
        
@app.post("/create")
def post_product(product: Product):
    products.append(product.model_dump())

@app.put("/update/{id}")
def update_product(product: Product,id:int):
    for i,produc in enumerate(products):
        if produc["id"] == id:
            products[i] = product.model_dump()
            return products[i]
    
    raise HTTPException(
        status_code=404,
        detail= "user not found"
    )

@app.delete("/delete/{id}")
def delete_product(id : int):
    for product in products:
        if product["id"] == id:
            products.remove(product)
            return {"Message": "Product Deleted"}
        
    raise HTTPException(
        status_code=404,
        detail= "user not found"
    )