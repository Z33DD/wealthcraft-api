import json
from typing import Callable
from fastapi.testclient import TestClient
from fastapi import status

from wealthcraft.models import Category, User
from wealthcraft.services.auth import create_access_token


def test_create_category(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None

    category = Category(
        name="Test Category",
        user_id=user.id,
    )

    token = create_access_token(user)
    response = test_client.post(
        "/category/",
        json=json.loads(category.model_dump_json()),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED

    payload = response.json()

    created_category = Category(**payload["category"])

    assert created_category.name == category.name
    assert str(created_category.user_id) == str(category.user_id) == str(user.id)


def test_read_category(
    user_factory: Callable[..., User],
    category_factory: Callable[..., Category],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    category: Category = category_factory(user, "Test category")

    response = test_client.get(
        f"/category/{category.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    db_category = Category(**payload["category"])

    assert db_category.name == category.name
    assert str(db_category.user_id) == str(category.user_id) == str(user.id)


def test_read_category_that_does_not_exists(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)
    category_id = "dc0577cc-59ee-4617-9619-fd22bba931d2"

    response = test_client.get(
        f"/category/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert payload["category"] is None


def test_read_categories(
    user_factory: Callable[..., User],
    category_factory: Callable[..., Category],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    categories: list[Category] = [
        category_factory(user, f"Test category {1}"),
        category_factory(user, f"Test category {2}"),
        category_factory(user, f"Test category {3}"),
    ]

    response = test_client.get(
        "/category/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    api_categories = payload["categories"]
    assert len(api_categories) == len(categories)

    for index, category in enumerate(categories):
        db_category = Category(**payload["categories"][index])

        assert db_category.name == category.name
        assert str(db_category.user_id) == str(category.user_id) == str(user.id)


def test_read_categories_that_are_empty(
    user_factory: Callable[..., User],
    test_client: TestClient,
):
    user = user_factory()
    assert user.id is not None
    token = create_access_token(user)

    response = test_client.get(
        "/category/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_200_OK

    payload = response.json()

    assert len(payload["categories"]) == 0
