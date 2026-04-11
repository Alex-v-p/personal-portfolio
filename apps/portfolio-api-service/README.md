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
- `DB_BOOTSTRAP_RECREATE_ON_DRIFT=true` to recreate the schema when incompatible drift is detected
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

Use the bearer token returned by `/api/admin/auth/login` for subsequent admin requests.


### Admin media uploads

The admin CMS can upload files through `POST /api/admin/media-files/upload` using multipart form data. The API writes the file to MinIO/S3-compatible storage, creates a `media_files` metadata record, and returns the uploaded media entry for immediate reuse in the CMS.
