"""Added to_dict funtion under User class in models.py

Revision ID: 846a503140a5
Revises: 6a74062e5b1c
Create Date: 2024-03-30 17:34:13.290532

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '846a503140a5'
down_revision = '6a74062e5b1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), nullable=False))
        batch_op.drop_column('date_crated')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_crated', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###