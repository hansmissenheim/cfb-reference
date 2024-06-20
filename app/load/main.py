from typing import BinaryIO

import ncaadb
from sqlmodel import Session, select

from app.database import engine
from app.load.utils import generate_url_slug
from app.models.player import Player, PlayerAttributes
from app.models.school import Coach, School, Stadium, Team


def load_save(save_file: BinaryIO) -> None:
    save_data = ncaadb.read_db(save_file)
    coach_dicts = save_data["COCH"].to_dict(orient="records")
    player_dicts = save_data["PLAY"].to_dict(orient="records")
    school_dicts = save_data["TEAM"].to_dict(orient="records")
    stadium_dicts = save_data["STAD"].to_dict(orient="records")
    if save_data["SEAI"] is None:
        raise ValueError("Error. No SEAI data found in save file.")
    else:
        current_year = 2013 + int(save_data["SEAI"].at[0, "SSYE"])

    load_stadiums(stadium_dicts)
    load_schools(school_dicts, current_year)
    load_players(player_dicts, current_year)
    load_coaches(coach_dicts, current_year)


def load_stadiums(stadium_dicts: list[dict]):
    with Session(engine) as session:
        for stadium_dict in stadium_dicts:
            stadium_in = Stadium(**stadium_dict)

            stadium = session.get(Stadium, stadium_dict["SGID"])
            if stadium:
                update_dict = stadium_in.model_dump()
                stadium.sqlmodel_update(update_dict)
                session.add(stadium)
            else:
                session.add(stadium_in)

        session.commit()


def load_schools(school_dicts: list[dict], year: int):
    with Session(engine) as session:
        for school_dict in school_dicts:
            school_id: int = school_dict["TGID"]
            school_name: str = school_dict["TDNA"]

            school_dict["url_slug"] = generate_url_slug(school_name)
            school_in = School(**school_dict)

            school = session.get(School, school_id)
            if school:
                update_dict = school_in.model_dump()
                school.sqlmodel_update(update_dict)
                session.add(school)
            else:
                session.add(school_in)

            team = session.exec(
                select(Team).where(Team.school_id == school_id).where(Team.year == year)
            ).first()

            if team is None:
                team = Team(school_id=school_id, year=year)
                session.add(team)

        session.commit()


def load_coaches(coach_dicts: list[dict], year: int):
    with Session(engine) as session:
        for coach_dict in coach_dicts:
            coach_in = Coach(**coach_dict)

            coach = session.get(Coach, coach_dict["CCID"])
            if coach:
                update_dict = coach_in.model_dump()
                coach.sqlmodel_update(update_dict)
            else:
                coach = coach_in

            session.add(coach)

            # Only add coach to team if they are the head coach
            if coach.position > 0:
                continue
            team = session.exec(
                select(Team)
                .where(Team.school_id == coach_dict["TGID"])
                .where(Team.year == year)
            ).first()

            if team is not None and team not in coach.teams:
                coach.teams.append(team)

        session.commit()


def player_url_slug(session: Session, first_name: str, last_name: str) -> str:
    url_slug = generate_url_slug(f"{first_name}-{last_name}")
    urls = session.exec(
        select(Player.url_slug).where(Player.url_slug.startswith(url_slug))
    ).all()
    return f"{url_slug}-{len(urls) + 1}"


def load_players(player_dicts: list[dict], year: int):
    with Session(engine) as session:
        for player_dict in player_dicts:
            player_dict["attributes"] = PlayerAttributes(**player_dict)
            player_in = Player(**player_dict)

            player = session.exec(
                select(Player)
                .join(PlayerAttributes, PlayerAttributes.player_id == Player.id)  # type: ignore
                .where(Player.game_id == player_in.game_id)
                .where(PlayerAttributes.PTEN == player_in.attributes.PTEN)
                .where(PlayerAttributes.PPOE == player_in.attributes.PPOE)
                .where(PlayerAttributes.PRNS == player_in.attributes.PRNS)
                .where(PlayerAttributes.PLSY == player_in.attributes.PLSY)
            ).first()

            if player:
                update_dict = player_in.model_dump(
                    exclude={"id", "schools", "teams", "url_slug"}
                )
                player.sqlmodel_update(update_dict)
            else:
                first_name: str = player_dict["PFNA"]
                last_name: str = player_dict["PLNA"]
                player_in.url_slug = player_url_slug(session, first_name, last_name)
                player = player_in

            session.add(player)

            team = session.exec(
                select(Team)
                .where(Team.school_id == player_dict["TGID"])
                .where(Team.year == year)
            ).first()

            if team is not None and team not in player.teams:
                player.teams.append(team)
                if team.school is not None and team.school not in player.schools:
                    player.schools.append(team.school)

        session.commit()
