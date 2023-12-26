from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table,Float
from app.database import Base

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gpa = Column(Float)
    attendance = Column(Integer)
    class_name = Column(String)