from typing import Optional
import uuid
from fastapi import APIRouter, Depends, status
from wealthcraft.controllers import BaseResponse
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_current_user, get_dao
from wealthcraft.models import Category, User

router = APIRouter(prefix="/category")


class CreateUpdateResponse(BaseResponse):
    category: Category


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    category: Category,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> CreateUpdateResponse:
    category.user = user
    dao.category.add(category)

    return CreateUpdateResponse(
        category=category,
        message="Category created!",
    )


class ReadCategories(BaseResponse):
    categories: list[Category]


@router.get("/", status_code=status.HTTP_200_OK)
async def read_categories(
    user: User = Depends(get_current_user),
) -> ReadCategories:

    return ReadCategories(
        categories=user.categories,
    )


class ReadCategory(BaseResponse):
    category: Optional[Category] = None


@router.get("/{category_id}", status_code=status.HTTP_200_OK)
async def read_category(
    category_id: uuid.UUID,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> ReadCategory:
    category = dao.category.get(category_id)

    return ReadCategory(category=category)


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_category(
    category: Category,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> CreateUpdateResponse:
    dao.category.session.add(category)

    return CreateUpdateResponse(category=category)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    category_id: uuid.UUID,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> BaseResponse:
    dao.category.delete(category_id)

    return BaseResponse(message="Category deleted!")
