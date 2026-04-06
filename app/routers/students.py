import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from .. import schemas, crud

router = APIRouter(prefix="/students", tags=["students"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@router.get("/", response_model=List[schemas.Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/{student_id}", response_model=schemas.StudentWithGrades)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/{student_id}/grades", response_model=List[schemas.Grade])
def read_student_grades(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.get_student_grades(db, student_id=student_id)



#---- task 3


# UPDATE студента
@router.put("/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int, 
    student: schemas.StudentCreate, 
    db: Session = Depends(get_db)
):
    db_student = crud.update_student(db, student_id, student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# DELETE студента
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# 1. Студенты по названию факультета
@router.get("/by-faculty/{faculty_name}", response_model=List[schemas.Student])
def get_students_by_faculty(faculty_name: str, db: Session = Depends(get_db)):
    students = crud.get_students_by_faculty_name(db, faculty_name)
    if not students:
        raise HTTPException(status_code=404, detail="No students found for this faculty")
    return students

# 3. Студенты по курсу с оценкой ниже 30
@router.get("/by-course-below-30/{course_name}", response_model=List[schemas.Student])
def get_students_by_course_below_30(course_name: str, db: Session = Depends(get_db)):
    students = crud.get_students_by_course_below_30(db, course_name)
    if not students:
        raise HTTPException(status_code=404, detail="No students found with grade < 30 for this course")
    return students