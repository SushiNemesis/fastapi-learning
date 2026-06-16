from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    name : str
    id : int
    class Config : from_attributes = True

class OrderCreate(BaseModel):
    user_id : int
    item_name : str

class OrderResponse(BaseModel):
    id : int  
    user_id : int
    item_name : str 
    class Config : from_attributes = True
