from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import Base, engine
from models.student_model import Student
from models.fees_model import Fee
from routes.student_routes import router as student_router
from routes.fees_routes import router as fees_router
from routes.auth_routes import router as auth_router
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management",
    lifespan=lifespan
)


app.include_router(student_router)
app.include_router(fees_router)
app.include_router(auth_router)
app.mount("/img", StaticFiles(directory="img"), name="img")

@app.get("/")
def home():
    return {"message": "Student Management System API is running"}
