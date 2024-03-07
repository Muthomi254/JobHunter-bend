"""icreasing jti length

Revision ID: 391a7b8a9db5
Revises: acfd33a9e042
Create Date: 2024-03-07 13:07:40.713250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '391a7b8a9db5'
down_revision = 'acfd33a9e042'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('revoked_token', schema=None) as batch_op:
        batch_op.alter_column('jti',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=500),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('revoked_token', schema=None) as batch_op:
        batch_op.alter_column('jti',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###