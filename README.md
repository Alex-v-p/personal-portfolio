# Personal Portfolio Platform

Monorepo base for a portfolio platform with:

- **Angular** frontend (`web-service`)
- **FastAPI** portfolio/content backend (`portfolio-api-service`)
- **FastAPI** assistant backend (`assistant-service`)
- **PostgreSQL** for application data
- **Redis** for async/caching support
- **Nginx** as an optional reverse proxy entrypoint

## Repository layout

```text
personal-portfolio/
├─ apps/
│  ├─ web-service/
│  ├─ portfolio-api-service/
│  └─ assistant-service/
├─ infra/
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

## Health endpoints

- Portfolio API: `http://localhost:8011/api/health`
- Assistant API: `http://localhost:8012/api/health`

## Notes

- This is intentionally a **base scaffold** only.
- No database migrations or business logic have been added yet.
- The frontend is structured as an Angular app skeleton so you can start building features immediately.
