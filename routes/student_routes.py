
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import student_controller
from service.auth_dependency import get_current_user

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(name: str, age: int, course: str, db: Session = Depends(get_db)):
    return student_controller.create_student_controller(db, name, age, course)

@router.get("/")
def get_all_students(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return student_controller.get_all_students_controller(db)

@router.get("/with-fees")
def get_students_with_fees(db: Session = Depends(get_db)):
    return student_controller.get_students_with_fees_controller(db)

@router.get("/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = student_controller.get_student_by_id_controller(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.get("/{student_id}/with-fees")
def get_student_with_fees(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = student_controller.get_student_with_fees_controller(
        db, student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student

@router.put("/{student_id}")
def update_student(
    student_id: int,
    name: str,
    age: int,
    course: str,
    db: Session = Depends(get_db)
):
    student = student_controller.update_student_controller(
        db, student_id, name, age, course
    )
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = student_controller.delete_student_controller(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
