from fastapi import FastAPI
from wealthcraft.config import Settings, settings

from wealthcraft.controllers import auth, user


def server_factory(config: Settings) -> FastAPI:
    settings.set(config)
    meta = config.metadata()

    app = FastAPI(
        title=meta["name"],
        version=meta["version"],
        description=meta["description"],
    )
    app.include_router(auth.router)
    app.include_router(user.router)
    return app


app = server_factory(Settings())


@app.get("/")
def root():
    return {
        "name": app.title,
        "description": app.description,
        "version": app.version,
    }
