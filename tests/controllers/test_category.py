import json
from pprint import pprint
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
        headers={"Authentication": f"Bearer {token}"},
    )

    pprint(response.json())

    assert response.status_code == status.HTTP_201_CREATED
