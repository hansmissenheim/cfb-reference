from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import Player

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


def get_player(url_slug: str, session: SessionDep) -> Player | None:
    """Retrieve a player by its URL slug."""
    return session.exec(select(Player).where(Player.url_slug == url_slug)).one_or_none()


def get_players_by_letter(
    letter: str, session: SessionDep, limit: int | None = None
) -> Sequence[Player]:
    """Retrieve all players with a last name starting with the specified letter."""
    return session.exec(
        select(Player)
        .where(Player.last_name.startswith(letter))
        .order_by(Player.last_name)
        .limit(limit)
    ).all()


def get_random_players_by_letter(
    letter: str, session: SessionDep, limit: int | None = None
) -> Sequence[Player]:
    """Retrieve all players with a last name starting with the specified letter."""
    return session.exec(
        select(Player)
        .where(Player.last_name.startswith(letter))
        .order_by(func.random())
        .limit(limit)
    ).all()


def get_players_alphabet(
    session: SessionDep, limit: int | None = None
) -> dict[str, Sequence[Player]]:
    """Retrieve players grouped by the first letter of their last name for all letters."""
    alphabet = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    players_dict = {}

    for letter in alphabet:
        players = get_random_players_by_letter(letter, session, limit)
        players_dict[letter] = players

    return players_dict


@router.get("/{url_slug}", response_class=HTMLResponse)
def player(request: Request, url_slug: str, session: SessionDep):
    """Serve the player page with details for the specified player."""
    player = get_player(url_slug, session)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    context = {"player": player}
    return templates.TemplateResponse(request, "player.html", context)


@router.get("", response_class=HTMLResponse)
def all_players(request: Request, session: SessionDep):
    """Serve the page for browsing players by alphabet."""
    context = {"players": get_players_alphabet(session, limit=5)}
    return templates.TemplateResponse(request, "player_all.html", context)


@router.get("/letter/{letter}", response_class=HTMLResponse)
def all_players_with_letter(request: Request, letter: str, session: SessionDep):
    """Serve the page for browsing players by specified letter."""
    context = {"players": get_players_by_letter(letter, session)}
    return templates.TemplateResponse(request, "player_letter.html", context)
