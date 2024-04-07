from datetime import datetime
import concurrent.futures
import warnings
from typing import List, Optional
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
import pandas as pd
from benzinga import news_data

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

class BenzingaNewsParser:
    def __init__(
        self,
        api_key: str,
        tickers: List[str] = None,
        start_date: str = None,
        end_date: str = None,
        log: bool = False,
    ):
        self.paper = news_data.News(api_key, log=log)
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.main_df = pd.DataFrame()

    @staticmethod
    def remove_html_tags(text: str) -> str:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def get_ticker_news(self, ticker: str, page: int, date_from: str) -> Optional[pd.DataFrame]:
        try:
            if not isinstance(ticker, str):
                ticker = ",".join(ticker)
            news = self.paper.news(
                company_tickers=ticker,
                display_output="full",
                date_from=date_from,
                date_to=self.end_date,
                page=page,
                pagesize=100,
            )
            if len(news) == 0:
                return None
            df = pd.DataFrame(news)
            df["teaser"] = df["teaser"].apply(self.remove_html_tags)
            df["body"] = df["body"].apply(self.remove_html_tags)
            return df
        except Exception as e:
            print(e)

    def get_df_news(self) -> pd.DataFrame:
        if self.main_df is None:
            self.run_concurrent()
        
        return self.main_df

    def save_dataset(self, filename: str = "datasets/news_sp_500.csv") -> None:
        self.main_df.to_csv(filename, index=False)

    def run_concurrent(self, max_workers: int = 10) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.fetch_ticker_news, ticker) for ticker in self.tickers
            ]
            for future in concurrent.futures.as_completed(futures):
                news_df = future.result()
                if news_df is not None:                    
                    self.main_df = pd.concat([self.main_df, news_df], ignore_index=True)
                    self.main_df = self.main_df.drop_duplicates(subset=["id"])

        self.main_df["stocks"] = self.main_df["stocks"].apply(lambda x: [entry["name"] for entry in x])
        self.main_df = self.main_df.explode("stocks")
        self.main_df["updated"] = pd.to_datetime(pd.to_datetime(self.main_df["updated"]).dt.strftime('%Y-%m-%d'))
        self.main_df = self.main_df[self.main_df['body'] != '']

    def fetch_ticker_news(self, ticker: str) -> Optional[pd.DataFrame]:
        page = 0
        date_from = self.start_date
        total_pages = 100
        main_df = pd.DataFrame()
        while page < total_pages:
            news_df = self.get_ticker_news(ticker, page, date_from)
            if news_df is None:
                break
            main_df = pd.concat([main_df, news_df], ignore_index=True)
            main_df = main_df.drop_duplicates(subset=["id"])
            page += 1
            if page > 100:  # Update date_from when page exceeds 100
                date_from = datetime.strptime(main_df['updated'].iloc[-1], "%a, %d %b %Y %H:%M:%S %z").strftime('%Y-%m-%d')
                page = 0
        return main_df

    def get_news(self, ticker, page, date_from, date_to, display_output="full"):
        if not isinstance(ticker, str):
            ticker = ",".join(ticker)
        news = self.paper.news(company_tickers=ticker,
                               display_output=display_output,
                               date_from=date_from,
                               date_to=date_to,
                               page=page,
                               pagesize=100)
        if len(news) == 0:
            return pd.DataFrame(columns=['id', 'title', 'teaser', 'body', 'author', 'source', 'updated', 'stocks'])
        df = pd.DataFrame(news)
        df['teaser'] = df['teaser'].apply(self.remove_html_tags)
        df['body'] = df['body'].apply(self.remove_html_tags)
        return df

if __name__ == "__main__":
    # Example usage:
    tickers = ["AAPL", "GOOGL", "MSFT"]  # Example list of tickers
    start_date = "2024-01-01"  # Example start date
    end_date = "2024-03-01"  # Example end date
    api_key = "d2d497c85f47496884ab3a91327a090f"  # Replace with your actual API key

    benzinga_fetcher = BenzingaNewsParser(api_key, tickers, start_date, end_date)
    benzinga_fetcher.run_concurrent()
    print(benzinga_fetcher.get_df_news().head().dtypes)
