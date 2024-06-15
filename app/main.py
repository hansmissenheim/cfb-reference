from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings

from .database import create_db_and_tables
from .save import load_players, load_schools, read_save


async def lifespan(app: FastAPI):
    create_db_and_tables()
    save_data = read_save()
    load_schools(save_data)
    load_players(save_data)
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(api_router)
