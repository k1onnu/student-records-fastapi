import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# ВРЕМЕННО импортируем напрямую
from app.database import SessionLocal
from .. import schemas, crud

router = APIRouter(prefix="/grades", tags=["grades"])

# ВРЕМЕННАЯ функция get_db прямо здесь
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Grade)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    return crud.create_grade(db=db, grade=grade)

@router.get("/", response_model=List[schemas.Grade])
def read_grades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    grades = crud.get_grades(db, skip=skip, limit=limit)
    return grades

@router.get("/faculty/{faculty_id}/average")
def read_faculty_average(faculty_id: int, db: Session = Depends(get_db)):
    average = crud.get_faculty_average_grade(db, faculty_id)
    return {"faculty_id": faculty_id, "average_grade": average}

@router.get("/faculties/average", response_model=List[schemas.FacultyAverage])
def read_all_faculties_average(db: Session = Depends(get_db)):
    return crud.get_all_faculties_average(db)



# --- task 3

# UPDATE оценки
@router.put("/{grade_id}", response_model=schemas.Grade)
def update_grade(
    grade_id: int, 
    grade: schemas.GradeCreate, 
    db: Session = Depends(get_db)
):
    db_grade = crud.update_grade(db, grade_id, grade)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return db_grade

# DELETE оценки
@router.delete("/{grade_id}")
def delete_grade(grade_id: int, db: Session = Depends(get_db)):
    db_grade = crud.delete_grade(db, grade_id)
    if db_grade is None:
        raise HTTPException(status_code=404, detail="Grade not found")
    return {"message": "Grade deleted successfully"}

# Средний балл по факультету (по названию)
@router.get("/faculty/{faculty_name}/average")
def get_faculty_average_by_name(faculty_name: str, db: Session = Depends(get_db)):
    average = crud.get_average_grade_by_faculty_name(db, faculty_name)
    return {"faculty_name": faculty_name, "average_grade": average}