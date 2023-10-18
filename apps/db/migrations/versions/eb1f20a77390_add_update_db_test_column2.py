"""add update db_test column2

Revision ID: eb1f20a77390
Revises: fa81880f41d2
Create Date: 2023-10-17 12:23:07.129780

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
import apps

revision = 'eb1f20a77390'
down_revision = 'fa81880f41d2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_test', sa.Column('status2', apps.test.models.JSONType(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_test', 'status2')
    # ### end Alembic commands ###
