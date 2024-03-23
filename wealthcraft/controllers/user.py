from fastapi import APIRouter, Depends, HTTPException, status
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


@router.post("/")
async def create_user(user_data: CreateUser, dao: DAO = Depends(get_dao)):
    existing_user = dao.user.query_one(User.email, user_data.email)
    if existing_user:
        raise HTTPException(
            detail="User with this email already exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )
    dao.user.add(user)

    return {
        "id": user.id,
        "message": "User created!",
    }, status.HTTP_201_CREATED
