from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException,status
from database import get_db
from sqlalchemy.orm import Session
from models import User

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(password , hashed_password):
    return pwd_context.verify(password,hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY ="supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKENS_EXPIRE_MINUTES = 30

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail = "Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
    )

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKENS_EXPIRE_MINUTES
    )
    to_encode.update(
        {"exp" : expire}
    )

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme),db:Session= Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise credentials_exception
    return user