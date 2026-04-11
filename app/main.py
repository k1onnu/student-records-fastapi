from fastapi import FastAPI
from app.routers import students, grades, courses, auth


app = FastAPI(title = "Student Grades API", description = "API for managing student grades", version = "2.0.0")

app.include_router(students.router)
app.include_router(grades.router)
app.include_router(courses.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Student Grades API", "docs": "/docs"}