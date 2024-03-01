from typing import Any, Generator
from sqlmodel import SQLModel, Session

from wealthcraft.config import settings
from wealthcraft.dao import DAO


def get_dao() -> Generator[DAO, Any, None]:
    config = settings.get()
    engine = config.build_engine()

    if config.create_tables:
        SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield DAO(session)
        session.commit()
