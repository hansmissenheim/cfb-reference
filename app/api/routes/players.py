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


@router.get("/{player_slug}", response_class=HTMLResponse)
def player(request: Request, player_slug: str, session: SessionDep):
    player = session.exec(
        select(Player).where(Player.url_slug == player_slug)
    ).one_or_none()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    context = {"request": request, "player": player}
    return templates.TemplateResponse("player.html", context)


@router.get("/", response_class=HTMLResponse)
def all_players(request: Request, session: SessionDep):
    alphabet = [chr(i) for i in range(ord("A"), ord("Z") + 1)]
    players_dict = {}

    for letter in alphabet:
        players = session.exec(
            select(Player)
            .where(Player.last_name.startswith(letter))
            .order_by(func.random())
            .limit(5)
        ).all()
        players_dict[letter] = players

    context = {"request": request, "players": players_dict}
    return templates.TemplateResponse("player_all.html", context)


@router.get("/letter/{letter}", response_class=HTMLResponse)
def all_players_with_letter(request: Request, letter: str, session: SessionDep):
    players = session.exec(
        select(Player)
        .where(Player.last_name.startswith(letter))
        .order_by(Player.last_name)
    ).all()

    context = {"request": request, "players": players}
    return templates.TemplateResponse("player_letter.html", context)
