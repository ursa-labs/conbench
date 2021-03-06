"""add parent drop url

Revision ID: 782f4533db71
Revises: 854c3ba5abd6
Create Date: 2021-04-16 10:38:04.994000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "782f4533db71"
down_revision = "854c3ba5abd6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("commit", sa.Column("parent", sa.String(length=50), nullable=True))
    op.drop_column("commit", "url")


def downgrade():
    op.add_column(
        "commit",
        sa.Column("url", sa.VARCHAR(length=250), autoincrement=False, nullable=False),
    )
    op.drop_column("commit", "parent")
