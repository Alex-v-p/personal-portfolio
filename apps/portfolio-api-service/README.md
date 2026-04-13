# portfolio-api-service

FastAPI service for public portfolio content, admin authentication, and CRUD endpoints.

## Runtime responsibility

This service no longer bootstraps the database on startup. Its runtime responsibility is limited to:
- connecting to the configured database
- reading and writing portfolio data through the API
- resolving public media metadata into usable public URLs

Schema creation and seed loading now run through the dedicated `portfolio-db-init` one-shot container in Docker Compose.

## Database bootstrap job

The Compose bootstrap job uses the same SQLAlchemy models but its implementation and seed definitions now live under `infra/postgres/bootstrap`, outside the API package and outside the API process.

Bootstrap environment flags:
- `DB_BOOTSTRAP_AUTO_SEED=true` to seed starter data when the schema is empty
- `DB_BOOTSTRAP_RECREATE_ON_DRIFT=true` to recreate the schema when incompatible drift is detected in development-only flows
- production mode rejects `DB_BOOTSTRAP_RECREATE_ON_DRIFT=true` so destructive drift repair cannot run by accident
- `DB_BOOTSTRAP_MAX_RETRIES=30` to keep retrying while PostgreSQL starts
- `DB_BOOTSTRAP_RETRY_DELAY_SECONDS=2` to control retry spacing

## Public media resolution

Public DTO media URLs are derived from:
- `media_files.bucket_name`
- `media_files.object_key`

Example:

```text
http://localhost:9000/portfolio/blog/building-a-portfolio-shell/cover.png
```

This keeps file metadata in the database while serving actual bytes from MinIO.

## Admin endpoints

The API now exposes protected Stage 10 CMS endpoints under `/api/admin`, including:

- `/api/admin/auth/login`
- `/api/admin/projects`
- `/api/admin/blog-posts`
- `/api/admin/profile`
- `/api/admin/contact-messages`
- `/api/admin/experiences`
- `/api/admin/navigation-items`
- `/api/admin/admin-users`
- `/api/admin/github-snapshots`
- `/api/admin/skill-categories`
- `/api/admin/skills`
- `/api/admin/blog-tags`
- `/api/admin/media-files`
- `/api/admin/media-files/upload`

Use the bearer token returned by `/api/admin/auth/login` for subsequent admin requests.

## Admin media uploads

Authenticated admin uploads are accepted as multipart form data and written directly into MinIO.
Each upload also creates a `media_files` row so the uploaded file becomes selectable from the CMS immediately.

Relevant settings:
- `MEDIA_STORAGE_ENDPOINT`
- `MEDIA_STORAGE_ACCESS_KEY`
- `MEDIA_STORAGE_SECRET_KEY`
- `MEDIA_STORAGE_SECURE`
- `MEDIA_PUBLIC_BUCKET`
- `MEDIA_MAX_UPLOAD_BYTES`
