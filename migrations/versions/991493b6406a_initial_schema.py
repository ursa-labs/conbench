"""Initial schema

Revision ID: 991493b6406a
Revises:
Create Date: 2021-04-07 13:57:22.257052

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "991493b6406a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "case",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("case_index", "case", ["name", "tags"], unique=True)
    op.create_table(
        "commit",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("sha", sa.String(length=50), nullable=False),
        sa.Column("repository", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(length=250), nullable=False),
        sa.Column("message", sa.String(length=250), nullable=False),
        sa.Column("author_name", sa.String(length=100), nullable=False),
        sa.Column("author_login", sa.String(length=50), nullable=True),
        sa.Column("author_avatar", sa.String(length=100), nullable=True),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "context",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("context_index", "context", ["tags"], unique=True)
    op.create_table(
        "machine",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("architecture_name", sa.Text(), nullable=False),
        sa.Column("kernel_name", sa.Text(), nullable=False),
        sa.Column("os_name", sa.Text(), nullable=False),
        sa.Column("os_version", sa.Text(), nullable=False),
        sa.Column("cpu_model_name", sa.Text(), nullable=False),
        sa.Column("cpu_l1d_cache_bytes", sa.Integer(), nullable=False),
        sa.Column("cpu_l1i_cache_bytes", sa.Integer(), nullable=False),
        sa.Column("cpu_l2_cache_bytes", sa.Integer(), nullable=False),
        sa.Column("cpu_l3_cache_bytes", sa.Integer(), nullable=False),
        sa.Column("cpu_core_count", sa.Integer(), nullable=False),
        sa.Column("cpu_thread_count", sa.Integer(), nullable=False),
        sa.Column("cpu_frequency_max_hz", sa.BigInteger(), nullable=False),
        sa.Column("memory_bytes", sa.BigInteger(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "machine_index",
        "machine",
        [
            "name",
            "architecture_name",
            "kernel_name",
            "os_name",
            "os_version",
            "cpu_model_name",
            "cpu_l1d_cache_bytes",
            "cpu_l1i_cache_bytes",
            "cpu_l2_cache_bytes",
            "cpu_l3_cache_bytes",
            "cpu_core_count",
            "cpu_thread_count",
            "cpu_frequency_max_hz",
            "memory_bytes",
        ],
        unique=True,
    )
    op.create_table(
        "user",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_table(
        "run",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=250), nullable=True),
        sa.Column(
            "timestamp", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("commit_id", sa.String(length=50), nullable=False),
        sa.Column("machine_id", sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(
            ["commit_id"],
            ["commit.id"],
        ),
        sa.ForeignKeyConstraint(
            ["machine_id"],
            ["machine.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "summary",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("case_id", sa.String(length=50), nullable=False),
        sa.Column("machine_id", sa.String(length=50), nullable=False),
        sa.Column("context_id", sa.String(length=50), nullable=False),
        sa.Column("run_id", sa.Text(), nullable=False),
        sa.Column("unit", sa.Text(), nullable=False),
        sa.Column("time_unit", sa.Text(), nullable=False),
        sa.Column("batch_id", sa.Text(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("iterations", sa.Integer(), nullable=False),
        sa.Column("min", sa.Numeric(), nullable=True),
        sa.Column("max", sa.Numeric(), nullable=True),
        sa.Column("mean", sa.Numeric(), nullable=True),
        sa.Column("median", sa.Numeric(), nullable=True),
        sa.Column("stdev", sa.Numeric(), nullable=True),
        sa.Column("q1", sa.Numeric(), nullable=True),
        sa.Column("q3", sa.Numeric(), nullable=True),
        sa.Column("iqr", sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(
            ["case_id"],
            ["case.id"],
        ),
        sa.ForeignKeyConstraint(
            ["context_id"],
            ["context.id"],
        ),
        sa.ForeignKeyConstraint(
            ["machine_id"],
            ["machine.id"],
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["run.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("summary_batch_id_index", "summary", ["batch_id"], unique=False)
    op.create_index("summary_case_id_index", "summary", ["case_id"], unique=False)
    op.create_index("summary_run_id_index", "summary", ["run_id"], unique=False)
    op.create_table(
        "data",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("summary_id", sa.String(length=50), nullable=False),
        sa.Column("iteration", sa.Integer(), nullable=False),
        sa.Column("result", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(["summary_id"], ["summary.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("data_summary_id_index", "data", ["summary_id"], unique=False)
    op.create_table(
        "time",
        sa.Column("id", sa.String(length=50), nullable=False),
        sa.Column("summary_id", sa.String(length=50), nullable=False),
        sa.Column("iteration", sa.Integer(), nullable=False),
        sa.Column("result", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(["summary_id"], ["summary.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("time_summary_id_index", "time", ["summary_id"], unique=False)


def downgrade():
    op.drop_index("time_summary_id_index", table_name="time")
    op.drop_table("time")
    op.drop_index("data_summary_id_index", table_name="data")
    op.drop_table("data")
    op.drop_index("summary_run_id_index", table_name="summary")
    op.drop_index("summary_case_id_index", table_name="summary")
    op.drop_index("summary_batch_id_index", table_name="summary")
    op.drop_table("summary")
    op.drop_table("run")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    op.drop_index("machine_index", table_name="machine")
    op.drop_table("machine")
    op.drop_index("context_index", table_name="context")
    op.drop_table("context")
    op.drop_table("commit")
    op.drop_index("case_index", table_name="case")
    op.drop_table("case")
