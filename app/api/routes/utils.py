from typing import Annotated

from fastapi import APIRouter, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import or_, select

from app.core.config import settings
from app.database import SessionDep
from app.load.main import load_save
from app.models import Player, School

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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
