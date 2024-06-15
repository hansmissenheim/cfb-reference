from typing import BinaryIO

import ncaadb
import pandas as pd
from sqlmodel import Session, select

from app.database import engine
from app.models import Player, PlayerAttributes, School, Team


def load_save(save_file: BinaryIO) -> None:
    save_data = ncaadb.read_db(save_file)
    school_data, player_data = save_data["TEAM"], save_data["PLAY"]
    if save_data["SEAI"] is None:
        raise ValueError("Error. No SEAI data found in save file.")
    else:
        current_year = 2013 + int(save_data["SEAI"].at[0, "SSYE"])

    load_schools(school_data, current_year)
    load_players(player_data, current_year)


def load_schools(school_data: pd.DataFrame, year: int):
    with Session(engine) as session:
        for row in school_data.itertuples():
            school = session.exec(select(School).where(School.id == row.TGID)).first()

            if school is None:
                school = School(id=row.TGID, name=row.TDNA, nickname=row.TMNA)
                session.add(school)
            else:
                school.name = row.TDNA
                school.nickname = row.TMNA

            team = session.exec(
                select(Team).where(Team.school_id == row.TGID).where(Team.year == year)
            ).first()

            if team is None:
                team = Team(year=year, school_id=row.TGID)
                session.add(team)

        session.commit()


def load_players(player_data: pd.DataFrame, year: int):
    with Session(engine) as session:
        for row in player_data.itertuples():
            team = session.exec(
                select(Team).where(Team.school_id == row.TGID).where(Team.year == year)
            ).first()

            player = session.exec(
                select(Player)
                .join(PlayerAttributes, PlayerAttributes.player_id == Player.id)  # type: ignore
                .where(Player.game_id == row.PGID)
                .where(PlayerAttributes.PTEN == row.PTEN)
                .where(PlayerAttributes.PPOE == row.PPOE)
                .where(PlayerAttributes.PRNS == row.PRNS)
                .where(PlayerAttributes.PLSY == row.PLSY)
            ).first()

            if player is None:
                player = Player(
                    game_id=row.PGID,
                    first_name=row.PFNA,
                    last_name=row.PLNA,
                    position=row.PPOS,
                    year=row.PYEA,
                    attributes=PlayerAttributes(
                        player_id=row.PGID,
                        PTEN=row.PTEN,
                        PPOE=row.PPOE,
                        PRNS=row.PRNS,
                        PLSY=row.PLSY,
                    ),
                    teams=[team] if team is not None else [],
                )
            else:
                player.first_name = row.PFNA
                player.last_name = row.PLNA
                player.position = row.PPOS
                player.year = row.PYEA

                if team is not None and team not in player.teams:
                    player.teams.append(team)
            session.add(player)

        session.commit()
