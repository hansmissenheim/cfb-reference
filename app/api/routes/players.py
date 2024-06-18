from fastapi import APIRouter, HTTPException, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import Player

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/{url_name}", response_class=HTMLResponse)
def player(request: Request, url_name: str, session: SessionDep):
    player = session.exec(
        select(Player).where(Player.url_name == url_name)
    ).one_or_none()
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    context = {"request": request, "player": player}
    return templates.TemplateResponse("player.html", context)


@router.get("/", response_class=HTMLResponse)
def all_players(request: Request):
    return templates.TemplateResponse("player_all.html", {"request": request})


@router.get("/{letter}", response_class=HTMLResponse)
def all_players_by_letter(
    request: Request, letter: str = Path(..., min_length=1, max_length=1)
):
    return templates.TemplateResponse("player_letter.html", {"request": request})
