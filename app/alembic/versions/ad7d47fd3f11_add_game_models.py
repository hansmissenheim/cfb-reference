"""add_game_models

Revision ID: ad7d47fd3f11
Revises: 1a3643bfcd59
Create Date: 2024-06-21 00:14:09.025100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ad7d47fd3f11'
down_revision: Union[str, None] = '1a3643bfcd59'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ea_id', sa.Integer(), nullable=False),
    sa.Column('home_score', sa.Integer(), nullable=False),
    sa.Column('away_score', sa.Integer(), nullable=False),
    sa.Column('stadium_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('url_slug', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['stadium_id'], ['stadium.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('url_slug')
    )
    op.create_table('teamgamelink',
    sa.Column('team_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('is_home', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('team_id', 'game_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teamgamelink')
    op.drop_table('game')
    # ### end Alembic commands ###
