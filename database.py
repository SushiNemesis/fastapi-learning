from sqlalchemyy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

Database_URL = "sqlite:///./store.db"
engine = create_engine(Database_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()