"""Update tables

Revision ID: c3a80d18c57a
Revises: 039bb2631d24
Create Date: 2024-09-13 23:09:40.207132

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3a80d18c57a'
down_revision: Union[str, None] = '039bb2631d24'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'bid', 'employee', ['authorId'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bid', type_='foreignkey')
    # ### end Alembic commands ###
