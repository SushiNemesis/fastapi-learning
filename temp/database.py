from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,Session,sessionmaker

engine = create_engine("sqlite:///students.db",connect_args={"check_same_thread":False})
Base = declarative_base()

SessionLocal = sessionmaker(
    autoflush= False,
    autocommit = False,
    bind = engine
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()