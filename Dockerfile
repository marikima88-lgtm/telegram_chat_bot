# syntax=docker/dockerfile:1

# --- Сборка окружения -------------------------------------------------------
# Компиляторы нужны только здесь: в финальный образ этот слой не попадёт.
FROM python:3.13-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .

RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt \
    # pip и его спутники в рантайме не нужны — экономят около 15 МБ
    && /opt/venv/bin/pip uninstall -y pip setuptools wheel 2>/dev/null || true \
    && find /opt/venv -name '__pycache__' -type d -exec rm -rf {} + \
    && find /opt/venv -name '*.pyc' -delete

# --- Рантайм ----------------------------------------------------------------
FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    DB_PATH=/data/database.db

# Бот не должен работать от root.
RUN adduser -D -H -u 1000 bot \
    && mkdir -p /data \
    && chown bot:bot /data

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY --chown=bot:bot . .

USER bot

# База данных переживает пересоздание контейнера.
VOLUME ["/data"]

CMD ["python", "bot.py"]
