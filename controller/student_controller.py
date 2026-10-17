
from sqlalchemy.orm import Session
from service import student_service


def create_student_controller(db: Session, name: str, age: int, course: str):
    return student_service.create_student(db, name, age, course)


def get_all_students_controller(db: Session):
    return student_service.get_all_students(db)


def get_student_by_id_controller(db: Session, student_id: int):
    return student_service.get_student_by_id(db, student_id)


def update_student_controller(
    db: Session,
    student_id: int,
    name: str,
    age: int,
    course: str
):
    return student_service.update_student(
        db, student_id, name, age, course
    )


def delete_student_controller(db: Session, student_id: int):
    return student_service.delete_student(db, student_id)

def get_students_with_fees_controller(db: Session):
    return student_service.get_students_with_fees(db)

def get_student_with_fees_controller(db: Session,student_id: int):
    return student_service.get_student_with_fees(db, student_id)