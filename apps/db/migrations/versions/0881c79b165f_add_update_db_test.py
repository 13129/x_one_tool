"""add update db_test

Revision ID: 0881c79b165f
Revises: ac3111d4a4d9
Create Date: 2023-10-17 11:48:45.189925

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0881c79b165f'
down_revision = 'ac3111d4a4d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('db_test',
                  sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'PENDING', name='statusenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('db_test', 'status')
    # ### end Alembic commands ###
