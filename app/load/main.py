from typing import BinaryIO

import ncaadb
from sqlalchemy import delete
from sqlmodel import Session, select

from app.load.utils import (
    game_datetime,
    generate_game_url_slug,
    generate_player_url_slug,
    generate_url_slug,
    get_all_player_stats,
    merge_tables,
)
from app.models.game import Game
from app.models.links import PlayerTeamLink, TeamGameLink
from app.models.player import (
    Player,
    PlayerAttributes,
    PlayerSeasonBlockingStats,
    PlayerSeasonDefenseStats,
    PlayerSeasonKickingStats,
    PlayerSeasonOffenseStats,
    PlayerSeasonReturnStats,
)
from app.models.school import Coach, School, SchoolStats, Team, TeamStats
from app.models.utils import Media


class DataLoader:
    TABLES = [
        "COCH",
        "MCOV",
        "PLAY",
        "PSDE",
        "PSOF",
        "PSOL",
        "PSKI",
        "PSKP",
        "SCHD",
        "SEAI",
        "TEAM",
        "TSSE",
    ]
    data_year = 2013

    save_data: dict[str, list[dict]]
    session: Session

    def __init__(self, save_file: BinaryIO, session: Session):
        ncaa_db_file = ncaadb.read_db(save_file)
        self.save_data = {
            table: ncaa_db_file[table]
            .reset_index()
            .rename(columns={"index": f"{table}_index", "sgmp": f"{table}_sgmp"})
            .to_dict(orient="records")
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

    def load_schools(self):
        team_info = self.save_data["TEAM"]
        team_stats = self.save_data["TSSE"]
        team_dicts = merge_tables("TGID", team_info, team_stats)

        for row in team_dicts:
            school_id: int = row["TGID"]
            school_name: str = row["TDNA"]
            row["url_slug"] = generate_url_slug(school_name)

            school_in_stats = SchoolStats(**row)
            school_in = School(**row, stats=school_in_stats)
            school = self.session.get(School, school_id)
            if school:
                update_dict = school_in.model_dump()
                school.sqlmodel_update(update_dict)
                self.session.add(school)
            else:
                self.session.add(school_in)

            team = self.get_team(school_id)
            team_in_stats = TeamStats(**row)
            if team is None:
                team = Team(
                    school_id=school_id, year=self.data_year, stats=team_in_stats
                )
            else:
                update_dict = team_in_stats.model_dump(exclude={"id", "team_id"})
                team.stats.sqlmodel_update(update_dict)

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

    def load_player_stats(self):
        players = self.session.exec(
            select(Player)
            .join(PlayerTeamLink, Player.id == PlayerTeamLink.player_id)
            .join(Team, Team.id == PlayerTeamLink.team_id)
            .where(Team.year == self.data_year)
        ).all()
        players_dict = {player.game_id: player for player in players}
        player_stats_dicts = get_all_player_stats(self.save_data)

        for player_stats_dict in player_stats_dicts:
            if player := players_dict.get(player_stats_dict["PGID"]):
                if ea_id := player_stats_dict.get("PSOF_index"):
                    new = True
                    stats_in = PlayerSeasonOffenseStats(
                        **player_stats_dict,
                        ea_id=ea_id,
                        sgmp=player_stats_dict["PSOF_sgmp"],
                        year=self.data_year,
                    )
                    for stats in player.stats_offense:
                        if stats.ea_id == stats_in.ea_id:
                            new = False
                            break
                    if new:
                        player.stats_offense.append(stats_in)

                if ea_id := player_stats_dict.get("PSDE_index"):
                    new = True
                    stats_in = PlayerSeasonDefenseStats(
                        **player_stats_dict,
                        ea_id=ea_id,
                        sgmp=player_stats_dict["PSDE_sgmp"],
                        year=self.data_year,
                    )
                    for stats in player.stats_defense:
                        if stats.ea_id == stats_in.ea_id:
                            new = False
                            break
                    if new:
                        player.stats_defense.append(stats_in)

                if ea_id := player_stats_dict.get("PSOL_index"):
                    new = True
                    stats_in = PlayerSeasonBlockingStats(
                        **player_stats_dict,
                        ea_id=ea_id,
                        sgmp=player_stats_dict["PSOL_sgmp"],
                        year=self.data_year,
                    )
                    for stats in player.stats_blocking:
                        if stats.ea_id == stats_in.ea_id:
                            new = False
                            break
                    if new:
                        player.stats_blocking.append(stats_in)

                if ea_id := player_stats_dict.get("PSKI_index"):
                    new = True
                    stats_in = PlayerSeasonKickingStats(
                        **player_stats_dict,
                        ea_id=ea_id,
                        sgmp=player_stats_dict["PSKI_sgmp"],
                        year=self.data_year,
                    )
                    for stats in player.stats_kicking:
                        if stats.ea_id == stats_in.ea_id:
                            new = False
                            break
                    if new:
                        player.stats_kicking.append(stats_in)

                if ea_id := player_stats_dict.get("PSKP_index"):
                    new = True
                    stats_in = PlayerSeasonReturnStats(
                        **player_stats_dict,
                        ea_id=ea_id,
                        sgmp=player_stats_dict["PSKP_sgmp"],
                        year=self.data_year,
                    )
                    for stats in player.stats_return:
                        if stats.ea_id == stats_in.ea_id:
                            new = False
                            break
                    if new:
                        player.stats_return.append(stats_in)
        self.session.add_all(players_dict.values())
        self.session.commit()

    def load_games(self):
        for row in self.save_data["SCHD"]:
            row["date"] = game_datetime(
                year=self.data_year,
                week=row["SEWN"],
                day=row["GDAT"],
                time=row["GTOD"],
            )

            game_in = Game(**row)
            game = self.session.exec(
                select(Game)
                .where(Game.ea_id == game_in.ea_id)
                .where(Game.date == game_in.date)
            ).one_or_none()

            home_team = self.get_team(row["GHTG"])
            away_team = self.get_team(row["GATG"])
            game_in.url_slug = generate_game_url_slug(game_in.date, home_team)

            if game:
                update_dict = game_in.model_dump(exclude={"id"})
                game.sqlmodel_update(update_dict)
                self.session.exec(
                    delete(TeamGameLink).where(TeamGameLink.game_id == game.id)  # type: ignore
                )
            else:
                game = game_in

            if home_team is None and away_team is None:
                self.session.add(game)
            if home_team is not None:
                game_link_home = TeamGameLink(team=home_team, game=game, is_home=True)
                self.session.add(game_link_home)
            if away_team is not None:
                game_link_away = TeamGameLink(team=away_team, game=game, is_home=False)
                self.session.add(game_link_away)

        self.session.commit()

    def load_media(self):
        self.session.exec(delete(Media))
        for row in self.save_data["MCOV"]:
            media = Media(**row, year=self.data_year)
            self.session.add(media)
        self.session.commit()


def load_save(save_file: BinaryIO, session: Session) -> None:
    loader = DataLoader(save_file, session)

    loader.load_schools()
    loader.load_players()
    loader.load_player_stats()
    loader.load_coaches()
    loader.load_games()
    loader.load_media()
