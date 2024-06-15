from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/{school_name}", response_class=HTMLResponse)
def school(request: Request, school_name: str):
    return templates.TemplateResponse("school.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
def all_schools(request: Request):
    return templates.TemplateResponse("school_all.html", {"request": request})


@router.get("/{school_name}/{team_year}", response_class=HTMLResponse)
def team(request: Request, school_name: str, team_year: int):
    return templates.TemplateResponse("team.html", {"request": request})
