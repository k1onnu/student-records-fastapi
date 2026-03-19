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