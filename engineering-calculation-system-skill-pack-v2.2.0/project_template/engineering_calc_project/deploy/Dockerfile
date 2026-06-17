FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV APP_HOST=0.0.0.0
ENV APP_PORT=5000
ENV FLASK_DEBUG=0

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir "flask>=3.0" "gunicorn>=21.2"

COPY src ./src
COPY webapp ./webapp

EXPOSE 5000

CMD ["gunicorn", "webapp.app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "2"]
