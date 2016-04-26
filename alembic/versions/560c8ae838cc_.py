"""Add coffee_shops table with latitude and longitude as dec numbers.

Revision ID: 560c8ae838cc
Revises: 
Create Date: 2016-04-22 16:33:24.196715

"""

# revision identifiers, used by Alembic.
revision = '560c8ae838cc'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table('coffee_shops',
                    sa.Column('id_coffee_shop', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('username', sa.Text(), nullable=False),
                    sa.Column('password', sa.Text(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=False),
                    sa.Column('image', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('address', sa.Text(), nullable=True),
                    sa.Column('phone', sa.Text(), nullable=True),
                    sa.Column('currency', postgresql.ENUM('eur', 'gbp', name='currency'), nullable=False),
                    sa.Column('swift', sa.Text(), nullable=False),
                    sa.Column('iban', sa.Text(), nullable=False),
                    sa.Column('transaction_account', sa.Text(), nullable=False),
                    sa.Column('latitude', sa.REAL(), nullable=True),
                    sa.Column('longitude', sa.REAL(), nullable=True),
                    sa.Column('services', postgresql.JSONB(), nullable=True),
                    sa.PrimaryKeyConstraint('id_coffee_shop'),
                    sa.UniqueConstraint('transaction_account'),
                    sa.UniqueConstraint('username')
                    )


def downgrade():
    op.drop_table('coffee_shops')
    op.execute('DROP TYPE currency;')
