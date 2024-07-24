"""add season stats models

Revision ID: fd631c8fb299
Revises: ad7d47fd3f11
Create Date: 2024-07-24 13:29:12.628861

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fd631c8fb299"
down_revision: Union[str, None] = "ad7d47fd3f11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "schoolstats",
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("wins", sa.Integer(), nullable=False),
        sa.Column("losses", sa.Integer(), nullable=False),
        sa.Column("ties", sa.Integer(), nullable=False),
        sa.Column("bowl_wins", sa.Integer(), nullable=False),
        sa.Column("bowl_losses", sa.Integer(), nullable=False),
        sa.Column("bowl_ties", sa.Integer(), nullable=False),
        sa.Column("conf_champs", sa.Integer(), nullable=False),
        sa.Column("natl_champs", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["school.id"],
        ),
        sa.PrimaryKeyConstraint("school_id"),
    )
    op.create_table(
        "playerseasonblockingstats",
        sa.Column("ea_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("pancakes", sa.Integer(), nullable=False),
        sa.Column("sacks_allowed", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playerseasondefensestats",
        sa.Column("ea_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("solo_tackles", sa.Integer(), nullable=False),
        sa.Column("assisted_tackles", sa.Integer(), nullable=False),
        sa.Column("tackles_for_loss", sa.Integer(), nullable=False),
        sa.Column("full_sacks", sa.Integer(), nullable=False),
        sa.Column("half_sacks", sa.Integer(), nullable=False),
        sa.Column("interceptions", sa.Integer(), nullable=False),
        sa.Column("intercepton_yards", sa.Integer(), nullable=False),
        sa.Column("longest_interception", sa.Integer(), nullable=False),
        sa.Column("pass_deflections", sa.Integer(), nullable=False),
        sa.Column("forced_fumbles", sa.Integer(), nullable=False),
        sa.Column("fumbles_recovered", sa.Integer(), nullable=False),
        sa.Column("fumble_yards", sa.Integer(), nullable=False),
        sa.Column("blocked_kicks", sa.Integer(), nullable=False),
        sa.Column("safeties", sa.Integer(), nullable=False),
        sa.Column("tds", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playerseasonkickingstats",
        sa.Column("ea_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("fg_made", sa.Integer(), nullable=False),
        sa.Column("fg_attempts", sa.Integer(), nullable=False),
        sa.Column("longest_fg", sa.Integer(), nullable=False),
        sa.Column("fg_blocks", sa.Integer(), nullable=False),
        sa.Column("xp_made", sa.Integer(), nullable=False),
        sa.Column("xp_attempts", sa.Integer(), nullable=False),
        sa.Column("xp_blocks", sa.Integer(), nullable=False),
        sa.Column("fg_made_17_29", sa.Integer(), nullable=False),
        sa.Column("fg_attempts_17_29", sa.Integer(), nullable=False),
        sa.Column("fg_made_30_39", sa.Integer(), nullable=False),
        sa.Column("fg_attempts_30_39", sa.Integer(), nullable=False),
        sa.Column("fg_made_40_49", sa.Integer(), nullable=False),
        sa.Column("fg_attempts_40_49", sa.Integer(), nullable=False),
        sa.Column("fg_made_50", sa.Integer(), nullable=False),
        sa.Column("fg_attempts_50", sa.Integer(), nullable=False),
        sa.Column("kickoffs", sa.Integer(), nullable=False),
        sa.Column("touchbacks", sa.Integer(), nullable=False),
        sa.Column("punts", sa.Integer(), nullable=False),
        sa.Column("punt_yards", sa.Integer(), nullable=False),
        sa.Column("net_punt_yards", sa.Integer(), nullable=False),
        sa.Column("punt_blocks", sa.Integer(), nullable=False),
        sa.Column("punts_in_20", sa.Integer(), nullable=False),
        sa.Column("punt_touchbacks", sa.Integer(), nullable=False),
        sa.Column("longest_punt", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playerseasonoffensestats",
        sa.Column("ea_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("completions", sa.Integer(), nullable=False),
        sa.Column("pass_attempts", sa.Integer(), nullable=False),
        sa.Column("pass_yards", sa.Integer(), nullable=False),
        sa.Column("pass_tds", sa.Integer(), nullable=False),
        sa.Column("interceptions", sa.Integer(), nullable=False),
        sa.Column("longest_pass", sa.Integer(), nullable=False),
        sa.Column("sacks", sa.Integer(), nullable=False),
        sa.Column("rush_attempts", sa.Integer(), nullable=False),
        sa.Column("rush_yards", sa.Integer(), nullable=False),
        sa.Column("rush_tds", sa.Integer(), nullable=False),
        sa.Column("longest_rush", sa.Integer(), nullable=False),
        sa.Column("yards_after_contact", sa.Integer(), nullable=False),
        sa.Column("twenty_yard_runs", sa.Integer(), nullable=False),
        sa.Column("broken_tackles", sa.Integer(), nullable=False),
        sa.Column("fumbles", sa.Integer(), nullable=False),
        sa.Column("receptions", sa.Integer(), nullable=False),
        sa.Column("recieving_yards", sa.Integer(), nullable=False),
        sa.Column("recieving_tds", sa.Integer(), nullable=False),
        sa.Column("longest_reception", sa.Integer(), nullable=False),
        sa.Column("yards_after_catch", sa.Integer(), nullable=False),
        sa.Column("drops", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "playerseasonreturnstats",
        sa.Column("ea_id", sa.Integer(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("games_played", sa.Integer(), nullable=False),
        sa.Column("kick_returns", sa.Integer(), nullable=False),
        sa.Column("kick_return_yards", sa.Integer(), nullable=False),
        sa.Column("kick_return_tds", sa.Integer(), nullable=False),
        sa.Column("longest_kick_return", sa.Integer(), nullable=False),
        sa.Column("punt_returns", sa.Integer(), nullable=False),
        sa.Column("punt_return_yards", sa.Integer(), nullable=False),
        sa.Column("punt_return_tds", sa.Integer(), nullable=False),
        sa.Column("longest_punt_return", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["player_id"],
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teamstats",
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("wins", sa.Integer(), nullable=False),
        sa.Column("losses", sa.Integer(), nullable=False),
        sa.Column("ties", sa.Integer(), nullable=False),
        sa.Column("streak", sa.Integer(), nullable=False),
        sa.Column("avg_attendance", sa.Integer(), nullable=False),
        sa.Column("bcs_rank", sa.Integer(), nullable=False),
        sa.Column("bcs_rank_prev", sa.Integer(), nullable=False),
        sa.Column("media_rank", sa.Integer(), nullable=False),
        sa.Column("media_rank_prev", sa.Integer(), nullable=False),
        sa.Column("media_points", sa.Integer(), nullable=False),
        sa.Column("media_first_votes", sa.Integer(), nullable=False),
        sa.Column("coaches_rank", sa.Integer(), nullable=False),
        sa.Column("coaches_rank_prev", sa.Integer(), nullable=False),
        sa.Column("coaches_points", sa.Integer(), nullable=False),
        sa.Column("coaches_first_votes", sa.Integer(), nullable=False),
        sa.Column("total_yards", sa.Integer(), nullable=False),
        sa.Column("offense_yards", sa.Integer(), nullable=False),
        sa.Column("pass_yards", sa.Integer(), nullable=False),
        sa.Column("rush_yards", sa.Integer(), nullable=False),
        sa.Column("pass_tds", sa.Integer(), nullable=False),
        sa.Column("rush_tds", sa.Integer(), nullable=False),
        sa.Column("offense_sacks", sa.Integer(), nullable=False),
        sa.Column("first_downs", sa.Integer(), nullable=False),
        sa.Column("pass_yards_allowed", sa.Integer(), nullable=False),
        sa.Column("rush_yards_allowed", sa.Integer(), nullable=False),
        sa.Column("third_down_conversions", sa.Integer(), nullable=False),
        sa.Column("third_down_attempts", sa.Integer(), nullable=False),
        sa.Column("fourth_down_conversions", sa.Integer(), nullable=False),
        sa.Column("fourth_down_attempts", sa.Integer(), nullable=False),
        sa.Column("two_point_conversions", sa.Integer(), nullable=False),
        sa.Column("two_point_attempts", sa.Integer(), nullable=False),
        sa.Column("redzone_attempts", sa.Integer(), nullable=False),
        sa.Column("redzone_tds", sa.Integer(), nullable=False),
        sa.Column("redzone_fgs", sa.Integer(), nullable=False),
        sa.Column("defense_redzone_attempts", sa.Integer(), nullable=False),
        sa.Column("defense_redzone_tds", sa.Integer(), nullable=False),
        sa.Column("defense_redzone_fgs", sa.Integer(), nullable=False),
        sa.Column("penalties", sa.Integer(), nullable=False),
        sa.Column("penalty_yards", sa.Integer(), nullable=False),
        sa.Column("offense_turnovers", sa.Integer(), nullable=False),
        sa.Column("offense_fumbles_lost", sa.Integer(), nullable=False),
        sa.Column("offense_interceptions", sa.Integer(), nullable=False),
        sa.Column("defense_turnovers", sa.Integer(), nullable=False),
        sa.Column("defense_fumbles_recoveries", sa.Integer(), nullable=False),
        sa.Column("defense_interceptions", sa.Integer(), nullable=False),
        sa.Column("defense_sacks", sa.Integer(), nullable=False),
        sa.Column("special_teams_yards", sa.Integer(), nullable=False),
        sa.Column("pass_attempts", sa.Integer(), nullable=False),
        sa.Column("rush_attempts", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["team_id"],
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("team_id"),
    )
    op.add_column("player", sa.Column("ea_id", sa.Integer(), nullable=False))
    op.add_column(
        "playerattributes", sa.Column("overall", sa.Integer(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("playerattributes", "overall")
    op.drop_column("player", "ea_id")
    op.drop_table("teamstats")
    op.drop_table("playerseasonreturnstats")
    op.drop_table("playerseasonoffensestats")
    op.drop_table("playerseasonkickingstats")
    op.drop_table("playerseasondefensestats")
    op.drop_table("playerseasonblockingstats")
    op.drop_table("schoolstats")
    # ### end Alembic commands ###
