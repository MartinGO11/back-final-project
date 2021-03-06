"""empty message

Revision ID: 68a5490a491a
Revises: 6d4dbfea58b6
Create Date: 2021-02-21 22:33:02.461031

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68a5490a491a'
down_revision = '6d4dbfea58b6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agendamiento', sa.Column('f_users_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'agendamiento', 'extras', ['f_extras_id'], ['extras_id'])
    op.create_foreign_key(None, 'agendamiento', 'users', ['f_users_id'], ['id'])
    op.create_foreign_key(None, 'agendamiento', 'servicios', ['f_servicios_id'], ['servicio_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    op.drop_column('agendamiento', 'f_users_id')
    # ### end Alembic commands ###
