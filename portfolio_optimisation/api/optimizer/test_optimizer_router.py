import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    from portfolio_optimisation.api.main import app
    return TestClient(app)

def test_optimize_portfolio(client):
    # Test case 1: Valid input
    tickers = ["AAPL", "GOOGL", "MSFT"]
    response = client.post("/portfolio/optimize", json=tickers)
    result = response.json()
    assert isinstance(result, dict)
    assert len(result) == len(tickers)

    # Test case 2: Empty input
    tickers = []
    response = client.post("/portfolio/optimize", json=tickers)
    result = response.json()
    assert isinstance(result, dict)
    assert "No tickers provided" in result["detail"]

    # Test case 3: Invalid input
    tickers = ["AAPL", "GOOGL", "INVALID"]
    response = client.post("/portfolio/optimize", json=tickers)
    result = response.json()
    assert isinstance(result, dict)
    assert 'No data available for 2/3 tickers.' in result["detail"]