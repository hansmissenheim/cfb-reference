from fastapi import APIRouter, Path, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/{first_name}-{last_name}", response_class=HTMLResponse)
def player(request: Request, first_name: str, last_name: str):
    return templates.TemplateResponse("player.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
def all_players(request: Request):
    return templates.TemplateResponse("player_all.html", {"request": request})


@router.get("/{letter}", response_class=HTMLResponse)
def all_players_by_letter(
    request: Request, letter: str = Path(..., min_length=1, max_length=1)
):
    return templates.TemplateResponse("player_letter.html", {"request": request})
