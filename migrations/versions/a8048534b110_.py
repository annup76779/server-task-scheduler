"""empty message

Revision ID: a8048534b110
Revises: 
Create Date: 2022-02-15 13:58:27.961968

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8048534b110'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('email', sa.String(length=225), nullable=False),
    sa.Column('name', sa.String(length=225), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('reg_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
