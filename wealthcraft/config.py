from contextvars import ContextVar
from enum import Enum, auto
from typing import Optional
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from sqlalchemy import Engine
from sqlmodel import create_engine


class LogLevel(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class Settings(BaseSettings):
    pg_dsn: Optional[PostgresDsn] = None
    sqlite_dsn: str = "sqlite:///./db.sqlite"
    jwt_secret: str = "secret"
    create_tables: bool = False
    port: int = 5000
    log_level: LogLevel = LogLevel.INFO

    def build_engine(self) -> Engine:
        pg_dsn = str(self.pg_dsn) if self.pg_dsn else None
        db_dsn = pg_dsn or self.sqlite_dsn

        debug = self.log_level == LogLevel.DEBUG

        engine = create_engine(
            db_dsn,
            echo=debug,
            connect_args={
                "check_same_thread": False,
            },
        )

        return engine


settings: ContextVar[Settings] = ContextVar(
    "settings",
    default=Settings(),
)
