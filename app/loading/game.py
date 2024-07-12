from datetime import datetime, timedelta

from sqlalchemy import delete
from sqlmodel import Session, select

from app.loading.school import all_teams_dict
from app.loading.utils import BaseLoader
from app.models import Game, Team, TeamGameLink


class GameLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.games = all_games_dict(session)
        self.teams = all_teams_dict(session)

    def load(self):
        for row in self.save_data["SCHD"]:
            self.process_game(row)
        self.session.commit()

    def process_game(self, row):
        date = game_datetime(self.year, row["SEWN"], row["GDAT"], row["GTOD"])
        game_in = Game(**row, datetime=date)

        home_team = self.teams.get((row["GHTG"], self.year))
        away_team = self.teams.get((row["GATG"], self.year))
        game_in.url_slug = generate_game_url_slug(game_in.date, home_team)

        game = self.update_or_create_game(game_in)
        self.create_game_links(game, home_team, away_team)
        self.session.add(game)

    def update_or_create_game(self, game_in):
        if game := self.games.get((game_in.ea_id, game_in.date)):
            update_dict = game_in.model_dump(exclude={"id"})
            game.sqlmodel_update(update_dict)
            self.session.exec(
                delete(TeamGameLink).where(TeamGameLink.game_id == game.id)  #  type: ignore
            )
        else:
            game = game_in
        return game

    def create_game_links(
        self, game: Game, home_team: Team | None, away_team: Team | None
    ):
        if home_team:
            self.session.add(TeamGameLink(team=home_team, game=game, is_home=True))
        if away_team:
            self.session.add(TeamGameLink(team=away_team, game=game, is_home=False))


def all_games_dict(session: Session):
    games = session.exec(select(Game)).all()
    return {(game.ea_id, game.date): game for game in games}


def game_datetime(year: int, week: int, day: int, time: int) -> datetime:
    schedule_start = datetime(year, 8, 19)
    start_monday = (
        schedule_start - timedelta(days=schedule_start.weekday()) + timedelta(days=7)
    )
    target_time = start_monday + timedelta(weeks=week, days=day, minutes=time)
    return target_time


def generate_game_url_slug(date: datetime, team: Team | None) -> str | None:
    if not team or not team.school:
        return None

    url_slug = f"{date.strftime('%Y-%m-%d')}-{team.school.url_slug}"
    return url_slug
