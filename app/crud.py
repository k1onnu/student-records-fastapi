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




# ----- task 3


def update_student(db: Session, student_id: int, student_update: schemas.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        db_student.first_name = student_update.first_name
        db_student.last_name = student_update.last_name
        db_student.faculty_id = student_update.faculty_id
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student

# UPDATE и DELETE для оценок
def update_grade(db: Session, grade_id: int, grade_update: schemas.GradeCreate):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if db_grade:
        db_grade.student_id = grade_update.student_id
        db_grade.course_id = grade_update.course_id
        db_grade.grade = grade_update.grade
        db.commit()
        db.refresh(db_grade)
    return db_grade

def delete_grade(db: Session, grade_id: int):
    db_grade = db.query(models.Grade).filter(models.Grade.id == grade_id).first()
    if db_grade:
        db.delete(db_grade)
        db.commit()
    return db_grade

# Студенты по названию факультета
def get_students_by_faculty_name(db: Session, faculty_name: str):
    return db.query(models.Student).join(models.Faculty).filter(
        models.Faculty.name == faculty_name
    ).all()

# Уникальные курсы
def get_unique_courses(db: Session):
    return db.query(models.Course).distinct().all()

# Студенты по курсу с оценкой ниже 30
def get_students_by_course_below_30(db: Session, course_name: str):
    return db.query(models.Student).join(models.Grade).join(models.Course).filter(
        models.Course.name == course_name,
        models.Grade.grade < 30
    ).all()

# Средний балл по факультету (у вас уже есть get_faculty_average_grade)
def get_average_grade_by_faculty_name(db: Session, faculty_name: str):
    result = db.query(
        func.avg(models.Grade.grade).label('average')
    ).join(
        models.Student, models.Grade.student_id == models.Student.id
    ).join(
        models.Faculty, models.Student.faculty_id == models.Faculty.id
    ).filter(
        models.Faculty.name == faculty_name
    ).first()
    
    return result.average if result.average else 0.0