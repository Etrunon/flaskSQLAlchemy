"""change coffee_shops latitude and longitude to GeoAlchemy types

Revision ID: df5dd1c0a34d
Revises: f23cf3dfa1a1
Create Date: 2016-04-22 20:33:51.124504

"""

# revision identifiers, used by Alembic.
import geoalchemy2

revision = 'df5dd1c0a34d'
down_revision = 'f23cf3dfa1a1'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # Example from stack overflow
    # op.add_column('coffee_shops', sa.Column('my_location', geoalchemy2.Geometry('POINT', management=True)))

    # Actual code
    op.add_column('coffee_shops', sa.Column('position', geoalchemy2.types.Geography(geometry_type='POINT', srid=4326), nullable=True))
    op.drop_column('coffee_shops', 'latitude')
    op.drop_column('coffee_shops', 'longitude')


def downgrade():
    op.add_column('coffee_shops', sa.Column('longitude', sa.REAL(), autoincrement=False, nullable=True))
    op.add_column('coffee_shops', sa.Column('latitude', sa.REAL(), autoincrement=False, nullable=True))
    op.drop_column('coffee_shops', 'position')

    # Mirror of above
    # op.drop_column('coffee_shops', 'my_location')
