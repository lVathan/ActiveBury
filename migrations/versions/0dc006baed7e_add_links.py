"""add links

Revision ID: 0dc006baed7e
Revises: 9fee0c23b437
Create Date: 2018-07-26 21:14:41.520264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0dc006baed7e'
down_revision = '9fee0c23b437'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('hyperlink', sa.String(length=240), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'hyperlink')
    # ### end Alembic commands ###
