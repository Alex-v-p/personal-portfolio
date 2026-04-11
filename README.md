# Personal Portfolio Platform

Monorepo base for a portfolio platform with:

- **Angular** frontend (`web-service`)
- **FastAPI** portfolio/content backend (`portfolio-api-service`)
- **FastAPI** assistant backend (`assistant-service`)
- **PostgreSQL** for application data
- **Redis** for async/caching support
- **MinIO** for public media/object storage
- **Nginx** as an optional reverse proxy entrypoint

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
│  └─ redis/
├─ docs/
├─ compose.yml
├─ .env.example
└─ .gitignore
```

## Service responsibilities

### web-service
Frontend application responsible for:
- public portfolio pages
- projects and experience views
- blog pages
- contact page/form
- future admin UI
- future assistant chat UI

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

### assistant-service
Backend responsible for:
- AI chat endpoints
- provider orchestration
- conversation handling
- future retrieval / RAG / search

### minio
Object storage responsible for:
- serving seeded public portfolio media
- hosting future uploaded images/files
- separating file delivery from the Angular frontend

## Quick start

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```
2. Review the values and adjust them as needed.
3. Start infrastructure and app containers:
   ```bash
   docker compose up --build
   ```

## Local endpoints

- Portfolio API: `http://localhost:8011/api/health`
- Assistant API: `http://localhost:8012/api/health`
- MinIO API: `http://localhost:9000`
- MinIO Console: `http://localhost:9001`

## Notes

- Public media is now served from MinIO rather than the Angular app's `/assets` folder.
- The API returns direct public media URLs so the frontend never needs MinIO credentials.
- `minio-init` mirrors the seed media in `infra/minio/seed` into the configured public bucket on startup.
