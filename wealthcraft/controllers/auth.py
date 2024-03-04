from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_dao
from wealthcraft.models import User
from wealthcraft.services.auth import authenticate_user

router = APIRouter(prefix="/auth")


class Credentials(BaseModel):
    email: EmailStr
    password: str


class ResponseSchema(BaseModel):
    access_token: str
    token_type: str
    user_id: str


@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate(
    credentials: Credentials, dao: DAO = Depends(get_dao)
) -> ResponseSchema:
    user = dao.user.query_one(User.email, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {credentials.email} not found.",
        )

    token = authenticate_user(user, credentials.password)

    return ResponseSchema(
        access_token=token,
        token_type="bearer",
        user_id=str(user.id),
    )
