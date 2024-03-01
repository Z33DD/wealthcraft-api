import pprint
from typing import Callable
from fastapi.testclient import TestClient
from faker import Faker

from wealthcraft.models import User


def test_login(
    # dao: DAO,
    test_client: TestClient,
    faker: Faker,
    user_factory: Callable[..., User],
):
    password = faker.password()
    user = user_factory(password)

    # pprint.pp(dao.user.all())

    payload = {
        "email": user.email,
        "password": password,
    }

    response = test_client.post("/auth/login", json=payload)

    pprint.pp(response.json())

    assert response.status_code == 200
