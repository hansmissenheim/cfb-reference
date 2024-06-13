from fastapi import FastAPI
from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import Player, School, Team
from .save import load_players, load_schools, read_save


async def lifespan(app: FastAPI):
    create_db_and_tables()
    save_data = read_save()
    load_schools(save_data)
    load_players(save_data)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/schools/")
def read_schools():
    with Session(engine) as session:
        return session.exec(select(School)).all()


@app.get("/teams/")
def read_teams():
    with Session(engine) as session:
        return session.exec(select(Team)).all()


@app.get("/players/")
def read_players():
    with Session(engine) as session:
        return session.exec(select(Player)).all()
