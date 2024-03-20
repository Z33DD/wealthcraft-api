from datetime import datetime, timedelta, timezone
import json
from typing import Any, Optional
from passlib.context import CryptContext
from fastapi import HTTPException, status
import jwt
from pydantic import BaseModel
from wealthcraft.config import settings
from wealthcraft.models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTPayload(BaseModel):
    exp: float
    user: User


def authenticate_user(user: User, password: str):
    login_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Incorrect password.",
    )

    if not user.password:
        raise login_error
    if not verify_password(user.password, password):
        raise login_error

    return create_access_token(user)


def hash_password(password: str) -> str:
    hashed = password_context.hash(password)

    return hashed


def verify_token(token: str) -> JWTPayload:
    config = settings.get()
    try:
        decoded_token = jwt.decode(
            token,
            config.jwt.secret,
            algorithms=["HS256"],
        )
        return JWTPayload(**decoded_token)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(real_password: str, password: str) -> bool:
    return password_context.verify(password, real_password)


def create_access_token(user: User) -> str:
    config = settings.get()
    exp = datetime.now(tz=timezone.utc) + config.jwt.expiration
    payload = JWTPayload(
        exp=exp.timestamp(),
        user=user,
    )

    token = jwt.encode(
        json.loads(payload.model_dump_json()),
        config.jwt.secret,
        algorithm=config.jwt.algorithm,
    )

    return token


def create_refresh_token(
    subject: str | Any, expires_delta: Optional[timedelta] = None
) -> str:
    config = settings.get()

    expiration = datetime.now(timezone.utc) + (
        expires_delta or config.jwt.refresh_expiration
    )

    to_encode = {"exp": expiration, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        config.jwt.secret,
        config.jwt.algorithm,
    )
    return encoded_jwt
