from fastapi import FastAPI,Depends, HTTPException
from auth import get_password_hash,verify_password,create_access_token,pwd_content
from model import User
from schemas import UserCreate, UserResponse, UserLogin
from database import engine,Base,get_db
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/signup",response_model= UserResponse)
def signup(user : UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code= 400,
            detail="Username Already Exists"
        )

    
    hash_password = get_password_hash(user.password)
    new_user = User(username = user.username,email = user.email,hashed_password = hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(
            status_code= 404,
            detail= "User Not Found"
        )
    if not verify_password(user.password,existing_user.hashed_password):
        raise HTTPException(
            status_code= 401,
            detail="Invalid Password"
        )
    access_token = create_access_token(
        {
            "sub" : existing_user.username,
            "user_id" : existing_user.id
        }
    )
    return{
        "access_token":access_token,
        "token_type" : "bearer"
    }