from fastapi import FastAPI
from app.routers import students, grades

app = FastAPI(title="Student Grades API", description="API for managing student grades", version="1.0.0")

app.include_router(students.router)
app.include_router(grades.router)

@app.get("/")
def root():
    return {"message": "Student Grades API", "docs": "/docs"}