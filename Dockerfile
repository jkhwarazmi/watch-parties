FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PRODUCTION=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Don't run as root
RUN useradd --create-home appuser
USER appuser

# Cloud Run sets PORT, threads suit the TMDB requests which are mostly waiting
CMD exec gunicorn --bind :${PORT:-8080} --workers 1 --threads 8 --timeout 0 run:app
