
from fastapi import FastAPI
from database import Base, engine
from models.student_model import Student
from models.fees_model import Fee
from routes.student_routes import router as student_router
from routes.fees_routes import router as fees_router
from routes.auth_routes import router as auth_router

app = FastAPI(title="Student Management ")


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(student_router)
app.include_router(fees_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Student Management System API is running"}
