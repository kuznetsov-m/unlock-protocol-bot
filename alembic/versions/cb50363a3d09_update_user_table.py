"""Update User table

Revision ID: cb50363a3d09
Revises: 2450c90e4636
Create Date: 2022-09-21 03:08:50.421699

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cb50363a3d09'
down_revision = '2450c90e4636'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('TelegramUser',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_start_timestamp', sa.DateTime(), nullable=True),
    sa.Column('is_stopped', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_TelegramUser_first_start_timestamp'), 'TelegramUser', ['first_start_timestamp'], unique=False)
    op.drop_index('ix_user_first_start_timestamp', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_start_timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_stopped', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('first_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_first_start_timestamp', 'user', ['first_start_timestamp'], unique=False)
    op.drop_index(op.f('ix_TelegramUser_first_start_timestamp'), table_name='TelegramUser')
    op.drop_table('TelegramUser')
    # ### end Alembic commands ###
