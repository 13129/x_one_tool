"""update account Table Columns

Revision ID: fde0a9ebd916
Revises: 4ad0ccd870c9
Create Date: 2023-07-12 17:30:39.744425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde0a9ebd916'
down_revision = '4ad0ccd870c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dk_catalog', sa.Column('catalog_code', sa.String(length=128), nullable=True, comment='目录编码'))
    op.drop_column('dk_catalog', 'code')
    op.drop_column('dk_catalog', 'tabl_ecode')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dk_catalog', sa.Column('tabl_ecode', sa.VARCHAR(length=128), nullable=True))
    op.add_column('dk_catalog', sa.Column('code', sa.VARCHAR(length=128), nullable=True))
    op.drop_column('dk_catalog', 'catalog_code')
    # ### end Alembic commands ###
