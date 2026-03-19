from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas
from typing import List, Optional

# Faculty CRUD
def get_faculty(db: Session, faculty_id: int):
    return db.query(models.Faculty).filter(models.Faculty.id == faculty_id).first()

def get_faculty_by_name(db: Session, name: str):
    return db.query(models.Faculty).filter(models.Faculty.name == name).first()

def create_faculty(db: Session, faculty: schemas.FacultyCreate):
    db_faculty = models.Faculty(name=faculty.name)
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty

# Course CRUD
def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_course_by_name(db: Session, name: str):
    return db.query(models.Course).filter(models.Course.name == name).first()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(name=course.name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Student CRUD
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_full_name(db: Session, first_name: str, last_name: str):
    return db.query(models.Student).filter(
        models.Student.first_name == first_name,
        models.Student.last_name == last_name
    ).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# Grade CRUD
def get_grades(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Grade).offset(skip).limit(limit).all()

def get_student_grades(db: Session, student_id: int):
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()

def create_grade(db: Session, grade: schemas.GradeCreate):
    db_grade = models.Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

# Statistics
def get_faculty_average_grade(db: Session, faculty_id: int):
    result = db.query(
        func.avg(models.Grade.grade).label('average')
    ).join(
        models.Student, models.Grade.student_id == models.Student.id
    ).filter(
        models.Student.faculty_id == faculty_id
    ).first()
    
    return result.average if result.average else 0

def get_all_faculties_average(db: Session):
    results = db.query(
        models.Faculty.name,
        func.avg(models.Grade.grade).label('average')
    ).join(
        models.Student, models.Faculty.id == models.Student.faculty_id
    ).join(
        models.Grade, models.Student.id == models.Grade.student_id
    ).group_by(
        models.Faculty.id
    ).all()
    
    return [{"faculty_name": r.name, "average_grade": float(r.average)} for r in results]