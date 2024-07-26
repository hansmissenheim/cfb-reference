from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlmodel import Session, create_engine

from app.database import get_db
from app.loading.main import load_save_file
from app.main import app
from app.models import SQLModel

TEST_DATABASE_URL = "sqlite:///tests/data/database.db"
TEST_USR_DATA = "tests/data/init.USR-DATA"


@pytest.fixture(scope="session", autouse=True)
def engine() -> Generator[Engine, None, None]:
    """Create and return a test database engine."""
    engine = create_engine(TEST_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def db(engine) -> Generator[Session, None, None]:
    """Provide a clean database using test data."""
    with Session(engine) as session:
        with open(TEST_USR_DATA, "rb") as save_file:
            load_save_file(save_file, session)
        yield session


@pytest.fixture(scope="module")
def client(engine) -> Generator[TestClient, None, None]:
    """Provide a test client for the FastAPI app."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            test_db = Session(engine)
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
