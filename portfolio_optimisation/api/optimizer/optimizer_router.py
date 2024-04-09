from fastapi import APIRouter
from typing import List
from datetime import date
from fastapi_cache.decorator import cache

from ...classes.portfolio_optimizer import PortfolioOptimizer
from ..predictor.predict_router import predict_weekly_return_batch
router = APIRouter(prefix="/portfolio", tags=["Parser"])
from fastapi import HTTPException
@router.post("/optimize")
async def optimize_portfolio(tickers: List[str]):
    """
    Optimize the portfolio for a given list of tickers.

    Parameters:
    - tickers (List[str]): List of ticker symbols of the stocks.

    Returns:
    - dict: A dictionary containing the optimized portfolio.
    """
    if not tickers:
        raise HTTPException(status_code=422, detail="No tickers provided.")
    today = date.today()
    start_date = '2022-01-01'
    optimizer = PortfolioOptimizer(tickers, start_date, today.strftime('%Y-%m-%d'))
    optimizer.initialize()
    weekly_return = await predict_weekly_return_batch(tickers)
    sorted_values = [weekly_return[key] for key in sorted(weekly_return)]
    return optimizer.run_optimization(sorted_values)