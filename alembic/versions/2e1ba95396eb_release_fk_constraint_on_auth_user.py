"""release fk constraint on auth.user

Revision ID: 2e1ba95396eb
Revises: 6eb2a0816a54
Create Date: 2024-06-08 13:24:51.987063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2e1ba95396eb'
down_revision: Union[str, None] = '6eb2a0816a54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_id_fkey', 'users', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('users_id_fkey', 'users', 'users', ['id'], ['id'], referent_schema='auth', ondelete='CASCADE')
    # ### end Alembic commands ###