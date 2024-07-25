from collections.abc import Generator

import pytest
from sqlmodel import Session, create_engine

from app.loading.main import load_save_file
from app.models import SQLModel

TEST_DATABASE_URL = "sqlite:///tests/data/database.db"
TEST_USR_DATA = "tests/data/init.USR-DATA"


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    """Provide a clean database using test data."""
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        with open(TEST_USR_DATA, "rb") as save_file:
            load_save_file(save_file, session)
        yield session

    SQLModel.metadata.drop_all(engine)
