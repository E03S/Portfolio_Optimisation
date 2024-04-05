import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command

from aiogram.types import Message
from aiogram.utils.markdown import hbold
import hydra
from omegaconf import DictConfig, OmegaConf
from hydra import compose, initialize
from ..classes.benzinga_parser import BenzingaNewsParser
from ..classes.llm_model import LLMModel
from ..classes.portfolio_optimizer import PortfolioOptimizer
from ..classes.client import Client
from datetime import datetime, timedelta
import pandas as pd

# All handlers should be attached to the Router (or Dispatcher)
with initialize(version_base="1.3", config_path="../../configs"):
    cfg = compose(config_name="config")

bot = Bot(token=cfg.bot.token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

hard_coded_portfolio = {
    'AAPL': 0.07,
    'MSFT': 0.065,
    'AMZN': 0.032,
    'NVDA': 0.028,
    'GOOGL': 0.021,
    'TSLA': 0.019,
    'GOOG': 0.018,
    'BRK-B': 0.018,
    'META': 0.018,
    'UNH': 0.013,
    'XOM': 0.013,
    'LLY': 0.012,
    'JPM': 0.012,
    'JNJ': 0.011,
    'V': 0.011,
    'PG': 0.01,
    'MA': 0.009,
    'AVGO': 0.009,
    'HD': 0.009,
    'CVX': 0.008,
    'MRK': 0.007,
    'ABBV': 0.007,
    'COST': 0.007,
    'PEP': 0.007,
    'ADBE': 0.007
}

client = Client(base_url='http://localhost:8000')
start_date = '2022-01-01'
today = datetime.today().strftime('%Y-%m-%d')
tickers = hard_coded_portfolio.keys()
tickers = list(tickers)
optimizer = PortfolioOptimizer(tickers, start_date, today)
optimizer.initialize()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")

@dp.message(Command("optimization_by_news"))
async def news_handler(message: types.Message) -> None:
    """
    Handler will get next message as a news for prediciton, if message empty it gets last news from benzinga for the last week and make prediction by them
    """
    try:
        # news = get_titles()
        # news_str = '\n'.join(news)
        # await message.answer(f"We assembled next news for you\n {news_str}")
        await make_prediction([], message)
        await message.answer(f"Your portfolio is\n `{get_porfolio_str()}`", parse_mode=ParseMode.MARKDOWN)

    except TypeError as e:
        print(e)
        await message.answer("Nice try!")

@dp.message(Command("optimization_by_input"))
async def news_handler(message: types.Message) -> None:
    """
    Handler will get next message as a news for prediciton, if message empty it gets last news from benzinga for the last week and make prediction by them
    """
    text_message = message.text
    try:
        command_len = len("/optimization_by_input ")
        if len(text_message) > command_len:
            news = text_message[command_len:]
            print(news)
        else:
            await message.answer("Please enter some news")
            return
        await make_prediction(news, message)
        await message.answer(f"Your portfolio is\n `{get_porfolio_str()}`", parse_mode=ParseMode.MARKDOWN)
    except TypeError as e:
        print(e)
        await message.answer("Nice try!")

async def make_prediction(news, message: types.Message):
    try:
        await message.answer("Now we are making prediction it can require some time")
        predictions = client.make_batch_prediction(tickers)
        new_portfolio = recalculate_portfolio(predictions)
        global hard_coded_portfolio
        hard_coded_portfolio = new_portfolio
        return new_portfolio
    except TypeError as e:
        print(e)
        return "Nice try!"

def make_portfolio_str_from_json(json_response):
    return '\n'.join(
            f"{entry['ticker']}, Sentiment: {entry['sentiment']}, Expected Return: {entry['expected_return']}%, Risk: {entry['risk_percentage']}%"
            for entry in json_response
        )

def recalculate_portfolio(json_response):
    sorted_tickers_in_alp = sorted(tickers)
    values = [json_response[ticker] for ticker in sorted_tickers_in_alp]
    return optimizer.run_optimization(values)

@dp.message(Command("portfolio"))
async def portfolio_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer(f"Your portfolio is\n `{get_porfolio_str()}`", parse_mode=ParseMode.MARKDOWN)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

def get_porfolio_str():
    return '\n'.join(f"{ticker}: {percentage}" for ticker, percentage in hard_coded_portfolio.items())

def get_titles():
    parser = BenzingaNewsParser(api_key=cfg.benzinga.api_key)
    last_week = datetime.now() - timedelta(days=7)
    last_week = last_week.strftime("%Y-%m-%d")
    tickers = hard_coded_portfolio.keys()
    news_df = parser.get_news(ticker=tickers, page=1, date_from=last_week, date_to=datetime.now().strftime("%Y-%m-%d"))
    if len(news_df) <= 1:
        week_and_half = datetime.now() - timedelta(days=10)
        week_and_half = week_and_half.strftime("%Y-%m-%d")
        news_df = parser.get_news(ticker=tickers, page=1, date_from=week_and_half, date_to=datetime.now().strftime("%Y-%m-%d"))
    return news_df['title'].tolist()

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())