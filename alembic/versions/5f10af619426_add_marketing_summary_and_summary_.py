"""Add marketing_summary and summary_updated_at columns to products

Revision ID: 5f10af619426
Revises: 
Create Date: 2025-08-03 01:42:00.991719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f10af619426'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('products', sa.Column('marketing_summary', sa.Text(), nullable=True))
    op.add_column('products', sa.Column('summary_updated_at', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('products', 'marketing_summary')
    op.drop_column('products', 'summary_updated_at')
