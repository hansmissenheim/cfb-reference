from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.mapping import HOMETOWNS, POSITIONS
from app.models.links import PlayerSchoolLink, PlayerTeamLink

if TYPE_CHECKING:
    from app.models.school import School, Team


class Player(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ea_id: int = Field(alias="PGID")
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
    stats_blocking: list["PlayerSeasonBlockingStats"] = Relationship(
        back_populates="player"
    )
    stats_kicking: list["PlayerSeasonKickingStats"] = Relationship(
        back_populates="player"
    )
    stats_return: list["PlayerSeasonReturnStats"] = Relationship(
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
    overall: int = Field(alias="POVR")
    PTEN: int
    PPOE: int
    PRNS: int
    PLSY: int

    player: Player = Relationship(back_populates="attributes")


class PlayerSeasonStats(SQLModel):
    ea_id: int = Field(alias="index")
    games_played: int = Field(alias="sgmp")
    year: int = Field(alias="year")


class PlayerSeasonOffenseStats(PlayerSeasonStats, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
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
    team: "Team" = Relationship()

    @property
    def completion_percentage(self):
        if self.pass_attempts == 0:
            percentage = 0.0
        else:
            percentage = self.completions / (self.pass_attempts)
        return f"{percentage * 100:.1f}"

    @property
    def yards_per_pass_attempt(self):
        if self.pass_attempts == 0:
            percentage = 0.0
        else:
            percentage = self.pass_yards / (self.pass_attempts)
        return f"{percentage:.1f}"

    @property
    def adjusted_yards_per_attempt(self):
        if self.pass_attempts == 0:
            percentage = 0.0
        else:
            percentage = (
                self.pass_yards + 20 * self.pass_tds - 45 * self.interceptions
            ) / (self.pass_attempts)
        return f"{percentage:.1f}"

    @property
    def passer_rating(self):
        if self.pass_attempts == 0:
            percentage = 0.0
        else:
            percentage = (
                8.4 * self.pass_yards
                + 330 * self.pass_tds
                - 200 * self.interceptions
                + 100 * (self.completions / (self.pass_attempts))
            ) / (self.pass_attempts)
        return f"{percentage:.1f}"

    @property
    def yards_per_rush_attempt(self):
        if self.rush_attempts == 0:
            percentage = 0.0
        else:
            percentage = self.rush_yards / (self.rush_attempts)
        return f"{percentage:.1f}"

    @property
    def yards_per_reception(self):
        if self.receptions == 0:
            percentage = 0.0
        else:
            percentage = self.recieving_yards / self.receptions
        return f"{percentage:.1f}"


class PlayerSeasonDefenseStats(PlayerSeasonStats, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
    games_played: int = Field(alias="sgmp")
    solo_tackles: int = Field(alias="sdta")
    assisted_tackles: int = Field(alias="sdht")
    tackles_for_loss: int = Field(alias="sdtl")
    full_sacks: int = Field(alias="slsk")
    half_sacks: int = Field(alias="slhs")
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
    team: "Team" = Relationship()

    @property
    def sacks(self) -> float:
        return self.full_sacks + (0.5 * self.half_sacks)

    @property
    def interception_average(self) -> float:
        if self.interceptions == 0:
            return 0.0
        return round(self.intercepton_yards / self.interceptions, 1)


class PlayerSeasonBlockingStats(PlayerSeasonStats, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
    games_played: int = Field(alias="sgmp")
    pancakes: int = Field(alias="sopa")
    sacks_allowed: int = Field(alias="sosa")

    player: Player = Relationship(back_populates="stats_blocking")
    team: "Team" = Relationship()


class PlayerSeasonKickingStats(PlayerSeasonStats, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
    games_played: int = Field(alias="sgmp")
    fg_made: int = Field(alias="skfm")
    fg_attempts: int = Field(alias="skfa")
    longest_fg: int = Field(alias="skfL")
    fg_blocks: int = Field(alias="skfb")
    xp_made: int = Field(alias="skem")
    xp_attempts: int = Field(alias="skea")
    xp_blocks: int = Field(alias="skeb")
    fg_made_17_29: int = Field(alias="skmb")
    fg_attempts_17_29: int = Field(alias="skab")
    fg_made_30_39: int = Field(alias="skmc")
    fg_attempts_30_39: int = Field(alias="skac")
    fg_made_40_49: int = Field(alias="skmd")
    fg_attempts_40_49: int = Field(alias="skad")
    fg_made_50: int = Field(alias="skme")
    fg_attempts_50: int = Field(alias="skae")
    kickoffs: int = Field(alias="sknk")
    touchbacks: int = Field(alias="sktb")
    punts: int = Field(alias="spat")
    punt_yards: int = Field(alias="spya")
    net_punt_yards: int = Field(alias="spny")
    punt_blocks: int = Field(alias="spbl")
    punts_in_20: int = Field(alias="sppt")
    punt_touchbacks: int = Field(alias="sptb")
    longest_punt: int = Field(alias="splN")

    player: Player = Relationship(back_populates="stats_kicking")
    team: "Team" = Relationship()

    @property
    def points(self):
        return self.fg_made * 3 + self.xp_made

    @property
    def fg_percentage(self):
        if self.fg_attempts == 0:
            return 0.0
        return round(self.fg_made / self.fg_attempts, 3) * 100

    @property
    def xp_percentage(self):
        if self.xp_attempts == 0:
            return 0.0
        return round(self.xp_made / self.xp_attempts, 3) * 100

    @property
    def punt_average(self):
        if self.punts == 0:
            return 0.0
        return round(self.punt_yards / self.punts, 1)


class PlayerSeasonReturnStats(PlayerSeasonStats, table=True):
    id: int | None = Field(default=None, primary_key=True)
    player_id: int | None = Field(default=None, foreign_key="player.id")
    team_id: int = Field(foreign_key="team.id")
    games_played: int = Field(alias="sgmp")
    kick_returns: int = Field(alias="srka")
    kick_return_yards: int = Field(alias="srky")
    kick_return_tds: int = Field(alias="srkt")
    longest_kick_return: int = Field(alias="srkL")
    punt_returns: int = Field(alias="srpa")
    punt_return_yards: int = Field(alias="srpy")
    punt_return_tds: int = Field(alias="srpt")
    longest_punt_return: int = Field(alias="srpL")

    player: Player = Relationship(back_populates="stats_return")
    team: "Team" = Relationship()

    @property
    def kick_return_average(self):
        if self.kick_returns == 0:
            return 0.0
        return round(self.kick_return_yards / self.kick_returns, 1)

    @property
    def punt_return_average(self):
        if self.punt_returns == 0:
            return 0.0
        return round(self.punt_return_yards / self.punt_returns, 1)
