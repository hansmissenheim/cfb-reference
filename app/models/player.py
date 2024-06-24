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
    stats_offense: list["PlayerSeasonOffenseStats"] = Relationship(
        back_populates="player"
    )
    stats_defense: list["PlayerSeasonDefenseStats"] = Relationship(
        back_populates="player"
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


class PlayerSeasonOffenseStats(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    games_played: int = Field(alias="sgmp")
    completions: int = Field(alias="sacm")
    pass_attempts: int = Field(alias="saat")
    pass_yards: int = Field(alias="saya")
    pass_tds: int = Field(alias="satd")
    interceptions: int = Field(alias="sain")
    longest_pass: int = Field(alias="salN")
    sacks: int = Field(alias="sasa")
    rush_attempts: int = Field(alias="suat")
    rush_yards: int = Field(alias="suya")
    rush_tds: int = Field(alias="sutd")
    longest_rush: int = Field(alias="sulN")
    yards_after_contact: int = Field(alias="suyh")
    twenty_yard_runs: int = Field(alias="su2y")
    broken_tackles: int = Field(alias="subt")
    fumbles: int = Field(alias="sufu")
    receptions: int = Field(alias="scca")
    recieving_yards: int = Field(alias="scya")
    recieving_tds: int = Field(alias="sctd")
    longest_reception: int = Field(alias="scrL")
    yards_after_catch: int = Field(alias="scyc")
    drops: int = Field(alias="scdr")

    player: Player = Relationship(back_populates="stats_offense")


class PlayerSeasonDefenseStats(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    games_played: int = Field(alias="sgmp")
    solo_tackles: int = Field(alias="sdta")
    assisted_tackles: int = Field(alias="sdht")
    tackles_for_loss: int = Field(alias="sdtl")
    sacks: float
    interceptions: int = Field(alias="ssin")
    intercepton_yards: int = Field(alias="ssiy")
    longest_interception: int = Field(alias="sslR")
    pass_deflections: int = Field(alias="sdpd")
    forced_fumbles: int = Field(alias="slff")
    fumbles_recovered: int = Field(alias="slfr")
    fumble_yards: int = Field(alias="slfy")
    blocked_kicks: int = Field(alias="slbl")
    safeties: int = Field(alias="slsa")
    tds: int = Field(alias="ssit")

    player: Player = Relationship(back_populates="stats_defense")
