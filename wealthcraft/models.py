from sqlalchemy import Column, String
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, date
from typing import Optional
from pydantic import EmailStr
import uuid
import enum
from alembic.config import Config
from alembic import command
from wealthcraft.config import settings


def execute_migration(db_url: str):
    config = settings.get()

    alembic_cfg = Config()
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    alembic_cfg.set_main_option(
        "script_location",
        config.full_path("/migrations"),
    )
    command.upgrade(alembic_cfg, "head")


def create_all_tables() -> None:
    config = settings.get()
    engine = config.build_engine()
    SQLModel.metadata.create_all(engine)


class PaymentType(enum.Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        primary_key=True,
        default_factory=uuid.uuid4,
    )
    created_at: datetime = Field(default_factory=datetime.now)
    name: str
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    password: Optional[str]

    categories: list["Category"] = Relationship()
    expenses: list["Expense"] = Relationship()


class Category(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        primary_key=True,
        default_factory=uuid.uuid4,
    )
    name: str
    icon: str = "archive-box"
    color: str = "slate-500"
    split: bool = False
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="categories")
    expenses: list["Expense"] = Relationship()


class Expense(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(
        primary_key=True,
        default_factory=uuid.uuid4,
    )
    date: date
    price: float
    payment_type: PaymentType
    realized: bool = True
    description: Optional[str] = None
    category_id: uuid.UUID = Field(foreign_key="category.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="expenses")
