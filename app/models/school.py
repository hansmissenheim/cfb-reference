from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.mapping import STATES
from app.models.links import PlayerTeamLink

if TYPE_CHECKING:
    from app.models.links import TeamGameLink
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
    stats: "SchoolStats" = Relationship(back_populates="school")
    teams: list["Team"] = Relationship(back_populates="school")


class SchoolStats(SQLModel, table=True):
    school_id: int | None = Field(
        default=None, foreign_key="school.id", primary_key=True
    )
    wins: int = Field(alias="TCWI")
    losses: int = Field(alias="TCLO")
    ties: int = Field(alias="TCTI")
    bowl_wins: int = Field(alias="CBOW")
    bowl_losses: int = Field(alias="CBOL")
    bowl_ties: int = Field(alias="CBOT")
    conf_champs: int = Field(alias="NUMC")
    natl_champs: int = Field(alias="NCYN")

    school: School = Relationship(back_populates="stats")


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    year: int

    coach_id: int | None = Field(default=None, foreign_key="coach.id")
    coach: Optional["Coach"] = Relationship(back_populates="teams")
    game_links: list["TeamGameLink"] = Relationship(back_populates="team")
    school_id: int | None = Field(default=None, foreign_key="school.id")
    school: School | None = Relationship(back_populates="teams")
    stats: "TeamStats" = Relationship(back_populates="team")
    players: list["Player"] = Relationship(
        back_populates="teams", link_model=PlayerTeamLink
    )


class TeamStats(SQLModel, table=True):
    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    wins: int = Field(alias="TSWI")
    losses: int = Field(alias="TSLO")
    ties: int = Field(alias="TSTI")
    streak: int = Field(alias="TSCS")
    avg_attendance: int = Field(alias="TMAA")
    bcs_rack: int = Field(alias="TBRK")
    bcs_rank_prev: int = Field(alias="TBPR")
    media_rank: int = Field(alias="TMRK")
    media_rank_prev: int = Field(alias="TMPP")
    media_points: int = Field(alias="tmpp")
    media_first_votes: int = Field(alias="TMPV")
    coaches_rank: int = Field(alias="TCRK")
    coaches_rank_prev: int = Field(alias="TCPR")
    coaches_points: int = Field(alias="TCPT")
    coaches_first_votes: int = Field(alias="TCFP")

    total_yards: int = Field(alias="tsTy", default=0)
    offense_yards: int = Field(alias="tsoy", default=0)
    pass_yards: int = Field(alias="tsop", default=0)
    rush_yards: int = Field(alias="tsor", default=0)
    pass_tds: int = Field(alias="tsPt", default=0)
    rush_tds: int = Field(alias="tsrt", default=0)
    offense_sacks: int = Field(alias="tssa", default=0)
    first_downs: int = Field(alias="ts1d", default=0)
    pass_yards_allowed: int = Field(alias="tsdp", default=0)
    rush_yards_allowed: int = Field(alias="tsdy", default=0)
    third_down_conversions: int = Field(alias="ts3c", default=0)
    third_down_attempts: int = Field(alias="ts3d", default=0)
    fourth_down_conversions: int = Field(alias="ts4c", default=0)
    fourth_down_attempts: int = Field(alias="ts4d", default=0)
    two_point_conversions: int = Field(alias="ts2c", default=0)
    two_point_attempts: int = Field(alias="ts2a", default=0)
    redzone_attempts: int = Field(alias="tsoz", default=0)
    redzone_tds: int = Field(alias="tsot", default=0)
    redzone_fgs: int = Field(alias="tsof", default=0)
    defense_redzone_attempts: int = Field(alias="tsdr", default=0)
    defense_redzone_tds: int = Field(alias="tsdt", default=0)
    defense_redzone_fgs: int = Field(alias="tsdf", default=0)
    penalties: int = Field(alias="tspe", default=0)
    penalty_yards: int = Field(alias="tsPy", default=0)
    offense_turnovers: int = Field(alias="tsga", default=0)
    offense_fumbles_lost: int = Field(alias="tsfl", default=0)
    offense_interceptions: int = Field(alias="tspi", default=0)
    defense_turnovers: int = Field(alias="tsta", default=0)
    defense_fumbles_recoveries: int = Field(alias="tsfr", default=0)
    defense_interceptions: int = Field(alias="tsDi", default=0)
    defense_sacks: int = Field(alias="tssk", default=0)
    special_teams_yards: int = Field(alias="tsty", default=0)
    pass_attempts: int = Field(alias="tspa", default=0)
    rush_attempts: int = Field(alias="tsra", default=0)

    team: Team = Relationship(back_populates="stats")


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
