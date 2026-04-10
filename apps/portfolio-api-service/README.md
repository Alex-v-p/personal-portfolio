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
