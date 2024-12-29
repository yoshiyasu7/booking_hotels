"""Initialization database

Revision ID: 0cdbfc2c3105
Revises:
Create Date: 2024-12-28 18:21:31.344563

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0cdbfc2c3105"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), unique=True, nullable=False),
        sa.Column("email", sa.String(), unique=True, nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_name", sa.String(), nullable=False),
        sa.Column("hotel_location", sa.String(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("price_per_night", sa.Float(), nullable=False),
        sa.Column("rooms_available", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["owner_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("guest_name", sa.String(), nullable=False),
        sa.Column("rooms_booked", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("bookings")
    op.drop_table("hotels")
    op.drop_table("users")
    # ### end Alembic commands ###