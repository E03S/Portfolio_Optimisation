FROM python:3.11

WORKDIR /portfolio_optimisation

RUN apt-get update && apt-get install -y libatlas-base-dev

RUN python -m pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-cache --only prod 

COPY portfolio_optimisation/ /portfolio_optimisation/portfolio_optimisation
COPY .env /portfolio_optimisation/

ENV PYTHOPATH="/portfolio_optimisation:$PYTHONPATH"

ENV APP_PORT=8000
EXPOSE $APP_PORT

CMD poetry run uvicorn portfolio_optimisation.api.main:app --reload --host 0.0.0.0 --port ${APP_PORT}
