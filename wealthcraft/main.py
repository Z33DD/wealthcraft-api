import pprint
from typing import Optional
import typer
import uvicorn
import pytest
from alembic.config import Config
from alembic import command


from typing_extensions import Annotated

from wealthcraft.config import settings
from wealthcraft.models import *

app = typer.Typer()


@app.command(help="Run the server.")
def serve():
    config = settings.get()

    server = uvicorn.Server(
        uvicorn.Config(
            "wealthcraft.server:app",
            port=config.port,
            log_level=config.log_level.value,
            use_colors=True,
            reload=True,
        )
    )
    server.run()


@app.command(help="Run the server.")
def migrate():
    config = settings.get()

    alembic_cfg = Config()
    alembic_cfg.set_main_option("sqlalchemy.url", config.get_dsn())
    alembic_cfg.set_main_option("script_location", config.full_path("/migrations"))
    command.upgrade(alembic_cfg, "head")


@app.command(help="Executes all tests and verifications.")
def test(
    name: Optional[str] = None,
    warnings: Annotated[bool, typer.Option(help="Stop suppressing warnings.")] = False,
):
    args = [
        "--pylama",
        "--no-header",
    ]

    if name:
        args.append(f"-k {name}")
    if not warnings:
        args.append("--disable-warnings")

    pytest.main(args)


@app.command(help="Displays project information.")
def info():
    config = settings.get()
    meta = config.metadata()

    pprint.pp(meta)


if __name__ == "__main__":
    app()
