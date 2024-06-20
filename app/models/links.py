from sqlmodel import Field, SQLModel


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
