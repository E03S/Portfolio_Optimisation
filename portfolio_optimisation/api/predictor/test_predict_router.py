import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    # Assuming you have a FastAPI app instance
    from ..main import app
    return TestClient(app)


def test_predict_weekly_return_batch(client):
    # Test case 1: Valid input
    tickers = ["AAPL", "GOOGL", "MSFT"]
    response = client.post(
        "/predictor/predict_weekly_return_batch",
        json=tickers
    )
    assert response.status_code == 200
    predictions = response.json()
    assert isinstance(predictions, dict)
    assert len(predictions) == len(tickers)
    for ticker, weekly_return in predictions.items():
        assert isinstance(ticker, str)
        assert isinstance(weekly_return, float)

    # Test case 2: Empty input
    tickers = []
    response = client.post(
        "/predictor/predict_weekly_return_batch",
        json=tickers
    )
    assert response.status_code == 422

    # Test case 3: Invalid input
    tickers = ["AAPL", "GOOGL", "INVALID"]
    response = client.post(
        "/predictor/predict_weekly_return_batch",
        json=tickers
    )
    assert response.status_code == 404
    assert "No data available" in response.json()["detail"]


def test_predict_weekly_return(client):
    # Test case 1: Valid input
    ticker = "AAPL"
    response = client.post(
        f"/predictor/predict_weekly_return?ticker={ticker}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert ticker in data

    # Test case 2: Empty input
    response = client.post("/predictor/predict_weekly_return?ticker=''")
    assert response.status_code == 404
    assert "No data available" in response.json()["detail"]

    # Test case 3: Invalid input
    ticker = "INVALID"
    response = client.post(f"/predictor/predict_weekly_return?ticker={ticker}")
    result = response.json()
    assert response.status_code == 404
    assert 'No data available' in result["detail"]

    # Test case 4: Invalid input
    response = client.post("/predictor/predict_weekly_return")
    result = response.json()
    assert response.status_code == 422
    assert 'Field required' in result["detail"][0]['msg']
