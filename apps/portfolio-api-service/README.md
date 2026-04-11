# portfolio-api-service

FastAPI service for public portfolio content, admin authentication, and CRUD endpoints.

## Database bootstrap

On startup, the service can now:
- create the full PostgreSQL schema for the portfolio domain
- enable the `vector` extension when PostgreSQL is being used
- seed starter content for profile, projects, blog posts, skills, navigation, media, experience, and GitHub stats

Environment flags:
- `DB_AUTO_CREATE=true` to create tables on startup
- `DB_AUTO_SEED=true` to seed starter data when the schema is empty
- `DB_STARTUP_GRACEFUL=true` to keep the API running even if the database is temporarily unavailable
- `MEDIA_PUBLIC_BASE_URL=http://localhost:9000` to resolve public media against MinIO (or another object store)

## Public media behavior

The service resolves media URLs from `media_files.bucket_name` + `media_files.object_key`.
When `MEDIA_PUBLIC_BASE_URL` is set, public DTOs return direct object-storage URLs such as:

```text
http://localhost:9000/portfolio/projects/personal-portfolio/cover.png
```

That keeps file delivery separate from the frontend and avoids exposing storage credentials to the browser.
