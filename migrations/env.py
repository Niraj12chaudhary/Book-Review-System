import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# --- Add app root directory to sys.path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Import FastAPI settings and models ---
from app.core.config import settings
from app.core.database import Base  # IMPORTANT: This Base must include all your models (or import them here manually)
from app.models import book  # Make sure this imports your model
target_metadata = book.Base.metadata
from app.models import review 
target_metadata = review.Base.metadata

# --- Alembic Config object ---
config = context.config

# --- Load database URL from FastAPI settings ---
config.set_main_option("sqlalchemy.url", settings.database_url)

# --- Configure logging ---
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode (without DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode (with DB connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# --- Entry point ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
