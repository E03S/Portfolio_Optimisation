FROM python:3.11

WORKDIR /

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml /

RUN poetry install --only api

COPY portfolio_optimisation/api /app/api/

ENV PYTHOPATH="/app:$PYTHONPATH"

ENV APP_PORT=8000

CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
