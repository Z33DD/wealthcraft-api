import pprint
from typing import Callable
from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker

from wealthcraft.models import User


def test_login(
    test_client: TestClient,
    faker: Faker,
    user_factory: Callable[..., User],
):
    password = faker.password()
    user = user_factory(password)

    payload = {
        "email": user.email,
        "password": password,
    }

    response = test_client.post("/auth/login", json=payload)

    pprint.pp(response.json())

    assert response.status_code == status.HTTP_200_OK
