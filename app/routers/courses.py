from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app import schemas, crud, models

router = APIRouter(prefix="/courses", tags=["courses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. Уникальные курсы
@router.get("/unique", response_model=List[schemas.Course])
def get_unique_courses(db: Session = Depends(get_db)):
    courses = crud.get_unique_courses(db)
    return courses

# Получить все курсы
@router.get("/", response_model=List[schemas.Course])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Course).offset(skip).limit(limit).all()

# Получить курс по ID
@router.get("/{course_id}", response_model=schemas.Course)
def read_course(course_id: int, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course