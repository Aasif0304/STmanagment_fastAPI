
from sqlalchemy.orm import Session
from models.student_model import Student
from models.fees_model import Fee

def create_student(db: Session, name: str, age: int, course: str):
    student = Student(
        name=name,
        age=age,
        course=course,
        is_deleted=False
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_all_students(db: Session):
    return db.query(Student).filter(
        Student.is_deleted == False
    ).all()


def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id,
        Student.is_deleted == False
    ).first()


def update_student(
    db: Session,
    student_id: int,
    name: str,
    age: int,
    course: str
):
    student = get_student_by_id(db, student_id)

    if student:
        student.name = name
        student.age = age
        student.course = course
        db.commit()
        db.refresh(student)

    return student


def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)

    if student:
        student.is_deleted = True
        db.commit()
        db.refresh(student)

    return student

def get_students_with_fees(db: Session):
    results = (
        db.query(Student, Fee)
        .outerjoin(
            Fee,
            (Student.id == Fee.student_id) &
            (Fee.is_deleted == False)
        )
        .filter(Student.is_deleted == False)
        .all()
    )

    response = []

    for student, fee in results:
        student_data = {
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "course": student.course,
            "fees": None
        }

        if fee:
            student_data["fees"] = {
                "id": fee.id,
                "total_fees": fee.total_fees,
                "paid_fees": fee.paid_fees,
                "pending_fees": fee.pending_fees
            }

        response.append(student_data)

    return response

def get_student_with_fees(db: Session, student_id: int):
    result = (
        db.query(Student, Fee)
        .join(
            Fee,
            (Student.id == Fee.student_id) &
            (Fee.is_deleted == False)
        )
        .filter(
            Student.id == student_id,
            Student.is_deleted == False
        )
        .first()
    )

    if not result:
        return None

    student, fee = result

    return {
        "id": student.id,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "fees": {
            "id": fee.id,
            "total_fees": fee.total_fees,
            "paid_fees": fee.paid_fees,
            "pending_fees": fee.pending_fees
        } if fee else None
    }