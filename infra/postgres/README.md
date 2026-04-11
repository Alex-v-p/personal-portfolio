# PostgreSQL

Infrastructure assets related to the PostgreSQL service live here.

Current contents:
- `bootstrap/` for the one-shot schema + seed job used by Docker Compose

The API service does not own schema/bootstrap startup logic anymore.
