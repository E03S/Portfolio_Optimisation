import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from portfolio_optimisation.api.main import app

    return TestClient(app)


def test_predict_weekly_return_batch(client):
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

    tickers = []
    response = client.post(
        "/predictor/predict_weekly_return_batch",
        json=tickers
    )
    assert response.status_code == 422

    tickers = ["AAPL", "GOOGL", "INVALID"]
    response = client.post(
        "/predictor/predict_weekly_return_batch",
        json=tickers
    )
    assert response.status_code == 404
    assert "No data available" in response.json()["detail"]


def test_predict_weekly_return(client):
    ticker = "AAPL"
    response = client.post(
        f"/predictor/predict_weekly_return?ticker={ticker}"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert ticker in data

    response = client.post("/predictor/predict_weekly_return?ticker=''")
    assert response.status_code == 404
    assert "No data available" in response.json()["detail"]

    ticker = "INVALID"
    response = client.post(f"/predictor/predict_weekly_return?ticker={ticker}")
    result = response.json()
    assert response.status_code == 404
    assert 'No data available' in result["detail"]

    response = client.post("/predictor/predict_weekly_return")
    result = response.json()
    assert response.status_code == 422
    assert 'Field required' in result["detail"][0]['msg']
