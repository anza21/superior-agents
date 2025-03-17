from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Προσθήκη του σωστού path για να βρει το models.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Εισαγωγή των models για να μπορέσει να πάρει το metadata
from models import Base

# Το Alembic Config object που διαβάζει το .ini αρχείο
config = context.config

# Ρυθμίσεις για logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ορισμός του metadata των models
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Εκτελεί τα migrations σε offline mode"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Εκτελεί τα migrations σε online mode"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
