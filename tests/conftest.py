import os
import random
import pytest
from typing import Any, Callable, Generator, Optional
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from wealthcraft.config import Settings, settings
from wealthcraft.dao import DAO
from wealthcraft.models import User
from wealthcraft.server import server_factory
from faker import Faker

from wealthcraft.services.auth import hash_password


@pytest.fixture()
def test_client() -> Generator[TestClient, Any, None]:
    config = Settings()

    app = server_factory(config)
    yield TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def db_file():
    yield
    os.remove("./db.sqlite")


@pytest.fixture()
def faker_seed():
    return random.randint(0, 100)


@pytest.fixture
def dao():
    config = settings.get()
    engine = config.build_engine()

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield DAO(session)
        session.commit()


@pytest.fixture
def user_factory(dao: DAO, faker: Faker, faker_seed) -> Callable[..., User]:
    def factory(password: Optional[str] = None) -> User:
        Faker.seed(0)

        if not password:
            password = str(faker.password())

        user = User(
            name=faker.name(),
            email=faker.email(),
            password=hash_password(password),
        )
        dao.user.add(user)
        dao.user.commit()

        return user

    return factory
