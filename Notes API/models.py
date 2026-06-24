from sqlalchemy import Column,String,Integer, DateTime, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    date_created = Column(DateTime,default=datetime.utcnow)
    owner_id = Column(Integer,ForeignKey("users.id"))

    owner = relationship("User",back_populates="notes")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index = True)
    username = Column(String,unique=True)
    email = Column(String,unique=True)
    hashed_password = Column(String)

    notes = relationship("Note", back_populates="owner")
