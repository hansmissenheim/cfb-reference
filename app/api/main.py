from fastapi import APIRouter

from app.api.routes import players, schools

api_router = APIRouter()
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
