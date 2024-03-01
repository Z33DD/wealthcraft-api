from fastapi import FastAPI
from wealthcraft.config import Settings, settings

from wealthcraft.controllers import auth, user


def server_factory(config: Settings) -> FastAPI:
    settings.set(config)

    app = FastAPI()
    app.include_router(auth.router)
    app.include_router(user.router)
    return app


app = server_factory(Settings())
