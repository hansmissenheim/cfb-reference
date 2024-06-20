from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.school import Team


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


class TeamGameLink(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    game_id: int | None = Field(default=None, foreign_key="game.id", primary_key=True)
    is_home: bool

    team: "Team" = Relationship(back_populates="game_links")
    game: "Game" = Relationship(back_populates="team_links")
