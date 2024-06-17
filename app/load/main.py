import re
from typing import BinaryIO

import ncaadb
from sqlmodel import Session, select

from app.database import engine
from app.models import Player, PlayerAttributes, School, Team


def load_save(save_file: BinaryIO) -> None:
    save_data = ncaadb.read_db(save_file)
    school_dicts = save_data["TEAM"].to_dict(orient="records")
    player_dicts = save_data["PLAY"].to_dict(orient="records")
    if save_data["SEAI"] is None:
        raise ValueError("Error. No SEAI data found in save file.")
    else:
        current_year = 2013 + int(save_data["SEAI"].at[0, "SSYE"])

    load_schools(school_dicts, current_year)
    load_players(player_dicts, current_year)


def load_schools(school_dicts: list[dict], year: int):
    with Session(engine) as session:
        for school_dict in school_dicts:
            school_id = school_dict.get("TGID")
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


def url_from_name(session: Session, player_dict: dict) -> str:
    first_name, last_name = player_dict.get("PFNA", ""), player_dict.get("PLNA", "")
    url_name = f"{first_name}-{last_name}".replace(" ", "-").lower()
    url_name = re.sub(r"[^a-z-]", "", url_name)

    urls = session.exec(
        select(Player.url_name).where(Player.url_name.startswith(url_name))
    ).all()
    return f"{url_name}-{len(urls) + 1}"


def load_players(player_dicts: list[dict], year: int):
    with Session(engine) as session:
        for player_dict in player_dicts:
            player_in = Player(
                **player_dict,
                attributes=PlayerAttributes(
                    **player_dict, player_id=player_dict.get("PGID")
                ),
                teams=[],
            )

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
                update_dict = player_in.model_dump(exclude={"id", "teams"})
                player.sqlmodel_update(update_dict)
            else:
                player = player_in

            team = session.exec(
                select(Team)
                .where(Team.school_id == player_dict.get("TGID"))
                .where(Team.year == year)
            ).first()

            if team is not None and team not in player.teams:
                player.teams.append(team)
            session.add(player)

        session.commit()
