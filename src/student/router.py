from fastapi import APIRouter, Depends, status, Response, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
import src.db.database as db
from src.auth.jwt import create_access_token, get_current_user
from src.auth.models import User
from sqlalchemy.orm import Session
from typing import List
from src.student import services
import src.db.database as db
import src.auth.models as auth_models
import src.student.models as models



router = APIRouter(tags=['student'], prefix='/student')

@router.get("/student/",status_code=200)
def get_all(db: Session = Depends(db.get_db),current_user: auth_models.User = Depends(get_current_user)):
    return services.get_all_students(db)

@router.get("/student/{student_id}", response_model=models.StudentCreate,status_code=200)
def read_item(student_id: int, db: Session = Depends(db.get_db),current_user: auth_models.User = Depends(get_current_user)):
    return services.get_item(db, student_id)

@router.post("/student/", response_model=models.StudentCreate,status_code=201)
def create_student(item: models.StudentCreate, db: Session = Depends(db.get_db),current_user: auth_models.User = Depends(get_current_user)):
    return services.create_item(db, item)

@router.put("/student/{student_id}",response_model=models.StudentCreate,status_code=200)
def update_a_student(student_id: int,studentobj: models.StudentCreate,db:Session = Depends(db.get_db),current_user: auth_models.User = Depends(get_current_user)):
    return services.update_student(db,student_id,studentobj)

@router.delete("/student/{student_id}",status_code=204)
def delete_a_student(student_id: int,db:Session = Depends(db.get_db),current_user: auth_models.User = Depends(get_current_user)):
    services.delete_student(db,student_id)

