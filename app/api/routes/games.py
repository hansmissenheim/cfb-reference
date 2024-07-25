from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import Game, Team

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


def get_game(url_slug: str, session: SessionDep) -> Game | None:
    """Retrieve a game by its URL slug."""
    return session.exec(select(Game).where(Game.url_slug == url_slug)).one_or_none()


def get_teams_from_game(game: Game) -> tuple[Team | None, Team | None]:
    """Extract and return the home and away teams from a game."""
    home_team, away_team = None, None
    for team_link in game.team_links:
        if team_link.is_home:
            home_team = team_link.team
        else:
            away_team = team_link.team
    return home_team, away_team


@router.get("/{url_slug}", response_class=HTMLResponse)
def game_page(request: Request, url_slug: str, session: SessionDep) -> HTMLResponse:
    """Serve the game page with details for the specified game."""
    game = get_game(url_slug, session)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    home_team, away_team = get_teams_from_game(game)
    context = {
        "request": request,
        "game": game,
        "home_team": home_team,
        "away_team": away_team,
    }
    return templates.TemplateResponse("game.html", context)
