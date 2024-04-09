import pandas as pd

from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache
from ..config import settings
from ...classes.yahoo_parser import SP500Parser
from ...classes.benzinga_parser import BenzingaNewsParser
from ...classes.predictor import FinancialPredictor
from ...classes.news_embedder import NewsEmbedder
import numpy as np
regressor_path = settings.regressor_path
preprocessor_path = settings.preproccessor_path

stock_parser = SP500Parser()
news_embedder = NewsEmbedder()
regressor = FinancialPredictor(regressor_path=regressor_path,
                               preprocessor_path=preprocessor_path)
news_parser = BenzingaNewsParser(api_key=settings.benzinga_token)

router = APIRouter(prefix="/predictor", tags=["Predictor"])

@router.post(
    "/predict_weekly_return", summary="Predict Weekly Return for Single Ticker"
)
# @cache(expire=3600)
async def predict_weekly_return(ticker: str):
    """
    Predict the weekly return for a given ticker within the specified date range.

    Parameters:
    - ticker (str): Ticker symbol of the stock.

    Returns:
    - dict: A dictionary containing the ticker symbol and the predicted weekly return.
    """
    if not ticker:
        raise HTTPException(status_code=422, detail="No ticker provided.")
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    data = stock_parser.download_custom_data([ticker], start_date, today)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for {ticker}.")
    response = await predict_weekly_return_batch([ticker])
    return response


@router.post(
    "/predict_weekly_return_batch", summary="Predict Weekly Return for Batch of Tickers"
)
# @cache(expire=3600)
async def predict_weekly_return_batch(tickers: List[str]):
    """
    Predict the weekly return for a batch of tickers within the specified date range.

    Parameters:
    - tickers (List[str]): List of ticker symbols of the stocks.

    Returns:
    - dict: A dictionary containing the ticker symbols and their predicted weekly returns.
    """
    if not tickers:
        raise HTTPException(status_code=422, detail="No tickers provided.")
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    news_df = await get_news_df(tickers)
    data = stock_parser.download_custom_data(tickers, start_date, today)
    number_of_news = len(data["Symbol"].value_counts())
    if number_of_news != len(tickers):
        raise HTTPException(status_code=404, detail=f"No data available for {number_of_news}/{len(tickers)} tickers.")
    ticker_data = stock_parser.apply_features_to_stocks(data)
    ticker_data = ticker_data.groupby("Symbol").tail(1)
    grouped_news = news_df.groupby("stocks")
    news_embeddings = news_embedder.calculate_common_embeddings(grouped_news['title'].apply(list).tolist())
    news_embeddings = pd.DataFrame(news_embeddings, columns=[f'title_embedding_{i}' for i in range(384)])
    news_embeddings['Symbol'] = grouped_news.groups.keys()
    ticker_data = ticker_data.join(news_embeddings.set_index('Symbol'), on='Symbol')
    ticker_data.fillna(0, inplace=True)
    ticker_data.columns = [col.lower() for col in ticker_data.columns]
    weekly_return = regressor.predict(ticker_data)
    predictions = {ticker: weekly_return for ticker, weekly_return in zip(ticker_data['symbol'], weekly_return)}
    return predictions


async def get_news_df(tickers: List[str]):
    last_days = datetime.now() - timedelta(days=3)
    last_days = last_days.strftime("%Y-%m-%d")
    news_df = news_parser.get_news(ticker=tickers, page=1, date_from=last_days, date_to=datetime.now().strftime("%Y-%m-%d"))
    needed_columns = ['title', 'stocks']
    news_df = news_df[needed_columns]
    news_df["stocks"] = news_df["stocks"].apply(lambda x: [entry["name"] for entry in x])
    news_df = news_df.explode("stocks")
    return news_df
