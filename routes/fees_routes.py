
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from controller import fees_controller
from service.auth_dependency import get_current_user, require_admin

router = APIRouter(prefix="/fees", tags=["Fees"])


@router.post("/")
def create_fee(
    student_id: int,
    total_fees: int,
    paid_fees: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    return fees_controller.create_fee_controller(
        db, student_id, total_fees, paid_fees
    )


@router.get("/")
def get_all_fees(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return fees_controller.get_all_fees_controller(db)


@router.get("/{fee_id}")
def get_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    fee = fees_controller.get_fee_by_id_controller(db, fee_id)

    if not fee:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return fee


@router.put("/{fee_id}")
def update_fee(
    fee_id: int,
    total_fees: int,
    paid_fees: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    fee = fees_controller.update_fee_controller(
        db, fee_id, total_fees, paid_fees
    )

    if not fee:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return fee


@router.delete("/{fee_id}")
def delete_fee(
    fee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    fee = fees_controller.delete_fee_controller(db, fee_id)

    if not fee:
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    return {"message": "Fee record deleted successfully"}
