#!/bin/sh
set -eu

MINIO_ALIAS="local"
MINIO_ENDPOINT="http://minio:9000"
BUCKET="${MINIO_PUBLIC_BUCKET:-portfolio}"

mc alias set "$MINIO_ALIAS" "$MINIO_ENDPOINT" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb --ignore-existing "$MINIO_ALIAS/$BUCKET"
mc anonymous set download "$MINIO_ALIAS/$BUCKET"
mc mirror --overwrite /seed/ "$MINIO_ALIAS/$BUCKET/"
