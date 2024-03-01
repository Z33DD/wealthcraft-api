from http import HTTPStatus
import bcrypt
from fastapi import HTTPException
import jwt
from wealthcraft.config import settings
from wealthcraft.models import User


def authenticate_user(user: User, password: str):
    login_error = HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail="Incorrect password.",
    )

    if not user.password:
        raise login_error
    if not __passwords_matches(user.password, password):
        raise login_error

    return __generate_jwt_token(user)


def hash_password(plain_password: str) -> bytes:
    encoded_password = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(encoded_password, bcrypt.gensalt(14))

    return hashed


def __passwords_matches(real_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), real_password)


def __generate_jwt_token(user: User) -> str:
    config = settings.get()
    payload = {"user": user.model_dump_json(exclude={"password"})}

    token = jwt.encode(
        payload,
        config.jwt_secret,
        algorithm="HS256",
    )

    return token
