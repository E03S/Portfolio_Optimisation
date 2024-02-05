import pandas as pd

from benzinga import news_data
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

import warnings

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning, module='bs4')


class BenzingaParser:
    def __init__(self, api_key, log=False):
        self.paper = news_data.News(api_key, log=log)

    @staticmethod
    def remove_html_tags(self, text):
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

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
            return []
        df = pd.DataFrame(news)
        df['teaser'] = df['teaser'].apply(self.remove_html_tags)
        df['body'] = df['body'].apply(self.remove_html_tags)
        return df
