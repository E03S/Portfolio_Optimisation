import pickle
import requests
import os

import bs4 as bs
import yfinance as yf
import pandas as pd

from typing import List, Optional
from datetime import datetime, date


class SP500Parser:
    def __init__(self) -> None:
        """
        Initializes an instance of the SP500Parser class.
        """
        self.tickers: Optional[List[str]] = None
        self.data: Optional[pd.DataFrame] = None

    def get_sp500_tickers(self) -> Optional[List[str]]:
        """
        Returns the list of S&P 500 company tickers.

        Returns:
        List[str]: A list of S&P 500 company tickers.
        """
        if self.tickers:
            return self.tickers

        resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        table = soup.find('table', {'class': 'wikitable sortable'})
        self.tickers = [row.findAll('td')[0].text.replace('\n', '') for row in table.findAll('tr')[1:]]
        self.tickers.sort()

        return self.tickers

    def save_sp500_tickers(self) -> None:
        """
        Retrieves the list of S&P 500 company tickers from Wiki and saves it to a pickle file.
        """
        if not self.tickers:
            self.get_sp500_tickers()

        data_dir = '../data'

        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        pickle_path = os.path.join(data_dir, 'sp500tickers.pickle')

        with open(pickle_path, 'wb') as f:
            pickle.dump(self.tickers, f)

    def download_sp500_data(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
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

        data = yf.download(self.tickers,
                           start=start_date,
                           end=end_date,
                           interval='1d')

        df = data.stack().reset_index().rename(index=str,
                                               columns={"level_1": "Symbol"}).sort_values(['Symbol',
                                                                                           'Date']).set_index('Date')
        self.data = df
        return self.data
    
    def save_data_to_csv(self, file_name: str) -> None:
        """
        Saves the DataFrame to a CSV file.

        Args:
        file_name (str): The name of the CSV file.
        """
        if self.data is not None:
            self.data.to_csv(file_name)