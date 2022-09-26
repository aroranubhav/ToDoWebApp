"""empty message

Revision ID: e2d6002c0f3b
Revises: 550d911d7dac
Create Date: 2022-09-26 01:04:37.291980

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2d6002c0f3b'
down_revision = '550d911d7dac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('todo_category_id', sa.Integer(), nullable=False))
    op.drop_constraint('todos_list_id_fkey', 'todos', type_='foreignkey')
    op.create_foreign_key(None, 'todos', 'todoslists', ['todo_category_id'], ['id'])
    op.drop_column('todos', 'list_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('list_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.create_foreign_key('todos_list_id_fkey', 'todos', 'todoslists', ['list_id'], ['id'])
    op.drop_column('todos', 'todo_category_id')
    # ### end Alembic commands ###