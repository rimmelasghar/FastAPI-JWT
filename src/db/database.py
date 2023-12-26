from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker,declarative_base
import sqlalchemy
import sqlite3

DATABASE_URL = "sqlite:///src/db/test.db"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=True, autoflush=False, bind=engine)

Base = declarative_base()


metadata = MetaData()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        


