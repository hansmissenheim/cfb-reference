from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import Game

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/{url_slug}", response_class=HTMLResponse)
def get_game(request: Request, url_slug: str, session: SessionDep):
    game = session.exec(select(Game).where(Game.url_slug == url_slug)).one_or_none()
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    home_team, away_team = None, None
    for team_link in game.team_links:
        if team_link.is_home:
            home_team = team_link.team
        else:
            away_team = team_link.team
    context = {
        "request": request,
        "game": game,
        "home_team": home_team,
        "away_team": away_team,
    }
    return templates.TemplateResponse("game.html", context)
