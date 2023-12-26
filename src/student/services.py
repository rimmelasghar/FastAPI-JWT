from sqlalchemy.orm import Session
from fastapi import Depends
from src.student.models import *
from src.student.schemas import *
from fastapi import HTTPException

def create_item(db: Session, student: StudentCreate):
    try:
        db_item = Student(**student.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        print(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_item(db: Session, item_id: int):
    item = db.query(Student).filter(Student.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return item

def get_all_students(db: Session):
    return db.query(Student).all()

def update_student(db: Session,student_id:int,student_obj: StudentCreate):
    student = get_item(db,student_id)
    student.name = student_obj.name
    student.gpa = student_obj.gpa
    student.attendance = student_obj.attendance
    student.class_name = student_obj.class_name
    db.commit()  
    db.refresh(student)  
    return student

def delete_student(db: Session,student_id:int):
    student = get_item(db,student_id)
    db.delete(student)
    db.commit() 
    return student

def get_all_students_behaviour(db: Session):
    return db.query(Behaviour).all()