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
    schedule_start = datetime(2013 + year, 8, 19)
    start_monday = (
        schedule_start - timedelta(days=schedule_start.weekday()) + timedelta(days=7)
    )
    target_time = start_monday + timedelta(weeks=week, days=day, minutes=time)
    return target_time
