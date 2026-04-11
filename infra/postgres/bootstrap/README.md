# PostgreSQL bootstrap job

This folder owns the operational PostgreSQL bootstrap flow for local Docker Compose.

Responsibilities:
- wait/retry until PostgreSQL is reachable
- enable required extensions
- create the schema from the API service's SQLAlchemy models
- recreate the schema when drift repair is enabled
- seed starter portfolio content

The API service itself does **not** run this logic on startup.
