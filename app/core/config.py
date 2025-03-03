from pathlib import Path

from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    APP_DIR: Path = APP_DIR
    DB_PATH: Path = APP_DIR.parent / "db"
    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATES_DIR: Path = APP_DIR / "templates"


settings = Settings()
