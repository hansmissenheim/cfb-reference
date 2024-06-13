import ncaadb
from sqlmodel import Session

from .database import engine
from .models import Player, School, Team


def read_save():
    with open("data/USR-DATA", "rb") as f:
        data = ncaadb.read_db(f)
    return data


def load_schools(save_data):
    team_data = save_data["TEAM"]
    seai_data = save_data["SEAI"]
    year = 2023 + seai_data.at[0, "SSYE"]

    schools = [
        School(id=row.TGID, name=row.TDNA, nickname=row.TMNA)
        for row in team_data.itertuples()
    ]
    teams = [Team(year=int(year), school_id=school.id) for school in schools]

    with Session(engine) as session:
        session.add_all(schools)
        session.add_all(teams)
        session.commit()


def load_players(save_data):
    player_data = save_data["PLAY"]
    players = [
        Player(
            id=row.PGID,
            first_name=row.PFNA,
            last_name=row.PLNA,
            position=row.PPOS,
            year=row.PYEA,
        )
        for row in player_data.itertuples()
    ]

    with Session(engine) as session:
        session.add_all(players)
        session.commit()
