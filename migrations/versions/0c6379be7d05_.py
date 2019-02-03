"""empty message

Revision ID: 0c6379be7d05
Revises: 
Create Date: 2019-02-03 10:28:59.904314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c6379be7d05'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(length=200), nullable=True),
    sa.Column('content_html', sa.Text(), nullable=True),
    sa.Column('t', sa.String(length=20), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('problems',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('abbr', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('content_html', sa.Text(), nullable=True),
    sa.Column('total_score', sa.Integer(), nullable=True),
    sa.Column('scoring_script', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('settings',
    sa.Column('setting', sa.String(), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('setting')
    )
    op.create_index(op.f('ix_settings_setting'), 'settings', ['setting'], unique=False)
    op.create_table('submissions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('uid', sa.Integer(), nullable=True),
    sa.Column('code', sa.Text(), nullable=True),
    sa.Column('code_hash', sa.String(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('memory', sa.Integer(), nullable=True),
    sa.Column('verdict', sa.String(length=10), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('status', sa.Text(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_table('testdatas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=True),
    sa.Column('time_limit', sa.Integer(), nullable=True),
    sa.Column('memory_limit', sa.Integer(), nullable=True),
    sa.Column('input', sa.Text(), nullable=True),
    sa.Column('answer', sa.Text(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['problems.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('testdatas')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('submissions')
    op.drop_index(op.f('ix_settings_setting'), table_name='settings')
    op.drop_table('settings')
    op.drop_table('problems')
    op.drop_table('messages')
    # ### end Alembic commands ###