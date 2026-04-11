# portfolio-api-service

FastAPI service for public portfolio content, admin authentication, and CRUD endpoints.

## Database bootstrap

On startup, the service can:
- create the PostgreSQL schema for the portfolio domain
- enable the `vector` extension when PostgreSQL is being used
- seed starter content for profile, projects, blog posts, skills, navigation, media, experience, and GitHub stats

Environment flags:
- `DB_AUTO_CREATE=true` to create tables on startup
- `DB_AUTO_SEED=true` to seed starter data when the schema is empty
- `DB_STARTUP_GRACEFUL=true` to keep the API running even if the database is temporarily unavailable
- `MEDIA_PUBLIC_BASE_URL=http://localhost:9000` to control the public object base used for resolved media URLs

## Public media resolution

Public DTO media URLs are derived from:
- `media_files.bucket_name`
- `media_files.object_key`

Example:

```text
http://localhost:9000/portfolio/blog/building-a-portfolio-shell/cover.png
```

This keeps file metadata in the database while serving actual bytes from MinIO.
