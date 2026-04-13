# PostgreSQL bootstrap job

This folder owns the one-shot startup init job used by Docker Compose.

Responsibilities:
- wait/retry until PostgreSQL is reachable
- apply Alembic migrations up to `head`
- auto-stamp an existing compatible schema that predates Alembic
- seed starter data only when the configured seed mode allows it

Non-responsibilities:
- schema drift repair
- `create_all` / `drop_all`
- runtime schema mutation inside the API service

Recommended seed modes:
- `if-empty` (default): seed only a brand-new empty database
- `always`: run seed logic every bootstrap (safe for local refreshes because content seeding is mostly idempotent)
- `never`: apply migrations only
