import requests

import bs4 as bs
import yfinance as yf
import pandas as pd

from ta.trend import MACD
from typing import List, Optional
from datetime import datetime


class SP500Parser:
    def __init__(self) -> None:
        """
        Initializes an instance of the SP500Parser class.
        """
        self.tickers: Optional[List[str]] = None
        self.data: Optional[pd.DataFrame] = None
        self.cat_features = ["Symbol", "week_of_year", "month"]

    def get_sp500_tickers(self) -> Optional[List[str]]:
        """
        Returns the list of S&P 500 company tickers.

        Returns:
        List[str]: A list of S&P 500 company tickers.
        """
        if self.tickers:
            return self.tickers

        resp = requests.get("http://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
        soup = bs.BeautifulSoup(resp.text, "lxml")
        table = soup.find("table", {"class": "wikitable sortable"})
        self.tickers = [
            row.findAll("td")[0].text.replace("\n", "")
            for row in table.findAll("tr")[1:]
        ]
        self.tickers.sort()
        return self.tickers

    def download_sp500_data(
        self, start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Downloads historical data for S&P 500 companies within the specified date range with 1 day granularity.
        Args:
            start_date (datetime): The start date for data retrieval.
            end_date (datetime): The end date for data retrieval.
        Returns:
            pd.DataFrame: A DataFrame containing historical data for S&P 500 companies.
        """
        if not self.tickers:
            self.get_sp500_tickers()

        data = yf.download(self.tickers, start=start_date, end=end_date, interval="1d")
        df = (
            data.stack()
            .reset_index()
            .rename(index=str, columns={"level_1": "Symbol"})
            .sort_values(["Ticker", "Date"])
            .set_index("Date")
        )
        df.reset_index(inplace=True)
        self.data = df
        return self.data

    def download_custom_data(
        self, custom_tickers: List[str], start_date: datetime, end_date: datetime
    ) -> pd.DataFrame:
        """
        Downloads historical data for custom companies within the specified date range with 1 day granularity.
        Args:
            custom_tickers (List[str]): List of specific tickers to parse.
            start_date (datetime): The start date for data retrieval.
            end_date (datetime): The end date for data retrieval.
        Returns:
            pd.DataFrame: A DataFrame containing historical data for S&P 500 companies.
        """
        data = yf.download(
            custom_tickers, start=start_date, end=end_date, interval="1d"
        )
        if len(custom_tickers) > 1:
            data = (
                data.stack()
                .reset_index()
                .rename(index=str, columns={"level_1": "Symbol"})
                .sort_values(["Ticker", "Date"])
                .set_index("Date")
            )
        else:
            data["Symbol"] = custom_tickers[0]
        data.reset_index(inplace=True)
        self.data = data
        return data

    @staticmethod
    def apply_features(group):
        group.index = pd.to_datetime(group.index)

        for lag in range(1, 4):
            group[f"lag_{lag}"] = group["Close"].shift(lag)

        group["5_day_MA"] = group["Close"].rolling(window=5).mean()
        group["20_day_MA"] = group["Close"].rolling(window=20).mean()
        group["5_day_volatility"] = group["Close"].rolling(window=5).std()
        group["momentum"] = group["Close"] - group["Close"].shift(1)
        macd = MACD(close=group["Close"], window_slow=26, window_fast=12, window_sign=9)
        group["MACD"] = macd.macd()
        group["MACD_signal"] = macd.macd_signal()
        group["MACD_histogram"] = macd.macd_diff()
        group["week_of_year"] = group.index.isocalendar().week
        group["month"] = group.index.month
        return group.dropna()

    def apply_features_to_stocks(self, stocks):
        df_stocks = stocks.groupby("Symbol").apply(self.apply_features)
        df_stocks.index = df_stocks.index.droplevel()
        df_stocks.reset_index(inplace=True)
        return df_stocks


if __name__ == "__main__":
    parser = SP500Parser()
