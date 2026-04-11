from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FacultyBase(BaseModel):
    name: str

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    name: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    faculty_id: int

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    faculty: Optional[Faculty] = None
    
    class Config:
        from_attributes = True

class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade: int

class GradeCreate(GradeBase):
    pass

class Grade(GradeBase):
    id: int
    student: Optional[Student] = None
    course: Optional[Course] = None
    
    class Config:
        from_attributes = True

class StudentWithGrades(Student):
    grades: List[Grade] = []

class FacultyAverage(BaseModel):
    faculty_name: str
    average_grade: float


#===== new
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_readonly: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str