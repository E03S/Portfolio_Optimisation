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
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    data = stock_parser.download_custom_data([ticker], start_date, today)
    if data.empty:
        raise HTTPException(status_code=404, detail=f"No data available for {ticker}.")

    ticker_data = stock_parser.apply_features_to_stocks(data).iloc[[-1]]
    weekly_return = regressor.predict(ticker_data)
    return {"ticker": ticker, "predicted_weekly_return": weekly_return[0]}


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
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    predictions = {}
    news_df = await get_news_df(tickers)
    for ticker in tickers:
        news_by_stock = news_df[news_df["stocks"] == ticker]
        data = stock_parser.download_custom_data([ticker], start_date, today)
        if data.empty:
            predictions[ticker] = "No data available"
        else:
            ticker_data = stock_parser.apply_features_to_stocks(data).iloc[[-1]]
            news_embedding = news_embedder.calculate_common_embedding(news_by_stock["title"].tolist())
            ticker_data = ticker_data.join(pd.DataFrame([news_embedding], columns=[f'title_embedding_{i}' for i in range(384)]))
            ticker_data.fillna(0, inplace=True)
            ticker_data.columns = [col.lower() for col in ticker_data.columns]
            weekly_return = regressor.predict(ticker_data)
            predictions[ticker] = weekly_return[0]

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
