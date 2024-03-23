from datetime import datetime, timezone
import json
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


class RefreshJWTPayload(BaseModel):
    exp: float
    sub: str


def authenticate_user(user: User, password: str) -> tuple[str, str]:
    login_error = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Incorrect password.",
    )

    if not user.password:
        raise login_error
    if not verify_password(user.password, password):
        raise login_error

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    return access_token, refresh_token


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


def verify_refresh_token(token: str) -> RefreshJWTPayload:
    config = settings.get()
    try:
        decoded_token = jwt.decode(
            token,
            config.jwt.secret,
            algorithms=["HS256"],
        )
        return RefreshJWTPayload(**decoded_token)
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


def create_access_token_from_refresh_token(
    refresh_token: str,
    user: User,
) -> str:
    verify_refresh_token(refresh_token)

    token = create_access_token(user)

    return token


def create_refresh_token(user: User) -> str:
    config = settings.get()
    assert user.id

    expiration = datetime.now(timezone.utc) + (config.jwt.refresh_expiration)
    payload = RefreshJWTPayload(
        exp=expiration.timestamp(),
        sub=str(user.id),
    )

    encoded_jwt = jwt.encode(
        payload.model_dump(),
        config.jwt.secret,
        config.jwt.algorithm,
    )
    return encoded_jwt
