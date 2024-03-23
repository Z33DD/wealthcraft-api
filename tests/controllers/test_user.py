from fastapi.testclient import TestClient
from fastapi import status
from faker import Faker


def test_create_account(test_client: TestClient, faker: Faker):
    payload = {
        "email": faker.email(),
        "name": faker.name(),
        "password": faker.password(),
    }
    response = test_client.post("/user/", json=payload)

    assert response.status_code == status.HTTP_200_OK


def test_create_user_existing_email(
    test_client: TestClient, faker: Faker, faker_seed: int
):
    # Create a user with a random email
    payload = {
        "email": faker.email(),
        "name": faker.name(),
        "password": faker.password(),
    }
    response = test_client.post("/user/", json=payload)
    assert response.status_code == status.HTTP_200_OK

    # Try to create another user with the same email
    response = test_client.post("/user/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User with this email already exists"
