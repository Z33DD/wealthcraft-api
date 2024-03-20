from datetime import date
import os
import random
import string
import pytest
from typing import Any, Callable, Generator, Optional
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session
from wealthcraft.config import Settings, settings
from wealthcraft.dao import DAO
from wealthcraft.models import Category, Expense, PaymentType, User
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
        # Faker.seed(0)

        if not password:
            password = str(faker.password())

        randint = str(random.randint(0, 100))

        user = User(
            name=faker.name(),
            email=randint + faker.email(),
            password=hash_password(password),
        )
        dao.user.add(user)
        dao.user.commit()

        return user

    return factory


@pytest.fixture
def category_factory(dao: DAO) -> Callable[..., Category]:
    def factory(user: User, name: Optional[str] = None) -> Category:
        Faker.seed(0)

        if not name:
            name = "".join([random.choice(string.digits) for _ in range(10)])

        assert user.id

        category = Category(
            name=name,
            user_id=user.id,
        )

        dao.category.add(category)
        dao.category.commit()

        return category

    return factory


@pytest.fixture
def expense_factory(
    dao: DAO, category_factory: Callable[..., Category]
) -> Callable[..., Expense]:
    def factory(
        user: User,
        category: Optional[Category] = None,
        expense_date: Optional[date] = None,
        payment_type: Optional[PaymentType] = None,
        name: Optional[str] = None,
        price: Optional[float] = None,
    ) -> Expense:
        Faker.seed(0)

        if not category:
            category = category_factory(user)
        if not expense_date:
            expense_date = date.today()
        if not name:
            name = "".join([random.choice(string.digits) for _ in range(10)])
        if not payment_type:
            payment_type = PaymentType.CREDIT
        if not price:
            price = random.uniform(1.0, 100)

        assert user.id
        assert category.id

        expense = Expense(
            date=expense_date,
            price=price,
            user_id=user.id,
            category_id=category.id,
            payment_type=payment_type,
        )

        dao.expense.add(expense)
        dao.expense.commit()

        return expense

    return factory
