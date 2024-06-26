from collections.abc import Generator
from typing import Annotated

from alembic import command
from alembic.config import Config
from fastapi import Depends
from sqlmodel import Session, create_engine

from app.core.config import settings

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///db/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def run_migrations() -> None:
    alembic_config_path = settings.APP_DIR.parent / "alembic.ini"
    alembic_config = Config(alembic_config_path)
    command.upgrade(alembic_config, "head")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
