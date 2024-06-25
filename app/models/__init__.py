from sqlmodel import SQLModel  # noqa

from app.models.game import Game
from app.models.links import PlayerSchoolLink, PlayerTeamLink, TeamGameLink
from app.models.player import (
    Player,
    PlayerAttributes,
    PlayerSeasonBlockingStats,
    PlayerSeasonDefenseStats,
    PlayerSeasonKickingStats,
    PlayerSeasonOffenseStats,
    PlayerSeasonReturnStats,
)
from app.models.school import Coach, School, SchoolStats, Stadium, Team, TeamStats
from app.models.utils import Media

__all__ = [
    "Coach",
    "Game",
    "Media",
    "Player",
    "PlayerAttributes",
    "PlayerSchoolLink",
    "PlayerSeasonBlockingStats",
    "PlayerSeasonDefenseStats",
    "PlayerSeasonKickingStats",
    "PlayerSeasonOffenseStats",
    "PlayerSeasonReturnStats",
    "PlayerTeamLink",
    "School",
    "SchoolStats",
    "Stadium",
    "Team",
    "TeamStats",
    "TeamGameLink",
]
