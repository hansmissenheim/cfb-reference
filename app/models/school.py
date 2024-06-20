from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.mapping import STATES
from app.models.links import PlayerTeamLink

if TYPE_CHECKING:
    from app.models.player import Player
    from app.models.school import Coach, School, Stadium, Team


class School(SQLModel, table=True):
    id: int = Field(alias="TGID", primary_key=True)
    name: str = Field(alias="TDNA")
    nickname: str = Field(alias="TMNA")
    url_slug: str = Field(default="", unique=True)
    logo_id: int = Field(alias="TLGL")
    stadium_id: int = Field(alias="SGID", foreign_key="stadium.id")

    stadium: "Stadium" = Relationship()
    teams: list["Team"] = Relationship(back_populates="school")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int

    coach_id: int | None = Field(default=None, foreign_key="coach.id")
    coach: Optional["Coach"] = Relationship(back_populates="teams")
    school_id: int | None = Field(default=None, foreign_key="school.id")
    school: School | None = Relationship(back_populates="teams")
    players: list["Player"] = Relationship(
        back_populates="teams", link_model=PlayerTeamLink
    )


class Coach(SQLModel, table=True):
    id: int = Field(alias="CCID", primary_key=True)
    first_name: str = Field(alias="CFNM")
    last_name: str = Field(alias="CLNM")
    age: int = Field(alias="CAGE")
    position: int = Field(alias="COPS")

    teams: list[Team] = Relationship(back_populates="coach")


class Stadium(SQLModel, table=True):
    id: int = Field(alias="SGID", primary_key=True)
    name: str = Field(alias="SNAM")
    city: str = Field(alias="SCIT")
    state_id: int = Field(alias="STAT")
    nickname: str = Field(alias="STNN", default="")
    capacity: int = Field(alias="SCAP")

    @property
    def state(self) -> str:
        return STATES[self.state_id]
