
from sqlalchemy.orm import Session
from service import fees_service


def create_fee_controller(
    db: Session,
    student_id: int,
    total_fees: int,
    paid_fees: int
):
    return fees_service.create_fee(
        db, student_id, total_fees, paid_fees
    )


def get_all_fees_controller(db: Session):
    return fees_service.get_all_fees(db)


def get_fee_by_id_controller(db: Session, fee_id: int):
    return fees_service.get_fee_by_id(db, fee_id)


def update_fee_controller(
    db: Session,
    fee_id: int,
    total_fees: int,
    paid_fees: int
):
    return fees_service.update_fee(
        db, fee_id, total_fees, paid_fees
    )


def delete_fee_controller(db: Session, fee_id: int):
    return fees_service.delete_fee(db, fee_id)
