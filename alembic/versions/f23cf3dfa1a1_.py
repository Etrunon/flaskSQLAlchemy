"""empty message

Revision ID: f23cf3dfa1a1
Revises: 560c8ae838cc
Create Date: 2016-04-22 16:37:20.316644

"""

# revision identifiers, used by Alembic.
revision = 'f23cf3dfa1a1'
down_revision = '560c8ae838cc'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


def upgrade():
    op.create_table('real_products',
                    sa.Column('id_real_product', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('id_coffee_shop', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('name', sa.Text(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('image', sa.Text(), nullable=True),
                    sa.Column('price', sa.REAL(), nullable=True),
                    sa.Column('currency', postgresql.ENUM('eur', 'gpb', name='currency', create_type=False), nullable=False),
                    sa.Column('enabled', sa.BOOLEAN(), nullable=True),
                    sa.Column('services', postgresql.JSONB(), nullable=True),
                    sa.ForeignKeyConstraint(['id_coffee_shop'], ['coffee_shops.id_coffee_shop'], ),
                    sa.PrimaryKeyConstraint('id_real_product')
                    )


def downgrade():
    op.drop_table('real_products')
