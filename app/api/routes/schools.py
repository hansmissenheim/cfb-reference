from collections.abc import Sequence

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select

from app.core.config import settings
from app.database import SessionDep
from app.models import School, Team

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


def get_school(url_slug: str, session: SessionDep) -> School | None:
    """Retrieve a school by its URL slug."""
    return session.exec(select(School).where(School.url_slug == url_slug)).one_or_none()


def get_all_schools(session: SessionDep) -> Sequence[School]:
    """Retrieve all schools."""
    return session.exec(select(School)).all()


def get_team(school_id: int, year: int, session: SessionDep) -> Team | None:
    """Retrieve a team by its school ID and year."""
    return session.exec(
        select(Team).where(Team.school_id == school_id, Team.year == year)
    ).one_or_none()


@router.get("/{school_slug}", response_class=HTMLResponse)
def school(request: Request, school_slug: str, session: SessionDep):
    """Serve the school page with details for the specified school."""
    school = get_school(school_slug, session)
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    context = {"school": school}
    return templates.TemplateResponse(request, "school.html", context)


@router.get("", response_class=HTMLResponse)
def all_schools(request: Request, session: SessionDep):
    """Serve the page for browsing all schools."""
    context = {"schools": get_all_schools(session)}
    return templates.TemplateResponse(request, "school_all.html", context)


@router.get("/{school_slug}/{year}", response_class=HTMLResponse)
def team(request: Request, school_slug: str, year: int, session: SessionDep):
    """Serve the team page with details for the specified team."""
    school = get_school(school_slug, session)
    if school is None:
        raise HTTPException(status_code=404, detail="School not found")
    team = get_team(school.id, year, session)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    context = {"team": team}
    return templates.TemplateResponse(request, "team.html", context)
