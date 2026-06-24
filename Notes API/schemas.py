from pydantic import BaseModel,Field
from datetime import datetime

class NoteCreate(BaseModel):
    title : str = Field(...,max_length=100,min_length=3)
    content : str = Field(...,min_length=1)

class NoteResponse(BaseModel):
    id : int
    title : str 
    content: str
    date_created : datetime

    model_config = { "from_attributes" : True }

class UserCreate(BaseModel):
    username : str
    email : str
    password : str

class UserResponse(BaseModel):
    id : int
    username : str
    email : str    
    model_config = {"from_attributes":True}

class UserLogin(BaseModel):
    username : str
    password : str