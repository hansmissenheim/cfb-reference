from fastapi import FastAPI

from .database import create_db_and_tables
from .models import Player, School


async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Hello, World!"}
