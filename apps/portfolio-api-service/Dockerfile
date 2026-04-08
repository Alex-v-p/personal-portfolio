FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORTFOLIO_API_PORT:-8001} --reload"]
