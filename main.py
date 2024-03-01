from typing import Optional
import typer
import uvicorn
import pytest

from wealthcraft.config import settings

app = typer.Typer()


@app.command()
def run():
    config = settings.get()

    server = uvicorn.Server(
        uvicorn.Config(
            "wealthcraft.server:app",
            port=config.port,
            log_level=config.log_level.value,
        )
    )
    server.run()


@app.command()
def test(test_name: Optional[str] = None):
    args = [
        "--pylama",
    ]
    if test_name:
        args.append(f"-k {test_name}")
    pytest.main(args)


if __name__ == "__main__":
    app()
