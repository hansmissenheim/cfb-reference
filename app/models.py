from sqlmodel import Field, Relationship, SQLModel


class PlayerTeamLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    game_id: int = Field(alias="PGID")
    first_name: str = Field(alias="PFNA")
    last_name: str = Field(alias="PLNA")
    position: int = Field(alias="PPOS")
    year: int = Field(alias="PYEA")

    # Ratings attributes
    attributes: "PlayerAttributes" = Relationship(back_populates="player")

    teams: list["Team"] = Relationship(
        back_populates="players", link_model=PlayerTeamLink
    )


class PlayerAttributes(SQLModel, table=True):
    player_id: int | None = Field(
        default=None, foreign_key="player.id", primary_key=True
    )
    PTEN: int
    PPOE: int
    PRNS: int
    PLSY: int

    player: Player = Relationship(back_populates="attributes")


class School(SQLModel, table=True):
    id: int = Field(alias="TGID", primary_key=True)
    name: str = Field(alias="TDNA")
    nickname: str = Field(alias="TMNA")

    teams: list["Team"] = Relationship(back_populates="school")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int

    school_id: int | None = Field(default=None, foreign_key="school.id")
    school: School | None = Relationship(back_populates="teams")
    players: list[Player] = Relationship(
        back_populates="teams", link_model=PlayerTeamLink
    )
