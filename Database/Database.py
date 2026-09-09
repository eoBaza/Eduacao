import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()


DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('user')}:"
    f"{os.getenv('password')}@"
    f"{os.getenv('host')}:"
    f"{os.getenv('port')}/"
    f"{os.getenv('database')}"
)

engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass