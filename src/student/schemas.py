from src.db.database import Base
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table,Float



class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    gpa = Column(Float)
    attendance = Column(Integer)
    class_name = Column(String)
    
class Behaviour(Base):
    __tablename__= "behaviour"
    id = Column(Integer, primary_key=True, index=True)
    student_id=Column(Integer)
    negative= Column(Integer)
    positive=Column(Integer)