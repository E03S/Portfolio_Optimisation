import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.command import Command

from aiogram.types import Message
from aiogram.utils.markdown import hbold
from ..classes.client import Client
from .config import settings

bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)
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

client = Client(base_url=f'{settings.api_host}:{settings.api_port}')
tickers = hard_coded_portfolio.keys()
tickers = list(tickers)
money = None

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {message.from_user.full_name}! It is a bot for portfolio optimization. You can satrt to optimize your portfolio by using /optimization_by_news command. Or you can check initial portfolio by using /portfolio command.")


@dp.message(Command("optimization_by_news"))
async def news_handler(message: types.Message) -> None:
    """
    Handler will get next message as a news for prediciton,
        if message empty it gets last news from benzinga for the last week and
        make prediction by them
    """
    try:
        await optimize_portfolio(message)
        await message.answer(
            f"Your portfolio is\n `{get_porfolio_str()}`",
            parse_mode=ParseMode.MARKDOWN
        )

    except TypeError as e:
        print(e)
        await message.answer("Nice try!")


async def optimize_portfolio(message: types.Message):
    try:
        await message.answer(
            "Now we are making prediction it can require some time"
        )
        new_portfolio = client.optimize_portfolio(tickers)
        global hard_coded_portfolio
        hard_coded_portfolio = new_portfolio
        return new_portfolio
    except TypeError as e:
        print(e)
        return "Nice try!"


@dp.message(Command("portfolio"))
async def portfolio_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message
        types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.answer(
            f"Your portfolio is\n `{get_porfolio_str()}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

@dp.message(Command("set_budget"))
async def portfolio_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message
        types (like a text, photo, sticker etc.)
    """
    try:
        # after set sum should be number of in dollars
        global money
        money = int(message.text.split(' ')[1])
        await message.answer(
            f"Your budget is {money}$",
            parse_mode=ParseMode.MARKDOWN
        )
    except (IndexError, ValueError):
        # But not all the types is supported to be copied so need to handle it
        await message.answer("After set_budget should be number of in dollars")

@dp.message(Command("reset"))
async def portfolio_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message
        types (like a text, photo, sticker etc.)
    """
    global money, hard_coded_portfolio
    money = None
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



@dp.message(Command("show_portfolio_shares"))
async def portfolio_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender
    By default, message handler will handle all message
        types (like a text, photo, sticker etc.)
    """
    try:
        # after set sum should be number of in dollars
        global money
        if not money:
            await message.answer("You should set budget first. Use /set_budget command")
            return
        today_json = client.get_today_price(tickers)
        today_df = pd.DataFrame(today_json)
        portfolion_items = hard_coded_portfolio.items()
        protfolio_str = '\n'.join(f"{tick}: {int((perc * money) // today_df[today_df['Symbol'] == tick]['Adj Close'].values[0])}" for tick, perc in portfolion_items)
        await message.answer(
            f"Your portfolio is\n `{protfolio_str}`",
            parse_mode=ParseMode.MARKDOWN
        )
    except TypeError as e:
        # But not all the types is supported to be copied so need to handle it
        print(e)
        await message.answer("After set_budget should be number of in dollars")


def get_porfolio_str():
    portfolion_items = hard_coded_portfolio.items()
    return '\n'.join(f"{tick}: {perc}" for tick, perc in portfolion_items)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
