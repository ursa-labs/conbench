"""run context

Revision ID: 52b6915e289a
Revises: b86538f84533
Create Date: 2021-04-26 10:39:14.479883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52b6915e289a"
down_revision = "b86538f84533"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("run", sa.Column("context_id", sa.String(length=50), nullable=True))
    op.create_foreign_key(None, "run", "context", ["context_id"], ["id"])


def downgrade():
    op.drop_constraint(None, "run", type_="foreignkey")
    op.drop_column("run", "context_id")
