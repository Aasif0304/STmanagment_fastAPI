
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models.user_model import User

password_hash = PasswordHash.recommended()

# Learning/testing only. Move this secret to .env before deployment.
SECRET_KEY = "replace-this-with-a-long-random-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return None

    user = User(
        name=name,
        email=email,
        password=password_hash.hash(password),
        role="USER"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user or not password_hash.verify(
        password, user.password
    ):
        return None

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    token = jwt.encode(
        {
            "sub": str(user.id),
            "role": user.role,
            "exp": expire
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None or role is None:
            return None

        return {
            "user_id": int(user_id),
            "role": role
        }

    except (jwt.InvalidTokenError, ValueError):
        return None
