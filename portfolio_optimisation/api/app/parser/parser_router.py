from fastapi import APIRouter
from typing import List
from datetime import date
from fastapi_cache.decorator import cache

from ..parser.yahoo_parser import SP500Parser


router = APIRouter(prefix="/parser", tags=["Parser"])

parser = SP500Parser()


@router.get("/sp500_tickers")
# @cache(expire=30)
async def get_sp500_tickers():
    """
    Retrieve the list of S&P 500 company tickers.
    """
    data = parser.get_sp500_tickers()
    return data
    

@router.get("/sp500_data")
# @cache(expire=3600)
async def get_sp500_data(start_date: date, end_date: date):
    """
    Download historical data for S&P 500 companies within the specified date range.

    Parameters:
    - start_date (date): The start date for data retrieval. Format: YYYY-MM-DD.
    - end_date (date): The end date for data retrieval. Format: YYYY-MM-DD.

    Returns:
    - dict: A dictionary containing historical data for S&P 500 companies.
    """

    data = parser.download_sp500_data(start_date, end_date)
    return data


@router.post("/custom")
async def get_custom_data(custom_tickers: List[str], start_date: date, end_date: date):
    """
    Download historical data for custom companies within the specified date range.

    Parameters:
    - custom_tickers (List[str]): List of specific tickers to parse.
    - start_date (date): The start date for data retrieval. Format: YYYY-MM-DD.
    - end_date (date): The end date for data retrieval. Format: YYYY-MM-DD.

    Returns:
    - dict: A dictionary containing historical data for custom companies.
    """

    data = parser.download_custom_data(custom_tickers, start_date, end_date)
    return data.to_dict()


@router.post("/download_and_apply_features")
async def download_and_apply_features(
    custom_tickers: List[str], start_date: date, end_date: date
):
    """
    Download stock data for custom companies and apply features.

    Parameters:
    - custom_tickers (List[str]): List of specific tickers to parse.
    - start_date (date): The start date for data retrieval. Format: YYYY-MM-DD.
    - end_date (date): The end date for data retrieval. Format: YYYY-MM-DD.

    Returns:
    - dict: A dictionary containing stock data with applied features.
    """
    stocks = parser.download_custom_data(custom_tickers, start_date, end_date)

    df_stocks = parser.apply_features_to_stocks(stocks)

    return df_stocks.to_dict()
