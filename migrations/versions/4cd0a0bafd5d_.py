"""empty message

Revision ID: 4cd0a0bafd5d
Revises: 94192324f94c
Create Date: 2018-09-29 06:57:59.460214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cd0a0bafd5d'
down_revision = '94192324f94c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.alter_column('posts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###