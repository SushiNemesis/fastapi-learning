from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base, get_db
from models import User, Order
from schemas import (
    UserCreate,
    UserResponse,
    OrderCreate,
    OrderResponse
)

app = FastAPI()

Base.metadata.create_all(bind = engine)

@app.post("/users", response_model= UserResponse)
def create_user( user : UserCreate,db: Session = Depends(get_db)):
    new_user = User(name = user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/orders",response_model= OrderResponse)
def create_order( order : OrderCreate, db : Session = Depends(get_db)):
    user = db.query(User).filter(User.id == order.user_id).first()
    if not user:
        raise HTTPException(
            status_code= 404,
            detail= "User not Found"      
            )
    new_order = Order(user_id = order.user_id, item = order.item_name)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@app.get("/users/{user_id}",response_model=UserResponse)
def get_user(user_id : int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code= 404,
            detail= "User not found"
        )

    return user

@app.get("/users",response_model=list[UserResponse])
def get_user(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user