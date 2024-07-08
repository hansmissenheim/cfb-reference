from sqlmodel import Session, func, select

from app.loading.school import all_teams_dict
from app.loading.utils import BaseLoader, generate_url_slug
from app.models import Player, PlayerAttributes


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
