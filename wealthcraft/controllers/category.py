from fastapi import APIRouter, Depends, status
from wealthcraft.dao import DAO

from wealthcraft.dependencies import get_current_user, get_dao
from wealthcraft.models import Category, User

router = APIRouter(prefix="/category")


@router.post("/")
async def create_category(
    category: Category,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
):
    category.user = user
    dao.category.add(category)

    return {
        "id": category.id,
        "message": "Category created!",
    }, status.HTTP_201_CREATED
