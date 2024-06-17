import requests
from datetime import date, timedelta

class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def make_api_call(
            self, endpoint, method='GET', params=None, json=None, headers=None, body=None
            ):
        url = self.base_url + endpoint
        response = requests.request(
            method, url, params=params, json=json, headers=headers, data=body
            )
        return response

    def make_prediction(self, ticker):
        response = self.make_api_call(
            '/predictor/predict_weekly_return_batch',
            method='POST',
            json=ticker
        )
        return response.json()

    def make_batch_prediction(self, tickers):
        response = self.make_api_call(
            '/predictor/predict_weekly_return_batch',
            method='POST',
            json=tickers
            )
        return response.json()

    def optimize_portfolio(self, tickers):
        response = self.make_api_call(
            '/portfolio/optimize', method='POST', json=tickers
        )
        return response.json()
    
    def get_today_price(self, tickers):
        today = None
        yesterday = None
        if date.today().isoweekday() == 6:
            today = date.today() - timedelta(days=1)
            yesterday = date.today() - timedelta(days=2)
        elif date.today().isoweekday() == 7 or date.today().isoweekday() == 1):
            today = date.today() - timedelta(days=2)
            yesterday = date.today() - timedelta(days=3)
        else:
            today = date.today()
            yesterday = date.today() - timedelta(days=1)
        today = today.strftime('%Y-%m-%d')
        yesterday = yesterday.strftime('%Y-%m-%d')
        response = self.make_api_call(
            f'/parser/custom?start_date={yesterday}&end_date={today}', method='POST', json=tickers
        )
        return response.json()
