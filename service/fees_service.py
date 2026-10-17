
from sqlalchemy.orm import Session
from models.fees_model import Fee
from models.student_model import Student


def sync_student_fees(db: Session, student_id: int):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return

    fee = db.query(Fee).filter(
        Fee.student_id == student_id,
        Fee.is_deleted == False
    ).order_by(Fee.id.desc()).first()

    if fee:
        student.fee_id = fee.id
        student.total_fees = fee.total_fees
        student.paid_fees = fee.paid_fees
        student.pending_fees = fee.pending_fees
    else:
        student.fee_id = None
        student.total_fees = None
        student.paid_fees = None
        student.pending_fees = None


def create_fee(db: Session, student_id: int, total_fees: int, paid_fees: int):
    student = db.query(Student).filter(
        Student.id == student_id,
        Student.is_deleted == False
    ).first()

    if not student:
        return None

    pending_fees = total_fees - paid_fees

    fee = Fee(
        student_id=student_id,
        total_fees=total_fees,
        paid_fees=paid_fees,
        pending_fees=pending_fees,
        is_deleted=False
    )

    db.add(fee)
    db.flush()

    sync_student_fees(db, student_id)

    db.commit()
    db.refresh(fee)
    return fee


def get_all_fees(db: Session):
    return db.query(Fee).filter(
        Fee.is_deleted == False
    ).all()


def get_fee_by_id(db: Session, fee_id: int):
    return db.query(Fee).filter(
        Fee.id == fee_id,
        Fee.is_deleted == False
    ).first()


def update_fee(db: Session, fee_id: int, total_fees: int, paid_fees: int):
    fee = get_fee_by_id(db, fee_id)

    if fee:
        fee.total_fees = total_fees
        fee.paid_fees = paid_fees
        fee.pending_fees = total_fees - paid_fees

        sync_student_fees(db, fee.student_id)

        db.commit()
        db.refresh(fee)

    return fee


def delete_fee(db: Session, fee_id: int):
    fee = get_fee_by_id(db, fee_id)

    if fee:
        student_id = fee.student_id
        fee.is_deleted = True

        sync_student_fees(db, student_id)

        db.commit()
        db.refresh(fee)

    return fee
