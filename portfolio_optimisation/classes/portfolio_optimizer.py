import yfinance as yf
from pypfopt.expected_returns import ema_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from datetime import datetime

class PortfolioOptimizer:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.daily_prices = None
        self.weekly_prices = None
        self.expected_weekly_returns = None
        self.covariance_matrix = None

    def fetch_daily_data(self):
        """Fetches daily price data for the tickers."""
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date)
        self.daily_prices = data['Adj Close']

    def convert_to_weekly(self):
        """Converts daily price data to weekly."""
        self.weekly_prices = self.daily_prices.resample('W').last()

    def calculate_weekly_ewma_returns(self, span=52):
        """Calculates expected weekly returns using EWMA."""
        print(self.weekly_prices)
        self.expected_weekly_returns = ema_historical_return(self.weekly_prices, span=span)

    def calculate_covariance_matrix(self):
        """Calculates the covariance matrix for the weekly returns."""
        self.covariance_matrix = CovarianceShrinkage(self.weekly_prices).ledoit_wolf()

    def optimize_portfolio(self):
        """Optimizes the portfolio to find the optimal weights."""
        print(self.expected_weekly_returns)
        ef = EfficientFrontier(self.expected_weekly_returns, self.covariance_matrix)
        weights = ef.max_sharpe()
        cleaned_weights = ef.clean_weights()
        return cleaned_weights

    def run_optimization(self):
        """Runs the full optimization process."""
        self.fetch_daily_data()
        self.convert_to_weekly()
        self.calculate_weekly_ewma_returns()
        self.calculate_covariance_matrix()
        return self.optimize_portfolio()

# Example usage
if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'BRK-B', 'JPM', 'JNJ', 'V']
    start_date = '2020-01-01'
    today = datetime.today().strftime('%Y-%m-%d')
    end_date = today
    optimizer = PortfolioOptimizer(tickers, start_date, end_date)
    optimal_weights = optimizer.run_optimization()
    print("Optimal Portfolio Weights:", optimal_weights)
