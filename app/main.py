from fastapi import FastAPI, HTTPException
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


@app.get("/schools/{school_name}")
def read_school(school_name: str):
    name = school_name.title().replace("-", " ")
    with Session(engine) as session:
        statement = select(School).where(School.name == name)
        school = session.exec(statement).first()
        if school is None:
            raise HTTPException(status_code=404, detail="School not found")
        return school


@app.get("/teams/")
def read_teams():
    with Session(engine) as session:
        return session.exec(select(Team)).all()


@app.get("/schools/{school_name}/{year}")
def read_team(school_name: str, year: int):
    name = school_name.title().replace("-", " ")

    with Session(engine) as session:
        statement = select(School).where(School.name == name)
        school = session.exec(statement).first()
        if school is None:
            raise HTTPException(status_code=404, detail="School not found")
        statement = (
            select(Team)
            .where(Team.school_id == school.id)
            .where(Team.year == int(year))
        )
        team = session.exec(statement).first()
        if team is None:
            raise HTTPException(status_code=404, detail="Team not found")
        return team


@app.get("/players/")
def read_players():
    with Session(engine) as session:
        return session.exec(select(Player)).all()


@app.get("/players/{first_name}-{last_name}")
def read_player(first_name: str, last_name: str):
    first_name = first_name.title()
    last_name = last_name.title()

    with Session(engine) as session:
        statement = (
            select(Player)
            .where(Player.first_name == first_name)
            .where(Player.last_name == last_name)
        )
        player = session.exec(statement).first()
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
