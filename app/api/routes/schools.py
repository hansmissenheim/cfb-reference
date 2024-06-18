from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import School, Team

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/{school_slug}", response_class=HTMLResponse)
def school(request: Request, school_slug: str, session: SessionDep):
    school = session.exec(
        select(School).where(School.url_slug == school_slug)
    ).one_or_none()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    context = {"request": request, "school": school}
    return templates.TemplateResponse("school.html", context)


@router.get("/", response_class=HTMLResponse)
def all_schools(request: Request):
    return templates.TemplateResponse("school_all.html", {"request": request})


@router.get("/{school_slug}/{year}", response_class=HTMLResponse)
def team(request: Request, school_slug: str, year: int, session: SessionDep):
    school = session.exec(
        select(School).where(School.url_slug == school_slug)
    ).one_or_none()
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    team = session.exec(
        select(Team).where(Team.school_id == school.id, Team.year == year)
    ).one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    context = {"request": request, "team": team}
    return templates.TemplateResponse("team.html", context)
