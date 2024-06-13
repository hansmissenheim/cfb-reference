import ncaadb
from sqlmodel import Session

from .database import engine
from .models import School


def read_save():
    with open("data/USR-DATA", "rb") as f:
        data = ncaadb.read_db(f)
    return data


def load_schools(save_data):
    team_data = save_data["TEAM"]
    schools = [
        School(id=row.TGID, name=row.TDNA, nickname=row.TMNA)
        for row in team_data.itertuples()
    ]

    with Session(engine) as session:
        session.add_all(schools)
        session.commit()
