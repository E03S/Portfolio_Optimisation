FROM python:3.11

WORKDIR /
COPY pyproject.toml poetry.lock /

RUN python -m pip install poetry
ENV PATH="/root/.local/bin:$PATH"

COPY portfolio_optimisation/bot/bot.py /app/bot/
COPY portfolio_optimisation/bot/config.py /app/bot/
RUN poetry install --only bot
ENTRYPOINT ["poetry", "run", "python", "-m", "app.bot.bot"]