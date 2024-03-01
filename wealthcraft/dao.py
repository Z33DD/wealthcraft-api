from typing import Any, Generic, TypeVar
from uuid import UUID
from sqlmodel import SQLModel, Session, select

from wealthcraft.models import Category, Expense, User

T = TypeVar("T", bound=SQLModel)


class BaseDAO(Generic[T]):
    session: Session
    model_class: type[SQLModel]
    cache: dict[str, T] = {}

    def __init__(self, session: Session, model_class: type[SQLModel]) -> None:
        self.session = session
        self.model_class = model_class

    def add(self, instance: T) -> None:
        self.session.add(instance)
        self.cache.update({str(instance.id): instance})

    def get(self, id: UUID) -> T | None:
        instance = self.session.get(self.model_class, id)
        if instance:
            self.cache.update({str(id): instance})
        return instance

    def query(self, field: str, value: Any) -> list[T]:
        statement = select(self.model_class).where(field == value)
        results = self.session.exec(statement).all()

        instances = []
        for instance in results:
            instances.append(instance)
            self.cache.update({str(instance.id): instance})

        return instances

    def query_one(self, field: str, value: Any) -> T | None:
        statement = select(self.model_class).where(field == value)
        instance = self.session.exec(statement).first()

        if instance:
            self.cache.update({str(instance.id): instance})

        return instance

    def all(self) -> list[T]:
        statement = select(self.model_class)
        results = self.session.exec(statement).all()

        instances = []
        for instance in results:
            instances.append(instance)
            self.cache.update({str(instance.id): instance})

        return instances

    def delete(self, id: UUID) -> None:
        instance = self.get(id)
        self.session.delete(instance)
        self.cache.pop(str(id))

    def commit(self):
        self.session.commit()


class DAO:
    user: BaseDAO[User]
    category: BaseDAO[Category]
    expense: BaseDAO[Expense]

    def __init__(self, session: Session):
        self.user = BaseDAO[User](model_class=User, session=session)
        self.category = BaseDAO[Category](model_class=Category, session=session)
        self.expense = BaseDAO[Expense](model_class=Expense, session=session)
