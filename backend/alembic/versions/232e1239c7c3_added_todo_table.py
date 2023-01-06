"""Added ToDo table

Revision ID: 232e1239c7c3
Revises: Mua
Create Date: 2023-01-04 22:07:30.150807

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "232e1239c7c3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "to_dos",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("to_do", sa.String(100), nullable=False),
        sa.Column("is_done", sa.Boolean()),
        sa.Column("create_date", sa.DateTime()),
    )


def downgrade():
    op.drop_table("to_dos")
