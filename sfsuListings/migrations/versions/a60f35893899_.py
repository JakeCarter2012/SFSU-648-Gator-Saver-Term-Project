"""empty message

Revision ID: a60f35893899
Revises: 
Create Date: 2018-11-12 17:31:48.708584

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a60f35893899'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registered_user',
    sa.Column('UserName', sa.String(length=30), nullable=False),
    sa.Column('password_hash', sa.String(length=96), nullable=False),
    sa.PrimaryKeyConstraint('UserName'),
    sa.UniqueConstraint('UserName'),
    sa.UniqueConstraint('password_hash')
    )
    op.drop_table('sqlite_sequence')
    op.create_unique_constraint(None, 'posts', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='unique')
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    op.drop_table('registered_user')
    # ### end Alembic commands ###
