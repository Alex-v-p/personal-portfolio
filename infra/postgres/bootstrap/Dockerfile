FROM python:3.12-slim

WORKDIR /workspace

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace/apps/portfolio-api-service:/workspace

COPY apps/portfolio-api-service/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY apps/portfolio-api-service /workspace/apps/portfolio-api-service
COPY infra /workspace/infra

CMD ["python", "-m", "infra.postgres.bootstrap.bootstrap_database"]
