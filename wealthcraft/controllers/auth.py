from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_dao
from wealthcraft.models import User
from wealthcraft.services.auth import authenticate_user

router = APIRouter(prefix="/auth")


class Credentials(BaseModel):
    email: EmailStr
    password: str


@router.post("/login")
async def authenticate(credentials: Credentials, dao: DAO = Depends(get_dao)):
    user = dao.user.query_one(User.email, credentials.email)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User with email {credentials.email} not found.",
        )

    token = authenticate_user(user, credentials.password)

    return {"token": token}, 200
