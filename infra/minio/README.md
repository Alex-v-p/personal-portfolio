# MinIO public media seed

This folder contains the seeded public media objects for the portfolio.

- `seed/` mirrors the object keys stored in `media_files.object_key`
- `init-public-bucket.sh` creates the public bucket and uploads the seed files

Default local URLs:
- S3 API: `http://localhost:9000`
- Console: `http://localhost:9001`
- Public objects: `http://localhost:9000/portfolio/<object_key>`


## Init container

The bucket bootstrap now runs from a small dedicated image under `infra/minio/init/` instead of bind-mounting the shell script directly into `minio/mc`. That avoids Windows CRLF issues and makes the one-shot init container run predictably once.
