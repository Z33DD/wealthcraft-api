from faker import Faker
from wealthcraft.dao import DAO
from wealthcraft.models import User


def test_create_user(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()
    name = faker.name()
    password = "password"

    user = User(
        name=name,
        email=email,
        password=password,
    )

    dao.user.add(user)
    dao.user.commit()

    del user

    user = dao.user.query_one(User.email, email)

    assert user is not None
    assert user.name == name
    assert user.email == email
    assert user.password == password


def test_query_one_user(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()
    name = faker.name()
    password = "password"

    user = User(
        name=name,
        email=email,
        password=password,
    )

    dao.user.add(user)
    dao.user.commit()

    del user

    queried_user = dao.user.query_one(User.email, email)

    assert queried_user is not None


def test_query_one_user_not_exists(dao: DAO, faker: Faker, faker_seed):
    email = faker.email()

    queried_user = dao.user.query_one(User.email, email)

    assert queried_user is None
