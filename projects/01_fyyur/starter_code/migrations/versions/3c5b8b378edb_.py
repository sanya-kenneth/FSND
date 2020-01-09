"""empty message

Revision ID: 3c5b8b378edb
Revises: 2638ef71b324
Create Date: 2019-11-04 19:17:42.303521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c5b8b378edb'
down_revision = '2638ef71b324'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_image_link', sa.String(length=300), nullable=True))
    op.add_column('Show', sa.Column('artist_name', sa.String(length=120), nullable=True))
    op.add_column('Show', sa.Column('venue_name', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Show', 'venue_name')
    op.drop_column('Show', 'artist_name')
    op.drop_column('Show', 'artist_image_link')
    # ### end Alembic commands ###