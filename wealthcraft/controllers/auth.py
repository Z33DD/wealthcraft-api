from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_dao
from wealthcraft.models import User
from wealthcraft.services.auth import (
    authenticate_user,
    create_access_token_from_refresh_token,
)
from wealthcraft.config import settings

router = APIRouter(prefix="/auth")


class Credentials(BaseModel):
    email: EmailStr
    password: str


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: str
    expiration: int = Field(..., description="Token expiration in seconds")


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate(
    credentials: Credentials, dao: DAO = Depends(get_dao)
) -> LoginResponseSchema:
    user = dao.user.query_one(User.email, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credentials.email} not found.",
        )

    token, refresh_token = authenticate_user(user, credentials.password)
    config = settings.get()

    return LoginResponseSchema(
        access_token=token,
        refresh_token=refresh_token,
        token_type="bearer",
        user_id=str(user.id),
        expiration=config.jwt.expiration.seconds,
    )


class RefreshResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    expiration: int = Field(..., description="Token expiration in seconds")


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(
    refresh_token: str, dao: DAO = Depends(get_dao)
) -> RefreshResponseSchema:
    user = dao.user.query_one(User.id, refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    token = create_access_token_from_refresh_token(refresh_token, user)
    config = settings.get()

    return RefreshResponseSchema(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
        expiration=config.jwt.expiration.seconds,
    )
