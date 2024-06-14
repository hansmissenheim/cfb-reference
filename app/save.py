import ncaadb
from sqlmodel import Session, select

from .database import engine
from .models import Player, PlayerAttributes, School, Team


def read_save():
    with open("saves/Year_0-Week_18.USR-DATA", "rb") as f:
        data = ncaadb.read_db(f)
    return data


def load_schools(save_data):
    team_data = save_data["TEAM"]
    seai_data = save_data["SEAI"]
    year = 2023 + int(seai_data.at[0, "SSYE"])

    with Session(engine) as session:
        for row in team_data.itertuples():
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


def load_players(save_data):
    player_data = save_data["PLAY"]
    seai_data = save_data["SEAI"]
    year = 2023 + int(seai_data.at[0, "SSYE"])

    with Session(engine) as session:
        for row in player_data.itertuples():
            team = session.exec(
                select(Team).where(Team.school_id == row.TGID).where(Team.year == year)
            ).first()

            player = session.exec(
                select(Player)
                .join(PlayerAttributes, PlayerAttributes.player_id == Player.id)
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

                if team is not None:
                    player.teams.append(team)
            session.add(player)

        session.commit()
