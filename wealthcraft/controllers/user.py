from http import HTTPStatus
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_dao
from wealthcraft.models import User
from wealthcraft.services.auth import hash_password

router = APIRouter(prefix="/user")


class CreateUser(BaseModel):
    email: EmailStr
    name: str
    password: str


@router.post("/account")
async def create_account(user_data: CreateUser, dao: DAO = Depends(get_dao)):
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )
    dao.user.add(user)

    return {
        "id": user.id,
        "message": "User created!",
    }, HTTPStatus.OK
