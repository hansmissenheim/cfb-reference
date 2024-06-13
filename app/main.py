from fastapi import FastAPI

from .database import create_db_and_tables
from .models import Player, School
from .save import read_save


async def lifespan(app: FastAPI):
    create_db_and_tables()
    save_data = read_save()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def index():
    return {"message": "Hello, World!"}
