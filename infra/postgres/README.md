# PostgreSQL

Infrastructure assets related to the PostgreSQL service live here.

Current contents:
- `bootstrap/` for the one-shot migration + seed job used by Docker Compose
- `migrations/` for Alembic migration history and CLI helpers

The API service does not own schema/bootstrap startup logic anymore.
