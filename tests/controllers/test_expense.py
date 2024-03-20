import json
from typing import Callable
from fastapi.testclient import TestClient
from fastapi import status

from wealthcraft.models import Expense, User
from wealthcraft.services.auth import create_access_token


def test_create_expense(
    user_factory: Callable[..., User],
    expense_factory: Callable[..., Expense],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    expense = expense_factory(user)
    assert expense.date

    response = test_client.post(
        "/expense/",
        json=json.loads(expense.model_dump_json()),
        headers={"Authorization": f"Bearer {token}"},
    )

    payload = response.json()
    assert response.status_code == status.HTTP_201_CREATED, payload["detail"]

    created_expense = Expense(**payload["expense"])

    assert created_expense.name == expense.name
    assert str(created_expense.user_id) == str(expense.user_id) == str(user.id)


def test_read_expense(
    user_factory: Callable[..., User],
    expense_factory: Callable[..., Expense],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    expense: Expense = expense_factory(user, name="Test expense")

    response = test_client.get(
        f"/expense/{expense.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    db_expense = Expense(**payload["expense"])

    assert db_expense.description == expense.description
    assert str(db_expense.user_id) == str(expense.user_id) == str(user.id)


def test_read_expense_that_does_not_exists(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)
    expense_id = "dc0577cc-59ee-4617-9619-fd22bba931d2"

    response = test_client.get(
        f"/expense/{expense_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert payload["expense"] is None


def test_read_expenses(
    user_factory: Callable[..., User],
    expense_factory: Callable[..., Expense],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    expenses: list[Expense] = [
        expense_factory(user),
        expense_factory(user),
        expense_factory(user),
    ]

    response = test_client.get(
        "/expense/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    api_expenses = payload["expenses"]
    assert len(api_expenses) == len(expenses)

    for index, expense in enumerate(expenses):
        db_expense = Expense(**payload["expenses"][index])

        assert db_expense.description == expense.description
        assert str(db_expense.user_id) == str(expense.user_id) == str(user.id)


def test_read_expenses_that_are_empty(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    response = test_client.get(
        "/expense/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert len(payload["expenses"]) == 0
