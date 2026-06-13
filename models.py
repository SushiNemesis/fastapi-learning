from sqlalchemyy import Column,Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    Price = Column(Float)
    

from database import SessionLocal

db = SessionLocal()

new_product = Product(
    name = "laptop",
    Price = 50000
)

db.add(new_product)
db.commit()

products = db.query(Product).all()
product = db.query(Product).filter(Product.id == 1).first()
product.Price = 10000
db.commit()