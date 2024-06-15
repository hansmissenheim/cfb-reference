from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(settings.TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/upload", response_class=HTMLResponse)
def get_upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload")
def upload_file(save_file_upload: UploadFile):
    return {"filename": save_file_upload.filename}
