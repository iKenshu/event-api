FROM python:3.12-slim

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc python3-pip python3-venv curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipx && \
    pipx install poetry && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

ENV PATH="${PATH}:/root/.local/bin"

RUN poetry config virtualenvs.create false && poetry install

COPY . /app

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]

