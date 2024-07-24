FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-dev

COPY ./alembic.ini /app/

COPY ./prestart.sh /app/

COPY ./app /app/app

EXPOSE 80

VOLUME /app/db

RUN mkdir -p /app/db

RUN /app/prestart.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
