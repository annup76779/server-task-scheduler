"""empty message

Revision ID: b2574c34b8a0
Revises: 
Create Date: 2022-02-17 02:11:15.663254

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b2574c34b8a0'
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
    op.create_table('jobs',
    sa.Column('job_id', sa.String(length=36), nullable=False),
    sa.Column('user', sa.String(length=225), nullable=False),
    sa.Column('ref_name', sa.UnicodeText(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.Column('time', sa.Time(), nullable=False),
    sa.Column('command_used', sa.UnicodeText(), nullable=False),
    sa.Column('syear', sa.Integer(), nullable=False),
    sa.Column('smonth', sa.Integer(), nullable=False),
    sa.Column('sday', sa.Integer(), nullable=False),
    sa.Column('stime', sa.Time(), nullable=False),
    sa.Column('completedOn', sa.DateTime(), nullable=True),
    sa.Column('tool_used', sa.String(length=30), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.email'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('job_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('jobs')
    op.drop_table('user')
    # ### end Alembic commands ###
