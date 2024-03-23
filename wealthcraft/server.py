from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from wealthcraft.config import Settings, settings
from contextlib import asynccontextmanager

from wealthcraft.controllers import auth, user, category, expense
from wealthcraft.models import create_all_tables


def server_factory(config: Settings) -> FastAPI:
    settings.set(config)
    meta = config.metadata()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        create_all_tables()

        yield

    app = FastAPI(
        title=meta["name"],
        version=meta["version"],
        summary=meta["summary"],
        description=meta["description"],
        lifespan=lifespan,
        redoc_url="/docs",
        docs_url=None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth.router)
    app.include_router(user.router)
    app.include_router(category.router)
    app.include_router(expense.router)
    return app


app = server_factory(Settings())


@app.get("/")
def api_information():
    return {
        "name": app.title,
        "summary": app.summary,
        "description": app.description,
        "version": app.version,
    }
