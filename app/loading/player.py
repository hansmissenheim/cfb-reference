from sqlmodel import Session, func, select

from app.loading.school import all_teams_dict
from app.loading.utils import BaseLoader, generate_url_slug
from app.models import (
    Player,
    PlayerAttributes,
    PlayerSeasonBlockingStats,
    PlayerSeasonDefenseStats,
    PlayerSeasonKickingStats,
    PlayerSeasonOffenseStats,
    PlayerSeasonReturnStats,
    PlayerTeamLink,
    Team,
)

PLAYER_STATS_CONFIG = [
    {"model": PlayerSeasonOffenseStats, "attribute": "stats_offense", "table": "PSOF"},
    {"model": PlayerSeasonDefenseStats, "attribute": "stats_defense", "table": "PSDE"},
    {
        "model": PlayerSeasonBlockingStats,
        "attribute": "stats_blocking",
        "table": "PSOL",
    },
    {"model": PlayerSeasonKickingStats, "attribute": "stats_kicking", "table": "PSKI"},
    {"model": PlayerSeasonReturnStats, "attribute": "stats_return", "table": "PSKP"},
]


class PlayerLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.players = all_players_dict(session)
        self.teams = all_teams_dict(session)
        self.url_cache = self._initialize_url_cache(session)

    def _initialize_url_cache(self, session):
        url_counts = session.exec(
            select(
                Player.first_name, Player.last_name, func.count("*").label("count")
            ).group_by(Player.first_name, Player.last_name)
        ).all()
        url_cache = {
            generate_url_slug(f"{first_name}-{last_name}"): count
            for first_name, last_name, count in url_counts
        }
        return url_cache

    def _generate_player_url_slug(self, player: Player) -> str:
        url_slug = generate_url_slug(f"{player.first_name}-{player.last_name}")
        count = self.url_cache.get(url_slug, 0)
        self.url_cache[url_slug] = count + 1

        return f"{url_slug}-{count + 1}"

    def load(self):
        for row in self.save_data["PLAY"]:
            self.process_player(row)
        self.session.commit()

    def process_player(self, row):
        player_in = Player(**row)
        player_in.attributes = PlayerAttributes(**row)

        player = self.update_or_create_player(player_in)
        self.add_school_to_player(player, row["TGID"])
        self.session.add(player)

    def update_or_create_player(self, player_in):
        if player := self.players.get(
            (
                player_in.game_id,
                player_in.attributes.PTEN,
                player_in.attributes.PPOE,
                player_in.attributes.PRNS,
                player_in.attributes.PLSY,
            )
        ):
            update_dict = player_in.model_dump(
                exclude={"id", "schools", "teams", "url_slug"}
            )
            player.sqlmodel_update(update_dict)
        else:
            player_in.url_slug = self._generate_player_url_slug(player_in)
            player = player_in
        return player

    def add_school_to_player(self, player, school_id):
        team = self.teams.get((school_id, self.year))
        if team and team not in player.teams:
            player.teams.append(team)
            if team.school is not None and team.school not in player.schools:
                player.schools.append(team.school)


class PlayerStatsLoader(BaseLoader):
    def __init__(self, save_data, year: int, session: Session):
        super().__init__(save_data, year, session)
        self.players = all_players_by_year_dict(year, session)

    def load(self):
        for stat_config in PLAYER_STATS_CONFIG:
            for row in self.save_data[stat_config["table"]]:
                self.process_player_stat(row, stat_config)
        self.session.commit()

    def process_player_stat(self, row, stat_config):
        player_with_team = self.players.get(row["PGID"])
        if player_with_team is None:
            return

        team_id = player_with_team["team_id"]
        player = player_with_team["player"]
        stats_in = stat_config["model"](**row, team_id=team_id, year=self.year)

        new = True
        for stats in getattr(player, stat_config["attribute"], []):
            if stats.ea_id == stats_in.ea_id:
                new = False
                break
        if new:
            stats = getattr(player, stat_config["attribute"], [])
            stats.append(stats_in)
            setattr(player, stat_config["attribute"], stats)

        self.session.add(player)


def all_players_dict(session: Session):
    players = session.exec(select(Player)).all()
    return {
        (
            player.game_id,
            player.attributes.PTEN,
            player.attributes.PPOE,
            player.attributes.PRNS,
            player.attributes.PLSY,
        ): player
        for player in players
    }


def all_players_by_year_dict(year: int, session: Session):
    players_with_teams = session.exec(
        select(Player, Team.id)
        .join(PlayerTeamLink, Player.id == PlayerTeamLink.player_id)  # type: ignore
        .join(Team, Team.id == PlayerTeamLink.team_id)  # type: ignore
        .where(Team.year == year)
    ).all()
    return {
        player.ea_id: {"player": player, "team_id": team_id}
        for player, team_id in players_with_teams
    }
