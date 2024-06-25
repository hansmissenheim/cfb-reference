from typing import Annotated

from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.sql import func
from sqlmodel import asc, desc, or_, select

from app.core.config import settings
from app.database import SessionDep
from app.load.main import load_save
from app.models import (
    Player,
    PlayerAttributes,
    PlayerSeasonOffenseStats,
    School,
    Team,
    TeamStats,
)

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request, session: SessionDep):
    random_players = session.exec(
        select(Player).order_by(func.random()).limit(12)
    ).all()
    trending_players = session.exec(
        select(Player)
        .join(PlayerAttributes)
        .order_by(desc(PlayerAttributes.overall))
        .limit(10)
    ).all()
    year = session.exec(select(func.max(Team.year))).one()

    passing_leaders = session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .order_by(desc(PlayerSeasonOffenseStats.pass_yards))
        .limit(3)
    ).all()
    rushing_leaders = session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .where(PlayerSeasonOffenseStats.rush_yards < 16000)
        .order_by(desc(PlayerSeasonOffenseStats.rush_yards))
        .limit(3)
    ).all()
    recieving_leaders = session.exec(
        select(Player, PlayerSeasonOffenseStats)
        .join(PlayerSeasonOffenseStats)
        .where(PlayerSeasonOffenseStats.year == year)
        .where(PlayerSeasonOffenseStats.recieving_yards < 16000)
        .order_by(desc(PlayerSeasonOffenseStats.recieving_yards))
        .limit(3)
    ).all()

    top_25 = session.exec(
        select(Team)
        .join(TeamStats)
        .where(Team.year == year)
        .where(TeamStats.bcs_rank > 0)
        .order_by(asc(TeamStats.bcs_rank))
        .limit(25)
    )

    context = {
        "request": request,
        "year": year,
        "random_players": random_players,
        "trending_players": trending_players,
        "passing_leaders": passing_leaders,
        "rushing_leaders": rushing_leaders,
        "recieving_leaders": recieving_leaders,
        "top_25": top_25,
    }
    return templates.TemplateResponse("index.html", context)


@router.post("/search")
def search(request: Request, search: Annotated[str, Form()], session: SessionDep):
    players = session.exec(
        select(Player)
        .where(
            or_(
                Player.first_name.startswith(search),
                Player.last_name.startswith(search),
            )
        )
        .limit(10)
    ).all()
    schools = session.exec(select(School).where(School.name.startswith(search))).all()

    return templates.TemplateResponse(
        "/shared/search_results.html",
        {"request": request, "players": players, "schools": schools},
    )


@router.get("/upload", response_class=HTMLResponse)
def get_upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload")
def upload_file(save_file_upload: UploadFile, session: SessionDep):
    try:
        load_save(save_file_upload.file, session)
    except UnicodeDecodeError:
        return HTMLResponse("Invalid file format. Please upload a NCAA 14 DB file.")
    return {"status": "success"}
