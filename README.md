# Personal Portfolio Platform

Monorepo base for a portfolio platform with:

- **Angular** frontend (`web-service`)
- **FastAPI** portfolio/content backend (`portfolio-api-service`)
- **FastAPI** assistant backend (`assistant-service`)
- **PostgreSQL** for application data
- **One-shot database init container** for migration + optional seed loading
- **Redis** for async/caching support
- **MinIO** for public media/object storage
- **Nginx** inside the frontend container for static asset serving and API reverse proxying

## Repository layout

```text
personal-portfolio/
├─ apps/
│  ├─ web-service/
│  ├─ portfolio-api-service/
│  └─ assistant-service/
├─ infra/
│  ├─ minio/
│  ├─ nginx/
│  ├─ postgres/
│  │  └─ bootstrap/
│  └─ redis/
├─ docs/
├─ compose.yml
├─ compose.dev.yml
├─ .env.example
└─ .gitignore
```

## Service responsibilities

### web-service
Frontend application and public entrypoint responsible for:
- serving the production Angular build as static assets
- proxying `/api/*` to `portfolio-api-service`
- proxying `/ai/*` to `assistant-service`
- rendering the public portfolio pages
- hosting the admin UI
- hosting the assistant chat UI

### portfolio-api-service
Backend responsible for:
- public content endpoints
- public media URL resolution
- admin authentication
- admin CRUD
- projects
- experience
- homepage/profile content
- blog metadata/content
- social/contact info

### portfolio-db-init
One-shot init job responsible for:
- applying Alembic migrations up to `head`
- auto-stamping an existing compatible schema that predates Alembic
- seeding starter portfolio content when the configured seed mode allows it

Its implementation lives under `infra/postgres/bootstrap` so the API package stays focused on request handling and data access.

In production mode it now refuses to run with destructive drift recreation enabled.

### assistant-service
Backend responsible for:
- AI chat endpoints
- provider orchestration
- conversation handling
- retrieval / RAG / search

### minio
Object storage responsible for:
- serving seeded public portfolio media
- hosting uploaded images/files
- separating file delivery from the Angular frontend

## Running the stack

### Production-style local run
This is the default Compose path and mirrors a real deployment more closely:

```bash
cp .env.example .env
docker compose up --build
```

This starts:
- a static frontend served by Nginx on `http://localhost:4200`
- internal-only API containers behind the frontend reverse proxy
- PostgreSQL, Redis, MinIO, bootstrap, and assistant dependencies

### Development run with live reload
Use the development override when you want bind mounts and hot reload:

```bash
docker compose -f compose.yml -f compose.dev.yml up --build
```

Development-mode differences:
- Angular runs with `ng serve`
- the API containers run `uvicorn --reload`
- source directories are bind-mounted
- database and Redis ports are exposed to the host

## Local endpoints

### Production-style compose
- Frontend + reverse proxy: `http://localhost:4200`
- Portfolio API health: `http://localhost:4200/api/health`
- Assistant API health: `http://localhost:4200/ai/health`
- MinIO API: `http://localhost:19000`
- MinIO Console: `http://localhost:19001`

### Development override compose
- Frontend dev server: `http://localhost:4200`
- Portfolio API health: `http://localhost:8011/api/health`
- Assistant API health: `http://localhost:8012/api/health`
- MinIO API: `http://localhost:19000`
- MinIO Console: `http://localhost:19001`

## Notes

- Public media is served from MinIO rather than the Angular app's `/assets` folder.
- The frontend now uses relative `/api` and `/ai` paths so it works through either the production reverse proxy or the dev proxy config.
- `portfolio-db-init` owns schema migration and seeding, so the API no longer mutates PostgreSQL on startup.
- `minio-init` mirrors the seed media in `infra/minio/seed` into the configured public bucket on startup.
- `DB_BOOTSTRAP_RECREATE_ON_DRIFT` should stay disabled in production.

## Admin CMS

- Admin login page: `http://localhost:4200/admin/login`
- The seeded admin account is created by `portfolio-db-init` from `.env`
- Default local credentials are `ADMIN_EMAIL=admin@example.com` and `ADMIN_PASSWORD=change-me-admin`
- Change those values in `.env` before first bootstrap if you do not want the defaults


## Database migrations

Schema changes are now tracked under `infra/postgres/migrations`.

Common commands:

```bash
python -m infra.postgres.migrations.cli status
python -m infra.postgres.migrations.cli upgrade head
python -m infra.postgres.migrations.cli check
python -m infra.postgres.migrations.cli revision --autogenerate -m "add something"
```

See `docs/database-migrations.md` for the short workflow.
