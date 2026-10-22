
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from controller import student_controller
from service.auth_dependency import get_current_user, require_admin


router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/")
def create_student(
    
    name: str,
    age: int,
    course: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    return student_controller.create_student_controller(
        db, name, age, course
    )


@router.get("/")
def get_all_students(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return student_controller.get_all_students_controller(db)


@router.get("/with-fees")
def get_students_with_fees(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return student_controller.get_students_with_fees_controller(db)


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    student = student_controller.get_student_by_id_controller(
        db, student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.get("/{student_id}/with-fees")
def get_student_with_fees(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    student = student_controller.update_student_controller(
        db, student_id, name, age, course
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    student = student_controller.delete_student_controller(
        db, student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {"message": "Student deleted successfully"}


@router.post("/{student_id}/upload-image")
def upload_student_image(
    student_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    student = student_controller.get_student_by_id_controller(
        db, student_id
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG and WEBP images are allowed"
        )

    upload_dir = Path(__file__).resolve().parent.parent / "img"
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Unique filename prevents different students' images overwriting each other.
    filename = f"student_{student_id}{extension}"
    file_path = upload_dir / filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        student.img_URL = f"http://127.0.0.1:8000/img/{filename}"

        db.commit()
        db.refresh(student)

        return {
            "message": "Student image uploaded successfully",
            "student_id": student.id,
            "img_url": student.img_URL
        }

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Image upload failed"
        )

    finally:
        file.file.close()
