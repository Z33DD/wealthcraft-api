import pprint
from typing import Optional
import typer
import uvicorn
import pytest

from wealthcraft.config import settings

app = typer.Typer()


@app.command(help="Run the server.")
def serve():
    config = settings.get()

    server = uvicorn.Server(
        uvicorn.Config(
            "wealthcraft.server:app",
            port=config.port,
            log_level=config.log_level.value,
        )
    )
    server.run()


@app.command(help="Executes all tests and verifications.")
def test(test_name: Optional[str] = None):
    args = [
        "--pylama",
    ]
    if test_name:
        args.append(f"-k {test_name}")
    pytest.main(args)


@app.command(help="Displays project information.")
def info():
    config = settings.get()
    meta = config.metadata()

    pprint.pp(meta)


if __name__ == "__main__":
    app()
