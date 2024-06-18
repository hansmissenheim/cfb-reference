from sqlmodel import Field, Relationship, SQLModel

from app.mapping import HOMETOWNS, POSITIONS, STATES


class PlayerSchoolLink(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    school_id: int | None = Field(
        default=None, foreign_key="school.id", primary_key=True
    )


class PlayerTeamLink(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)


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


class Stadium(SQLModel, table=True):
    id: int = Field(alias="SGID", primary_key=True)
    name: str = Field(alias="SNAM")
    city: str = Field(alias="SCIT")
    state_id: int = Field(alias="STAT")
    nickname: str = Field(alias="STNN", default="")
    capcity: int = Field(alias="SCAP")

    @property
    def state(self) -> str:
        return STATES[self.state_id]


class School(SQLModel, table=True):
    id: int = Field(alias="TGID", primary_key=True)
    name: str = Field(alias="TDNA")
    nickname: str = Field(alias="TMNA")
    url_slug: str = Field(default="", unique=True)
    stadium_id: int = Field(alias="SGID", foreign_key="stadium.id")

    stadium: Stadium = Relationship()
    teams: list["Team"] = Relationship(back_populates="school")


class Coach(SQLModel, table=True):
    id: int = Field(alias="CCID", primary_key=True)
    first_name: str = Field(alias="CFNM")
    last_name: str = Field(alias="CLNM")
    age: int = Field(alias="CAGE")
    position: int = Field(alias="COPS")

    teams: list["Team"] = Relationship(back_populates="coach")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int

    coach_id: int | None = Field(default=None, foreign_key="coach.id")
    coach: Coach | None = Relationship(back_populates="teams")
    school_id: int | None = Field(default=None, foreign_key="school.id")
    school: School | None = Relationship(back_populates="teams")
    players: list[Player] = Relationship(
        back_populates="teams", link_model=PlayerTeamLink
    )
