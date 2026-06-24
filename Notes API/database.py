from sqlalchemy.orm import Session,sessionmaker ,declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine("sqlite:///notes.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False,autocommit= False,bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()