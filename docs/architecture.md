# Architecture Notes

## High-level flow

```text
Browser
  ↓
Angular frontend
  ↓
────────────────────────────────────
| portfolio-api-service            |
| assistant-service                |
────────────────────────────────────
  ↓
PostgreSQL + Redis
```

## Reverse proxy flow (optional)

```text
Browser
  ↓
nginx
 ├─ /      -> Angular frontend
 ├─ /api   -> portfolio-api-service
 └─ /ai    -> assistant-service
```

## Boundaries

### Portfolio API
Owns standard site content and administration.

### Assistant Service
Owns AI-specific orchestration, chat, and future retrieval logic.

### Frontend
Consumes both APIs and remains free of backend business logic.
