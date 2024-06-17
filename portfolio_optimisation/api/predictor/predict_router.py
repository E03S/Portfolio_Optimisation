import pandas as pd

from typing import List
from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException

from portfolio_optimisation.api.config import settings
from portfolio_optimisation.classes.yahoo_parser import SP500Parser
from portfolio_optimisation.classes.benzinga_parser import BenzingaNewsParser
from portfolio_optimisation.classes.predictor import FinancialPredictor
from portfolio_optimisation.classes.news_embedder import NewsEmbedder
import yfinance as yf
import logging
regressor_path = settings.regressor_path
preprocessor_path = settings.preproccessor_path

stock_parser = SP500Parser()
news_embedder = NewsEmbedder()
regressor = FinancialPredictor(regressor_path=regressor_path,
                               preprocessor_path=preprocessor_path)
# news_parser = BenzingaNewsParser(api_key=settings.benzinga_token)

router = APIRouter(prefix="/predictor", tags=["Predictor"])


@router.post(
    "/predict_weekly_return", summary="Predict Weekly Return for Single Ticker"
)
async def predict_weekly_return(ticker: str):
    """
    Predict the weekly return for a given ticker within the date range.

    Parameters:
    - ticker (str): Ticker symbol of the stock.

    Returns:
    - dict: A dictionary containing the ticker symbol and
        the predicted weekly return.
    """
    if not ticker:
        raise HTTPException(status_code=422, detail="No ticker provided.")
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    data = stock_parser.download_custom_data([ticker], start_date, today)
    if data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No data available for {ticker}."
        )
    response = await predict_weekly_return_batch([ticker])
    return response


@router.post(
    "/predict_weekly_return_batch",
    summary="Predict Weekly Return for Batch of Tickers"
)
# @cache(expire=3600)
async def predict_weekly_return_batch(tickers: List[str]):
    """
    Predict the weekly return for a batch of tickers within the date range.

    Parameters:
    - tickers (List[str]): List of ticker symbols of the stocks.

    Returns:
    - dict: A dictionary containing the ticker symbols and
        their predicted weekly returns.
    """
    if not tickers:
        raise HTTPException(status_code=422, detail="No tickers provided.")
    today = datetime.now().date()
    start_date = today - timedelta(days=60)

    news_df = await get_news_df(tickers)
    data = stock_parser.download_custom_data(tickers, start_date, today)
    number_of_news = len(data["Symbol"].value_counts())
    proportion = f"{number_of_news}/{len(tickers)}"
    if number_of_news != len(tickers):
        raise HTTPException(
            status_code=404,
            detail=f"No data available for {proportion} tickers.")
    ticker_data = stock_parser.apply_features_to_stocks(data)
    ticker_data = ticker_data.groupby("Symbol").tail(1)
    grouped_news = news_df.groupby("stocks")
    news_embeddings = news_embedder.calculate_common_embeddings(
        grouped_news['title'].apply(list).tolist()
    )
    column_names = [f'title_embedding_{i}' for i in range(384)]
    news_embeddings = pd.DataFrame(news_embeddings, columns=column_names)
    news_embeddings['Symbol'] = grouped_news.groups.keys()
    ticker_data = ticker_data.join(
        news_embeddings.set_index('Symbol'),
        on='Symbol'
    )
    ticker_data.fillna(0, inplace=True)
    ticker_data.columns = [col.lower() for col in ticker_data.columns]
    weekly_return = regressor.predict(ticker_data)
    zipped_return = zip(ticker_data['symbol'], weekly_return)
    predictions = {ticker: wr for ticker, wr in zipped_return}
    return predictions

def get_news(ticker):
    try:
        ticker = yf.Ticker(ticker)
        news = ticker.get_news()
        return news
    except Exception as e:
        logging.error(f"Error in get_news: {e}")
        return None
    
def get_news_for_tickers(tickers):
    news = {}
    for ticker in tickers:
        news[ticker] = get_news(ticker)
    return news

async def get_news_df(tickers: List[str]):
    news = get_news_for_tickers(tickers)
    news_list = []
    for stock in news:
        for news_item in news[stock]:
            news_list.append({'stocks': stock, 'title': news_item['title']})
    news_df = pd.DataFrame(news_list)
    return news_df

