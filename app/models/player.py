from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.mapping import HOMETOWNS, POSITIONS
from app.models.links import PlayerSchoolLink, PlayerTeamLink

if TYPE_CHECKING:
    from app.models.school import School, Team


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(alias="POID")
    first_name: str = Field(alias="PFNA")
    last_name: str = Field(alias="PLNA")
    position_id: int = Field(alias="PPOS")
    height: int = Field(alias="PHGT")
    weight: int = Field(alias="PWGT")
    face_id: int = Field(alias="PGHE")
    jersey_number: int = Field(alias="PJEN")
    year: int = Field(alias="PYEA")
    hometown_id: int = Field(alias="RCHD")
    url_slug: str = Field(default="", unique=True)

    # Ratings attributes
    attributes: "PlayerAttributes" = Relationship(back_populates="player")
    schools: list["School"] = Relationship(
        back_populates=None, link_model=PlayerSchoolLink
    )
    teams: list["Team"] = Relationship(
        back_populates="players", link_model=PlayerTeamLink
    )

    @property
    def hometown(self) -> str:
        return HOMETOWNS[self.hometown_id]

    @property
    def position(self) -> str:
        return POSITIONS[self.position_id]

    @property
    def height_ft(self) -> str:
        return f"{self.height // 12}-{self.height % 12}"

    @property
    def height_cm(self) -> int:
        return round(self.height * 2.54)

    @property
    def weight_lbs(self) -> int:
        return self.weight + 160

    @property
    def weight_kg(self) -> int:
        return round((self.weight + 160) * 0.45359237)


class PlayerAttributes(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    PTEN: int
    PPOE: int
    PRNS: int
    PLSY: int

    player: Player = Relationship(back_populates="attributes")
