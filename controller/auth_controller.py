
from sqlalchemy.orm import Session

from service.auth_service import register_user, login_user


def register_user_controller(
    db: Session,
    name: str,
    email: str,
    password: str
):
    return register_user(db, name, email, password)


def login_user_controller(
    db: Session,
    email: str,
    password: str
):
    return login_user(db, email, password)
