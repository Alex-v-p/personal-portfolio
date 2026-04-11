# MinIO public media seed

This folder contains the seeded public media objects for the portfolio.

- `seed/` mirrors the object keys stored in `media_files.object_key`
- `init-public-bucket.sh` creates the public bucket and uploads the seed files

Default local URLs:
- S3 API: `http://localhost:9000`
- Console: `http://localhost:9001`
- Public objects: `http://localhost:9000/portfolio/<object_key>`
