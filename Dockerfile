FROM python:3.11

WORKDIR /portfolio_optimisation

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml /

RUN poetry install --only api 

COPY portfolio_optimisation/ /portfolio_optimisation/portfolio_optimisation
COPY .env /portfolio_optimisation/

ENV PYTHOPATH="/portfolio_optimisation:$PYTHONPATH"

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD poetry run uvicorn portfolio_optimisation.api.main:app --reload --host 0.0.0.0 --port ${APP_PORT}
