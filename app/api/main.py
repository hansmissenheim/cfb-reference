from fastapi import APIRouter

from app.api.routes import games, players, schools, utils

api_router = APIRouter()
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
api_router.include_router(utils.router, prefix="")
