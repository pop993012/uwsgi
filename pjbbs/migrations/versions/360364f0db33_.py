"""empty message

Revision ID: 360364f0db33
Revises: 6f8c6a6dffd6
Create Date: 2018-09-28 20:41:09.818636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '360364f0db33'
down_revision = '6f8c6a6dffd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bk',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bkname', sa.String(length=20), nullable=False),
    sa.Column('bknum', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bk')
    # ### end Alembic commands ###
