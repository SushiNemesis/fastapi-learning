from fastapi import Depends, FastAPI,HTTPException
from sqlalchemy import create_engine,Integer,Column,Row, String, Float
from sqlalchemy.orm import declarative_base, Session,sessionmaker
from pydantic import BaseModel

app = FastAPI()

engine = create_engine("sqlite:///store.db", connect_args= {"check_same_thread": False})

SessionLocal = sessionmaker(autoflush= False,autocommit = False, bind = engine)

Base = declarative_base()

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    model_config = {
        "from_attributes": True
    }
                    
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    
Base.metadata.create_all(bind = engine)

class ProductCreate(BaseModel):
    name: str
    price: float

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()

@app.post("/products")
def create_product(product : ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(name = product.name, price = product.price)

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

@app.get("/products", response_model= list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.get("/products/{product_id}",response_model=ProductResponse)
def get_product(product_id: int,db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if product is None:
        raise HTTPException(
            status_code= 404,
            detail="Product not found"
        )
    
    return product