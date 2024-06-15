from fastapi import APIRouter

from app.api.routes import players

api_router = APIRouter()
api_router.include_router(players.router, prefix="/players", tags=["players"])
