"""empty message

Revision ID: 473404d1e038
Revises: 3b8419773623
Create Date: 2016-04-19 19:08:06.202566

"""

# revision identifiers, used by Alembic.
revision = '473404d1e038'
down_revision = '3b8419773623'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'uuid')
    ### end Alembic commands ###