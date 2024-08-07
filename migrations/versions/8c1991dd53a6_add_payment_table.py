"""Add payment table

Revision ID: 8c1991dd53a6
Revises: fea3d6d16171
Create Date: 2024-08-06 22:01:00.076790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c1991dd53a6'
down_revision = 'fea3d6d16171'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('booking_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('payment_method', sa.String(), nullable=False),
    sa.Column('status', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], name=op.f('fk_payments_booking_id_bookings')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_payments'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payments')
    # ### end Alembic commands ###
