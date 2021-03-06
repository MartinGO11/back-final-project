"""empty message

Revision ID: a9444af086bf
Revises: 68a5490a491a
Create Date: 2021-02-22 16:26:39.384971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9444af086bf'
down_revision = '68a5490a491a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'agendamiento', 'servicios', ['f_servicios_id'], ['servicio_id'])
    op.create_foreign_key(None, 'agendamiento', 'extras', ['f_extras_id'], ['extras_id'])
    op.create_foreign_key(None, 'agendamiento', 'users', ['f_users_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    op.drop_constraint(None, 'agendamiento', type_='foreignkey')
    # ### end Alembic commands ###
