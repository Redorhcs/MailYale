"""add state

Revision ID: 181b8071d020
Revises: 07f2372d6219
Create Date: 2020-09-02 21:17:46.244529

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '181b8071d020'
down_revision = '07f2372d6219'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('state', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('students', 'state')
    # ### end Alembic commands ###
