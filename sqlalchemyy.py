from fastapi import Depends,FastAPI
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker, Session

app = FastAPI()

engine = create_engine("sqlite:///store.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind = engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True)
    username = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()

    try:
        yield db
    
    finally:
        db.close()
    
@app.get("/")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()