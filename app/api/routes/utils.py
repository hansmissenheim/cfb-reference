from collections.abc import Sequence
from typing import Annotated, Tuple

from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from sqlmodel import asc, desc, or_, select

from app.core.config import settings
from app.database import SessionDep
from app.loading.main import load_save_file
from app.models import (
    Media,
    Player,
    PlayerAttributes,
    PlayerSeasonOffenseStats,
    School,
    Team,
    TeamStats,
)
from app.models.player import PlayerSeasonDefenseStats

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


def get_year(session: SessionDep) -> int:
    """Get the current year from the database."""
    return session.exec(select(func.max(Team.year))).one()


def get_random_players(
    session: SessionDep, limit: int | None = None
) -> Sequence[Player]:
    """Get a list of random players from the database."""
    return session.exec(select(Player).order_by(func.random()).limit(limit)).all()


def get_trending_players(
    session: SessionDep, limit: int | None = None
) -> Sequence[Player]:
    """Get a list of trending players from the database."""
    return session.exec(
        select(Player)
        .join(PlayerAttributes)
        .order_by(desc(PlayerAttributes.overall))
        .limit(limit)
    ).all()


def get_passing_leaders(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Tuple[Player, PlayerSeasonOffenseStats]]:
    """Get a list of passing leaders from the database."""
    return session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .order_by(desc(PlayerSeasonOffenseStats.pass_yards))
        .limit(limit)
    ).all()


def get_rushing_leaders(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Tuple[Player, PlayerSeasonOffenseStats]]:
    """Get a list of passing leaders from the database."""
    return session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .order_by(desc(PlayerSeasonOffenseStats.rush_yards))
        .limit(limit)
    ).all()


def get_receiving_leaders(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Tuple[Player, PlayerSeasonOffenseStats]]:
    """Get a list of passing leaders from the database."""
    return session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .order_by(desc(PlayerSeasonOffenseStats.recieving_yards))
        .limit(limit)
    ).all()


def get_pass_rushing_leaders(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Tuple[Player, PlayerSeasonDefenseStats]]:
    """Get a list of passing leaders from the database."""
    return session.exec(
        select(Player, PlayerSeasonDefenseStats)
        .join(PlayerSeasonDefenseStats)
        .where(PlayerSeasonDefenseStats.year == year)
        .order_by(desc(PlayerSeasonDefenseStats.full_sacks))
        .limit(limit)
    ).all()


def get_coverage_leaders(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Tuple[Player, PlayerSeasonDefenseStats]]:
    """Get a list of passing leaders from the database."""
    return session.exec(
        select(Player, PlayerSeasonDefenseStats)
        .join(PlayerSeasonDefenseStats)
        .where(PlayerSeasonDefenseStats.year == year)
        .order_by(desc(PlayerSeasonDefenseStats.interceptions))
        .limit(limit)
    ).all()


def get_top_25_teams(year: int, session: SessionDep) -> Sequence[Team]:
    """Get the top 25 teams from the database."""
    return session.exec(
        select(Team)
        .join(TeamStats)
        .where(Team.year == year)
        .where(TeamStats.bcs_rank > 0)
        .order_by(asc(TeamStats.bcs_rank))
        .limit(25)
    ).all()


def get_media(
    year: int, session: SessionDep, limit: int | None = None
) -> Sequence[Media]:
    """Get a list of media from the database."""
    return session.exec(
        select(Media)
        .where(Media.year == year)
        .group_by(Media.school_id)  # type: ignore
        .order_by(desc(Media.week))
        .order_by(asc(Media.game_ea_id))
        .limit(limit)
    ).all()


def get_players_from_search(
    search: str, session: SessionDep, limit: int | None = None
) -> Sequence[Player]:
    """Get a list of players from the database based on a search term."""
    return session.exec(
        select(Player)
        .where(
            or_(
                Player.first_name.startswith(search),
                Player.last_name.startswith(search),
            )
        )
        .limit(limit)
    ).all()


def get_schools_from_search(search: str, session: SessionDep) -> Sequence[School]:
    """Get a list of schools from the database based on a search term."""
    return session.exec(select(School).where(School.name.startswith(search))).all()


@router.get("/", response_class=HTMLResponse)
def index(request: Request, session: SessionDep):
    year = get_year(session)
    context = {
        "year": year,
        "random_players": get_random_players(session, limit=12),
        "trending_players": get_trending_players(session, limit=12),
        "passing_leaders": get_passing_leaders(year, session, limit=3),
        "rushing_leaders": get_rushing_leaders(year, session, limit=3),
        "recieving_leaders": get_receiving_leaders(year, session, limit=3),
        "pass_rushing_leaders": get_pass_rushing_leaders(year, session, limit=3),
        "coverage_leaders": get_coverage_leaders(year, session, limit=3),
        "top_25": get_top_25_teams(year, session),
        "media": get_media(year, session, limit=10),
    }
    return templates.TemplateResponse(request, "index.html", context)


@router.post("/search", response_class=HTMLResponse)
def search(request: Request, search: Annotated[str, Form()], session: SessionDep):
    return templates.TemplateResponse(
        request,
        "/shared/search_results.html",
        {
            "players": get_players_from_search(search, session, limit=10),
            "schools": get_schools_from_search(search, session),
        },
    )


@router.get("/upload", response_class=HTMLResponse)
def get_upload_form(request: Request):
    return templates.TemplateResponse(request, "upload.html")


@router.post("/upload")
def upload_file(save_file_upload: UploadFile, session: SessionDep):
    try:
        load_save_file(save_file_upload.file, session)
    except UnicodeDecodeError:
        return HTMLResponse("Invalid file format. Please upload a NCAA 14 DB file.")
    return {"status": "success"}
