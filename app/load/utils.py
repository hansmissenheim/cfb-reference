import re
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.models import Player, Team


def generate_url_slug(string: str) -> str:
    url_slug = string.replace(" ", "-").lower()
    return re.sub(r"[^a-z0-9-]", "", url_slug)


def generate_player_url_slug(player: Player, session: Session) -> str:
    url_slug = generate_url_slug(f"{player.first_name}-{player.last_name}")
    urls = session.exec(
        select(Player.url_slug).where(Player.url_slug.startswith(url_slug))
    ).all()
    return f"{url_slug}-{len(urls) + 1}"


def generate_game_url_slug(date: datetime, team: Team | None) -> str | None:
    if team is None or team.school is None:
        return None

    url_slug = f"{date.strftime('%Y-%m-%d')}-{team.school.url_slug}"
    return url_slug


def game_datetime(year: int, week: int, day: int, time: int) -> datetime:
    schedule_start = datetime(year, 8, 19)
    start_monday = (
        schedule_start - timedelta(days=schedule_start.weekday()) + timedelta(days=7)
    )
    target_time = start_monday + timedelta(weeks=week, days=day, minutes=time)
    return target_time


def merge_tables(key: str, table_1: list[dict], table_2: list[dict]) -> list[dict]:
    lookup = {row[key]: row for row in table_2}
    result = []
    for row in table_1:
        if row[key] in lookup:
            row.update(lookup[row[key]])
        result.append(row)

    for row in table_2:
        if row[key] not in {r[key] for r in table_1}:
            result.append(row)

    return result


def get_all_player_stats(save_data: dict[str, list[dict]]) -> list[dict[str, dict]]:
    player_info = save_data["PLAY"]
    player_offense = save_data["PSOF"]
    player_defense = save_data["PSDE"]
    player_blocking = save_data["PSOL"]
    player_kicking = save_data["PSKI"]
    player_return = save_data["PSKP"]

    player_dicts = merge_tables("PGID", player_offense, player_defense)
    player_dicts = merge_tables("PGID", player_dicts, player_blocking)
    player_dicts = merge_tables("PGID", player_dicts, player_kicking)
    player_dicts = merge_tables("PGID", player_dicts, player_return)
    player_dicts = merge_tables("PGID", player_dicts, player_info)

    return player_dicts
