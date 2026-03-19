import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, schemas, crud

def load_csv_to_db(csv_path: str):
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Dictionary to store unique faculties and courses
        faculties = {}
        courses = {}
        students = {}
        
        for _, row in df.iterrows():
            # Get or create faculty
            faculty_name = row['Факультет']
            if faculty_name not in faculties:
                faculty = crud.get_faculty_by_name(db, faculty_name)
                if not faculty:
                    faculty = crud.create_faculty(db, schemas.FacultyCreate(name=faculty_name))
                faculties[faculty_name] = faculty
            
            # Get or create course
            course_name = row['Курс']
            if course_name not in courses:
                course = crud.get_course_by_name(db, course_name)
                if not course:
                    course = crud.create_course(db, schemas.CourseCreate(name=course_name))
                courses[course_name] = course
            
            # Get or create student
            student_key = (row['Фамилия'], row['Имя'])
            if student_key not in students:
                student = crud.get_student_by_full_name(db, row['Имя'], row['Фамилия'])
                if not student:
                    student = crud.create_student(db, schemas.StudentCreate(
                        first_name=row['Имя'],
                        last_name=row['Фамилия'],
                        faculty_id=faculties[faculty_name].id
                    ))
                students[student_key] = student
            
            # Create grade
            grade = schemas.GradeCreate(
                student_id=students[student_key].id,
                course_id=courses[course_name].id,
                grade=int(row['Оценка'])
            )
            crud.create_grade(db, grade)
        
        print(f"Successfully loaded {len(df)} records into database")
        
    finally:
        db.close()

if __name__ == "__main__":
    load_csv_to_db("students.csv")