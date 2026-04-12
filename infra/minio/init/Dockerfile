FROM minio/mc:RELEASE.2025-03-12T17-29-24Z AS mc

FROM alpine:3.20
COPY --from=mc /usr/bin/mc /usr/local/bin/mc
COPY infra/minio/init-public-bucket.sh /usr/local/bin/init-public-bucket.sh
RUN tr -d '\r' < /usr/local/bin/init-public-bucket.sh > /tmp/init-public-bucket.sh \
    && mv /tmp/init-public-bucket.sh /usr/local/bin/init-public-bucket.sh \
    && chmod +x /usr/local/bin/init-public-bucket.sh
ENTRYPOINT ["/bin/sh", "/usr/local/bin/init-public-bucket.sh"]
