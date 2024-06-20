from typing import BinaryIO

import ncaadb
from sqlmodel import Session, select

from app.database import get_db
from app.load.utils import generate_player_url_slug, generate_url_slug
from app.models.player import Player, PlayerAttributes
from app.models.school import Coach, School, Stadium, Team


class DataLoader:
    TABLES = ["COCH", "PLAY", "TEAM", "STAD", "SEAI"]
    data_year = 2013

    save_data: dict[str, list[dict]]
    session: Session

    def __init__(self, save_file: BinaryIO, session: Session):
        ncaa_db_file = ncaadb.read_db(save_file)
        self.save_data = {
            table: ncaa_db_file[table].to_dict(orient="records")
            for table in self.TABLES
        }
        self.data_year += int(self.save_data["SEAI"][0]["SSYE"])
        self.session = session

    def get_team(self, school_id: int) -> Team | None:
        return self.session.exec(
            select(Team)
            .where(Team.school_id == school_id)
            .where(Team.year == self.data_year)
        ).one_or_none()

    def load_stadiums(self):
        for stadium_dict in self.save_data["STAD"]:
            stadium_in = Stadium(**stadium_dict)

            stadium = self.session.get(Stadium, stadium_dict["SGID"])
            if stadium:
                update_dict = stadium_in.model_dump()
                stadium.sqlmodel_update(update_dict)
                self.session.add(stadium)
            else:
                self.session.add(stadium_in)

        self.session.commit()

    def load_schools(self):
        for school_dict in self.save_data["TEAM"]:
            school_id: int = school_dict["TGID"]
            school_name: str = school_dict["TDNA"]

            school_dict["url_slug"] = generate_url_slug(school_name)
            school_in = School(**school_dict)

            school = self.session.get(School, school_id)
            if school:
                update_dict = school_in.model_dump()
                school.sqlmodel_update(update_dict)
                self.session.add(school)
            else:
                self.session.add(school_in)

            team = self.get_team(school_id)
            if team is None:
                team = Team(school_id=school_id, year=self.data_year)
                self.session.add(team)

        self.session.commit()

    def load_coaches(self):
        for coach_dict in self.save_data["COCH"]:
            coach_in = Coach(**coach_dict)

            coach = self.session.get(Coach, coach_dict["CCID"])
            if coach:
                update_dict = coach_in.model_dump()
                coach.sqlmodel_update(update_dict)
            else:
                coach = coach_in

            self.session.add(coach)

            # Only add coach to team if they are the head coach
            if coach.position > 0:
                continue

            team = self.get_team(coach_dict["TGID"])
            if team is not None and team not in coach.teams:
                coach.teams.append(team)

        self.session.commit()

    def load_players(self):
        for player_dict in self.save_data["PLAY"]:
            player_dict["attributes"] = PlayerAttributes(**player_dict)
            player_in = Player(**player_dict)

            player = self.session.exec(
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
                player_in.url_slug = generate_player_url_slug(player_in, self.session)
                player = player_in

            self.session.add(player)

            team = self.get_team(player_dict["TGID"])
            if team is not None and team not in player.teams:
                player.teams.append(team)
                if team.school is not None and team.school not in player.schools:
                    player.schools.append(team.school)

        self.session.commit()


def load_save(save_file: BinaryIO) -> None:
    session = next(get_db())
    loader = DataLoader(save_file, session)

    loader.load_stadiums()
    loader.load_schools()
    loader.load_players()
    loader.load_coaches()
