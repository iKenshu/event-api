FROM python:3.12-slim

WORKDIR /app

# Copiar los archivos de dependencias para evitar reconstrucción innecesaria
COPY ./pyproject.toml ./poetry.lock /app/

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc python3-pip python3-venv curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar pipx y poetry
RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Configurar Poetry para no crear entornos virtuales
ENV PATH="${PATH}:/root/.local/bin"

# Instalar las dependencias del proyecto sin las dev (si no las necesitas para producción)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copiar el resto de la aplicación
COPY . /app

EXPOSE 8000

