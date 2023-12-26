from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    gpa: float
    attendance: int
    class_name: str
