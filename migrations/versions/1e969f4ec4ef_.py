"""empty message

Revision ID: 1e969f4ec4ef
Revises: b283f6a9d9ae
Create Date: 2020-04-11 15:03:06.367990

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1e969f4ec4ef'
down_revision = 'b283f6a9d9ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('entries')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('text', mysql.TEXT(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('articles')
    # ### end Alembic commands ###
