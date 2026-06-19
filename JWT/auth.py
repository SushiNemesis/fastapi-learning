from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime,timedelta

pwd_content = CryptContext(schemes=["bcrypt"],deprecated = "auto")

def get_password_hash(password):
    return pwd_content.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_content.verify(plain_password,hashed_password)
    

hase = get_password_hash("hello123")
print(hase)

SECRET_KEY ="supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKENS_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes= ACCESS_TOKENS_EXPIRE_MINUTES
    )

    to_encode.update(
        {"exp": expire}
    )

    encoded_jwt = jwt.encode(
        to_encode,SECRET_KEY,algorithm=ALGORITHM
    )

    return encoded_jwt