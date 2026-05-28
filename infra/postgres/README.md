# PostgreSQL

Infrastructure assets related to the PostgreSQL service live here.

Current contents:
- `bootstrap/` for the one-shot init job used by Docker Compose
- `migrations/` for Alembic migration history, state inspection, and CLI helpers

Current split of responsibility:
- **migrations** own schema history and database structure
- **bootstrap** owns startup orchestration and optional seeding
- the API service does **not** create or repair schema on startup
