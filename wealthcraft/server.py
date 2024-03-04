from fastapi import FastAPI
from wealthcraft.config import Settings, settings
from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from wealthcraft.controllers import auth, user, category
from wealthcraft.models import *


def server_factory(config: Settings) -> FastAPI:
    settings.set(config)
    meta = config.metadata()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine = config.build_engine()
        SQLModel.metadata.create_all(engine)

        yield

    app = FastAPI(
        title=meta["name"],
        version=meta["version"],
        description=meta["description"],
        lifespan=lifespan,
    )
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(category.router)
    return app


app = server_factory(Settings())


@app.get("/")
def root():
    return {
        "name": app.title,
        "description": app.description,
        "version": app.version,
    }
