FROM python:3.11

WORKDIR /portfolio_optimisation

RUN python -m pip install poetry

COPY pyproject.toml poetry.lock /portfolio_optimisation/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-cache --only bot 


COPY portfolio_optimisation/bot /portfolio_optimisation/portfolio_optimisation/bot
COPY portfolio_optimisation/classes /portfolio_optimisation/portfolio_optimisation/classes

ENV PYTHOPATH="/portfolio_optimisation:$PYTHONPATH"

ENTRYPOINT ["poetry", "run", "python", "-m", "portfolio_optimisation.bot.bot"]