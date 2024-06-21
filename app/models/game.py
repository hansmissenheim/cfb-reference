from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.links import TeamGameLink
    from app.models.school import Stadium


class Game(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ea_id: int = Field(alias="SGNM")
    home_score: int = Field(alias="GHSC")
    away_score: int = Field(alias="GASC")
    stadium_id: int = Field(alias="SGID", foreign_key="stadium.id")
    date: datetime = Field(alias="datetime")

    stadium: "Stadium" = Relationship()
    team_links: list["TeamGameLink"] = Relationship(back_populates="game")
