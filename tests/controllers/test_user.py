from fastapi.testclient import TestClient
from faker import Faker


def test_create_account(test_client: TestClient, faker: Faker):
    payload = {
        "email": faker.email(),
        "name": faker.name(),
        "password": faker.password(),
    }
    response = test_client.post("/user/account", json=payload)

    assert response.status_code == 200
