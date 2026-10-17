
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from controller.auth_controller import (
    register_user_controller,
    login_user_controller
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register_user(
    name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = register_user_controller(
        db, name, email, password
    )

    if not user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    return {
        "message": "User registered successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


@router.post("/login")
def login_user(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    token = login_user_controller(
        db, email, password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token
