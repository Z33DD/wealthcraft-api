from typing import Any, Generator
from sqlmodel import SQLModel, Session
from fastapi.security import OAuth2PasswordBearer

from wealthcraft.config import settings
from wealthcraft.dao import DAO
from wealthcraft.models import User
from wealthcraft.services import auth
from datetime import datetime
from fastapi import Depends, HTTPException, status

import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT",
)


def get_dao() -> Generator[DAO, Any, None]:
    config = settings.get()
    engine = config.build_engine()

    with Session(engine) as session:
        yield DAO(session)
        session.commit()


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    dao: DAO = Depends(get_dao),
) -> User:
    try:
        payload = auth.verify_token(token)

        if datetime.fromtimestamp(payload.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = dao.user.get(payload.user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
