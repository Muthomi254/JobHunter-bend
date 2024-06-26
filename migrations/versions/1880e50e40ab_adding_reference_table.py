"""adding reference table

Revision ID: 1880e50e40ab
Revises: 05dee7febf98
Create Date: 2024-03-13 16:15:30.962484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1880e50e40ab'
down_revision = '05dee7febf98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('references',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(length=255), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('job_title', sa.String(length=255), nullable=True),
    sa.Column('organization', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['user_email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('references')
    # ### end Alembic commands ###
