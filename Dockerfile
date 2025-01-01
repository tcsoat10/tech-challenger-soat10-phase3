FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    build-essential \
    libpq-dev \
    && apt-get clean

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

COPY . .

RUN chmod +x /app/config/init_db/init_db.sh

ARG PORT=8000
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["poetry", "run", "uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
