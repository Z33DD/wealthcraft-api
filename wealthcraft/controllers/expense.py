from datetime import date
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, status
from wealthcraft.controllers import BaseResponse
from wealthcraft.dao import DAO
from wealthcraft.dependencies import get_current_user, get_dao
from wealthcraft.models import Expense, User

router = APIRouter(prefix="/expense")


class CreateUpdateResponse(BaseResponse):
    expense: Expense


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense: Expense,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> CreateUpdateResponse:
    expense.user = user
    assert user.id is not None
    expense.user_id = user.id
    expense.date = date.fromisoformat(str(expense.date))
    dao.expense.add(expense)

    return CreateUpdateResponse(
        message="Expense created!",
        expense=expense,
    )


@router.get("/", status_code=status.HTTP_200_OK)
async def read_expenses(
    offset: int = 0,
    limit: int = 100,
    user: User = Depends(get_current_user),
    dao: DAO = Depends(get_dao),
) -> list[Expense]:
    expenses = dao.expense.query(
        "user_id",
        user.id,
        offset=offset,
        limit=limit,
    )
    return expenses


class ReadExpense(BaseResponse):
    expense: Optional[Expense] = None


@router.get("/{expense_id}", status_code=status.HTTP_200_OK)
async def read_category(
    expense_id: uuid.UUID,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> ReadExpense:
    expense = dao.expense.get(expense_id)

    return ReadExpense(expense=expense)


@router.put("/", status_code=status.HTTP_201_CREATED)
async def update_category(
    expense: Expense,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> CreateUpdateResponse:
    dao.expense.session.add(expense)

    return CreateUpdateResponse(expense=expense)


@router.delete("/{expense_id}", status_code=status.HTTP_200_OK)
async def delete_category(
    expense_id: uuid.UUID,
    dao: DAO = Depends(get_dao),
    user: User = Depends(get_current_user),
) -> BaseResponse:
    dao.expense.delete(expense_id)

    return BaseResponse(message="Expense deleted!")
