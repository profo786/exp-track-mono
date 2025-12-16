# Alembic migrations

Use the commands below from the `auth` directory:

1. `alembic revision --autogenerate -m "short message"` – create a new migration.
2. `alembic upgrade head` – apply all pending migrations.
3. `alembic downgrade -1` – roll back the last migration.

The configuration reads the `AUTH_DATABASE_URL` environment variable (falls back to `sqlite:///./auth.db`). The metadata for autogeneration comes from `app.db.base.Base`, so import new models into `app/db/models/__init__.py` to expose them to Alembic.

