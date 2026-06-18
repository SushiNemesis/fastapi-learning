from sqlalchemy import Integer, Column, String,Float, ForeignKey
from database import Base
from sqlalchemy.orm import relationship 

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True)
    name = Column(String)

    orders = relationship("Order", back_populates= "user")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key= True)
    item = Column(String)
    user_id = Column(Integer,ForeignKey("users.id"))

    user = relationship("User", back_populates= "orders")
