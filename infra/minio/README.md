# MinIO media bootstrap

This folder contains the public seed media used by the portfolio.

## What happens in Docker Compose

- `minio` starts an S3-compatible object store
- `minio-init` creates the public bucket defined by `MINIO_PUBLIC_BUCKET`
- the same init step mirrors `infra/minio/seed/<bucket>` into that bucket
- the portfolio API resolves public media URLs against `MEDIA_PUBLIC_BASE_URL`

## Local defaults

- API endpoint: `http://localhost:9000`
- Console: `http://localhost:9001`
- Bucket: `portfolio`

The seed structure mirrors the `object_key` values stored in `media_files`.
