from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings

app = FastAPI()
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

app.include_router(api_router)
