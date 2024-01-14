import warnings

import riskfolio as rp

from datetime import datetime, timedelta
from typing import Dict, Optional

from yahoo_parser import SP500Parser

warnings.filterwarnings("ignore")
yahoo_parser = SP500Parser()


class PortfolioOptimizer:
    def __init__(self, current_portfolio: Dict[str, float]) -> None:
        """
        Initializes an instance of the PortfolioOptimizer class.
        """
        self.current_portfolio = current_portfolio
        self.optimized_portfolio: Optional[Dict[str, float]] = None

    def optimise(self) -> Dict[str, float]:
        """
        Optimize the current portfolio using historical data.

        Parameters:
        - current_portfolio: Dictionary containing the current portfolio weights.

        Returns:
        - Dict[str, float]: Optimized portfolio weights.
        """
        end = datetime.now()
        start = end - timedelta(days=5)

        tickers = list(self.current_portfolio.keys())
        df = yahoo_parser.download_custom_data(tickers, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
        df_pivoted = df.loc[:, ['Symbol', 'Adj Close']].pivot(columns="Symbol", values="Adj Close")
        portfolio_change = df_pivoted.pct_change().dropna()
        port = rp.Portfolio(returns=portfolio_change)

        method_mu = 'hist'  # Method to estimate expected returns based on historical data.
        method_cov = 'hist'  # Method to estimate covariance matrix based on historical data.

        port.assets_stats(method_mu=method_mu, method_cov=method_cov, d=0.94)

        # Estimate optimal portfolio:
        model = 'Classic'  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
        rm = 'MV'  # Risk measure used, this time will be variance
        obj = 'Sharpe'  # Objective function, could be MinRisk, MaxRet, Utility, or Sharpe
        hist = True  # Use historical scenarios for risk measures that depend on scenarios
        rf = 0  # Risk-free rate
        l = 0  # Risk aversion factor, only useful when obj is 'Utility'

        optimised_weights = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
        output_dict = optimised_weights.to_dict()['weights']

        self.optimized_portfolio = output_dict  # Save the optimized portfolio
        return output_dict
