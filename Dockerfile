FROM python:3.11-slim as base

# Сборка зависимостей
ARG BUILD_DEPS="curl"
RUN apt-get update && apt-get install -y $BUILD_DEPS

# Установка poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.3.0 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

# Инициализация проекта
WORKDIR /app
ENTRYPOINT ["python", "-m", "bot"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка питонячьих библиотек
COPY poetry.lock pyproject.toml /
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Копирование в контейнер папок и файлов.
COPY . /app